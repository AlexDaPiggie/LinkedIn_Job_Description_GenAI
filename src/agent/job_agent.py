"""Orchestration of job description generation and refinement."""

from collections.abc import Callable, Iterator

from pydantic import BaseModel

from src.agent.parser import (
    parse_job_description,
    parse_section,
)
from src.agent.prompts import (
    LIST_SECTION_KEYS,
    build_generation_prompt,
    build_quick_action_prompt,
    build_refinement_prompt,
    build_section_prompt,
)
from src.rendering.pay import format_pay_range
from src.llm.client import LLMResult, generate_text, stream_text
from src.llm.models import MODEL_FALLBACKS
from src.rendering.markdown import render_job_description
from src.schema.job_description import JobDescriptionDraft
from src.schema.job_info import JobInfo


class AgentResult(BaseModel):
    """Output of one generation or refinement run.

    Attributes:
        draft: The parsed, validated job description.
        markdown: The draft rendered as Markdown.
        llm_result: Raw LLM response with latency and token usage.
    """

    draft: JobDescriptionDraft
    markdown: str
    llm_result: LLMResult


class JobAgent:
    """Orchestrates job description generation and refinement.

    Attributes:
        generate_text_fn: Function used for non-streaming LLM calls. It can
            be replaced to inject a fake LLM in tests or evaluations.
    """

    def __init__(
        self,
        generate_text_fn: Callable[..., LLMResult] = generate_text,
    ):
        """Initializes the agent.

        Args:
            generate_text_fn: Function called as
                `fn(prompt, provider, model, fallback_models=...)` that
                returns an `LLMResult`.
        """
        self.generate_text_fn = generate_text_fn

    def _build_result(
        self,
        llm_result: LLMResult,
        company_name: str,
        skipped_fields: list[str],
        pay_range: str = "",
    ) -> AgentResult:
        """Parses an LLM response and renders it as Markdown.

        Args:
            llm_result: Raw LLM response.
            company_name: Company name used in the rendered heading.
            skipped_fields: Fields to omit from the rendered output.

        Returns:
            The parsed draft together with its Markdown.
        """
        draft = parse_job_description(llm_result.text)
        draft.pay_range = pay_range
        markdown = render_job_description(
            draft,
            company_name=company_name,
            skipped_fields=skipped_fields,
        )
        return AgentResult(draft=draft, markdown=markdown, llm_result=llm_result)

    def _call_llm(self, prompt: str, provider: str, model: str) -> LLMResult:
        """Calls the LLM with the configured fallbacks for the model."""
        return self.generate_text_fn(
            prompt,
            provider,
            model,
            fallback_models=MODEL_FALLBACKS.get(model, []),
        )

    def _stream_draft_events(
        self,
        stream_text_fn: Callable,
        prompt: str,
        provider: str,
        model: str,
        company_name: str,
        skipped_fields: list[str],
        pay_range: str = "",
    ) -> Iterator[dict]:
        """Streams LLM output, then yields the parsed draft.

        Args:
            stream_text_fn: Function yielding text chunks for a prompt.
            prompt: Prompt sent to the LLM.
            provider: LLM provider name.
            model: Model identifier.
            company_name: Company name used in the rendered heading.
            skipped_fields: Fields to omit from the rendered output.
            pay_range: Pay text built from the user numbers; attached to
                the draft (the LLM never writes it).

        Yields:
            `{"event": "chunk", "data": text}` for each streamed chunk,
            followed by one `{"event": "done", "draft": dict,
            "markdown": str}` event.
        """
        accumulated_text = ""
        fallback_models = MODEL_FALLBACKS.get(model, [])
        for chunk in stream_text_fn(prompt, provider, model, fallback_models=fallback_models):
            accumulated_text += chunk
            yield {"event": "chunk", "data": chunk}

        try:
            draft = parse_job_description(accumulated_text)
        except ValueError:
            # Truncated or malformed JSON: retry once without streaming.
            retry_result = self._call_llm(prompt, provider, model)
            draft = parse_job_description(retry_result.text)
        draft.pay_range = pay_range
        markdown = render_job_description(
            draft,
            company_name=company_name,
            skipped_fields=skipped_fields,
        )
        yield {"event": "done", "draft": draft.model_dump(), "markdown": markdown}

    def generate_draft(
        self,
        job_info: JobInfo,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
    ) -> AgentResult:
        """Generates a job description from hiring details.

        Args:
            job_info: Hiring details supplied by the user.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.

        Returns:
            The draft, its Markdown, and the raw LLM result.

        Raises:
            ValueError: If the LLM output is not a valid draft.
        """
        skipped = skipped_fields or []
        prompt = build_generation_prompt(job_info, skipped)
        llm_result = self._call_llm(prompt, provider, model)
        return self._build_result(llm_result, job_info.company_name, skipped, format_pay_range(job_info))

    def refine_draft(
        self,
        company_name: str,
        current_draft: JobDescriptionDraft,
        user_request: str,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
    ) -> AgentResult:
        """Revises an existing draft according to a user request.

        Args:
            company_name: Company name used in the rendered heading.
            current_draft: Draft to revise.
            user_request: Free-text change requested by the user.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.

        Returns:
            The revised draft, its Markdown, and the raw LLM result.

        Raises:
            ValueError: If the LLM output is not a valid draft.
        """
        skipped = skipped_fields or []
        prompt = build_refinement_prompt(
            company_name=company_name,
            current_draft=current_draft,
            user_request=user_request,
            skipped_fields=skipped,
        )
        llm_result = self._call_llm(prompt, provider, model)
        return self._build_result(llm_result, company_name, skipped, current_draft.pay_range)

    def stream_generate_draft(
        self,
        job_info: JobInfo,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
        stream_text_fn: Callable = stream_text,
    ) -> Iterator[dict]:
        """Streams the generation of a job description.

        Args:
            job_info: Hiring details supplied by the user.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.
            stream_text_fn: Function yielding text chunks; replaceable
                for testing.

        Yields:
            "chunk" events while text streams, then one "done" event with
            the parsed draft and its Markdown.
        """
        skipped = skipped_fields or []
        prompt = build_generation_prompt(job_info, skipped)
        yield from self._stream_draft_events(
            stream_text_fn, prompt, provider, model, job_info.company_name, skipped,
            pay_range=format_pay_range(job_info),
        )

    def stream_refine_draft(
        self,
        company_name: str,
        current_draft: JobDescriptionDraft,
        user_request: str,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
        stream_text_fn: Callable = stream_text,
    ) -> Iterator[dict]:
        """Streams the refinement of a job description.

        Args:
            company_name: Company name used in the rendered heading.
            current_draft: Draft to revise.
            user_request: Free-text change requested by the user.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.
            stream_text_fn: Function yielding text chunks; replaceable
                for testing.

        Yields:
            "chunk" events while text streams, then one "done" event with
            the revised draft and its Markdown.
        """
        skipped = skipped_fields or []
        prompt = build_refinement_prompt(
            company_name=company_name,
            current_draft=current_draft,
            user_request=user_request,
            skipped_fields=skipped,
        )
        yield from self._stream_draft_events(
            stream_text_fn, prompt, provider, model, company_name, skipped,
            pay_range=current_draft.pay_range,
        )

    def quick_edit(
        self,
        company_name: str,
        current_draft: JobDescriptionDraft,
        action: str,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
    ) -> AgentResult:
        """Applies a fixed one-click edit (shorter, more inclusive, ...).

        Args:
            company_name: Company name used in the rendered heading.
            current_draft: Draft to revise.
            action: Key of `QUICK_ACTIONS`.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.

        Returns:
            The revised draft, its Markdown, and the raw LLM result.

        Raises:
            ValueError: If the action is unknown or the output is invalid.
        """
        skipped = skipped_fields or []
        prompt = build_quick_action_prompt(current_draft, action)
        llm_result = self._call_llm(prompt, provider, model)
        try:
            return self._build_result(llm_result, company_name, skipped, current_draft.pay_range)
        except ValueError:
            llm_result = self._call_llm(prompt, provider, model)
            return self._build_result(llm_result, company_name, skipped, current_draft.pay_range)

    def regenerate_section(
        self,
        company_name: str,
        current_draft: JobDescriptionDraft,
        section: str,
        provider: str,
        model: str,
        skipped_fields: list[str] | None = None,
    ) -> AgentResult:
        """Rewrites one section and leaves every other section untouched.

        Args:
            company_name: Company name used in the rendered heading.
            current_draft: Draft whose other sections stay as they are.
            section: Section key to rewrite.
            provider: LLM provider name.
            model: Model identifier.
            skipped_fields: Fields the user chose to skip.

        Returns:
            The draft with the new section, its Markdown, and the LLM result.

        Raises:
            ValueError: If the section is unknown or the output is invalid.
        """
        prompt = build_section_prompt(current_draft, section)
        is_list = section in LIST_SECTION_KEYS
        llm_result = self._call_llm(prompt, provider, model)
        try:
            value = parse_section(llm_result.text, section, is_list)
        except ValueError:
            llm_result = self._call_llm(prompt, provider, model)
            value = parse_section(llm_result.text, section, is_list)
        draft = current_draft.model_copy(update={section: value})
        markdown = render_job_description(
            draft, company_name=company_name, skipped_fields=skipped_fields or []
        )
        return AgentResult(draft=draft, markdown=markdown, llm_result=llm_result)
