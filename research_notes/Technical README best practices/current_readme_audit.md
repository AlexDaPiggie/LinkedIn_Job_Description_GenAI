# Current README and docs audit (LinkedIn_Job_Description_GenAI)

Scope: README.md (207 lines), docs/ROADMAP_SETUP_CHECKLIST.md, docs/migrations/, front_end/architecture.html, front_end/eval.html, eval_results/, src/evaluation/ (runner, metrics, scenarios, summary, notebook), src/quality/README.md, tests/, pyproject.toml, requirements.txt, Dockerfile, .dockerignore, git history. Audit date 2026-11-17. All sources are local repo files; "Source" links are repo-relative paths with line numbers. Nothing in the project was edited.

## 1. Writing problems: typos, inflated claims, voice, tone, duplication, outdated facts

### Takeaway
The README's top half reads as marketing copy, with unprovable superlatives ("better than most free-tier AI models", "guarantees") and several typos. Several facts are out of date: provider list, API key names, venv instructions and the clone URL. The best-written docs in the repo are the newer ones (ROADMAP checklist, src/quality/README.md, eval.html), and their plain, precise tone shows how the README should sound.

### Cited Findings

Typos and grammar (README.md):
- L1 heading "Linked In GenAI(Click to see the Website)": the product name is spelled 3 different ways in the repo ("Linked In GenAI" L1, "linked-in-gen-ai" L17, "LinkedInGenAI" in front_end/eval.html and architecture.html nav). There is also a missing space before "(", and "(Click to see...)" inside an H1 is a UI instruction, not a title. - [README.md L1-2](README.md)
- L17 "withotu" -> "without". - [README.md L17](README.md)
- L29 "ouptut" -> "output"; L31 "converst" -> "converts"; L35 "will blocks" -> "will block"; L151 "less that 2 seconds" -> "less than". - [README.md L29, L31, L35, L151](README.md)
- L25 "(e.g. company's name, length, tone,...)" uses e.g. and an ellipsis together; L33 "feedbacks" (not countable in English). - [README.md L25, L33](README.md)
- L15 "Job Description Forms" / "user's descriptions": the output is a job posting, not a form. - [README.md L15](README.md)
- The notebook has typos too ("Averate Pass Rate", "Complexede Cases", "qwern 2.5 coder 42b" when the model is 32b), and so does the judge prompt ("sepcificity_score", "responsibilites"). The judge prompt typo sits inside the scoring prompt itself. - [src/evaluation/Model_Comparison_Analysis.ipynb cells 3, 6, 9](src/evaluation/Model_Comparison_Analysis.ipynb); [src/evaluation/metrics.py L36](src/evaluation/metrics.py)
- models.py `purpose` strings have typos ("versin", "abilties", "fomratting complexed", "decenet", "differnt", "heavire"). These strings show up in test IDs and pytest output. - [src/llm/models.py L43-127](src/llm/models.py)

