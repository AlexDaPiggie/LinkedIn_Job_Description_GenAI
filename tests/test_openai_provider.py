import pytest 
import os 
from src.llm.providers import generate_with_openai
from src.llm.client import LLMResult
from dotenv import load_dotenv

load_dotenv(override=True)
def test_generate_with_openai():
    """Test the if the function works"""
    api_key = os.getenv("OPENAI_API_KEY")
    assert api_key is not None, "OPEN_API_KEY is missing"

    result = generate_with_openai(
        prompt = "Say Hello",
        model = "gpt-4o-mini",
    )

    assert isinstance(result, LLMResult)
    assert result.provider == "openai"
    assert result.model == "gpt-4o-mini"
    assert len(result.text.strip()) > 0
    assert result.latency_seconds > 0
    assert result.input_tokens is not None and result.input_tokens > 0
    assert result.output_tokens is not None and result.output_tokens > 0
    print (f"Result: {result}")

