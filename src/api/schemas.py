"""Request and response models for the HTTP API."""

import json
from pathlib import Path

from pydantic import BaseModel, Field

from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config.json"
FALLBACK_PROVIDER = "openai"
FALLBACK_MODEL = "gpt-4o"


def _load_default_llm() -> tuple[str, str]:
    """Reads the default LLM provider and model from `src/config.json`.

    Returns:
        A `(provider, model)` tuple. Falls back to built-in defaults (and
        prints a warning) if the file is missing or unreadable.
    """
    try:
        with open(CONFIG_PATH, "r") as config_file:
            config = json.load(config_file)
        return config.get("LLM_PROVIDER"), config.get("LLM_MODEL")
    except Exception as error:
        print(f"Warning: Could not load config.json. Using defaults. Error: {error}")
        return FALLBACK_PROVIDER, FALLBACK_MODEL


DEFAULT_PROVIDER, DEFAULT_MODEL = _load_default_llm()


class QuestionResponse(BaseModel):
    """An intake question as exposed by the API."""

    question_name: str
    question_text: str
    required: bool
    answer_type: str
    recommended: bool = False


class GenerateRequest(BaseModel):
    """Request body for generating a job description.

    Attributes:
        job_info: Hiring details supplied by the user.
        skipped_fields: Fields the user chose to skip.
        provider: LLM provider name.
        model: Model identifier.
    """

    job_info: JobInfo
    skipped_fields: list[str] = Field(default_factory=list)
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


class GenerateResponse(BaseModel):
    """A generated job description.

    Attributes:
        draft: The structured draft.
        markdown: The draft rendered as Markdown.
        credits_remaining: Credits left for the user, if known.
    """

    draft: JobDescriptionDraft
    markdown: str
    credits_remaining: int | None = None


class RefineRequest(BaseModel):
    """Request body for refining an existing draft.

    Attributes:
        company_name: Name of the hiring company.
        current_draft: Draft to revise.
        user_request: Free-text change requested by the user.
        skipped_fields: Fields the user chose to skip.
        provider: LLM provider name.
        model: Model identifier.
    """

    company_name: str
    current_draft: JobDescriptionDraft
    user_request: str
    skipped_fields: list[str] = Field(default_factory=list)
    job_info: dict | None = None
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


class QuickEditRequest(BaseModel):
    """Request body for a one-click edit (free, no typed text).

    Attributes:
        company_name: Name of the hiring company.
        current_draft: Draft to revise.
        action: Key of a fixed quick action (e.g. "shorter").
        skipped_fields: Fields the user chose to skip.
        job_info: Intake answers, used for the quality report.
    """

    company_name: str = ""
    current_draft: JobDescriptionDraft
    action: str
    skipped_fields: list[str] = Field(default_factory=list)
    job_info: dict = Field(default_factory=dict)
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


class SectionRequest(BaseModel):
    """Request body for rewriting one section (free, no typed text)."""

    company_name: str = ""
    current_draft: JobDescriptionDraft
    section: str
    skipped_fields: list[str] = Field(default_factory=list)
    job_info: dict = Field(default_factory=dict)
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


class QualityRequest(BaseModel):
    """Request body for linting a draft (for example after manual edits)."""

    draft: JobDescriptionDraft
    job_info: dict = Field(default_factory=dict)


class ScreeningRequest(BaseModel):
    """Request body for suggesting screening questions."""

    current_draft: JobDescriptionDraft
    provider: str = DEFAULT_PROVIDER
    model: str = DEFAULT_MODEL


class EventRequest(BaseModel):
    """A usage event (which button was clicked). Holds no personal data."""

    event: str
    detail: str = ""


class CheckoutRequest(BaseModel):
    """Request body for starting a credit purchase.

    Attributes:
        pack_id: Id of a pack from `GET /config`.
        redirect_url: Page to return to after payment.
    """

    pack_id: str
    redirect_url: str = ""


class ErrorResponse(BaseModel):
    """Error body returned by the API."""

    detail: str


class AuthSignupRequest(BaseModel):
    """Request body for creating an account."""

    username: str
    email: str
    password: str


class AuthLoginRequest(BaseModel):
    """Request body for signing in."""

    email: str
    password: str


class UserDetail(BaseModel):
    """Public details of a signed-in user."""

    id: str
    email: str
    username: str | None = None


class AuthResponse(BaseModel):
    """Session returned after a successful authentication.

    Attributes:
        access_token: Supabase access token for the `Authorization` header.
        user: Details of the signed-in user.
        credits: Credits remaining on the account.
    """

    access_token: str
    user: UserDetail
    credits: int


class VerifyOtpRequest(BaseModel):
    """Request body for confirming a signup with an emailed code.

    Attributes:
        email: Email address that received the code.
        token: One-time code from the email.
    """

    email: str
    token: str


class ResendOtpRequest(BaseModel):
    """Request body for re-sending a signup code."""

    email: str


class SignupStatusResponse(BaseModel):
    """Result of a signup request that awaits email verification."""

    status: str
    email: str
    message: str


class ForgotPasswordRequest(BaseModel):
    """Request body for starting a password reset."""

    email: str


class ResetPasswordConfirmRequest(BaseModel):
    """Request body for completing a password reset.

    Attributes:
        email: Email address of the account.
        token: One-time recovery code from the email.
        new_password: Password to set.
    """

    email: str
    token: str
    new_password: str


class ChangeUsernameRequest(BaseModel):
    """Request body for changing the username."""

    new_username: str
