"""Rule-based quality linter for job descriptions.

Pure functions, no network or LLM calls, so it is cheap to run on every
draft and easy to unit test. Public entry point: `lint_job_description`.
"""

import re
from typing import Literal

from pydantic import BaseModel, Field

from src.quality import wordlists

Severity = Literal["error", "warning", "info"]

MAX_BULLETS = 8
MIN_REQUIREMENTS = 3
WORD_COUNT_SHORT = 250
WORD_COUNT_LONG = 1200
READING_GRADE_MAX = 14.0
NARROW_RANGE_RATIO = 1.1
WIDE_RANGE_RATIO = 2.0
ENTRY_TITLES = ("junior", "entry", "intern", "graduate", "associate", "trainee")
LIST_SECTIONS = ("responsibilities", "requirements", "nice_to_haves", "benefits")
PENALTY = {"error": 15, "warning": 7, "info": 2}
SEVERITY_ORDER = {"error": 0, "warning": 1, "info": 2}
STOP_WORDS = {
    "and", "the", "with", "for", "of", "in", "to", "a", "an", "or",
    "experience", "skills", "strong", "ability", "work", "working",
    "knowledge", "years",
}


class Finding(BaseModel):
    """One issue found in a draft.

    Attributes:
        code: Stable machine-readable id (used by tests and the UI).
        severity: "error", "warning" or "info".
        section: Draft section the issue relates to, or "general".
        message: Short human-readable explanation.
        suggestion: What to do about it.
        matches: Offending words or phrases, if any.
    """

    code: str
    severity: Severity
    section: str = "general"
    message: str
    suggestion: str = ""
    matches: list[str] = Field(default_factory=list)


class QualityReport(BaseModel):
    """Result of linting a draft.

    Attributes:
        score: 0-100 quality score (higher is better).
        findings: Issues, most severe first.
        stats: Word count, reading grade and bullet counts.
    """

    score: int
    findings: list[Finding]
    stats: dict[str, float | int]


def _wordlist_regex(entries: tuple[str, ...]) -> re.Pattern:
    """Compiles word-list entries (`*` = prefix wildcard) into one regex."""
    parts = []
    for entry in entries:
        escaped = re.escape(entry.rstrip("*"))
        parts.append(escaped + (r"\w*" if entry.endswith("*") else r"\b"))
    return re.compile(r"\b(?:" + "|".join(parts) + ")", re.IGNORECASE)


MASCULINE_RE = _wordlist_regex(wordlists.MASCULINE_CODED)
FEMININE_RE = _wordlist_regex(wordlists.FEMININE_CODED)


def _phrase_matches(text: str, phrases: tuple[str, ...]) -> list[str]:
    """Returns the phrases found in the text, in list order."""
    lowered = text.lower()
    found = []
    for phrase in phrases:
        suffix = r"\b" if phrase[-1].isalnum() else ""
        if re.search(r"\b" + re.escape(phrase) + suffix, lowered):
            found.append(phrase)
    return found


def count_syllables(word: str) -> int:
    """Estimates the syllables in an English word (vowel-group heuristic)."""
    word = re.sub(r"[^a-z]", "", word.lower())
    if not word:
        return 0
    count = len(re.findall(r"[aeiouy]+", word))
    if word.endswith("e") and not word.endswith(("le", "ee")) and count > 1:
        count -= 1
    return max(count, 1)


def reading_grade(text: str) -> float:
    """Flesch-Kincaid grade level of a text (0.0 for empty text)."""
    sentences = [s for s in re.split(r"[.!?]+|\n", text) if s.strip()]
    words = re.findall(r"[A-Za-z][A-Za-z'-]*", text)
    if not sentences or not words:
        return 0.0
    syllables = sum(count_syllables(word) for word in words)
    grade = 0.39 * (len(words) / len(sentences)) + 11.8 * (syllables / len(words)) - 15.59
    return round(max(grade, 0.0), 1)


def _draft_text(draft: dict) -> str:
    """Flattens a draft (body only, no title) into one string."""
    parts = [draft.get("about_company", ""), draft.get("about_role", ""), draft.get("why_join_us", "")]
    for section in LIST_SECTIONS:
        parts.extend(draft.get(section) or [])
    return "\n".join(part for part in parts if part)


