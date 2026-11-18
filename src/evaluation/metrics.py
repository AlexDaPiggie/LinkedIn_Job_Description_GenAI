"""Metrics for benchmarking models: cost, LLM-as-judge, and rule checks."""

import json
import re

from src.evaluation.pricing import load_prices
from src.llm.client import generate_text
from src.schema.job_description import JobDescriptionDraft

# The judge comes from a model family that is not among the candidates, so it
# does not grade its own outputs. Temperature 0 keeps its scores repeatable.
JUDGE_MODEL = "anthropic/claude-haiku-4.5"
JUDGE_TEMPERATURE = 0.0

# Criteria the judge scores from 1 to 5. The overall score is computed in code
# as the mean of these, not asked from the judge.
# "faithfullness" keeps its old spelling: it is a key in stored result files.
JUDGE_CRITERIA = (
    "specificity_score",
    "tone_score",
    "faithfullness_score",
    "linkedin_readiness_score",
)
REFINE_CRITERION = "refinement_quality_score"
JUDGE_SCORE_KEYS = JUDGE_CRITERIA + (REFINE_CRITERION, "overall_quality_score")

JUDGE_PROMPT = """
You are an experienced recruiter grading a generated LinkedIn job description.
Score each criterion from 1 (poor) to 5 (excellent). Use whole numbers.

- specificity_score: concrete responsibilities, tools and requirements, not generic filler.
- tone_score: matches the requested tone in Job Info (and any tone change in the refinement request).
- faithfullness_score: every fact comes from Job Info. Deduct for invented pay, benefits, perks, locations or company claims.
- linkedin_readiness_score: could be posted on LinkedIn as is (structure, length, no placeholders).
- refinement_quality_score: only for Task "refine" - how well the draft applies the refinement request. Use null for Task "generate".

Return ONLY this JSON, no other text:
{"specificity_score": 4, "tone_score": 5, "faithfullness_score": 5, "linkedin_readiness_score": 4, "refinement_quality_score": null}
"""

# Matches pay figures such as "$120,000", "120k", "USD 90000" or "£45,000".
PAY_PATTERN = re.compile(
    r"([$£€]\s?\d[\d,.]*\s?[kK]?)|(\b\d{2,3}\s?[kK]\b)|(\b(USD|EUR|GBP)\s?\d[\d,.]*)"
)


def calculate_cost(
    model_id: str,
    input_tokens: int | None,
    output_tokens: int | None,
    prices: dict | None = None,
) -> float | None:
    """Computes the USD cost of one LLM call from the saved price snapshot.

    Args:
        model_id: OpenRouter model identifier.
        input_tokens: Prompt tokens reported by the provider.
        output_tokens: Completion tokens reported by the provider.
        prices: `{model_id: [input_rate, output_rate]}` in USD per 1M tokens.
            Defaults to `eval_results/openrouter_prices.json`.

    Returns:
        The cost rounded to 6 decimals, or None when the token counts or the
        model's price are unknown. Unknown prices are never guessed.
    """
    if not input_tokens or not output_tokens:
        return None
    if prices is None:
        prices = load_prices()["usd_per_million_tokens"]
    rates = prices.get(model_id)
    if not rates:
        return None
    input_rate, output_rate = rates
    return round((input_tokens * input_rate + output_tokens * output_rate) * 1e-6, 6)


def _parse_judge_json(response_text: str) -> dict:
    """Extracts the JSON object from a judge reply (tolerates code fences)."""
    text = response_text.strip()
    fence_match = re.search(r"```(?:json)?(.*?)```", text, re.DOTALL)
    if fence_match:
        text = fence_match.group(1).strip()
    brace_match = re.search(r"\{.*\}", text, re.DOTALL)
    return json.loads(brace_match.group(0) if brace_match else text)


def evaluate_quality_with_judge(
    text: str,
    job_info: dict,
    task_type: str,
    refinement_request: str | None = None,
    generate_text_fn=generate_text,
) -> dict:
    """Scores a generated draft using an LLM as the judge.

    Args:
        text: The generated job description to score.
        job_info: The hiring details the draft was generated from.
        task_type: "generate" or "refine".
        refinement_request: The refinement instruction, if any.
        generate_text_fn: LLM function; replaceable for testing.

    Returns:
        A dict with the keys in `JUDGE_SCORE_KEYS` plus `judge_error`.
        If the judge call or its JSON fails, scores are None (not 0) and
        `judge_error` holds the reason, so failures are visible, not averaged in.
    """
    prompt = (
        f"{JUDGE_PROMPT}\n\nJob Info:\n{json.dumps(job_info)}\n\n"
        f"Task: {task_type}\nRefinement request: {refinement_request or 'none'}\n\nDraft:\n{text}"
    )
    empty = {key: None for key in JUDGE_SCORE_KEYS}
    try:
        response = generate_text_fn(
            prompt,
            provider="openrouter",
            model=JUDGE_MODEL,
            temperature=JUDGE_TEMPERATURE,
        )
        raw = _parse_judge_json(response.text)
        scores = {key: float(raw[key]) for key in JUDGE_CRITERIA}
    except Exception as error:
        return {**empty, "judge_error": f"{type(error).__name__}: {error}"[:300]}

    refine_score = raw.get(REFINE_CRITERION)
    scores[REFINE_CRITERION] = float(refine_score) if task_type == "refine" and refine_score is not None else None
    counted = [scores[key] for key in JUDGE_CRITERIA]
    if scores[REFINE_CRITERION] is not None:
        counted.append(scores[REFINE_CRITERION])
    scores["overall_quality_score"] = round(sum(counted) / len(counted), 3)
    scores["judge_error"] = ""
    return scores


def score_schema_result(draft: JobDescriptionDraft) -> dict:
    """Checks that a parsed draft has the core sections every posting needs.

    The equal opportunity statement is not required: it is optional input, and
    one scenario forbids it on purpose.

    Args:
        draft: The parsed draft (already schema-valid).

    Returns:
        A dict with `schema_pass` (always True for a parsed draft) and
        `required_fields_present`.
    """
    required_text_fields = [draft.title, draft.about_company, draft.about_role]
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


def check_no_invented_pay(text: str, job_info: dict) -> bool:
    """Binary faithfulness check: no pay figure unless the input gave one.

    Args:
        text: Generated job description.
        job_info: Input hiring details.

    Returns:
        True if the input has a salary, or the output contains no pay figure.
    """
    if job_info.get("salary_range") or job_info.get("pay_min") or job_info.get("pay_max"):
        return True
    return PAY_PATTERN.search(text) is None
