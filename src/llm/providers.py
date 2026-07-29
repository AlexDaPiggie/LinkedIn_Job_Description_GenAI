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


def generate_with_openai (prompt: str, model: str): 
    from src.llm.client import LLMResult
    load_dotenv()
    client = OpenAI(api_key = os.getenv ("OPENAI_API_KEY"))
    start = time.perf_counter()
    response = client.responses.create (
        model = model,
        input = prompt,
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

def generate_with_gemini(prompt: str, model: str = "gemini-2.5-flash"):
    from src.llm.client import LLMResult
    from google import genai
    #We don't use openAI framework because google genAI provides free token for flash model everyday, that's a great idea for everything.
    
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    start = time.perf_counter()
    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )
    latency = time.perf_counter() - start
    
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