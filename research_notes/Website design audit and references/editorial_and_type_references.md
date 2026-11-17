# Editorial and type references for a document-like JD generator

Tags: [F] = verified from fetch/search this session. [M] = from memory, unverified. [C] = computed here (WCAG contrast, python).
Tool budget was hit (15 calls). Site CSS/hex fetching was NOT done; most site-level detail is [M] or absent. No Awwwards/CSSDA/FWA/Godly/Land-book pages were fetched.

## 1. Award-recognised / type-led reference sites

### Takeaway
Only Typewolf Sites of the Day (late 2025) were verified. These show the current type-led consensus: a characterful serif plus a neutral grotesk, usually licensed. No verified site has a long form as hero in productivity/HR/legal; those are suggestions to inspect, flagged [M].

### Cited Findings
- Typewolf Sites of the Day, Sep-Dec 2025 [F], with fonts used - [Typewolf SOTD](https://www.typewolf.com/site-of-the-day):
  - Every (Sep 28 2025): Signifier + Switzer - [entry](https://www.typewolf.com/site-of-the-day/every-2025). Writing/publishing company; the closest topical match (serif editorial + neutral grotesk).
  - Speakeasy (Dec 8 2025): Tobias + Diatype + Diatype Mono - [entry](https://www.typewolf.com/site-of-the-day/speakeasy) (live: speakeasy.com). Developer tool using serif display + mono; relevant for a "tool with editorial voice".
  - Daylight (Dec 14 2025): Grenette + Styrene - [entry](https://www.typewolf.com/site-of-the-day/daylight-health).
  - Heart & Soil (Dec 13): Cardinal, Sweet Sans, Baskerville - [entry](https://www.typewolf.com/site-of-the-day/heart-and-soil).
  - Dirty Vine (Dec 12): Swear + DM Mono - [entry](https://www.typewolf.com/site-of-the-day/dirty-vine).
  - Muse (Dec 11): DaVinci + Suisse Int'l - [entry](https://www.typewolf.com/site-of-the-day/muse-paris).
  - Board (Dec 10): Kabel + Neue Haas Grotesk - [entry](https://www.typewolf.com/site-of-the-day/board).
  - Elena Scott (Dec 9): Editorial Old + Neue Montreal - [entry](https://www.typewolf.com/site-of-the-day/elena-scott).
  - TR Studio (Sep 27): Arizona Flare + Dia - [entry](https://www.typewolf.com/site-of-the-day/tr-studio).
  - Pattern across all: one expressive serif (or display) paired with one neutral sans/mono; no site uses two geometric/rounded sans families. Typewolf pages gave no commentary on layout/colour, so "why it feels authored" is my inference.
- Typewolf earlier examples [F]: Bookr (Mar 2022) uses Eksell Display + Manrope; Flask & Field (Mar 2023) uses Fraunces + DM Mono - [Manrope](https://www.typewolf.com/manrope), [Fraunces](https://www.typewolf.com/fraunces).
- Awwwards lists a "Typography Honors" tag and an "Editorial New" typeface profile (narrow serif for long-form + titles) [F] - [Awwwards Editorial New](https://awwwards.com/sites/editorial-new). No specific winning site vetted.
- 2026 trend writing (agency blogs, low authority, opinion) [F]: serif headlines + sans body, strong grids, asymmetric layouts, oversized margins, flanking columns used for margin notes/pull quotes; "visible structure" trend. No source mentioned hairline rules - [Law-firm trends](https://www.paperstreet.com/blog/2026-law-firm-website-design-trends/), [Creative Bloq typography 2026](https://www.creativebloq.com/design/fonts-typography/breaking-rules-and-bringing-joy-top-typography-trends-for-2026), [Line25](https://line25.com/articles/web-design-trends-2026/).

### Inferences
- Sites to inspect manually (all [M], not verified as award-winning in 2024-26, treat as leads): Stripe Press (press.stripe.com, book-as-hero, serif/grotesk, warm paper), Linear's changelog/method pages, iA Writer (ia.net, mono-led writing tool), Are.na, Read.cv, Every.to, Ghost/Substack editors, Notion/Craft docs pages, Pitch, Clerk/Rippling-style legal docs, Bear, Readwise. Use DevTools to pull font-family/hex.
- Technique list typical of this genre [M]: 1px hairline rules instead of card boxes; small-caps or mono labels (10-12px, +0.06-0.1em tracking); numbered sections (01, 02); a narrow left or right margin column of 160-220px for notes; body measure 60-70ch; warm off-white (#faf7f0-ish) with near-black ink; single accent used only for links/active state; motion limited to opacity/translate on section reveal and underline growth.

### Gaps
- No verified CSS/hex from any site; no CSSDA/FWA/Godly/Siteinspire/Mobbin/Land-book data fetched; no verified HR/legal/finance document-hero site. Awwwards search returned listing pages only.

## 2. Typography: Fraunces + Manrope

### Takeaway
Fraunces is a characterful "Old Style soft-serve" display serif; its quirky forms (WONK, SOFT) lean playful, not legal/HR-trustworthy, unless you pin WONK=0, SOFT=0 and use mid weights at opsz-aware sizes. Manrope is a semi-condensed geometric-ish sans that is fine for UI but a slightly techy/generic body for long documents.

### Cited Findings
- Fraunces axes [F] - [undercasetype/Fraunces](https://github.com/undercasetype/Fraunces): opsz 9-144 (default 144), wght 100-900, SOFT 0-100, WONK 0-1 (default 1). Lower opsz = higher x-height, looser spacing, wider letters. WONK swaps in quirky leaning n/m/h (roman) and flagged b/d/h/k/l (italic); wonky forms are "less desirable for continuous reading"; WONK auto-substitutes when opsz > 18 and is disabled at 18 and below. SOFT gives rounded forms toward the optical minimum.
- README default opsz 144 vs older Android mirror 36 - sources conflict; check the Google Fonts file - [search result summary](https://github.com/arrowtype/Fraunces).
- Typewolf on Fraunces [F]: open-source, by Phaedra Charles and Flavia Zimbardi, 2020, drawn from quirky early-20th-century Old Style serifs; similar to Windsor, Cooper; Adobe alternative New Spirit; suggested pair Garnett - [Typewolf Fraunces](https://www.typewolf.com/fraunces). Note: Windsor/Cooper associations are warm, retro, friendly, not institutional.
- Typewolf on Manrope [F]: only listed pairing is Reckless; used with Eksell Display on Bookr - [Typewolf Manrope](https://www.typewolf.com/manrope). Typewolf's Google Fonts list marks Manrope as NOT body-friendly (no asterisk), while Fraunces, Source Serif, Lora, Spectral, Libre Baskerville, DM Sans, Inter, IBM Plex Sans, Libre Franklin, Work Sans, Source Sans are marked body-friendly - [Typewolf Google Fonts](https://www.typewolf.com/google-fonts). Also mentions Instrument Serif, Newsreader, Literata as options.
- Typewolf Google-font combos [F] - [combinations](https://www.typewolf.com/blog/google-fonts-combinations): Cormorant Garamond + Proza Libre; Libre Franklin + Libre Baskerville ("traditional, established tone"); Trirong + Rubik; Work Sans + Taviraj; Eczar + Gentium Basic.
- 2026 trend piece names Playfair Display + Inter, DM Serif Display + Lato as common serif+sans pairs (indicates these are now cliche) - [search summary](https://www.creativebloq.com/design/fonts-typography/breaking-rules-and-bringing-joy-top-typography-trends-for-2026).

### Inferences / critique
- Weights 500-600 at heading sizes with default axes (opsz 144, WONK 1, SOFT 0 via Google CSS defaults) give high-contrast "fat" wonky display shapes. Fix: `font-optical-sizing: auto` and, if self-hosting/using axes API, `font-variation-settings: "WONK" 0, "SOFT" 0` for a sober look; or SOFT 50-100 only if you want friendly. Verify Google Fonts CSS2 serves WONK/SOFT axes (it supports opsz,wght,SOFT,WONK in the axis list) [M].
- Fraunces + Manrope: both are "friendly/rounded-ish" so neither supplies sober contrast; Manrope's geometric forms plus Fraunces soft forms = startup warmth, not recruiter-document gravitas. Manrope not body-marked by Typewolf.
- Five refined pairings (sizes [M], recommendations from typographic convention, not cited unless stated). Body 16-18px, line-height 1.55-1.65, measure 60-72ch; headings line-height 1.1-1.2, tracking -0.01 to -0.02em at 32px+, 0 at body, +0.06em on small caps labels.
  1. Newsreader (opsz variable, headings wght 500-600, opsz auto) + Inter/Public Sans body 16-17px. Newsreader named by Typewolf as an option [F]. Most document-like; Google Fonts, free.
  2. Source Serif 4 (headings 600, opsz auto) + Source Sans 3 body 16px. Both body-friendly per Typewolf [F]; trusty, plain, legal/government feel.
  3. Fraunces refined: headings wght 500, opsz 72-144 auto, WONK 0, SOFT 0, letter-spacing -0.015em + body in IBM Plex Sans 16px (body-friendly [F]) or Libre Franklin. Keeps your brand, removes quirk.
  4. Literata (body AND doc preview 17-18px, designed for long reading) + Libre Franklin/Work Sans for UI labels 13-14px. Literata named by Typewolf as option [F]. Good for the generated document pane.
  5. Instrument Serif (display only, 40-64px, one weight 400, sparing) + Geist/Inter body 16px + IBM Plex Mono 12px for labels/metadata (cf. Speakeasy and Flask & Field mono usage [F]). More editorial/trend-forward; risk: Instrument Serif is increasingly common [M].
  Licensed option [M]: Signifier + Switzer (Every, [F] pairing) or Tobias + Diatype; Lyon/Tiempos + Söhne.
- Variable axes use [M]: Newsreader/Literata/Source Serif have opsz; set `font-optical-sizing: auto` so body gets sturdier text cut and headings get display cut. Inter 4 has opsz too.

### Gaps
- No independent expert critique of Fraunces or Manrope found (search returned only specs/READMEs). No verified source on recommended line-height/measure; those are conventional values [M].

## 3. Colour

### Takeaway
Keep one accent, derive neutrals from the same hue, prefer warm paper neutrals with a dark ink for "document" trust; LinkedIn blue is functional but associates with a brand you are not.

### Cited Findings
- AI-default tell: indigo/violet gradient (Tailwind indigo-500) = "no real brand colour chosen"; fix = palette built from "something true about the product" - [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells), [Utsubo](https://www.utsubo.com/blog/built-with-ai-trust-signals-2026).
- Current palette contrast [C]: #0a66c2 on white 5.69:1; on #f4f8fc 5.33:1 (passes AA body).
- No research-backed study on warm vs cool neutral trust was retrieved. [M] Common claim: blue = trust in finance/HR; counter-view: it is the default so reads generic.

### Inferences (3 palettes, contrasts [C])
- A "Paper + navy ink" (trust, closest to legal/HR): bg #faf7f0, ink #1b1a17 (16.26:1), secondary text #4a4740 (8.66:1), muted #6b665c (5.33:1), accent navy #1f3a5f (10.73:1), hairline #e4ddcc, warm highlight/error #b4411f (5.28:1).
- B "Newsprint + green": bg #f7f5ef, ink #14213d (14.65:1), muted #5b6472 (5.49:1), accent deep green #0f6b5c (5.88:1) for primary button/links (white text on it also passes, approx 6:1 [M]); hairline #dedacd. Differentiates from LinkedIn blue while staying calm.
- C "Cool paper + ink blue + rust": bg #f5f3ee, ink #111827 (16.0:1), muted #475569 (6.83:1), accent #1d4ed8 (6.04:1) or keep blue family, secondary accent rust #9a3412 (6.59:1) for annotations/margin notes only; hairline #d9d5c8.
- Rules: 1 accent for actions, 1 annotation colour max, no gradients, avoid pure #fff cards on tinted bg (the boxed-card look); put white document sheet on warm bg only if it is the one "paper" object. Muted text min 4.5:1: #6b7280 on #fbfaf7 is 4.63:1 [C], so don't go lighter.

### Gaps
- No empirical colour-trust study found; guidance is design convention.

## 4. Layout

### Takeaway
Evidence retrieved is thin; patterns below are mostly convention [M] backed by 2026 trend writing on asymmetry/margins [F].

### Cited Findings
- 2026 trend writing expects strong grids, asymmetric layouts, oversized margins; an editorial layout example uses flanking columns for margin notes/pull quotes - [Paper Street](https://www.paperstreet.com/blog/2026-law-firm-website-design-trends/), [Editorial Magazine Layout example](https://chrislemke.github.io/website_designs/examples/Editorial_Magazine_Layout.html). Low-authority sources.
- "Three equal cards + uniform spacing" is a named AI tell; fix = asymmetry, different rhythm, content not forced into a triptych - [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells), [Utsubo](https://www.utsubo.com/blog/built-with-ai-trust-signals-2026).

### Inferences [M]
- Grid: 12-col, document in cols 3-9 or 4-10 (about 66ch), annotations in a 2-3 col margin; left rail numbering; asymmetry via text left, sticky note column right.
- Hairlines vs cards: use 1px rules (#e4ddcc) between sections, rows and fields; use a single shadowless elevated "sheet" for the document; reserve boxes for inputs and one result container. Density: tabular rows with rules and 12-13px mono/caps labels, 8px baseline, 24-32px section gaps.
- Sticky margins: `position: sticky; top: 24px` for a quality-score/notes column beside the document; collapse to inline notes under 900px.
- Tool UI: two-pane (inputs left 360-420px, live document right) with an inspector (tone, seniority, bias/quality lint flags) as a right margin or tabbed drawer; mirror iA Writer / Notion / Google Docs patterns [M]. Not verified by fetch.

### Gaps
- No fetched analysis of long-form tool UIs; no site CSS.

## 5. Tells of AI-generated sites

### Takeaway
Consistent across 2026 design blogs: indigo/violet gradients, Inter, centred hero, three equal cards, generic copy, purposeless motion.

### Cited Findings (all [F]; blogs/vendors, opinion not studies)
- Utsubo's 12 signals - [Utsubo](https://www.utsubo.com/blog/built-with-ai-trust-signals-2026): blue-purple gradient; Inter everywhere; generic centred hero; three equal cards with uniform spacing; purposeless motion (decorative fade-ins/hover); plastic AI imagery; no real proof (stock team photos vs real screenshots/customers/numbers); em-dash overuse and stock openers; buzzword soup ("seamless", "cutting-edge"); hedging and emoji bullets; boilerplate metadata (duplicate descriptions, missing OG image, generic alt); templated code with a11y/perf gaps.
- 925 Studios four tells - [925 Studios](https://www.925studios.co/blog/ai-slop-design-tells): Inter unchosen; indigo-to-purple gradient tied to Tailwind indigo-500; dark hero with gradient behind headline; gradient "Get Started" button; three rounded cards with soft shadows; thin interchangeable line icons; weightless headlines ("Build faster. Ship smarter.").
- Search summary: also glassmorphism, glowing dark-mode accents, gradient text, emoji icons, cards nested inside cards; training-data feedback loop; banning purple alone just shifts to next default - sources include [DEV Community](https://dev.to/alanwest/why-every-ai-built-website-looks-the-same-blame-tailwinds-indigo-500-3h2p), [Capital and Compute](https://capitalandcompute.net/blog/fix-ai-slop-design/), [Noqta](https://noqta.tn/blog/ai-design-slop-overused-ui-patterns-fix-2026), [21st.dev](https://21st.dev/blog/website-not-look-ai-generated), [Impeccable slop list](https://924b8765.impeccable-2rv.pages.dev/slop) (only seen as search listings, not fetched).

### Inferences
- Current site risk: white cards on pale blue, cyan accents, LinkedIn blue = default SaaS look; Fraunces + Manrope is a fairly common "AI-chosen" pair [M]. Em dashes also flagged as a tell (and banned in your own style rules).
- Counter-moves: real example JD as proof, hairlines not cards, one accent, asymmetric layout, specific copy, mono labels, motion only on state change.

### Gaps
- No peer-reviewed or large-sample study; slop-list pages beyond the two fetched were not read.
