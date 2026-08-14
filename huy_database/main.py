import os
from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from src.api.schemas import AuthLoginRequest, AuthResponse, AuthSignupRequest, GenerateRequest,GenerateResponse, QuestionResponse, RefineRequest
from src.api.services import current_user, generate_job_description, list_questions, login, refine_job_description, signup
from src.storage.markdown_files import load_markdown
from pathlib import Path

app = FastAPI(
    title = 'LinkedIn Job Description Generator',
    version = '0.1.0',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
        "VERCEL_ORIGIN_PLACEHOLDER",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization"],
)


def bearer_token(authorization: str | None):
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Please sign in first")
    return authorization.split(" ", 1)[1].strip()


def auth_user_id(authorization: str | None):
    try:
        return current_user(bearer_token(authorization)).user.id
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get('/health')
def health(): 
    return {'status': 'ok'}

@app.post('/auth/signup', response_model=AuthResponse)
def auth_signup(request: AuthSignupRequest):
    if not request.username.strip():
        raise HTTPException(status_code=422, detail="username is required")
    if not request.email.strip():
        raise HTTPException(status_code=422, detail="email is required")
    if len(request.password) < 6:
        raise HTTPException(status_code=422, detail="password must be at least 6 characters")
    try:
        return signup(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.post('/auth/login', response_model=AuthResponse)
def auth_login(request: AuthLoginRequest):
    try:
        return login(request)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.get('/auth/me', response_model=AuthResponse)
def auth_me(authorization: str | None = Header(default=None)):
    try:
        return current_user(bearer_token(authorization))
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

@app.get ('/questions')
def get_questions():
    response_model = list[QuestionResponse]
    return list_questions()
    
@app.post ('/generate', response_model=GenerateResponse)
def generate (request: GenerateRequest, authorization: str | None = Header(default=None)): 
    try:
        return generate_job_description(request, auth_user_id(authorization))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    
@app.post ('/refine', response_model = GenerateResponse)
def refine (request: RefineRequest, authorization: str | None = Header(default=None)): 
    if not request.user_request.strip():
        raise HTTPException(status_code=422, detail = 'user_request is required')
    
    try: 
        return refine_job_description(request, auth_user_id(authorization))
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    
@app.get ("/markdown/{filename}", response_class=PlainTextResponse)
def get_markdown (filename: str): 
    return load_markdown(filename)
