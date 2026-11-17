# Rebuild the site around its paper example

Decision: commit to one direction, **"Paper and ink"**. Warm paper page, near-black ink, one navy accent, Fraunces for headings only, a body-friendly sans for everything else, hairline rules instead of cards. The site already contains this identity in one place: the warm-paper annotated example with the 96/100 score (shot 01). Everything else is a generic "white card + blue pill + soft shadow" SaaS dashboard stacked under it. The best-evidenced gap versus competitors is not fonts. It is (1) the tool is not the hero and Sign In outranks Generate, (2) no type scale or token discipline (36 font sizes, 25 border colours, 10 radii), (3) failing contrast on functional labels (muted grey 3.9:1, Rewrite pills ~2.3:1), and (4) the template pages are identical cards with no real preview. Evidence is uneven: our own audit is **measured** (Playwright, computed styles); competitor research is mostly **fetched text and stylesheet tokens**, with **no computed layout or type sizes** for any competitor. The palette and type picks below are therefore **judgment from convention plus partial evidence**, not proven conversion wins. Fixes are ranked at the end; the top 6 are cheap and carry most of the effect.

Tags used: **[M]** measured on our site, **[V]** verified from fetched page or CSS text, **[Mem]** memory/unverified, **[I]** my inference.

---

## 1. Critique of our site: strong core, generic shell

### What is genuinely good (keep)

- Warm-paper annotated example with underlined flags and a score table [M, shot 01]. Only part with a point of view. It shows value before use.
- Real quality panel: severity tags, concrete fix text, one-click fixes [M, shot 03b]. Substance, not decoration.
- Accordion intake with Required / Recommended / Optional and green answered state [M].
- Honest pricing copy ("Free to write. Pay only to refine.") [M].
- Fraunces H1 + Manrope body is legible and readable at line length [M].

### What reads AI-generated or generic

