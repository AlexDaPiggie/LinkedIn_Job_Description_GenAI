"""Parsing of raw LLM output into validated Python objects."""

import json
import re

from pydantic import ValidationError

from src.schema.job_description import JobDescriptionDraft


def strip_json(text: str) -> str:
    """Removes an optional Markdown code fence around a JSON payload.

    Args:
        text: Raw LLM output, possibly wrapped in a ```json fence.

    Returns:
        The JSON text without the fence and surrounding whitespace.
    """
    stripped_text = text.strip()
    fence_match = re.search(r"```(?:json)?\s*(.*?)\s*```", stripped_text, flags=re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()
    return stripped_text


def parse_job_description(text: str) -> JobDescriptionDraft:
    """Parses LLM output into a validated job description draft.

    Args:
        text: Raw LLM output containing the draft as JSON.

    Returns:
        The validated draft.

    Raises:
        ValueError: If the text is not valid JSON or fails schema validation.
    """
    json_text = strip_json(text)
    try:
        data = json.loads(json_text)
        return JobDescriptionDraft.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(f"Invalid job description JSON: {exc}") from exc


def parse_extracted_doc(text: str) -> dict:
    """Parses the JSON produced by document-extraction prompts.

    Args:
        text: Raw LLM output containing a JSON object.

    Returns:
        The decoded object, or an empty dict if the JSON is not an object.

    Raises:
        ValueError: If the text is not valid JSON.
    """
    json_text = strip_json(text)
    try:
        data = json.loads(json_text)
        return data if isinstance(data, dict) else {}
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid extraction JSON: {exc}") from exc


def parse_section(text: str, section: str, is_list: bool) -> list[str] | str:
    """Parses the one-key JSON returned when a single section is rewritten.

    Args:
        text: Raw LLM output.
        section: Expected section key.
        is_list: Whether the section is a list of bullets.

    Returns:
        The new section value (list of strings, or a string).

    Raises:
        ValueError: If the JSON is invalid or the key is missing or empty.
    """
    try:
        data = json.loads(strip_json(text))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid section JSON: {exc}") from exc
    value = data.get(section) if isinstance(data, dict) else None
    if is_list:
        if not isinstance(value, list):
            raise ValueError(f"Section '{section}' must be a list")
        items = [str(item).strip() for item in value if str(item).strip()]
        if not items:
            raise ValueError(f"Section '{section}' came back empty")
        return items
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Section '{section}' came back empty")
    return value.strip()


def parse_screening_questions(text: str) -> list[dict]:
    """Parses screening questions from LLM output.

    Args:
        text: Raw LLM output containing a `questions` list.

    Returns:
        Up to 10 dicts with `question`, `type` and `ideal_answer` keys.

    Raises:
        ValueError: If the JSON is invalid or has no usable questions.
    """
    try:
        data = json.loads(strip_json(text))
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid screening JSON: {exc}") from exc
    raw = data.get("questions") if isinstance(data, dict) else None
    if not isinstance(raw, list):
        raise ValueError("Screening questions missing")
    questions = []
    for item in raw[:10]:
        if isinstance(item, dict) and str(item.get("question", "")).strip():
            questions.append({
                "question": str(item["question"]).strip(),
                "type": str(item.get("type", "must_have")),
                "ideal_answer": str(item.get("ideal_answer", "")).strip(),
            })
    if not questions:
        raise ValueError("No screening questions returned")
    return questions
