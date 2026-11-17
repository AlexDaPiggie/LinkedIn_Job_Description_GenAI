"""FastAPI dependencies for reading the signed-in user from a request."""

from fastapi import Header, HTTPException

from src.database.supabase_client import supabase

BEARER_PREFIX = "Bearer "


def extract_bearer_token(authorization: str | None) -> str | None:
    """Pulls the token out of an `Authorization: Bearer <token>` header.

    Args:
        authorization: Raw header value, or None if absent.

    Returns:
        The token, or None if the header is missing or not a bearer token.
    """
    if not authorization or not authorization.startswith(BEARER_PREFIX):
        return None

    return authorization.split(" ")[1]


def require_bearer_token(
    authorization: str | None = Header(default=None),
) -> str:
    """Dependency that requires a bearer token.

    Raises:
        HTTPException: 401 if the header is missing or malformed.
    """
    token = extract_bearer_token(authorization)
    if token is None:
        raise HTTPException(status_code=401, detail="Please sign in first")
    return token


def get_user_id_from_auth(authorization: str = Header(None)) -> str:
    """Dependency that returns the ID of the signed-in user.

    Args:
        authorization: Raw `Authorization` header.

    Returns:
        The Supabase user ID.

    Raises:
        HTTPException: 401 if the token is missing, invalid or expired.
    """
    token = extract_bearer_token(authorization)
    if token is None:
        raise HTTPException(
            status_code=401,
            detail="The token is either missing or invalid",
        )
    try:
        auth_response = supabase.auth.get_user(token)
        return auth_response.user.id
    except Exception:
        raise HTTPException(status_code=401, detail="Unauthorized")


def get_optional_user_id_from_auth(
    authorization: str | None = Header(default=None),
) -> str | None:
    """Dependency that returns the signed-in user ID, or None for guests.

    Args:
        authorization: Raw `Authorization` header.

    Returns:
        The Supabase user ID, or None when no token was sent.

    Raises:
        HTTPException: 401 if a token was sent but is invalid or expired.
    """
    token = extract_bearer_token(authorization)
    if token is None:
        return None
    try:
        auth_response = supabase.auth.get_user(token)
        if not auth_response or not auth_response.user:
            raise HTTPException(status_code=401, detail="Session expired. Please sign in again.")
        return auth_response.user.id
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Session expired or invalid token. Please sign in again.",
        )
