"""Job description endpoints: config, questions, generate, refine, edits, upload.

Billing rule: only `/refine` (typed feedback) costs a credit. Generating,
one-click edits, section rewrites, quality checks, screening questions and
uploads are free and open to guests, protected by Turnstile, a per-IP daily
limit and a global daily cap instead of credits.
"""

import os
from collections.abc import Iterator

from fastapi import APIRouter, Depends, File, Header, HTTPException, Request, UploadFile
from fastapi.responses import StreamingResponse

from src.agent.job_agent import JobAgent
from src.agent.prompts import QUICK_ACTIONS, SECTION_LABELS
from src.api.dependencies import get_optional_user_id_from_auth, get_user_id_from_auth
from src.api.schemas import (
    EventRequest,
    GenerateRequest,
    QualityRequest,
    QuestionResponse,
    QuickEditRequest,
    RefineRequest,
    ScreeningRequest,
    SectionRequest,
)
from src.api.services import (
    MAX_UPLOAD_BYTES,
    build_quality_report,
    extract_job_info_from_doc,
    list_questions,
    quick_edit_job_description,
    regenerate_section_job_description,
    stream_generate_job_description,
    stream_refine_job_description,
    to_sse,
)
from src.credits import ledger
from src.credits.packs import CREDIT_PACKS, FREE_SIGNUP_CREDITS, REFINE_COST
from src.database.supabase_client import supabase
from src.database.supabase_credits import get_supabase_credits
from src.quality.jurisdictions import JURISDICTIONS
from src.security.limits import (
    GUEST_DAILY_LIMIT,
    check_global_cap,
    check_guest_limit,
    check_user_limit,
    client_ip,
)
from src.security.turnstile import turnstile_enabled, verify_turnstile

router = APIRouter()

ALLOWED_UPLOAD_EXTENSIONS = (".pdf", ".docx", ".doc", ".txt", ".md")
SSE_HEADERS = {"Cache-Control": "no-cache", "Connection": "keep-alive"}
ALLOWED_EVENTS = {"quick_action", "section_regen", "refine_click", "pack_view", "pack_click", "export", "upload"}
MAX_REFINE_CHARS = 2000


def _sse_response(event_stream: Iterator[str]) -> StreamingResponse:
    """Wraps an event iterator in a Server-Sent Events response."""
    return StreamingResponse(
        event_stream,
        media_type="text/event-stream",
        headers=SSE_HEADERS,
    )


def _guard_free_llm_call(request: Request, user_id: str | None, turnstile_token: str | None) -> None:
    """Applies abuse protection to a free LLM endpoint.

    Signed-in users get a per-user hourly limit. Guests must pass Turnstile
    and are limited per IP per day. Everyone counts against the global cap.

    Raises:
        HTTPException: 400/429/503 when a check fails.
    """
    if user_id:
        check_user_limit(user_id)
    else:
        verify_turnstile(turnstile_token, client_ip(request))
        check_guest_limit(request)
    check_global_cap()


@router.api_route("/health", methods=["GET", "HEAD"])
def health():
    """Reports service status and whether the database is reachable."""
    try:
        supabase.table("profiles").select("id").limit(1).execute()
        return {"status": "ok", "database": "connected"}
    except Exception as error:
        return {"status": "ok", "database_error": str(error)}


@router.get("/config")
def get_config():
    """Returns public settings the front end needs (packs, limits, rules)."""
    return {
        "free_signup_credits": FREE_SIGNUP_CREDITS,
        "refine_cost": REFINE_COST,
        "guest_daily_limit": GUEST_DAILY_LIMIT,
        "turnstile_site_key": os.getenv("TURNSTILE_SITE_KEY", "") if turnstile_enabled() else "",
        "packs": [pack.model_dump() for pack in CREDIT_PACKS],
        "quick_actions": list(QUICK_ACTIONS),
        "sections": list(SECTION_LABELS),
        "jurisdictions": [item.model_dump() for item in JURISDICTIONS],
    }


@router.get("/questions", response_model=list[QuestionResponse])
def get_questions():
    """Returns the intake questions."""
    return list_questions()


