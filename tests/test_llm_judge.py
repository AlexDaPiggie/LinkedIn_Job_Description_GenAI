import pytest 
import os 
from dotenv import load_dotenv
from src.llm.client import generate_text
from src.evaluation.metrics import JUDGE_PROMPT
import json

load_dotenv()

def test_openai_api_call():
    "STEP 1: Test basic OpenAI API connection and response format."
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPEN_API_KEY is missing from .env!"

    result = generate_text(
        prompt = "Say Hello",
        provider = "openrouter",
        model = "gpt-4.1",
    )

    assert result is not None, "generate_text returned None!"
    assert hasattr (result, "text"), "result has no 'text' attribute!"
    assert len (result.text.strip()) > 0, "result.text is empty!"
    print (f"\n[SUCCESS] API Response: {result.text}")

def test_judge_raw_response():
    job_info = {
        "title": "software engineer", 
        "company_name": "tech company",
    }
    prompt = f"{JUDGE_PROMPT}\n\nJob Info:\n{json.dumps (job_info)}"

    response = generate_text(
        prompt = prompt,
        provider = "openrouter",
        model = "gpt-4.1"
    )

    raw_text = response.text
    print (f"\n[RAW LIM RESPONSE]:\n{raw_text}")
    assert len(raw_text.strip()) > 0, "Judge returned empty text!"
