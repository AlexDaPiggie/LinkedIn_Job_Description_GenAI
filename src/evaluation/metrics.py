"""Metrics for benchmarking models: cost, LLM-as-judge, and rule checks."""

import json
import re

from src.llm.client import generate_text
from src.schema.job_description import JobDescriptionDraft

# Price in USD per 1M tokens as (input_rate, output_rate).
MODEL_PRICING = {
    "openai/gpt-4o-mini": (0.15, 0.60),
    "deepseek/deepseek-chat": (0.14, 0.28),
    "meta-llama/llama-3.3-70b-instruct": (0.12, 0.30),
    "qwen/qwen-2.5-72b-instruct": (0.35, 0.40),
    "mistralai/mistral-small-24b-instruct-2501": (0.10, 0.30),
    "anthropic/claude-3.5-haiku": (0.80, 4.00),
    "microsoft/phi-4": (0.07, 0.14),
}
DEFAULT_PRICING = (0.20, 0.80)
JUDGE_MODEL = "openai/gpt-4o-mini"

# The score keys are kept as-is (including the "faithfullness" spelling)
# because they are stored in existing evaluation result files.
JUDGE_SCORE_KEYS = (
    "specificity_score",
    "tone_score",
    "faithfullness_score",
    "linkedin_readiness_score",
    "refinement_quality_score",
    "overall_quality_score",
)

JUDGE_PROMPT = """
You are an expert HR evaluation judge. Evaluate the following generated LinkedIn Job Description on a scale of 1 to 5 for each category:

1. sepcificity_score (1-5): Clear requirements, tool, responsibilites
2. tone_score (1-5): How well the draft matches the requested tone (specified in Job Info under "tone") and any tone-related adjustments in the refinement request.
3. faithfullness_score (1-5): Accurate to input job info, no hallucinations.
4. linkedin_readiness_score (1-5): Directly ready to post on LinkedIn.
5. refinement_quality_score (1-5): Appropriately addressed refinement request (or 5.0 of initial generation).

Return ONLY valid JSON in this exact structure:
{
    "specificity_score": 4.5,
    "tone_score": 5.0,
    "faithfullness_score": 4.8,
    "linkedin_readiness_score": 4.5,
    "refinement_quality_score": 5.0,
    "overall_quality_score": 4.76
}
"""


def calculate_cost(model_id: str, input_tokens: int | None, output_tokens: int | None) -> float:
    """Estimates the USD cost of one LLM call.

    Args:
        model_id: OpenRouter model identifier. Unknown models use a default rate.
        input_tokens: Prompt tokens used.
        output_tokens: Completion tokens used.

    Returns:
        The cost rounded to 6 decimals, or 0.0 if either token count is
        missing or zero.
    """
    if not input_tokens or not output_tokens:
        return 0.0
    input_rate, output_rate = MODEL_PRICING.get(model_id, DEFAULT_PRICING)
    cost = (float(input_tokens) * float(input_rate) * 1e-6) + (float(output_tokens) * float(output_rate) * 1e-6)
    return round(cost, 6)


def evaluate_quality_with_judge(
    text: str,
    job_info: dict,
    task_type: str,
    refinement_request: str | None = None,
) -> dict:
    """Scores a generated draft using an LLM as the judge.

    Args:
        text: The generated job description to score.
        job_info: The hiring details the draft was generated from.
        task_type: "generate" or "refine".
        refinement_request: The refinement instruction, if any.

    Returns:
        A dict with the keys in `JUDGE_SCORE_KEYS`. All scores are 0.0 if
        the judge call or its JSON parsing fails.
    """
    prompt = (
        f"{JUDGE_PROMPT}\n\nJob Info:\n{json.dumps(job_info)}\n\n"
        f"Task:{task_type}\nRefinement:{refinement_request}\n\nDraft:\n{text}"
    )
    try:
        response = generate_text(
            prompt=prompt,
            provider="openrouter",
            model=JUDGE_MODEL,
        )

        response_text = response.text.strip()
        fence_match = re.search(r"```(?:json)?(.*?)```", response_text, re.DOTALL)
        if fence_match:
            response_text = fence_match.group(1).strip()

        return json.loads(response_text)
    except Exception:
        return {key: 0.0 for key in JUDGE_SCORE_KEYS}


def score_schema_result(draft: JobDescriptionDraft) -> dict:
    """Checks that a parsed draft has all required content.

    Args:
        draft: The parsed draft (already schema-valid).

    Returns:
        A dict with `schema_pass` (always True for a parsed draft) and
        `required_fields_present`.
    """
    required_text_fields = [
        draft.title,
        draft.about_company,
        draft.about_role,
        draft.why_join_us,
        draft.equal_opportunity,
    ]
    required_list_fields = [draft.responsibilities, draft.requirements]

    return {
        "schema_pass": True,
        "required_fields_present": (
            all(value.strip() for value in required_text_fields)
            and all(len(items) > 0 for items in required_list_fields)
        ),
    }


def check_expected_terms(
    text: str,
    must_include: list[str],
    must_not_include: list[str],
) -> dict:
    """Checks a text for required and forbidden terms (case-insensitive).

    Args:
        text: Text to search.
        must_include: Terms that must all appear.
        must_not_include: Terms that must not appear.

    Returns:
        A dict with `must_include_pass` and `must_not_include_pass`.
    """
    lowered_text = text.lower()
    return {
        "must_include_pass": all(term.lower() in lowered_text for term in must_include),
        "must_not_include_pass": all(term.lower() not in lowered_text for term in must_not_include),
    }
