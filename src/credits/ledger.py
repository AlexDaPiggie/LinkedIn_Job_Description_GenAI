"""Atomic, idempotent credit operations backed by Supabase RPC functions.

The functions live in `docs/migrations/001_credit_ledger.sql`. If they are
not installed, every call fails closed with `LedgerNotInstalled` instead of
falling back to a read-then-write path, which could double-credit on a
retried webhook or charge unevenly under concurrent requests.
"""

import uuid

from src.database.supabase_client import get_service_client

INSUFFICIENT = -1


class LedgerNotInstalled(RuntimeError):
    """Raised when the credit SQL functions have not been installed."""


def _rpc(name: str, params: dict):
    """Calls a Supabase RPC function and returns its data.

    Raises:
        LedgerNotInstalled: If the function does not exist in the database.
    """
    try:
        return get_service_client().rpc(name, params).execute().data
    except Exception as error:
        text = str(error).lower()
        if "pgrst202" in text or "could not find the function" in text or "does not exist" in text:
            raise LedgerNotInstalled(
                f"{name} is missing. Run docs/migrations/001_credit_ledger.sql in Supabase."
            ) from error
        raise


def new_request_key() -> str:
    """Creates a unique idempotency key for one billable request."""
    return uuid.uuid4().hex


def spend(user_id: str, cost: int, key: str) -> int:
    """Spends credits atomically.

    Args:
        user_id: ID of the user.
        cost: Credits to spend.
        key: Idempotency key; repeating it does not charge twice.

    Returns:
        The new balance, or `INSUFFICIENT` (-1) if the user cannot pay.
    """
    return int(_rpc("spend_credits", {"p_user": user_id, "p_cost": cost, "p_key": key}))


def refund(user_id: str, amount: int, key: str) -> int:
    """Gives back credits spent under `key` (once). Returns the new balance."""
    return int(_rpc("refund_credits", {"p_user": user_id, "p_amount": amount, "p_key": key}))


def grant(user_id: str, amount: int, key: str, reason: str) -> int:
    """Adds credits once per key. Returns the new balance."""
    return int(_rpc("grant_credits", {"p_user": user_id, "p_amount": amount, "p_key": key, "p_reason": reason}))


def claim_stripe_event(event_id: str) -> bool:
    """Records a Stripe event id. Returns False if it was already handled."""
    return bool(_rpc("claim_stripe_event", {"p_event_id": event_id}))


def claim_free_grant(user_id: str, email_normalized: str, amount: int) -> int:
    """Gives the signup grant once per normalized email.

    Returns:
        Credits granted (0 if this email already received a grant).
    """
    return int(
        _rpc(
            "claim_free_grant",
            {"p_user": user_id, "p_email_normalized": email_normalized, "p_amount": amount},
        )
    )