| Tell | Where | Evidence | Strength |
|---|---|---|---|
| Gradient glowing "J" in H1, breaks kerning ("J ob") | Home hero (01, 11) | [M] screenshot | Strongest tell |
| Letter-spaced blue eyebrow above almost every heading (11 on home), plus a meaningless "GEN AI MODEL \| LINKEDIN" | Everywhere | [M] count | High. Named tell in 2026 design blogs, but those are opinion pieces ([Utsubo](https://www.utsubo.com/blog/built-with-ai-trust-signals-2026), [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells)) |
| Card in card in card: 29 soft bordered cards on home, nested | Whole site | [M] | High |
| 3 identical cards: How it works 01/02/03, 3-tier pricing, 3-col template grid | Home, templates | [M] | High. "Three equal cards" is a named tell (same blogs) |
| Sparkle/star icon on "AI Custom" and "Customize this with AI" | Templates, role | [M] (07, 08) | Medium-high |
| Glass layers: translucent whites, inset highlights (22), cyan glow, graph-paper bg | Whole site | [M] | Medium |
| Marketing copy: "Tested, high-converting", "zero hallucinated facts", "verified LLM prompt pipelines" with no shown evidence | Templates, SEO block | [M] | High for a recruiter audience. Over-claiming costs trust |
| Default-recipe components: white, 1px alpha border, 8-20px radius, soft shadow, blue pill | Everywhere | [M] | Root cause |
| White card on pale-blue page, LinkedIn blue #0a66c2 accent | Whole site | [M], [I] | "Default SaaS" look. Also blurs into LinkedIn's own brand |
| Fraunces + Manrope as a pair | Type | [I]. Typewolf shows Fraunces + DM Mono and Manrope + Eksell Display in use, not this pair ([Typewolf](https://www.typewolf.com/fraunces)) | Weak. Pair itself is not the problem. Settings are (see 3) |

Caution: the "AI tells" lists are low-authority opinion, not studies. Use them as a checklist, not proof. Recruiters will not think "AI-made". They will think "generic, can I trust this". Our own signals (score 96 vs score 69, pay range flag) are the credibility.

### Hard usability and accessibility defects [M]

| Defect | Number | Fix target |
|---|---|---|
| `--muted` #738295 on white | 3.92:1, fails AA. Used on 50 text nodes, including Required/Optional status | #5b6b7e on white computes to **5.46:1** (our audit note said 4.9; recomputed here, conflict is minor, both pass) |
| Rewrite pill, opacity .55, 11.5px, ~18px tall | ~2.3:1 | Full opacity, 32px+ target |
| Answered badge white on #0b8f61 | 4.1:1 | #0f6b5c gives 6.41:1 |
| Text under 12px | 55 elements | Floor 12px |
| Targets under 44px | 43 | 40 px min, 44 on mobile |
| H1 twice on home; H2 alternates serif/sans, 18/22/24/26px | Outline broken | One H1 per page |
| Scroll-inside-scroll draft box | Draft column | Single page scroll |
| Hero CTA hierarchy: Sign In is the loudest button, Generate sits at y~730 | 01 | Tool first |
| Empty 520px draft void | 02 | Ghost sample draft |
| Fixed number rail floats over pricing, SEO, footer | 04-06 | Scope to intake column |
| Mobile: no brand, ~7 screens of accordions before Generate | 11-13 | Sticky Generate bar |

Template pages specifically (screens 07, 08 viewed):

- Index: 9 identical cards, grey meta box, two competing buttons ("View Free Template" grey, "AI Custom" blue). No preview of the actual document inside the card. Header is centred while the home hero is left-aligned (alignment drift).
- Role page: 9 pills of mixed meaning (location, years, salary, skills) all styled the same. Document section headings are blue and fade lighter down the page (probably the reveal animation caught mid-fade, [M] per audit, same in 07). On slow devices that reads as disabled text. Role page already has Copy and Customize, so the "copy-first" gap noted in the references is partly closed. What is missing is the sticky bar and highlighted `[Company Name]` placeholders.

---

## 2. What the better products do that we do not

Ordered by how much evidence backs the claim.

### Layout and UX

- **Free generator tools put the form first.** Workable: H1, one-line promise, Job Title field, optional Industry, optional Tone, Generate; honest loading copy ("It may take up to 10 secs"); upsell kept secondary ([Workable](https://www.workable.com/job-description-generator)) [V, text]. We lead with a 60px title plus a sample, push Generate below the fold, and ask 10 questions. Our intake is richer, which is our edge, but the entry feels heavier. [I] Offer "Job title first, rest optional" as step one.
- **Inline annotation of the text under review is a proven category pattern.** Textio shows tooltip screenshots of flags on text (age-bias flag, examples) ([Textio](https://www.textio.com/)) [V, text]. Our hero example already does the static version. We do not make flags interactive or reuse the pattern inside the product at the same visual quality. [I]
- **Real product fragments, not abstract icons or 3-card grids.** Greenhouse (candidate chips like "Strong Match"), Ashby (labelled product tour), Attio (annotated tables with specific numbers), Linear (real issue view, "Fig 0.1" labels) ([Greenhouse](https://www.greenhouse.com/), [Linear](https://linear.app)) [V, text]. Our "How it works" 01/02/03 cards and template cards are the opposite.
- **Templates: curated looks different from auto-generated.** Notion cards show a preview thumbnail, creator, price, "Handpicked by our editorial team"; Resume.io makes the whole card one link and deep-links "Use this template" into the builder ([Notion](https://www.notion.com/templates), [Resume.io](https://resume.io/resume-templates)) [V, text]. Workable's template index is a link dump with duplicate titles, an auto-generated tell ([Workable index](https://resources.workable.com/job-descriptions)) [V]. With 9 templates we have no need to filter. We need real previews and one-line role-specific copy.
- **Detail-page skeleton:** breadcrumb, H1, updated date and read time, TOC or jump row, fixed section order, FAQ, related roles, disclaimer ([Indeed SWE](https://www.indeed.com/hire/job-description/software-engineer)) [V, text]. Workable's page shows a "Refreshed" date that conflicts with its "2024" title; do not repeat that ([Workable SWE](https://resources.workable.com/software-engineer-job-description)) [V].

### Fonts and type

- **Serif display plus a restrained sans body is the norm among the better-looking HR tools**: Ashby (Signifier + TT Norms), Greenhouse (Untitled Serif + Sans), Pinpoint (GT Sectra Fine + Walsheim), Gem (Society Book), Textio (Iskra), Workable (Source Serif accents) [V, from stylesheets]. So our serif choice is on-trend for the category, not a mistake. That is good news.
- **Published, small type scales.** Vercel's Geist publishes heading sizes 72/64/56/48/40/32/24/20/16/14, body 14 default, 13 secondary ([Geist](https://vercel.com/geist/typography)) [V]. GOV.UK uses 19px body, one lead paragraph per page ([GOV.UK](https://design-system.service.gov.uk/styles/paragraphs)) [V]. Smashing: 60-70 characters per line ([Smashing](https://www.smashingmagazine.com/2020/07/css-techniques-legibility/)) [V]. We have 36 sizes and 55 elements under 12px.
- **Fraunces settings matter.** Default Fraunces has WONK on (quirky n/m/h) when opsz is above 18, and the maintainers call wonky forms "less desirable for continuous reading" ([Fraunces repo](https://github.com/undercasetype/Fraunces)) [V]. Whether our CSS serves WONK, SOFT and opsz axes was not checked [gap]. Also Typewolf lists Fraunces as body-friendly but not Manrope ([Typewolf Google Fonts](https://www.typewolf.com/google-fonts)) [V as a list; weak evidence, since a missing mark is not a verdict].
- **A tool-like signal is mono for numbers and metadata** (Vercel, Speakeasy, Flask & Field use serif or sans plus mono) [V]. We already have accidental mono in quality chips (9 nodes). Make it deliberate or remove it.

### Colour

- **Warm neutral base plus one hot or deep accent is how the non-generic HR tools look.** Pinpoint ivory #f7f3e7 + ink #1f2729 + accent #ff492c; Teamtailor cream #f4f3f0; LinkedIn's own offset background #f4f2ee; Greenhouse ink #15372c + green #008561 [V, stylesheet frequency, not proven hero use]. Cool slate/teal Tailwind defaults look templated (Lever's CSS matches Tailwind values) [V, [I] for the judgment].
- Our home already uses warm paper #f6f2ea in the hero. The cold blue page contradicts it.

### Trust cues

- Named reviewers, last-updated dates, sourced data, an editorial policy (Indeed, Workable) [V]. We cannot honestly claim reviewers. We can claim **"drafted by AI, edited by a person, last reviewed <date>"** and show the rule count of the free linter [I]. Real numbers from our own checker beat "trusted by".

---

## 3. Decision: "Paper and ink", editorial tool

### Why this one (and not the alternatives)

| Option | Verdict | Reason |
|---|---|---|
| A. Paper and ink (editorial, warm) | **Chosen** | Builds on the one distinctive asset we own. Matches how Pinpoint/Greenhouse/Ashby escape SaaS defaults [V]. Product is text under review, so a "document" look is native. Low rewrite risk: most tokens exist already. |
| B. Dense app UI (Linear-like) | Rejected | Linear's app density (13px body) does not transfer; source itself says app UI, not first touch [V]. Recruiters read long text. |
| C. Friendly pastel/pill (Teamtailor, Recruitee) | Rejected | Needs photography and brand work we do not have. 32px pills are a generic tell. |
| D. Keep cool blue, just clean up | Fallback | Cheapest, but keeps the "default SaaS + LinkedIn blue" look and the two-design split. |

Honest limit: no study shows warm vs cool neutral changes trust or conversion [gap, editorial notes]. This is design convention plus category practice, not proof.

Tone of copy: plain, specific, short. Say what the checker does ("flags 'rockstar', missing pay range, age-coded wording") instead of "AI-powered, high-converting". Sentence case. No sparkle, no "zero hallucinations". Recruiter words: posting, intake call, pay range.

### Type system

Families (3, all intentional):

| Role | Font | Notes |
|---|---|---|
| Headings, doc title | **Fraunces** wght 500, opsz auto, **WONK 0, SOFT 0**, tracking -0.015em at 28px+ | Keeps brand, removes quirk. If axes cannot be set from the Google CSS, keep weight 500 and accept the quirk [I]. |
| UI and body | **IBM Plex Sans** (swap for Manrope) | Typewolf body-friendly list [V]; neutral, avoids the "geometric-friendly + soft serif = startup" feel [I]. Medium confidence. If you want zero churn, keep Manrope; the scale fix matters more than the swap. |
| Metadata, flags, counts | **IBM Plex Mono** 12px, tabular figures | Only for chips, scores, char counts. Replaces the accidental monospace. |

Scale (8 steps, replaces 36). Desktop / mobile:

| Token | px desktop / mobile | Line height | Family, weight | Use |
|---|---|---|---|---|
| display | 52 / 36 | 1.08 | Fraunces 500 | Home H1 only |
| h1 | 40 / 30 | 1.12 | Fraunces 500 | Template pages, auth |
| h2 | 28 / 24 | 1.2 | Fraunces 500 | Section titles, one style everywhere |
| h3 | 20 / 20 | 1.3 | Plex Sans 600 | Panel titles, card titles |
| doc | 17 / 17 | 1.6 | Plex Sans 400, max 66ch | Generated JD and template body |
| ui | 15 / 15 | 1.5 | Plex Sans 400/500 | Forms, buttons, helper text |
| label | 13 / 13 | 1.4 | Plex Sans 500 | Field labels, meta |
| tag | 12 / 12 | 1.3 | Plex Mono 500, +0.04em | Chips, status, counts. Floor of the system |

Weights: 400, 500, 600 only (drop 450, 700, 800). Eyebrows: keep at most 2 sitewide, in the `tag` style, and only where they carry information (e.g. "Example", "Quality check").

### Palette with contrast (computed, WCAG 2.x)

| Token | Hex | Use | Ratio |
|---|---|---|---|
| paper | #faf7f0 | Page bg | base |
| sheet | #fffdf8 | Document, modals, inputs | base |
| ink | #1b1a17 | Headings, body | 16.26:1 on paper |
| ink-2 | #4a4740 | Secondary text | 8.66:1 on paper |
| muted | #6b665c | Helper, Required/Optional | 5.33:1 on paper, 5.61:1 on sheet. Do not go lighter |
| accent | #1f3a5f (navy) | Primary button bg, links, focus ring | 10.73:1 on paper; white on accent 11.48:1 |
| accent-hover | #172c49 | Hover | white on it 14.07:1 |
| flag (rust) | #b4411f | Annotation underline, error text | 5.28:1 on paper |
| pass (green) | #0f6b5c | Pass, answered state; white on it 6.41:1 | 5.99:1 on paper |
| warn text on tint | #7a4b00 on #fff1cf | Warning badge | 6.61:1 (existing) |
| field border | #857f72 | Input and button outlines (non-text 3:1) | 3.92:1 on sheet |
| hairline | #e4ddcc | Section rules, decoration only | 1.27:1 (ok for decoration, never for inputs) |

Why navy accent, not green or the current LinkedIn blue: green is crowded in HR (Workable, Greenhouse, Lever teal [V]); #0a66c2 is LinkedIn's brand colour and blurs identity for a tool that outputs to LinkedIn [V, hex from LinkedIn CSS]; navy keeps continuity with the current blue brand and passes on paper. Rule: accent only on actions and links. One annotation colour (rust), one success colour (green). No gradients, no glow, no translucent layers. Dark mode: not scoped here.

### Layout system

- One container, **1200px max**, 12 columns, 24px gutter, 24px page margin (16px mobile). Today 4 different widths (1290, 960, 920, 1230) [M].
- Spacing on a 4/8 scale: 4, 8, 12, 16, 24, 32, 48, 64, 96. Section gap 64-96. No 10, 11, 14, 28.8.
- Left-aligned everywhere (nav, hero, template header). Logo aligns with the container edge, not 24px from the window [M finding 20].
- Home order: hero (copy + one primary CTA left, annotated paper example right) -> workspace -> how it works as 3 short rows with rules, not cards -> pricing -> FAQ -> footer.
- Workspace: intake left (5 cols), document right (7 cols, sticky, single page scroll), quality panel directly under the document as a "margin note" block. Number rail lives inside the intake column, sticky there only. Mobile: one column, sticky bottom Generate bar.
- Template index: 3x3 grid, document thumbnails. Role page: document at ~66ch centred in cols 3-10 with a sticky action bar.

### Component rules

| Component | Rule |
|---|---|
| Surfaces | Page = paper. Only 2 elevated objects: the document sheet and modals. Everything else is a hairline-ruled row, not a card. Max nesting depth 1. |
| Radius | 6 (controls, chips), 12 (sheet, modal), 999 (status tags only). Three values. |
| Shadow | One: `0 1px 2px` + `0 8px 24px` at ink 6%. Sheet and modal only. |
| Primary button | Navy fill, white text, 44px tall, 6 radius. One per view. Generate is primary on home; Sign In becomes a text link. |
| Secondary | Navy 1px outline, same height. Tertiary: underlined text link. No grey filled buttons. |
| Chips and pills | Two types only: action chips (outlined, 32px+) and info tags (mono 12px, no border, tinted bg). Rewrite pill becomes an action chip at full opacity. |
| Flags | Underline in rust or pass-green on the text, tag in mono, hover shows the reason. Same visual in hero and product. |
| Inputs | 1px #857f72 border, sheet fill, 44px single line; Company name becomes a single-line input, not a 4-row textarea. Focus ring 2px navy + 2px offset. |
| Motion | Opacity and 8px translate on section reveal only, 150-200ms. Respect `prefers-reduced-motion`. Remove title/eyebrow/rail stagger. Cards must never sit half-faded for the user. |
| Icons | Plain line icons. No sparkle for "AI". |
| Copy | No eyebrow unless it says something. No unproven superlatives. |

Evidence on these specifics: scale, radius, shadow and sizes are **my inference** from convention and Geist/GOV.UK/Smashing values. No competitor's computed sizes were measured.

---

## 4. Reference board

Ranked by usefulness to us. "Evidence" = how much of the claim is verified.

| # | Reference | Study exactly | Do NOT copy | Evidence |
|---|---|---|---|---|
| 1 | [Textio](https://www.textio.com/) | Inline highlight plus tooltip on text, Iskra-style serif + grotesk pairing, hard numeric stat blocks, punchy copy | Demo-led CTAs, enterprise stats, magenta/orange ribbon gradients | [V] text and CSS font names; no computed styles |
| 2 | [Workable JD generator](https://www.workable.com/job-description-generator) | Title-first form, optional fields labelled "optional", tone select, honest loading and error copy, secondary next steps | Its generic green SaaS look, 1000+ link-dump index | [V] text and CSS tokens (#00756a, 8px radius) |
| 3 | [Pinpoint](https://pinpointhq.com/) | Warm ivory + one hot accent + serif display; 8/16px radii | The orange-red itself, carousel | [V] CSS tokens; hero usage not verified |
| 4 | [Linear](https://linear.app) and [redesign post](https://linear.app/now/how-we-redesigned-the-linear-ui) | Restraint: grey ramp plus one accent, hairlines, "reduce visual noise, maintain visual alignment", numbered "Fig" labels, real UI frames | Dark canvas, 13px density, keyboard-first, third-party hex values (not official) | [V] text; hex tokens secondary only |
| 5 | [Indeed Hire SWE page](https://www.indeed.com/hire/job-description/software-engineer) | Section order, jump list, last-updated, labelled sample fields, FAQ, related roles, disclaimer | Promo banner above the article, repeated "Create" CTAs | [V] text only; no visuals |
| 6 | [Notion templates](https://www.notion.com/templates) | Card with real preview, counts, "handpicked" editorial label, different density per section | Marketplace scale, creator/price fields | [V] text only |
| 7 | [Greenhouse](https://www.greenhouse.com/) | Serif + dark ink + status chips ("Strong Match") reused as quality chips; 12px radius token system | Botanical art, logo walls, SOC/G2 claims | [V] CSS tokens |
| 8 | [Vercel Geist typography](https://vercel.com/geist/typography) | Small published scale, Strong/Subtle modifiers, mono beside sans, tabular figures | Black/white Swiss minimalism, heroes at 72px | [V] text |
| 9 | [Resume.io templates](https://resume.io/resume-templates) | Whole card = one link, "Use this template" deep-link pre-filled into builder | Repeating the same card in many sections, padded SEO text, duplicated FAQs | [V] text |
| 10 | [GOV.UK paragraphs](https://design-system.service.gov.uk/styles/paragraphs) + [Smashing](https://www.smashingmagazine.com/2020/07/css-techniques-legibility/) | 17-19px body, one lead paragraph, 60-70 ch measure, taller line height | Government visual style | [V] text |
| Hon. | [Ashby](https://www.ashbyhq.com/) | Single-CTA hero, serif on a SaaS product | Lilac palette, "Get in touch" CTA | [V] text and CSS |
| Hon. | [Teamtailor](https://www.teamtailor.com/en/) | Light-weight large display type scale tokens (3.75rem, 1.05 line height) | Pink + lime, device mockups, photography | [V] CSS tokens |
| Hon. | [Attio](https://attio.com) | Annotated realistic screens, fragment copy, big-numeral stats | Agent panels, dark app density | [V] text |

Not covered: Betterteam and Indeed Employer (HTTP 403, so anything said about them is memory), Canva, Figma Community, Zety (blocked), Pitch, Loom, Arc type. Typewolf Site of the Day examples (Every: Signifier + Switzer; Speakeasy: Tobias + Diatype + Diatype Mono) back the "serif plus neutral sans, optional mono" pattern but are licensed fonts ([Typewolf SOTD](https://www.typewolf.com/site-of-the-day)) [V].

---

## 5. Ranked fixes

Impact and effort: H/M/L. Ranked by impact first, then cheapness. "Page" H = home, T = templates, A = both.

| Rank | Fix | Page | Impact | Effort | Why |
|---|---|---|---|---|---|
| 1 | Raise muted to #5b6b7e (or #6b665c on paper); Rewrite pills to full opacity; 12px type floor | A | H | L | Functional labels fail contrast now [M]. A few token edits |
| 2 | Make the tool the hero: primary "Start writing" next to H1; Sign In becomes text link; ghost sample draft in the empty panel | H | H | L-M | Biggest hierarchy fault [M 01, 02] |
| 3 | Delete gradient "J", most eyebrows (keep 2), sparkle icons | A | H | L | Cheapest removal of the loudest AI tells |
| 4 | Collapse tokens: 8 type sizes, 3 radii, 1 shadow, 4/8 spacing, 1 container; one H1, one H2 style | A | H | M | Fixes the "two designs stacked" feeling |
| 5 | Template cards: real document thumbnail (first lines, faded), role-specific one-line "best for", whole card is the link, one action; drop grey "View Free Template" + "AI Custom" pair | T | H | M | Biggest evidence-backed gap vs Notion/Resume.io [V] |
| 6 | Remove over-claims ("Tested, high-converting", "zero hallucinated facts", "verified LLM prompt pipelines"); replace with what the checker really does and a "drafted by AI, edited by a person, last reviewed <date>" line | A | H | L | Trust for recruiters; copy-only |
| 7 | Adopt paper identity site-wide: paper bg, sheet for document and quality panel, hairlines instead of cards, navy accent | A | H | M-H | The direction itself. Do after 1-4 so it lands on clean tokens |
| 8 | Single-scroll workspace: remove the inner draft scrollbox, sticky document column, number rail scoped to intake | H | M-H | M | Fixes scroll-in-scroll and rail clutter [M] |
| 9 | Role page: sticky action bar (Copy primary-secondary, Download, Customize prefilled with role), highlight `[Company Name]` placeholders, ink headings (no fading blue), split meta pills from skill tags | T | M-H | M | Copy exists; sticky bar and placeholder highlight are the open gap [I] |
| 10 | Mobile: brand mark in nav, short sample, sticky bottom Generate, Expand as full-row tap target | H | M-H | M | ~7 screens before Generate [M] |
| 11 | Fraunces axes: WONK 0, SOFT 0, weight 500; swap Manrope for Plex Sans; planned Plex Mono for tags | A | M | L-M | Real but modest; judgment-based [I] |
| 12 | Pricing and How-it-works as ruled rows, not 3 equal cards; larger price numerals | H | M | M | Template tell, lower priority than copy and layout |
| 13 | Role page extras: related roles, FAQ with FAQPage and BreadcrumbList JSON-LD, last-reviewed date | T | M | M | Matches Indeed/Workable structure [V]; check if schema already exists first [gap] |
| 14 | Single-line Company name input; Name/pay placeholders look like placeholders | H | M | L | Small, visible polish |
| 15 | Motion: cut 17 keyframes to reveal-only; fix half-faded cards; honour reduced motion | A | M | L-M | Fading cards read as disabled |
| 16 | Billing modal empty state; ensure one modal at a time; fix footer (1-link Resources column) | H | M | L | Credibility bug; unverified when signed in [gap] |
| 17 | Align template header left; align logo to container | T | L | L | Polish |

Suggested order: 1, 3, 6, 2 (one day) -> 4, 5 -> 7, 8, 9, 10 -> the rest.

---

## 6. Evidence quality and conflicts

| Claim group | Level | Note |
|---|---|---|
| Our site metrics, contrast, counts | Measured (Playwright, computed styles, local copy) | Strongest. Mock draft text ("Own roadmap item number 1...") means copy was not judged |
| Our screenshots 01, 03, 07, 08 | Viewed here | Consistent with the audit. Not viewed: 13b, 14, 15, 07b, 08b |
| Competitor fonts and hex | Fetched stylesheet text | Hex frequency is not proof of hero use. No competitor computed sizes, widths, or motion |
| Competitor layout and copy | Fetched page text, no visuals | Layout "feel" is inference |
| Betterteam, Indeed Employer, Canva, Zety, Figma | Blocked | Memory only; excluded from the board |
| "AI tell" lists, trend pieces | Vendor and agency blogs | Opinion, consistent with each other, no studies |
| Warm vs cool neutral and trust | No evidence found | Convention only |
| Target type scale, palette, component rules | My inference | Contrast ratios are computed here; the choices are not tested with users |

Conflicts and open points:

- **Fraunces default opsz:** repo README says 144, an older Android mirror says 36. Check the font file we serve.
- **Muted fix:** our audit says #5b6b7e is 4.9:1 on white; recomputed here as 5.46:1. Both pass; use the computed value.
- **Notion serif:** Lyon in some teardowns, Noto Serif in one. Unsettled; do not cite as fact. Notion brand sans as "Inter cut" comes from a search summary; its own page loaded empty.
- **Linear hex values** (#5E6AD2 etc.) come from a third-party article about app UI, not official.
- **Typewolf "not body-friendly" for Manrope** is an absence of a mark, not a statement. Weak support for the swap.
- **Workable date mismatch** (Refreshed Feb 2022, "2024" title) is a verified counter-example, not a style to follow.
- **Role page "copy-first gap":** the references say competitors lack a copy button; our page already has Copy. Remaining gap is a sticky bar.
- **Unchecked on our side:** focus rings, keyboard order, reduced-motion behaviour, signed-in billing modal, existing JSON-LD, whether Fraunces serves the WONK/SOFT axes.

---

## Conclusion

The site does not need a redesign. It needs to stop designing against its best idea. The paper example with underlined flags already says "this tool checks real hiring problems", and the ruled-row, mono-tag, serif-headline language that goes with it is both cheaper to build and harder to mistake for a template than another card system. The change that matters most for recruiters is not aesthetic: put Generate where the eye lands, make labels readable, and replace superlatives with what the linter actually catches.

The honest limit is that none of this was tested against users or measured on competitor pages. Treat the type scale and palette as a defensible first pass. Next step with the highest information value: pull computed styles for Textio, Workable, Pinpoint and Linear with Playwright, and run 5 recruiters through "title to copied post" on the current and rebuilt home page.
