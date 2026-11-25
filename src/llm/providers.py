"""Low-level OpenRouter API calls (single-model, no fallback logic)."""

import os
import time
from collections.abc import Iterator

from dotenv import load_dotenv

OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
OPENROUTER_HEADERS = {
    "HTTP-Referer": "https://github.com/AlexDaPiggie/LinkedIn_Job_Description_GenAI",
    "X-Title": "LinkedIn Job Description Generator",
}
RETRYABLE_STATUS_CODES = (429, 502, 503, 504)
MAX_RETRIES = 3
BACKOFF_FACTOR = 2
INITIAL_RETRY_DELAY_SECONDS = 1


def _get_openrouter_client():
    """Creates an OpenAI-compatible client pointed at OpenRouter.

    Returns:
        A configured `openai.OpenAI` client.

    Raises:
        ValueError: If `OPENROUTER_API_KEY` is not set.
    """
    # Imported here: the openai package is slow to load (about 1s), and
    # deferring it shortens backend startup.
    from openai import OpenAI

    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("The API Key for OpenRouter is not available in environment or .env")
    return OpenAI(api_key=api_key, base_url=OPENROUTER_BASE_URL)


def count_tokens(text: str, model: str | None = None) -> int:
    """Roughly estimates the token count of a text.

    Uses a heuristic of about 1.33 tokens per word.

    Args:
        text: Text to measure.
        model: Unused; kept for interface compatibility.

    Returns:
        The estimated number of tokens (at least 1).
    """
    return max(1, int(len(text.split()) * 1.33))


def generate_with_openrouter(prompt: str, model: str, temperature: float | None = None):
    """Sends a prompt to one OpenRouter model and returns the full reply.

    Retries with exponential backoff on rate-limit and gateway errors.

    Args:
        prompt: User prompt text.
        model: OpenRouter model identifier, for example "openai/gpt-4o-mini".
        temperature: Sampling temperature; None keeps the provider default.

    Returns:
        An `LLMResult` with the text, latency and token usage.

    Raises:
        openai.APIError: If the call fails after retries or with a
            non-retryable error.
    """
    # Imported here to avoid a circular import with src.llm.client, and to
    # keep the slow openai import out of backend startup.
    from openai import APIError

    from src.llm.client import LLMResult

    client = _get_openrouter_client()
    retry_delay = INITIAL_RETRY_DELAY_SECONDS

    for attempt in range(MAX_RETRIES):
        try:
            start_time = time.perf_counter()
            optional_args = {"temperature": temperature} if temperature is not None else {}
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                extra_headers=OPENROUTER_HEADERS,
                **optional_args,
            )
            latency_seconds = time.perf_counter() - start_time
            break
        except APIError as error:
            is_last_attempt = attempt == MAX_RETRIES - 1
            if not is_last_attempt and error.status_code in RETRYABLE_STATUS_CODES:
                time.sleep(retry_delay)
                retry_delay *= BACKOFF_FACTOR
                continue
            raise

    text = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", None) if usage else None
    output_tokens = getattr(usage, "completion_tokens", None) if usage else None

    return LLMResult(
        text=text,
        provider="openrouter",
        model=model,
        served_model=getattr(response, "model", None),
        latency_seconds=latency_seconds,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=None,
    )


def stream_with_openrouter(prompt: str, model: str) -> Iterator[str]:
    """Streams a reply from one OpenRouter model.

    Args:
        prompt: User prompt text.
        model: OpenRouter model identifier.

    Yields:
        Non-empty text chunks as they arrive.
    """
    client = _get_openrouter_client()
    response_stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        extra_headers=OPENROUTER_HEADERS,
        stream=True,
    )
    for chunk in response_stream:
        delta_text = chunk.choices[0].delta.content if chunk.choices else ""
        if delta_text:
            yield delta_text
