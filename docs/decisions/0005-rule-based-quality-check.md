# 0005 - Quality check with plain rules, not a second LLM

**Context.** Users want to know if a draft has biased wording, a missing pay
range or too many bullets. A second LLM call could judge this, but it costs
money, adds latency and gives different answers for the same draft.

**Options.**
1. LLM review of each draft.
2. Deterministic rules: published word lists (gender-coded words from Gaucher,
   Friesen and Kay, 2011; age-coded phrases), pay-range rules, bullet caps and
   reading level.

**Decision.** Option 2, in `src/quality`, with no network or LLM dependency.

**Consequences.** Free, instant and repeatable: the same draft always gets the
same result. It cannot catch subtle problems a human would. It is presented as a
screening aid, not proof of bias or legal advice.
