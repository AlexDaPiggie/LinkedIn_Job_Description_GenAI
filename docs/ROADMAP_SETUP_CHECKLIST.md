# Setup checklist for the roadmap changes

The code works without these steps (features degrade safely), but money safety
and abuse protection only turn on once you finish them.

## 1. Database (Supabase SQL editor) - REQUIRED for safe credits

1. Run `docs/migrations/001_credit_ledger.sql` once. Safe to re-run.
2. It adds: `credit_ledger`, `stripe_events`, `free_grants`, `usage_events`, and
   the functions `spend_credits`, `refund_credits`, `grant_credits`,
   `claim_stripe_event`, `claim_free_grant`.
3. It sets `profiles.credits` default to 0. New users now get their 20 free
   credits from `claim_free_grant` after confirming their email.
4. Existing balances are not changed.
5. Until you run it, credit operations fail closed: refine returns an error, Stripe webhooks
   return 500 (Stripe retries them, so no payment is lost) and new signups get 0 credits.
   Do not deploy without it.

6. Add `SUPABASE_SERVICE_ROLE_KEY` (Supabase > Project settings > API > service_role) to the server env.
   The credit functions are locked away from the public anon key on purpose, so only the server can call them.
   Never put this key in the front end. Without it, credit operations fail closed.

## 2. Stripe

- Prices now come from code (`src/credits/packs.py`): $5 = 20, $10 = 40, $20 = 80 credits.
  No Stripe products needed.
- Webhook endpoint stays `POST /webhook`. Subscribe to `checkout.session.completed`
  (and optionally `checkout.session.async_payment_succeeded`).
- Env vars: `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET` (unchanged).
- Test with Stripe test cards, then check that a repeated webhook does not add credits twice.
- Old call `POST /create-checkout-session?user_id=...&amount=...` is gone. The new call needs the
  sign-in token and a JSON body `{pack_id, redirect_url}`. Deploy the front end and back end together.

## 3. Cloudflare Turnstile (free bot check for guests and signup)

1. Create a widget at the Cloudflare dashboard (Turnstile), add your domains.
2. Set env vars on the back end: `TURNSTILE_SECRET_KEY`, `TURNSTILE_SITE_KEY`.
3. If unset, the check is skipped (fine for local work).

## 4. Env vars for limits (all optional)

| Variable | Default | Meaning |
|---|---|---|
| `GUEST_DAILY_LIMIT` | 10 | Free LLM calls per IP per day for guests |
| `GLOBAL_DAILY_LLM_CALLS` | 3000 | Daily kill switch across everyone |
| `USER_HOURLY_LIMIT` | 60 | LLM calls per signed-in user per hour |
| `TRUSTED_PROXY_HOPS` | 1 | Number of proxies in front of the app (see below) |
| `DISPOSABLE_EMAIL_DOMAINS` | empty | Extra blocked email domains, comma separated |

**Check the real client IP on Hugging Face Spaces.** After deploying, send a request with a fake
header, for example `curl -H "X-Forwarded-For: 1.2.3.4" https://<space>/config`, and confirm the guest
counter is not keyed on `1.2.3.4`. If every visitor looks like one IP, set `TRUSTED_PROXY_HOPS=0`
and rely on the Turnstile check plus the global cap instead. Counters live in memory and reset on restart.

## 5. Email (custom SMTP)

Supabase built-in email is heavily rate limited (reported around 2 per hour). Set up custom SMTP in
Supabase Auth settings (Resend, Brevo, or similar free tiers) so signup codes are not blocked.

## 6. Keep the Space awake (optional)

Free Hugging Face Spaces sleep after inactivity. Add a free uptime pinger (for example UptimeRobot)
hitting `GET /health` every 5 to 10 minutes. `config.js` already sends a wake-up request on page load.

## 7. Things I could not do for you

- Get listed in "best free JD generator" roundups (outreach).
- Decide to open-source the repo. The linter in `src/quality` is ready to publish alone.
- A/B tests and conversion tracking beyond the simple `usage_events` table. Query it in Supabase to see
  which quick-edit chips and packs people click.
- Legal review. Pay-law notes are summaries, not legal advice. Penalty amounts were not verified.
- Cost per JD: measure real token use from your provider dashboard. The README numbers are estimates.

## 8. Run locally

`python -m pytest tests -q --ignore=tests/test_all_models.py` runs the new tests (no network).