def _pay_findings(draft: dict, job_info: dict, pay_required: bool) -> list[Finding]:
    """Checks that pay information is present and sensible."""
    pay_min = job_info.get("pay_min")
    pay_max = job_info.get("pay_max")
    benefits_text = " ".join(draft.get("benefits") or []).lower()
    has_pay = bool(pay_min and pay_max) or any(m in benefits_text for m in wordlists.PAY_MARKERS)
    findings: list[Finding] = []

    if not has_pay:
        reason = "Your location requires one." if pay_required else "Ads with pay get more applicants."
        findings.append(Finding(
            code="pay_missing",
            severity="error" if pay_required else "warning",
            section="benefits",
            message=f"No pay range found. {reason}",
            suggestion="Add a minimum and maximum pay in the pay range fields.",
        ))
    if pay_min and pay_max:
        if pay_min > pay_max:
            findings.append(Finding(
                code="pay_min_gt_max", severity="error", section="benefits",
                message="Minimum pay is higher than maximum pay.",
                suggestion="Swap or correct the two values.",
            ))
        elif pay_min > 0:
            ratio = pay_max / pay_min
            if ratio > WIDE_RANGE_RATIO:
                findings.append(Finding(
                    code="pay_range_wide", severity="warning", section="benefits",
                    message=f"Pay range is very wide (max is {ratio:.1f}x min). Wide ranges can breach good-faith rules.",
                    suggestion="Narrow the range to what you would really pay.",
                ))
            elif ratio < NARROW_RANGE_RATIO:
                findings.append(Finding(
                    code="pay_range_narrow", severity="info", section="benefits",
                    message="Pay range is very narrow.",
                    suggestion="Some room (10-20%) is normal.",
                ))
    return findings


def _tokens(text: str) -> set[str]:
    """Meaningful lower-case tokens of a text."""
    return set(re.findall(r"[a-z0-9+#.]{3,}", text.lower())) - STOP_WORDS


def untraceable_requirements(draft: dict, job_info: dict) -> list[str]:
    """Finds requirement bullets sharing no meaningful word with user input.

    Only runs when the user supplied requirements, so uploads and sparse
    forms do not produce noise.
    """
    user_items = job_info.get("requirements") or []
    if not user_items:
        return []
    user_tokens = set().union(*(_tokens(item) for item in user_items))
    flagged = []
    for bullet in draft.get("requirements") or []:
        bullet_tokens = _tokens(bullet)
        if bullet_tokens and not (bullet_tokens & user_tokens):
            flagged.append(bullet)
    return flagged


def _bias_findings(body: str) -> list[Finding]:
    """Checks age-coded, exclusionary, filler and gender-coded wording."""
    findings: list[Finding] = []
    age_hits = _phrase_matches(body, wordlists.AGE_CODED_PHRASES)
    if age_hits:
        findings.append(Finding(
            code="age_coded", severity="warning",
            message="Age-coded wording can put off older applicants.",
            suggestion="Describe skills, not age or career stage.", matches=age_hits,
        ))
    exclusion_hits = _phrase_matches(body, wordlists.EXCLUSIONARY_PHRASES)
    if exclusion_hits:
        findings.append(Finding(
            code="exclusionary", severity="warning",
            message="Wording may exclude some candidates.",
            suggestion="Use neutral wording (e.g. 'salesperson', 'chair').", matches=exclusion_hits,
        ))
    filler_hits = _phrase_matches(body, wordlists.FILLER_PHRASES)
    if filler_hits:
        findings.append(Finding(
            code="filler", severity="info",
            message="Cliches and hype words add noise.",
            suggestion="Replace with concrete details.", matches=filler_hits,
        ))

    masculine_matches = MASCULINE_RE.findall(body)
    feminine_matches = FEMININE_RE.findall(body)
    masculine_count, feminine_count = len(masculine_matches), len(feminine_matches)
    if masculine_count >= 3 and masculine_count >= 2 * max(feminine_count, 1):
        findings.append(Finding(
            code="gender_masculine", severity="info",
            message="Wording leans masculine-coded (Gaucher 2011). It can lower applications from women.",
            suggestion="Balance with collaborative language where it is true.",
            matches=sorted({m.lower() for m in masculine_matches})[:8],
        ))
    elif feminine_count >= 3 and feminine_count >= 2 * max(masculine_count, 1):
        findings.append(Finding(
            code="gender_feminine", severity="info",
            message="Wording leans feminine-coded (Gaucher 2011).",
            suggestion="Balance if it does not reflect the role.",
            matches=sorted({m.lower() for m in feminine_matches})[:8],
        ))
    return findings


