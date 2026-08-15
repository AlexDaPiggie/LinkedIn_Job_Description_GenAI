from pydantic import BaseModel, Field
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo
import json 
import os

config_path = os.path.join (os.path.dirname(__file__), '../config.json')
try: 
    with open (config_path, 'r') as file: 
        config = json.load (file)
    PROVIDER = config.get ("LLM_PROVIDER")
    MODEL = config.get ("LLM_MODEL")
except Exception as e:
    print (f"Warning: Could not load config.json. Using defaults. Error: {e}")
    PROVIDER = 'openai'
    MODEL = 'gpt-4o'

class QuestionResponse (BaseModel):
    question_name: str
    question_text: str
    required: bool
    answer_type: str

class GenerateRequest (BaseModel):
    job_info: JobInfo
    skipped_fields: list[str] = Field(default_factory=list)
    provider: str = PROVIDER
    model: str = MODEL

class GenerateResponse (BaseModel):
    draft: JobDescriptionDraft
    markdown: str
    credits_remaining: int | None = None

class RefineRequest (BaseModel):
    company_name: str
    current_draft: JobDescriptionDraft
    user_request: str
    skipped_fields: list[str] = Field(default_factory=list)
    provider: str = PROVIDER
    model: str = MODEL

class ErrorResponse (BaseModel): 
    detail: str

class AuthSignupRequest(BaseModel):
    username: str
    email: str
    password: str

class AuthLoginRequest (BaseModel):
    email: str
    password: str

class UserDetail (BaseModel):
    id: str
    email: str
    username: str | None = None

class AuthResponse(BaseModel):
    access_token: str
    user: UserDetail
    credits: int
    
class VerifyOtpRequest(BaseModel):
    email: str
    token: str

class SignupStatusResponse(BaseModel):
    status: str
    email: str
    message: str

class ForgotPasswordRequest(BaseModel):
    email: str

class ResetPasswordConfirmRequest(BaseModel):
    email: str
    token: str
    new_password: str

class ChangeUsernameRequest(BaseModel):
    new_username: str

    