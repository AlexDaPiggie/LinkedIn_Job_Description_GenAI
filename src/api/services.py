"""Business logic behind the job description endpoints."""

import hashlib
import json
import threading
from collections import OrderedDict
from collections.abc import Iterator

from src.agent.doc_parser import extract_text_from_file
from src.agent.job_agent import JobAgent
from src.agent.parser import parse_extracted_doc
from src.agent.prompts import build_extraction_prompt, sanitize_document_text
from src.agent.questions import QUESTIONS
from src.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    QuestionResponse,
    RefineRequest,
)
from src.llm.client import generate_text
from src.llm.models import MODEL_FALLBACKS
from src.quality import QualityReport, lint_job_description
from src.quality.jurisdictions import pay_required_for
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo

EXTRACTION_MODEL = "google/gemini-2.5-flash-lite"
EXTRACTION_DEFAULT_FALLBACKS = ["openai/gpt-4o-mini"]
MAX_UPLOAD_BYTES = 5 * 1024 * 1024
CACHE_MAX_ENTRIES = 200

_cache: "OrderedDict[str, dict]" = OrderedDict()
_cache_lock = threading.Lock()


def list_questions() -> list[QuestionResponse]:
    """Returns every intake question in display order."""
    return [
        QuestionResponse(
            question_name=question.question_name,
            question_text=question.question_text,
            required=question.required,
            answer_type=question.answer_type,
            recommended=question.recommended,
        )
        for question in QUESTIONS
    ]


def build_quality_report(draft: dict, job_info: JobInfo | dict) -> QualityReport:
    """Lints a draft using the user's pay and location answers.

    Args:
        draft: Draft as a dict.
        job_info: Intake answers (model or dict).

    Returns:
        The quality report.
    """
    info = job_info.model_dump() if isinstance(job_info, JobInfo) else job_info
    required = pay_required_for(info.get("jurisdiction", "none"))
    return lint_job_description(draft, info, pay_required=required)


def _cache_key(request: GenerateRequest) -> str:
    """Hashes a generate request so identical requests can share a result."""
    payload = json.dumps(
        [request.job_info.model_dump(), sorted(request.skipped_fields), request.model],
        sort_keys=True,
    )
    return hashlib.sha256(payload.encode()).hexdigest()


def _cache_get(key: str) -> dict | None:
    """Returns a cached done-event (a copy), refreshing its recency."""
    with _cache_lock:
        event = _cache.get(key)
        if event is not None:
            _cache.move_to_end(key)
            return json.loads(json.dumps(event))
    return None


def _cache_put(key: str, event: dict) -> None:
    """Stores a done-event, evicting the oldest when full."""
    with _cache_lock:
        _cache[key] = json.loads(json.dumps(event))
        _cache.move_to_end(key)
        while len(_cache) > CACHE_MAX_ENTRIES:
            _cache.popitem(last=False)


def clear_cache() -> None:
    """Empties the response cache (used by tests)."""
    with _cache_lock:
        _cache.clear()


def generate_job_description(request: GenerateRequest) -> GenerateResponse:
    """Generates a job description in one blocking call.

    Args:
        request: Generation parameters.

    Returns:
        The draft and its Markdown.
    """
    result = JobAgent().generate_draft(
        request.job_info,
        request.provider,
        request.model,
        skipped_fields=request.skipped_fields,
    )
    return GenerateResponse(draft=result.draft, markdown=result.markdown)


def refine_job_description(request: RefineRequest) -> GenerateResponse:
    """Refines a job description in one blocking call.

    Args:
        request: Refinement parameters.

    Returns:
        The revised draft and its Markdown.
    """
    result = JobAgent().refine_draft(
        request.company_name,
        request.current_draft,
        request.user_request,
        request.provider,
        request.model,
        request.skipped_fields,
    )
    return GenerateResponse(draft=result.draft, markdown=result.markdown)


def stream_generate_job_description(request: GenerateRequest) -> Iterator[dict]:
    """Streams a job description generation.

    Identical requests are answered from a small in-memory cache without
    calling the LLM.

    Args:
        request: Generation parameters.

    Yields:
        "chunk" events, then a "done" event holding the draft, Markdown and
        a quality report.
    """
    key = _cache_key(request)
    cached = _cache_get(key)
    if cached is not None:
        cached["cached"] = True
        yield cached
        return

    agent = JobAgent()
    for event in agent.stream_generate_draft(
        job_info=request.job_info,
        provider=request.provider,
        model=request.model,
        skipped_fields=request.skipped_fields,
    ):
        if event.get("event") == "done":
            event["quality"] = build_quality_report(event["draft"], request.job_info).model_dump()
            _cache_put(key, event)
        yield event


