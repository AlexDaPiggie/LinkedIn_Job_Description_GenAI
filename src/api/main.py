import os
import stripe
from src.api.schemas import AuthLoginRequest, AuthSignupRequest, AuthResponse
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from src.api.services import generate_job_description, list_questions, refine_job_description
from src.storage.markdown_files import load_markdown
from src.database.supabase_client import supabase
from src.database.supabase_credits import deduct_supabase_credits, get_supabase_credits, add_supabase_credits
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.auth.google_verifier import verify_google_id_token
from fastapi import Depends
from pathlib import Path
from contextlib import asynccontextmanager
from src.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    QuestionResponse,
    RefineRequest,
    AuthSignupRequest,
    AuthLoginRequest,
    AuthResponse,
    VerifyOtpRequest,
    SignupStatusResponse,
    ForgotPasswordRequest,
    ResetPasswordConfirmRequest,
    ChangeUsernameRequest,
)
from src.auth.supabase_service import (
    signup_user, 
    login_user, 
    get_current_user_profile, 
    verify_user_otp,
    request_password_reset,
    confirm_password_reset,
    change_supabase_username,
)

class GoogleLoginRequest(BaseModel):
    token: str

#INitializing backend config
app = FastAPI(
    title = 'LinkedIn Job Description Generator',
    version = '0.1.0',
)

#Initializing stripe api key
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

#This function is to get the user_id from the authentication
def get_user_id_from_auth (authorization: str = Header (None)): 
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException (
            status_code= 401,
            detail = "The token is either missing or invalid"
        )
    token = authorization.split(" ")[1]
    try: 
        user_heap = supabase.auth.get_user(token)
        return user_heap.user.id

    except Exception as e:
        raise HTTPException(status_code=401, detail = "Unauthorized")

#Intializing a placeholder for Goolge token
@app.post("/auth/google")
def google_login(
    payload: GoogleLoginRequest,
):
    try:
        email = verify_google_id_token(payload.token)
        result = supabase.table("profiles").select("*").eq("email", email).execute()

        if not result.data:
            import secrets
            dummy_password = secrets.token_urlsafe(16)
            resp = supabase.auth.sign_up({
                "email": email,
                "password": dummy_password,
            })
            if not resp.user:
                raise ValueError("Google user registration failed")
            user_id = resp.user.id

            supabase.table("profiles").insert ({
                "id": user_id,
                "email": email,
            }).execute()

        else:
            user_id = result.data[0]["id"]

        credits = get_supabase_credits(user_id)
        return {
            "status": "success",
            "email": email,
            "credits": credits
        }
            
    except ValueError as exc:
        raise HTTPException(status_code=401, detail = str(exc))

#Intializing credits payment config
@app.post ("/create-checkout-session")
def create_checkout_session(user_id: str, amount: int = 1, redirect_url: str = "http://localhost:3000"): 
    if amount < 1:
        raise HTTPException(status_code=400, detail="Amount must be at least 1 dollar")
    
    # Stripe requires http:// or https:// for redirect URLs
    if not redirect_url.startswith("http://") and not redirect_url.startswith("https://"):
        redirect_url = "http://localhost:3000"
        
    try: 
        connector = "&" if "?" in redirect_url else "?"
        success_url = f"{redirect_url}{connector}session_id={{CHECKOUT_SESSION_ID}}"
        
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items = [{
                "price_data":{
                    "currency": "usd",
                    "product_data": {
                        "name": "30 credits",
                        "description": "Each credit can be used for either 'refining' or 'generating'",
                    },
                    "unit_amount": 100, #1 dollar gives 30 credits
                },
                "quantity": amount
            }],
            mode = "payment",
            success_url = success_url,
            client_reference_id=user_id,
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))

