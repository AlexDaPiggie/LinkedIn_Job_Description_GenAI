# Reporting Numbers and Evals in Technical Docs (LLM + software products)

Scope: how credible products present benchmarks, evals, cost, latency, quality metrics; anti-patterns; what the LinkedIn JD generator (OpenRouter: gemini-2.5-flash-lite primary, gpt-4o-mini, mistral-small, llama fallbacks; cost, latency, schema pass rate, gpt-4o-mini judge; PNG charts in README) should report. Research date 2026-11-17.

## 1. How LLM tooling products and model makers report evals and benchmarks

### Takeaway
Credible model makers attach settings to every number (model snapshot, prompt, sampling, thinking budget, trials, harness), footnote every exception (competitor re-runs, best-of-N, harness changes), and the most rigorous add SEM/95% CI and caveats (saturation). Leaderboards add vote/sample counts, CIs and repro commands.

### Cited Findings
- OpenAI simple-evals: one markdown table, rows = models, columns = benchmarks (MMLU, GPQA, MATH, HumanEval, MGSM, DROP, SimpleQA), plus a "Prompt" column for the system prompt used ("assistant" = "You are a helpful assistant.", "n/a" for o-series, "unknown" for third-party) - [openai/simple-evals](https://github.com/openai/simple-evals)
- simple-evals uses dated snapshots (gpt-4o-2024-11-20, gpt-4.1-2025-04-14); some rows (o3, o1) undated - [simple-evals](https://github.com/openai/simple-evals)
- simple-evals footnotes deviations: o3/o4-mini no tools; MATH-500 for o1+; GPQA regex tweak; DROP/MGSM flagged likely saturated; "Other Models (Reported)" rows taken from external publications, not re-run - [simple-evals](https://github.com/openai/simple-evals)
- simple-evals states evals are prompt-sensitive, cross-source scores may not be comparable; defines "n/a" vs "-" - [simple-evals](https://github.com/openai/simple-evals)
- Weakness: single scores, no variance/CI/run count/temperature. July 2025 banner: no longer updated for new models (good freshness practice) - [simple-evals](https://github.com/openai/simple-evals)
- Anthropic Opus 4.5 methodology footnote: 64K thinking budget, interleaved scratchpads, 200K context, default effort high, default sampling, "averaged over 5 independent trials"; exceptions (SWE-bench Verified no thinking budget, Terminal Bench 128K); full details deferred to system card - [Anthropic Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- Same post discloses flattering factors: take-home result used parallel test-time compute (best of N); competitor Terminal Bench re-runs in changed environment raised Gemini 3 to 56.7% and GPT-5.1 to 48.6%, above developers' own figures (Terminus-2 harness); safety results from earlier snapshot; BrowseComp-Plus 70.48% to 85.30% only with context management + memory + tools - [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- Same post admits a tau2-bench task scored as failure though model found a valid solution. Weakness: headline numbers mostly in images; text gives relative claims ("10.6% jump over Sonnet 4.5") - [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- Anthropic stats guidance: report SEM with every score; 95% CI = mean +/- 1.96 x SEM; cluster SEs when questions share a source (clustered SEs >3x naive on popular evals); resample several answers per question and average; paired differences when comparing models (question-score correlations 0.3-0.7 = "free" variance reduction); power analysis to size the eval - [Anthropic, statistical approach to model evals](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- Chatbot Arena: moved from online Elo to Bradley-Terry MLE with bootstrapped CIs (earlier 1,000 permutations); ties = half win; shows vote count per model (Dec 2023: GPT-4-Turbo 1217 / 7,007 votes; PPLX-7B-Online 1016 / 1,041 votes); explicitly says fewer votes = wider CIs - [LMSYS Dec 2023](https://lmsys.org/blog/2023-12-07-leaderboard/)
- Arena rates snapshots separately (gpt-4-0314 1201 vs gpt-4-0613 1152), verified with 1,000 new votes - [LMSYS](https://lmsys.org/blog/2023-12-07-leaderboard/)
- HF Open LLM Leaderboard: lists per-task shots (IFEval 0, BBH 3, MATH Lvl5 4, GPQA 0, MMLU-PRO 5), metric names (acc_norm, exact_match, prompt_level_strict_acc), num_choices; publishes raw results + per-sample inputs/outputs as HF datasets; exact lm-eval repro command with revision/dtype; warns batch size changes results slightly (padding); marks community-flagged models - [HF leaderboard About](https://huggingface.co/docs/leaderboards/open_llm_leaderboard/about)
- promptfoo llm-rubric: judge returns JSON {reason, score 0-1, pass}; default grader depends on available keys (e.g. gpt-5 with OpenAI key); grader pinnable via --grader/provider + config (temperature); gotcha: {pass:true, score:0} passes unless threshold set - [promptfoo llm-rubric](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/)

### Inferences
- Baseline = every number footnoted with snapshot ID, prompt, sampling, trials, harness. Disclosing unfavorable facts (re-runs, best-of-N, benchmark bugs) builds trust.
- Image-only charts are less inspectable; pair PNG with a markdown table.
- JD project: pin exact OpenRouter slugs; record upstream provider (OpenRouter may route differently); state temperature, max_tokens, runs per model.

### Gaps
- Langfuse, Braintrust, Ragas, DeepEval, Ollama docs not fetched (budget); mostly metric definitions, not reporting norms.
- Artificial Analysis run counts/percentiles/Intelligence Index CIs not visible in fetched page.

## 2. Cost and latency reporting and test setup

### Takeaway
Define each metric exactly (TTFT vs E2E vs tokens/s), report percentiles not means, state window and load profile, price per token with stated blend ratio. Infra benchmarks list instances, vCPU/RAM, users, request rate, tool, mock vs real backend.

### Cited Findings
- Artificial Analysis definitions: TTFT (first reasoning token for reasoning models); Time to First Answer Token (includes reasoning, fair comparison); End-to-End Time; Output Speed (output tokens incl. reasoning / s over full request incl. TTFT) - [AA methodology](https://artificialanalysis.ai/methodology)
- AA rolling 5-day window for timing and endpoint error rate; errors include rate limits, timeouts, deadline overruns; exclude invalid keys, quota, safety blocks, max_tokens cutoffs - [AA](https://artificialanalysis.ai/methodology)
- AA pricing per native token at current list price; blended price uses stated 7:2:1 cache-hit:input:output (many secondary sources cite older 3:1 input:output - always state yours); Cost per Task weights by actual tokens used - [AA](https://artificialanalysis.ai/methodology)
- LiteLLM: methodology table per test set; high-throughput test reports p50/p95/p99 gateway latency, client TTFT p50, HTTP 200 rate; setup 33 pods x 4 workers, 4 vCPU, 16 GiB, Locust 30 load workers, 3,000 users at 1 req/s, mock model behind AWS ALB, caching off - [LiteLLM benchmarks](https://docs.litellm.ai/docs/benchmarks)
- LiteLLM caveats: mock endpoints exclude provider latency; client TTFT includes upload/ALB; Redis off in some tests; logging-callback set omits deployment details (visible gap) - [LiteLLM](https://docs.litellm.ai/docs/benchmarks)
- vllm bench serve: metrics ttft, tpot, itl, e2el; --metric-percentiles default 99, configurable (25,50,75); --num-prompts default 1000; --request-rate default inf (all at t=0) else Poisson/gamma; --seed 0; dataset sharegpt/random/hf/custom; "goodput" = share of requests under ms thresholds - [vLLM docs](https://docs.vllm.ai/en/latest/cli/bench/serve.html)
- ClickBench stores results as results/YYYYMMDD/<machine>.json, so every number is dated and machine-tied - [ClickBench](https://github.com/ClickHouse/ClickBench)

### Inferences
- JD project per model: n requests, p50/p95 E2E latency (s), TTFT if streaming, mean input/output tokens, $/request and $/1k JDs from actual usage tokens x OpenRouter price with price date and cost source stated.
- Setup block: date range, slugs, network location, sequential vs concurrent, temperature, max_tokens, n inputs, runs per input, whether retries/fallbacks count in latency.
- Report error/fallback rate separately with failure definition.
- With small n, p95 is near max - say so, or show p50 + max.

### Gaps
- AA runs/day, prompt lengths, percentile use not confirmed.
- No sourced "$ per 1k requests" example; per-token and per-task pricing is the sourced norm.

## 3. LLM-as-judge credibility

### Takeaway
Name judge model+version, publish rubric, prefer binary pass/fail with written critique, validate against human labels with TPR/TNR or kappa (not raw agreement), address position, verbosity, self-preference, inflation biases.

### Cited Findings
- Husain: pass/fail over 1-5 scales (scales are a smell); each verdict has a critique detailed enough to reuse as few-shot - [Hamel Husain](https://hamel.dev/blog/posts/llm-judge/)
- Husain: treat judge as classifier vs expert labels; report TPR and TNR separately (raw agreement misleads when failures rare); example reached >90% after 3 iterations - [Husain](https://hamel.dev/blog/posts/llm-judge/)
- Husain sample sizes: ~30 examples to find failure modes; ~100 per failure mode to validate (<60 gives too-wide CIs); 30-50 Pass and 30-50 Fail per split; split ~10-20% train / 40-45% dev / 40-45% test; freeze prompt, score test once, re-validate on model/product change - [Husain](https://hamel.dev/blog/posts/llm-judge/)
- Eugene Yan judge biases: position (gpt-3.5 ~50%, claude-v1 ~70%); verbosity (longer preferred >90% even with no added info); self-enhancement (gpt-4 +10%, claude-v1 +25%); inflation (gpt-4 4.7/7 vs human 2.9) - [Eugene Yan](https://eugeneyan.com/writing/llm-evaluators/)
- Yan agreement metrics: Cohen's kappa gpt-4 0.84, llama-3-70b 0.79, human-human 0.97; llama-3-8b 80% raw agreement but kappa 0.62; UMbrela kappa 0.3-0.5 vs tau/rho 0.8-0.9 on same data - [Yan](https://eugeneyan.com/writing/llm-evaluators/)
- Yan method: direct scoring for objective criteria (faithfulness, policy), pairwise for subjective (tone); binary where possible for precision/recall; Spearman/Kendall for Likert, kappa for pairwise; a few hundred samples in development - [Yan](https://eugeneyan.com/writing/llm-evaluators/)
- promptfoo shows credible config: rubric text, pinned grader + temperature, threshold, stored reason - [promptfoo](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/llm-rubric/)

### Inferences
- JD risk: gpt-4o-mini judging gpt-4o-mini = self-enhancement setup. Mitigations to state: disclose; add a second judge from another family on a subset and report agreement; hand-label 30-50 outputs, report TPR/TNR or kappa; hide model names from judge; randomize order if pairwise.
- Verbosity bias: report mean output length next to judge score.
- Use per-criterion binary checks (sections present, no invented salary, matches seniority) and report % pass with n. Link rubric file; give judge slug + temperature.

### Gaps
- Shreya Shankar (criteria drift) not fetched. No data on gpt-4o-mini's human agreement as judge.

## 4. Performance numbers in software READMEs

### Takeaway
Pattern: one headline bar chart + caption naming the workload; trust comes from a linked methodology doc (hardware, versions, cold/warm, repro command, caveats). uv and ClickBench do it well; Ruff's README has no methodology link; Bun's README now uses only qualitative claims.

### Cited Findings
- Ruff README: SVG bar chart, caption "Linting the CPython codebase from scratch", claim "10-100x faster than existing linters"; no methodology link, hardware or versions; anecdotal testimonials ("nearly 1000x faster") - [ruff](https://github.com/astral-sh/ruff)
- uv BENCHMARKS.md: hyperfine script in scripts/benchmark; one real project (Trio docs-requirements.in); 4 scenarios warm/cold install, warm/cold resolve; exact repro + chart render commands; competitors on Python 3.12.4 - [uv BENCHMARKS](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md)
- uv caveats: results vary by OS/filesystem (reflink vs hardlink) and package set (heavy source build equalizes tools); cold runs flaky from ISP throttling. Weakness: only "macOS", no CPU/RAM or tool versions - [uv](https://github.com/astral-sh/uv/blob/main/BENCHMARKS.md)
- Bun README: no charts/numbers, only "significantly faster"; speed badge links to an X post; bench dir not linked - [bun](https://github.com/oven-sh/bun)
- ClickBench setup: 99,997,497 rows, 43 queries; default AWS c6a.4xlarge + 500 GB gp2; benchmark.sh per system; 3 runs per query (run 1 cold with caches cleared + restart, 2-3 hot); result caches banned; tuned configs listed separately as "-tuned"; failures recorded as null - [ClickBench](https://github.com/ClickHouse/ClickBench)
- ClickBench scoring: per-query (10 ms + t) / (10 ms + best); missing = 2x max runtime (min 300 s); geometric mean summary; combined load 10% / size 10% / cold 20% / hot 60% - [ClickBench](https://github.com/ClickHouse/ClickBench)
- ClickBench limitations section: flat table favors denormalized systems; small dataset; mostly single node; sequential queries; few runs so results vary; tl;dr "All Benchmarks Are Bastards" - [ClickBench](https://github.com/ClickHouse/ClickBench)

### Inferences
- JD README: one headline chart + caption (n, runs, date, judge) + markdown table of exact values + link to BENCHMARKS.md (setup, repro, raw data, caveats).
- Commit raw per-call JSONL/CSV in dated files; render PNGs from them via script. Show failures, don't drop them.

### Gaps
- Biome, Turborepo, bun.sh benchmark pages not fetched.

## 5. Hallucination / faithfulness / structured-output reliability

### Takeaway
Separate coverage from compliance, count timeouts/failures as non-compliant (JSONSchemaBench). Vendor "100%" claims use their own eval sets. Measure on your schemas, report retry-adjusted cost, validate even native structured output.

### Cited Findings
- JSONSchemaBench (arXiv 2501.10868): ~10K real schemas, 6 frameworks (Guidance, Outlines, llama.cpp, XGrammar, OpenAI, Gemini); separates declared coverage, empirical coverage, compliance; Outlines' lower compliance mainly from timeouts; unconstrained LM-only lowest; closed providers score high partly by supporting only a subset of JSON Schema - [JSONSchemaBench](https://arxiv.org/html/2501.10868v3)
- Retry loops hide cost; per-call success understates cost - [tianpan.co](https://tianpan.co/blog/2026-04-28-structured-output-retry-loop-hidden-compute-waste) (blog)
- Small practitioner benchmark reports 95% CIs: 65% adherence (CI 43.2%-82.3%) on 20 runs - shows how wide CIs are at small n - [dev.to](https://dev.to/david_moores_cbc0233b7447/benchmarking-llm-structured-outputs-1ijc) (individual blog)
- "15-20% naive JSON failure" and "<1% with constrained decoding" are blog anecdotes, not controlled studies - [tianpan.co](https://tianpan.co/blog/2026-04-10-structured-output-reliability-llm-production)
- AA defines exactly which failures count - [AA](https://artificialanalysis.ai/methodology)

### Inferences
- JD funnel per model, each with k/n: (1) parse OK; (2) schema pass first attempt; (3) pass within K retries (state K); (4) fallback rate (and to which model); (5) hard fail.
- State mode: OpenRouter response_format json_schema strict vs prompt-only; some routed providers may not enforce schemas.
- Report retry-inclusive cost and latency.
- "100%" on n=20 has 95% lower bound ~83% (rule of three; standard binomial stats, not from sources above). Write "20/20".
- Faithfulness for JDs = binary "facts not in input (salary, benefits, company claims)?" plus hand-checked sample.

### Gaps
- Ragas/DeepEval faithfulness formulas not fetched. OpenRouter per-provider structured-output support docs not fetched.

## 6. Anti-patterns that make numbers look untrustworthy

### Takeaway
Trust drops with no setup/date/n/units/uncertainty, mixed sources unlabeled, hidden best-of-N or tuning, dropped failures, charts with no table or raw data.

### Cited Findings
- Single scores with no variance (simple-evals) vs 5-trial averages (Anthropic) and SEM/CI (Anthropic stats) - [simple-evals](https://github.com/openai/simple-evals); [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5); [stats](https://www.anthropic.com/research/statistical-approach-to-model-evals)
- Unlabeled external numbers; fix = "Reported" label, disclosed competitor re-runs - same sources
- Hidden best-of-N/scaffolding; Anthropic footnotes it - [Opus 4.5](https://www.anthropic.com/news/claude-opus-4-5)
- Unpinned model names; snapshots differed ~50 rating points - [LMSYS](https://lmsys.org/blog/2023-12-07-leaderboard/)
- Stale results; fix = deprecation banner, dated result files - [simple-evals](https://github.com/openai/simple-evals); [ClickBench](https://github.com/ClickHouse/ClickBench)
- Chart with no methodology link (Ruff); speed badge pointing to a tweet (Bun) - [ruff](https://github.com/astral-sh/ruff); [bun](https://github.com/oven-sh/bun)
- Tuned results passed as defaults; dropped failures; ClickBench's -tuned and nulls fix both - [ClickBench](https://github.com/ClickHouse/ClickBench)
- Raw judge agreement (80% but kappa 0.62); unvalidated 1-5 scales; judge validation sets <60 - [Yan](https://eugeneyan.com/writing/llm-evaluators/); [Husain](https://hamel.dev/blog/posts/llm-judge/)
- Mock-backend latency not labeled; LiteLLM states it - [LiteLLM](https://docs.litellm.ai/docs/benchmarks)
- Unstated price blend; AA states 7:2:1 - [AA](https://artificialanalysis.ai/methodology)
- Ignoring saturation/benchmark bugs; simple-evals, Anthropic, ClickBench flag theirs - sources above

### Inferences - JD README checklist
- Headline chart: judge pass % vs $/1k JDs, one point per model, primary highlighted; caption with n, date, judge.
- Table: slug (+provider) | n | first-try schema pass (k/n) | pass after retries | fallback % | p50/p95 latency (s) | mean tokens in/out | $/1k JDs | judge pass % (CI or k/n) | mean words.
- Setup block: run dates, price snapshot date, temperature, max_tokens, response_format mode, dataset (n, how chosen, link), runs/input, concurrency, network, retry K, fallback chain order.
- Judge block: judge slug + temperature, rubric link, binary criteria, self-preference caveat, human spot-check (agreement X/40, TPR/TNR), length-bias note.
- Limitations: small n, single-network latency, OpenRouter routing variance, prices change, synthetic inputs, judge is not a recruiter.
- Reproduce: one command; raw dated JSONL/CSV committed; chart render script.
- Wording: no bare "100%"/"best" without k/n; units on every axis/column; charts generated from data only.

### Gaps
- No single authoritative anti-pattern list; synthesized from contrasts across cited sources.
