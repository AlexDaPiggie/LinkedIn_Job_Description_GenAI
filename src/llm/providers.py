import os
import time
from dotenv import load_dotenv
from huggingface_hub import InferenceClient
from openai import OpenAI
from transformers import AutoTokenizer

'''
We cache tokenizer to avoid having to load it many times 
'''
TOKENIZER_CACHE = {}

def count_tokens (text: str, model: str): 
    '''
    This function is simly for couting the the token consumed by the model. In case tokenizer cannot count the number of tokens, the function multiplies the number of words by 1.33 as a fallback.
    '''
    try: 
        if model not in TOKENIZER_CACHE:
            TOKENIZER_CACHE[model] = AutoTokenizer.from_pretrained(
                model,
                dtype = "auto",
                device_map = "auto",
            )
        tokenizer = TOKENIZER_CACHE[model]
        return len (tokenizer.encode (text))
    except Exception:
        return max(1, int(len(text.split()) * 1.33))

def generate_with_openrouter(prompt: str, model: str): 
    from src.llm.client import LLMResult
    from openai import OpenAI, APIError
    load_dotenv()
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key: 
        raise ValueError("The API Key for open Router is not availablle")
    client = OpenAI(
        api_key = api_key,
        base_url = "https://openrouter.ai/api/v1",
    )
    max_retries = 3
    backoff_factor = 2
    delay = 1

    for attempt in range (max_retries):
        try: 
            start = time.perf_counter()
            response = client.chat.completions.create(
                model = model, 
                messages = [{"role": "user", "content": prompt}],
                extra_headers = {
                    'HTTP-Referer': (
                        "https://github.com/alexdapiggie/"
                        "LinkedIn_Job_Description_Generator"
                    ),
                    "Vercel": "LinkedIn Job Descriotion Generator",
                }
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

    usage = getattr (response, "usage", None)
    input_tokens = getattr (usage, "prompt_tokens", None) if usage else None 
    output_tokens = getattr (usage, "completion_tokens", None) if usage else None
    
    return LLMResult (
        text = text, 
        provider = "openrouter",
        model = model, 
        latency_seconds = latency,
        input_tokens = input_tokens,
        output_tokens = output_tokens,
        estimated_cost = None,
    )


def generate_with_openai (prompt: str, model: str): 
    from src.llm.client import LLMResult

    load_dotenv()
    client = OpenAI(api_key = os.getenv ("OPENAI_API_KEY"))
    start = time.perf_counter()
    response = client.responses.create (
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
    )
    latency = time.perf_counter() - start
    usage = getattr (response, "usage", None)
    input_tokens = getattr(usage, "input_tokens", None) if usage else None
    output_tokens = getattr (usage, "output_tokens", None) if usage else None

    return LLMResult(
        text = response.output_text,
        provider = "openapi",
        model = model,
        latency_seconds=latency,
        input_tokens = input_tokens,
        output_tokens= output_tokens,
        estimated_cost = None,
    )

def generate_with_gemini(prompt: str, model: str = "gemini-2.0-flash"):
    from src.llm.client import LLMResult
    from google import genai
    from google.genai.errors import ClientError, ServerError
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    max_retries = 5
    backoff_factor = 2
    delay = 1
    
    for attempt in range(max_retries):
        try:
            start = time.perf_counter()
            response = client.models.generate_content(
                model=model,
                contents=prompt,
            )
            latency = time.perf_counter() - start
            break
        except (ClientError, ServerError) as e:
            # Check if this is a transient 503 / 429
            if attempt < max_retries - 1 and ("503" in str(e) or "429" in str(e) or "UNAVAILABLE" in str(e) or "RESOURCE_EXHAUSTED" in str(e)):
                time.sleep(delay)
                delay *= backoff_factor
                continue
            raise e
    
    usage = getattr(response, "usage_metadata", None)
    input_tokens = getattr(usage, "prompt_token_count", None) if usage else None
    output_tokens = getattr(usage, "candidates_token_count", None) if usage else None

    return LLMResult(
        text=response.text,
        provider="gemini",
        model=model,
        latency_seconds=latency,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=None,
    )


def generate_with_deepseek(prompt: str, model: str = "deepseek-chat"):
    from src.llm.client import LLMResult
    
    load_dotenv()
    # Uses OpenAI SDK configured with DeepSeek's API key & endpoint
    client = OpenAI(
        api_key=os.getenv("DEEPSEEK_API_KEY"),
        base_url="https://api.deepseek.com",
    )
    
    start = time.perf_counter()
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    latency = time.perf_counter() - start
    
    text = response.choices[0].message.content
    usage = getattr(response, "usage", None)
    input_tokens = getattr(usage, "prompt_tokens", None) if usage else None
    output_tokens = getattr(usage, "completion_tokens", None) if usage else None

    return LLMResult(
        text=text,
        provider="deepseek",
        model=model,
        latency_seconds=latency,
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        estimated_cost=None,
    )

def generate_with_huggingface (prompt: str, model: str): 
    from src.llm.client import LLMResult
    load_dotenv()
    client = InferenceClient(
        token = os.getenv ("HF_TOKEN"),
        timeout = 600,
    )
    start = time.perf_counter()
    response = client.chat_completion(
        model = model,
        messages = [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        max_tokens= 2500,
        temperature=0.3,
    )

    latency = time.perf_counter() - start

    text = response.choices[0].message.content
    return LLMResult(
        text = text, 
        provider = "huggingface", 
        model = model,
        latency_seconds=latency,
        input_tokens=count_tokens(prompt, model),
        output_tokens = count_tokens(text, model),
        estimated_cost=None,
    )

