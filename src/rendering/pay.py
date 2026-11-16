"""Formatting of the pay range shown in a job description."""

from src.schema.job_info import JobInfo

CURRENCY_SYMBOLS = {"USD": "$", "CAD": "CA$", "EUR": "EUR ", "GBP": "GBP "}
PERIOD_LABELS = {"year": "per year", "month": "per month", "hour": "per hour"}


def format_pay_range(job_info: JobInfo) -> str:
    """Builds the pay-range sentence from the user's own numbers.

    The text is built in code, never by the LLM, so figures cannot be
    invented or altered.

    Args:
        job_info: Intake answers with `pay_min` and `pay_max`.

    Returns:
        Text such as "$90,000 - $120,000 per year", or "" if either end of
        the range is missing or the range is reversed.
    """
    low, high = job_info.pay_min, job_info.pay_max
    if not low or not high or low > high:
        return ""
    symbol = CURRENCY_SYMBOLS.get(job_info.pay_currency.upper(), f"{job_info.pay_currency.upper()} ")
    period = PERIOD_LABELS.get(job_info.pay_period, "per year")
    return f"{symbol}{low:,.0f} - {symbol}{high:,.0f} {period}"
