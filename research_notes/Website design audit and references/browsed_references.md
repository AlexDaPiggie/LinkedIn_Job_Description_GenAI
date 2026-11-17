# Browsed design references

Method: all 12 sites loaded at 1440x900 (Chromium, headless, date 2026-11-16, cookie banners left in place). Playwright MCP browser was locked by another process ("already in use"), so I used the globally installed Python Playwright with a fresh context instead. Same viewport, same computed-style extraction. Screenshots in `refs/<name>.png`.

Tags: [M] = measured via getComputedStyle (first ~4000 elements, hero state). [J] = my judgement from viewing the screenshot.
Caveats [M]: colour counts are element counts, not area. "max-w" = largest max-width px found (<=1800). Section padding is often 0 because sites use wrappers not `<section>`. Shadow/gradient counts are elements with box-shadow / gradient background-image.

## Award check (what I actually saw)
- Typewolf Site of the Day page (listing page 1 as served; newest entry shown was DEC 14, 2025, so the served page looked stale vs today): **Speakeasy - DEC 8, 2025** (fonts listed: Tobias, Diatype, Diatype Mono). **Every - SEP 28, 2025** (Signifier, Switzer). Both confirmed. [M]
- Awwwards Sites of the Day page 1: none of the 12 sites appeared. Not claimed. [M]
- No award claims for any other site.

## Table
| Site | H1 font | H1 size/wt/lh/ls | Body font/size | Page bg | Text | CTA | Top colours | Max-w | Radii | Shadows/Grads | # font sizes |
|---|---|---|---|---|---|---|---|---|---|---|---|
| every.to | Signifier (serif) in logo/headlines; no h1 tag | headlines ~40-48px | Switzer 15px | #020202 | #fff | pale cyan #C0F0FB, r6 | white, black, #1a1a1a, warm cream #FDFAF7 | 1280 | pill, 4, 6, 10 | 3 / 8 | 14 |
| delphi.co | Delphi Pythia (serif-ish display) | 50 / 500 / 51 / -1.75px | Delphi Inter 16 | #fff over warm #F7F4F0 wash | #21201C | orange oklch(.67 .22 42), r26 | #21201C, white, #63635E, #F0EAE4 | 1152 | 24-28, pill | 71 / 33 | 20 |
| speakeasy | Tobias (serif) | 79 / 100 / 79 / -2.8px | ABC Diatype 16; ABC Diatype Mono for labels | #FAFAFA | #0F0A07 | black btn, mono caps label, r8 | #0F0A07, #000, #575251, #969696 | 1728 | 2-5, pill | 26 / 74 | 27 |
| granola | Quadrant (serif) | 86 / 400 / 80 / -1.7px | Melange 16 | #fff | #292929 | black pill / translucent olive pill | #292929, #0E0F0C, #fff, #72726E | 1440 | pill, 4, 8, 16, 24 | 50 / 120 | 20 |
| attio | Inter Display | 64 / 600 / 61 / -1.3px | Inter 16, JetBrains Mono, Tiempos Text (accent) | #fff | near-black #0F1114 area | near-black btn, r10 | near-black, white, #E3E6EA, #5A6270 | 1440 | 6, 8, 10, 12, pill | 88 / 122 | 20 |
| mercury | Arcadia Display | 49 / 480 / 54 / normal | Arcadia 16 | photo bg (dark) | #EDEDF3 | periwinkle #5266EB, r32 | #EDEDF3, black, #C3C3CC | 1376 | 4, 8, 12, 32, 40 | 3 / 1 | 11 |
| linear | Inter Variable | 64 / 510 / 64 / -1.4px | Inter 16, Berkeley Mono | #08090A | #F7F8F8 | indigo #5E6AD2; white pill nav btn | #F7F8F8, #8A8F98, #62666D, #D0D6E0 | 1436 | 4, 8, 12, pill | 39 / 56 | 14 |
| ramp | TWK Lausanne | 64 / 400 / 64 / ~0 | Lausanne 16, Mono Regular for stat labels | #fff | near-black warm | lime #E4F222-ish (visual) + black, r6 | near-black, white, 60% black | 1440 | 4, 6, 12 | 2 / 7 | 9 |
| cal.com | Cal Sans | 80 / 700 / 86 / -0.8px | Cal Sans + Segoe UI Variable 16 | #fff | #242424 | #242424 btn, r10 | #242424, #5F6570, white | 1320 | 8, 10, 14, pill | 209 / 6 | 24 |
| raycast | Inter | 64 / 600 / 70 / normal | Inter 16, Geist Mono | #07080A | #fff | light grey #E6E6E6, r8 | white, 60% white, #9C9C9D | 1440 | 4, 6, 11, 12 | 352 / 235 | 18 |
| paper.design | Matter | 48 / 360 / 48 / -0.96px | Matter 18, paperMono | #EFEFEA-ish warm grey (lab 94) | near-black | black btn, r4 | black, 80% black, slate oklch(.2 .019 258) | 1080 | 1, 4, 5, 6 | 31 / 7 | 12 |
| plain.com | ABC Favorit Medium | 48 / 500 / 46 / -1px | ABC Favorit Regular 16 (body tag reported 12px), Geist Mono | #fff | #252D2A | deep green #1A5C45-ish btn, mono caps, pill | #0E2D20, #252D2A, #9AF6BB mint | 1470 | 3, 5, 8, pill | 110 / 0 | 13 |

Notes on table: Every h1 not found (logo is the masthead); headline sizes read from the screenshot/sizes list. Ramp and paper CTA colours partly [J] from screenshot (lab() values not converted).

