from src.schema.job_description import JobDescriptionDraft
def score_schema_result (draft: JobDescriptionDraft): 
    required_text = [
        draft.title,
        draft.about_company,
        draft.about_role,
        draft.why_join_us,
        draft.equal_opportunity,
    ]
    required_list = [draft.responsibilities, draft.requirements]

    return {
        "schema_pass": True,
        "required_fields_preset": all(value.strip() for value in required_text) and all(len(items) > 0 for items in required_list),
    }

def check_expected_terms (
    text: str, 
    must_include: list[str], 
    must_not_include: list[str],
):
    lowered = text.lower()
    return {
        "must_include_pass": all(term.lower() in lowered for term in must_include),
        "must_not_include_pass": all (term.lower() not in lowered for term in must_not_include)
    }


