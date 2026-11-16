"""Schema of a generated job description."""

from pydantic import BaseModel, Field


class JobDescriptionDraft(BaseModel):
    """Structured job description produced by the LLM.

    Attributes:
        title: Job title.
        about_company: Company overview paragraph.
        about_role: Role overview paragraph.
        responsibilities: Bullet points describing duties.
        requirements: Bullet points describing required qualifications.
        nice_to_haves: Bullet points describing optional qualifications.
        benefits: Bullet points describing perks and compensation.
        why_join_us: Paragraph explaining why candidates should apply.
        equal_opportunity: Equal opportunity statement.
        pay_range: Pay range text. Built by the server from the user's
            input, never written by the LLM.
    """

    title: str
    about_company: str
    about_role: str
    responsibilities: list[str] = Field(default_factory=list)
    requirements: list[str] = Field(default_factory=list)
    nice_to_haves: list[str] = Field(default_factory=list)
    benefits: list[str] = Field(default_factory=list)
    why_join_us: str = ""
    equal_opportunity: str = ""
    pay_range: str = ""
