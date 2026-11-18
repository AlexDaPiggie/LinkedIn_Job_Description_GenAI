"""Tests for benchmark metrics and the runner's no-fallback rule (no network)."""

from src.evaluation import runner
from src.evaluation.metrics import (
    calculate_cost,
    check_no_invented_pay,
    evaluate_quality_with_judge,
)
from src.llm.client import LLMResult

PRICES = {"a/model": [1.0, 2.0]}


def test_cost_uses_snapshot_prices():
    assert calculate_cost("a/model", 1_000_000, 500_000, PRICES) == 2.0


def test_cost_is_none_for_unknown_price_or_tokens():
    assert calculate_cost("unknown/model", 100, 100, PRICES) is None
    assert calculate_cost("a/model", None, 100, PRICES) is None


def _judge_reply(text):
    def fake_generate(prompt, **kwargs):
        assert kwargs["temperature"] == 0.0
        return LLMResult(text=text, model="judge", latency_seconds=0.0)
    return fake_generate


def test_judge_overall_is_computed_in_code():
    reply = '{"specificity_score": 4, "tone_score": 5, "faithfullness_score": 3, "linkedin_readiness_score": 4, "refinement_quality_score": 5}'
    generate_scores = evaluate_quality_with_judge("jd", {}, "generate", generate_text_fn=_judge_reply(reply))
    assert generate_scores["refinement_quality_score"] is None
    assert generate_scores["overall_quality_score"] == 4.0
    refine_scores = evaluate_quality_with_judge("jd", {}, "refine", "shorter", generate_text_fn=_judge_reply(reply))
    assert refine_scores["overall_quality_score"] == 4.2


def test_judge_failure_gives_none_not_zero():
    scores = evaluate_quality_with_judge("jd", {}, "generate", generate_text_fn=_judge_reply("not json"))
    assert scores["overall_quality_score"] is None
    assert scores["judge_error"]


def test_invented_pay_is_caught_only_without_pay_input():
    assert not check_no_invented_pay("Salary: $120,000 per year", {})
    assert not check_no_invented_pay("Pay 90k plus bonus", {})
    assert check_no_invented_pay("Competitive pay and bonus", {})
    assert check_no_invented_pay("Salary: $120,000", {"pay_min": 100000})


def test_benchmark_calls_skip_fallback_models(monkeypatch):
    seen = {}

    def fake_generate_text(prompt, provider, model, **kwargs):
        seen.update(kwargs, model=model)
        return LLMResult(text="ok", model=model, latency_seconds=0.0)

    monkeypatch.setattr(runner, "generate_text", fake_generate_text)
    runner.generate_without_fallback("p", "openrouter", "a/model", fallback_models=["b/model"])
    assert seen == {"model": "a/model"}