Inflated or unverifiable claims:
- "Better than most free-tier AI models, our app guarantees the output with professional LinkedIn Layout" - no comparison against free-tier chat apps exists anywhere in the repo. The eval only compares API models with each other. Unbacked: remove, or replace with a concrete mechanism ("output is validated against a Pydantic schema; malformed JSON is retried once"). - [README.md L16](README.md); retry logic at [src/agent/job_agent.py L132-134](src/agent/job_agent.py)
- "Different from other apps on the market which just generate ... allowing users to refine their output as much as they want without losing any information" - a competitor claim with no evidence. Refine also costs 1 credit, so "as much as they want" sits awkwardly next to L19. "Without losing any information" is not tested. Rewrite as a feature statement. - [README.md L17, L19](README.md)
- "Guarantee LinkedIn Format ... guaranteeing the output to always follow LinkedIn format, minimize hallucination" - the schema guarantees JSON structure, not "LinkedIn format", and schema validation does nothing about hallucination. The eval data shows schema failures for several models (claude-3-haiku 6/8, gemini-2.5-pro 7/8, qwen-2.5-7b 10/13, qwen3.5-flash 3/6 schema_pass). Rewrite as "validated against `JobDescriptionDraft`; retried once on malformed JSON, else a clear error". - [README.md L29](README.md); [eval_results/model_comparison.csv](eval_results/model_comparison.csv) (computed)
- "100% test-case pass rate" for gemini-2.5-flash-lite: true only under the notebook's definition (schema_pass AND must_include AND must_not_include = 8/8). The stricter `required_fields_present` check is 3/8 for that model. "100%" is also over n=8 calls (4 scenarios x 2 tasks, 1 run each). openai/gpt-4o also scores 8/8. Needs the definition and the n stated. - [README.md L159](README.md); [Model_Comparison_Analysis.ipynb cell 3](src/evaluation/Model_Comparison_Analysis.ipynb); computed from [eval_results/model_comparison.csv](eval_results/model_comparison.csv)
- "latency < 2s" for the primary model and "gemini-2.5-flash-lite and gpt-4o-mini can generate a draft in less that 2 seconds" are **contradicted by the data**. Mean latency_seconds is 2.87 s for gemini-2.5-flash-lite and 5.32 s for gpt-4o-mini (8 rows each). gpt-4o (3.03 s) is the second-fastest, not gpt-4o-mini. Fix the numbers or remove. - [README.md L151, L159](README.md); [eval_results/model_comparison.csv](eval_results/model_comparison.csv) (computed); visible in [src/output/eval_latency_comparison.png](src/output/eval_latency_comparison.png)
- "Token Efficiency: Models like gpt-4o-mini generated structured drafts without token hike" is vague ("token hike" is not a term) and gives no number. - [README.md L141](README.md)
- "Most Cost-Effective: phi4, llama-3.3-70b, mistral-small, gpt-4o-mini": the order matches the CSV means (phi-4 $0.000122, llama-3.3-70b $0.000228, mistral-small $0.000237, gpt-4o-mini $0.000297). But see section 3: only 5 of the 22 evaluated models have real prices in the pricing table. - [README.md L140](README.md); [src/evaluation/metrics.py L10-19](src/evaluation/metrics.py)
- "atomic credit ledger and idempotent webhooks" is backed by code: `spend_credits`, `claim_stripe_event` in the SQL migration and [src/credits/ledger.py](src/credits/ledger.py). It is also covered by 40 tests in [tests/test_api_billing_and_limits.py](tests/test_api_billing_and_limits.py). Keep it, and link the evidence. - [docs/ROADMAP_SETUP_CHECKLIST.md L8-11](docs/ROADMAP_SETUP_CHECKLIST.md)

Outdated or wrong facts:
- Authors row: "multi-provider LLM client (OpenAI, Hugging Face, OpenRouter)". The code is OpenRouter only: "The provider is currently always OpenRouter" (client.py docstring). providers.py reads only `OPENROUTER_API_KEY`, and no Hugging Face client exists. - [README.md L8](README.md); [src/llm/client.py](src/llm/client.py) generate_text docstring; [src/llm/providers.py L1, L34](src/llm/providers.py)
- Prerequisites list `OPENAI_API_KEY`, `HUGGINGFACE_API_KEY`, `SUPABASE_KEY`. None of these is read by the code. The code reads `OPENROUTER_API_KEY`, `SUPABASE_URL`, `SUPABASE_ANON_KEY`, `SUPABASE_SERVICE_ROLE_KEY`, `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `TURNSTILE_SECRET_KEY`, `TURNSTILE_SITE_KEY`, plus optional `GUEST_DAILY_LIMIT`, `GLOBAL_DAILY_LLM_CALLS`, `USER_HOURLY_LIMIT`, `TRUSTED_PROXY_HOPS`, `DISPOSABLE_EMAIL_DOMAINS`. Someone following the README cannot run the app. - [README.md L68, L85-88](README.md); `grep os.getenv src/` (src/llm/providers.py L34, src/api/config.py, src/security/*.py, src/database/supabase_client.py L40)
- There is no `.env.example` file, so the full env var list exists only in scattered code and in the ROADMAP checklist. - repo root (file absent)
- venv instructions (L77-80) conflict with how the owner works (global env). They also give Windows-first commands, with Linux in a comment. pyproject.toml has a `[project.optional-dependencies] dev = [pytest]` group that the README never mentions. - [README.md L77-83](README.md); [pyproject.toml L23-26](pyproject.toml)
- Clone URL `github.com/AlexDaPiggie/LinkedIn_Job_Description_GenAI.git`, but the git remote is `AlexDaPiggie/LinkedIn_Job_Description_Generator`. The OpenRouter referer header also uses `..._Generator`. GitHub may redirect a renamed repo, but the names are inconsistent. - [README.md L74](README.md); `git remote -v`; [src/llm/providers.py L11](src/llm/providers.py)
- Frontend setup says serve on port 3000, but `src/config.json` lists `FRONT_END_URL: http://127.0.0.1:5500` (Live Server). `front_end/config.js` uses `API_BASE_URL = ""` (same origin), and FastAPI already serves the frontend at `/`. The separate frontend step is therefore not needed: running uvicorn alone serves the whole app. - [README.md L97-104](README.md); [src/config.json](src/config.json); [front_end/config.js L2](front_end/config.js); [src/api/main.py L45-47](src/api/main.py)
- Pipeline step 6, "Billing & Auth Check: Deducts 1 credit in Supabase before running LLM", is listed last but happens before the LLM call. It also applies only to refine now, since generation is free per L19. Step order and wording are stale. - [README.md L54-59](README.md)
- The pipeline (L54-59) leaves out the quality linter, retry-once and doc-upload extraction steps that architecture.html describes. The README and the site tell different stories. - [front_end/architecture.html](front_end/architecture.html) "The five steps"
- requirements.txt lists `google-genai`, `sqlalchemy`, `bcrypt`, `requests`, none of which is imported anywhere in src/ or tests/ (grep). `slowapi` appears only in src/api/config.py and payments.py. The files are unpinned (no versions), and pyproject.toml and requirements.txt disagree (pyproject lacks `requests`; requirements lacks pytest). - [requirements.txt](requirements.txt); [pyproject.toml L6-21](pyproject.toml)
- Model `anthropic/claude-3-haiku` is still in MODELS_TO_EVALUATE. OpenRouter now returns 404 "Claude 3 Haiku was deprecated on Sep 10, 2026" (seen in a test run). - [src/llm/models.py L135-140](src/llm/models.py)

