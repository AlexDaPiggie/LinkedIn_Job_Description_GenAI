"""Credit balance operations on the Supabase `profiles` table."""

from src.database.supabase_client import supabase


def get_supabase_credits(user_id: str) -> int:
    """Fetches a user's credit balance.

    Args:
        user_id: ID of the user.

    Returns:
        The balance, or 0 if the profile does not exist.
    """
    result = supabase.table("profiles").select("credits").eq("id", user_id).execute()
    if not result.data:
        return 0
    return result.data[0]["credits"] or 0


def deduct_supabase_credits(user_id: str) -> bool:
    """Spends one credit (called for each generate or refine).

    Args:
        user_id: ID of the user.

    Returns:
        True if a credit was deducted, False if the profile is missing or
        the balance is already zero.
    """
    result = supabase.table("profiles").select("credits").eq("id", user_id).execute()
    if not result.data:
        return False

    current_credits = result.data[0]["credits"] or 0
    if current_credits <= 0:
        return False

    supabase.table("profiles").update({
        "credits": current_credits - 1,
    }).eq("id", user_id).execute()
    return True


def add_supabase_credits(user_id: str, amount: int) -> None:
    """Adds credits to a user's balance.

    Does nothing if the profile does not exist.

    Args:
        user_id: ID of the user.
        amount: Number of credits to add.
    """
    result = supabase.table("profiles").select("credits").eq("id", user_id).execute()
    if result.data:
        current_credits = result.data[0]["credits"] or 0
        supabase.table("profiles").update({
            "credits": current_credits + amount,
        }).eq("id", user_id).execute()
