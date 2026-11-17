# Fix pricing, lint output, harden credits first

**Bottom line:** the product already beats most rivals on friction (no login, upload-existing-JD, LinkedIn format, Word export). No competitor in the research does all four. Biggest gaps are not features but money, trust, and safety. Top moves, in order:
- Stop selling the $1 pack. Stripe takes **32.9%** of it. Move to a $5 minimum pack ([Stripe pricing](https://stripe.com/pricing)).
- Add a free rule-based "quality report" next to each JD (bias words, pay range, length). Textio charges demo-level prices for this; Greenhouse has none ([Textio](https://textio.com/products/flow), [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/36960585376283-Job-post-description-suggestions)).
- Lock down credits (atomic ledger, webhook dedup) and the anonymous endpoint (Turnstile, trusted-IP limits, daily spend cap).
- Make Refine cheaper to use: quick-action chips, section regenerate, undo.
- Publish proof (public eval page, architecture page) for the employer-portfolio goal.

Caveat: little hard data exists on conversion or recruiter behavior. Ranking below mixes sourced facts with my judgment. Inferences are labeled.

## Where we stand vs competitors

Two camps exist:
- **Free top-of-funnel tools:** Workable, Grammarly, Ongig GPT, Testlify. Title in, draft out, copy-paste ([Metaview roundup](https://www.metaview.ai/resources/blog/free-ai-job-description-generators)).
- **Embedded in paid ATS or job platforms:** LinkedIn Hiring Pro, Indeed, Greenhouse, Ashby. Gated by plan, promoted job, or admin setup ([LinkedIn Help](https://www.linkedin.com/help/learning/answer/a6895976), [Greenhouse](https://support.greenhouse.io/hc/en-us/articles/36960585376283-Job-post-description-suggestions)).

Notes:
- LinkedIn's own tool is desktop-only, gradual rollout, limited to members who promote jobs. No standalone use, no export.
- Ongig's free tool is a ChatGPT custom GPT, copy-paste only. Bias and readability scoring sit in its paid platform ([Ongig](https://www.ongig.com/free-ai-job-description-generator)).
- Textio has no public price. Third-party estimates conflict (about $6k per 6 months to $12-15k per year). Unverified.
- Indeed gives two modes: one-shot draft, or step-by-step with tips. Draft in under 5s in beta ([Indeed](https://uk.indeed.com/lead/attract-great-candidates-with-indeeds-new-ai-powered-job-description-tool)).
- Friction ladder, lowest to highest: no account, free account, work email, paid plan, promoted job, demo. We sit at the bottom. Keep it there.
- Betterteam wins SEO with **2,000+** template pages and Word downloads ([TechRadar](https://www.techradar.com/features/30-resources-to-find-job-description-examples)). Our role pages follow this pattern.

Our edge, stated plainly (inference): no-login + upload-and-improve + LinkedIn format + Word export. Put "No signup. Word export." in the H1 or subhead. Get listed in the "best free generator" roundups (Metaview, Fitgap, others).

## Generator UX and output format

What recruiters complain about ([Fortune](https://fortune.com/2025/09/30/recruiters-caution-against-using-ai-write-job-postings-been-trained-on-crappy-descriptions/), [IT Brew](https://www.itbrew.com/stories/2025/09/29/recruiting-against-using-ai-job-descriptions)):
- Generic, not company or team specific.
- Too many bullets.
- No "why join us".
- Little pay or benefits info.
- Hiring managers skip thinking about the role.

What to do:
- **Keep the guided wizard.** It forces role-specific input, which counters "generic" (inference). Add a **fast path**: title-only quick draft, or upload a JD. Mirrors Indeed's dual mode. No conversion data exists on wizard vs chat vs single prompt, so test it yourself.
- **Make company-specific inputs mandatory-ish:** "why join", team context, pay, benefits.
- **Cap bullets** (5-8 requirements), split must-have vs nice-to-have (inference).
- **Show "assumptions - please verify" flags** on requirements not traced to the user's answers. Counters hallucinated requirements. No primary source on that complaint, so this is a judgment call.
- **Upload flow: show "what changed and why"** (diff). Matches Ashby's use of existing postings and recruiter habit of merging own JD with AI version ([Ashby](https://www.ashbyhq.com/product-updates/the-new-ai-content-assistant-uses-rich-context-to-help-you-generate-content-direct-in-ashby)).
- **Free extras (zero LLM cost):** pay-range warning, readability score, LinkedIn length/format check, tone variants. Add screening questions as an extra; LinkedIn and Hireguide pair JDs with these ([LinkedIn Business](https://business.linkedin.com/in/en/hire/post-jobs/ai-assistant)).
- **Pay range matters legally:** CA, CO, WA, NYC, VA (from July 2026) require it. EU directive deadline was 7 June 2026, though most states missed it ([Cooley](https://www.cooley.com/news/insight/2026/2026-07-06-show-me-the-money-or-the-wage-range-new-state-pay-transparency-laws), [remoteworkeurope](https://remoteworkeurope.eu/news/2026/eu-pay-transparency-most-states-miss-deadline/)). About 24% of ads in covered states were non-compliant as of Jan 2025 ([Deel](https://www.deel.com/deel-works/pay-transparency-compliance-gap-2026)). Add a jurisdiction toggle that makes pay fields required. Penalty amounts conflict across sources; do not quote them.
- **Landing page:** sample output above the fold. Skip self-reported lift stats like Indeed's; use honest ones (time saved, count generated). Indeed cites 2+ hours to write a JD (HRSG via Indeed), a usable hook.

## Refine feature and credit model

**Pricing math (Stripe 2.9% + 30c):**

| Pack | Fee | Fee % | Net |
|---|---|---|---|
| $1 | $0.329 | 32.9% | $0.671 |
| $3 | $0.387 | 12.9% | $2.613 |
| $5 | $0.445 | 8.9% | $4.555 |
| $10 | $0.590 | 5.9% | $9.410 |
| $20 | $0.880 | 4.4% | $19.12 |

- International cards add 1.5% (+1% for FX). Fee is not returned on refund. A dispute costs **$15** ([Stripe pricing](https://stripe.com/pricing)).
- LLM cost per refine is tiny (my estimate, assumes ~1,500 in / 800 out tokens): about $0.0006-$0.017 by model. Fees, not the LLM, are the problem. Log real cost per refine; the project model is unknown to the research.
- One dispute wipes out 30-90 $1 packs of profit (my math).
- **Suggested packs (one-time Checkout, no subscription):** $5 = 100 credits, $10 = 250, $20 = 600. Put discounts in credit count, not price. Keep 1 credit = 1 refine. Chargebee advises simple whole-number credit ratios and hard paywall at zero ([Chargebee](https://www.chargebee.com/blog/how-to-make-credit-based-pricing-work-design-sell-and-scale-a-credit-model/)).
- No subscription at this scale: recruiters hire in bursts (judgment, unsourced).
- **Free grant:** 30 is generous. Teal gives about 10 AI bullet credits plus a few more actions; Writesonic 25/month ([Dupple](https://dupple.com/learn/best-ai-resume-builders), [DEV Writesonic](https://dev.to/techsifted/writesonic-pricing-2026-lite-vs-standard-vs-professional-plans-2pd3)). Those figures are secondary and conflict. Fine at cheap-model cost. If model is expensive or abuse rises, cut to 10-15, or give 10 at signup + 10 after first successful refine (judgment).
- Freemium conversion benchmarks: 3-5% good, 8-12% great, SaaS-wide, not recruiter-specific ([ChartMogul](https://chartmogul.com/reports/saas-conversion-report/), [Appcues](https://www.appcues.com/blog/free-to-paid-conversion)).
- Comparable AI tools charge $29-$79/month subscriptions. A $5 prepaid pack is unusual and cheap; a real differentiator for occasional recruiters.

**Paywall flow (synthesis):**
- Logged-out user clicks Refine: save draft and feedback to localStorage, show sign-in, auto-run the pending refine after auth.
- Button label shows cost and balance: "Refine - 1 credit (28 left)". Low-balance nudge at 3.
- At zero: draft stays intact, copy/download stays free, one-click $5 Checkout, auto-resume after return.
- Preview cost before action, alert before balance runs out ([Metronome](https://metronome.com/blog/the-rise-of-ai-credits-why-cost-plus-credit-models-work-until-they-dont)).
- Stripe fulfillment: use webhooks, idempotent per Checkout Session ID, also fulfill on the return page for instant balance ([Stripe docs](https://docs.stripe.com/checkout/fulfillment)).

**Refine UX beyond free text:**
- **Quick-action chips** (1 credit each): Shorter, More inclusive, Add salary range, More casual/formal, Add benefits, Simplify jargon, Mark nice-to-have, Remote-friendly. Removes typing burden, makes cost predictable. Backed by prompt-augmentation patterns ([UX Tigers](https://www.uxtigers.com/post/prompt-augmentation), [arXiv 2412.02357](https://arxiv.org/html/2412.02357v1)).
- **Section-level regenerate** (Responsibilities, Requirements, Benefits) and **lock section**. Fewer tokens, no regressions.
- **Version history** (last ~5 in localStorage), free undo, highlighted diff, short "what changed" note. ChatGPT canvas has version restore plus length and reading-level sliders ([OpenAI Help](https://help.openai.com/en/articles/9930697-what-is-the-canvas-feature-in-chatgpt)).
- No usage data on which refine features recruiters use. Log chip clicks and find out.

**Abuse and refunds:**
- Cheapest stack: Turnstile on signup, confirmed email (OTP exists), disposable-domain blocklist, grant credits only after confirmation and server-side, one grant per normalized email (strip Gmail dots and plus tags), per-user rate limit on /refine, token caps, global daily spend kill switch ([Stripe guide](https://stripe.com/resources/more/how-to-prevent-free-trial-abuse-in-saas-and-ai-products)).
- Do not rely on IP-only limits. Shared office networks cause false blocks.
- Supabase built-in email is reportedly ~2/hour project-wide (secondary source). Use custom SMTP or signup floods block real users ([vibe-eval](https://vibe-eval.com/fix/supabase-rate-limit-api/)).
- Deduct credit only on success, or reserve then commit. Auto-refund on LLM error, timeout, empty or malformed output. State terms: spent credits non-refundable, expiry policy. Legal rules on credit expiry vary; not researched.

## AI and system design

**Ship these (all near-zero cost):**
- **Structured output with checks.** Schema-constrained output still needs checks for refusal, truncation at max tokens, and business rules the schema cannot express ([OpenAI guide](https://developers.openai.com/api/docs/guides/structured-outputs.md)). Vendor reports say strict mode can still fail; keep validate-and-retry. Provider here is unconfirmed; "keep current LLM" applies, so check what your provider offers.
- **Rule-based linter shown in UI (zero LLM cost):**
  - Gender-coded words from Gaucher et al. 2011 ([Duke Fuqua](https://www.fuqua.duke.edu/duke-fuqua-insights/employment-ad-gender-roles)). Full word lists were not retrieved; get them from the paper or the Oregon PDF.
  - Age-coded phrases: "digital native", "recent graduate" ([UCI](https://www.socsci.uci.edu/newsevents/news/2022/2022-08-04-ageist-language-in-job-ads-discourages-older-applicants-uci-led-study-finds.php), [AARP](https://www.aarp.org/work/age-discrimination/age-bias-language-job-listings)). The UCI-led study found subtle ageist phrases cut over-40 applicants by 12 percentage points.
  - Pay block present and min <= max; narrow-range ratio (my suggestion, tune it).
  - Required sections, bullet caps, filler words ("rockstar", "ninja"), reading level, length, EEO statement, duplicate requirements.
  - Heuristic checks: entry-level title with 3+ years asked; degree required with no "or equivalent". No source for degree inflation; treat as a heuristic.
  - Pitch: Textio's own test of 167 ChatGPT posts found bias, and more specific prompts gave more biased posts ([Textio](https://primary.textio.com/blog/chatgpt-writes-job-posts)). Vendor source, not independent. Still a good line: "we lint output".
- **Atomic credit ledger:** one Postgres function via Supabase rpc, conditional `UPDATE ... WHERE balance >= cost`, append-only ledger with unique idempotency key, refund sweeper for stale reservations ([DEV credit system](https://dev.to/youngalgy/how-to-build-a-credit-system-for-a-nextjs-ai-app-stripe-supabase-heb)).
- **Stripe webhook dedup:** stores event IDs with unique constraint, return 200 on duplicates. Stripe delivery is at-least-once ([Activepieces](https://www.activepieces.com/blog/webhook-idempotency-how-to-handle-duplicate-events-2026)).
- **Anonymous endpoint defense:** Turnstile free plan has unlimited challenges ([Cloudflare](https://developers.cloudflare.com/turnstile/plans)). Add per-IP daily limit, global spend cap, input and max_tokens caps.
  - HF proxy: everyone may look like one IP, and raw `X-Forwarded-For` is spoofable. Test with a forged header on the live Space. HF behavior was not found in sources.
- **Uploads = untrusted:** treat uploaded JD text as data. Extract, cap size, wrap in delimiters, no tools or secrets in that prompt, validate output fields. Injection cannot be fully prevented ([OWASP LLM01](https://genai.owasp.org/llmrisk/llm01-prompt-injection/), not fetched; secondary summaries only).
- **Speed and cost:** put static instructions first, user data last to use automatic prefix caching (OpenAI-style, 1024+ tokens; discounts vary). Cache by hash of normalized intake for demos. Stream text for perceived speed (not verified in FastAPI sources). Health endpoint plus free uptime pinger for HF sleep (free Spaces sleep after 48h; forum reports of restrictions on free tier conflict with official docs, so verify) ([HF docs](https://huggingface.co/docs/hub/en/spaces-overview)).
- **Observability:** Langfuse free tier reportedly 50k units/month, 30-day retention ([Langfuse](https://langfuse.com/pricing)); check the live page.

**For employers viewing the portfolio (inference, no source on recruiter reaction):**
- Public `/eval` page from the existing eval harness: per-model quality, cost per JD, date, dataset size. Use LLM-as-judge only with pairwise position swap and criterion rubrics, cross-checked on a second provider or human samples ([Cameron Wolfe](https://cameronrwolfe.substack.com/p/llm-as-a-judge)).
- `/architecture` page with a diagram: intake -> generate -> validate -> lint -> render.
- Open-source the linter and eval set. Changelog of score by prompt version. Include injection test cases.
- Publish real cost per JD. Current model pricing was not verified; measure it.

## Ranked roadmap (impact vs effort)

Effort: S = under a day, M = a few days, L = a week plus. Impact: judgment, not measured.

| # | Item | Impact | Effort | Why |
|---|---|---|---|---|
| 1 | Replace $1 pack with $5/$10/$20 packs | High | S | 32.9% fee at $1; pure margin fix |
| 2 | Atomic credit ledger + Stripe webhook dedup + refund on failed refine | High | M | Money bugs are costly and visible |
| 3 | Turnstile + trusted-IP rate limits + daily spend cap on anon endpoint | High | M | Protects near-zero budget |
| 4 | Free signup abuse stack (confirm email first, disposable blocklist, normalized-email grant, custom SMTP) | High | S-M | Stops free-credit farming |
| 5 | Quality report (rule linter: bias, age, pay, sections, readability) | High | M | Main visible edge over free rivals |
| 6 | Pay-range field + jurisdiction toggle + warning | High | S | Legal need; many ads fail it |
| 7 | Refine chips + section regenerate + undo/version history + "what changed" | High | M | Cuts friction, makes cost predictable |
| 8 | Paywall flow: keep draft, auto-resume after login/pay, cost on button | Med-High | S-M | Prevents lost work at highest-intent moment |
| 9 | Assumption flags + mandatory "why join"/team input + bullet caps | Med-High | S | Fixes top recruiter complaint |
| 10 | Upload-JD diff view ("what changed and why") | Medium | M | Unique niche feature |
| 11 | Public `/eval` + `/architecture` pages | Medium (portfolio High) | M | Proof for employers |
| 12 | Structured-output validation + retry, truncation handling | Medium | S | Reliability |
| 13 | Upload prompt-injection hardening + tests | Medium | S | Safety, good portfolio story |
| 14 | Prompt-cache ordering, response cache, health pinger | Low-Med | S | Cost and cold-start |
| 15 | Free grant tuning (30 vs 10+20 staged) | Low-Med | S | Depends on measured cost per refine |
| 16 | Screening questions / tone variants extra | Medium | M | Adjacent value, rivals offer it |
| 17 | SEO: sample above fold, roundup listings, role pages feeding wizard | Medium | M, ongoing | Discovery |
| 18 | Open-source linter + eval set | Low-Med | M | Portfolio polish |

Suggested order: do 1, 6, 9 first (small, quick). Then 2-4 (safety before growth). Then 5, 7, 8. Then portfolio items 11, 13, 18.

## Unknowns to close first
- Actual LLM, tokens and cost per generate and per refine. All cost math here assumes numbers.
- Real client IP behind HF proxy; HF free-tier limits and any recent restrictions.
- First-pack purchase rate at $5 vs $1. No data; instrument it.
- Which refine chips get used.
- Jurisdiction penalty amounts, credit expiry law, Textio and LinkedIn 2026 pricing: unconfirmed.
- No conversion data on wizard vs chat vs single prompt, or on login-wall timing. Run own tests.

## Takeaway

Gap is trust and money plumbing, not features. A free no-login tool with a visible quality report, a clean $5 prepaid pack, and a public eval page is rare among free JD tools and cheap to build. Biggest risk is not competitors but the $1 pack and unguarded free endpoints draining a near-zero budget. Fix those, then measure real refine cost and chip usage before adding anything else.
