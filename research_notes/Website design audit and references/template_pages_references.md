# Template-library and SEO content page design references (job description generator)

Legend: [V] verified from a 2026-11 WebFetch (text/markdown only, NO CSS/visuals seen). [M] from memory, unverified. [S] from search snippet. Blocked (403/timeout/404): Betterteam pages, Canva, Figma Community, Zety, Webflow templates, workable.com/job-descriptions. Fetch gave text structure only; colour, fonts, widths NOT observed for any site except where stated.

## Index/gallery pages: filtering, grouping, card vs list, previews, density

### Takeaway
Best galleries show the content in the card (thumbnail or excerpt), group by few named categories, and stay curated via editorial labels and counts. Job-description libraries (Workable) are plain link lists, which is the "auto-generated" look to avoid. For 9 templates: no filters/search needed, one grid with real previews.

### Cited Findings
- Workable index: breadcrumb, H1 "1000+ job description templates", 25 category links, then category sections of plain text links, no cards, no images, no search or filter; only a "Type in a job title" input + Next; very dense; claims "Optimized for job board approval and SEO". [V] - [Workable](https://resources.workable.com/job-descriptions)
- Workable index shows some titles duplicated across categories (e.g. "Copy Editor", "Nurse Manager"), a visible auto-generated tell. [V] - same URL
- Notion gallery: top-category tiles with thumbnail + count ("13,989 templates"), "Browse 349 categories" link; template card = preview thumbnail, title, creator, price ("Free"); collections cards = illustration, category label, title, one-line description, "Explore" link; featured templates labelled "Handpicked by our editorial team". Different card density per section. [V] - [Notion](https://www.notion.com/templates)
- Resume.io gallery: whole card is one link; thumbnail ~380px, "Use this template" line, format tags (pdf, docx), optional badges ("Monochrome", "Gold Standard"), name, 1-2 line description; chip row filters (style, layout, format, ATS) are links to separate category pages not in-page toggles; ~37 cards in uniform grid; same templates repeat across sections (padding); alt text inconsistent; SEO text blocks, comparison tables, two overlapping FAQ blocks. [V] - [Resume.io](https://resume.io/resume-templates)
- Stripe guides: themed sections each with heading, one-line summary, "See all"; card grid with small category label, title, "Read now"; no search/filter; no excerpts so titles carry meaning; dense (~10 sections). [V] - [Stripe](https://stripe.com/guides)
- Indeed Hire is not an index of templates (it is a post-a-job landing page); its job description resources sit in a mega-menu "Job Descriptions" group and an A-Z index at the foot of detail pages. [V] - [Indeed](https://www.indeed.com/hire/job-description), [Indeed SWE](https://www.indeed.com/hire/job-description/software-engineer)
- Linear Method: numbered, grouped nav (Introduction 1, Direction 4, Building 6; entries numbered e.g. 2.2, 3.5) - numbering signals editorial curation. [V] - [Linear](https://linear.app/method)
- Betterteam: 2,000+ templates per TechRadar; sample structure title / "Reports To" / "Job Overview" (4 sentences) / "Responsibilities and Duties"; offered as Word file; PDF via Save As. [S] - [Betterteam template](https://www.betterteam.com/job-description-template). Page fetch itself 403.

### Inferences
- With 9 items, a card grid beats a list. Each card should preview real content (first 2 lines of summary + 3 responsibilities, or a mini document thumbnail), not just a title and icon.
- Skip search/filter/pagination; use 1 line of "who it is for" per card plus a small meta line (e.g. seniority, sections, "reviewed <date>").
- Avoid repeating a card across sections (Resume.io padding) and avoid duplicate titles (Workable).
- Counts and numbering ("9 templates", 01-09) read as editorial; Linear numbering and Notion "handpicked" label are the models.

### Gaps
- Canva, Figma Community, Zety, Webflow, Betterteam index: all blocked; filter UI details unverified [M only].
- No visual style (colour/fonts/spacing) observed on any site.

## Detail pages: layout, actions, TOC, related, SEO, AI CTA

### Takeaway
Leading detail pages share: breadcrumb, H1 + dated byline, TOC, standard section order, FAQ with schema, related roles. Surprisingly, none of Workable/Indeed expose a copy/download button in fetched text - an opening for a copy-first design.

### Cited Findings
- Workable SWE page: skip link; 4-level breadcrumb with BreadcrumbList schema; H1 + one-paragraph definition + short responsibility list; template sections Job brief / Responsibilities / Requirements and skills; no copy/download (only social share); mid-page banner "Hiring for this role? Post this job for free"; three related blocks (job descriptions, interview questions, topics) with "View more"; "Available in" language links; author byline with photo and bio; reviewer credit (Senior Recruitment Manager); "Refreshed on" date (Feb 1 2022) while title says "2024 TEMPLATE" (stale-date inconsistency); view count 208,938; FAQ with FAQPage schema; an AI JD generator secondary link; "Jump to section" label with no links. [V] - [Workable SWE](https://resources.workable.com/software-engineer-job-description)
- Indeed SWE page: breadcrumb Home > How to Write a Job Description > Software Engineer (top and bottom); promo banner above article ($75 credit); H1 "...: Top Duties and Qualifications"; "Last updated", editor byline, "9 min read"; "On this page" TOC with See more/less; fixed sequence: summary, duties, skills, salary, education, experience, FAQs; sample postings with labelled fields (Job Type, Pay, Benefits, Schedule, Experience, Location) truncated by "Show more"; repeated "Create job description" CTAs; related "samples for similar positions"; A-Z title index; FAQ accordions; salary data with dates; editorial guidelines link; disclaimer not legal advisor; no copy/download seen. [V] - [Indeed SWE](https://www.indeed.com/hire/job-description/software-engineer)
- Indeed footer claim "over 15,000 articles in 6 languages", named editorial team. [V] - same URL
- A List Apart article: byline with original and updated dates, topic categories, anchored headings (no TOC), "Further reading" and "More from ALA" blocks. [V] - [ALA](https://alistapart.com/article/responsive-web-design/)
- Linear Method: banner for agents/MCP at top; prev/next and breadcrumbs not present in extracted text. [V] - [Linear](https://linear.app/method)
- Resume.io card CTA "Use this template" deep-links to builder with template param (?template=london) - model for "customize with AI" carrying role pre-filled. [V] - [Resume.io](https://resume.io/resume-templates)

### Inferences
- Layout: breadcrumb > H1 > 1-line meta (updated date, reviewer, read time) > action bar (Copy, Download .docx, Customize with AI) > the document as a visibly "paper" block > "How to customize" notes > FAQ > related roles (other 8, or 3).
- Sticky action bar (Copy / Download / Customize) is an unmet gap; competitors only have post-job banners. Make Customize with AI the primary button, passing the role into the generator.
- Document preview should be selectable plain text with a one-click copy, and optionally highlighted placeholders [Company], [Location] to show where customizing happens.
- Put promo CTA after the document, not above it (Indeed puts banner above the article; likely hurts the "just give me the template" intent) [inference].
- Add FAQ + FAQPage JSON-LD, BreadcrumbList JSON-LD; show a real "Last reviewed" date and keep it consistent with the title (Workable mismatch hurts credibility).
- TOC is only useful if the page is long; for a template page use a compact in-page jump row (Summary / Responsibilities / Requirements / FAQ).

### Gaps
- Sticky behaviour, widths, copy buttons on Betterteam, Canva, Zety: not observable (403 or text-only fetch).
- Whether JD-generation "customize" CTA converts better in sticky vs inline: no data found.

## Typography and colour on long reading pages

### Takeaway
Evidence found is about measure and size, not colour. Use ~60-70ch measure, ~1.5+ line height, body 16-19px.

### Cited Findings
- Smashing: aim ~60-70 characters per line, `width: 60ch; max-width: 100%`; body line-height `calc(1ex / 0.32)` (browser default 1.2 too tight); use rem/em so user preferences apply; headings h1 2.5em, h2 2em, h3 1.75em, h4 1.5em. [V] - [Smashing](https://www.smashingmagazine.com/2020/07/css-techniques-legibility/)
- GOV.UK Design System: default paragraph 19px (`govuk-body`); lead paragraph 24px desktop, "only use once per page"; small body 16px use sparingly. [V] - [GOV.UK paragraphs](https://design-system.service.gov.uk/styles/paragraphs)
- GOV.UK type scale: 19px body pairs with 25px line height; since Frontend v6.0.0 19px on all screen sizes. [S] - [GOV.UK type scale](https://design-system.service.gov.uk/styles/type-scale)
- GOV.UK page itself did not state a 75-character measure; one third-party source says layout is two-thirds of 960px (secondary). [S]

### Inferences
- Document block: 17-18px body, line-height ~1.6, max-width ~65ch, headings in a slightly heavier weight, section labels small caps/16px. Use one lead paragraph only (GOV.UK rule).
- Colour: high-contrast near-black on warm off-white for the document "paper"; one accent colour for CTAs only [M/opinion, no fetched source].

### Gaps
- No fetched colour palettes or font stacks from any reference site; Linear/Stripe/ALA visuals not observed.

## Trust and credibility cues

### Takeaway
Named reviewers, dated updates, sourced data and editorial policy are the cues that exist at scale; the AI-generated risk is stale or inconsistent dates.

### Cited Findings
- Workable: byline + bio, reviewer credit with title, "Refreshed on" date, view count, FAQ; date inconsistent with "2024" title. [V] - [Workable SWE](https://resources.workable.com/software-engineer-job-description)
- Indeed: editorial guidelines link, named editorial team, last updated, sourced salary data with dates, legal disclaimer, footnoted survey stats (e.g. N=600 employer survey) on hire landing. [V] - [Indeed SWE](https://www.indeed.com/hire/job-description/software-engineer), [Indeed Hire](https://www.indeed.com/hire/job-description)
- Notion: "Handpicked by our editorial team"; category counts. [V] - [Notion](https://www.notion.com/templates)
- Resume.io: unsourced claims in FAQs and repeated/overlapping FAQ blocks (credibility weakness). [V] - [Resume.io](https://resume.io/resume-templates)

### Inferences
- For a free AI tool: state how templates were made ("drafted by AI, edited by a person, last reviewed <date>"); honest provenance beats a fake expert byline. Link a short methodology note; add a "not legal advice" line for compliance items (pay transparency, EEO).
- Show free/no signup/no card near the CTA; avoid made-up usage counts.

### Gaps
- No evidence found on whether AI disclosure helps or hurts trust.

## What makes a library feel curated vs auto-generated

### Takeaway
Curated = few items, distinct per-item copy, consistent structure, editorial labels, real previews, honest dates. Auto-generated = giant link dumps, duplicate entries, repeated cards, boilerplate FAQs, stale dates.

### Cited Findings
- Auto-generated tells observed: Workable duplicate titles across categories and 1000+ link dump [V]; Resume.io same templates repeated across sections, inconsistent alt text, duplicated FAQ [V]; Workable date mismatch [V]; Indeed page with repeated keyword/number strings in source (widget artifacts) [V].
- Curated tells observed: Notion editorial "handpicked"; Linear numbered, grouped method pages; Stripe sections each with one-line summary [V].

### Inferences
- Write a unique 1-line positioning for each of 9 roles (who hires, what's unusual), not a template string "X job description template".
- Differentiate role pages with role-specific sections (e.g. must-have vs nice-to-have, typical salary band caveat, pitfalls) rather than identical skeleton text.

### Gaps
- No quantitative research on perceived curation.

## Recommendations for the 9-template library

1. Index: 3x3 grid desktop, 2 col tablet, 1 col mobile. No filters/search. Optional single row of 3 group labels only if natural (e.g. Tech / Business / Operations) - otherwise one flat grid.
2. Card: mini document thumbnail (real first lines of the JD, faded bottom), role name, 1-line "best for", meta (sections count, updated date), whole card is link, hover shows "Open template". Number 01-09.
3. Header: H1 + one-sentence promise + "9 templates, free to copy" + secondary CTA "Write one from scratch with AI". Provenance note beneath grid.
4. Detail: breadcrumb (Templates > Role); H1; meta line; sticky bar with Copy (primary secondary), Download .docx/.txt, Customize with AI (primary, prefilled role); document in a paper-like panel, ~65ch; highlighted placeholders.
5. Below document: "How to customize" 3 bullets, role-specific tips, FAQ (3-5 Qs, FAQPage JSON-LD), "Other templates" (all 8 as compact list or 3 nearest), final CTA band.
6. SEO: unique title/meta per role, BreadcrumbList + FAQPage (+ optional Article) JSON-LD, one H1, real last-reviewed date, internal links between roles.
7. Typography: 17-18px/1.6, 60-70ch, one lead paragraph, rem units.
8. Trust: reviewed date, methodology link, no fake counts or reviewers.

## Ranked references (study order)

1. Indeed Hire SWE page - https://www.indeed.com/hire/job-description/software-engineer : fixed section sequence, "On this page" TOC, last updated + read time, labelled sample fields, FAQ, related roles, disclaimer. [V]
2. Workable SWE page - https://resources.workable.com/software-engineer-job-description : breadcrumb schema, reviewer credit, FAQ schema, related blocks; study what NOT to do (date mismatch, no copy button, link-dump index). [V]
3. Notion template gallery - https://www.notion.com/templates : card anatomy with preview thumbnail, editorial "handpicked" labelling, counts. [V]
4. Resume.io templates - https://resume.io/resume-templates : whole-card link, "Use this template" deep link to builder, format tags, badges; avoid repetition and SEO padding. [V]
5. GOV.UK Design System + Smashing legibility - https://design-system.service.gov.uk/styles/paragraphs , https://www.smashingmagazine.com/2020/07/css-techniques-legibility/ : body size, one lead paragraph, 60-70ch measure, line height. [V]

Honorable: Stripe guides (section heading + one-line summary + See all) [V]; Linear Method (numbered grouped nav) [V]; Canva/Figma/Zety/Webflow could not be fetched - revisit with a browser.
