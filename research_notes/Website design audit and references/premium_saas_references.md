# Premium SaaS / developer-tool design references (for a light-theme recruiter JD generator)

Method note: WebFetch returns markdown text only. It strips CSS, so NO homepage CSS (font-family, :root vars, hex, radii, shadows, max-width) could be fetched for any site. Tags used below: [F] = verified from fetch of the cited page (copy, structure, section order, quoted write-ups); [S] = from search-result summary, secondary source; [M] = from memory, unverified. Page fetches done 2026-11-15, so copy is current-ish. Not reached/not fetched: Pitch, Loom, Vercel homepage, Arc (only thin page), Cal.com brand page (redirect, not followed). Attio brand/type search returned nothing.

## 1. Per-site facts

### Linear
#### Takeaway
Dense, neutral, single-accent product UI; marketing shows real product screens with numbered "Fig" labels. Pairing is Inter Display (headings) + Inter (text).
#### Cited Findings
- Headline "The product development system for teams and agents"; small announcement pill above headline; one-line subhead; two CTAs (Get started / Contact sales). [F] [linear.app](https://linear.app)
- Feature sections: bold heading, short paragraph, "Learn more" link; numbered figures "Fig 0.1-0.3" labelled Purpose-built / Powered by agents / Designed for speed. [F] [linear.app](https://linear.app)
- Product UI shown: real issue detail view with properties sidebar, kanban board, Slack-style thread, code diff, dated changelog list. Social proof: OpenAI and Ramp quotes, "over 50,000 product teams". [F] [linear.app](https://linear.app)
- Inter Display for headings "to add more expression", regular Inter for rest. [F] [Linear redesign post](https://linear.app/now/how-we-redesigned-the-linear-ui)
- Colour: moved HSL to LCH (perceptually uniform); theme = 3 inputs (base, accent, contrast) instead of 98 variables; limited blue chroma for more neutral look; text/neutral icons darkened in light mode. [F] same post
- Principles quoted: "reduce visual noise, maintain visual alignment"; "polish is felt more than seen"; evolve not rebuild. [F] same post
- Third-party token approximation (NOT official): canvas #010102, surfaces #0f1011/#141516/#18191a, accent #5E6AD2, text #f7f8f8/#8a8f98/#62666d, hairline #23252a, 8px radius, 4px grid, 13px body, depth from lightness steps not shadows. Article itself says it is for app UI, not marketing. [F, secondary] [buildmvpfast](https://www.buildmvpfast.com/blog/linear-aesthetic-tokens-density-keyboard-first-ux-2026)
#### Inferences
- Single desaturated indigo accent + grey ramp = the "authored" look. Light-mode equivalent: near-white page, one ink colour, 1px hairlines.
#### Gaps
- Real CSS (type scale, max width, motion) not retrievable.

### Stripe
#### Takeaway
Gradient mesh + big metric numerals + product widgets built from real billing data. Gradient is WebGL, not CSS.
#### Cited Findings
- Hero "Financial infrastructure to grow your revenue."; wave motif image (desktop/mobile variants); product tiles with photo backgrounds. [F] [stripe.com](https://stripe.com)
- Product UI shown as small live-looking widgets: "Pro Plan, billed monthly", "Tokens $0.01 per 1,000 units", usage meter. Large numerals as proof: 135+ currencies, $1.9T 2025 volume, 99.999% uptime, 200M+ subscriptions. [F] [stripe.com](https://stripe.com)
- Gradient rendered in WebGL as animated noise field (not CSS/SVG/video); credited to Kevin Hufnagl's reverse-engineering; newer homepage uses custom tool tuning blur, grain, rotation, thickness; bento grid for product range. [S] [search result summary](https://www.bram.us/2021/10/13/how-to-create-the-stripe-website-gradient-effect), [teardown](https://uirip.pages.dev/blog/teardowns/stripe)
- Font (Sohne, was Camphor) and #635BFF "blurple": [M]
#### Gaps
- Leerob and Hobday Stripe write-ups: fetch failed (blog body missing / 404).

### Notion
#### Takeaway
Warm, monochrome, illustrated; Inter-derived sans plus an editorial serif in marketing.
#### Cited Findings
- Copy: "The AI workspace that works for you."; centred headline, primary "Get Notion free", secondary "Request a demo"; hero pile of seven image assets; logo wall; tabs Capture / Find / Automate with desktop screenshot stacks; use-case cards with small illustrated icons; monochrome SVG logos; testimonial cards with portrait + logo. [F] [notion.com](https://www.notion.com)
- Official typography page says brand face is a cut of Inter renamed NotionInter, Regular and Semi Bold. [S] [Notion typography](https://notion.notion.site/Typography-55a8984fad2f472eb14287b98d84010c) (page itself fetched empty; claim from search summary)
- Serif: several third-party teardowns say Lyon (Commercial Type) for editorial headings/pull quotes; one says Noto Serif. Unsettled. [S] [madegooddesigns](https://madegooddesigns.com/?p=7570)
#### Gaps
- Hex, radii, shadows unverified.

### Vercel
#### Takeaway
Swiss-inspired restrained system; typography is the product.
#### Cited Findings
- Geist Sans for interfaces/body, Geist Mono for code/tabular; "readability and precision with a restrained style inspired by Swiss design"; SIL OFL 1.1 (free to use). [F] [vercel.com/font](https://vercel.com/font)
- Type system: heading sizes 72/64/56/48/40/32/24/20/16/14; label 20-12; copy 24-13 (24/20/18 for marketing heroes and quotes, 14 most common body, 13 secondary); mono variants pair with labels; Subtle/Strong modifiers via nested strong; tabular figures for numbers. [F] [vercel.com/geist/typography](https://vercel.com/geist/typography)
- Black/white high-contrast, hairline borders, grid lines: [M]
#### Inferences
- Mono for numbers/metadata next to sans labels is a cheap "tool-like" signal.

### Cal.com
#### Takeaway
Open-source, own display font (Cal Sans) + Inter; scannable feature list with metric-led proof.
#### Cited Findings
- Hero: "scheduling infrastructure for absolutely everyone", "highest-rated scheduling system", free for individuals; three CTAs (sign up / sales / pricing). [F] [cal.com](https://cal.com)
- ~40-item feature grid in "Name: description" format; metric-led customer cards ("6,000+ hours saved per week"); 4 pricing tiers; FAQ. Page showed a raw i18n key "landing.enterprise.complianceTitle" (a bug; shows even premium pages slip). [F] [cal.com](https://cal.com)
- Cal Sans (Mark Davis), open source, OFL; Cal Sans headings w600 + Inter body per third-party summaries. [S] [cal.com/brand](https://cal.com/brand), [cal.com/fonts](https://cal.com/fonts), [webdesignhot](https://www.webdesignhot.com/design.md/cal-com/)

### Superhuman
#### Cited Findings
- H1 "Superpowers, everywhere you work"; one primary button; layered product mockup (AI chat, inbox with tabs, team doc); logos strip; each product block repeats logo + big headline + one-line sub + filled and outlined buttons; ~12 feature cards with small gradient icons; dark bento screenshots for Go, light UI for Mail/Docs; accent rotation purple/green/orange. Closing CTA "Make it your best workday yet". [F] [superhuman.com](https://superhuman.com)
- Brand serif/colour specifics: [M] only.

### Raycast
#### Cited Findings
- H1 "Your shortcut to everything."; Download for Mac CTA; drawn keyboard with key caps and callouts (Fast, Ergonomic, Personal, Reliable); launcher-style mockups with "Actions Ctrl K" footer; tagline "It's not about saving time."; closing "Take the short way." Key-cap motif throughout. [F] [raycast.com](https://raycast.com)
- Inter with calt/kern/liga/ss03 features: third-party extract, unofficial. [S] [hagicode](https://design.hagicode.com/designs/raycast/)

### Attio
#### Cited Findings
- H1 "Welcome to agentic revenue."; hero with live-looking product preview (transcript, Slack thread, terminal panel); realistic annotated screens (company table with ICP scores, pipeline by stage with days-in-stage, workflow builder); floating caption cards; numbered anchor tabs; stats as large numerals with small labels; fragment copy: "Agents dig. You close." "Picks up leads at 2am." [F] [attio.com](https://attio.com)
- Typeface: no source found. [M] only.

### Framer
#### Cited Findings
- H1 "Framer is the pro website builder with a world-class design agent"; looping demo video; "New" pill; mockups embedded (agent chat, canvas variants, CMS table, SEO panel, localization list with completion %); benefit-led short headings; stats (Core Web Vitals, 99.99% uptime); closing "Your next idea starts here". [F] [framer.com](https://www.framer.com)

### Figma
#### Cited Findings
- Text-first hero "The full-stack creative canvas", single "Get started"; then big screenshot carousels of real tool panels with one dark-text caption each and "Explore..." links; testimonial; logo wall with "95%"; template gallery tiles; "New"/"Beta" badges. [F] [figma.com](https://www.figma.com)

### Arc / The Browser Company
#### Cited Findings
- Page is a short mission line "We're building better ways to use the internet with Dia and Arc", two CTAs, minimal nav, theme toggle. Brief, first-person plural, confident. [F] [thebrowser.company](https://thebrowser.company)
- Typography not retrievable.

### Pitch, Loom
- Not fetched (call budget). No claims made.

## 2. Synthesis: what makes them feel authored

Principles (each backed by [F] observations above unless marked):
1. Real product UI, not stock art. Linear, Attio, Framer, Figma, Superhuman, Stripe all show actual screens/widgets with plausible data (issue IDs, days-in-stage, "$0.01 per 1,000 units"). Specific fake data is the single strongest signal.
2. Restricted palette: grey ramp + one accent (Linear indigo [S]). Notion and Raycast near-monochrome. Colour rotates only where products are many (Superhuman).
3. Typographic contrast with few families: Inter Display vs Inter (Linear), Cal Sans vs Inter (Cal), Geist Sans vs Mono (Vercel), sans vs serif (Notion [S]). Mono for metadata/numbers.
4. Rules and hairlines instead of boxes; depth via tonal steps, not heavy shadows [S, Linear]. Radius about 8px, consistent.
5. Specific, short copy: fragments, verbs, concrete times ("Picks up leads at 2am"), sentence case. Cal's metric cards and Stripe's big numerals beat adjectives.
6. Numbered/labelled structure (Linear "Fig 0.1", Attio numbered tabs) gives an editorial, document feel.
7. One signature motif: Stripe gradient, Raycast key caps, Linear pill + Fig labels. One, not many.
8. Consistent section recipe: heading + one sentence + link + visual. Repetition reads as system.
9. Polish bugs break the spell (Cal's raw i18n key).
10. Sizing discipline: a published scale with few sizes (Geist: 14 body default, 13 secondary, 24/20/18 for marketing).

## 3. Cheap for a small team
- One free variable font pair: Inter (+ Inter Display style via tighter tracking/opsz) or Geist Sans + Geist Mono (OFL). Optionally one free serif (e.g. Source Serif / Newsreader [M]) for the JD output preview or pull quote.
- 3-input palette: ink, paper, one accent; define with CSS vars; hairline 1px border at about 8-12% ink.
- Hero shows a real generated JD (exact example input -> output) instead of illustration. Annotate with 2-3 floating caption cards.
- Numbered "Fig" labels and mono metadata chips (tokens, word count, reading level, bias flags) as tabular figures.
- Metric numerals if real (time saved, readability score) - only real ones.
- Specific fragment copy in recruiter terms ("Paste a messy intake call. Get a posting you can publish.").
- Type scale of about 6 sizes; line-height 1.5 body; max reading width 65ch for JD text.
- Subtle motion only: 150-200ms ease on hover/focus, streaming text reveal as the signature micro-interaction.

## 4. Does not transfer to a recruiter utility
- Dark canvas / glow / 13px dense app type (Linear tokens are app-density; source says not for first-touch pages [F]). Recruiters read long text; use 16px+ body.
- WebGL gradients (Stripe), keyboard-first/cmd-K (Raycast, Linear), agent/terminal panels (Attio, Framer), logo walls and enterprise sales tiers, developer-flavoured mono-heavy aesthetic - use mono sparingly.
- Fake social proof; "50,000 teams" style claims. Free tool: use honest specifics.

## 5. Five ranked references and what to study
1. Linear - restraint: grey ramp + one accent, Inter Display/Inter, hairlines, "Fig" labels, real UI blocks. Study homepage product frames; blog: [How we redesigned the Linear UI](https://linear.app/now/how-we-redesigned-the-linear-ui). Light theme version to emulate.
2. Vercel Geist - type system as the design: scale, Strong/Subtle, mono pairing, tabular figures. [Typography](https://vercel.com/geist/typography), [font](https://vercel.com/font).
3. Notion - warm, approachable for non-technical users; sans + editorial serif contrast; illustrated small icons; plain "Get Notion free" CTA. [notion.com](https://www.notion.com)
4. Attio - realistic annotated product screens with floating captions; fragment copy; numbered tabs; big-numeral stats. [attio.com](https://attio.com)
5. Stripe - widgets with real numbers, big numerals, disciplined grid; take the idea, skip WebGL (use a static soft gradient). [stripe.com](https://stripe.com)
Honourable: Cal.com (open fonts, scannable "Name: description" list, metric proof), Raycast (one signature motif, short copy).

## Gaps (overall)
- No CSS values verified for any site (tool limitation). To get them: browser DevTools / curl the stylesheet, which WebFetch cannot do. Another agent with Playwright could pull computed styles for Linear, Notion, Vercel, Attio.
- Pitch, Loom, Vercel homepage, Arc design, Attio typeface: not covered.
- Stripe/Notion write-ups partly unfetchable; serif identity for Notion unsettled.