## Per-site notes
Format: layout [J], product shown [J], designer-made signal [J], steal.

**Every.to** (Typewolf SOTD Sep 28 2025 [M]) - Dark, serif masthead centred, 3-column editorial grid with hairline rules. Product = articles; no UI. Feels designed: Signifier serif with a swash italic "E" inserted in words, engraved-style illustrations in saturated colour blocks, hairline dividers. Steal: hairline vertical/horizontal rules between columns instead of cards; one serif quirk (italic swash letter) as brand signature. Relevance: low (dark), but best serif/sans pairing proof.

**Delphi.co** - Light warm off-white, centred, big search/prompt box with soft shadow and concentric arcs behind it, pill filter chips, then dark jewel-tone cards. Product = the input box itself, the tool IS the hero. Feels designed: tight negative tracking on the serif-ish display (-1.75px), warm neutral (#21201C ink, #F0EAE4 tint) not grey, orange accent used once. Steal: hero IS the working input, with example-prompt chips under it. Very relevant to a generator.

**Speakeasy** (Typewolf SOTD Dec 8 2025 [M]) - Light #FAFAFA, left-aligned thin serif (weight 100, 79px) headline, ASCII art on right, mono ALL-CAPS buttons and labels, hairline-boxed logo grid, rainbow hairline on top and on CTA border. Feels designed: serif display + mono labels + 1px rules, ASCII image replaces stock hero art. Steal: thin serif headline with mono uppercase button labels and 1px-ruled tables. Relevance: high for type pairing.

**Granola** - White, left-aligned giant serif (86px, tight 0.93 line-height), real product mock on right: a paper-like warm-grey note window with serif note title, sitting over textured art. Feels designed: product screenshot is a literal document in the same serif; olive/lime accent; pill buttons. Steal: show the product as a warm paper document with a serif title inside a window chrome. Highest relevance (document in a tool).

**Attio** - White, centred, sans 64px/600 headline, subtle blue-to-white wash at bottom of hero, big app mock in a grey window frame with traffic lights; includes an input with typing animation. Uses Tiempos serif sparingly. Steal: app mock framed in a light grey bezel (#F4F5F7), with a typing prompt box inside. Relevance: high for the tool-like UI and pale cool wash.

**Mercury** - Full-bleed dreamy photograph, centred white sans headline, periwinkle pill CTA with email field. Photo is the design. Not transferable (needs photo budget, dark overlay). Steal: email-inline CTA group in one rounded capsule. Relevance: low. Colour hint: periwinkle #5266EB is close to a cool-blue accent.

**Linear** - Near-black, left-aligned 64px headline, hairline top nav, large app screenshot bleeding off the fold. Dark, so low direct relevance. Steal: product screenshot starts above the fold inside a 1px-bordered panel; tight -1.4px tracking; mono used for tiny identifiers.

**Ramp** - White, left-aligned 64px headline, pill email capture with lime CTA, faint dot-grid background, large grey panel holding a clean product UI, and a live ticking stats strip with mono labels at the bottom. Steal: faint dot-grid backdrop (very cheap, tool-like) and mono small-caps for metadata. Relevance: high; strong light UI.

**Cal.com** - White, centred, heavy Cal Sans 80px headline with inline UI chips (clock, avatar, booking pill) in place of words. Browser-frame mock below. Steal: inline UI chips inside the headline. Cal Sans bold is too blunt for a serif-led design; skip the type, keep the chips idea. Shadow count 209 is mostly the mock, not the shell.

**Raycast** - Near-black, huge red diagonal gradient art, centred bold headline over it, mono small print under the download button. Heavy gradient (235 elements), conflicts with our no-gradient/glow rule. Steal: only the mono small print line under the CTA. Relevance: low.

**Paper.design** - Warm light grey #EFEFEA-ish with paper grain texture and a folded-corner ruler diagonal top right; lowercase headline with two-tone (black / grey) second line; lightweight 360 weight; mono used for the terminal mock; very black-and-white with ONE blue accent in the logo. Real app mock directly under the CTA. Feels designed: paper texture, lowercase voice, two-tone headline, tiny radii (4-5px). Steal: two-tone headline (black line then mid-grey continuation) and tiny radii with 1px borders. Highest relevance for the paper/tool feel, and its 1080px content width.

**Plain.com** - White, left headline in ABC Favorit, forest-green + mint palette, mono caps buttons, dotted radial diagram art. Steal: mono caps button labels plus a single deep-ink colour (#0E2D20 style) used for all text and buttons instead of black. Relevance: medium.

## Patterns across the set [J, supported by measured values]
- Light sites mostly use headline sizes 48-86px with negative letter-spacing -1 to -2.8px and line-height ~1.0. Measured on 8 of 12.
- Serif display + sans body on light: Granola, Speakeasy, Delphi, Every. All four use a cut with tight tracking and no bold (weights 100-500 measured on 3).
- Mono for labels/buttons: Speakeasy, Plain, Ramp, Paper, Linear, Attio (measured mono families on 9 of 12).
- Content width is 1080-1440; sections 96-160px vertical padding where measurable (Speakeasy 96, Linear/Ramp 128, Granola 160).
- Radii: designer-made sites use either small (2-6px, Speakeasy, Paper, Mercury cards) or full pills; mixed 8-12 generic radii appear on the more template-like ones.
- Font-size count: restrained ones (Ramp 9, Mercury 11, Paper 12) vs messy (Speakeasy 27, Cal 24). Fewer = more disciplined.
- Warm neutrals (Delphi, Paper, Granola) beat pure white; our cool-blue page should tint neutrals toward blue in the same way (ink with slight blue, not #000).
