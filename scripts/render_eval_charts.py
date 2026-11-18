"""Renders the benchmark charts and summary table from the raw results.

Charts are generated only from eval_results/model_comparison.json, so they
can always be traced back to the data. Run after the benchmark:

    python scripts/render_eval_charts.py
"""

import json
import statistics
import sys
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from src.llm.models import MODEL_FALLBACKS  # noqa: E402

RESULTS = ROOT / "eval_results" / "model_comparison.json"
IMAGES = ROOT / "docs" / "images"
TABLE = ROOT / "eval_results" / "summary.md"

PRIMARY = next(iter(MODEL_FALLBACKS))
FALLBACKS = MODEL_FALLBACKS[PRIMARY]
INK, MUTED, GRID = "#1f2328", "#8a8f98", "#e6e8eb"
BAR, BAR_PRIMARY, BAR_FALLBACK = "#c9ced6", "#0a66c2", "#7fa9d6"
LINE_IN, LINE_OUT, LINE_SCORE = "#b7791f", "#2f855a", "#c53030"


def short_name(model_id: str) -> str:
    """Drops the vendor prefix: 'openai/gpt-4o-mini' -> 'gpt-4o-mini'."""
    return model_id.split("/", 1)[-1].replace("-instruct", "")


def mean(values):
    numbers = [value for value in values if isinstance(value, (int, float))]
    return statistics.fmean(numbers) if numbers else None


def summarize(rows: list[dict]) -> list[dict]:
    """Per-model statistics. Failed calls count in pass rates, not in timings."""
    grouped = defaultdict(list)
    for row in rows:
        grouped[row["model_id"]].append(row)

    stats = []
    for model_id, items in grouped.items():
        ok = [item for item in items if item["valid_json"]]
        latencies = sorted(item["latency_seconds"] for item in ok if item["latency_seconds"] is not None)
        rule_pass = [
            item for item in ok
            if item["must_include_pass"] and item["must_not_include_pass"]
        ]
        stats.append({
            "model_id": model_id,
            "calls": len(items),
            "ok": len(ok),
            "rule_pass": len(rule_pass),
            "sections": sum(1 for item in ok if item["required_fields_present"]),
            "no_invented_pay": sum(1 for item in ok if item.get("no_invented_pay")),
            "median_latency": statistics.median(latencies) if latencies else None,
            "max_latency": latencies[-1] if latencies else None,
            "p90_latency": latencies[min(len(latencies) - 1, int(0.9 * len(latencies)))] if latencies else None,
            "input_tokens": mean(item["input_tokens"] for item in ok),
            "output_tokens": mean(item["output_tokens"] for item in ok),
            "cost": mean(item["estimated_cost"] for item in ok),
            "judge": mean(item["overall_quality_score"] for item in ok),
            "judged": sum(1 for item in ok if isinstance(item["overall_quality_score"], (int, float))),
            "words": mean(item.get("output_words") for item in ok),
        })
    return stats


def bar_colors(model_ids):
    return [
        BAR_PRIMARY if model_id == PRIMARY else BAR_FALLBACK if model_id in FALLBACKS else BAR
        for model_id in model_ids
    ]


def style_axes(axis):
    axis.spines[["top"]].set_visible(False)
    axis.tick_params(colors=INK, labelsize=9)
    axis.grid(axis="y", color=GRID, linewidth=0.8)
    axis.set_axisbelow(True)


def caption(fig, meta: str):
    fig.text(0.01, 0.01, meta, fontsize=8, color=MUTED, ha="left", va="bottom", wrap=True)


def cost_chart(stats, meta):
    data = sorted((s for s in stats if s["cost"] is not None), key=lambda s: s["cost"])
    names = [short_name(s["model_id"]) for s in data]
    fig, cost_axis = plt.subplots(figsize=(12, 5.6))
    style_axes(cost_axis)
    cost_axis.bar(names, [s["cost"] * 1000 for s in data], color=bar_colors(s["model_id"] for s in data), width=0.6)
    cost_axis.set_yscale("log")
    cost_axis.set_ylabel("Mean cost per 1,000 calls (USD, log scale)", color=INK)
    cost_axis.set_title("Cost per call vs tokens used", color=INK, loc="left", fontsize=13, pad=30)
    cost_axis.tick_params(axis="x", rotation=45)
    plt.setp(cost_axis.get_xticklabels(), ha="right")

    token_axis = cost_axis.twinx()
    token_axis.plot(names, [s["input_tokens"] for s in data], color=LINE_IN, marker="o", ms=4, lw=1.6, label="Input tokens")
    token_axis.plot(names, [s["output_tokens"] for s in data], color=LINE_OUT, marker="s", ms=4, lw=1.6, label="Output tokens")
    token_axis.set_ylabel("Mean tokens per call", color=INK)
    token_axis.set_ylim(bottom=0)
    token_axis.spines[["top"]].set_visible(False)
    token_axis.tick_params(colors=INK, labelsize=9)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=BAR_PRIMARY, label="Primary model"),
        plt.Rectangle((0, 0), 1, 1, color=BAR_FALLBACK, label="Fallback models"),
        plt.Rectangle((0, 0), 1, 1, color=BAR, label="Other candidates"),
    ] + token_axis.get_legend_handles_labels()[0]
    cost_axis.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=5, frameon=False, fontsize=9)
    caption(fig, meta)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(IMAGES / "eval_cost_and_tokens.png", dpi=160)
    plt.close(fig)


