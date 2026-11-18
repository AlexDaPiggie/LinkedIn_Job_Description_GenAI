# Deployment

Production runs as one Docker container on **Google Cloud Run** (us-central1),
behind **Cloudflare**, at https://www.linkedingenai.com. FastAPI serves both
the API and the static front end, so there is one service to deploy.

The app starts without most settings, but payments and abuse protection only
turn on once every step below is done.

## 1. Environment variables

Copy `.env.example`. On Cloud Run, set these as service env vars (secrets in
Secret Manager).

| Variable | Required | Default | Used by | Secret |
|---|---|---|---|---|
| `OPENROUTER_API_KEY` | yes | - | `src/llm/providers.py` | yes |
| `SUPABASE_URL` | yes | - | `src/database/supabase_client.py` | no |
| `SUPABASE_ANON_KEY` | yes | - | auth flows | no |
| `SUPABASE_SERVICE_ROLE_KEY` | for credits | - | credit ledger | yes |
| `STRIPE_SECRET_KEY` | for payments | - | `src/api/routers/payments.py` | yes |
| `STRIPE_WEBHOOK_SECRET` | for payments | - | webhook signature check | yes |
| `TURNSTILE_SITE_KEY` | optional | - | sent to the browser | no |
| `TURNSTILE_SECRET_KEY` | optional | - | `src/security/turnstile.py` | yes |
| `GUEST_DAILY_LIMIT` | optional | 10 | free LLM calls per IP per day | no |
| `GLOBAL_DAILY_LLM_CALLS` | optional | 3000 | daily kill switch | no |
| `USER_HOURLY_LIMIT` | optional | 60 | calls per signed-in user per hour | no |
| `TRUSTED_PROXY_HOPS` | optional | 1 | proxies in front of the app | no |
| `DISPOSABLE_EMAIL_DOMAINS` | optional | empty | extra blocked domains | no |

## 2. Database (Supabase)

1. Run `docs/migrations/001_credit_ledger.sql` once in the SQL editor. It is
   safe to re-run.
2. It adds the tables `credit_ledger`, `stripe_events`, `free_grants`,
   `usage_events` and the functions `spend_credits`, `refund_credits`,
   `grant_credits`, `claim_stripe_event`, `claim_free_grant`.
3. New users get 20 free credits from `claim_free_grant` after confirming
   their email. Existing balances are not changed.
4. Until the migration runs, credit operations fail closed. Do not deploy
   without it.
5. Set up custom SMTP in Supabase Auth (Resend, Brevo or similar). The
   built-in email is heavily rate limited.

## 3. Stripe

- Prices come from code (`src/credits/packs.py`): $5 = 20, $10 = 40,
  $20 = 80 credits. No Stripe products are needed.
- Webhook endpoint: `POST /webhook`. Subscribe to
  `checkout.session.completed` and `checkout.session.async_payment_succeeded`.
- Test mode and live mode have separate endpoints and separate signing secrets.
- Local testing:

```bash
stripe listen --forward-to localhost:8000/webhook
```

- After setup, replay an event and confirm credits are not added twice.

## 4. Cloudflare Turnstile

Create a widget for your domains and set `TURNSTILE_SITE_KEY` and
`TURNSTILE_SECRET_KEY`. When unset, the check is skipped (fine for local work).

## 5. Build and deploy

```bash
gcloud run deploy linkedingenai --source . --region us-central1
```

The Dockerfile installs `requirements.txt`, runs as a non-root user and starts
`uvicorn src.api.main:app` on `$PORT`.

## 6. Check after deploying

- `GET /health` returns 200.
- **Client IP:** send `curl -H "X-Forwarded-For: 1.2.3.4" https://<host>/config`
  and confirm the guest limit is not keyed on `1.2.3.4`. If every visitor
  looks like one IP, adjust `TRUSTED_PROXY_HOPS`.
- Buy the $5 pack in Stripe test mode and confirm 20 credits arrive once.

## Rollback

Cloud Run keeps earlier revisions. Send traffic back to the last good one:

```bash
gcloud run services update-traffic linkedingenai --to-revisions <REVISION>=100 --region us-central1
```

Database migrations are additive, so rolling back the app does not need a
database rollback.
