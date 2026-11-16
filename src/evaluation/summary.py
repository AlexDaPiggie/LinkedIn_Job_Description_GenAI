"""Aggregates the evaluation harness results for the public /eval page."""

import json
from collections import defaultdict
from pathlib import Path

RESULTS_PATH = Path(__file__).resolve().parent.parent.parent / "eval_results" / "model_comparison.json"
SCORE_KEYS = (
    "specificity_score",
    "tone_score",
    "faithfullness_score",
    "linkedin_readiness_score",
    "overall_quality_score",
)


def _mean(values: list[float], digits: int = 3) -> float | None:
    """Average of the numbers rounded to `digits`, or None if there are none."""
    numbers = [value for value in values if isinstance(value, (int, float))]
    return round(sum(numbers) / len(numbers), digits) if numbers else None


def summarize_results(rows: list[dict]) -> dict:
    """Builds per-model statistics from raw evaluation rows.

    Args:
        rows: Rows as written by the evaluation runner.

    Returns:
        `{"runs": n, "scenarios": n, "models": [...]}` with, per model, the
        number of runs, JSON and schema pass rates, mean scores, mean latency
        and mean cost per call, sorted by overall quality (best first).
    """
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row.get("model_id", "unknown")].append(row)

    models = []
    for model_id, items in grouped.items():
        entry = {
            "model_id": model_id,
            "runs": len(items),
            "valid_json_rate": _mean([1.0 if item.get("valid_json") else 0.0 for item in items]),
            "schema_pass_rate": _mean([1.0 if item.get("schema_pass") else 0.0 for item in items]),
            "mean_latency_seconds": _mean([item.get("latency_seconds") for item in items]),
            "mean_cost_usd": _mean([item.get("estimated_cost") for item in items], digits=6),
        }
        for key in SCORE_KEYS:
            entry[key] = _mean([item.get(key) for item in items])
        models.append(entry)

    models.sort(key=lambda entry: entry["overall_quality_score"] or 0, reverse=True)
    return {
        "runs": len(rows),
        "scenarios": len({row.get("scenario_id") for row in rows}),
        "models": models,
    }


def load_summary(path: Path = RESULTS_PATH) -> dict:
    """Loads and summarizes the results file (empty summary if missing)."""
    try:
        rows = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        rows = []
    return summarize_results(rows if isinstance(rows, list) else [])
