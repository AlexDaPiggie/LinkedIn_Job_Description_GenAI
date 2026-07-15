import json
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo
from src.agent.state import SessionState as state

JSON_SCHEMA_DESCRIPTION = """
{
    "title": "string",
    "about_company": "string",
    "about_role": "string",
    "responsibilities": ["string"],
    "requirements": ["string"],
    "nice_to_haves": ["string"],
    "benefits": ["string"],
    "why_join_us": "string",
    "equal_opportunity": "string"
}
""".strip()


def build_generation_prompt (job_info: JobInfo, skipped_fields: list[str]): 
    skipped = skipped_fields or []
    return f"""
You are an expert recruiter writing a polished LinkedIn job description.

Return only valid JSON matching this schema:
{JSON_SCHEMA_DESCRIPTION}

Writing rules:
- Expand short user answers into professional job-description language.
- Do not invent salary, benefits, tools, company facts, candidate motivations, or requirements.
- If optional information is missing, return an empty string or empty list for that field.
- Do not write "Not specified", "N/A", "TBD", or placeholder text.
- For every field listed in skipped_fields, return an empty string or empty list in the related JSON section.
- Do not infer, invent, or backfill content for skipped_fields from other context.
- Keep requirements fair and inclusive.
- For list fields such as responsibilities, requirements, nice_to_haves, and benefits, do not merely copy or split short user phrases into bullets.
- Treat short or comma-separated inputs as rough notes. Reinterpret each idea into clear, complete, professional bullet points.
- Combine, expand, or rephrase short fragments when needed, while preserving the user's intent.
- Do not invent unsupported facts, tools, requirements, benefits, or company claims.
- Each bullet should read like a complete job-description bullet, not a keyword list.
- For equal_opportunity, if job_info.equal_opportunity is "yes" or another affirmative answer, write a concise, general equal opportunity statement.
- Formatting requests such as "make this a paragraph" or "use bullets" must not change the JSON schema.
- responsibilities, requirements, nice_to_haves, and benefits must always be arrays of strings.
- If job_info.equal_opportunity is "no", empty, or listed in skipped_fields, return "" for equal_opportunity.
- If job_info.equal_opportunity contains custom wording, preserve the user's intent and polish it into a concise equal opportunity statement.
- Match the requested tone and length.
- You must include every JSON key exactly as shown in the schema.
- Never omit a key.
- For skipped or unknown string fields, return "".
- For skipped or unknown list fields, return [].

Length guidance:
- short: under 500 words after rendering
- medium: roughly 600-900 words after rendering
- long: roughly 900-1200 words after rendering

Job information:
{json.dumps(job_info.model_dump(), indent=2)}

skipped_fields:
{json.dumps(skipped, indent=2)}
""".strip()


def build_refinement_prompt (
    job_info: JobInfo,
    current_draft: JobDescriptionDraft,
    user_request: str, 
    skipped_fields: list[str]
):
    skipped = skipped_fields or []
    return f"""
You are revising a LinkedIn job description.

Return only valid JSON matching this schema:
{JSON_SCHEMA_DESCRIPTION}

Refinement rules:
- Apply the user's request.
- Preserve unchanged facts.
- Do NOT introduce unsupported claims.
- Continue returning empty strings or empty lists for skipped_fields, unless the user has edited that answer and it is no longer skipped
- Return the full revised JSON object.
- You must include every JSON key exactly as shown in the schema.
- Never omit a key.
- For skipped or unknown string fields, return "".
- For skipped or unknown list fields, return [].
- When revising list fields, keep bullets polished and complete.
- Do not reduce them to comma-split fragments unless the user explicitly asks for terse keywords.
- Formatting requests such as "make this a paragraph" or "use bullets" must not change the JSON schema.
- responsibilities, requirements, nice_to_haves, and benefits must always be arrays of strings.
- If the user asks to change a list section into paragraph form, keep that field as an array of strings and only improve the wording. Do not return a plain string for any list field.
- For equal_opportunity, if job_info.equal_opportunity is "yes" or another affirmative answer, write a concise, general equal opportunity statement.
- If job_info.equal_opportunity is "no", empty, or listed in skipped_fields, return "" for equal_opportunity.
- If job_info.equal_opportunity contains custom wording, preserve the user's intent and polish it into a concise equal opportunity statement.

User request: 
{user_request}

Job information: 
{json.dumps (job_info.model_dump(), indent=2)}

skipped_fields: 
{json.dumps(skipped, indent = 2)}

Current draft: 
{json.dumps (current_draft.model_dump(), indent = 2)}
""".strip()
