# Our site visual design audit (live, local copy)

Method: Playwright on http://audit.localhost:8765/ (same server; the 127.0.0.1 and localhost hosts had a stuck browser zoom of 33% and 75%, so a fresh *.localhost host was used to get true 1440 and 390 CSS px). Metrics measured on home at 1440 after generating a draft (524 visible elements). Shots in `research_notes/Website design audit and references/shots/`. Draft text is mock output ("Own roadmap item number 1..9"), so judge layout, not copy.

## 1. Overall verdict

Competent, clean, coherent blue/white product UI with one genuinely distinctive idea (the warm-paper annotated example + score panel). But the page is two designs stacked: an editorial serif/paper top and a generic "SaaS blue card dashboard" everywhere else. Too many tiny sizes, too many near-identical soft cards, low-contrast helper text, and a heavy left rail. Score: structure 7/10, typography 6/10, originality 5/10, accessibility 5/10, mobile 6/10.

## 2. Measured facts (home, desktop 1440)

- Font families: 3 (Manrope on 271 text nodes, Fraunces on 17, monospace on 9 - the code chips in quality panel). Matches the brief; monospace is the unplanned third.
- Distinct font-size values: 36 (12px x58, 14px x26, 13px x21, 11px x20, 16px x19, 12.8, 13.5, 10.88, 15, 15.68, 10.5, 13.44, 13.76, 12.16 ...). Several are 0.1 to 0.5px apart (13 / 13.12 / 13.44 / 13.5 / 13.76 / 14 / 14.08 / 14.5). No type scale. 55 text elements are under 12px (min 8.5px, 10.24, 10.5, 10.88, 11).
- Font weights: 6 (400, 450, 500, 600, 700, 800). 450 is a variable-font oddity used 5 times.
- Heading hierarchy: H1 appears TWICE on home (hero "Job Description Generator" 60px Fraunces and the draft title "Senior Product Manager" 34px Fraunces). H2 sizes: 24 Manrope (panel titles), 18 Manrope bold (draft sections), 26 Fraunces (pricing, SEO), 22 Fraunces (FAQ, templates). So H2 alternates between serif and sans and between 18/22/24/26. Hero H3 is serif 23px.
- Text colours: 19 distinct (main: #33475f x55, #738295 muted x50, #102033 x49, #0a66c2 x44, #073f7a x27, white x11, teal #0f6b5c x11, warm #1b1a17 x9, warm muted #6e6a60 x7, green #087852, amber #7a4b00 ...).
- Background colours: 22 distinct, many translucent whites (rgba 255 at .92 / .86 / .85 / .82 / .76). Real surfaces: white, #f8fcff, #e8fbff (cyan soft), warm paper #f6f2ea, amber #fff1cf/#fff8e8/#ffe3a3, green #0b8f61.
- Border colours: 25 distinct, mostly alpha blues/slates (rgba(19,54,89,.13) x32, rgba(10,102,194,.18/.2/.34/.17/.12), #d0d7de, cyan .5).
- Border radii: 10 values (6px x41, 8px x36, 999px x16, 4px x14, 7px x12, 20px x9, 10px x7, 12px x4, 3px x3, 50%). 6 vs 7 vs 8 vs 10 vs 12 coexist.
- Box shadows: 20 distinct; recurring: inset white highlight x22 (glass bevel), 0 8px 24px a.055 x9, 0 1px 3px x9, 0 10px 26px a.07 x5, cyan glow ring + 0 8px 18px cyan x4, green glow 0 8px 16px x4. Root tokens also define panel 0 24px 70px and active 0 24px 62px blue glow.
- Gradients on 34 elements; backdrop-filter/filter on 4 (nav, modals, rail); glass: translucent white panels + blurred modal backdrop; glow: cyan/green/blue shadows on active question card, number badges, rail.
- Animation: 36 elements with a CSS animation, 17 keyframes (modalEntry, eyebrowIn, titleIn, authorsPanelIn, authorCardIn, surfaceIn, controlIn, cardIn, railFloatIn, viewIn, blockIn, caretBlink, shimmer, changedFlash, backdropIn, proofFixIn, doc-spin); 129 elements with transitions. scroll-behavior smooth.
- Spacing: flex/grid gaps 21 distinct values (10px x25, 8 x18, 4 x15, 14 x12, 11 x11, 12 x9, 6, 16, 24, 2, 20, 28, 28.8, 32, 3, 5, 18 ...). Not a 4/8 grid (10, 11, 14, 28.8 are off-grid). 22 distinct padding-top values.
- Container widths (element widths 600-1440): 1290 x13 (home grid), 960 x16 (SEO inner), 920 (templates / role / 1024 grid), 617, 680, 698, 725, 922. At least 4 different max widths between sections (1290 workspace, 960 SEO, ~1230 template grid, 920 role page).
- Button styles: 19 distinct computed style combos, 15 class families. Visual types: solid blue primary (Generate, Sign In, Refine, AI Custom), dark navy solid (Close), outlined pill chips (quick edits, rewrite, fixes), blue-outline 8px small (Expand / Upload), cyan-outline small, white ghost 6px (Clear answers), text link buttons, segmented controls (tone/length/EEO), grey "View Free Template", number rail buttons. Radii on buttons: 0, 4, 6, 8, 999.
- Card-like surfaces on home: 29 (bordered + filled + rounded, >60px tall). Plus 3 pricing, 3 how-it-works, 10 intake rows, pay card, quality panel, draft preview, refine box, FAQ x4, example card, outer paper panel.
- Tap targets: 43 button-like elements below 44px in height or width (Expand 32px high at 11px text, rewrite pill 18px high at 11.5px / 0.55 opacity, segment buttons, rail 30px, Close).
- Tiny text: 55 elements under 12px.
- Overflow: no horizontal scroll at 390 or 1024.
- CSS tokens exist (:root --canvas, --ink, --blue, --cyan, ...), but values are not consistently used (22 bgs, 25 borders, 19 text colours).

## 3. Contrast (WCAG 2.x, computed from tokens)

| Pair | Ratio | Verdict |
|---|---|---|
| ink #102033 on canvas #f6fbff | 15.8 | pass AAA |
| ink-soft #33475f on white | 9.51 | pass AAA |
| blue-deep #073f7a on white | 10.49 | pass AAA |
| link blue #0a66c2 on white | 5.69 | pass AA |
| white on #0a66c2 (primary btn) | 5.69 | pass AA |
| teal #0f6b5c on paper #fffdf8 | 6.3 | pass AA |
| amber #7a4b00 on #fff1cf (WARNING badge) | 6.61 | pass AA |
| danger #b3261e on white | 6.54 | pass AA |
| warm muted #6e6a60 on #f5f0e8 | 4.75 | pass AA (barely) |
| muted #738295 on white (--muted, 50 text nodes: "Required", "Optional", helper text, "Answer before generating") | 3.92 | FAIL AA for normal text |
| muted on canvas #f6fbff | 3.76 | FAIL |
| muted on cyan-soft #e8fbff | 3.67 | FAIL |
| white on green #0b8f61 (answered number badge) | 4.1 | FAIL AA for small text (badge is bold ~13px) |
| textarea placeholder #9aa7b5 on white | about 2.5 | FAIL (placeholder, not essential but "Type your answer." and refine example are the only hint) |
| Rewrite pill: #0a66c2 at opacity .55 on white, 11.5px | about 2.3 | FAIL, and it is a primary per-section action |
| Disabled-looking template cards below fold (faded in reveal at screenshot time) | transient | reveal fade is timing, see 4 |

## 4. What is good (keep)

- Warm-paper annotated example with underlined flags + score table (shots 01, 11). Only part with a point of view; shows the product's value before use. Keep and extend the paper idea.
- Fraunces for H1 and Manrope body: legible, well paired, readable line lengths.
- Real quality panel: severity tags (WARNING/INFO), concrete fix text, offending phrases as code chips, one-click fixes (shot 03b). Substance, not decoration.
- Accordion intake with number rail and Required / Recommended / Optional labels, green answered state (03). Clear progress.
- Honest pricing copy (shot 04): "Free to write. Pay only to refine." Middle card highlighted. Failed-refine refund stated.
- Ink/blue text contrast on primary content is strong; no horizontal overflow on mobile; breadcrumb, chips and CTA hierarchy on role page are clear (08).
- Modals are simple and consistent in tone (09).

## 5. Findings ranked by severity

### Severity A (hurts credibility or usability)

1. Muted grey text fails contrast everywhere (3.9 : 1). Where: "Required/Optional/Recommended", "Answer before generating", helper lines, footer copyright, pricing "= 20 refines" (02, 03, 04, 06). Why it matters: the intake status labels are functional, not decorative.
2. Rewrite pills almost invisible (opacity .55, 11.5px, ~18px high) (03). Primary editing affordance reads as disabled. Fails contrast and tap size.
3. Hero is wasted on desktop and the CTA is wrong (01). The first 900px show title + sign-in + sample + a TONE/LENGTH/EEO bar; the actual start action sits below the fold at y~730. "Sign In" (solid blue, top right, far from the title) is the most prominent button although signup is "not needed". Hierarchy: Sign In looks like the primary CTA, "Generate" is lower and equal weight.
4. Empty draft panel is a huge blank 520px box with centred grey text (02). First-time user sees a big void next to the form; no preview of what comes, no steps hint. Good place for a ghost/sample draft.
5. Page length / density: 5,107px home on desktop; 10,403px on mobile. Intake (10 accordions + pay card) is a 1,680px tall left column against a draft column that grows differently; the two columns are decoupled, so the left stays long while the right scrolls inside a fixed-height inner scroll box (03: inner scrollbar inside the draft preview, a scroll-inside-scroll). Quality panel and quick edits sit below the fold of the draft.
6. Tap targets and tiny type: 43 controls under 44px; 55 text elements under 12px (8.5 to 11.5px). Expand (32px, 11px text) and Rewrite are the main actions. On mobile (12) Expand buttons are 32px high and stack under each title, leaving 250px tall rows with dead space.
7. Fixed number rail (left, 64px wide, 10 buttons) floats over every section including pricing, SEO, FAQ and footer (04, 05, 06). It has no meaning there (it navigates the questions only), it overlaps nothing at 1440 but crowds the 126px left gutter, and at narrower widths would collide. Looks heavy: cyan glow, glass, 10 equal chips. Hidden on mobile (fine).
8. Mobile has no logo/brand (11): nav only. Sign In is a 150px button floating alone under the sub-copy. The sample excerpt takes a full screen (about 1,700 device px) before any input. Section order on mobile forces ~7 screens of accordion before Generate; Generate is placed after all questions at the top of the draft panel, so the user must scroll up and down (13: "Loaded your earlier result instantly" banner reveals cached output, good, but the layout shift when it appears pushes content ~90px).
9. Billing modal (10): when forced open it renders a short white card with only a heading and one-line copy and an empty gap (no pack buttons visible, probably loaded only when signed in). Empty state looks broken. Also the modal stacked on the open auth modal in my forced test, so check that only one modal can be open at once.

### Severity B (reads template-like / inconsistent)

10. Gradient-letter "J" in the H1 (01, 11). First letter has a glowing blue-cyan 3D gradient and a halo; it looks like a rendering bug or a dropped effect, not a drop cap, and it breaks kerning ("Job" reads as "J ob"). Strong "AI-generated flourish" signal. Source: `<span class="gradient-letter">J</span>`.
11. Eyebrow labels everywhere (GEN AI MODEL | LINKEDIN, INTAKE, DRAFT, QUICK EDITS - FREE, NO ACCOUNT, FREE ACCOUNT, NEED MORE?, AI WRITING GUIDE, FREQUENTLY ASKED QUESTIONS, FREE HIRING RESOURCES, FREE RESOURCE LIBRARY): tiny blue letter-spaced caps above nearly every heading. This is the single most recognisable LLM-landing-page tic. 11 instances on home. "GEN AI MODEL | LINKEDIN" in the hero is also meaningless to a recruiter.
12. Everything is a white rounded bordered soft-shadow card (29 on home, nested: panel card > question card > textarea; SEO section is a card containing 3 cards containing FAQ cards). Hierarchy flattens; cards inside cards inside cards (05).
13. Numbered 01 / 02 / 03 "How it works" cards in serif blue numerals (05) plus numbered rail 01-10 plus numbered intake 01-10: numbering overused; the three-step cards are the textbook template component, with generic copy ("zero hallucinated facts", "No blank-page syndrome").
14. SEO block copy is generic and over-claiming ("verified LLM prompt pipelines", "hallucination-free drafts", "Real-Time AI Generation") (05). Reads as keyword stuffing; sits inside the product page between pricing and footer in a card with heavy H2 ("How Our LinkedIn Job Description Generator & JD Writer Works", wrapping to 2 lines with an orphaned "Writer Works"). The ampersand in Fraunces is decorative and distracting.
15. Three-column pricing with the middle card highlighted (04): standard SaaS template. Prices are small ("$5 = 20 refines" is understated), bullets default-styled, cards equal height with blank bottoms, heading "Free to write..." is small relative to the cards. Pricing strip is also detached from the generator it prices.
16. Template library (07): 3-col identical card grid, each with eyebrow category, title, blurb, grey meta box with icons, and two buttons ("View Free Template" grey, "AI Custom" blue with star icon). Star/sparkle icon on "AI Custom" and "Customize this with AI (Free)" (08) are the generic AI marker. Role cards are all the same salary/years pattern. Role page (08) has 9 pill chips of mixed meaning (location, experience, salary, skills) all styled identically.
17. Draft "Rewrite" pills, quick-edit chips, "Fix:" chips, segmented controls and nav all use pills/outlines in the same blue: 5 different pill/chip styles that look alike but differ in radius (4, 6, 8, 999), size and weight, so affordances are blurry.
18. Quality panel mixes 3 languages: sans body, monospace chips (third font), and coloured tag badges (amber WARNING, pale-blue INFO, red ERROR in top hero). Small (11px) and dense: 8 items with 2 lines each in 13px (03b). Score badge (amber circle, 69) is small relative to its importance; the hero score (96, serif red) is far more striking, so the app's own score looks weaker than the marketing one.
19. Two accent systems: blue/cyan (app) and warm paper + teal/green/amber underlines (hero). They do not meet; paper card ends, page goes back to cold blue. Subtle graph-paper grid background and cyan glow are low-key but add to the "default SaaS" feel.
20. Hero H1 is 60px but the page's body width is 1290px with the title and sub-copy left-aligned at x=126 while nav is centred and logo left at x=24: three different alignments in the first 100px (01). Logo (24px from edge) does not align with content (126px). Nav links centred, sign-in at far right 1395 under the content edge.
21. H1 used twice on home (hero and draft title) and H2 serif/sans mix: weak document outline, inconsistent heading hierarchy (SEO, accessibility).
22. Native details/summary FAQ marker triangles (05) next to Manrope questions: unstyled default; first FAQ open by default but looks like a card, others look like input boxes.

### Severity C (polish)

23. 36 font sizes, 10 radii, 20 shadows, 21 gaps: token drift. Pick 6 sizes, 4 radii, 3 shadows.
24. Footer (06): 3 columns but Resources has a single link ("Documentation"), Product has 5; empty right area and 80px of bottom padding. Footer brand mark is plain blue serif text with no logo.
25. Motion: 17 keyframes and 36 animated elements on load (title/eyebrow/surface/card/control stagger, railFloatIn, proofFixIn). Cumulatively heavy; scroll reveal leaves cards half-faded in screenshots (07, 08 show below-fold cards at partial opacity). Need prefers-reduced-motion check.
26. Hero "Replay" link (underlined, grey 11px) and "Try it on your own role" link are the only entry points from the sample into the tool and are very quiet.
27. Intake: first question opens with a huge 4-row textarea for "Company Name" (02): single-line data in a large box. Number badge turns dark green on answered but the rail does not show the same state strongly.
28. The grey template cards below the fold appear dimmed at screenshot time (07), implying disabled; due to reveal animation but will look the same on slow devices or when users scroll fast.
29. Pay range card: placeholders 90000/120000 look like real values (grey but readable); long selects with default chevrons (03b).
30. Layout shifts: "Loaded your earlier result instantly (same answers)" banner and the "What changed" bar insert above the draft and push content; draft scroll box height changes between empty (520px) and filled.

## 6. Elements that read "AI-generated / template-like" (evidence summary)

- Gradient-letter J + halo (01, 11): strongest tell.
- Letter-spaced blue eyebrows on every section (01-08).
- 01/02/03 serif-numeral feature cards and generic three-column pricing (04, 05).
- Card-in-card-in-card soft shadows, inset white highlight (22 elements), translucent white layers (rgba .76-.92), cyan glow shadows, graph-paper background (01, 02).
- Sparkle/star "AI" icon on buttons (07, 08).
- Marketing phrasing: "high-converting", "zero hallucinated facts", "verified LLM prompt pipelines", "Tested, high-converting templates" (05, 07, 08). No evidence is shown for "Tested".
- Identical template cards with the same stats row (07).
- Why they read generic: no brand mark beyond text, no real photography/illustration/data, one blue family everywhere, every component styled from the same recipe (white, 1px alpha border, 8-20px radius, soft shadow, blue pill).

## 7. Recommended direction (short)

1. Kill the gradient J; drop most eyebrows (keep 2-3); remove the sparkle icon.
2. Make the paper/editorial language the identity: apply the warm paper surface and serif headings to the draft preview and quality panel; make the rest quieter (flat white, one border, fewer shadows).
3. Move the primary action up: put "Start / Generate" in the hero, demote Sign In to a text link.
4. Raise --muted to at least #5b6b7e (4.9:1 on white), raise Rewrite opacity to 1, minimum text 12px, minimum controls 40-44px.
5. Collapse tokens: 6 font sizes, 4 radii, 3 shadows, 4/8 spacing, 1 container width per page type.
6. Scope the number rail to the intake column only; make it sticky within it.
7. Replace the empty draft void with a ghost sample or step hints; resolve scroll-inside-scroll.
8. Mobile: add brand, shorten sample, make Generate sticky bottom bar, put Expand as the full row tap target.
9. Fix H1 duplication; unify H2 style.
10. Fix billing modal empty state and ensure single modal.

## 8. Shot index

- 01_home_top_1440.png: hero, sample, bar (findings 3, 10, 11, 19, 20)
- 02_home_intake_1440.png: intake + empty draft (4, 6, 27)
- 03_home_draft_1440.png / 03b_home_draft_lower_1440.png: generated draft, quality panel, quick edits, refine, pay card (2, 5, 18, 29, 30)
- 04_pricing_1440.png: pricing + SEO start (15)
- 05_seo_1440.png: how it works, FAQ (13, 14, 22)
- 06_footer_1440.png: template chips + footer (24)
- 07_templates_index_1440.png (+ 07b full): library (16, 28)
- 08_role_page_1440.png (+ 08b full): role page (16, 17)
- 09_auth_modal_1440.png: sign in modal
- 10_billing_modal_1440.png: billing modal over auth (9)
- 11_home_top_390.png, 12_home_intake_390.png, 13_home_draft_390.png, 13b_home_draft_lower_390.png, 14_pricing_390.png, 15_role_390.png: mobile (8, 6, 30). 14 and 15 and 13b were captured but not individually reviewed.

## Gaps

- Not reviewed visually: 13b, 14, 15, 07b, 08b mobile/full-page captures.
- Billing modal buttons likely depend on sign-in state; not verified when signed in.
- Reduced-motion behaviour, focus rings and keyboard order not tested.
- Browser zoom oddity on 127.0.0.1 / localhost in the shared Playwright profile (33% / 75%): worked around with audit.localhost; the earlier first shot overwritten.
