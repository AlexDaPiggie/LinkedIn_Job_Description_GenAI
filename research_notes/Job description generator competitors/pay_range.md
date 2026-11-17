# Pay range: required or optional? (researched 2026-11-15)

## Verdict
Optional by default, jurisdiction-aware: soft nudge everywhere, hard require (or strong warning on export) only when location is in a covered jurisdiction.

## 1. Competitors
- Greenhouse: admin-defined "pay transparency rules"; selecting a rule makes pay range fields required on the job post, can lock values. So jurisdiction-driven requirement. https://support.greenhouse.io/hc/en-us/articles/10027759675931
- Ashby: structured compensation field on job settings / posting level, compliance-oriented. https://docs.ashbyhq.com/compensation.md , https://www.ashbyhq.com/blog/recruiting/salary-transparency-feature
- Workable, Indeed, LinkedIn, Betterteam, Textio, Grammarly, Ongig: NOT verified (search returned no official docs). Treat as unconfirmed; check manually.
- Pattern verified: ATS = location-triggered required; generators = unverified.

## 2. Candidate / recruiter data (survey-based, vendor-sourced; stated intent, not application data)
- Monster Jan 2026: 60% of 1,000+ US workers would not apply without a salary range. https://www.monster.com/career-advice/research/job-search-dealbreakers
- Patriot Software Jan 2026: 44% unlikely to apply without pay range. https://www.patriotsoftware.com/blog/payroll/pay-transparency-hiring-survey/
- Gartner (via coverage): 44% skipped a posting for no range. https://www.cfodive.com/news/job-seekers-avoid-postings-no-salary-transparency-report-labor-compensation/818192/
- Not found: Indeed Hiring Lab application-lift figures, recruiter-reluctance data. Gap.

## 3. Legal (sources conflict on counts; verify before citing)
| Jurisdiction | Pay range in posting? |
|---|---|
| CA, CO, NY state, WA | Yes, essentially all postings (CO/CA/NY per roundup) |
| NYC | Yes (good-faith range) |
| VA | Effective 2026-07-01 |
| ME | Effective 2026-07-29 (10+ employees) |
| Others (CT, DC, HI, IL, MD, MA, MN, NJ, RI, VT...) | Mostly yes; some only on request/after interview |
| DE | Scheduled 2027-09-26 |
| Ontario, BC | Not verified (searched not; BC and Ontario known to require ranges from background knowledge - confirm) |
| EU Directive | Deadline 2026-06-07 missed by most; only IT, SK, LT, MT transposed as of ~Jun 30 2026 |
- Remote postings visible in covered states generally trigger those laws.
Sources: https://www.seyfarth.com/dir_docs/documents/50-state-guides/2026-Pay-Transparency-Wage-Range-Disclosure-Compendium.pdf , https://www.cooley.com/news/insight/2026/2026-07-06-show-me-the-money-or-the-wage-range-new-state-pay-transparency-laws , https://www.foley.com/insights/publications/2026/05/trends-of-pay-transparency-laws-and-salary-history-bans-continue-to-grow-new-laws-enacted-in-virginia-maine-and-delaware/ , https://www.morganlewis.com/pubs/2026/06/eu-pay-transparency-directive-the-deadline-for-transposition-has-passed-what-now , https://wageindicator.org/ai/work/collective-bargaining-agreement/updates/2026/eu-sources-just-four-member-states-have-transposed-the-pay-transparency-directive-june-30-2026/

## 4. UX (from general practice, not sourced)
- Hard-require only when law requires; else friction raises abandonment and fake ranges (0-999999), which are non-compliant (good-faith standard).
- Soft nudge with benefit stat; allow "skip"; don't block generation.

## Recommended UI
1. Field "Pay range (min/max, currency, period)" optional, labelled "Recommended".
2. Helper text: "~44-60% of candidates say they skip jobs without pay (Monster/Patriot 2026)".
3. If location matches covered jurisdiction (US states/NYC list, Ontario, BC, EU countries once transposed) or remote: show inline notice "Pay range required by law in X"; make field required for export/copy, not for generating draft.
4. If left blank elsewhere: generate draft with no invented numbers; show dismissible banner after generation.
5. Validate min<=max, warn on very wide range (>~50% spread).
6. Never auto-fill pay with AI guess.
7. Disclaimer: not legal advice.
