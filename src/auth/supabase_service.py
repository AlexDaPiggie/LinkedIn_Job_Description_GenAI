"""Account operations backed by Supabase Auth and the `profiles` table."""

import os

from supabase import create_client

from src.database.supabase_client import get_service_client, supabase
from src.credits.ledger import claim_free_grant
from src.credits.packs import FREE_SIGNUP_CREDITS
from src.database.supabase_credits import get_supabase_credits
from src.security.emails import normalize_email

RATE_LIMIT_MARKERS = ("rate", "security purposes")


def _is_rate_limited(error_message: str) -> bool:
    """Whether a Supabase error message indicates rate limiting."""
    lowered = error_message.lower()
    return any(marker in lowered for marker in RATE_LIMIT_MARKERS)


def _build_auth_payload(
    access_token: str,
    user_id: str,
    email: str,
    username: str | None,
) -> dict:
    """Builds the session payload returned by authentication endpoints.

    Args:
        access_token: Supabase access token.
        user_id: ID of the user.
        email: Email address of the user.
        username: Display name, or None if not set.

    Returns:
        A dict matching the `AuthResponse` schema, with the current credits.
    """
    return {
        "access_token": access_token,
        "user": {
            "id": user_id,
            "email": email,
            "username": username,
        },
        "credits": get_supabase_credits(user_id),
    }


def _metadata_username(user) -> str | None:
    """Returns the username stored in a Supabase user's metadata, if any."""
    return user.user_metadata.get("username") if user.user_metadata else None


def _profiles():
    """Returns a query on `profiles` using the service-role client.

    `profiles` has row level security, so the anon client sees no rows unless
    a user session happens to be attached to the shared client. Every lookup
    here is keyed by a verified user id or by the email/username being
    registered, so server-side access is safe.
    """
    return get_service_client().table("profiles")


def _lookup_username(user) -> str | None:
    """Finds a user's username, preferring the profile row over metadata.

    Args:
        user: Supabase user object.

    Returns:
        The username, or None if neither source has one.
    """
    profile_rows = _profiles().select("username").eq("id", user.id).execute()
    if profile_rows.data and profile_rows.data[0].get("username"):
        return profile_rows.data[0]["username"]
    return _metadata_username(user)


def signup_user(email: str, password: str, username: str) -> dict:
    """Registers a new account and sends a verification code by email.

    The profile row is created later, once the code is verified.

    Args:
        email: Email address for the account.
        password: Chosen password.
        username: Chosen display name.

    Returns:
        A `SignupStatusResponse`-shaped dict with status "pending_verification".

    Raises:
        ValueError: If the email or username is taken, the request is rate
            limited, or Supabase rejects the signup.
    """
    clean_email = email.strip()
    clean_username = username.strip()

    existing_email = _profiles().select("id").eq("email", clean_email).execute()
    if existing_email.data:
        raise ValueError("Email is already registered")

    existing_username = _profiles().select("id").eq("username", clean_username).execute()
    if existing_username.data:
        raise ValueError("Username is already taken")

    try:
        response = supabase.auth.sign_up(
            {
                "email": clean_email,
                "password": password,
                "options": {"data": {"username": clean_username}},
            }
        )
    except Exception as exc:
        error_message = str(exc)
        if _is_rate_limited(error_message):
            raise ValueError("Too many attempts. Please wait a minute before trying again.")
        raise ValueError(error_message)

    if not response.user:
        raise ValueError("Signup process failed. Please try again.")

    # A previously registered but unconfirmed user comes back with empty
    # identities and Supabase does not re-send the email, so resend it here.
    identities = getattr(response.user, "identities", None)
    if identities is not None and len(identities) == 0:
        try:
            supabase.auth.resend({"type": "signup", "email": clean_email})
        except Exception:
            pass

    return {
        "status": "pending_verification",
        "email": clean_email,
        "message": "Verification code has been sent to your email",
    }


def resend_signup_otp(email: str) -> dict:
    """Re-sends the signup verification code.

    Args:
        email: Email address awaiting verification.

    Returns:
        A dict with status "success" and a message.

    Raises:
        ValueError: If the email is blank, already verified, or the request
            is rate limited.
    """
    clean_email = email.strip() if email else ""
    if not clean_email:
        raise ValueError("Email is required")

    existing_profile = _profiles().select("id").eq("email", clean_email).execute()
    if existing_profile.data:
        raise ValueError("This email is already verified. Please sign in instead.")

    try:
        supabase.auth.resend({"type": "signup", "email": clean_email})
        return {
            "status": "success",
            "message": "A new verification code has been sent to your email.",
        }
    except Exception as exc:
        error_message = str(exc)
        if _is_rate_limited(error_message):
            raise ValueError("Please wait a minute before requesting another code.")
        if "already confirmed" in error_message.lower():
            raise ValueError("This email is already verified. Please sign in instead.")
        raise ValueError(error_message)


