from collections.abc import Callable, Generator
from pydantic import BaseModel
from src.llm.providers import (
    generate_with_huggingface,
    generate_with_openai,
    generate_with_gemini,
    generate_with_deepseek,
    generate_with_openrouter,
    stream_with_openrouter,
    stream_with_openai,
    stream_with_gemini,
    stream_with_deepseek,
    stream_with_huggingface,
)

'''
Structured container for the result of one LLM call
'''
class LLMResult (BaseModel):
    text: str
    provider: str
    model: str
    latency_seconds: float
    input_tokens: int | None = None
    output_tokens: int | None = None
    estimated_cost: float | None = None 

'''
This is a structured alias for any function that takes in two strings and returns an LLMResult.

This support things like: 
* generate_with_openai
* generate_with_huggingface
'''
ProviderFunction = Callable[[str, str], LLMResult]
StreamProviderFunction = Callable[[str, str], Generator[str, None, None]]

def generate_text (
    prompt: str,
    provider: str,
    model: str,
    provider_functions: dict[str, ProviderFunction] | None = None,
    fallback_models: list[str] | None = None
):
    
    '''
    This function is to call the correct provider model, knowing the names of provider, model, and function
    '''
    providers = provider_functions or {
        "openrouter": generate_with_openrouter,
        "openai": generate_with_openai,
        "huggingface": generate_with_huggingface,
        "gemini": generate_with_gemini,
        "deepseek": generate_with_deepseek,
    }

    if provider not in providers:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    #Build a sequence of model to work in case the current model is not available 
    try: 
        return providers[provider](prompt, model)
    except Exception as e:
        last_error = e
        if fallback_models:
            for fallback in fallback_models:
                print (f"Main model is not available: {e}. Trying fallback models {fallback}....")
                try:
                    return providers[provider](prompt, fallback)
                except Exception as fallback_error: 
                    last_error = fallback_error
                    continue

    raise last_error or RuntimeError ("All models are not available")


def stream_text(
    prompt: str,
    provider: str,
    model: str,
    stream_functions: dict[str, StreamProviderFunction] | None = None,
    fallback_models: list[str] | None = None
) -> Generator[str, None, None]:
    streams = stream_functions or {
        "openrouter": stream_with_openrouter,
        "openai": stream_with_openai,
        "huggingface": stream_with_huggingface,
        "gemini": stream_with_gemini,
        "deepseek": stream_with_deepseek,
    }

    if provider not in streams:
        raise ValueError(f"Unsupported LLM provider: {provider}")

    models_to_try = [model] + (fallback_models or [])
    last_error = None

    for candidate in models_to_try:
        try:
            gen = streams[provider](prompt, candidate)
            # Peek at first chunk to make sure the stream successfully initialized
            first_chunk = next(gen)
            yield first_chunk
            for chunk in gen:
                yield chunk
            return
        except Exception as e:
            last_error = e
            continue

    raise last_error or RuntimeError("All models failed during streaming")

