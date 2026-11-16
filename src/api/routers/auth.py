"""Account endpoints: signup, login, OTP, password reset, profile."""

from fastapi import APIRouter, Depends, Header, HTTPException, Request

from src.api.dependencies import require_bearer_token
from src.api.schemas import (
    AuthLoginRequest,
    AuthResponse,
    AuthSignupRequest,
    ChangeUsernameRequest,
    ForgotPasswordRequest,
    ResendOtpRequest,
    ResetPasswordConfirmRequest,
    SignupStatusResponse,
    VerifyOtpRequest,
)
from src.auth.supabase_service import (
    change_supabase_username,
    confirm_password_reset,
    get_current_user_profile,
    login_user,
    request_password_reset,
    resend_signup_otp,
    signup_user,
    verify_user_otp,
)

router = APIRouter(prefix="/auth")

from src.security.emails import is_disposable
from src.security.limits import client_ip
from src.security.turnstile import verify_turnstile

MIN_PASSWORD_LENGTH = 6


@router.post("/signup", response_model=SignupStatusResponse)
def auth_signup(
    request: AuthSignupRequest,
    http_request: Request,
    x_turnstile_token: str | None = Header(default=None),
):
    """Registers an account and emails a verification code.

    Blocks throwaway email providers and requires a human check when
    Turnstile is configured.
    """
    verify_turnstile(x_turnstile_token, client_ip(http_request))
    if is_disposable(request.email):
        raise HTTPException(status_code=400, detail="Please use a permanent email address.")
    if not request.username.strip():
        raise HTTPException(status_code=422, detail="username is required")
    if not request.email.strip():
        raise HTTPException(status_code=422, detail="email is required")
    if len(request.password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(status_code=422, detail="password must be at least 6 characters")
    try:
        return signup_user(request.email, request.password, request.username)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/verify-otp", response_model=AuthResponse)
def auth_verify_otp(request: VerifyOtpRequest):
    """Confirms a signup with the emailed code and signs the user in."""
    try:
        return verify_user_otp(request.email, request.token)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/resend-otp")
def auth_resend_otp(request: ResendOtpRequest):
    """Re-sends the signup verification code."""
    try:
        return resend_signup_otp(request.email)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/login", response_model=AuthResponse)
def auth_login(request: AuthLoginRequest):
    """Signs in with email and password."""
    try:
        return login_user(request.email, request.password)
    except Exception as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@router.post("/forgot-password")
def auth_forgot_password(request: ForgotPasswordRequest):
    """Emails a password-reset code."""
    try:
        return request_password_reset(request.email)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.post("/reset-password")
def auth_reset_password(request: ResetPasswordConfirmRequest):
    """Sets a new password using the emailed reset code."""
    if len(request.new_password) < MIN_PASSWORD_LENGTH:
        raise HTTPException(
            status_code=422,
            detail="new password must be at least 6 characters",
        )
    try:
        return confirm_password_reset(request.email, request.token, request.new_password)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


@router.get("/me", response_model=AuthResponse)
def auth_me(token: str = Depends(require_bearer_token)):
    """Returns the profile and credits of the signed-in user."""
    try:
        return get_current_user_profile(token)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc


@router.post("/change-username", response_model=AuthResponse)
def auth_change_username(
    request: ChangeUsernameRequest,
    token: str = Depends(require_bearer_token),
):
    """Changes the username of the signed-in user."""
    if not request.new_username.strip():
        raise HTTPException(status_code=422, detail="username is required")
    try:
        return change_supabase_username(token, request.new_username.strip())
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