Voice, tone and duplication:
- Mixed voice: "our app" (L16), "I created an automated model sequence" (L156), third person elsewhere. architecture.html uses "We check". - [README.md L16, L156](README.md)
- The benchmark command `python -m src.evaluation.runner` appears twice (L112 and L129). - [README.md L106-130](README.md)
- The notebook link text says "Model_Comparison.ipynb" but the file is `Model_Comparison_Analysis.ipynb`. The link works; the text is wrong. - [README.md L156](README.md)
- Random emphasis: "EXPORT Word file or COPY & PASTE" in caps. - [README.md L18](README.md)
- The feature list mixes long bold-titled paragraphs (L25-37) with terse one-liners (L38-43), which looks like two authors or two eras. L38-43 were added on 2026-11-15 (commit 45d4cf6). - [README.md L23-43](README.md); `git log -- README.md`

### Inferences
- A technical reader will hit "Better than most free-tier AI models ... guarantees" in the second paragraph and stop trusting the rest. That one line does the most damage.
- The latency claim is the most dangerous mistake, because a reviewer can check it against the repo's own CSV and chart in under a minute.
- The ROADMAP checklist and quality README already use plain, honest language ("not legal advice", "The README numbers are estimates"). The README should match them.

### Gaps
- Did not check external links (YouTube, live site, portfolio, LinkedIn) because research was limited to local files.

## 2. Structure problems: order, first screen, missing sections, tree, links

### Takeaway
The first screen is two link-headings plus an authors table, with no description, screenshot, tech stack or results. Key sections (tech stack, tests, deployment, design decisions, limitations, license) are missing. The repo tree is long, stale and partly wrong.

