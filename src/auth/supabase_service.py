from src.database.supabase_client import supabase
from src.database.supabase_credits import get_supabase_credits

def signup_user(email: str, password: str, username: str):
    "This function is for user to register a new account"
    # Check if email is already registered
    email_check = supabase.table("profiles").select("*").eq("email", email).execute()
    if email_check.data:
        raise ValueError("Email is already registered")

    # Check if username is already taken
    username_check = supabase.table("profiles").select("id").eq("username", username).execute()
    if username_check.data:
        raise ValueError("Username is already taken")

    response = supabase.auth.sign_up(
        {
            "email": email,
            "password": password,
            "options": {
                "data": {
                    "username": username
                }
            }
        }
    )
    #in case there's no response from the system
    if not response.user: 
        raise ValueError("Signup Process is failed")
    
    #Return status info. Profile row will be created once OTP has been verified
    return {
        "status": "pending_verification",
        "email": email,
        "message": "Verification code has been sent to your email",
    }

def verify_user_otp(email: str, token: str):
    #Verify if the 6-digit otp token is created
    response = supabase.auth.verify_otp({
        "email": email,
        "token": token,
        "type": "signup",
    })
    #Check if the system doesn't response with the session or user's account
    if not response.user or not response.session:
        raise ValueError("Invalid or expired verification code")
    user_id = response.user.id
    metadata_username = response.user.user_metadata.get("username") if response.user.user_metadata else None
    profile_check = supabase.table("profiles").select("*").eq("id", user_id).execute()

    # if that user's account doesn't exist
    if not profile_check.data:
        supabase.table("profiles").insert({
            "id": user_id,
            "email": email,
            "username": metadata_username,
        }).execute()
        current_username = metadata_username
    else:
        current_username = profile_check.data[0].get("username") or metadata_username

    credits = get_supabase_credits(user_id)
    return {
        "access_token": response.session.access_token,
        "user": {
            "id": user_id,
            "email": response.user.email,
            "username": current_username
        },
        "credits": credits,
    }
    

# This function is to return the acconut of the user's profile
def get_current_user_profile (token: str):
    response = supabase.auth.get_user(token)
    if not response.user:
        raise ValueError("Invalid or expired session")
    user_id = response.user.id
    profile_check = supabase.table("profiles").select("username").eq("id", user_id).execute()
    username = None
    if profile_check.data and profile_check.data[0].get("username"):
        username = profile_check.data[0]["username"]
    elif response.user.user_metadata:
        username = response.user.user_metadata.get("username")

    credits = get_supabase_credits(user_id)

    return {
        "access_token": token,
        "user": {
            "id": user_id,
            "email": response.user.email,
            "username": username
        },
        "credits": credits
    }

#This function is for users to login into their account
def login_user (email: str, password: str):
    #Login into a user's existiing account
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })

    # In case the system doesn't response with the request to login
    if not response.user or not response.session:
        raise ValueError("The login process fails")

    user_id = response.user.id
    profile_check = supabase.table("profiles").select("username").eq("id", user_id).execute()
    username = None
    if profile_check.data and profile_check.data[0].get("username"):
        username = profile_check.data[0]["username"]
    elif response.user.user_metadata:
        username = response.user.user_metadata.get("username")

    credits = get_supabase_credits(user_id)

    return {
        "access_token": response.session.access_token,
        "user": {
            "id": user_id,
            "email": response.user.email,
            "username": username
        },
        "credits": credits
    }

# THis functino is to send the OTP to email in order to reset password
def request_password_reset(email: str):
    response = supabase.auth.reset_password_email(email)
    return {
        "status": "success",
        "message": "Password reset code sent."
    }

#This function is to confirm that the password has been reseted
def confirm_password_reset (email: str, token: str, new_password: str):
    try:
        # Check if the password is already correct
        signin_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": new_password
        })
        if signin_response.user and signin_response.session:
            credits = get_supabase_credits(signin_response.user.id)
            return {
                "access_token": signin_response.session.access_token,
                "user": {
                    "id": signin_response.user.id,
                    "email": signin_response.user.email,
                    "username": signin_response.user.user_metadata.get("username") if signin_response.user.user_metadata else None
                },
                "credits": credits,
            }
    except Exception:
        pass

    verify_response = supabase.auth.verify_otp({
        "email": email,
        "token": token,
        "type": "recovery",
    })

    #This is to check if the system rejects the sessin or the token
    if not verify_response.user or not verify_response.session:
        raise ValueError("Invalid or expired reset code")

    #update the new password if the token is valid
    update_response = supabase.auth.update_user({
        "password": new_password
    })

    #if update fails
    if not update_response.user:
        raise ValueError("Failed to update password!")

    credits = get_supabase_credits(verify_response.user.id)
    return {
      "access_token": verify_response.session.access_token,
      "user": {
        "id": verify_response.user.id,
        "email": verify_response.user.email,
        "username": verify_response.user.user_metadata.get("username") if verify_response.user.user_metadata else None
      },
      "credits": credits,
    }

def change_supabase_username(token: str, new_username: str):
    from supabase import create_client
    import os
    
    # 1. Initialize temporary client
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_ANON_KEY")
    client = create_client(url, key)
    
    # 2. Populate the active session on the client
    client.auth.set_session(access_token=token, refresh_token=token)
    
    # 3. Update Auth user metadata
    client.auth.update_user({
        "data": {
            "username": new_username
        }
    })
    
    # 4. Update profiles table
    client.postgrest.auth(token)
    client.table("profiles").update({
        "username": new_username
    }).eq("id", client.auth.get_user(token).user.id).execute()
    
    user = client.auth.get_user(token).user
    credits = get_supabase_credits(user.id)
    return {
        "access_token": token,
        "user": {
            "id": user.id,
            "email": user.email,
            "username": new_username
        },
        "credits": credits
    }