from src.database.supabase_client import supabase

def signup_user (email: str, password: str):
    "This function is for user to register a new account"
    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password
        }
    )
    #in case there's no response from the system
    if not response.user: 
        raise ValueError("Signup Process is failed")

    #Create a new row in the profile table
    supabase.table("profiles") .insert ({
        "id": response.user.id,
        "email": email
    }).execute()

    return response

#This function is for users to login into their account
def login_user (email: str, password: str):
    "Login into a user's existiing account"
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    # In case the system doesn't response with the request to login
    if not response.user or not response.session:
        raise ValueError("The login process fails")
    return response 