def stream_refine_job_description(request: RefineRequest) -> Iterator[dict]:
    """Streams a refinement of a job description from typed feedback.

    Args:
        request: Refinement parameters.

    Yields:
        "chunk" events, then a "done" event with the revised draft,
        Markdown and a quality report.
    """
    agent = JobAgent()
    for event in agent.stream_refine_draft(
        company_name=request.company_name,
        current_draft=request.current_draft,
        user_request=request.user_request,
        provider=request.provider,
        model=request.model,
        skipped_fields=request.skipped_fields,
    ):
        if event.get("event") == "done":
            event["quality"] = build_quality_report(event["draft"], request.job_info or {}).model_dump()
        yield event


def quick_edit_job_description(
    company_name: str,
    draft: JobDescriptionDraft,
    action: str,
    skipped_fields: list[str],
    job_info: dict,
    provider: str,
    model: str,
) -> dict:
    """Applies a one-click edit and returns the new draft with its report.

    Returns:
        A dict with `draft`, `markdown` and `quality`.

    Raises:
        ValueError: If the action is unknown or the output is invalid.
    """
    result = JobAgent().quick_edit(company_name, draft, action, provider, model, skipped_fields)
    return {
        "draft": result.draft.model_dump(),
        "markdown": result.markdown,
        "quality": build_quality_report(result.draft.model_dump(), job_info).model_dump(),
    }


def regenerate_section_job_description(
    company_name: str,
    draft: JobDescriptionDraft,
    section: str,
    skipped_fields: list[str],
    job_info: dict,
    provider: str,
    model: str,
) -> dict:
    """Rewrites one section and returns the new draft with its report.

    Returns:
        A dict with `draft`, `markdown` and `quality`.

    Raises:
        ValueError: If the section is unknown or the output is invalid.
    """
    result = JobAgent().regenerate_section(company_name, draft, section, provider, model, skipped_fields)
    return {
        "draft": result.draft.model_dump(),
        "markdown": result.markdown,
        "quality": build_quality_report(result.draft.model_dump(), job_info).model_dump(),
    }


def to_sse(event: dict) -> str:
    """Formats an event as a Server-Sent Events `data:` message.

    Args:
        event: JSON-serializable event.

    Returns:
        The encoded message including the trailing blank line.
    """
    return f"data: {json.dumps(event)}\n\n"


def extract_job_info_from_doc(file_bytes: bytes, filename: str) -> dict:
    """Extracts intake answers from an uploaded hiring document.

    Args:
        file_bytes: Raw bytes of the uploaded file.
        filename: Original file name, used to detect the file type.

    Returns:
        `{"data": {...}, "original_text": str}` with the extracted
        `JobInfo`-style fields and the (capped) text of the document.

    Raises:
        ValueError: If the document is empty or the LLM output is invalid.
    """
    document_text = extract_text_from_file(file_bytes, filename)
    if not document_text.strip():
        raise ValueError("The uploaded document is empty or could not be read.")

    prompt = build_extraction_prompt(document_text)
    fallback_models = MODEL_FALLBACKS.get(EXTRACTION_MODEL, EXTRACTION_DEFAULT_FALLBACKS)
    result = generate_text(
        prompt,
        "openrouter",
        EXTRACTION_MODEL,
        fallback_models=fallback_models,
    )
    return {
        "data": _clean_extracted(parse_extracted_doc(result.text)),
        "original_text": sanitize_document_text(document_text),
    }


def _clean_extracted(data: dict) -> dict:
    """Keeps only known `JobInfo` fields with sane types.

    Guards against a hostile document steering the model into returning
    unexpected keys or huge values.
    """
    allowed = {
        "company_name", "role_title", "role_summary", "responsibilities", "requirements",
        "nice_to_haves", "company_description", "why_join_us", "benefits",
        "team_context", "equal_opportunity", "pay_min", "pay_max",
    }
    list_fields = {"responsibilities", "requirements", "nice_to_haves", "benefits"}
    number_fields = {"pay_min", "pay_max"}
    cleaned: dict = {}
    for key, value in data.items():
        if key not in allowed:
            continue
        if key in list_fields:
            if isinstance(value, list):
                cleaned[key] = [str(item)[:500] for item in value[:30]]
        elif key in number_fields:
            if isinstance(value, (int, float)) and not isinstance(value, bool) and value >= 0:
                cleaned[key] = value
        elif isinstance(value, str):
            cleaned[key] = value[:2000]
    return cleaned
