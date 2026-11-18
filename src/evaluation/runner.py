"""Benchmark runner comparing LLMs on job description generation.

Each run sends every scenario to every model (generate, then refine), scores
the output with rule checks and an LLM judge, and writes one row per call.

Usage:
    python -m src.evaluation.runner                  # all models, 3 runs each
    python -m src.evaluation.runner --runs 1
    python -m src.evaluation.runner --model openai/gpt-4o-mini
    python -m src.evaluation.runner --workers 6     # models in parallel

Calls for one model always run one after another, so its latency is not
affected by its own load. `--workers` only runs different models side by side.
"""

import csv
import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from src.agent.job_agent import JobAgent
from src.evaluation.metrics import (
    JUDGE_MODEL,
    calculate_cost,
    check_expected_terms,
    check_no_invented_pay,
    evaluate_quality_with_judge,
    score_schema_result,
)
from src.evaluation.pricing import load_prices
from src.evaluation.scenarios import EVALUATION_SCENARIOS
from src.llm.client import generate_text
from src.llm.models import MODELS_TO_EVALUATE
from src.schema.job_info import JobInfo

DEFAULT_RUNS = 3
RESULT_FILES = ("model_comparison.json", "model_comparison.csv")


def generate_without_fallback(prompt, provider, model, fallback_models=None, **kwargs):
    """Calls only the requested model.

    The app falls back to other models when one fails. In a benchmark that
    would credit one model with another model's output, so fallbacks are off.
    """
    return generate_text(prompt, provider=provider, model=model, **kwargs)


def run_single_evaluation(
    model_config: dict,
    scenario: dict,
    run_context: dict,
    generate_text_fn=generate_without_fallback,
    judge_fn=evaluate_quality_with_judge,
) -> list[dict]:
    """Runs one model on one scenario: a generation, then a refinement.

    The refinement step is skipped if generation fails.

    Args:
        model_config: Entry from `MODELS_TO_EVALUATE`.
        scenario: Entry from `EVALUATION_SCENARIOS`.
        run_context: Shared columns for this run (run_id, run_index, prices).
        generate_text_fn: LLM function; replaceable for testing.
        judge_fn: Judge function; replaceable for testing.

    Returns:
        One result row per task that ran (success or failure).
    """
    agent = JobAgent(generate_text_fn=generate_text_fn)
    job_info = JobInfo.model_validate(scenario["job_info"])
    rows = []

    try:
        generated = agent.generate_draft(job_info, provider=model_config["provider"], model=model_config["model_id"])
        rows.append(_build_row(model_config, scenario, "generate", generated, run_context, judge_fn))
    except Exception as exc:
        rows.append(_build_failed_row(model_config, scenario, "generate", str(exc), run_context))
        return rows

    try:
        refined = agent.refine_draft(
            job_info.company_name,
            generated.draft,
            scenario["refinement_request"],
            provider=model_config["provider"],
            model=model_config["model_id"],
        )
        rows.append(_build_row(model_config, scenario, "refine", refined, run_context, judge_fn))
    except Exception as exc:
        rows.append(_build_failed_row(model_config, scenario, "refine", str(exc), run_context))

    return rows


def run_benchmark(
    output_dir: str = "eval_results",
    target_model: str | None = None,
    runs: int = DEFAULT_RUNS,
    workers: int = 1,
) -> list[dict]:
    """Benchmarks models over all scenarios and saves the results.

    A full run (no `target_model`) replaces the results files. A targeted run
    replaces only that model's rows.

    Args:
        output_dir: Directory holding `model_comparison.json` and `.csv`.
        target_model: Model ID or name to (re-)evaluate.
        runs: Times each model runs each scenario.
        workers: Models evaluated at the same time.

    Returns:
        All result rows in the results file after the run.
    """
    target = target_model.strip().lower() if target_model else None
    models_to_run = [
        config for config in MODELS_TO_EVALUATE
        if not target or target in (config["model_id"].lower(), config["name"].lower())
    ]
    if not models_to_run:
        print(f"No matching model found for: {target_model}")
        return []

    existing_rows: list[dict] = []
    json_path = Path(output_dir) / RESULT_FILES[0]
    if target and json_path.exists():
        target_ids = {config["model_id"] for config in models_to_run}
        existing_rows = [
            row for row in json.loads(json_path.read_text(encoding="utf-8"))
            if row.get("model_id") not in target_ids
        ]

    price_snapshot = load_prices()
    started = datetime.now(timezone.utc)

    def run_model(model_config: dict) -> list[dict]:
        model_rows = []
        for run_index in range(1, runs + 1):
            run_context = {
                "run_id": started.strftime("%Y%m%dT%H%M%SZ"),
                "run_index": run_index,
                "prices": price_snapshot["usd_per_million_tokens"],
                "price_date": price_snapshot["fetched_on"],
            }
            print(f"Run {run_index}/{runs}: {model_config['model_id']}", flush=True)
            for scenario in EVALUATION_SCENARIOS:
                model_rows.extend(run_single_evaluation(model_config, scenario, run_context))
        return model_rows

    with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
        new_rows = [row for model_rows in pool.map(run_model, models_to_run) for row in model_rows]

    combined_rows = existing_rows + new_rows
    _write_results(combined_rows, output_dir)
    return combined_rows


