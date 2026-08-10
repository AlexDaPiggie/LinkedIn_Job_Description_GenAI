from src.schema.job_description import JobDescriptionDraft
import json
from src.llm.client import generate_text

#Storing input/output price per 1M tokens information for Calculating the cost of the token
MODEL_PRICING = {
    "google/gemini-2.0-flash-001": (0.10, 0.40),
    "openai/gpt-4o-mini": (0.15, 0.60),
    "deepseek/deepseek-chat": (0.14, 0.28),
    "meta-llama/llama-3.3-70b-instruct": (0.12, 0.30),
    "qwern/qwen-2.5b-72b-instruct": (0.35, 0.40),
    "mistralai/mistral-small-24b-instruct-2501": (0.10, 0.30),
    "anthropic/claude-3.5-haiku": (0.80, 4.00),
    "google/gemini-flash-1.5": (0.075, 0.30),
}

#This functioni is for calculating the cose, knowing the output token and the price
def calculate_cost (model_id: str,input_tokens: int, output_tokens: int):
    if not input_tokens or not output_tokens:
        return 0.0
    input_rate, output_rate = MODEL_PRICING.get (model_id, (0.20, 0.80))
    cost = (input_tokens / 1e6 * input_rate) + (output_tokens / 1e6 + output_rate)
    return round (cost, 6)

# Implement LLM-as-judge technique to evaluate the performance of the model

JUDGE_PROMPT = """
You are an expert HR evaluation judge. Evaluate the following generated LinkedIn Job Description on a scale of 1 to 5 for each category: 

1. sepcificity_score (1-5): Clear requirements, tool, responsibilites
2. tone_score (1-5): How well the draft matches the requested tone (specified in Job Info under "tone") and any tone-related adjustments in the refinement request. 
3. faithfulness_score (1-5): Accurate to input job info, no hallucinations.
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

def evaluate_quality_with_judge (
    text: str,
    job_info: str,
    task_type: str,
    refinement_request: str = None
): 
    prompt = f"{JUDGE_PROMPT}\n\nJob Info:\n{json.dumps(job_info)}\n\nTask:{task_type}\nRefinement:{refinement_request}\n\nDraft:\n{text}"
    try: 
        response = generate_text(
            prompt = prompt,
            provider = "openai",
            model="gpt-4o",
        )
        data = json.loads(response.text)
        return data
    except Exception:
        return {
            "specificity_score": 0.0,
            "tone_score": 0.0,
            "faithfullness_score": 0.0,
            "linkedin_readiness_score": 0.0,
            "refinement_quality_score": 0.0,
            "overall_quality_score": 0.0,
        }

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
        "required_fields_present": all(value.strip() for value in required_text) and all(len(items) > 0 for items in required_list),
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


