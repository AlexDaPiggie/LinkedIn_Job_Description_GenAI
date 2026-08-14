import os
from functools import lru_cache

from dotenv import load_dotenv
from supabase import Client, create_client


INITIAL_FREE_CREDIT_ALLOWANCE = 20
MONTHLY_CREDIT_ALLOWANCE = 5


@lru_cache
def get_supabase() -> Client:
    load_dotenv()
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY are required")
    return create_client(url, key)


def get_user_from_token(token: str):
    if not token:
        raise ValueError("Missing access token")
    response = get_supabase().auth.get_user(token)
    user = getattr(response, "user", None)
    if not user:
        raise ValueError("Invalid or expired access token")
    return user


def sign_up_user(username: str, email: str, password: str):
    response = get_supabase().auth.sign_up({
        "email": email,
        "password": password,
        "options": {
            "data": {
                "username": username,
            },
        },
    })
    user = getattr(response, "user", None)
    if not user:
        raise ValueError("Could not create account")
    return response


def sign_in_user(email: str, password: str):
    response = get_supabase().auth.sign_in_with_password({
        "email": email,
        "password": password,
    })
    user = getattr(response, "user", None)
    session = getattr(response, "session", None)
    if not user or not session:
        raise ValueError("Invalid email or password")
    return response