@router.post("/generate")
def generate(
    payload: GenerateRequest,
    request: Request,
    user_id: str | None = Depends(get_optional_user_id_from_auth),
    x_turnstile_token: str | None = Header(default=None),
):
    """Streams a generated job description as Server-Sent Events.

    Free for everyone, with no account needed. The final "done" event holds
    the full draft, its Markdown and a quality report.

    Args:
        payload: Generation parameters.
        request: Incoming request (used for the client IP).
        user_id: ID of the signed-in user, or None for guests.
        x_turnstile_token: Turnstile token (guests only, when enabled).

    Raises:
        HTTPException: 400 for a failed human check, 429/503 for limits.
    """
    _guard_free_llm_call(request, user_id, x_turnstile_token)

    def event_stream() -> Iterator[str]:
        try:
            for event in stream_generate_job_description(payload):
                if event.get("event") == "done" and user_id:
                    event["credits_remaining"] = _balance(user_id)
                yield to_sse(event)
        except Exception as exc:
            yield to_sse({"event": "error", "detail": _public_error(exc)})

    return _sse_response(event_stream())


def _balance(user_id: str) -> int | None:
    """Returns the user balance, or None if it cannot be read."""
    try:
        return get_supabase_credits(user_id)
    except Exception:
        return None


def _refund_quietly(user_id: str, request_key: str) -> int | None:
    """Refunds a refine charge, returning the new balance (None on failure)."""
    try:
        return ledger.refund(user_id, REFINE_COST, request_key)
    except Exception:
        return None


def _public_error(exc: Exception) -> str:
    """Returns an error text that is safe to show to users."""
    if isinstance(exc, ValueError):
        return "The AI returned an unreadable draft. Please try again."
    return "Something went wrong while generating. Please try again."


def _refine_event_stream(
    payload: RefineRequest, user_id: str, request_key: str, balance: int
) -> Iterator[str]:
    """Streams a paid refine and refunds the credit only for real failures.

    A refund is given when the AI call fails or returns an unreadable draft.
    If the client disconnects, the credit is refunded only when no text was
    sent yet. Once chunks went out the user already received the paid output,
    so a disconnect must not be a way to get free refines.
    """
    succeeded = False
    sent_any = False
    try:
        for event in stream_refine_job_description(payload):
            if event.get("event") == "done":
                succeeded = True
                event["credits_remaining"] = balance
            if event.get("event") == "chunk":
                sent_any = True  # set before yielding: the client may leave right after receiving it
            yield to_sse(event)
    except GeneratorExit:
        if not succeeded and not sent_any:
            _refund_quietly(user_id, request_key)
        raise
    except Exception as exc:
        yield to_sse({"event": "error", "detail": f"{_public_error(exc)} Your credit was refunded."})
    if not succeeded:
        remaining = _refund_quietly(user_id, request_key)
        yield to_sse({"event": "refunded", "credits_remaining": remaining if remaining is not None else balance})


@router.post("/refine")
def refine(
    payload: RefineRequest,
    user_id: str = Depends(get_user_id_from_auth),
):
    """Streams a refined job description from typed feedback (costs 1 credit).

    The credit is charged up front and refunded automatically if the AI
    call fails, times out or returns an unreadable draft.

    Args:
        payload: Refinement parameters.
        user_id: ID of the signed-in user.

    Raises:
        HTTPException: 402 if the user has no credits, 422 for blank or
            oversized feedback, 429/503 for limits.
    """
    text = payload.user_request.strip()
    if not text:
        raise HTTPException(status_code=422, detail="user_request is required")
    if len(text) > MAX_REFINE_CHARS:
        raise HTTPException(status_code=422, detail=f"Feedback is too long (max {MAX_REFINE_CHARS} characters).")
    check_user_limit(user_id)
    check_global_cap()

    request_key = ledger.new_request_key()
    balance = ledger.spend(user_id, REFINE_COST, request_key)
    if balance == ledger.INSUFFICIENT:
        raise HTTPException(status_code=402, detail="Insufficient credits.")

    return _sse_response(_refine_event_stream(payload, user_id, request_key, balance))


