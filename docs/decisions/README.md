# Decision records

Short notes on choices that shape the code. Format: context, options, decision, consequences.

| # | Decision |
|---|---|
| [0001](0001-credit-ledger-in-postgres.md) | Credits change only through SQL functions with idempotency keys |
| [0002](0002-stripe-webhook-idempotency.md) | Credit Stripe payments per Checkout session, record events after success |
| [0003](0003-openrouter-with-fallbacks.md) | One OpenRouter client with a benchmarked primary model and ordered fallbacks |
| [0004](0004-free-generate-paid-refine.md) | Generating is free; only typed refine requests cost a credit |
| [0005](0005-rule-based-quality-check.md) | Quality check uses plain rules, not a second LLM call |
| [0006](0006-eval-harness-design.md) | Benchmark with fallbacks off, real prices and an outside judge |