### Cited Findings
- First screen: two H1 links ("Click to see"), then the Authors table with long bio paragraphs. The one-line "what it is" appears only at L15. No screenshot/GIF of the product, although `front_end/images/social-preview.png` exists. - [README.md L1-15](README.md); [front_end/images/social-preview.png](front_end/images/social-preview.png)
- Authors were moved above About on purpose (commit cbedbdb "Reorder sections: move Authors before About", 2026-09-11). Recruiters scan "what it is" first, so authors and contributions usually go near the end. - `git log -- README.md`
- Missing: a tech stack summary (FastAPI, Pydantic, OpenRouter, Supabase, Stripe, Cloudflare Turnstile, vanilla JS, docx.js). It is only implied inside the Authors bio. - [README.md L8](README.md)
- Missing: a "Tests" section. 96 tests exist, and the README never mentions pytest. - tests/ (5 files)
- Missing: deployment. The Dockerfile targets Cloud Run ("Cloud Run sets PORT (default 8080); falls back to 7860 elsewhere" - but the code sets ENV PORT=8080, so the 7860 comment is wrong). The ROADMAP checklist talks about Hugging Face Spaces (L50-63), and commit 005786f says "configure Dockerfile and CORS for Hugging Face Spaces". The README does not say where the live site runs or how. - [Dockerfile L20-24](Dockerfile); [docs/ROADMAP_SETUP_CHECKLIST.md L50-63](docs/ROADMAP_SETUP_CHECKLIST.md)
- Missing: the database setup step. The app needs `docs/migrations/001_credit_ledger.sql` ("Do not deploy without it"), but the README links the checklist only as "Setup steps for the new features". - [docs/ROADMAP_SETUP_CHECKLIST.md L6-17](docs/ROADMAP_SETUP_CHECKLIST.md); [README.md L45](README.md)
- Missing: a limitations section. eval.html has a good one ("a small test ... an AI judge can be biased. Treat quality gaps under about 0.1 as ties"), but the README has none. - [front_end/eval.html](front_end/eval.html) footer note
- Missing: license. There is no LICENSE file, and the ROADMAP says "Decide to open-source the repo" is still open. A public repo with no license is "all rights reserved" by default. - repo root; [docs/ROADMAP_SETUP_CHECKLIST.md L68](docs/ROADMAP_SETUP_CHECKLIST.md)
- Missing: design decisions. architecture.html has a "Design choices" block (AI never writes pay, rules not AI for checks, data-last prompt to resist injection) that would be strong README content for an engineer reader. - [front_end/architecture.html](front_end/architecture.html)
- Image path uses backslashes: `front_end\images\Workflow.drawio.png`. GitHub usually renders it, but it is non-portable and looks careless. The other images use forward slashes. - [README.md L51](README.md)
- The workflow diagram is from 2026-09-05 (file mtime), before the 2026-11 changes (free generate, linter, Turnstile). It probably does not show the current flow. - `front_end/images/Workflow.drawio.png`; [README.md L51](README.md)
- Repo tree (L169-207, about 40 lines) problems:
  - Says `eval_results/  # Automated benchmark CSVs & analysis notebooks`, but the notebook lives in `src/evaluation/`.
  - Leaves out src/credits/, src/quality/, src/security/, src/storage/, src/api/routers/public.py, src/api/config.py, src/agent/doc_parser.py, src/evaluation/summary.py, tests/, docs/, Dockerfile.
  - Lists `providers.py  # OpenRouter adapter` while the Authors row says multi-provider.
  - At this length it adds little a reader cannot see in GitHub's file view; a 6-10 line "where to look" table would serve better.
  - [README.md L169-207](README.md)
- The repo tracks clutter visible on GitHub: 41 `.playwright-mcp/*.yml/png/log` files, `research_notes/` (100+ screenshots), `reports/`, `output/latest_*.md`, plus `.vscode/settings.json`. `.gitignore` does not exclude `.playwright-mcp`. - `git ls-files`; [.gitignore](.gitignore)
- Charts are stored in `src/output/`, a source folder, rather than `docs/` or `eval_results/`. - [README.md L137, L148](README.md)

### Inferences
- A recruiter's 10-second scan currently gets: name, video link, two bios, then marketing bullets. A one-line pitch, a screenshot, a stack line and one headline number (e.g. "22 models benchmarked; chosen model: 2.9 s mean latency, 8/8 rule-check pass") would do far more.
- The Authors bio for Phong is the de facto stack summary. It should be split into a neutral "Tech stack" section plus a short contributions table.

### Gaps
- Did not render the README on GitHub to confirm how the backslash image path displays.

## 3. Numbers: do the eval charts and README claims match eval_results?

### Takeaway
The charts are generated from real data in eval_results (179 rows, 22 models, 4 scenarios, generate + refine). The cost/token and latency charts are a real strength. However, the README states none of the methodology (n, dates, judge model, pricing source). Two README numbers contradict the data, and the cost numbers mostly rest on a placeholder price.

