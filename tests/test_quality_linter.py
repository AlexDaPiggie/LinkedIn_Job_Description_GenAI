"""Tests for the rule-based quality linter and pay helpers."""

from src.quality import lint_job_description
from src.quality.jurisdictions import get_jurisdiction, pay_required_for
from src.quality.linter import count_syllables, reading_grade, untraceable_requirements
from src.rendering.pay import format_pay_range
from src.schema.job_info import JobInfo

GOOD_DRAFT = {
    "title": "Data Analyst",
    "about_company": "Acme builds tools that help small shops understand their sales.",
    "about_role": " ".join(["You will turn sales data into clear answers for the team."] * 25),
    "responsibilities": ["Build weekly sales reports.", "Clean data from three sources.", "Present findings to managers."],
    "requirements": ["SQL and Excel skills.", "Clear writing.", "Two years of analysis work or equivalent experience."],
    "nice_to_haves": ["Python."],
    "benefits": ["Health cover.", "25 days leave."],
    "why_join_us": "Small team, big impact, and room to grow.",
    "equal_opportunity": "We welcome everyone.",
}


def codes(report):
    return {finding.code for finding in report.findings}


def test_clean_draft_has_high_score_and_no_errors():
    report = lint_job_description(GOOD_DRAFT, {"pay_min": 80000, "pay_max": 100000})
    assert report.score >= 80
    assert not [f for f in report.findings if f.severity == "error"]


def test_missing_pay_is_warning_normally_and_error_when_required():
    soft = lint_job_description(GOOD_DRAFT, {}, pay_required=False)
    hard = lint_job_description(GOOD_DRAFT, {}, pay_required=True)
    assert next(f for f in soft.findings if f.code == "pay_missing").severity == "warning"
    assert next(f for f in hard.findings if f.code == "pay_missing").severity == "error"


def test_pay_range_checks():
    assert "pay_min_gt_max" in codes(lint_job_description(GOOD_DRAFT, {"pay_min": 100, "pay_max": 50}))
    assert "pay_range_wide" in codes(lint_job_description(GOOD_DRAFT, {"pay_min": 10, "pay_max": 90}))
    assert "pay_range_narrow" in codes(lint_job_description(GOOD_DRAFT, {"pay_min": 100, "pay_max": 101}))
    assert "pay_missing" not in codes(lint_job_description(GOOD_DRAFT, {"pay_min": 50, "pay_max": 60}))


def test_pay_in_benefits_text_counts_as_pay():
    draft = {**GOOD_DRAFT, "benefits": ["Salary of $90,000 to $110,000."]}
    assert "pay_missing" not in codes(lint_job_description(draft, {}))


def test_age_coded_and_filler_and_exclusionary_words():
    draft = {**GOOD_DRAFT, "about_role": "We want a digital native rockstar who is a culture fit. " * 3}
    found = codes(lint_job_description(draft, {}))
    assert {"age_coded", "filler", "exclusionary"} <= found


def test_masculine_coded_imbalance_flagged():
    draft = {**GOOD_DRAFT, "about_role": "Aggressive, competitive, dominant leaders who are ambitious and fearless."}
    assert "gender_masculine" in codes(lint_job_description(draft, {}))


def test_bullet_caps_and_duplicates():
    draft = {**GOOD_DRAFT, "responsibilities": [f"Task number {i} for the team." for i in range(12)]}
    assert "too_many_responsibilities" in codes(lint_job_description(draft, {}))
    dup = {**GOOD_DRAFT, "requirements": ["SQL skills.", "sql skills", "Clear writing."]}
    assert "duplicate_items" in codes(lint_job_description(dup, {}))


def test_entry_level_title_with_many_years():
    draft = {**GOOD_DRAFT, "title": "Junior Analyst", "requirements": ["5+ years of analysis.", "SQL.", "Excel."]}
    assert "entry_level_experience" in codes(lint_job_description(draft, {}))


def test_degree_without_equivalent_flagged():
    draft = {**GOOD_DRAFT, "requirements": ["Bachelor degree in statistics.", "SQL.", "Excel."]}
    assert "degree_required" in codes(lint_job_description(draft, {}))
    ok = {**GOOD_DRAFT, "requirements": ["Bachelor degree or equivalent experience.", "SQL.", "Excel."]}
    assert "degree_required" not in codes(lint_job_description(ok, {}))


def test_empty_sections_reported():
    empty = {"title": "X", "about_company": "", "about_role": "", "responsibilities": [], "requirements": []}
    found = codes(lint_job_description(empty, {}))
    assert {"missing_responsibilities", "missing_requirements", "missing_why_join", "too_short"} <= found


def test_unverified_requirements_only_when_user_gave_some():
    draft = {**GOOD_DRAFT, "requirements": ["SQL and Excel skills.", "Kubernetes cluster operations."]}
    assert untraceable_requirements(draft, {"requirements": ["SQL", "Excel"]}) == ["Kubernetes cluster operations."]
    assert untraceable_requirements(draft, {}) == []


def test_findings_sorted_by_severity():
    report = lint_job_description({"title": "X"}, {}, pay_required=True)
    order = {"error": 0, "warning": 1, "info": 2}
    ranks = [order[f.severity] for f in report.findings]
    assert ranks == sorted(ranks)


def test_reading_helpers():
    assert count_syllables("table") == 2
    assert reading_grade("") == 0.0
    assert reading_grade("The cat sat. The dog ran.") < reading_grade(
        "Interdepartmental collaboration necessitates comprehensive organizational communication strategies."
    )


def test_jurisdictions():
    assert pay_required_for("US-CA")
    assert pay_required_for("EU")
    assert not pay_required_for("none")
    assert get_jurisdiction("nonsense").code == "none"


def test_format_pay_range():
    info = JobInfo(pay_min=90000, pay_max=120000)
    assert format_pay_range(info) == "$90,000 - $120,000 per year"
    assert format_pay_range(JobInfo(pay_min=25, pay_max=40, pay_period="hour")) == "$25 - $40 per hour"
    assert format_pay_range(JobInfo(pay_min=100, pay_max=50)) == ""
    assert format_pay_range(JobInfo(pay_min=100)) == ""
