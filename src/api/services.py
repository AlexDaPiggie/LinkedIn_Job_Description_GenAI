from src.agent.job_agent import JobAgent
from src.agent.questions import QUESTIONS
from src.api.schemas import (
    GenerateRequest,
    GenerateResponse,
    QuestionResponse,
    RefineRequest
)
from src.storage.markdown_files import save_markdown

def list_questions():
    return [
        QuestionResponse(
            question_name = question.question_name,
            question_text = question.question_text,
            required = question.required,
            answer_type= question.answer_type,
        )
        for question in QUESTIONS
    ]

def generate_job_description (request: GenerateRequest): 
    result = JobAgent().generate_draft(
        request.job_info,
        request.provider,
        request.model,
        skipped_fields = request.skipped_fields,
    )

    save_markdown ('latest_job_description.md', result.markdown)
    return GenerateResponse(
        draft = result.draft,
        markdown = result.markdown,
    )

def refine_job_description(request: RefineRequest): 
    result = JobAgent().refine_draft(
        request.company_name,
        request.current_draft,
        request.user_request,
        request.provider,
        request.model,
        request.skipped_fields,
    )

    save_markdown ('latest_job_refinement.md', result.markdown)

    return GenerateResponse(
        draft = result.draft,
        markdown = result.markdown,
    )