### Cited Findings
- Data size: 179 rows in model_comparison.csv/json; 22 model_ids; 4 scenarios (scenario_only_required_fields, scenario_all_fields, scenario_various_fields_sparse, scenario_complex_edge_case); 92 generate + 87 refine rows. 20 models have 8 rows (4 scenarios x generate+refine, single run). qwen-2.5-7b has 13 rows (duplicated runs), and qwen3.5-flash has 6. - [eval_results/model_comparison.csv](eval_results/model_comparison.csv) (computed); [src/evaluation/scenarios.py](src/evaluation/scenarios.py)
- No repeated trials: each model x scenario x task is one call, so there is no variance or confidence interval. - [src/evaluation/runner.py L122-125](src/evaluation/runner.py)
- No timestamps in the result rows. The only dating is git history: results and charts were committed between 2026-08-09 and 2026-09-09 (commit 3c6ccfe "Change source of evaluating diagrams"; chart mtimes 2026-09-09). The README gives no run date. - `git log -- eval_results src/output`; CSV header (no date column)
- Judge: `JUDGE_MODEL = "openai/gpt-4o-mini"`, which is also one of the evaluated models and the first fallback. That creates self-preference risk. The README does not mention an LLM judge at all; eval.html says only "A second AI model judges". - [src/evaluation/metrics.py L20](src/evaluation/metrics.py); [front_end/eval.html](front_end/eval.html)
- Judge failure is silently scored 0.0 on all scores. 2 rows have overall_quality_score 0, which drags those models' means down. - [src/evaluation/metrics.py L108-109](src/evaluation/metrics.py); CSV (computed)
- The judge prompt asks for 5 scores but the example JSON includes `overall_quality_score`, so the judge model makes up the "overall" value instead of code computing it. - [src/evaluation/metrics.py L33-51](src/evaluation/metrics.py)
- Cost: `MODEL_PRICING` has 7 entries. Only 5 match evaluated model_ids exactly (gpt-4o-mini, llama-3.3-70b, qwen-2.5-72b, mistral-small, phi-4). `deepseek/deepseek-chat` does not match `deepseek/deepseek-chat-v3.1`, and `anthropic/claude-3.5-haiku` does not match `anthropic/claude-3-haiku`. The other 17 models, including the chosen gemini-2.5-flash-lite, gpt-4o, gemini-2.5-pro and deepseek-r1, use `DEFAULT_PRICING = (0.20, 0.80)`. So for most models the "cost" bar is just a weighted token count. - [src/evaluation/metrics.py L10-19, L68](src/evaluation/metrics.py)
- Inference from known list prices (not verified in this audit): gpt-4o costs well above $0.20/$0.80 per 1M tokens, so its $0.000358 per call (cheaper than several small models in the chart) is very likely understated. The ROADMAP itself says "The README numbers are estimates". - [docs/ROADMAP_SETUP_CHECKLIST.md L72](docs/ROADMAP_SETUP_CHECKLIST.md)
- Token counts are real API usage (`response.usage.prompt_tokens/completion_tokens`), not the 1.33 tokens-per-word heuristic, which is good. - [src/llm/providers.py](src/llm/providers.py) generate_with_openrouter (usage lines)
- Latency is real wall-clock per call (`time.perf_counter`) from one client location. Network and OpenRouter routing are included, and it is not stated. - [src/llm/providers.py](src/llm/providers.py)
- Fallback contamination risk: when the benchmark runs gemini-2.5-flash-lite, `MODEL_FALLBACKS` applies (via JobAgent `_call_llm`). A failed primary call could be silently answered by gpt-4o-mini, yet the row is labeled with the configured model_id (`model_config["model_id"]`), not `llm_result.model`. - [src/agent/job_agent.py L88-93](src/agent/job_agent.py); [src/evaluation/runner.py L171-173](src/evaluation/runner.py); [src/llm/models.py L4-10](src/llm/models.py)
- `schema_pass` is always True for any parsed draft ("always True for a parsed draft"), so it duplicates `valid_json` for successful rows. - [src/evaluation/metrics.py L118-132](src/evaluation/metrics.py)
- The checks contradict each other: `required_fields_present` requires a non-empty `equal_opportunity`, while scenario_only_required_fields has `must_not_include: "equal opportunity employer"`, and sparse inputs give no company / EEO info. Result: required_fields_present is False for 45/46 sparse rows and 35/44 edge-case rows. The metric is mostly measuring the scenario design. - [src/evaluation/metrics.py L122-136](src/evaluation/metrics.py); [src/evaluation/scenarios.py L22-24](src/evaluation/scenarios.py); CSV (computed)
- Per-model means (computed from CSV), to check README claims:
  - gemini-2.5-flash-lite: latency 2.87 s, rule pass (schema & include & exclude) 8/8, required_fields 3/8, overall 4.75, cost $0.000611 (default price)
  - gpt-4o: 3.03 s, 8/8, overall 4.77
  - gpt-4o-mini: 5.32 s, 6/8, overall 4.78
  - mistral-small: 7.91 s, 7/8, overall 4.77
  - llama-3.1-70b (third fallback): 11.95 s, 6/8
  - deepseek-r1: 109.46 s, overall 4.88 (highest judge score, slowest)
  - [eval_results/model_comparison.csv](eval_results/model_comparison.csv)
