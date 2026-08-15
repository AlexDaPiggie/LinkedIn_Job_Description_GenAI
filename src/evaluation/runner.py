import csv
import json
from pathlib import Path
from src.agent.job_agent import JobAgent
from src.evaluation.metrics import check_expected_terms, score_schema_result, calculate_cost, evaluate_quality_with_judge
from src.evaluation.scenarios import EVALUATION_SCENARIOS
from src.llm.client import generate_text
from src.llm.models import MODELS_TO_EVALUATE
from src.schema.job_info import JobInfo

def run_single_evaluation (
    model_config: dict, 
    scenario: dict,
    generate_text_fn = generate_text
):

    agent = JobAgent(generate_text_fn = generate_text_fn)
    job_info = JobInfo.model_validate(scenario["job_info"])
    rows = []

    try:
        generated = agent.generate_draft(
            job_info,
            provider=model_config["provider"],
            model=model_config["model_id"],
        )
        rows.append(_build_row(model_config, scenario, "generate", generated))
    except Exception as exc:
        rows.append(_build_failed_row(model_config, scenario, "generate", str(exc)))
        return rows

    try:
        refined = agent.refine_draft(
            job_info.company_name,
            generated.draft,
            scenario["refinement_request"],
            provider=model_config["provider"],
            model=model_config["model_id"],
        )
        rows.append(_build_row(model_config, scenario, "refine", refined))
    except Exception as exc:
        rows.append(_build_failed_row(model_config, scenario, "refine", str(exc)))

    return rows

def run_benchmark (output_dir: str = "eval_results"):
    rows: list[dict] = []
    for model_config in MODELS_TO_EVALUATE:
        for scenario in EVALUATION_SCENARIOS:
            rows.extend(run_single_evaluation(model_config, scenario))
    _write_results(rows, output_dir)
    return rows

# add new rows to the .csv file
def _build_row(
    model_config: dict, 
    scenario: dict, 
    task_type: str, 
    agent_result,
):
    
    schema_scores = score_schema_result(agent_result.draft)
    term_scores = check_expected_terms(
        agent_result.markdown,
        scenario["expected_checks"]["must_include"],
        scenario["expected_checks"]["must_not_include"],
    )

    #compute token cost
    cost = calculate_cost (
        model_config["model_id"],
        agent_result.llm_result.input_tokens,
        agent_result.llm_result.output_tokens,
    )

    #evaluate quality with judge
    quality_scores = evaluate_quality_with_judge(
        agent_result.markdown, 
        scenario["job_info"],
        task_type,
        scenario.get ("refinement_request")
    )

    return {
        "model_name": model_config["name"],
        "provider": model_config["provider"],
        "model_id": model_config["model_id"],
        "scenario_id": scenario["id"],
        "scenario_category": scenario["category"],
        "task_type": task_type,
        "valid_json": True,
        "schema_pass": schema_scores["schema_pass"],
        "required_fields_present": schema_scores["required_fields_present"],
        "must_include_pass": term_scores["must_include_pass"],
        "must_not_include_pass": term_scores["must_not_include_pass"],
        "latency_seconds": agent_result.llm_result.latency_seconds,
        "input_tokens": agent_result.llm_result.input_tokens,
        "output_tokens": agent_result.llm_result.output_tokens,
        "estimated_cost": cost,
        "specificity_score": quality_scores.get("specificity_score", ""),
        "tone_score": quality_scores.get("tone_score", ""),
        "faithfullness_score": quality_scores.get("faithfullness_score", ""),
        "linkedin_readiness_score": quality_scores.get("linkedin_readiness_score", ""),
        "refinement_quality_score": quality_scores.get("refinement_quality_score", ""),
        "overall_quality_score": quality_scores.get("overall_quality_score", ""),
        "notes": "",
    }

def _build_failed_row(model_config: dict, scenario: dict, task_type: str, error_msg: str):
    return {
        "model_name": model_config["name"],
        "provider": model_config["provider"],
        "model_id": model_config["model_id"],
        "scenario_id": scenario["id"],
        "scenario_category": scenario["category"],
        "task_type": task_type,
        "valid_json": False,
        "schema_pass": False,
        "required_fields_present": False,
        "must_include_pass": False,
        "must_not_include_pass": False,
        "latency_seconds": None,
        "input_tokens": None,
        "output_tokens": None,
        "estimated_cost": None,
        "specificity_score": "",
        "tone_score": "",
        "faithfullness_score": "",
        "linkedin_readiness_score": "",
        "refinement_quality_score": "",
        "overall_quality_score": "",
        "notes": error_msg,
    }

def _write_results(rows: list[dict], output_dir: str):
    path = Path (output_dir)
    path.mkdir(parents = True, exist_ok=True)
    json_path = path / "model_comparison.json"
    csv_path = path / "model_comparison.csv"
    json_path.write_text (json.dumps(rows, indent = 2), encoding = 'utf-8')
    if rows: 
        with csv_path.open(
            'w', 
            newline = '', 
            encoding = 'utf-8'
        ) as file:
            writer = csv.DictWriter(
                file,
                fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

if __name__ == "__main__":
    run_benchmark()