@router.post("/quick-edit")
def quick_edit(
    payload: QuickEditRequest,
    request: Request,
    user_id: str | None = Depends(get_optional_user_id_from_auth),
    x_turnstile_token: str | None = Header(default=None),
):
    """Applies a one-click edit such as "shorter" or "more inclusive" (free)."""
    if payload.action not in QUICK_ACTIONS:
        raise HTTPException(status_code=422, detail="Unknown action")
    _guard_free_llm_call(request, user_id, x_turnstile_token)
    try:
        return quick_edit_job_description(
            payload.company_name, payload.current_draft, payload.action,
            payload.skipped_fields, payload.job_info, payload.provider, payload.model,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=_public_error(exc))


@router.post("/regenerate-section")
def regenerate_section(
    payload: SectionRequest,
    request: Request,
    user_id: str | None = Depends(get_optional_user_id_from_auth),
    x_turnstile_token: str | None = Header(default=None),
):
    """Rewrites one section and keeps the rest of the draft as is (free)."""
    if payload.section not in SECTION_LABELS:
        raise HTTPException(status_code=422, detail="Unknown section")
    _guard_free_llm_call(request, user_id, x_turnstile_token)
    try:
        return regenerate_section_job_description(
            payload.company_name, payload.current_draft, payload.section,
            payload.skipped_fields, payload.job_info, payload.provider, payload.model,
        )
    except Exception as exc:
        raise HTTPException(status_code=502, detail=_public_error(exc))


@router.post("/quality")
def quality(payload: QualityRequest):
    """Lints a draft with rule-based checks. No AI call, so it is always free."""
    report = build_quality_report(payload.draft.model_dump(), payload.job_info)
    return report.model_dump()


@router.post("/screening-questions")
def screening_questions(
    payload: ScreeningRequest,
    request: Request,
    user_id: str | None = Depends(get_optional_user_id_from_auth),
    x_turnstile_token: str | None = Header(default=None),
):
    """Suggests screening questions for the role (free)."""
    _guard_free_llm_call(request, user_id, x_turnstile_token)
    try:
        questions = JobAgent().screening_questions(payload.current_draft, payload.provider, payload.model)
        return {"questions": questions}
    except Exception as exc:
        raise HTTPException(status_code=502, detail=_public_error(exc))


@router.post("/events", status_code=204)
def log_event(payload: EventRequest):
    """Records which feature was used (button name only, no personal data)."""
    if payload.event not in ALLOWED_EVENTS:
        return
    try:
        supabase.table("usage_events").insert(
            {"event": payload.event, "detail": payload.detail[:60]}
        ).execute()
    except Exception:
        pass


@router.post("/api/extract-doc")
async def extract_doc(
    request: Request,
    file: UploadFile = File(...),
    user_id: str | None = Depends(get_optional_user_id_from_auth),
    x_turnstile_token: str | None = Header(default=None),
):
    """Extracts intake answers from an uploaded hiring document (free).

    Args:
        request: Incoming request (used for the client IP).
        file: Uploaded PDF, Word, text or Markdown file.
        user_id: ID of the signed-in user, or None for guests.
        x_turnstile_token: Turnstile token (guests only, when enabled).

    Returns:
        `{"status": "success", "data": {...}, "original_text": "..."}`.

    Raises:
        HTTPException: 400 for unsupported, empty or oversized files,
            429/503 for limits, 500 if extraction fails.
    """
    filename = file.filename or ""
    if not filename.lower().endswith(ALLOWED_UPLOAD_EXTENSIONS):
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Please upload one of: {', '.join(ALLOWED_UPLOAD_EXTENSIONS)}",
        )

    file_bytes = await file.read(MAX_UPLOAD_BYTES + 1)
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")
    if len(file_bytes) > MAX_UPLOAD_BYTES:
        raise HTTPException(status_code=400, detail="File is too large (max 5 MB).")

    _guard_free_llm_call(request, user_id, x_turnstile_token)
    try:
        result = extract_job_info_from_doc(file_bytes, filename)
        return {"status": "success", "data": result["data"], "original_text": result["original_text"]}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to extract the document. Please try another file.")