- Fallback order is not what the data ranks next. On the notebook's pass definition and on latency, gpt-4o (8/8, 3.03 s) beats gpt-4o-mini (6/8, 5.32 s), and the README does not explain why llama-3.1-70b (6/8, 11.95 s) is in the chain. Cost may be the reason, but it is not stated. - [README.md L160-163](README.md); [src/llm/models.py L4-10](src/llm/models.py)
- The notebook's markdown analysis is stale against its own outputs:
  - It says "Required Fields only: 21 fails"; the output gives 45.45% of 44 rows passed, i.e. 24 fails.
  - The cost ranking text lists about 10 models, while the data has 22.
  - It concludes "Cheap models with low temperature seems to meet the requirements better", but no temperature is set anywhere in providers.py.
  - [Model_Comparison_Analysis.ipynb cells 3, 6, 9](src/evaluation/Model_Comparison_Analysis.ipynb); grep "temperature" src/llm/providers.py (none)
- Chart craft issues:
  - The latency chart's right axis is truncated to 4.0-5.0 (`set_ylim(4,5)`), which makes 0.1-point judge differences look like big swings.
  - The cost chart's right axis has no label (tokens).
  - Titles are generic ("Chart showing the estimated cost in correlation with input & output tokens", "Bar: ... Line: ...").
  - x labels repeat the "openrouter_" prefix 20 times.
  - Neither chart states n or run date.
  - [src/output/eval_latency_comparison.png](src/output/eval_latency_comparison.png); [src/output/eval_cost_and_tokens.png](src/output/eval_cost_and_tokens.png); notebook cell 12
- The README shows 2 of the 4 generated charts. eval_failures_pass_rates.png and eval_quality_scores.png are not shown, so the README makes pass-rate and quality claims ("100%", "high LinkedIn readiness scores") without showing the chart behind them. - [README.md L132-152](README.md); [src/output/](src/output/)
- Strength: the public `/api/eval-summary` endpoint and eval.html compute stats live from the same JSON ("Numbers come straight from the evaluation harness in the repository"). eval.html also states its limits honestly. - [src/evaluation/summary.py](src/evaluation/summary.py); [src/api/routers/public.py L11-15](src/api/routers/public.py); [front_end/eval.html](front_end/eval.html)

### Inferences
- The cost/token chart and latency chart are the README's most credible content, because they come from real usage and timing. They become fully defensible with (a) a methodology line (22 models, 4 scenarios x generate+refine, 1 run each, run Aug-Sep 2026 via OpenRouter, latency from one client) and (b) real per-model prices, or a note saying which models use a placeholder price.
- Replacing "100% pass rate, < 2 s" with exact numbers ("8/8 rule checks, 2.9 s mean latency, n=8") is more convincing to an engineer and is also true.
- Self-judging by gpt-4o-mini should be disclosed. A stronger or different-family judge, or a small human-rated sample, would make quality claims credible.

### Gaps
- Could not confirm current OpenRouter list prices for the 17 default-priced models (local-only scope). The gpt-4o understatement is an inference from general knowledge.
- Could not tell from the data whether any gemini-2.5-flash-lite row was actually served by a fallback model (rows do not record the serving model).

## 4. Verification and deployment: tests, CI, deploy docs

