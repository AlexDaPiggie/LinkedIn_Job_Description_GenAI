# Refine/iteration UX and credit/pricing models for an AI job description generator

Scope note: ~15 tool calls. Many 2026 pricing sources are third-party aggregators that conflict; flagged. Official Stripe pages fetched directly. LLM per-refine cost math is my own calculation under stated assumptions (project model unknown).

## Q1. Is $1 / 30 credits viable after Stripe fees and LLM cost? Better pack structure?

### Takeaway
$1 pack loses 32.9% to Stripe (fixed 30c dominates). It is above the $0.50 floor but barely worth selling; one dispute ($15) wipes out ~15-30+ packs of profit. LLM cost per refine is tiny (~$0.0006-$0.017 depending on model), so the fee, not the LLM, is the problem. Move to a $5 minimum pack (e.g. $5 = 100 credits), plus optional $10 and $20 tiers.

### Cited Findings
- Stripe US standard online card fee: 2.9% + 30c per successful domestic card transaction; +1.5% for international cards; +1% if currency conversion; Checkout itself has no extra fee. - [Stripe pricing](https://stripe.com/pricing)
- Dispute fee $15 per dispute (countered: refunded only if you win). Refunds: no refund fee for cards, but original processing fee is NOT returned. - [Stripe pricing](https://stripe.com/pricing)
- Stripe enforces a USD minimum charge of $0.50 so its fee never exceeds the charge; below-minimum payments are rejected (amount_too_small). - [Stripe currencies](https://docs.stripe.com/currencies) (from search summary; page text not directly read)
- Third-party worked example: a $5 sale carries ~$0.45 fee (~9%). - [utilweb Stripe fees guide](https://utilweb.pages.dev/guides/how-stripe-fees-work) (secondary)
- Prepaid-credit precedent: OpenAI API requires prepaying with a $5 minimum. - [Orb prepaid credits guide](https://www.withorb.com/blog/an-ai-founders-guide-to-prepaid-credits) (secondary; $5 figure not verified on OpenAI's own page)
- LLM list prices (conflicting aggregators; unofficial): Haiku 4.5 $1 in / $5 out per M tokens; Sonnet 4.6 $3/$15; newer Oct 2026 listings show Sonnet 5/5.5 at $2/$10 and an unconfirmed Haiku 5.5 at $0.10/$0.50. Official page: platform.claude.com/docs/en/about-claude/pricing. - [Finout](https://www.finout.io/blog/anthropic-api-pricing), [BenchLM](https://benchlm.ai/anthropic/api-pricing)
- Chargebee: keep dollar-to-credit simple ("1 credit per dollar, or 10, or 100, never a fraction"); price the outcome the customer recognizes, not compute; apply volume discounts at the dollar-to-credit layer; self-serve out-of-credit = hard paywall; roll over whole credits rather than partial. - [Chargebee](https://www.chargebee.com/blog/how-to-make-credit-based-pricing-work-design-sell-and-scale-a-credit-model/)
- Chargebee: 75%+ of AI cost often comes from 1% or fewer of users; avoid flat per-user caps. - same source

### Inferences (my math, 2.9% + $0.30, domestic card)
| Pack | Stripe fee | Fee % | Net to you |
|---|---|---|---|
| $1 | $0.329 | 32.9% | $0.671 |
| $2 | $0.358 | 17.9% | $1.642 |
| $3 | $0.387 | 12.9% | $2.613 |
| $5 | $0.445 | 8.9% | $4.555 |
| $10 | $0.590 | 5.9% | $9.410 |
| $20 | $0.880 | 4.4% | $19.12 |
- International card: add 1.5% (+1% FX), so a $1 pack nets ~$0.65 or less.
- LLM cost per refine, ASSUMING ~1,500 input + ~800 output tokens (draft + feedback in, revised JD out): Haiku 4.5 ~$0.0055; Sonnet 4.6 ~$0.0165; hypothetical $0.10/$0.50 model ~$0.0006. If 1 credit = 1 refine, 30 credits cost $0.02-$0.50 in LLM. $1 pack profit if fully used: ~$0.50 (Haiku) down to ~$0.17 (Sonnet), before refunds, support time, taxes. A $15 dispute = 30-90 packs of profit. Not worth it.
- Free grant cost: 30 free credits = max ~$0.02-$0.50 per signup if all spent; fine at Haiku-class cost, risky at Sonnet-class with abuse.
- Suggested structure (no subscription; one-time Checkout mode=payment): $5 = 100 credits (starter, ~9% fee), $10 = 250 (+25% bonus), $20 = 600 (+50% bonus). Or one default $5 button. Keep 1 credit = 1 refine (plain outcome); put discounts in credit count, not price. Remeasure once real LLM cost per refine is logged. Subscription not recommended at this scale: recruiters hire in bursts, prepaid packs avoid churn/dunning complexity (judgment, not sourced).

### Gaps
- Project's actual LLM and tokens per refine unknown; costs above are assumptions.
- Official Anthropic pricing page not fetched; aggregators conflict on newest models.
- No data on first-pack purchase rate at $5 vs $1.

## Q2. Comparable-tool pricing and freemium conversion; free-credit grant size

### Takeaway
Comparable tools gate AI via small free allowances plus $29-$79/mo subscriptions; JD-specific generators are mostly free lead-gen (Grammarly, GoHire, Recooty, Workable). A prepaid pack is unusual and cheap relative to subscriptions, a differentiator for occasional recruiters. Freemium conversion: typically 2-5%, strong 8-12% (not AI-specific).

### Cited Findings
- Teal free: ~10 AI bullet credits, 2 summaries, 2 cover letters; reviewers say credits run out fast. Teal+ about $13/week, $29/month, $79/quarter, no annual plan. - [Dupple comparison](https://dupple.com/learn/best-ai-resume-builders), [LoopCV Teal review](https://blog.loopcv.pro/teal-hq-review/) (secondary; prices vary by source)
- Jasper: no permanent free plan, 7-day trial; Pro ~$59/mo annual or $69 monthly; Business custom (reportedly ~$125/seat). - [DEV Jasper pricing](https://dev.to/techsifted/jasper-ai-pricing-2026-creator-vs-pro-vs-business-plans-compared-3ei7), [CostBench](https://www.costbench.com/compare/jasper-vs-copy-ai/) (secondary, conflicting)
- Copy.ai: ~$29/mo chat plan; workflow credits (Starter 500/mo, Advanced 2,000/mo); free 2,000 words/mo reported. - [eesel Copy.ai pricing](https://eesel.ai/blog/copy-ai-pricing) (secondary, conflicting)
- Writesonic: free 25 credits/mo; paid reported $49-$79/mo entry, higher $199/$399; credit rollover unconfirmed. - [DEV Writesonic](https://dev.to/techsifted/writesonic-pricing-2026-lite-vs-standard-vs-professional-plans-2pd3) (secondary, conflicting)
- Notion AI: bundled in Business ($20/user/mo annual); Custom Agents credits reported $10 per 1,000 credits, pooled, monthly reset, no rollover; Notion publishes no numbers for included AI allowance. - [Breeze Notion AI pricing](https://www.breeze.pm/articles/notion-ai-pricing), [Notion help](https://www.notion.com/fi/help/standard-select-and-notion-credits-eligible-features) (conflicting)
- Textio: no public pricing; priced by open jobs; limited trial. Free JD tools exist: Grammarly (no signup), GoHire, Recooty, Workable (gated). - [Metaview roundup](https://www.metaview.ai/resources/blog/free-ai-job-description-generators), [Toolsforhumans Textio](https://toolsforhumans.ai/ai-tools/textio)
- Freemium conversion: median 8% across products but wide spread (a quarter <2.5%, a quarter 10-15%); freemium "good" 3-5%, "great" 8-12%; First Page Sage 3.7%; trials 15-25%. - [ChartMogul Conversion Report](https://chartmogul.com/reports/saas-conversion-report/), [Appcues](https://www.appcues.com/blog/free-to-paid-conversion)
- Credit design: show cost before action, real-time balance, low-balance alerts, cap spend, never surprise with overages; append-only ledger and idempotency. - [Schematic](https://schematichq.com/blog/ai-credit-overages), [Flexprice](https://flexprice.io/blog/how-to-implement-credit-based-billing-for-ai-applications), [Metronome](https://metronome.com/blog/the-rise-of-ai-credits-why-cost-plus-credit-models-work-until-they-dont)
- Unspent credits are deferred revenue/liability; legal treatment of prepaid value varies by jurisdiction. - [Lago](https://getlago.com/blog/credit-based-pricing)

### Inferences
- 30 free refines is generous vs Teal (10+2+2 AI actions) and Writesonic (25/mo). With 2-5% conversion, 100 signups x 30 credits at Haiku-class cost ~= $0.5-$17 of cost vs 2-5 buyers x ~$4.55 net = $9-$23. OK at cheap model; at Sonnet-class consider 10-15 free credits. Since generation is free and refine is the gated action, 10-15 credits likely enough to show value (judgment). Option: 10 on signup + 10 after verified email/first save.
- 2-5% is a SaaS-wide benchmark; no recruiter-specific figure found.

### Gaps
- No official pricing pages fetched for Jasper/Copy.ai/Writesonic/Grammarly/Canva (aggregators only; conflicting). No Canva/Grammarly credit numbers found.
- No AI-specific free-to-paid benchmark.

## Q3. Gating and paywall UX at the refine moment

### Takeaway
Sources: let users get value first (free generation), gate at highest intent (refine), show cost and balance inline, hard paywall at zero credits rather than mid-work cutoff. No hard A/B data on login-wall timing found.

### Cited Findings
- Self-serve out-of-credit is typically a hard paywall; avoid cutting people off mid-work. - [Chargebee](https://www.chargebee.com/blog/how-to-make-credit-based-pricing-work-design-sell-and-scale-a-credit-model/)
- Preview the cost of an AI action before executing; alerts before balance runs dry. - [Metronome](https://metronome.com/blog/the-rise-of-ai-credits-why-cost-plus-credit-models-work-until-they-dont), [Schematic](https://schematichq.com/blog/ai-credit-overages)
- Stripe fulfillment: webhooks required to grant credits (do not rely on success page); handler must be idempotent per Checkout Session ID, and also run on the landing page for instant balance; Checkout waits up to 10s for webhook response before redirect; handle checkout.session.async_payment_succeeded/failed for delayed methods. - [Stripe fulfillment docs](https://docs.stripe.com/checkout/fulfillment)
- Adapty "State of Paywalls 2026" covers 78,000+ paywalls (mobile subscription focus); not read in detail. - [Adapty](https://adapty.io/blog/freemium-to-premium-conversion-techniques)

### Inferences
- Graceful flow (synthesis): logged-out user clicks Refine -> keep draft and typed feedback in localStorage -> sign-in modal (Google/magic link) "Sign in to refine - N free credits" -> after auth, auto-run the pending refine. Never lose the draft. At zero credits: modal with draft intact, "Copy/download still free", one-click $5 Checkout, return and auto-resume. Button label "Refine - 1 credit (28 left)". Low-balance nudge at 3 left.
- Keep copy/export free so refine is value-add, not hostage.

### Gaps
- No A/B data on login-wall timing (before generate vs at refine).

## Q4. Refine UX features users expect beyond free-text feedback

### Takeaway
Tools converge on chat/prompt refine + selection-based inline edit + one-click shortcuts (length, reading level, tone) + version back/restore. NN/g reports users frequently iterate via follow-up prompts; prompt-assist patterns (suggested rewrites, parametrization) reduce the burden of articulating feedback.

### Cited Findings
- NN/g: in testing, users frequently refine AI output through additional prompts (snippet only; full article not read). - [NN/g Accordion Editing & Apple Picking](https://www.nngroup.com/articles/accordion-editing-apple-picking/)
- Nielsen prompt-augmentation patterns: style galleries, prompt rewrite, targeted prompt rewrite, related prompts, prompt builders, parametrization. - [UX Tigers](https://www.uxtigers.com/post/prompt-augmentation)
- ChatGPT canvas: "Adjust the length" slider (shortest to longest), "Reading level" slider (kindergarten to graduate school), back button/arrows to view and restore previous versions; inline highlight-and-ask editing. Whether shortcuts apply to whole doc vs selection is unconfirmed. - [OpenAI Help: canvas](https://help.openai.com/en/articles/9930697-what-is-the-canvas-feature-in-chatgpt)
- Pattern "Response refinement": contextual menu on output to modify without retyping the prompt. - [AI UX Playground](https://aiuxplayground.com/pattern/response-refinement)
- Microsoft Research dynamic prompt middleware: generate inline refinement options users click instead of typing. - [arXiv 2412.02357](https://arxiv.org/html/2412.02357v1)
- Notion AI case study: inline "Edit with AI" chosen over chat sidebar because the task is editing text (secondary). - [UX Collective](https://uxdesign.cc/the-chat-box-isnt-a-ui-paradigm-it-s-what-shipped-96e931d92769)

### Inferences (JD-specific synthesis)
- Quick-action chips (each 1 credit): Shorter, More inclusive (flag gendered/biased wording), Add salary range, More casual/formal, Add benefits, Simplify jargon, Mark requirements nice-to-have, Remote-friendly. Chips remove articulation burden and make cost predictable.
- Section-level regeneration (Responsibilities, Requirements, Benefits) cuts tokens and avoids rewriting parts the recruiter liked; "lock section" is cheap client-side and prevents regressions.
- Version history (last ~5 drafts in localStorage) with Undo and highlighted diff builds trust at zero LLM cost; consider making Undo free.
- Return a short "what changed" summary with each refine.

### Gaps
- No usage data on which refine features recruiters use most. NN/g full text and Reddit/HN threads not retrieved.

## Q5. Anti-abuse for free credits at near-zero cost; refund/failed-generation policy

### Takeaway
Layered cheap defenses: verified (non-anonymous) login via Google/email OTP, CAPTCHA (Turnstile/hCaptcha), disposable-email blocklist, per-IP and per-account rate limits, per-request token caps, small free grant, credits granted server-side only. Deduct a credit only on a successful refine.

### Cited Findings
- Stripe guide: tighten in order - bot detection, disposable email blocking, device fingerprinting, progressive verification/payment; monitor 2-4 weeks first; stricter controls only for high-risk cohorts; track infra cost per trial account; per-session token caps; rate-limit by credential not IP alone; signals: signup velocity by IP/subnet/ASN, reused phone/payment/device. - [Stripe: preventing free trial abuse](https://stripe.com/resources/more/how-to-prevent-free-trial-abuse-in-saas-and-ai-products)
- Stripe illustrative example: 200 abusive accounts on a 10,000-token trial burn 2M tokens free. - same
- A search summary claimed Stripe estimates 7.4% of AI signups are free-account abuse; the Stripe page I fetched did NOT contain 7.4%, so UNVERIFIED. Canva AI credit seat-cycling abuse also reported. - [Socure blog](https://www.socure.com/blog/what-fake-accounts-are-really-costing-ai-platforms) (vendor)
- Vendor reports: $220 of GPU credits burned in an hour via disposable emails; one phone number could register unlimited accounts at OpenAI. - [Checkmarx](https://checkmarx.com/blog/openai-allowed-unlimited-credit-on-new-accounts/), [ShieldLabs](https://shieldlabs.ai/blog/trial-farming-ai) (vendors, unverified)
- Social login shifts verification to the OAuth provider (vendor claim; some abusers slip through). - [Verisoul](https://www.verisoul.ai/industries/saas-ai-tech)
- Supabase: anonymous sign-ins limited to 30/hour per IP (not customizable); 429 on limit; supports hCaptcha and Cloudflare Turnstile on sign-in/sign-up/reset; forum report that CAPTCHA breaks signInAnonymously unless a token is passed. - [Supabase rate limits](https://www.supabase.com/docs/guides/auth/rate-limits), [Supabase CAPTCHA](https://supabase.com/docs/guides/auth/auth-captcha)
- Turnstile hostname matching can be bypassed via preview deployments using your site key (Vercel community post). - [Vercel community](https://community.vercel.com/t/supabase-cloudflare-turnstile-hostname-matching-doesn-t-cover-vercel-preview-deployment-subdomains/33043)
- Built-in Supabase email is ~2/hour project-wide (third-party table); signup floods can drain it, so use custom SMTP. - [vibe-eval](https://vibe-eval.com/fix/supabase-rate-limit-api/) (secondary)
- Metering: append-only ledger, idempotency, real-time balance. - [Flexprice](https://flexprice.io/blog/how-to-implement-credit-based-billing-for-ai-applications)

### Inferences
- Cheapest stack (free tiers): Turnstile on signup + confirmed email (OTP already built) + disposable-domain blocklist + grant credits only after email confirmation, server-side/DB trigger + per-user and per-IP rate limit on /refine (e.g. 10/min) + max input/output token caps + global daily LLM spend cap/kill switch + one free grant per normalized email (strip Gmail dots/+tags). Optional: release half of free credits after first successful action.
- Credit policy: deduct after successful response (or reserve then commit); auto-refund credit on LLM error/timeout/empty or malformed output; ledger entry per request with idempotency key. Paid refunds only on request; processing fee not returned (a refunded $1 pack still costs ~$0.33). Spent credits non-refundable; state expiry (none or 12-24 months) in terms.
- Do not rely on IP-only limits (shared agency/corporate networks cause false positives).

### Gaps
- No source on abuse rates for small projects; vendor data is biased. No source on legal rules for credit expiry/refund (jurisdiction varies). Reddit/HN threads on recruiter-tool pricing not retrieved.
