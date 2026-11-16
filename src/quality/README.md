# quality - rule-based job description linter

Checks a job description draft with plain rules. No network, no LLM, no
dependency on the rest of this app apart from `pydantic`. Copy the `quality/`
folder into any Python project to reuse it.

```python
from src.quality import lint_job_description

report = lint_job_description(
    draft={"title": "Data Analyst", "responsibilities": [...], "requirements": [...], "benefits": [...]},
    job_info={"pay_min": 80000, "pay_max": 100000},
    pay_required=True,  # for example California or New York City
)
print(report.score)          # 0-100
for finding in report.findings:
    print(finding.severity, finding.code, finding.message)
```

## What it checks

- Missing sections (responsibilities, requirements, why join, equal opportunity)
- Bullet caps (over 8 responsibilities or requirements) and duplicates
- Pay range present, min not above max, range not too wide or narrow
- Gender-coded words (Gaucher, Friesen and Kay, 2011), age-coded phrases, hype words, exclusionary terms
- Entry-level title asking for 3+ years, degree required without "or equivalent"
- Requirements that share no words with what the user supplied ("verify" flags)
- Length and reading grade (Flesch-Kincaid)

`jurisdictions.py` lists places that generally require a pay range in the ad.
It is a screening aid, not legal advice. Word lists in `wordlists.py` are
short and editable; tune them for your own hiring context.

## Tests

`python -m pytest tests/test_quality_linter.py`
