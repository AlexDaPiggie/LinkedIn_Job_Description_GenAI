from pydantic import BaseModel, Field
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo

class QuestionResponse (BaseModel):
    question_name: str
    question_text: str
    required: bool
    answer_type: str

class GenerateRequest (BaseModel):
    job_info: JobInfo
    skipped_fields: list[str] = Field(default_factory=list)
    provider: str = 'huggingface'
    model: str = 'Qwen/Qwen2.5-7B-Instruct'

class GenerateResponse (BaseModel):
    draft: JobDescriptionDraft
    markdown: str

class RefineRequest (BaseModel):
    job_info: JobInfo
    current_draft: JobDescriptionDraft
    user_request: str
    skipped_fields: list[str] = Field(default_factory=list)
    provider: str = 'huggingface'
    model: str = 'Qwen/Qwen2.5-7B-Instruct'

class ErrorResponse (BaseModel): 
    detail: str

