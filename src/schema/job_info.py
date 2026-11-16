"""Schema of the hiring information supplied by the user."""

from pydantic import BaseModel, Field


def parse_list_answer(answer: str) -> list[str]:
    """Splits a free-text answer into list items.

    Items may be separated by newlines, commas, or both.

    Args:
        answer: Raw answer text typed by the user.

    Returns:
        The stripped, non-empty items in their original order.
    """
    pieces: list[str] = []
    for line in answer.splitlines():
        pieces.extend(line.split(","))
    return [piece.strip() for piece in pieces if piece.strip()]


class JobInfo(BaseModel):
    """Hiring details collected from the user (input to generation).

    Attributes:
        company_name: Name of the hiring company.
        role_title: Title of the open role.
        role_summary: Why the role exists and what it should achieve.
        responsibilities: Main duties of the role.
        requirements: Required skills and qualifications.
        company_description: Short company description, if provided.
        nice_to_haves: Optional skills and experience.
        benefits: Perks and compensation details.
        why_join_us: Reasons candidates should join.
        equal_opportunity: "yes", "no", or custom equal opportunity wording.
        tone: Requested writing tone.
        target_length: Requested length: "short", "medium", or "long".
        team_context: Team size, structure and who the role works with.
        pay_min: Lower end of the pay range, if the user gave one.
        pay_max: Upper end of the pay range, if the user gave one.
        pay_currency: ISO currency code of the pay range.
        pay_period: "year", "month" or "hour".
        jurisdiction: Pay-transparency jurisdiction code (see
            `src.quality.jurisdictions`), or "none".
    """

    company_name: str = ""
    role_title: str = ""
    role_summary: str = ""
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    company_description: str | None = None
    nice_to_haves: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    why_join_us: str = ""
    equal_opportunity: str = ""
    tone: str = "professional"
    target_length: str = "medium"
    team_context: str = ""
    pay_min: float | None = Field(default=None, ge=0)
    pay_max: float | None = Field(default=None, ge=0)
    pay_currency: str = "USD"
    pay_period: str = "year"
    jurisdiction: str = "none"
