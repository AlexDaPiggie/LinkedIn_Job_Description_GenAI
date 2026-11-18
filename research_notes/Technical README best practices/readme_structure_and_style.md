# README structure and writing style in well-documented products

Method note: READMEs for 15 repos were downloaded raw from GitHub (HEAD, fetched 2026-11-17) and measured with `wc` plus heading extraction. Line/word counts include HTML and code blocks, so they overstate prose length. Repo URLs are given as `https://github.com/<owner>/<repo>`.

## 1. Section order, length and above-the-fold content of real product READMEs

### Takeaway
Product READMEs (Supabase, PostHog, Plausible, Next.js, Twenty, Immich) are short landing pages: logo, one-line pitch, a row of 4-7 links (Docs / Cloud / Self-host / Demo / Community), a short "what it is" paragraph, then getting-started and pointers out to a docs site. Libraries (Stripe SDKs, FastAPI) are longer because the README doubles as usage reference. The very long ones (Cal.com 837 lines, Langfuse 414, Ollama 358) get long from integration lists or credential-setup steps, not from prose.

### Cited Findings

Measured length (lines / words, raw markdown):
- Next.js `packages/next/README.md`: 50 lines / 291 words. Sections: Getting Started, Documentation, Community, Contributing, Good First Issues, Security. Almost everything links to nextjs.org - [vercel/next.js](https://github.com/vercel/next.js/blob/canary/packages/next/README.md)
- Excalidraw: 124 / 495. Sections: Features, Excalidraw.com, Quick start, Contributing, Integrations, Who's integrating, Sponsors - [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw)
- Immich: 128 / 508. Sections: Links, Demo (with login credentials table), Features (feature x Mobile/Web table), Translations, Repository activity, Contributors - [immich-app/immich](https://github.com/immich-app/immich)
- Twenty: 176 / 826. Sections: Why Twenty, Installation (Cloud / Build an app / Self-hosting), Everything you need, Stack, Thanks, Join the Community - [twentyhq/twenty](https://github.com/twentyhq/twenty)
- Dify: 184 / 1018. Sections: Quick start, Key features, Using Dify, Staying ahead, Advanced Setup, Contributing, Community, Star History, Security disclosure, License - [langgenius/dify](https://github.com/langgenius/dify)
- Supabase: 288 / 1133. Sections: (feature checklist), Documentation, Community & Support, How it works (architecture diagram + one line per component), Badges, Translations - [supabase/supabase](https://github.com/supabase/supabase)
- PostHog: 178 / 1278. Sections: "PostHog is your product's context layer", Table of Contents, Getting started (Cloud recommended / self-host hobby deploy "Advanced"), Setting up, Learning more, Contributing, Open-source vs. paid, We're hiring - [PostHog/posthog](https://github.com/PostHog/posthog)
- Infisical: 194 / 1527. Sections: Introduction, Features (one sub-heading per product area), Getting started, Open-source vs. paid, Security, Contributing, We are hiring - [Infisical/infisical](https://github.com/Infisical/infisical)
- Plausible: 143 / 1627. Sections: (pitch + 5 bullets + dashboard screenshot), Why Plausible?, Why is Plausible Analytics Cloud not free like Google Analytics?, Getting started, Can Plausible be self-hosted?, Technology, Contributors, Feedback & Roadmap, License & Trademarks - [plausible/analytics](https://github.com/plausible/analytics)
- Ollama: 358 / 1629. Download (per-OS one-line install), Get started, REST API, Python/JS, Supported backends, Documentation, then a long Community Integrations list split into ~11 categories - [ollama/ollama](https://github.com/ollama/ollama)
- FastAPI: 535 / 2428. Sponsors, Opinions (quotes from engineers at Microsoft, Uber, Netflix etc.), Requirements, Installation, Example (Create / Run / Check / Interactive docs), Example upgrade, Recap, Performance, Dependencies, License - [fastapi/fastapi](https://github.com/fastapi/fastapi)
- stripe-python: 486 / 2526; stripe-node: 734 / 3247. Order: title, version/build badges, tip box (Discord), one-paragraph description, link to API docs, Requirements, Installation, Usage, then many Configuration sub-sections (retries, proxy, webhooks, telemetry, preview SDKs), Support, Development - [stripe/stripe-python](https://github.com/stripe/stripe-python), [stripe/stripe-node](https://github.com/stripe/stripe-node)
- Langfuse: 414 / 3649. Emoji-prefixed headings: Core Features, Deploy, Integrations, Quickstart (incl. "Agentic installation (recommended)"), Support, Contributing, License, Star History, Security & Privacy / Telemetry - [langfuse/langfuse](https://github.com/langfuse/langfuse)
- Cal.com repo (now presented as "Cal.diy" community edition): 837 / 4680. Most length is Deployment (6 hosting targets) and "Integrations" with ~12 "Obtaining X Client ID and Secret" sub-sections - [calcom/cal.com](https://github.com/calcom/cal.com)

Above the fold (first ~15 rendered lines):
- Ollama opens with the name, one sentence ("Start building with open models..."), then a copy-paste install command per OS. No badges, no feature list - [ollama/ollama](https://github.com/ollama/ollama)
- Supabase: name, one sentence ("Supabase is the Postgres development platform"), second sentence on approach, then a checked feature list where every item links to its docs page - [supabase/supabase](https://github.com/supabase/supabase)
- Plausible: logo, link row (Live Demo / Open Source / Docs / Contributing), one-paragraph positioning ("open source, privacy-first web analytics tool... alternative to Google Analytics"), 5 short linked bullets, then a dashboard screenshot - [plausible/analytics](https://github.com/plausible/analytics)
- Immich: tagline "High performance self-hosted photo and video management solution", language links, a WARNING callout about the 3-2-1 backup rule, a NOTE saying main docs are on immich.app, then a Links list and a public demo with credentials - [immich-app/immich](https://github.com/immich-app/immich)
- Stripe SDKs: title, 2-3 badges (version, build, downloads), tip callout, a 1-2 sentence plain description ("provides convenient access to the Stripe API from applications written in..."), then "See the API docs" - [stripe/stripe-node](https://github.com/stripe/stripe-node)
- FastAPI: logo, tagline, badges, explicit "Documentation:" and "Source Code:" links, then one definition sentence and a bold-keyword feature list - [fastapi/fastapi](https://github.com/fastapi/fastapi)
- Langfuse and Dify: logo/cover image, a link row (Cloud / Self-host / Demo / Docs), then a wall of shields.io badges (Discord, X, Reddit, LinkedIn, etc.) before the first sentence of prose - [langfuse/langfuse](https://github.com/langfuse/langfuse), [langgenius/dify](https://github.com/langgenius/dify)
- Next.js: logo, badges, then "Getting Started" whose first sentence is a positioning line, then links to the Learn course and Showcase - [vercel/next.js](https://github.com/vercel/next.js/blob/canary/packages/next/README.md)

Recurring sections:
- "Cloud vs self-host" split with Cloud marked recommended: PostHog ("PostHog Cloud (Recommended)" / "Self-hosting... (Advanced)"), Twenty (Cloud / Build an app / Self-hosting), Langfuse, Dify - [PostHog](https://github.com/PostHog/posthog), [Twenty](https://github.com/twentyhq/twenty)
- Architecture shown once, briefly: Supabase has a single "How it works" section with an SVG architecture diagram and one sentence per component (Postgres, Realtime, PostgREST, GoTrue, Storage, etc.) - [supabase/supabase](https://github.com/supabase/supabase)
- "Stack"/"Technology" as a short section near the end: Twenty ("Stack"), Plausible ("Technology"), Cal.com ("Built With") - [Twenty](https://github.com/twentyhq/twenty), [Plausible](https://github.com/plausible/analytics)
- Honest business-model section: Plausible "Why is Plausible Analytics Cloud not free like Google Analytics?"; PostHog and Infisical "Open-source vs. paid" - [Plausible](https://github.com/plausible/analytics), [Infisical](https://github.com/Infisical/infisical)
- Live demo with shared login (Immich, Plausible "Live Demo", Langfuse "Demo") - [Immich](https://github.com/immich-app/immich)

### Inferences
- Common skeleton for a hosted product: (1) name + one-line "X is a Y for Z", (2) link row, (3) screenshot, (4) 3-6 feature bullets each with a fact, (5) try it (live URL / demo) and run it locally, (6) how it works (one diagram + one line per part), (7) stack, (8) links out, license.
- Under ~300 lines of prose is the norm when a docs site exists. Length beyond that comes from reference material (SDK config, integration lists, per-provider credential steps) which is exactly what guides say to move out.
- For a 2-person portfolio SaaS, the closest models are Plausible (small team, screenshot early, plain "why" section, Technology section), Supabase's "How it works" (diagram + one line per service maps directly onto FastAPI / Supabase / Stripe / OpenRouter), and Immich's live demo + callouts. The Stripe SDK and Cal.com depth is not a fit.
- Benchmark charts fit as a dedicated short section with one image and 2-3 sentences of method (what was measured, how many samples, date), in the spirit of FastAPI's "Performance" section, which links to an external benchmark rather than asserting.

### Gaps
- Next.js root `readme.md` is a symlink to `packages/next/README.md`; counted the package file.
- Line counts measure markdown source, not rendered height; no screenshot-based "above the fold" measurement was done.
- Did not check the Stripe docs site structure itself, only the SDK READMEs.

## 2. Writing style: tone, sentence length, first person, claims vs facts

### Takeaway
The best READMEs define the product in one plain sentence ("X is a Y"), then back claims with links, numbers, diagrams or demos. First-person plural ("we") appears for mission and business-model text, not for features. The boastful patterns that do exist in praised repos (Twenty's "#1 Open-Source CRM", FastAPI's percentage claims) are either marketing taglines or footnoted, and are not a safe model for a portfolio project.

### Cited Findings
- Definitional opening sentences: "Supabase is the Postgres development platform." / "Plausible Analytics is an open source, privacy-first web analytics tool." / "FastAPI is a modern, fast (high-performance), web framework for building APIs with Python..." / "Dify is an open-source LLM app development platform." - [Supabase](https://github.com/supabase/supabase), [Plausible](https://github.com/plausible/analytics), [FastAPI](https://github.com/fastapi/fastapi), [Dify](https://github.com/langgenius/dify)
- Stripe SDKs use the most neutral register: the library "provides convenient access to the Stripe API", with no adjectives about quality, and they immediately state scope limits (use Stripe.js for browser-side collection) - [stripe/stripe-node](https://github.com/stripe/stripe-node)
- Supabase uses "we" to state a principle: they use existing open-license tools where they exist and build them otherwise - a design decision, not a claim of superiority - [supabase/supabase](https://github.com/supabase/supabase)
- Plausible's "Why Plausible?" bullets pair each benefit with a concrete mechanism ("No personal data or IP addresses are stored, and no cookies or persistent identifiers are used") and a link to the policy - [plausible/analytics](https://github.com/plausible/analytics)
- Infisical uses "We're on a mission to make security tooling more accessible..." - first person reserved for intent - [Infisical/infisical](https://github.com/Infisical/infisical)
- Inflated claims in praised repos: Twenty's tagline is "The #1 Open-Source CRM" - [twentyhq/twenty](https://github.com/twentyhq/twenty). FastAPI claims "Increase the speed to develop features by about 200% to 300%" and "Reduce about 40% of human (developer) induced errors", both marked with an asterisk footnote, and links its speed claim to a Performance section - [fastapi/fastapi](https://github.com/fastapi/fastapi). Next.js: "Used by some of the world's largest companies" with a link to the Showcase - [Next.js](https://github.com/vercel/next.js/blob/canary/packages/next/README.md)
- Google developer docs style guide: conversational, friendly, respectful; show some personality but do not try to entertain; avoid buzzwords and jargon, exclamation marks, "simply", "it's easy", "quickly" in procedures, "please note", and choppy or long-winded sentences - [Google developer documentation style guide: Voice and tone](https://developers.google.com/style/tone)
- Make a README: description should say what the project does and give context; comparing against alternatives can help; usage should show the smallest example with expected output - [Make a README](https://www.makeareadme.com/)

### Inferences
- Rule of thumb from the samples: every adjective needs a receipt (number, link, screenshot, chart). "Fast" becomes "p50 latency 1.8 s on model X (chart below)".
- "We" works for a 2-person team when stating decisions ("we chose OpenRouter so models can be swapped without code changes"). Avoid "we" for praise.
- A portfolio README cannot borrow a company's social proof (FastAPI's "Opinions", Next.js's "largest companies"). The substitute is evidence: live URL, screenshots, benchmark method, tests.
- Comparisons to other products or models ("better than most AI models") read as boastful unless the README shows the benchmark, sample size and date. Plausible's Google Analytics comparison works because it is about mechanism (no cookies), not superiority.

### Gaps
- No quantitative study of sentence length in top READMEs was found; style observations are from direct reading.
- Google's tone page does not explicitly address marketing hype or second person in that excerpt.

## 3. What stays in the README vs /docs, CONTRIBUTING, ARCHITECTURE.md, docs site

### Takeaway
Products with a docs site keep the README as a router: one sentence per topic plus a link. Contributor setup, security policy and deep architecture live in CONTRIBUTING.md, SECURITY.md and the docs site. ARCHITECTURE.md (matklad) is a short codemap for contributors, separate from the README.

### Cited Findings
- CONTRIBUTING.md exists at root in Supabase, PostHog, Plausible, Langfuse, Ollama, Excalidraw, Immich, Infisical, Dify; SECURITY.md in Plausible, Langfuse, Ollama, Infisical, Dify (checked by HTTP 200 on raw URLs) - [Supabase](https://github.com/supabase/supabase), [Dify](https://github.com/langgenius/dify)
- None of the sampled repos had a root ARCHITECTURE.md (checked root and docs/); Supabase puts a diagram in the README instead - [supabase/supabase](https://github.com/supabase/supabase)
- Immich README explicitly says main documentation including installation guides is on immich.app, and its Links section is just pointers (Documentation, Installation, Roadmap, Contributing) - [immich-app/immich](https://github.com/immich-app/immich)
- Next.js README: "Visit https://nextjs.org/docs to view the full documentation"; contributing defers to `contributing.md`; security says to disclose responsibly and NOT open a public issue - [Next.js](https://github.com/vercel/next.js/blob/canary/packages/next/README.md)
- Supabase feature list items each end with a "[Docs]" link rather than an explanation - [supabase/supabase](https://github.com/supabase/supabase)
- Counter-example: Cal.com keeps ~12 per-provider OAuth credential walkthroughs in the README, pushing it to 837 lines - [calcom/cal.com](https://github.com/calcom/cal.com)
- GitHub docs: a README typically covers what the project does, why it is useful, how to get started, where to get help, and who maintains it; GitHub renders an automatic outline from headings; content beyond 500 KiB is truncated; prefer relative links to repo files - [GitHub Docs: About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes)
- matklad: add an ARCHITECTURE document next to README and CONTRIBUTING, aimed at projects of roughly 10k-200k lines; keep it short; include only things unlikely to change frequently; structure it as bird's-eye overview, then a codemap of coarse modules (where does the code for X live), then cross-cutting concerns; name files/modules/types but do not link them (links rot); call out invariants, especially ones expressed as an absence; mark layer boundaries - [matklad: ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html)
- Diataxis: four kinds of docs - tutorials (learning), how-to guides (doing a task), reference (accurate facts mirroring the system), explanation (why); blurring them is "at the heart of" many documentation problems, e.g. a tutorial overloaded with explanation - [Diataxis: Start here](https://diataxis.fr/start-here/)
- Make a README: "too long is better than too short", but when it gets unwieldy, move content to a wiki or docs site rather than deleting it - [Make a README](https://www.makeareadme.com/)
- Write the Docs template sections: title and description with a short usage example, features, installation, contribute, support, license - [Write the Docs: Beginner's guide](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/)
- Art of README's "cognitive funneling": order from broad and most pertinent to specific, so readers can quickly decide whether to keep going; keep structure consistent and brief - [Art of README (mirror)](https://benbridle.com/art-of-readme.html); summarized by [Dendron wiki](https://wiki.dendron.so/notes/v4buc90lf8w7ak0240qmaae/) and [Abilian lab](https://lab.abilian.com/Tech/Documentation/READMEs)

### Inferences
- Diataxis mapping for a README: the README is mostly "explanation lite" (what/why) + a minimal tutorial (run it locally). Reference (env var tables, API endpoints) and how-tos (rotate Stripe webhook secret, add a model) belong in `docs/`.
- For a small FastAPI/Supabase/Stripe/OpenRouter app (likely well under matklad's 10k-line floor), a separate ARCHITECTURE.md is optional; a short "How it works" section with one diagram plus a 5-10 line codemap in the README may be enough. If written, keep it to stable facts: request flow, where LLM calls happen, where credits/billing is enforced, invariants (e.g. "credits are only deducted server-side after a successful generation").
- Candidates to push out of the README: full env var reference, Stripe webhook setup, Supabase migration steps, model-by-model benchmark tables (keep one summary chart), per-provider setup.

### Gaps
- Original Art of README text (hackergrrl repo) returned 404 on several URLs; findings rely on a mirror and secondary summaries.
- Did not verify each repo's docs-site information architecture.

## 4. What makes a README look amateur or AI-generated

### Takeaway
Tells: emoji on every heading/bullet, badge walls before any sentence, generic openers, superlatives without evidence, development-status chatter, over-documentation of internals, and info in the wrong order (edge-case workarounds inside setup). Several praised repos use emoji or badge walls too, so the real signal is emoji/badges *instead of* substance, plus inaccuracy.

### Cited Findings
- AI-README tells named by a practitioner: emoji bullets, a stock-feeling header image saying nothing specific, and an opener about "today's fast-paced landscape" - [DEV Community: "Your AI slop bores me"](https://dev.to/eschmechel/your-ai-slop-bores-me-4g7k)
- NCC Group paper on LLM content: emoji bullets are common; LLMs use em dashes far more than humans; no single sign is proof - [NCC Group: Unmasking techno sophists (PDF)](https://www.nccgroup.com/media/l5cjcey2/unmasking_techno_sophists.pdf)
- Wikipedia's "Signs of AI writing" guide notes chatbots decorate headings/bullets with emoji and overuse em dashes, and cautions against relying on detectors - [Wikipedia: Signs of AI writing (via markdown.new)](https://markdown.new/https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
- Editorial failures of an AI-drafted README (Vanna W): it looks finished before anyone edited it; it reports build status ("All four are built") instead of what the reader can do; instructions technically accurate but unusable; a niche hardware workaround in the setup section; over-documentation of implementation details; development history mixed into user docs; emoji added "with unnerving confidence". Its limitations section was the part worth keeping - [HackerNoon: Treat AI-generated READMEs like first drafts](https://hackernoon.com/treat-ai-generated-readmes-like-first-drafts)
- Google style guide: no exclamation marks, no "simply/easy/quickly", no buzzwords, no cutesy phrasing - [Google developer documentation style guide: Voice and tone](https://developers.google.com/style/tone)
- Praised repos that still use emoji: Excalidraw's feature bullets (e.g. "Free & open-source", "Dark mode" each with an emoji), Plausible's 5 top bullets, Langfuse's headings - [Excalidraw](https://github.com/excalidraw/excalidraw), [Plausible](https://github.com/plausible/analytics), [Langfuse](https://github.com/langfuse/langfuse)
- Badge walls in praised repos: Langfuse and Dify show 5+ social/community badges before prose - [Langfuse](https://github.com/langfuse/langfuse), [Dify](https://github.com/langgenius/dify). Stripe SDKs show only 2-3 functional badges (version, build, downloads) - [stripe-node](https://github.com/stripe/stripe-node)
- Long feature lists in praised repos are grouped and each item is one linked line with a mechanism (PostHog groups under Analytics / Session replay / Observability) - [PostHog](https://github.com/PostHog/posthog)
- Hiring-side signal: vague repeated commit messages ("fix", "update") read as sloppy - [Underdog.io / aggregated in search](https://underdog.io/blog/what-hiring-managers-look-for-on-github)

### Inferences
- Patterns to avoid for this project:
  - Emoji on headings or as icons (also a user design rule).
  - Badge wall; at most CI status, license, maybe Python version. Social badges (Discord/X) only make sense with a real community.
  - Opening with adjectives ("powerful, cutting-edge AI-powered...") instead of "X generates LinkedIn job descriptions from a role brief."
  - Claims like "better than most AI models" - replace with the benchmark chart, models compared, metric, sample count, date, and a limitations note.
  - Full `tree` output of the repo; use a 5-10 line codemap of key folders only.
  - Install steps interleaved with marketing; keep "what/why" above, "run it" below, as a separate section.
  - Changelog-style status ("Phase 3 done", "All features built") in the README.
  - Em/en dashes and other LLM tells; typos; stale screenshots.
- Praised projects get away with emoji/badges because the substance underneath (live product, docs site, adoption) is real. A portfolio README has no such cushion, so the plain Stripe/Next.js register is safer.

### Gaps
- No rigorous study quantifies how reviewers react to emoji or badges; evidence is practitioner opinion and style guides.
- The Wikipedia guide was read via a mirror/proxy, not directly.

## 5. Portfolio READMEs: what hiring engineers say they want

### Takeaway
Credible hiring-manager writing is thin and mostly opinion, but it converges: write for developers while knowing a hiring manager is the real reader; show it running (screenshots, demo, live URL); explain architecture and decisions; give install steps; show impact; few well-finished projects beat many dumps.

### Cited Findings
- Alishah Novin (engineer turned engineering manager, 10+ years hiring): approach READMEs as if writing for other developers while "secretly thinking about the hiring manager"; include an overview, screenshots and a changelog to show you can communicate technical concepts; do not just upload the project and call it a day; meaningful projects over commit frequency; avoid many unfinished projects - [HackerNoon: FAQs for a software engineering hiring manager, part 3](https://hackernoon.com/faqs-for-a-software-engineering-hiring-manager-part-3-of-5-portfolios-and-githubs)
- Recruiter/hiring blog consensus (opinion, not data): 3-5 well-documented projects, clear README, screenshots/demos/videos, technical architecture explanation, business or user impact; a README without install instructions is a project nobody will try; pinned repos (max 6) are the only ones most visitors see - [Underdog.io: What hiring managers look for on GitHub](https://underdog.io/blog/what-hiring-managers-look-for-on-github); [Underdog.io: Software engineer portfolio](https://underdog.io/blog/software-engineer-portfolio)
- Sources conflict on contribution graphs (some call them overrated, others a consistency signal) - per aggregated search results including [Underdog.io](https://underdog.io/blog/what-hiring-managers-look-for-on-github)
- Make a README: state project status at the top if development slowed; show smallest usage example with expected output - [Make a README](https://www.makeareadme.com/)

### Inferences
- For a 2-person GenAI SaaS portfolio, the README should answer, in order, what a reviewer checks in 1-2 minutes: what it does (1 sentence), proof it works (live URL + screenshot/GIF), how it is built (diagram: frontend -> FastAPI -> Supabase (auth/DB) / Stripe (credits, webhooks) / OpenRouter (LLMs)), interesting engineering decisions and trade-offs (model routing, cost per generation, prompt/eval approach, idempotent Stripe webhooks, RLS), evidence (benchmark chart with method, tests/CI), run locally, team split (who built what - matters for a 2-person project), limitations / next steps.
- A short "Decisions" or "Trade-offs" section is the highest-signal portfolio addition and is mostly absent from product READMEs (which serve users, not reviewers). This is where portfolio READMEs should diverge from the product model.
- A "Limitations" section signals judgment (the HackerNoon author singled it out as the strongest part of the AI draft).

### Gaps
- Found no staff-engineer or big-company hiring manager writing with data on README impact; available sources are individual opinion and recruiter blogs, several of which are SEO content. Treat as heuristics.
- No source specifically on GenAI portfolio projects (e.g. expectations around evals, cost tracking, prompt versioning) was found in this pass.
