import os
import time
from dotenv import load_dotenv
from openai import OpenAI, APIError

'''
Cache and helper to get OpenRouter client
'''
def _get_openrouter_client() -> OpenAI:
    load_dotenv(override=True)
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise ValueError("The API Key for OpenRouter is not available in environment or .env")
    return OpenAI(
        api_key=api_key,
        base_url="https://openrouter.ai/api/v1",
    )

def count_tokens(text: str, model: str | None = None) -> int:
    return max(1, int(len(text.split()) * 1.33))

def generate_with_openrouter(prompt: str, model: str):
    from src.llm.client import LLMResult
    client = _get_openrouter_client()
    max_retries = 3
    backoff_factor = 2
    delay = 1

    for attempt in range(max_retries):
        try:
            start = time.perf_counter()
            response = client.chat.completions.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                extra_headers={
                    "HTTP-Referer": "https://github.com/alexdapiggie/LinkedIn_Job_Description_Generator",
                    "X-Title": "LinkedIn Job Description Generator",
                },
            )
            latency = time.perf_counter() - start
            break
        except APIError as e:
            if attempt < max_retries - 1 and (e.status_code in [429, 502, 503, 504]):
                time.sleep(delay)
                delay *= backoff_factor
                continue
            raise e

    text = response.choices[0].message.content or ""
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", None) if usage else None
    output_tokens = getattr(usage, "completion_tokens", None) if usage else None

    return LLMResult(
        text=text,
        provider="openrouter",
        model=model,
        latency_seconds=latency,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=None,
    )

def stream_with_openrouter(prompt: str, model: str):
    client = _get_openrouter_client()
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        extra_headers={
            "HTTP-Referer": "https://github.com/alexdapiggie/LinkedIn_Job_Description_Generator",
            "X-Title": "LinkedIn Job Description Generator",
        },
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else ""
        if delta:
            yield delta