import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse
from src.api.schemas import GenerateRequest,GenerateResponse, QuestionResponse, RefineRequest
from src.api.services import generate_job_description, list_questions, refine_job_description
from src.storage.markdown_files import load_markdown
from pathlib import Path

app = FastAPI(
    title = 'LinkedIn Job Description Generator',
    version = '0.1.0',
)


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
def generate (request: GenerateRequest): 
    try:
        return generate_job_description(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.post ('/refine', response_model = GenerateResponse)
def refine (request: RefineRequest): 
    if not request.user_request.strip():
        raise HTTPException(status_code=422, detail = 'user_request is required')
    
    try: 
        return refine_job_description(request)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail = str(exc)) from exc
    
@app.get ("/markdown/{filename}", response_class=PlainTextResponse)
def get_markdown (filename: str): 
    return load_markdown(filename)