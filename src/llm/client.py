"""LLM text generation with automatic model fallbacks."""

from collections.abc import Generator
from pydantic import BaseModel
from src.llm.providers import generate_with_openrouter, stream_with_openrouter

class LLMResult(BaseModel):
    """Result of one LLM call.

    Attributes:
        text: Generated text.
        provider: Provider that served the call.
        model: Model that produced the text.
        latency_seconds: Wall-clock duration of the call.
        input_tokens: Prompt tokens used, if reported.
        output_tokens: Completion tokens used, if reported.
        estimated_cost: Estimated cost in USD, if known.
    """

    text: str
    provider: str = "openrouter"
    model: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None

def generate_text(
    prompt: str,
    *args,
    provider: str = "openrouter",
    model: str | None = None,
    fallback_models: list[str] | None = None,
) -> LLMResult:
    """Generates text with OpenRouter, trying fallback models on failure.

    Supports both `generate_text(prompt, model)` and
    `generate_text(prompt, provider, model)`, as well as keyword arguments.
    The provider is currently always OpenRouter.

    Args:
        prompt: Prompt text.
        *args: Optional positional `model` or `provider, model`.
        provider: Provider name (keyword form).
        model: Model identifier (keyword form).
        fallback_models: Models to try, in order, if the primary fails.

    Returns:
        The result of the first model that succeeds.

    Raises:
        ValueError: If no model is given.
        Exception: The last error raised if every model fails.
    """
    if len(args) == 1:
        # Called as generate_text(prompt, model)
        model = args[0]
    elif len(args) >= 2:
        # Called as generate_text(prompt, provider, model)
        provider, model = args[0], args[1]
    elif not model and args:
        model = args[0]

    if not model:
        raise ValueError("Model must be specified for text generation")

    candidate_models = [model] + (fallback_models or [])
    last_error = None

    for candidate_model in candidate_models:
        try:
            return generate_with_openrouter(prompt, candidate_model)
        except Exception as error:
            last_error = error
            if fallback_models:
                print(f"Model {candidate_model} failed: {error}. Trying fallback...")
            continue

    raise last_error or RuntimeError("All models failed during generation")


def stream_text(
    prompt: str,
    *args,
    provider: str = "openrouter",
    model: str | None = None,
    fallback_models: list[str] | None = None,
) -> Generator[str, None, None]:
    """Streams text from OpenRouter, trying fallback models on failure.

    Supports the same call signatures as `generate_text`. Fallback only
    happens before the first chunk arrives or if a model fails mid-stream
    (in which case already-yielded chunks are not retracted).

    Args:
        prompt: Prompt text.
        *args: Optional positional `model` or `provider, model`.
        provider: Provider name (keyword form).
        model: Model identifier (keyword form).
        fallback_models: Models to try, in order, if the primary fails.

    Yields:
        Text chunks.

    Raises:
        ValueError: If no model is given.
        Exception: The last error raised if every model fails.
    """
    if len(args) == 1:
        model = args[0]
    elif len(args) >= 2:
        provider, model = args[0], args[1]
    elif not model and args:
        model = args[0]

    if not model:
        raise ValueError("Model must be specified for streaming")

    candidate_models = [model] + (fallback_models or [])
    last_error = None

    for candidate_model in candidate_models:
        try:
            chunk_stream = stream_with_openrouter(prompt, candidate_model)
            first_chunk = next(chunk_stream)
            yield first_chunk
            for chunk in chunk_stream:
                yield chunk
            return
        except Exception as error:
            last_error = error
            continue

    raise last_error or RuntimeError("All models failed during streaming")

