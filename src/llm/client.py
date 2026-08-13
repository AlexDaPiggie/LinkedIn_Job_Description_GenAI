from collections.abc import Callable
from pydantic import BaseModel
from src.llm.providers import generate_with_huggingface, generate_with_openai, generate_with_gemini, generate_with_deepseek, generate_with_openrouter

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