def verify_user_otp(email: str, token: str) -> dict:
    """Confirms a signup with the emailed 6-digit code.

    Creates the profile row on first verification.

    Args:
        email: Email address that received the code.
        token: One-time code from the email.

    Returns:
        A session payload matching the `AuthResponse` schema.

    Raises:
        ValueError: If the code is invalid or expired.
    """
    response = supabase.auth.verify_otp({
        "email": email,
        "token": token,
        "type": "signup",
    })
    if not response.user or not response.session:
        raise ValueError("Invalid or expired verification code")

    user_id = response.user.id
    metadata_username = _metadata_username(response.user)
    existing_profile = _profiles().select("*").eq("id", user_id).execute()

    if not existing_profile.data:
        _profiles().insert({
            "id": user_id,
            "email": email,
            "username": metadata_username,
            "credits": 0,
        }).execute()
        # Free refine credits are given once per real mailbox, only after
        # the email was confirmed.
        try:
            claim_free_grant(user_id, normalize_email(email), FREE_SIGNUP_CREDITS)
        except Exception as error:
            # Never block signup on the grant. Fails closed, so no credits are given
            # until the migration is installed; fix it and grant manually.
            print(f"Warning: free credit grant failed for {user_id}: {error}")
        username = metadata_username
    else:
        username = existing_profile.data[0].get("username") or metadata_username

    return _build_auth_payload(response.session.access_token, user_id, response.user.email, username)


def get_current_user_profile(token: str) -> dict:
    """Returns the session payload for an existing access token.

    Args:
        token: Supabase access token.

    Returns:
        A session payload matching the `AuthResponse` schema.

    Raises:
        ValueError: If the token is invalid or expired.
    """
    try:
        response = supabase.auth.get_user(token)
    except Exception as exc:
        # Supabase raises AuthApiError for bad or expired tokens; the route
        # maps ValueError to 401 instead of a 500.
        raise ValueError("Invalid or expired session") from exc
    if not response or not response.user:
        raise ValueError("Invalid or expired session")
    return _build_auth_payload(token, response.user.id, response.user.email, _lookup_username(response.user))


def login_user(email: str, password: str) -> dict:
    """Signs in with email and password.

    Args:
        email: Account email.
        password: Account password.

    Returns:
        A session payload matching the `AuthResponse` schema.

    Raises:
        ValueError: If Supabase returns no user or session.
    """
    response = supabase.auth.sign_in_with_password({
        "email": email,
        "password": password,
    })
    if not response.user or not response.session:
        raise ValueError("The login process fails")

    return _build_auth_payload(
        response.session.access_token,
        response.user.id,
        response.user.email,
        _lookup_username(response.user),
    )


def request_password_reset(email: str) -> dict:
    """Emails a password-reset code.

    Args:
        email: Email address of the account.

    Returns:
        A dict with status "success" and a message.
    """
    supabase.auth.reset_password_email(email)
    return {
        "status": "success",
        "message": "Password reset code sent.",
    }


def confirm_password_reset(email: str, token: str, new_password: str) -> dict:
    """Sets a new password using an emailed recovery code.

    If the new password already works (for example the request was retried
    after succeeding), the user is simply signed in.

    Args:
        email: Email address of the account.
        token: One-time recovery code from the email.
        new_password: Password to set.

    Returns:
        A session payload matching the `AuthResponse` schema.

    Raises:
        ValueError: If the code is invalid or expired, or the password
            update fails.
    """
    try:
        sign_in_response = supabase.auth.sign_in_with_password({
            "email": email,
            "password": new_password,
        })
        if sign_in_response.user and sign_in_response.session:
            return _build_auth_payload(
                sign_in_response.session.access_token,
                sign_in_response.user.id,
                sign_in_response.user.email,
                _metadata_username(sign_in_response.user),
            )
    except Exception:
        pass

    verify_response = supabase.auth.verify_otp({
        "email": email,
        "token": token,
        "type": "recovery",
    })
    if not verify_response.user or not verify_response.session:
        raise ValueError("Invalid or expired reset code")

    update_response = supabase.auth.update_user({"password": new_password})
    if not update_response.user:
        raise ValueError("Failed to update password!")

    return _build_auth_payload(
        verify_response.session.access_token,
        verify_response.user.id,
        verify_response.user.email,
        _metadata_username(verify_response.user),
    )


def change_supabase_username(token: str, new_username: str) -> dict:
    """Changes a user's username in Auth metadata and the profile row.

    Uses a temporary client authenticated as the user so row-level security
    applies.

    Args:
        token: The user's access token.
        new_username: New display name.

    Returns:
        A session payload matching the `AuthResponse` schema.
    """
    user_client = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))
    user_client.auth.set_session(access_token=token, refresh_token=token)

    user_client.auth.update_user({"data": {"username": new_username}})

    user_client.postgrest.auth(token)
    user = user_client.auth.get_user(token).user
    user_client.table("profiles").update({
        "username": new_username,
    }).eq("id", user.id).execute()

    return _build_auth_payload(token, user.id, user.email, new_username)
