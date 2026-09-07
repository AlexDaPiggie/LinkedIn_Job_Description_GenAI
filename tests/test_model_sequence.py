import pytest
from src.llm.client import generate_text
from src.llm.models import MODEL_FALLBACKS

def test_fall_back_primary_model():
    called_models = []

    def mock_provider_funcion (prompt, model):
        called_models.append (model)
        return "draft generated successfully"

    custom_providers = {"openrouter": mock_provider_funcion}

    result = generate_text (
        prompt = "test prompt", 
        provider = "openrouter",
        model = "google/gemini-2.5-flash-lite",
        provider_functions = custom_providers,
        fallback_models = ["openai/gpt-4o"]
    )
    assert result == "draft generated successfully"
    assert called_models == ["google/gemini-2.5-flash-lite"]

def test_fallback_secondary_model():
    called_models = []

    def mock_provider_function (prompt, model):
        called_models.append (model)
        if model == "google/gemini-2.5-flash-lite":
            raise RuntimeError("Error with model")
        return "fallback draft generated successfully"
    
    custom_providers = {"openrouter": mock_provider_function}
    result = generate_text(
        prompt = "test prompt",
        provider = "openrouter",
        model = "google/gemini-2.5-flash-lite",
        provider_functions = custom_providers,
        fallback_models = ["openai/gpt-4o"],
    )

    print (called_models)
    assert result == "fallback draft generated successfully"
    assert called_models == ["google/gemini-2.5-flash-lite", "openai/gpt-4o"]

def test_model_fallbacks_from_config():
    primary_model = "google/gemini-2.5-flash-lite"
    fallbacks = MODEL_FALLBACKS.get(primary_model)
    assert fallbacks is not None, f"Sequence fails for {primary_model}"
    assert len(fallbacks) >= 2, "Fallback must have at least 2 models"

    called_models = []

    def mock_provider_function (prompt, model):
        called_models.append(model)
        if model == primary_model:
            raise RuntimeError ('Primary model error')
        if model == fallbacks[0]:
            raise RuntimeError('First fall back model error')
        return "fallback success"

    custom_providers = {"openrouter": mock_provider_function}
    result = generate_text(
        prompt = "say Hi",
        provider = "openrouter",
        model = primary_model,
        provider_functions = custom_providers,
        fallback_models = fallbacks
    )

    assert result == "fallback success"
    assert called_models == [primary_model, fallbacks[0], fallbacks[1]]
    
