from collections.abc import Callable
from pydantic import BaseModel
from src.llm.providers import generate_with_huggingface, generate_with_openai, generate_with_gemini, generate_with_deepseek

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
):
    
    '''
    This function is to call the correct provider model, knowing the names of provider, model, and function
    '''
    providers = provider_functions or {
        "openai": generate_with_openai,
        "huggingface": generate_with_huggingface,
        "gemini": generate_with_gemini,
        "deepseek": generate_with_deepseek,
    }

    if provider not in providers:
        raise ValueError(f"Unsupported LLM provider: {provider}")
    return providers[provider](prompt, model)