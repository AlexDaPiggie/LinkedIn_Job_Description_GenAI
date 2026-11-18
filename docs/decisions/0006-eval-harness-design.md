# 0006 - Benchmark with fallbacks off, real prices and an outside judge

**Context.** The first benchmark ran each model once, priced 17 of 22 models with
a placeholder rate, used gpt-4o-mini as the judge while also testing it, scored
judge failures as 0, and could silently fall back to another model.

**Options.**
1. Keep the quick benchmark and caveat it.
2. Fix the method and re-run.

**Decision.** Option 2:
- Fallbacks off in the benchmark; the served model is recorded per call.
- Costs from a dated snapshot of OpenRouter list prices; unknown prices stay
  empty instead of guessed.
- Judge from a family that is not a candidate (`anthropic/claude-haiku-4.5`),
  temperature 0, overall score computed in code, failures stored as empty with
  the error.
- Three runs per model and scenario, with run ID and timestamps.
- A binary "no invented pay" check next to the judge scores.

**Consequences.** Every number in the charts can be traced to a row and a price
date. The old results are kept in `eval_results/archive/` for comparison.
Remaining limits are listed in [EVALS.md](../EVALS.md).
