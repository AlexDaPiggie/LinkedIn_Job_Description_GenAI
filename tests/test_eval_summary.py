"""Tests for the public evaluation summary."""

from fastapi.testclient import TestClient

from src.api.main import app
from src.evaluation.summary import load_summary, summarize_results

ROWS = [
    {"model_id": "a", "scenario_id": "s1", "valid_json": True, "schema_pass": True, "latency_seconds": 2.0,
     "estimated_cost": 0.001, "overall_quality_score": 4.0},
    {"model_id": "a", "scenario_id": "s2", "valid_json": True, "schema_pass": False, "latency_seconds": 4.0,
     "estimated_cost": 0.003, "overall_quality_score": 5.0},
    {"model_id": "b", "scenario_id": "s1", "valid_json": False, "schema_pass": False, "latency_seconds": 1.0,
     "estimated_cost": 0.0001, "overall_quality_score": 4.9},
]


def test_summary_groups_and_sorts_by_quality():
    summary = summarize_results(ROWS)
    assert summary["runs"] == 3 and summary["scenarios"] == 2
    assert [m["model_id"] for m in summary["models"]] == ["b", "a"]
    first = summary["models"][1]
    assert first["overall_quality_score"] == 4.5
    assert first["schema_pass_rate"] == 0.5
    assert first["mean_latency_seconds"] == 3.0
    assert first["mean_cost_usd"] == 0.002


def test_missing_file_gives_empty_summary(tmp_path):
    assert load_summary(tmp_path / "nope.json") == {"runs": 0, "scenarios": 0, "models": []}


def test_endpoint_returns_summary():
    response = TestClient(app).get("/api/eval-summary")
    assert response.status_code == 200 and "models" in response.json()
