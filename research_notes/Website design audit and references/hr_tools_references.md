# Design references: HR / recruiting / job-description tools (2026)

Method note. Fetched 2026-11 via WebFetch (markdown summaries, no CSS) plus direct curl of homepage HTML and linked stylesheets (no browser tools). Tags: [V] = verified from fetched HTML/CSS/page text; [M] = from memory/unverified; [I] = my inference. Hex counts are frequency in the stylesheet, not proof of usage on the hero. Betterteam and Indeed Employer returned HTTP 403 to all automated fetches (also Indeed's Medium brand post), so those two are [M] only.

## 1. Per-site facts

### Ashby - https://www.ashbyhq.com/
- Type [V, CSS https://www.ashbyhq.com/_next/static/css/cc11fecf1e7f45c4.css]: Signifier (serif, display) + TT Norms Pro (sans, body); CSS vars `--fonts-primary`, `--fonts-serif`. No mono seen.
- Colour [V, partial]: neutral near-white/lilac greys (#fcfcfe, #fafaff, #f7f7f8, #f3f2ff, #ebe9fe), purple-ish tints; accent amber #fcb415 and red #ff4143 appear. Rest of hex are code-highlight colours (ignore). [I] Pale lavender neutrals + one saturated accent.
- Hero [V]: H1 "What an ATS should be." Single primary CTA "Get in Touch" (no pricey "free trial"). Announcement banner above (AI Interviewer launch event). 18-logo strip directly under hero. Product tour with labelled tabs (Platform, ATS, Scheduling, CRM, Analytics) around a real "Custom Dashboard" screenshot.
- Cards [V]: 4 audience cards by headcount (1-100, 101-1000, 1000+, analytics) with image + "Learn more". Testimonial blocks with photo, title, logo. G2 + SOC 2 badges in footer. Closing CTA "Hiring excellence is one conversation away."
- Tone [V]: confident, opinionated, slightly cheeky; one emoji.
- Distinctive [I]: serif headline on a SaaS ATS signals editorial confidence; one CTA only.

### Workable (free JD generator) - https://www.workable.com/job-description-generator
- Type [V, CSS + Typekit https://use.typekit.net/lls2wtj.css]: proxima-nova (sans) + source-serif-pro (serif accents). No mono.
- Colour [V]: deep green #004038, brand green #00756a, #00544c/#00665b, mint tint #e0f9eb / #f6fefb, bright green #1fbc88, ink #151a21 / #0f161e, grey #6f7073; accents cyan #00b7cd, yellow #ffca00, red #d5351a (error), purple #7e59dc. Radius 8px most common, 16px for larger, 50% for pills/avatars.
- Tool UX [V]: H1 "Free Job Description Generator", subhead "Create the perfect job description for any position in seconds." Form = Job Title (text), Industry (optional, searchable dropdown, 148 options), Tone (optional: Generic/Formal/Friendly), Generate button. Loading text "It may take up to 10 secs." with AI-loader SVG; branded error state with spark icon. Below: "View all templates" + "Try Workable's free tools for managers"; "Free Tools for Managers" 3 blocks. Top banner promoting AI Recruiting Agent.
- Trust [V]: "1,000+ curated job descriptions" library; meta claims training on "millions of professionally crafted job descriptions".
- Tone [V]: short imperative, speed promise.
- Takeaway [I]: closest direct competitor. Minimal fields, optional labelled, honest loading copy, upsell kept secondary. Visually fairly generic green-SaaS.

### Textio - https://www.textio.com/
- Type [V, CSS template_fonts/main/home on textio.com/hubfs]: Iskra (display/heading, `--typography-font-iskra`), Ally Web (body), Charis (serif, secondary). Fonts load: Iskra x16 references on home.
- Colour [V]: charcoal #3f3f3f / #272526, greys #c7c5c6 #d0d0d0 #f4f3f4, white; magenta/violet gradients #f1b8ff #e166ff #b30bdb #ed32a2, orange #ff8500 #ff5c35, teal #1dc1a6, blue #00bdff, lime #85c902. Radius 6px/10px, many 0.
- Hero [V]: H1 "Attract. Interview. Hire. Develop. It's all on Textio." Hero image + logo strip. CTAs "See Textio", "See Lavalier", header "Get a demo", closing "Start trial now". Ribbon SVG dividers (gradient ribbons, filenames suggest orange/magenta + teal/blue [I]).
- Product [V]: tooltip screenshots (age-bias flag, examples) - i.e. inline annotation of text, their signature.
- Trust [V]: stats 30+ models, 1B+ HR docs, 25% of Fortune 500, 10 years; quotes from T-Mobile, Zendesk, Micron (500+ hours saved).
- Tone [V]: punchy, slightly irreverent ("crappy, biased data", "the og ai for hr").
- Distinctive [I]: the only one whose product IS text-under-review, so highlight-and-tooltip visuals are native. Most relevant for annotation idea.

### Greenhouse - https://www.greenhouse.com/
- Type [V, CSS www-greenhouse-com.shared.ff9127a38.min.css]: Untitled Serif (headlines, 147 uses) + Untitled Sans (body/UI). Tokens `greenhouse-design-system_2-0-*` with headline/body scales.
- Colour [V]: forest ink #15372c (151 uses), #031c17, #133026; green #008561, #006147, #4cb398; mint #c9f0e6 / #e6fff8; greys #f5f5f5 #efefef; blue #3574d6, #0050bd. Filenames mention mint, persimmon, periwinkle, pecan, earth accents [V names]. Radius 12px dominant, 1.5rem, 4px, 0.
- Hero [V]: H1 "Hiring. Orchestrated." subhead sourcing/interviewing/ATS "in one place". CTAs "Request a demo" (primary), "Explore the ecosystem" (secondary). Hero art: botanical outlined/filled SVGs.
- Product [V]: many mock UI snippets (candidate list with Strong Match / Dream Job badges, fraud alert, Voice AI Listening/Speaking panel, interview kit).
- Trust [V]: logo strips (Buzzfeed, Doordash, Hubspot, Zapier, Adyen), stats (228 recruiter hours, 118%), quotes with names, security/compliance icons.
- Tone [V]: short declaratives, "real shot / real signal".
- Distinctive [I]: serif + dark forest green + botanical illustration = warm, premium, non-"blue SaaS".

### Lever - https://www.lever.co/
- Type [V, CSS _next/static/css/338e76be4dec5bab.css, befb7163cff8a021.css]: Onest (sans, `--font-onest`), system serif/mono fallbacks. Tailwind-style scale vars.
- Colour [V]: teal/ink: #1a2e3b, #2a7a72 (accent, 29 uses), #134e4a, #14b8a6 #2dd4bf #5eead4, tints #e6f4ef #f4fbf8 #f0fdf9; slate greys #64748b #94a3b8 #e2e8f0 #f1f5f9 #f8fafc; success #16a34a #dcfce7. Radius 8px, rounded-lg, pills 9999px.
- Hero [V]: "Hiring That Doesn't Hijack..." (truncated in fetch); H2s "An ATS That Works Overtime (So You Don't Have To)", "Your Hiring Problems,".
- [I] Colour system is Tailwind slate/teal defaults = closest to "template-looking" of the set. Tone is playful.

### Gem - https://www.gem.com/
- Type [V, CSS chunks on gem.com/_next/static/chunks]: heading "Society Book" (serif, `--font-heading`), body "Die Grotesk A" (sans).
- Colour [V, sparse]: near-black #0a0a0a/#0b0b0b, whites #fcfcfc/#f3f2f2, pastel tints #f1d883 (butter), #f5dce7 (pink), #e1f6c3 (lime), #d6e8fe (blue), #3b94c4. Radius .3125rem (5px) common, 1.25rem, 1px (hairlines). CTA hover shadow `0 8px 32px #00000029`.
- Hero [V]: H1 "Better recruiting." then "Hire great people. Show off your success." / "Source, review, hire, and report. All in one place, in the blink of AI." Sections: "The numbers speak for themselves", "Trusted by the Best in the Biz", "20+ Industries. Thousands of Customers." Eyebrow pills present (`--eyebrow-pill-bg`).
- Tone [V]: playful, short.
- Distinctive [I]: serif headline, pastel tint blocks on near-white, tight hairlines.

### Pinpoint - https://pinpointhq.com/
- Type [V, CSS pinpointhq.shared.16aa6849a.css]: GT Sectra Fine (display serif) + GT Walsheim Pro (body/UI).
- Colour [V]: ivory background tokens (#f7f3e7, #e8dfca; "ivory-10/30/60" vars), ink #1f2729, deep green #3a5045 / #1f3329 / #455c51 / #278753; accent red-orange #ff492c (17), #f1564e, #ed9d85, yellow #fcb643, blue #0266fd / #4d65ff, Trustpilot green #00b67a. Radius 8px, 16px, 50%.
- Hero [V]: "The ATS built for multi-stream hiring" - run different processes side by side (desk-based vs deskless, early career vs exec). Swiper carousel in use.
- Distinctive [I]: warm ivory paper + serif + one hot orange-red. Strongest "not default SaaS" palette among ATS tools.

### Recruitee (Tellent) - https://recruitee.com/
- Type [V, CSS template_style / template_main on recruitee.com/hubfs]: PP Neue Montreal (primary), Nunito Sans, Lora (serif).
- Colour [V]: deep aubergine #140032 (177 uses), purple #5a1cb7, lilac #ece0f5, navy #04004a, magenta #e23393 / #d91c7a, plum #430848, greys #edebef #f7f7f7 #827a8d. Radius: heavy rounding - 32px (37), 2rem, 10px, .5rem.
- Hero [V]: "The customizable hiring software that helps you hire smarter and faster". Module `hero-custom`.
- [I] Purple/pink + large pill-ish radii = friendly, more generic SaaS.

### Teamtailor - https://www.teamtailor.com/en/
- Type [V, CSS _astro/BaseLayout.DbbuUeIU.css]: Archivo (sans, self-hosted woff2); Tailwind-v4-style tokens. Display scale `--text-display-l` 5.25rem, `--text-display-s` 3.75rem at weight 300, line-height 1.05, letter-spacing -.01em. Light-weight huge display = distinctive.
- Colour [V]: brand pink #f75fad (`--color-brand`), pastel pinks #fba5e7 #fdb9f2 #fde3fc, warm cream #f4f3f0 / #ece7df, lime #d8e372 / #deef5d / #e8f08c, brown ink #483434, white. Radii tokens: tile 12px, card 20px, small 8px.
- Hero [V]: H1 "For hiring people." subhead "All you need to make every hire count. Made smarter with AI and better with people." Photo of two people at a table, laptop glowing pink. CTA "Book a demo" repeated. iPad/iPhone device mockups of job list + career site. Product tour with orb image.
- Trust [V]: G2 4.6/5 badges, logos, SOC 2 / ISO 27001/27701/42001, GDPR.
- Tone [V]: warm, human, fragments.
- Distinctive [I]: pink + lime on cream, light-weight display type, real photography, rounded cards. Most personality.

### LinkedIn Talent Solutions - https://business.linkedin.com/talent-solutions
- Type [V, CSS clientlib-site]: system stack (-apple-system, Segoe UI, Roboto...) as base; "Community" (custom, SF Pro Display fallback) for display. Design tokens `--hue-web-*`.
- Colour [V]: LinkedIn blue #0a66c2 (131 uses), green #057642, red #cb112d, warm neutral background #f4f2ee and #eae6df, ink #474139, light blue #dde7f1 / #71b7fb. White bg tokens, offset bg #f4f2ee (warm grey, not cool). Radius 4px, 8px, 50%, token-driven.
- Hero [V]: H1 "Hire the people you need". Title "Powerful Recruiting Tools | Hiring on LinkedIn".
- Relevance [I]: the destination platform; the generator output is pasted here, so matching the cultural expectations (plain blue-trust, warm neutral) helps credibility, but do not imitate the brand (avoid confusion).

### Betterteam - https://www.betterteam.com/ [403, unverified]
- Fetch blocked. Only verified via search: support article on new dashboard job-description editor (headings, lists, dividers) https://support.betterteam.com/en/articles/15516109-meet-your-new-betterteam-dashboard ; regional homepage headline "HIRING MADE EASY", posts to 100+ job boards https://www.betterteam.com/uk . [M] Known for a large library of SEO job-description templates and plain, light-blue/white styling; not verified.

### Indeed Employer - https://employers.indeed.com/ [403, unverified]
- Fetch blocked. Search lists "Introducing Indeed's New Brand Identity" https://medium.com/indeed-design/indeed-new-brand-identity-launch-announcement-de9483e97678 and https://inside.indeed.jobs/?p=3328 (content not read). [M] Indeed Sans custom typeface, blue #2557a7-ish, human-centred photography, mostly dense functional UI. Search snippet confirmed only that Indeed built a custom typeface "Indeed Sans" (via search summary).

## 2. Cross-site patterns [V unless marked]
- Serif display is common among the better-looking set: Ashby (Signifier), Textio (Iskra), Greenhouse (Untitled Serif), Gem (Society Book), Pinpoint (GT Sectra Fine), Workable (source-serif-pro accents), Recruitee (Lora). Sans for body in all. No site showed a mono face in CSS beyond Tailwind defaults (Lever, Teamtailor).
- Neutral warm base is common: Teamtailor cream #f4f3f0, Pinpoint ivory #f7f3e7, LinkedIn #f4f2ee. Typical SaaS uses cool grey/white.
- Single accent: Pinpoint #ff492c, Teamtailor #f75fad, Greenhouse #008561 on #15372c ink, Workable #00756a.
- Radii: 8px (Workable, Pinpoint), 12px (Greenhouse, Teamtailor tile), 20px (Teamtailor card), 32px (Recruitee). Gem 5px.
- Hero formulas: short 3-5 word declarative H1 (Ashby, Greenhouse, Teamtailor, Gem, LinkedIn). Single or dual CTA, demo-led.
- Product shown as real UI fragments with badges/status chips (Greenhouse, Ashby), device mockups (Teamtailor), inline tooltip annotations (Textio).
- Trust = logo strips, specific numeric stats, security badges (SOC 2, ISO, GDPR), G2 rating. Free-tool pages (Workable) use just a library count.
- Copy: confident, fragment-based, a little wit.

## 3. Synthesis

What the best do better than a template-looking AI-built site [I from the verified data]:
- Own a type pair with a serif display and restrained sans body, not Inter-only.
- Warm neutral paper background (ivory/cream) + one saturated accent + one deep ink; not purple gradients, not white+blue.
- Real product fragments (badges, chips, tooltips) rather than abstract icons/3-card grids.
- Specific numbers and named proof instead of generic "trusted by".
- Short declarative headline, one primary CTA.
- Distinct radius system (consistent 8/12/20) instead of mixed.

Suit a free utility tool for recruiters [I]:
- Workable's flow: title first, optional fields labelled optional, tone selector, honest loading copy ("up to 10 secs"), custom error state, secondary next-step links.
- Textio's inline annotation: highlight phrases in the output and tooltip the reason (bias, clarity, LinkedIn length).
- Pinpoint/Teamtailor warm base + single hot accent; Greenhouse serif + deep green ink.
- Greenhouse-style status chips ("Strong Match") reused as quality chips on the output.
- Specific counts and a plain privacy/security line instead of logo walls (no customers to claim).
- LinkedIn-expected signals: character count, preview of how it looks in a post/posting.

Avoid:
- Demo-led CTAs and "Get in Touch" (sales copy) on a free tool; go straight to the tool above the fold.
- Logo-wall or G2/SOC claims you cannot back.
- Cool-slate + teal Tailwind default look (Lever's CSS is exactly slate/teal Tailwind values).
- Over-rounded 32px pill cards (Recruitee) and generic 3-column feature cards.
- Copying LinkedIn blue #0a66c2 or logo/brand (impersonation risk, confuses trust).
- Emoji in headlines; stock people photography without purpose.
- Fake stats. Textio's stats are real company claims; a new tool should show its own (e.g. documented lint rules count).

## 4. Ranked top 5 references to study
1. Workable JD generator (https://www.workable.com/job-description-generator): form field order, optional labels, 148-option searchable industry dropdown, tone select, loading/error microcopy, secondary CTAs, 8px radius and green palette tokens. Direct competitor - differentiate on output quality.
2. Textio (https://www.textio.com/): inline tooltip annotation of text, Iskra serif + grotesk pairing, stat blocks, punchy copy. Study how flags are shown on text.
3. Pinpoint (https://pinpointhq.com/): ivory #f7f3e7 + ink #1f2729 + single #ff492c accent, GT Sectra-style serif with Walsheim-style sans, 8/16px radii. Study how warm neutral + one hot accent avoids SaaS look.
4. Greenhouse (https://www.greenhouse.com/): serif headline + dark forest ink #15372c + #008561, botanical line illustration, UI fragments with chips/badges, 12px radius token system.
5. Teamtailor (https://www.teamtailor.com/en/): light-weight (300) large display type at 1.05 line-height, cream + pink + lime, tile/card radius tokens, warm human copy, device mockups. Study scale and restraint; do not copy pink.
Honourable: Ashby (single-CTA hero, serif, product tour tabs), Gem (pastel tint blocks, hairlines).

## 5. Gaps
- Betterteam and Indeed Employer not fetchable (403); everything about them is memory/unverified.
- Textio headline text not extracted from HTML (h1 not matched); hero headline came from WebFetch summary. Gem's Die Grotesk A as body is inferred from @font-face names; Gem hex list is sparse (CSS split in chunks).
- No computed styles: type sizes/spacing/grid widths and motion are not verified for any site except Teamtailor display scale tokens. Layout widths, grid, animation behaviour not measured.
- Hex frequency counts include non-hero UI/code colours; usage on hero not verified.
- Workable CSS is Next.js shared chunks; colours may include other pages' components.
