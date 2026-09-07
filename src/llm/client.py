from collections.abc import Generator
from pydantic import BaseModel
from src.llm.providers import generate_with_openrouter, stream_with_openrouter

'''
Structured container for the result of one LLM call
'''
class LLMResult(BaseModel):
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
    '''
    Calls OpenRouter model with automatic fallbacks.
    Supports both signatures:
      generate_text(prompt, model)
      generate_text(prompt, provider, model)
    '''
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

    models_to_try = [model] + (fallback_models or [])
    last_error = None

    for candidate in models_to_try:
        try:
            return generate_with_openrouter(prompt, candidate)
        except Exception as err:
            last_error = err
            if fallback_models:
                print(f"Model {candidate} failed: {err}. Trying fallback...")
            continue

    raise last_error or RuntimeError("All models failed during generation")


def stream_text(
    prompt: str,
    *args,
    provider: str = "openrouter",
    model: str | None = None,
    fallback_models: list[str] | None = None,
) -> Generator[str, None, None]:
    '''
    Streams tokens from OpenRouter with automatic fallbacks.
    Supports both signatures:
      stream_text(prompt, model)
      stream_text(prompt, provider, model)
    '''
    if len(args) == 1:
        model = args[0]
    elif len(args) >= 2:
        provider, model = args[0], args[1]
    elif not model and args:
        model = args[0]

    if not model:
        raise ValueError("Model must be specified for streaming")

    models_to_try = [model] + (fallback_models or [])
    last_error = None

    for candidate in models_to_try:
        try:
            gen = stream_with_openrouter(prompt, candidate)
            first_chunk = next(gen)
            yield first_chunk
            for chunk in gen:
                yield chunk
            return
        except Exception as err:
            last_error = err
            continue

    raise last_error or RuntimeError("All models failed during streaming")

