"""Benchmark runner comparing LLMs on job description generation."""

import csv
import json
from pathlib import Path
from src.agent.job_agent import JobAgent
from src.evaluation.metrics import check_expected_terms, score_schema_result, calculate_cost, evaluate_quality_with_judge
from src.evaluation.scenarios import EVALUATION_SCENARIOS
from src.llm.client import generate_text
from src.llm.models import MODELS_TO_EVALUATE
from src.schema.job_info import JobInfo

def run_single_evaluation(
    model_config: dict,
    scenario: dict,
    generate_text_fn=generate_text,
) -> list[dict]:
    """Runs one model on one scenario: a generation, then a refinement.

    The refinement step is skipped if generation fails.

    Args:
        model_config: Entry from `MODELS_TO_EVALUATE`.
        scenario: Entry from `EVALUATION_SCENARIOS`.
        generate_text_fn: LLM function; replaceable for testing.

    Returns:
        One result row per task that ran (success or failure).
    """

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

def run_benchmark(
    output_dir: str = "eval_results",
    target_model: str | None = None,
    skip_existing: bool = True,
) -> list[dict]:
    """Benchmarks models over all scenarios and saves the results.

    Args:
        output_dir: Directory holding `model_comparison.json` and `.csv`.
        target_model: Model ID or name to (re-)evaluate. When set, only
            that model runs and its previous rows are replaced.
        skip_existing: Skip models that already have results (ignored when
            `target_model` is set).

    Returns:
        All result rows, previous and new.
    """
    results_dir = Path(output_dir)
    json_path = results_dir / "model_comparison.json"
    existing_rows: list[dict] = []
    evaluated_model_ids: set[str] = set()

    if json_path.exists():
        try:
            existing_rows = json.loads(json_path.read_text(encoding="utf-8"))
            evaluated_model_ids = {row["model_id"] for row in existing_rows}
        except Exception as error:
            print(f"Warning: Could not read existing results: {error}")

    # Determine which models to run
    models_to_run = []
    target_normalized = target_model.strip().lower() if target_model else None

    for model_config in MODELS_TO_EVALUATE:
        model_id = model_config["model_id"]
        model_name = model_config["name"]

        # If user explicitly specifies a model via --model
        if target_normalized:
            if target_normalized in (model_id.lower(), model_name.lower()):
                models_to_run.append(model_config)
            continue

        # Default run: skip already evaluated models
        if skip_existing and model_id in evaluated_model_ids:
            print(f"Skipping already evaluated model: {model_id}")
            continue
        models_to_run.append(model_config)

    if not models_to_run:
        if target_model:
            print(f"No matching model found for: {target_model}")
        else:
            print("No new models to evaluate.")
        return existing_rows

    # If re-evaluating specific model, remove previous results of that model from existing_rows
    if target_normalized:
        target_ids = {config["model_id"] for config in models_to_run}
        existing_rows = [row for row in existing_rows if row.get("model_id") not in target_ids]

    new_rows: list[dict] = []
    for model_config in models_to_run:
        print(f"Running evaluation for: {model_config['name']} ({model_config['model_id']})")
        for scenario in EVALUATION_SCENARIOS:
            new_rows.extend(run_single_evaluation(model_config, scenario))

    combined_rows = existing_rows + new_rows
    _write_results(combined_rows, output_dir)
    return combined_rows

def _build_row(
    model_config: dict,
    scenario: dict,
    task_type: str,
    agent_result,
) -> dict:
    """Builds the result row for a successful generation or refinement.

    Args:
        model_config: Entry from `MODELS_TO_EVALUATE`.
        scenario: Entry from `EVALUATION_SCENARIOS`.
        task_type: "generate" or "refine".
        agent_result: The `AgentResult` to score.

    Returns:
        A flat dict with rule checks, usage, cost and judge scores.
    """
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

def _build_failed_row(model_config: dict, scenario: dict, task_type: str, error_message: str) -> dict:
    """Builds the result row for a task that raised an error.

    Args:
        model_config: Entry from `MODELS_TO_EVALUATE`.
        scenario: Entry from `EVALUATION_SCENARIOS`.
        task_type: "generate" or "refine".
        error_message: Text of the error, stored in `notes`.

    Returns:
        A row with all checks failed and empty scores.
    """
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
        "notes": error_message,
    }

def _write_results(rows: list[dict], output_dir: str) -> None:
    """Writes result rows to JSON and CSV files.

    Args:
        rows: Result rows to save.
        output_dir: Directory for `model_comparison.json` and `.csv`.
    """
    results_dir = Path(output_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    json_path = results_dir / "model_comparison.json"
    csv_path = results_dir / "model_comparison.csv"
    json_path.write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if rows:
        with csv_path.open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)

if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser(description="Run LLM benchmark for job description generation.")
    arg_parser.add_argument(
        "--model",
        type=str,
        default=None,
        help="Specific model ID or name to evaluate or re-evaluate (e.g. 'microsoft/phi-4' or 'openai/gpt-4o-mini')",
    )
    args = arg_parser.parse_args()

    run_benchmark(target_model=args.model)