@app.post ("/webhook")
async def stripe_webhook (
    request: Request, 
    stripe_signature: str = Header(None),
):
    payload = await request.body()
    webhook_secret = os.getenv ("STRIPE_WEBHOOK_SECRET")
    try: 
        event = stripe.Webhook.construct_event (
            payload,
            stripe_signature,
            webhook_secret,
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")
    
    if event["type"] == "checkout.session.completed":
        session = event['data']['object']
        user_id = getattr(session, "client_reference_id", None)
        amount_total = getattr(session, "amount_total", None)
        if user_id and amount_total: 
            try:
                credits_to_add = (amount_total // 100) * 30
                add_supabase_credits(user_id, credits_to_add)
            except Exception as e:
                import traceback
                print("Error processing webhook credits:")
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=str(e))

    return {"status": "success"}
    
@app.get("/user/credits/{user_id}")
def check_credits (user_id: str):
    return {"user_id": user_id, "credits": get_supabase_credits(user_id)}

@app.post("/auth/signup", response_model = SignupStatusResponse)
def auth_signup(request: AuthSignupRequest):
    if not request.username.strip():
        raise HTTPException(status_code=422, detail = "username is required")
    if not request.email.strip():
        raise HTTPException(status_code=422, detail = "email is required")
    if len (request.password) < 6:
        raise HTTPException(status_code=422, detail = "password must be at least 6 characters")
    try:
        return signup_user(
            request.email,
            request.password,
            request.username,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post("/auth/verify-otp", response_model = AuthResponse)
def auth_verify_otp(request: VerifyOtpRequest):
    try:
        return verify_user_otp(request.email, request.token)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post('/auth/login', response_model = AuthResponse)
def auth_login(request: AuthLoginRequest):
    try:
        return login_user(request.email, request.password)
    except Exception as exc:
        raise HTTPException(
            status_code=401, 
            detail = str(exc)
        ) from exc

@app.post('/auth/forgot-password') 
def auth_forgot_password(request: ForgotPasswordRequest):
    try:
        return request_password_reset(request.email)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.post('/auth/reset-password')
def auth_reset_password(request: ResetPasswordConfirmRequest):
    if len (request.new_password) < 6:
        raise HTTPException(
            status_code=422,
            detail="new password must be at least 6 characters"
        )
    try:
        return confirm_password_reset(
            request.email, 
            request.token,
            request.new_password,
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@app.get('/auth/me', response_model = AuthResponse)
def auth_me (authorization: str | None = Header (default = None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail = "Please sign in first")
    token = authorization.split(" ")[1]
    try:
        return get_current_user_profile(token)
    except ValueError as exc:
        raise HTTPException(
            status_code=401, 
            detail = str(exc)
        ) from exc

@app.post('/auth/change-username', response_model = AuthResponse)
def auth_change_username(request: ChangeUsernameRequest, authorization: str | None = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Please sign in first")
    if not request.new_username.strip():
        raise HTTPException(status_code=422, detail="username is required")
    token = authorization.split(" ")[1]
    try:
        return change_supabase_username(token, request.new_username.strip())
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "https://linked-in-gen-ai.vercel.app/",
    ],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get('/health')
def health(): 
    return {'status': 'ok'}

@app.get ('/questions')
def get_questions():
    response_model = list[QuestionResponse]
    return list_questions()

@app.post ('/generate', response_model=GenerateResponse)
def generate (
    payload: GenerateRequest,
    user_id: str = Depends(get_user_id_from_auth),
): 

    #deduct user's credits by 1
    if not deduct_supabase_credits(user_id):
        raise HTTPException(
            status_code = 402,
            detail = "Insufficient credits"
        )
    
    try:
        resp = generate_job_description(payload)
        credits = get_supabase_credits(user_id)
        return GenerateResponse(
            draft=resp.draft,
            markdown=resp.markdown,
            credits_remaining=credits
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.post ('/refine', response_model = GenerateResponse)

def refine (
    payload: RefineRequest,
    user_id: str = Depends(get_user_id_from_auth),
): 
    if not deduct_supabase_credits(user_id):
        raise HTTPException(status_code=402, detail = "Insufficient credits.")
    
    if not payload.user_request.strip():
        raise HTTPException(status_code=422, detail = 'user_request is required')
    
    try: 
        resp = refine_job_description(payload)
        credits = get_supabase_credits(user_id)
        return GenerateResponse(
            draft=resp.draft,
            markdown=resp.markdown,
            credits_remaining=credits
        )
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.get ("/markdown/{filename}", response_class=PlainTextResponse)
def get_markdown (filename: str): 
    return load_markdown(filename)