def _base_row(model_config: dict, scenario: dict, task_type: str, run_context: dict) -> dict:
    """Columns shared by success and failure rows."""
    return {
        "run_id": run_context["run_id"],
        "run_index": run_context["run_index"],
        "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "model_name": model_config["name"],
        "provider": model_config["provider"],
        "model_id": model_config["model_id"],
        "scenario_id": scenario["id"],
        "scenario_category": scenario["category"],
        "task_type": task_type,
    }


def _build_row(
    model_config: dict,
    scenario: dict,
    task_type: str,
    agent_result,
    run_context: dict,
    judge_fn=evaluate_quality_with_judge,
) -> dict:
    """Builds the result row for a successful generation or refinement.

    Args:
        model_config: Entry from `MODELS_TO_EVALUATE`.
        scenario: Entry from `EVALUATION_SCENARIOS`.
        task_type: "generate" or "refine".
        agent_result: The `AgentResult` to score.
        run_context: Shared columns for this run.
        judge_fn: Judge function.

    Returns:
        A flat dict with rule checks, usage, cost and judge scores.
    """
    llm_result = agent_result.llm_result
    schema_scores = score_schema_result(agent_result.draft)
    term_scores = check_expected_terms(
        agent_result.markdown,
        scenario["expected_checks"]["must_include"],
        scenario["expected_checks"]["must_not_include"],
    )
    quality_scores = judge_fn(
        agent_result.markdown,
        scenario["job_info"],
        task_type,
        scenario.get("refinement_request"),
    )
    return {
        **_base_row(model_config, scenario, task_type, run_context),
        "served_model": llm_result.served_model or "",
        "valid_json": True,
        "schema_pass": schema_scores["schema_pass"],
        "required_fields_present": schema_scores["required_fields_present"],
        "must_include_pass": term_scores["must_include_pass"],
        "must_not_include_pass": term_scores["must_not_include_pass"],
        "no_invented_pay": check_no_invented_pay(agent_result.markdown, scenario["job_info"]),
        "latency_seconds": round(llm_result.latency_seconds, 3),
        "input_tokens": llm_result.input_tokens,
        "output_tokens": llm_result.output_tokens,
        "output_words": len(agent_result.markdown.split()),
        "estimated_cost": calculate_cost(
            model_config["model_id"], llm_result.input_tokens, llm_result.output_tokens, run_context["prices"]
        ),
        "price_date": run_context["price_date"],
        "judge_model": JUDGE_MODEL,
        **quality_scores,
        "notes": "",
    }


def _build_failed_row(
    model_config: dict,
    scenario: dict,
    task_type: str,
    error_message: str,
    run_context: dict,
) -> dict:
    """Builds the result row for a task that raised an error.

    Failures stay in the results so pass rates count them.
    """
    return {
        **_base_row(model_config, scenario, task_type, run_context),
        "served_model": "",
        "valid_json": False,
        "schema_pass": False,
        "required_fields_present": False,
        "must_include_pass": False,
        "must_not_include_pass": False,
        "no_invented_pay": None,
        "latency_seconds": None,
        "input_tokens": None,
        "output_tokens": None,
        "output_words": None,
        "estimated_cost": None,
        "price_date": run_context["price_date"],
        "judge_model": JUDGE_MODEL,
        "specificity_score": None,
        "tone_score": None,
        "faithfullness_score": None,
        "linkedin_readiness_score": None,
        "refinement_quality_score": None,
        "overall_quality_score": None,
        "judge_error": "",
        "notes": error_message[:500],
    }


def _write_results(rows: list[dict], output_dir: str) -> None:
    """Writes result rows to JSON and CSV files."""
    results_dir = Path(output_dir)
    results_dir.mkdir(parents=True, exist_ok=True)
    (results_dir / RESULT_FILES[0]).write_text(json.dumps(rows, indent=2), encoding="utf-8")
    if rows:
        with (results_dir / RESULT_FILES[1]).open("w", newline="", encoding="utf-8") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=list(rows[0].keys()))
            writer.writeheader()
            writer.writerows(rows)


if __name__ == "__main__":
    import argparse

    arg_parser = argparse.ArgumentParser(description="Run the LLM benchmark for job description generation.")
    arg_parser.add_argument("--model", default=None, help="Model ID or name to (re-)evaluate, e.g. openai/gpt-4o-mini")
    arg_parser.add_argument("--runs", type=int, default=DEFAULT_RUNS, help="Runs per model and scenario")
    arg_parser.add_argument("--workers", type=int, default=1, help="Models evaluated in parallel")
    args = arg_parser.parse_args()
    run_benchmark(target_model=args.model, runs=args.runs, workers=args.workers)