def latency_chart(stats, meta):
    data = sorted((s for s in stats if s["median_latency"] is not None), key=lambda s: s["median_latency"])
    names = [short_name(s["model_id"]) for s in data]
    medians = [s["median_latency"] for s in data]
    spreads = [s["p90_latency"] - s["median_latency"] for s in data]
    fig, latency_axis = plt.subplots(figsize=(12, 5.6))
    style_axes(latency_axis)
    latency_axis.bar(names, medians, color=bar_colors(s["model_id"] for s in data), width=0.6,
                     yerr=[[0] * len(data), spreads], error_kw={"ecolor": MUTED, "elinewidth": 1, "capsize": 2})
    latency_axis.set_ylabel("Seconds per call (bar: median, whisker: p90)", color=INK)
    latency_axis.set_title("Latency vs judge score", color=INK, loc="left", fontsize=13, pad=30)
    latency_axis.tick_params(axis="x", rotation=45)
    plt.setp(latency_axis.get_xticklabels(), ha="right")

    score_axis = latency_axis.twinx()
    score_axis.plot(names, [s["judge"] for s in data], color=LINE_SCORE, marker="o", ms=4, lw=1.6, label="Judge score")
    score_axis.set_ylim(1, 5)
    score_axis.set_ylabel("Mean judge score (1-5, full scale)", color=INK)
    score_axis.spines[["top"]].set_visible(False)
    score_axis.tick_params(colors=INK, labelsize=9)
    handles = [
        plt.Rectangle((0, 0), 1, 1, color=BAR_PRIMARY, label="Primary model"),
        plt.Rectangle((0, 0), 1, 1, color=BAR_FALLBACK, label="Fallback models"),
        plt.Rectangle((0, 0), 1, 1, color=BAR, label="Other candidates"),
    ] + score_axis.get_legend_handles_labels()[0]
    latency_axis.legend(handles=handles, loc="lower left", bbox_to_anchor=(0, 1.02), ncol=4, frameon=False, fontsize=9)
    caption(fig, meta)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(IMAGES / "eval_latency_and_quality.png", dpi=160)
    plt.close(fig)


def fmt(value, pattern):
    return pattern.format(value) if value is not None else "-"


def write_table(stats, rows):
    header = (
        "| Model | Calls OK | Term checks | All core sections | No invented pay | Median latency (s) | Max latency (s) "
        "| Tokens in / out | $ per 1k calls | Judge (1-5) | Words |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
    )
    lines = []
    for s in sorted(stats, key=lambda s: (s["judge"] is None, -(s["judge"] or 0))):
        role = " (primary)" if s["model_id"] == PRIMARY else " (fallback)" if s["model_id"] in FALLBACKS else ""
        lines.append(
            f"| `{s['model_id']}`{role} | {s['ok']}/{s['calls']} | {s['rule_pass']}/{s['ok']} "
            f"| {s['sections']}/{s['ok']} | {s['no_invented_pay']}/{s['ok']} | {fmt(s['median_latency'], '{:.1f}')} "
            f"| {fmt(s['max_latency'], '{:.1f}')} "
            f"| {fmt(s['input_tokens'], '{:.0f}')} / {fmt(s['output_tokens'], '{:.0f}')} "
            f"| {fmt(s['cost'] * 1000 if s['cost'] is not None else None, '{:.2f}')} "
            f"| {fmt(s['judge'], '{:.2f}')} (n={s['judged']}) | {fmt(s['words'], '{:.0f}')} |"
        )
    first = rows[0]
    note = (
        f"Run `{first['run_id']}`, prices from OpenRouter on {first['price_date']}, "
        f"judge `{first['judge_model']}`. Generated by `scripts/render_eval_charts.py`.\n\n"
    )
    TABLE.write_text("# Benchmark summary\n\n" + note + header + "\n".join(lines) + "\n", encoding="utf-8")


def main():
    rows = json.loads(RESULTS.read_text(encoding="utf-8"))
    IMAGES.mkdir(parents=True, exist_ok=True)
    stats = summarize(rows)
    failures = {s["model_id"]: s["calls"] - s["ok"] for s in stats}
    runs = max(row["run_index"] for row in rows)
    scenarios = len({row["scenario_id"] for row in rows})
    meta = (
        f"{len(stats)} models x {scenarios} scenarios x (generate + refine) x {runs} runs = {len(rows)} calls. "
        f"Run {rows[0]['run_id']}. Prices: OpenRouter list price on {rows[0]['price_date']}. "
        f"Judge: {rows[0]['judge_model']}.\n"
        "Fallbacks off. Failed calls are excluded from timings and costs ("
        + ", ".join(f"{short_name(model_id)}: {count} failed" for model_id, count in failures.items() if count)
        + "). Full table: eval_results/summary.md."
    )
    cost_chart(stats, meta)
    latency_chart(stats, meta)
    write_table(stats, rows)
    print(f"Wrote charts to {IMAGES} and table to {TABLE}")


if __name__ == "__main__":
    main()
