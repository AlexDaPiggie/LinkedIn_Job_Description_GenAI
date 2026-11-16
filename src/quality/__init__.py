"""Rule-based quality checks for job descriptions (no LLM calls)."""

from src.quality.linter import Finding, QualityReport, lint_job_description

__all__ = ["Finding", "QualityReport", "lint_job_description"]
