from src.database.supabase_client import supabase

# This function is to deduct 1 credit from users any time they 'generate' or 'refine'
def deduct_supabase_credits (user_id: str):
    result= supabase.table ("profiles").select("credits").eq ("id", user_id).execute()
    # incase the database is empty
    if not result.data:
        return False
    current_credits = result.data[0]["credits"]

    # if the user doesn't have any credits, there's no point deducting
    if current_credits <= 0:
        return False

    # minus one credit and update the database
    supabase.table ("profiles").update ({
        "credits": current_credits - 1
    }).eq("id", user_id).execute()

    return True

#This function is to fetch a user's credits from the database
def get_supabase_credits(user_id: str):
    result = supabase.table("profiles").select("credits").eq("id", user_id).execute()

    # In case the user's profile doesn't exist
    if not result.data:
        return 0

    return result.data[0]["credits"]

#This function is to add more credits to the user's account
def add_supabase_credits(user_id: str, amount: int):
    result = supabase.table("profiles").select("credits").eq("id", user_id).execute()
    if result.data:
        current_credits = result.data[0]["credits"]
        supabase.table ("profiles").update ({
            "credits": current_credits + amount
        }).eq("id", user_id).execute()

    
    