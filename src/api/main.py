import os
import stripe
from fastapi import FastAPI, HTTPException, Request, Header
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from src.api.schemas import GenerateRequest,GenerateResponse, QuestionResponse, RefineRequest
from src.api.services import generate_job_description, list_questions, refine_job_description
from src.storage.markdown_files import load_markdown
from src.database.session import get_db, init_db
from src.database.credits import deduct_user_db_credit, add_user_db_credits, get_user_db_credits
from sqlalchemy.orm import Session
from pydantic import BaseModel
from src.auth.google_verifier import verify_google_id_token
from src.auth.services import register_or_login_google_user
from fastapi import Depends
from pathlib import Path
from contextlib import asynccontextmanager

class GoogleLoginRequest(BaseModel):
    token: str

#Initializing the database config
@asynccontextmanager
async def lifespan (app: FastAPI):
    init_db()
    yield

#INitializing backend config
app = FastAPI(
    title = 'LinkedIn Job Description Generator',
    version = '0.1.0',
    lifespan = lifespan,
)

#Intializing a placeholder for Goolge token
@app.post("/auth/google")
def google_login(
    payload: GoogleLoginRequest,
    db: Session = Depends(get_db)
):
    try:
        email = verify_google_id_token(payload.token)
        user = register_or_login_google_user(db, email)

        return {
            "status": "success",
            "email": user.email,
            "free_credits": user.free_credits,
            "purchased_credits": user.purchased_credits,
        }
    
    except ValueError as exc:
        raise HTTPException(status_code=401, detail = str(exc))

#Intializing credits payment config
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
@app.post ("/create-checkout-session")
def create_checkout_session(user_id: str): 
    try: 
        session = stripe.checkout.Session.create(
            payment_method_types = ["card"],
            line_items = [{
                "price_data": {
                    "currency": "usd",
                    "product_data": {
                        "name": "20 Credits",
                        "description": "Each credit can be used for job description generate or refine"
                    },
                    "unit_amount": 150, #1.5 dollars = 150 cents
                },
                "quantity": 1
            }],
            mode = "payment",
            success_url = "http://localhost:3000/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url = "http://localhost:3000/cancel",
            client_reference_id = user_id,
        )
        return {"checkout_url": session.url}
    except Exception as e:
        raise HTTPException(status_code=400, detail = str(e))

@app.post ("/webhook")
async def stripe_webhook (
    request: Request, 
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db)
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
        user_id = session.get ("client_reference_id")
        if user_id: 
            add_user_db_credits(db, user_id, 20) #Add 20 credits for each user

    return {"status": "success"}
    
@app.get("/user/credits/{user_id}")
def check_credits (user_id: str, db: Session = Depends(get_db)):
    return {"user_id": user_id, "credits": get_user_db_credits(db,user_id)}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
    request: Request, 
    payload: GenerateRequest,
    user_id: str = "default_user",
    db: Session = Depends(get_db)
): 

    #deduct user's credits by 1
    if not deduct_user_db_credit(db, user_id):
        raise HTTPException(
            status_code = 402,
            detail = "Insufficient credits"
        )
    
    try:
        return generate_job_description(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.post ('/refine', response_model = GenerateResponse)

def refine (
    request: Request, 
    payload: RefineRequest,
    user_id: str = "default_user",
    db: Session = Depends(get_db),
): 
    if not deduct_user_db_credit(db, user_id):
        raise HTTPException(status_code=402, detail = "Insufficient credits.")
    
    if not payload.user_request.strip():
        raise HTTPException(status_code=422, detail = 'user_request is required')
    
    try: 
        return refine_job_description(payload)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.get ("/markdown/{filename}", response_class=PlainTextResponse)
def get_markdown (filename: str): 
    return load_markdown(filename)