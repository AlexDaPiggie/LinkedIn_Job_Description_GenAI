from src.schema.job_description import JobDescriptionDraft

SKIPPED_FIELD_TO_SECTION = {
    "company_description": "about_company", 
    "nice_to_haves": "nice_to_haves", 
    "benefits": "benefits",
    "why_join_us": "why_join_us",
    "equal_opportunity": "equal_opportunity",
}

def _append_text_section (
    sections: list[str],
    heading: str,
    value: str,
    section_key: str, 
    suppressed_sections: set[str],
):
    '''
    This helper function is for appending the text into the .md file
    '''
    if section_key in suppressed_sections:
        return 
    stripped = value.strip()
    if stripped: 
        sections.append (f"## {heading} \n \n {stripped}")

def _append_bullet_section(
    sections: list[str],
    heading: str,
    items: list[str],
    section_key: str,
    suppressed_sections: set[str],
): 
    '''
    THis helper function is to append in the sections with bulletpoints. 
    '''
    if section_key in suppressed_sections:
        return 
    cleaned = [item.strip() for item in items if item.strip()]
    if cleaned: 
        if len(cleaned) == 1:
            _append_text_section(sections, heading, cleaned[0], section_key, suppressed_sections)
        else:
            sections.append (f"## {heading} \n \n" + "\n".join(f"- {item}" for item in cleaned))
    
def render_job_description (
    draft: JobDescriptionDraft, 
    company_name: str = "",
    skipped_fields: list[str] | None = None
): 
    sections = [f"# {draft.title}"]
    company_heading = f"About {company_name.strip()}" if company_name.strip() else "About the Company"
    suppressed_sections = {
        SKIPPED_FIELD_TO_SECTION[field]
        for field in skipped_fields or []
        if field in SKIPPED_FIELD_TO_SECTION
    }
    _append_text_section (sections, company_heading, draft.about_company, "about_company", suppressed_sections)
    _append_text_section (sections, "About the Role", draft.about_role, "about_role", suppressed_sections)
    _append_bullet_section (sections, "Responsibilities", draft.responsibilities, "responsibilities", suppressed_sections)
    _append_bullet_section (sections, "Requirements", draft.requirements, "requirements", suppressed_sections)
    _append_bullet_section (sections, "Nice to Have", draft.nice_to_haves, "nice_to_haves", suppressed_sections)
    _append_bullet_section(sections, "Benefits", draft.benefits, "benefits", suppressed_sections)
    _append_text_section (sections, "Why Join Us", draft.why_join_us, "why_join_us", suppressed_sections)
    _append_text_section(
        sections, 
        "Equal Opportunity Statement", 
        draft.equal_opportunity,
        "equal_opportunity", 
        suppressed_sections,
    )

    return "\n \n".join (sections)

def render_job_description_preview(
    draft: JobDescriptionDraft,
    company_name: str = "",
    skipped_fields: list[str] | None = None,
) -> tuple[JobDescriptionDraft, str]:
    sections = [f"# {draft.title}"]
    company_heading = f"About {company_name.strip()}" if company_name.strip() else "About the Company"
    suppressed_sections = {
        SKIPPED_FIELD_TO_SECTION[field]
        for field in skipped_fields or []
        if field in SKIPPED_FIELD_TO_SECTION
    }
    _append_text_section(sections, company_heading, draft.about_company, "about_company", suppressed_sections)
    _append_text_section(sections, "About the Role", draft.about_role, "about_role", suppressed_sections)

    preview_resps = [item.strip() for item in draft.responsibilities[:2] if item.strip()]
    if preview_resps:
        _append_bullet_section(sections, "Key Responsibilities (Preview)", preview_resps, "responsibilities", suppressed_sections)

    sections.append(
        "---\n \n"
        "### 🔒 Sign in to see the full output\n \n"
        "You are viewing a free preview. Sign in or create a free account to unlock:\n"
        "- Complete responsibilities and daily expectations\n"
        "- Required qualifications, core skills, and nice-to-haves\n"
        "- Benefits, perks, and company culture statements\n"
        "- AI refinement and Word (.docx) export"
    )

    preview_draft = JobDescriptionDraft(
        title=draft.title,
        about_company=draft.about_company if "about_company" not in suppressed_sections else "",
        about_role=draft.about_role if "about_role" not in suppressed_sections else "",
        responsibilities=preview_resps,
        requirements=[],
        nice_to_haves=[],
        benefits=[],
        why_join_us="",
        equal_opportunity="",
    )

    return preview_draft, "\n \n".join(sections)