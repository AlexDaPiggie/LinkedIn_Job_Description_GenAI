# 0003 - OpenRouter with a benchmarked primary and ordered fallbacks

**Context.** The first version had separate clients for OpenAI and Hugging Face.
Each provider had its own errors and outages, and switching models meant code
changes.

**Options.**
1. One client per provider.
2. One OpenAI-compatible client pointed at OpenRouter, with the model as data.

**Decision.** Option 2. `src/llm/client.py` tries the primary model, then each
model in `MODEL_FALLBACKS`. The primary and the order were picked from the
benchmark (cost, latency, rule checks, judge score) - see
[EVALS.md](../EVALS.md).

**Consequences.** Swapping a model is a config change. An outage of one model
costs a retry, not a failed request. OpenRouter adds a small routing overhead and
may route one model to different upstream hosts.
