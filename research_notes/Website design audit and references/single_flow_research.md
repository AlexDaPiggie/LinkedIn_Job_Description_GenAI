# Single-flow tool page research

Legend: [V] = fetched text this session. [M] = memory, not verified. Not fetched: Workable page (404), Canva, Calendly, TinyWow, Typeform, Notion AI, Linear, Stripe Checkout (redirect only), Hemingway editor (landing only).

## 1. Tool-first pages
- Smallpdf Merge [V] smallpdf.com/merge-pdf: nav + breadcrumb + H1 + ONE drop zone / "Choose Files". 1 primary control. Below: intro, 6 feature blocks, 5-step how-to, 7 FAQ, blog, rating, tool directory, big footer. Tool alone above fold; the SEO tail is what NOT to copy at that size. [M] after upload the area becomes file thumbnails + one right-side panel with Merge.
- Grammarly AI detector [V] grammarly.com/ai-detector: H1 + short intro, then tool: 3 buttons (Scan, Upload, Try sample text) + result panel with one score. Below: why-choose, use cases, stats, related tools, 5 FAQ, CTA, footer. Sample-text button = cheap way to show a result.
- Wise converter [V] wise.com/gb/currency-converter: converter first (amount, from, to, one CTA). Then promo, app promo, chart, stats, FAQ, link lists. Result is live in place.
- remove.bg [V] remove.bg: headline "Remove Image Background 100% Automatically and Free" + one upload. Fetch showed no result state. Below: audiences, blog, newsletter, footer. [M] result replaces upload in place; download is the single primary; options in a narrow right column.
- Hemingway [V] landing is marketing only (trial CTA, links to free tools). [M] editor: big text area left, narrow right column with colour counts (adverbs, passive, hard sentences) and grade level. Document wide, tools narrow, counts not prose.
- Workable JD generator [V via search only] help.workable.com: copy without sign-in; sign-up keeps history. [M] title in, result below, sign-up to save.
- Typeform [M]: one question per screen, big type, progress bar, Enter to advance. Cost: no overview, no cross-comparison.
- Calendly [M]: booking page = info column, calendar, times appear only after a day is picked. Reveal in place; no marketing.
- Stripe Checkout [M]: summary left, payment form right; uncommon fields (promo code) collapsed; one pay button.
- Canva tools, TinyWow, Notion AI, Linear sign-up [M, unverified]: Canva tool pages = H1 + one upload/prompt + examples + FAQ; TinyWow = one input + one button per tool; Linear sign-up = one button per auth method.
Common pattern: 1 H1, 1 input zone, 1 primary button above fold; result replaces/extends input in place; extras in a side panel or link; marketing after, mostly FAQ + related tools.

## 2. Principles
- Progressive disclosure [V] nngroup.com/articles/progressive-disclosure/: few core options first, rest on request; max 2 levels (3+ gets users lost); avoid redundant routes to same secondary options; staged/wizard only when steps are independent, bad when users flip between steps; sometimes 2 screens beat 1 or 5.
- Hick's law [V] lawsofux.com/hicks-law/: decision time grows with number and complexity of choices; split complex work; flag the recommended option. Over-simplifying makes UI vague.
- Forms [V] nngroup.com/articles/web-form-design/: single column; cut fields; max 1-2 optional, labelled optional; labels above; group related fields; no placeholder-as-label; no Reset button.
- Baymard [V] baymard.com/blog/current-state-of-checkout-ux: optional fields often disrupted flows, steps 5-30% longer; hide uncommon optional fields behind a link; mark both required and optional (32% missed a required field when only optional was marked). Single-column not covered in that article.
- Editor + inspector, one primary action per view [M]: common design practice, no source fetched.

## 3. Patterns to reuse
(a) Compose -> result, same page: form collapses to a one-line summary ("Senior nurse, London, friendly - Edit - Regenerate") when result arrives; result takes the space; focus moves to result heading; no scroll jump.
(b) Document + narrow tools column: document ~680px, tools ~300px with collapsed groups: Check (show score number always), Quick edits (4 chips max), Refine (one box), Screening questions. One group open at a time. Undo = toast, not a bar. Change note = one line under the doc.
(c) Optional fields: required = job title (+ location). Everything else under one "Add detail (optional)" disclosure with a count badge when filled. Tone/length = one segmented control inside it with defaults. 10-question accordion becomes 3 prompts + "More questions", no side number rail.
(d) Marketing: one line under tool (pay card becomes a sentence: free to generate, refine costs credits), 4-item FAQ, one-row footer (Terms, Privacy, Contact, Templates). Drop how-it-works and the pricing section.
(e) Templates: gallery = plain list of text rows (title + one line) with one search box. Detail page = same tool page with the template pre-filled; no new layout.

## 4. Generic / AI-looking vs authored
- Numbered step cards -> one prose sentence, or a real example output.
- Icon grids -> text rows with hairline dividers.
- Stat rows -> omit, or one honest line.
- Sparkles / wand -> plain verb labels ("Write it", "Tighten").
- Centered everything -> left-aligned, one strong column edge, asymmetric document + tools split.
- Gradient CTA -> one flat solid button, used only for the single primary.
- Cards in cards -> one surface, hairlines, whitespace.
- Pill chips everywhere -> text links or one segmented control.
- Authored detail: real sample text, stated limits ("1 free refine"), specific copy, one accent colour.

## 5. Recommended flow
Header (logo, Templates, Sign in) -> H1 + 1 line -> compose -> result -> 1 pricing line -> 4 FAQ -> compact footer.

Desktop A (compose): ~5 controls (title, location, "Add detail" link, Generate, nav). Below fold: 1 line + 4 FAQ + footer.
```
[Logo]                         Templates  Sign in
Write a job description in a minute
Free. No sign-up.
[ Job title ______________ ] [Location v]
  + Add detail (optional)
[ Generate ]
```
Desktop B (result): summary bar replaces form (Edit, Regenerate); document; tools column; Copy / Download. ~9 controls.
```
Senior nurse - London - Friendly      [Edit] [Regenerate]
+--- document (editable) ---------+  +-- Check   score 82 >
| Title / About / Duties / ...    |  +-- Quick edits >
|                                 |  +-- Refine >
| [Copy] [Download]               |  +-- Screening questions >
+---------------------------------+
Free to generate. Refine costs 1 credit.
FAQ (4)        footer (1 row)
```
Mobile A: stacked, Generate sticky at bottom. ~4 controls.
Mobile B: summary bar -> full-width document -> sticky bar [Copy] [Tools]; Tools opens a bottom sheet with the groups, one open at a time. ~3 visible controls.
Counts: current page 25+ controls, 10+ sections in one state. Target: A = 5 controls; B = 9 controls; marketing = 3 blocks.
Risk [M]: collapsing Check may cut its use; keep the score number visible. Test with a few real recruiters.