### Takeaway
There is a solid offline test suite (74 tests, all pass in 2.6 s), but the README never mentions it. Plain `python -m pytest -q` also runs 22 live, paid OpenRouter calls, and 4 of them fail. There is no CI, and deployment is undocumented and inconsistent across files.

### Cited Findings
- `python -m pytest -q` (global Python, run 2026-11-17): **4 failed, 92 passed in 33.8 s**. All 4 failures are in tests/test_all_models.py (live network calls per model): deepseek_r1, qwen_2_5_7b, wizardlm_2_8x22b, claude_3_haiku. claude_3_haiku failed with OpenRouter 404 "Claude 3 Haiku was deprecated on Sep 10, 2026". - local run; [tests/test_all_models.py](tests/test_all_models.py)
- `python -m pytest -q --ignore=tests/test_all_models.py`: **74 passed in 2.61 s**. This is the command the ROADMAP checklist recommends ("runs the new tests (no network)"). - local run; [docs/ROADMAP_SETUP_CHECKLIST.md L74-76](docs/ROADMAP_SETUP_CHECKLIST.md)
- Test files and function counts:
  - test_api_billing_and_limits.py: 40
  - test_quality_linter.py: 15
  - test_agent_and_prompts.py: 13
  - test_eval_summary.py: 3
  - test_all_models.py: 1, parametrized over 22 models
  - tests/*.py (grep -c "def test_")
- test_all_models.py is not marked (no `@pytest.mark.network`/skip-if-no-key). It runs by default and costs money, needs `OPENROUTER_API_KEY`, and calls `load_dotenv(override=True)`. - [tests/test_all_models.py L1-8](tests/test_all_models.py); [pyproject.toml L28-30](pyproject.toml)
- No CI: there is no `.github/` directory. `.dockerignore` lists `.github`, but none exists. - repo root; [.dockerignore](.dockerignore)
- Deployment config: a Dockerfile only (python:3.11-slim, non-root user, uvicorn on $PORT=8080). There is no vercel/render/railway/fly config. Hosting is inconsistent across files:
  - Dockerfile comment says Cloud Run
  - ROADMAP and commit 005786f say Hugging Face Spaces
  - security/limits.py says "single Hugging Face Space"
  - config.js says "The free host sleeps when idle"
  - [Dockerfile](Dockerfile); [src/security/limits.py L4](src/security/limits.py); [front_end/config.js L5-8](front_end/config.js)
- In-memory rate-limit counters "reset on restart" and work per container. This is a real limitation worth stating in the README. - [docs/ROADMAP_SETUP_CHECKLIST.md L53](docs/ROADMAP_SETUP_CHECKLIST.md); [src/security/limits.py L4](src/security/limits.py)
- Stale `__pycache__` files for deleted modules (security.cpython-312, credits.cpython-312, test_google_auth...) exist locally. They are untracked, so this is not a docs issue, only local noise. - src/auth/__pycache__, tests/__pycache__
- CORS: two middleware layers, the first `allow_origins=["*"]` with `allow_credentials=True`. Not a README issue, but an engineer reading main.py will notice it. The code comment explains the ordering. - [src/api/main.py L22-38](src/api/main.py)

### Inferences
- Adding a "Tests" section with the offline command and a CI badge (a simple GitHub Actions job running the 74 offline tests) would be the cheapest credibility gain.
- test_all_models.py should be opt-in (marker or env flag), so a reviewer who clones and runs pytest does not see red failures caused by deprecated models.
- The README should name the one real deployment target and link the ROADMAP checklist as "Deployment / production setup".

### Gaps
- Did not check the reasons for the deepseek_r1, qwen_2_5_7b and wizardlm failures (output was truncated to the last failure). They are likely model availability or quota issues, but this is unconfirmed.
- Could not confirm the live host (HF Space vs Cloud Run) from local files alone.

## 5. What looks amateur or AI-generated, and what is genuinely strong

### Takeaway
The amateur signals are concentrated in the README's top half: clickbait headings, superlatives, typos, and a stale tree. The strengths are real engineering work that the README undersells: credit ledger with idempotent webhooks, offline tests, a deterministic linter, a reproducible eval harness with a public eval page, and honest limits on eval.html.

### Cited Findings
Amateur or AI-like signals:
- "(Click to see the Website)" / "(Click to see)" inside H1s. - [README.md L1-2](README.md)
- Superlative marketing: "Better than most", "guarantees", "goes even further", "very detailed output". - [README.md L16-17](README.md)
- Bold-label bullet lists with filler phrasing ("Simple Guiding Questions: Provide simple questions..."), a common AI-template pattern. - [README.md L25-37](README.md)
- Model `purpose` blurbs read as invented marketing ("SOTA open reasoning model", "A better sidekick of gpt-4o-mini"), not reasons for inclusion. - [src/llm/models.py](src/llm/models.py)
- The ROADMAP checklist contains "Things I could not do for you", which reads like an AI assistant's handoff note addressed to the owner, committed as project docs. - [docs/ROADMAP_SETUP_CHECKLIST.md L65-72](docs/ROADMAP_SETUP_CHECKLIST.md)
- Commit messages like "front-end bullshit hardcode" are visible in `git log` on a public repo. - commit ce4e102
- Committed tool artifacts (.playwright-mcp logs and screenshots) and large research_notes screenshot folders. - `git ls-files`
- Authors bio says "refined the UI/UX using AI agents for design research and iteration". This is honest; fine to keep, but it invites scrutiny of the docs. - [README.md L8](README.md)

Genuine strengths (keep and surface):
- The cost/token and latency charts are generated from real API usage and wall-clock timing over 22 models, and the README explains what each chart measures in one line. Clear strength. - [README.md L132-152](README.md); [src/llm/providers.py](src/llm/providers.py)
- The eval harness is reproducible: one command, `--model` re-run flag, skip-existing, and CSV + JSON outputs. - [src/evaluation/runner.py](src/evaluation/runner.py)
- The model fallback chain is documented and matches code exactly (gemini-2.5-flash-lite -> gpt-4o-mini -> mistral-small-24b -> llama-3.1-70b). - [README.md L158-163](README.md); [src/llm/models.py L4-10](src/llm/models.py)
- The extraction model claim (gemini-2.5-flash-lite for upload auto-fill) matches code. - [README.md L27](README.md); [src/api/services.py L27](src/api/services.py)
- Pricing claims ($5=20, $10=40, $20=80; 20 free credits; refund on failed refine) are consistent across README L19, architecture.html, and the ROADMAP checklist L25. - [README.md L19](README.md); [docs/ROADMAP_SETUP_CHECKLIST.md L12-13, L25](docs/ROADMAP_SETUP_CHECKLIST.md)
- Swagger docs at /docs are mentioned, a useful pointer for reviewers. - [README.md L95](README.md)
- eval.html states limits plainly ("a handful of runs per model", "an AI judge can be biased", "Treat quality gaps under about 0.1 as ties"). This is the right tone for the README too. - [front_end/eval.html](front_end/eval.html)
- architecture.html explains design choices (AI never writes pay; deterministic rule checks; retry once then a clear error; data placed after instructions). Senior-level content that is missing from the README. - [front_end/architecture.html](front_end/architecture.html)
- src/quality/README.md is a model of a good small README: one-paragraph purpose, a runnable snippet, a checks list with a citation (Gaucher, Friesen and Kay, 2011), a disclaimer, and a test command. - [src/quality/README.md](src/quality/README.md)
- The ROADMAP checklist is concrete and operational: migration step, fail-closed behavior, env var table with defaults, and a proxy IP check. It could become a proper "Deployment" doc after removing the assistant-handoff section. - [docs/ROADMAP_SETUP_CHECKLIST.md](docs/ROADMAP_SETUP_CHECKLIST.md)

### Inferences
- Summary of recommended actions per item:
  - **Remove:** L16-17 superlatives; "(Click to see)" headings; duplicate benchmark block; "OpenAI, Hugging Face" in the bio; the long repo tree (replace it with a short map).
  - **Rewrite with numbers:** latency and pass-rate claims (L151, L159); "Guarantee LinkedIn Format" (L29); the pipeline steps to match architecture.html.
  - **Back with evidence:** cost chart (real prices or a disclosed placeholder); judge model and n; run date.
  - **Move:** the full env var table and production setup to a deployment doc, linked from the README; the Authors section lower.
  - **Add:** screenshot, tech stack, tests + CI badge, deployment target, design decisions, limitations, license, `.env.example`.

### Gaps
- No external reference set on README best practices was gathered here (local-only scope). Other researchers cover that.
