"""Rendering of job description drafts as Markdown."""

from src.schema.job_description import JobDescriptionDraft

# Maps a skipped intake question to the draft section it suppresses.
SKIPPED_FIELD_TO_SECTION = {
    "company_description": "about_company",
    "nice_to_haves": "nice_to_haves",
    "benefits": "benefits",
    "why_join_us": "why_join_us",
    "equal_opportunity": "equal_opportunity",
}

def _company_heading(company_name: str) -> str:
    """Returns the "About ..." heading for the company section."""
    name = company_name.strip()
    return f"About {name}" if name else "About the Company"


def _suppressed_sections(skipped_fields: list[str] | None) -> set[str]:
    """Maps skipped intake fields to the draft sections to hide.

    Args:
        skipped_fields: Names of intake questions the user skipped.

    Returns:
        The draft section keys that must not be rendered.
    """
    return {
        SKIPPED_FIELD_TO_SECTION[field]
        for field in skipped_fields or []
        if field in SKIPPED_FIELD_TO_SECTION
    }


def _append_text_section(
    sections: list[str],
    heading: str,
    value: str,
    section_key: str,
    suppressed_sections: set[str],
) -> None:
    """Appends a paragraph section unless it is suppressed or empty.

    Args:
        sections: Markdown sections collected so far (modified in place).
        heading: Section heading.
        value: Section body text.
        section_key: Draft section key, checked against `suppressed_sections`.
        suppressed_sections: Section keys that must not be rendered.
    """
    if section_key in suppressed_sections:
        return
    body = value.strip()
    if body:
        sections.append(f"## {heading} \n \n {body}")


def _append_bullet_section(
    sections: list[str],
    heading: str,
    items: list[str],
    section_key: str,
    suppressed_sections: set[str],
) -> None:
    """Appends a bullet-list section unless it is suppressed or empty.

    A single item is rendered as a paragraph instead of a one-item list.

    Args:
        sections: Markdown sections collected so far (modified in place).
        heading: Section heading.
        items: Bullet texts.
        section_key: Draft section key, checked against `suppressed_sections`.
        suppressed_sections: Section keys that must not be rendered.
    """
    if section_key in suppressed_sections:
        return
    cleaned_items = [item.strip() for item in items if item.strip()]
    if not cleaned_items:
        return
    if len(cleaned_items) == 1:
        _append_text_section(sections, heading, cleaned_items[0], section_key, suppressed_sections)
    else:
        bullets = "\n".join(f"- {item}" for item in cleaned_items)
        sections.append(f"## {heading} \n \n" + bullets)


def render_job_description(
    draft: JobDescriptionDraft,
    company_name: str = "",
    skipped_fields: list[str] | None = None,
) -> str:
    """Renders a full job description as Markdown.

    Args:
        draft: Draft to render.
        company_name: Company name used in the "About ..." heading.
        skipped_fields: Intake fields whose sections should be omitted.

    Returns:
        The Markdown document.
    """
    sections = [f"# {draft.title}"]
    suppressed = _suppressed_sections(skipped_fields)

    _append_text_section(sections, _company_heading(company_name), draft.about_company, "about_company", suppressed)
    _append_text_section(sections, "About the Role", draft.about_role, "about_role", suppressed)
    _append_bullet_section(sections, "Responsibilities", draft.responsibilities, "responsibilities", suppressed)
    _append_bullet_section(sections, "Requirements", draft.requirements, "requirements", suppressed)
    _append_bullet_section(sections, "Nice to Have", draft.nice_to_haves, "nice_to_haves", suppressed)
    _append_text_section(sections, "Pay Range", draft.pay_range, "pay_range", suppressed)
    _append_bullet_section(sections, "Benefits", draft.benefits, "benefits", suppressed)
    _append_text_section(sections, "Why Join Us", draft.why_join_us, "why_join_us", suppressed)
    _append_text_section(
        sections,
        "Equal Opportunity Statement",
        draft.equal_opportunity,
        "equal_opportunity",
        suppressed,
    )

    return "\n \n".join(sections)
