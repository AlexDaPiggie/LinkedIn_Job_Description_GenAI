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

def generate_with_openai (prompt: str, model: str): 
    from src.llm.client import LLMResult
    load_dotenv()
    client = OpenAI(api_key = os.getenv ("OPEN_API_KEY"))
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