# Security and abuse protection

Each risk, the mechanism that handles it, and the test that proves it.
Tests are in `tests/test_api_billing_and_limits.py` unless noted.

| Risk | Mechanism | Test |
|---|---|---|
| Forged Stripe webhook | Signature checked on the raw body with `STRIPE_WEBHOOK_SECRET` | `test_webhook_rejects_bad_signature` |
| Duplicate webhook delivery | Credits keyed on the Checkout session ID; event ID recorded after success | `test_fulfill_grants_pack_credits_once_keyed_on_session` |
| Webhook fails mid-way | Returns 500 so Stripe retries; nothing is marked done until credits land | `test_webhook_failure_returns_500_so_stripe_retries` |
| Tampered or unpaid session | Only paid sessions with a known pack are fulfilled | `test_fulfill_ignores_unpaid_or_tampered_sessions` |
| Client sets its own price | Packs and prices live on the server (`src/credits/packs.py`) | `test_checkout_uses_server_side_pack_and_safe_redirect` |
| Open redirect after checkout | Return URL must match an allowlist | `test_redirect_allowlist` |
| Credit double spend | One SQL function checks and subtracts in one step, keyed per request | `test_refine_charges_one_credit_on_success` |
| Paying for a failed answer | Credit refunded if the model fails before any text | `test_refine_refunds_when_llm_fails` |
| Ledger not set up | Credit operations fail closed | `test_ledger_fails_closed_when_sql_functions_missing` |
| Bots burning LLM spend | Cloudflare Turnstile, per-IP daily limit, global daily cap | `test_guest_daily_limit_blocks_after_ten`, `test_global_cap_is_a_kill_switch` |
| Forged client IP | Only the trusted right-most `X-Forwarded-For` hop is used | `test_client_ip_ignores_forged_left_side_of_forwarded_for` |
| Free-credit farming | One free grant per normalized mailbox; disposable domains blocked | `test_normalize_email_collapses_aliases`, `test_signup_blocks_disposable_email` |
| Prompt injection from uploads | File text cleaned, capped and wrapped as data; extracted fields filtered | `test_extracted_data_is_cleaned` |
| Model invents pay | Pay is added by code, never by the model; benchmark checks it too | `tests/test_eval_metrics.py` |
| Secret exposure | Service-role and Stripe keys are server-only env vars | Code review; see `.env.example` |

## Data handling

- Stored in Supabase: account email, credit balance, credit ledger entries,
  Stripe event IDs, and simple usage events (which buttons were clicked).
- Job details typed by users are sent to the model provider through OpenRouter
  to generate the draft. They are not stored in our database.
- Payments are handled by Stripe Checkout. Card details never reach this app.

## Known limits

- Rate-limit counters live in memory, so they reset when the container restarts
  and are not shared across instances.
- The quality check is a screening aid for wording, not legal advice.

## Reporting a problem

Please open a private security advisory on GitHub or contact the maintainers
through the links in the README. Do not open a public issue for security bugs.
