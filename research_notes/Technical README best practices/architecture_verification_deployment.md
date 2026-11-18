# How credible products document architecture, verification, deployment, and production hardening

Scope: concrete patterns from respected projects (rust-analyzer, Supabase, Immich, Langfuse, Cal.com, Plausible, PostHog, Stripe) plus standards (ADR/MADR, GitHub badges/Mermaid, promptfoo action). Target fit: 2-person portfolio GenAI SaaS (FastAPI, vanilla JS, Supabase auth/Postgres, Stripe credit packs with atomic ledger + idempotent webhooks, OpenRouter multi-model fallbacks, Turnstile + rate limits, pytest, eval harness, custom domain). Researched 2026-11-17.

## How do respected products document architecture (format, diagrams, level of detail, data flow vs component list)?

### Takeaway
The most respected pattern is a short, stable ARCHITECTURE.md: bird's-eye view, codemap ("where is the thing that does X"), explicit invariants and boundaries, and a cross-cutting concerns section - plus one high-level diagram. Product docs (Supabase, Immich) pair a single diagram with a component list that names each service's job and how requests/jobs flow between them; detailed internals live elsewhere.

### Cited Findings
- matklad's ARCHITECTURE.md recommendations: bird's-eye overview of the problem; codemap of coarse modules and their relations; name important files/modules/types but do not link them (links go stale; symbol search works); state invariants, especially ones expressed as absence of a dependency; describe layer boundaries; separate "cross-cutting concerns" section after the codemap - [matklad, ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- matklad: "Keep it short: every recurring contributor will have to read it." Avoid explaining module internals; do not try to keep it synchronized with code; only record things unlikely to change; revisit a couple of times a year - [matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- matklad cites rust-analyzer's architecture.md as the model - [matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- rust-analyzer architecture doc structure: four top sections - Bird's Eye View, Entry Points, Code Map (one subsection per crate/dir group), Cross-Cutting Concerns (stability, cancellation, testing, error handling, observability, configurability, serialization). One embedded image only. Roughly two dozen bolded "**Architecture Invariant:**" callouts placed at the end of the relevant component (e.g. what a crate must not depend on, what must never fail). Some crates marked "**API Boundary**". ~350 lines, conversational, includes rationale - [rust-analyzer architecture.md](https://raw.githubusercontent.com/rust-lang/rust-analyzer/master/docs/book/src/contributing/architecture.md)
- rust-analyzer code map is organized by component; data flow appears only where it matters (input to lazily computed semantic model, parser event stream, cancellation on new revision, LSP request dispatch) - [rust-analyzer architecture.md](https://raw.githubusercontent.com/rust-lang/rust-analyzer/master/docs/book/src/contributing/architecture.md)
- Supabase architecture page: one diagram (API gateway in front of Auth/GoTrue, PostgREST, Realtime, Storage, pg_meta, Functions, pg_graphql, all on one Postgres), then per-component short descriptions with links to docs, source, license, language; then seven "product principles" (works in isolation, integrated, extensible, portable, long game, built for developers, supports existing tools). Explains choices like Postgres over NoSQL - [Supabase Architecture](https://supabase.com/docs/guides/getting-started/architecture)
- Immich developer architecture page: high-level image (webp) of clients calling the server REST API, plus a separate mobile-app layer diagram; sections: clients (mobile, web, CLI), server components (server, API endpoints, DTOs, background jobs, ML, Postgres, Redis). Names concrete libs (NestJS, Kysely, FastAPI, BullMQ). Lists services with one-line responsibilities (immich-server, immich-machine-learning, postgres, redis) and describes data flow: REST from clients; server reaches Redis/Postgres/ML/filesystem via repository interfaces; job chaining (smart search and face recognition run after thumbnail generation) - [Immich Architecture](https://docs.immich.app/developer/architecture)
- Immich doc has a minor inconsistency (mentions immich-microservices container in diagram section but omits it from service list) - shows how architecture docs drift - [Immich Architecture](https://docs.immich.app/developer/architecture)
- GitHub renders Mermaid natively in fenced code blocks in Markdown files, issues, PRs, discussions, wikis (also GeoJSON, TopoJSON, ASCII STL) - [GitHub Docs: Creating diagrams](https://docs.github.com/en/get-started/writing-on-github/working-with-advanced-formatting/creating-diagrams)

### Inferences
- Diagram format: Supabase and Immich use exported images; GitHub-native Mermaid is the low-maintenance choice for a small repo because it is diffable text and renders on GitHub without tooling. For a portfolio, a Mermaid flowchart (browser -> Turnstile -> FastAPI -> Supabase/Stripe/OpenRouter) plus one Mermaid sequence diagram for the payment/credit flow would cover the "data flow" that technical readers look for. An Excalidraw/PNG hero image is fine for the README's visual hook, but keep the source file (.excalidraw) in repo so it can be edited.
- Best fit for the target: rust-analyzer shape scaled down to ~100-200 lines: Bird's eye view, Request lifecycle (generate JD), Code map (backend modules, frontend, migrations, evals), Invariants (e.g. "credits are only changed through the ledger function", "webhook handler never grants credits without a verified signature + unseen event ID", "frontend never holds service-role key", "LLM fallback order is config, not code"), Cross-cutting (auth, rate limiting, observability, errors, testing).
- "Invariant" callouts are a high-signal, low-cost device: they show a reviewer that the authors thought about failure modes, which is what distinguishes a portfolio project from a tutorial clone.

### Gaps
- Did not fetch Excalidraw, Sentry, PostHog, Plausible, or Linear architecture docs directly; no verified data on their diagram tooling. Excalidraw/Sentry/Linear claims should not be made without checking.
- Diagram tool used by Supabase/Immich not stated on their pages.

## How do they show verification (CI badges, test commands, test layout, coverage, e2e, evals in CI, status pages)?

### Takeaway
Credible repos show verification through runnable commands in the README (test, e2e, report viewing) and a CI status badge, not long prose. For LLM products, evals in CI are now a recognizable signal; the promptfoo GitHub Action runs evals on PRs that touch prompts and posts pass/fail counts with thresholds.

### Cited Findings
- GitHub Actions status badge URL: `https://github.com/OWNER/REPO/actions/workflows/WORKFLOW-FILE/badge.svg`, with optional `?branch=main` and `?event=push` - [GitHub Docs: status badge](https://docs.github.com/en/actions/how-tos/monitor-workflows/add-a-status-badge)
- Langfuse README badges: MIT license, YC W23, Docker pulls, PyPI and npm downloads, Discord, X, LinkedIn, commits last month, issues closed, discussion posts - mostly popularity/community badges, not test badges - [Langfuse README](https://raw.githubusercontent.com/langfuse/langfuse/main/README.md)
- Cal.com (README now branded Cal.diy) badges: license, stars, monthly commit activity, Docker pulls, Help Wanted, Contributor Covenant - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)
- Cal.com README documents e2e (Playwright) concretely: `yarn test-e2e`, view report with `yarn playwright show-report ...`, `npx playwright install` if browsers missing, required env (NEXTAUTH_URL=http://localhost:3000), Mailhog when `E2E_TEST_MAILHOG_ENABLED=1` - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)
- rust-analyzer covers testing as a cross-cutting concern in its architecture doc, with invariants clustered in the Testing section - [rust-analyzer architecture.md](https://raw.githubusercontent.com/rust-lang/rust-analyzer/master/docs/book/src/contributing/architecture.md)
- promptfoo GitHub Action: triggers on pull_request/pull_request_target (selects changed prompt files, posts PR comment), push (workflow summary), workflow_dispatch. Inputs: `config`, `github-token` required; `prompts` globs, `fail-on-threshold` (required pass %), `repeat`/`repeat-min-pass` (handles LLM nondeterminism), `max-concurrency` (default 4), `no-share`, `no-cache`, `env-files`. PR comment shows pass/fail counts, assertion failures vs execution errors separately; it evaluates only current checkout, NOT a base-vs-head before/after diff. Disk cache needs `actions/cache` to persist across runners - [promptfoo-action](https://github.com/promptfoo/promptfoo-action)
- Langfuse itself is an LLM eval/observability product; its self-host config includes LLM-as-a-Judge retry/media settings, showing evals-as-infrastructure is mainstream - [Langfuse configuration](https://langfuse.com/self-hosting/configuration)

### Inferences
- For the target: one CI badge (tests on push to main) is enough; popularity badges (stars, downloads) look hollow on a portfolio repo. Add a short "Verification" section: `pytest` command, test layout (unit vs integration vs webhook/ledger tests), what's mocked (Stripe, OpenRouter), and how to run the eval harness with what it measures.
- Eval-in-CI fit: run the existing eval harness (or promptfoo) only on PRs that change prompts/model config, with a pass threshold and `repeat` to manage nondeterminism; keep API costs bounded by small golden sets and caching. Be honest in docs that it is a regression gate, not a quality guarantee.
- Showing a sample eval table (model x metric, with date and dataset size) in docs is more convincing than a coverage % badge.

### Gaps
- No verified source fetched on coverage badge practice (Codecov etc.) among named products, or on status pages (status.supabase.com etc.) - not researched within budget.
- No direct example found of a named product publishing eval scores in its README.

## How do they document deployment and config (env var tables, deploy buttons, Docker compose, migrations, releases)?

### Takeaway
Pattern: quick start in README (clone, copy `.env.example`, generate secrets with `openssl rand`, `docker compose up`), with a full env var reference table (Variable | Required/Default | Description) and upgrade/migration guide in separate docs. Hosted option listed first, self-host options as a bulleted menu.

### Cited Findings
- Cal.com local setup: clone, `yarn`, copy `.env.example` to `.env`, generate `NEXTAUTH_SECRET` via `openssl rand -base64 32` and `CALENDSO_ENCRYPTION_KEY` via `openssl rand -base64 24`, optional `yarn dx` for seeded Docker Postgres, `yarn dev` - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)
- Cal.com env tables only in Docker section, split run-time vs build-time (DATABASE_URL, NEXT_PUBLIC_WEBAPP_URL, NEXTAUTH_URL, NEXTAUTH_SECRET, CALENDSO_ENCRYPTION_KEY; build-time adds telemetry/legal URL vars) - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)
- Cal.com deploy options: Railway, Northflank, Vercel, Render, Elestio; migrations documented with separate dev vs production commands (`db-migrate` may clear dev DB; `db-deploy` for prod) and a check for `.env` changes after upgrades - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)
- Langfuse README deploy section: Cloud (free tier, sign-up link) then Self-Host bullet list - Docker Compose ("about 5 minutes", git clone + docker compose up, log rotation note), Kubernetes/Helm (preferred production), Terraform for AWS/Azure/GCP, community Render/Railway; links full self-host docs - [Langfuse README](https://raw.githubusercontent.com/langfuse/langfuse/main/README.md)
- Langfuse env var reference: three-column tables Variable | Required / Default | Description, ~110 variables, main table grouped by name prefix plus separate tables per feature, version notes like "Available from >=v4.61.0" - [Langfuse configuration](https://langfuse.com/self-hosting/configuration)
- Plausible CE: states requirements (Docker/Compose, CPU with SSE 4.2 or NEON for ClickHouse, ~2 GB RAM), clone at a pinned tag (`-b v3.2.1`), `.env` with BASE_URL and SECRET_KEY_BASE (64+ bytes via openssl rand), port override file for automatic Let's Encrypt, `docker compose up -d`, create first user; upgrades and full config in wiki; releases on GitHub releases - [Plausible CE](https://github.com/plausible/community-edition)
- Plausible README referenced an older version branch for its logo - small sign of doc drift - [Plausible CE](https://github.com/plausible/community-edition)

### Inferences
- For the target (hosted SaaS, not self-host product): a DEPLOYMENT.md should cover environments (local, staging?, prod), hosting provider + custom domain/TLS, env var table (Variable | Required | Where used | Example/notes - mark secrets and which are public, e.g. Turnstile site key vs secret, Supabase anon vs service-role), Supabase migrations workflow (how applied, never edit applied migrations), Stripe webhook endpoint setup per environment (separate whsec per mode/endpoint), and rollback steps.
- Pinning versions in install commands (Plausible) and splitting dev vs prod migration commands (Cal.com) are cheap credibility signals.
- One-click deploy buttons matter for self-hostable OSS; for a portfolio SaaS they add little - a live demo link and a `.env.example` are more relevant.

### Gaps
- Did not verify CHANGELOG format usage (Keep a Changelog, release-please) among named products.
- Infra diagrams in deployment docs not observed in fetched pages.

## How do they document design decisions and trade-offs (ADRs, "why we chose X", RFCs, postmortems)?

### Takeaway
Two formats dominate: lightweight ADRs in the repo (MADR: numbered markdown files in docs/decisions) and RFC-style written proposals (PostHog: problem, options, recommendation). What impresses technical readers is concrete evidence - measured numbers, rejected options and why.

### Cited Findings
- ADR = record of one architectural decision with rationale, trade-offs, consequences; collection = decision log; popularized by Michael Nygard's 2011 post; Y-statements (Zdun et al.) also cited - [adr.github.io](https://adr.github.io/)
- MADR template sections: Title; Context and Problem Statement; Decision Drivers (optional); Considered Options; Decision Outcome (optional Consequences, Confirmation); Pros and Cons of the Options (optional); More Information. Optional front matter: status, date, decision-makers, consulted, informed. Location `docs/decisions`, naming `NNNN-title-with-dashes.md`. MADR 4.0.0 released 2024-09-17, includes bare/minimal templates - [MADR](https://adr.github.io/madr/)
- PostHog: cross-team decisions go through async RFCs (problem, options, recommendation); implementing team usually decides; Temporal RFC drew 46 comments; also documents rejections with numbers (Amazon EFS: ~$600/day actual vs $300/month estimate) and prototypes (C++ SQL parsing ~120ms to ~7ms); keeps re-evaluating ClickHouse vs alternatives - [PostHog: How we choose technologies](https://posthog.com/newsletter/choosing-technologies)
- Supabase explains design choices (Postgres instead of NoSQL) directly in its architecture page via principles - [Supabase Architecture](https://supabase.com/docs/guides/getting-started/architecture)
- rust-analyzer embeds rationale and "lessons learned" inline in architecture doc - [rust-analyzer architecture.md](https://raw.githubusercontent.com/rust-lang/rust-analyzer/master/docs/book/src/contributing/architecture.md)

### Inferences
- For a 2-person portfolio: 4-6 short MADR-minimal ADRs beat a long design doc. Strong candidates: (1) credit ledger as append-only table + DB function vs balance column; (2) idempotent webhook processing via stored event IDs; (3) OpenRouter with ordered fallbacks vs single provider SDK; (4) vanilla JS vs framework; (5) Turnstile + per-user/IP rate limits; (6) eval harness design. Each with "Considered options" and one measured fact where possible (latency, cost per generation, fallback rate).
- Most impressive to technical readers (inference from PostHog/rust-analyzer style): numbers, rejected alternatives, and stated invariants; least impressive: generic "we chose X because it is popular/scalable".
- A short postmortem-style note for a real bug (e.g. duplicate webhook or race in credit deduction) would be strong evidence of production thinking, if one actually happened.

### Gaps
- Did not fetch postmortem examples (Cloudflare, GitLab, Supabase incidents) within budget.
- No reliable data comparing reader impressions across formats; ranking above is inference.

## How do they document production hardening (webhook idempotency, rate limits, auth, abuse, secrets, privacy)?

### Takeaway
Stripe's own docs define the checklist a reviewer will compare against: verify signatures on the raw body, dedupe by event ID, do not rely on event order, return 2xx fast, handle retries for up to three days, use idempotency keys on outbound POSTs. Documenting how the project meets each item is high signal. Privacy/telemetry is documented explicitly (Langfuse) with what is and isn't collected and how to opt out.

### Cited Findings
- Stripe webhooks: endpoint may receive same event more than once - log processed event IDs and skip already-logged; sometimes two distinct Event objects are generated - dedupe with `data.object` ID + `event.type` - [Stripe webhooks](https://docs.stripe.com/webhooks)
- Stripe does not guarantee event order; do not use `created` for ordering or dedupe (events can share a timestamp); track event IDs; fetch missing objects via API - [Stripe webhooks](https://docs.stripe.com/webhooks)
- Verify `Stripe-Signature` with the `whsec_` secret using the unmodified raw body; libraries default to 5-minute timestamp tolerance against replay; never use tolerance 0; constant-time compare; only `v1` scheme counts - [Stripe webhooks](https://docs.stripe.com/webhooks)
- Return 2xx quickly before complex logic; process via async queue for spikes; live-mode retries up to three days with exponential backoff (sandbox: three times over a few hours); manual resend up to 15 days (Dashboard) / 30 days (CLI) - [Stripe webhooks](https://docs.stripe.com/webhooks)
- Additional: subscribe only to needed event types; exempt webhook route from CSRF; IP allowlisting plus signature verification; roll signing secrets periodically (old secret can stay valid up to 7 days); separate secrets for test vs live and per endpoint; local testing via `stripe listen --forward-to` and `stripe trigger` - [Stripe webhooks](https://docs.stripe.com/webhooks)
- Stripe idempotency keys: for API v1, first response (status + body, including 500s) saved and replayed for same key; keys up to 255 chars, V4 UUID suggested, no sensitive data in keys; prunable after 24h; parameter mismatch errors; GET/DELETE don't need keys - [Stripe idempotent requests](https://docs.stripe.com/api/idempotent_requests)
- Stripe engineering blog (Brandur Leach, 2017-02-22): networks fail ambiguously; idempotency keys make retries safe; exponential backoff with jitter avoids thundering herd - [Stripe blog: idempotency](https://stripe.com/blog/idempotency)
- Langfuse README Security & Privacy: links dedicated security page; telemetry on by default for self-host, sends basic usage stats to PostHog, excludes traces/prompts/scores/datasets; opt out with `TELEMETRY_ENABLED=false` - [Langfuse README](https://raw.githubusercontent.com/langfuse/langfuse/main/README.md)
- Cal.com documents generating secrets with `openssl rand` and a telemetry-disable env var - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)

### Inferences
- For the target, a SECURITY / "Production hardening" section mapping each risk to mechanism + test is ideal, e.g.:
  - Webhook forgery -> raw-body signature verification (test: bad signature returns 400).
  - Duplicate delivery -> unique constraint on Stripe event ID, credit grant in same DB transaction (test: replay same event twice, balance changes once).
  - Out-of-order events -> handler keyed on checkout session/payment state, not arrival order.
  - Double spend/race on credits -> atomic ledger function / row lock (test: concurrent deductions).
  - Bot abuse / LLM cost burn -> Turnstile on generation + per-user and per-IP rate limits (document limits and 429 behavior).
  - Provider outage -> OpenRouter fallback chain with timeout and logged fallback reason.
  - Secrets -> server-only env vars, Supabase service-role key never shipped to browser, RLS on user tables.
  - Privacy -> what user inputs/outputs are stored, retention, whether prompts are sent to third-party model providers.
- Outbound idempotency keys matter less if the app only creates Checkout Sessions, but noting it shows awareness.

### Gaps
- No fetched source on how named products document rate limits or observability (e.g. Sentry/OpenTelemetry setup); Supabase RLS docs not fetched.
- Turnstile docs not fetched; no verified wording on server-side token validation (siteverify) here.

## Should a small portfolio product keep architecture/deploy docs in the README or separate files?

### Takeaway
Respected projects keep the README as a landing page (what, why, quick start, links) and push architecture, full config, and upgrade/deploy detail to separate docs. For a small project: README with a short architecture summary + one diagram + links, and separate docs/ARCHITECTURE.md, docs/DEPLOYMENT.md, docs/decisions/.

### Cited Findings
- Langfuse README keeps deploy options to a short bullet list and links full self-hosting docs; full env var reference (~110 vars) lives on separate config page - [Langfuse README](https://raw.githubusercontent.com/langfuse/langfuse/main/README.md); [Langfuse configuration](https://langfuse.com/self-hosting/configuration)
- Plausible CE README covers only 4 env vars and defers full config and upgrades to the wiki - [Plausible CE](https://github.com/plausible/community-edition)
- matklad recommends a dedicated ARCHITECTURE.md at repo level, kept short, with internals in separate docs - [matklad](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- MADR standard location is `docs/decisions` with numbered files - [MADR](https://adr.github.io/madr/)
- Cal.com is a counterexample: puts dev setup, Docker env tables, deploy options, migrations, and e2e commands all in a long README - [Cal.com README](https://raw.githubusercontent.com/calcom/cal.com/main/README.md)

### Inferences
- Recommended layout for target (lean, no bloat):
  - README.md: one-line pitch, live demo link, screenshot/GIF, CI badge, feature bullets, 6-10 line architecture summary + Mermaid diagram, quick start (5 commands), "Verification" (pytest + eval commands, latest eval snapshot), links to docs.
  - docs/ARCHITECTURE.md: matklad shape with invariants (~100-200 lines).
  - docs/DEPLOYMENT.md: environments, hosting, domain/TLS, env var table, migrations, Stripe webhook setup, rollback.
  - docs/SECURITY.md or a section in ARCHITECTURE: hardening table (risk -> mechanism -> test).
  - docs/decisions/0001-...md: 4-6 minimal ADRs.
  - docs/EVALS.md (optional): dataset, metrics, results table with date.
  - `.env.example` with comments - single source of truth the env table mirrors.
- Avoid: duplicating env lists in README and DEPLOYMENT (drift, as seen in Plausible/Immich small inconsistencies), popularity badges, and directory-tree dumps without explanation.
- Docs drift risk is real even for big projects (Immich, Plausible examples); matklad's advice to record only stable facts and use names not links is the cheapest mitigation.

### Gaps
- No authoritative survey on README length vs reader engagement; recommendation based on observed practice.
- Did not verify GitHub's own README guidance page.
