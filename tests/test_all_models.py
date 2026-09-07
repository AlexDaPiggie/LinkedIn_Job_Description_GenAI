import pytest
import os
from src.llm.client import generate_text
from src.llm.models import MODELS_TO_EVALUATE
from dotenv import load_dotenv

#overriding local .env with global environment variable
load_dotenv(override=True)

@pytest.mark.parametrize (
    "model_config",
    MODELS_TO_EVALUATE,
    ids = lambda config: config["name"],
)
def test_model_generation(model_config):
    # THis testcase is to test if all models are able to generate text
    provider = model_config["provider"]
    model_id = model_config["model_id"]
    model_name = model_config["name"]

    print (f"\nTesting models: {model_name} ({provider} - {model_id})...")
    try: 
        result = generate_text(
            prompt = "Say 'test passed'",
            provider = provider,
            model = model_id,
        )
        assert result is not None, f"{model_name} has failed to generate text"
        assert len(result.text.strip()) > 0, f"The generated text from {model_name} is empty"
        print (f"The model successfully responses: {result.text.strip()}")

    except Exception as e:
        pytest.fail (f"Model {model_name} failed: {str(e)}")