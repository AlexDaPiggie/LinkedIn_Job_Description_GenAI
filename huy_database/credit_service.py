from datetime import date

from src.auth.supabase_auth import INITIAL_FREE_CREDIT_ALLOWANCE, MONTHLY_CREDIT_ALLOWANCE, get_supabase


def _next_month(value: date) -> date:
    month = value.month + 1
    year = value.year
    if month == 13:
        month = 1
        year += 1

    days_in_month = [31, 29 if year % 4 == 0 and (year % 100 != 0 or year % 400 == 0) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(value.day, days_in_month[month - 1])
    return date(year, month, day)


def _account_data(response):
    data = getattr(response, "data", None)
    if isinstance(data, list):
        return data[0] if data else None
    return data


def _int_value(account, key: str, fallback: int = 0) -> int:
    value = account.get(key) if isinstance(account, dict) else None
    if value is None:
        return fallback
    return int(value)


def credit_totals(account):
    free_balance = _int_value(account, "free_balance", _int_value(account, "balance", 0))
    paid_balance = _int_value(account, "paid_balance", 0)
    return {
        "free_balance": free_balance,
        "paid_balance": paid_balance,
        "balance": free_balance + paid_balance,
    }


def ensure_profile(user_id: str, username: str, email: str):
    client = get_supabase()
    existing = client.table("profiles").select("*").eq("id", user_id).limit(1).execute()
    if _account_data(existing):
        return _account_data(existing)

    created = client.table("profiles").insert({
        "id": user_id,
        "username": username,
        "email": email,
    }).execute()
    return _account_data(created)


def ensure_credit_account(user_id: str):
    client = get_supabase()
    today = date.today()
    existing = client.table("credit_accounts").select("*").eq("user_id", user_id).limit(1).execute()
    account = _account_data(existing)

    if not account:
        created = client.table("credit_accounts").insert({
            "user_id": user_id,
            "free_balance": INITIAL_FREE_CREDIT_ALLOWANCE,
            "paid_balance": 0,
            "balance": INITIAL_FREE_CREDIT_ALLOWANCE,
            "monthly_allowance": MONTHLY_CREDIT_ALLOWANCE,
            "monthly_free_allowance": MONTHLY_CREDIT_ALLOWANCE,
            "current_period_start": today.isoformat(),
            "current_period_end": _next_month(today).isoformat(),
        }).execute()
        return _account_data(created)

    period_end = date.fromisoformat(str(account["current_period_end"])[:10])
    if today >= period_end:
        paid_balance = _int_value(account, "paid_balance", 0)
        refreshed_free_balance = MONTHLY_CREDIT_ALLOWANCE
        refreshed = client.table("credit_accounts").update({
            "free_balance": refreshed_free_balance,
            "paid_balance": paid_balance,
            "balance": refreshed_free_balance + paid_balance,
            "monthly_allowance": MONTHLY_CREDIT_ALLOWANCE,
            "monthly_free_allowance": MONTHLY_CREDIT_ALLOWANCE,
            "current_period_start": today.isoformat(),
            "current_period_end": _next_month(today).isoformat(),
        }).eq("user_id", user_id).execute()
        return _account_data(refreshed)

    return account


def require_available_credit(user_id: str):
    account = ensure_credit_account(user_id)
    if credit_totals(account)["balance"] < 1:
        raise ValueError("You do not have enough credits. Your free credits refresh next month.")
    return account


def spend_credit(user_id: str, reason: str):
    client = get_supabase()
    account = require_available_credit(user_id)
    totals = credit_totals(account)
    free_balance = totals["free_balance"]
    paid_balance = totals["paid_balance"]
    credit_type = "free"

    if free_balance > 0:
        free_balance -= 1
    else:
        paid_balance -= 1
        credit_type = "paid"

    new_balance = free_balance + paid_balance

    updated = client.table("credit_accounts").update({
        "free_balance": free_balance,
        "paid_balance": paid_balance,
        "balance": new_balance,
    }).eq("user_id", user_id).execute()
    account = _account_data(updated)

    client.table("credit_transactions").insert({
        "user_id": user_id,
        "amount": -1,
        "reason": reason,
        "credit_type": credit_type,
        "balance_after": new_balance,
    }).execute()

    return account

def record_generation(user_id: str, action_type: str, result_text: str):
    get_supabase().table("generation_history").insert({
        "user_id": user_id,
        "action_type": action_type,
        "result_text": result_text,
        "credits_used": 1,
    }).execute()
