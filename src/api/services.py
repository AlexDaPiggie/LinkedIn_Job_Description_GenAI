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


def stream_generate_job_description(request: GenerateRequest):
    agent = JobAgent()
    for item in agent.stream_generate_draft(
        job_info=request.job_info,
        provider=request.provider,
        model=request.model,
        skipped_fields=request.skipped_fields,
    ):
        if item.get("event") == "done" and "markdown" in item:
            save_markdown("latest_job_description.md", item["markdown"])
        yield item


def stream_refine_job_description(request: RefineRequest):
    agent = JobAgent()
    for item in agent.stream_refine_draft(
        company_name=request.company_name,
        current_draft=request.current_draft,
        user_request=request.user_request,
        provider=request.provider,
        model=request.model,
        skipped_fields=request.skipped_fields,
    ):
        if item.get("event") == "done" and "markdown" in item:
            save_markdown("latest_job_refinement.md", item["markdown"])
        yield item


def extract_job_info_from_doc(file_bytes: bytes, filename: str) -> dict:
    from src.agent.doc_parser import extract_text_from_file
    from src.agent.prompts import build_extraction_prompt
    from src.agent.parser import parse_extracted_doc
    from src.llm.client import generate_text
    from src.llm.models import MODEL_FALLBACKS

    text = extract_text_from_file(file_bytes, filename)
    if not text.strip():
        raise ValueError("The uploaded document is empty or could not be read.")

    prompt = build_extraction_prompt(text)
    model = "google/gemini-2.5-flash-lite"
    fallbacks = MODEL_FALLBACKS.get(model, ["openai/gpt-4o-mini"])

    result = generate_text(
        prompt,
        "openrouter",
        model,
        fallback_models=fallbacks,
    )
    return parse_extracted_doc(result.text)
