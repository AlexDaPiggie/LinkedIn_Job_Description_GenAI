from collections.abc import Callable
from pydantic import BaseModel
from src.agent.parser import parse_job_description
from src.agent.prompts import build_generation_prompt, build_refinement_prompt
from src.llm.client import LLMResult, generate_text
from src.rendering.markdown import render_job_description
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo
from src.llm.models import MODEL_FALLBACKS

'''
Structured data to store the ouput of the agents together
'''
class AgentResult (BaseModel): 
    draft: JobDescriptionDraft
    markdown: str
    llm_result: LLMResult

class JobAgent:
    '''
    This is the orchestrator for job-description generation and refinement
    '''
    def __init__(
        self,
        generate_text_fn: Callable[[str, str, str], LLMResult] = generate_text
    ):
        self.generate_text_fn = generate_text_fn

    def generate_draft(
        self, 
        job_info: JobInfo, 
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
    ):
        
        skipped = skipped_fields or []
        prompt = build_generation_prompt(job_info, skipped)

        llm_result = self.generate_text_fn(
            prompt,
            provider,
            model,
            fallbacks,
        )
        draft = parse_job_description(llm_result.text)

        #add the fallback models for sequencing in case the main model is not available
        fallbacks = MODEL_FALLBACKS.get(model, [])

        return AgentResult(
            draft = draft,
            markdown = render_job_description(
                draft, 
                company_name = job_info.company_name,
                skipped_fields=skipped,
            ),
            llm_result = llm_result,
        )
    
    def refine_draft(
        self,
        company_name: str,
        current_draft: JobDescriptionDraft,
        user_request: str,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None
    ): 
        skipped = skipped_fields or []
        prompt = build_refinement_prompt(
            company_name=company_name, 
            current_draft=current_draft, 
            user_request=user_request, 
            skipped_fields=skipped
        )
        llm_result = self.generate_text_fn(prompt, provider, model)
        draft = parse_job_description(llm_result.text)

        #add the fallback models
        fallbacks = MODEL_FALLBACKS.get (model, [])

        return AgentResult(
            draft = draft,
            markdown=render_job_description(
                draft = draft,
                company_name=company_name,
                skipped_fields=skipped,
            ),
            llm_result=llm_result,
        )