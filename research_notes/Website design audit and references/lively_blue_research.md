# Lively blue theme research

Evidence key: [V] = verified via search result text (secondary sources); [M] = memory, unverified. WebFetch returned no CSS for stripe.com, wise.com, typeform.com (rendered text only); LinkedIn brand page 404. Most brand data is [M]. Contrast ratios computed (WCAG 2.x formula, Python) - verified.

## 1. Reference brands
- Stripe: blurple #635BFF [V colorfyi.com/brands/stripe]; navy #0A2540, cyan #00D4FF as pairings [V, aggregator]. Cool navy ink, gradient mesh bands, real product UI hero [M]. Alive via colour fields + real UI.
- Coinbase: #0052FF + near-black #0A0B0D [V colorfyi.com/brands/coinbase]. Full-bleed blue blocks, white type, crisp edges [M].
- Wise: lime #9FE870, forest #163300, ink #0E0F0C, canvas ~#E8EBE6 / cream [V, unofficial: shadcn.io/design/wise, refero.design]. Lesson: second hue = distinct. Huge heavy grotesk headline [M].
- LinkedIn: #0A66C2 [M]; warm grey surfaces, blue only on actions. Familiar, not lively.
- Mercury [M]: soft periwinkle, off-white, editorial display; calm.
- Ramp [M]: near-black + acid yellow; blue not primary. One loud accent.
- Intercom [M]: black/off-white, blue in product UI. Figma [M]: multicolour dots, plurality = alive. Typeform [M]: near-black, pastel colour blocks, big friendly type. Notion [M]: warm neutrals, blue #2383E2 sparingly. Mailchimp [M]: yellow #FFE01B + deep teal, quirky serif. Dropbox [M]: #0061FE + cream/pastel blocks + illustration. Canva [M]: teal-violet gradient, illustration. Zoom [M]: #0B5CFF, white/navy blocks. Framer/Webflow/Squarespace [M]: black/white + one electric blue on big product mockups. Linear [M]: dark, muted indigo. Gusto/Rippling/Deel/Remote/Lattice [M]: warm accent (coral, amber, rose) + product screenshots + illustrated people.
Pattern: none rely on blue alone. Each has (a) a non-blue partner hue or near-black ink, (b) at least one full-width colour field, (c) real product UI or custom illustration, (d) a distinctive heavy display face.

## 2. What reads generic / AI-made
- Blue-to-purple gradient, indigo default (#6366F1, #3B82F6, #2563EB), purple glow.
- Pale blue page + identical white rounded cards + soft grey shadow; blue only on buttons.
- Cyan/neon glows everywhere; glassmorphism everywhere. Keep glow ONLY on the J: then it is a signature.
- Pure black/grey-900 text, Inter, centered hero + 3 icon cards.
Counter-moves: second hue (warm, small, sharp); tinted neutrals from blue hue; ONE big saturated blue block; navy ink not black; real product output (the JD sheet) as hero; crisp 2-4px corners; coloured hard offset shadows; one highlighted word per headline; sticker tags; saturation high (S 85-100%).

## 3. Colour science
- Lively pro blue: hue 220-232 (ultramarine/cobalt). Avoid 240+ (indigo, AI look) and 205-215 (LinkedIn/corporate). S 80-100%, L 45-55%; white text needs L <= ~50 for 4.5:1.
- 9-step ramp (hue 226): L 97, 93, 86, 76, 64, 54, 45, 36, 24; S ~100 mid, 70-80 at ends. Step 6 = primary, 7 = hover, 1-2 = tints, 9 = navy ink.
- Tinted neutrals: same hue 220-230, S 8-20%: bg L 97, hairline L 88-90, muted L 40, ink L 12-15.
- Accents: amber/marigold = optimism, highlighter, highest contrast vs blue, ink on it passes. Coral = warm/human, but near danger red. Mint = cool, blends with cyan glow, keep for success. Pink = playful, off for hiring.
- Navy ink 15-18:1 on white, so navy vs black has no accessibility cost.

## 4. Three palettes
Shared: success #12805C, warning #B45309, danger #C62828 (>=4.5 on white); field border #7C8CB0 (~3.4:1, passes non-text 3:1; assumed, not computed).
| token | A Ultramarine + Marigold | B Cobalt + Coral | C Electric + Mint |
|---|---|---|---|
| page bg | #F3F6FD | #EEF3FF | #F6F8FC |
| sheet | #FFFFFF | #FFFFFF | #FFFFFF |
| ink | #0B1B3F | #0A1633 | #101A33 |
| ink-soft | #3A4A6E | #38486B | #3F4B68 |
| muted | #5C6B8C | #586786 | #5E6A85 |
| primary | #1F4FFF | #2456E8 | #1D5BFF |
| hover | #1238D6 | #1A41C0 | #1445D1 |
| light tint | #E3EAFF | #DCE6FF | #E6EEFF |
| accent | #FFC53D | #FF6B57 | #14C9A5 |
| hairline | #D5DDF0 | #CCD8F2 | #DAE1EF |
Computed ratios (A / B / C):
- ink on bg 15.62 / 16.08 / 16.22; ink on sheet 16.9 / 17.87 / 17.25
- ink-soft on sheet 8.81 / 9.1 / 8.69
- muted on sheet 5.33 / 5.68 / 5.42; muted on bg 4.93 / 5.11 / 5.1
- white on primary 5.8 / 5.88 / 5.26; white on hover 8.2 / 8.2 / 7.5
- primary on bg (links) 5.36 / 5.29 / 4.95
- ink on accent 10.71 / 6.37 / 8.15 (accent as fill/highlight with ink text, never as text on white)

## 5. Liveliness without animation
- One full-bleed primary or navy band (hero or CTA); J glow reads best on deep blue.
- Alternate section backgrounds: bg tint / white / light tint / navy.
- Blue-tinted shadows: 0 12px 32px -12px rgba(31,79,255,.35); hard offset 4px 4px 0 ink for sheets.
- Marigold highlighter behind one headline word.
- Real JD sheet, rotated 1-2deg, ink border + offset shadow.
- Sticker tags: pill, 1px ink border, accent fill. Mixed corners: sheets 4px, tags pill.
- Big blue section numerals, mono labels in primary.

## 6. Typography
Fraunces SOFT/WONK 0 light reads formal/editorial; clashes in tone with a glossy modern J. Options (Google Fonts):
1. Fraunces opsz 144, wght 600-700, SOFT 100, WONK 1: friendlier, chunky, same family. Low risk.
2. Bricolage Grotesque 700-800: characterful, Wise/Typeform energy.
3. Onest / Plus Jakarta Sans / Instrument Sans for display (safer, less distinct).
Keep Plex Sans body, Plex Mono labels.

## Ranked recommendation
Palette A "Ultramarine + Marigold". Hue 226 sits between LinkedIn blue and AI-indigo; marigold is the strongest second hue (ink on it 10.7:1), works as highlighter and sticker, warm vs cool J glow; navy ink 16.9:1; all text pairs AA. B coral near danger red; C mint blends with cyan glow, weaker contrast.
Type: Fraunces opsz 144, wght ~650, SOFT 100, WONK 1 for H1/H2, marigold highlighter on one word; Plex Sans body, Plex Mono labels. Fallback test: Bricolage Grotesque 800.

Sources: https://colorfyi.com/brands/stripe , https://colorfyi.com/brands/coinbase/ , https://www.shadcn.io/design/wise , https://styles.refero.design/style/367c0c6e-73a7-441c-a8ff-91d139ac60dc