def _requirement_findings(draft: dict, job_info: dict) -> list[Finding]:
    """Checks structure and fairness of the requirement bullets."""
    findings: list[Finding] = []
    requirements = draft.get("requirements") or []
    requirements_text = " ".join(requirements).lower()
    title = (draft.get("title") or "").lower()

    years = [int(y) for y in re.findall(r"(\d+)\+?\s*(?:years|yrs)", requirements_text)]
    if years and any(t in title for t in ENTRY_TITLES) and max(years) >= 3:
        findings.append(Finding(
            code="entry_level_experience", severity="warning", section="requirements",
            message=f"Entry-level title asks for {max(years)}+ years of experience.",
            suggestion="Lower the years or change the title.",
        ))
    wants_degree = re.search(r"\b(bachelor|master|degree|phd)", requirements_text)
    allows_equivalent = re.search(r"or equivalent|or related|equivalent (experience|work)|or similar", requirements_text)
    if wants_degree and not allows_equivalent:
        findings.append(Finding(
            code="degree_required", severity="info", section="requirements",
            message="Degree required with no 'or equivalent experience'.",
            suggestion="Add 'or equivalent experience' to widen your pool.",
        ))

    seen: set[str] = set()
    duplicates = []
    for item in requirements + (draft.get("nice_to_haves") or []):
        key = re.sub(r"\W+", " ", item.lower()).strip()
        if key in seen:
            duplicates.append(item[:60])
        seen.add(key)
    if duplicates:
        findings.append(Finding(
            code="duplicate_items", severity="warning", section="requirements",
            message="Duplicate requirement bullets.", suggestion="Remove repeats.", matches=duplicates,
        ))

    unverified = untraceable_requirements(draft, job_info)
    if unverified:
        findings.append(Finding(
            code="unverified_requirements", severity="info", section="requirements",
            message="Some requirements are not from your answers. Please verify them.",
            suggestion="Remove anything you did not ask for.", matches=unverified[:5],
        ))
    return findings


def _structure_findings(draft: dict, word_count: int, grade: float) -> list[Finding]:
    """Checks required sections, bullet caps, length and readability."""
    findings: list[Finding] = []
    for section, label in (("responsibilities", "Responsibilities"), ("requirements", "Requirements")):
        count = len(draft.get(section) or [])
        if count == 0:
            findings.append(Finding(
                code=f"missing_{section}", severity="warning", section=section,
                message=f"{label} section is empty.",
                suggestion=f"Add {label.lower()} so candidates know what to expect.",
            ))
        elif count > MAX_BULLETS:
            findings.append(Finding(
                code=f"too_many_{section}", severity="warning", section=section,
                message=f"{count} bullets in {label.lower()}. Long lists lower applications.",
                suggestion=f"Keep it to {MAX_BULLETS} or fewer; move extras to nice-to-have.",
            ))
        elif section == "requirements" and count < MIN_REQUIREMENTS:
            findings.append(Finding(
                code="few_requirements", severity="info", section=section,
                message="Very few requirements listed.", suggestion="Add the 3-6 that really matter.",
            ))
    if not (draft.get("why_join_us") or "").strip():
        findings.append(Finding(
            code="missing_why_join", severity="info", section="why_join_us",
            message="No 'Why join us' section. Recruiters say this is the most common gap.",
            suggestion="Add mission, team, growth or impact.",
        ))
    if not (draft.get("equal_opportunity") or "").strip():
        findings.append(Finding(
            code="no_eeo", severity="info", section="equal_opportunity",
            message="No equal opportunity statement.", suggestion="Add one if your company has it.",
        ))
    if word_count < WORD_COUNT_SHORT:
        findings.append(Finding(
            code="too_short", severity="info",
            message=f"Only {word_count} words. Short ads can feel vague.", suggestion="Add role detail.",
        ))
    elif word_count > WORD_COUNT_LONG:
        findings.append(Finding(
            code="too_long", severity="warning",
            message=f"{word_count} words is long for a job post.", suggestion="Trim to under 900 words.",
        ))
    if grade > READING_GRADE_MAX:
        findings.append(Finding(
            code="hard_to_read", severity="info",
            message=f"Reading level is grade {grade}. Aim for 10-12 so more people finish reading.",
            suggestion="Use shorter sentences and plain words.",
        ))
    return findings


def lint_job_description(
    draft: dict,
    job_info: dict | None = None,
    pay_required: bool = False,
) -> QualityReport:
    """Checks a draft against rule-based quality, bias and pay rules.

    Args:
        draft: Draft as a dict (`JobDescriptionDraft.model_dump()`).
        job_info: Intake answers (used for pay range and traceability).
        pay_required: Whether the user's location legally requires pay.

    Returns:
        A report with a 0-100 score, findings and simple statistics.
    """
    job_info = job_info or {}
    body = _draft_text(draft)
    word_count = len(re.findall(r"\w+", body))
    grade = reading_grade(body)

    findings = (
        _structure_findings(draft, word_count, grade)
        + _pay_findings(draft, job_info, pay_required)
        + _bias_findings(body)
        + _requirement_findings(draft, job_info)
    )
    findings.sort(key=lambda finding: SEVERITY_ORDER[finding.severity])
    penalty = sum(PENALTY[finding.severity] for finding in findings)
    stats = {
        "word_count": word_count,
        "reading_grade": grade,
        "responsibilities": len(draft.get("responsibilities") or []),
        "requirements": len(draft.get("requirements") or []),
    }
    return QualityReport(score=max(0, 100 - penalty), findings=findings, stats=stats)
