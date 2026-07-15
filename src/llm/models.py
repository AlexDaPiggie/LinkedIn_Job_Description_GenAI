MODELS_TO_EVALUATE = [
    {
        "name": "qwen_0_5b_instruct",
        "provider": "huggingface",
        "model_id": "Qwen/Qwen2.5-0.5B-Instruct",
        "purpose": "tiny speed/cost baseline",
    },
    {
        "name": "qwen_3b_instruct",
        "provider": "huggingface",
        "model_id": "Qwen/Qwen2.5-3B-Instruct",
        "purpose": "small model baseline",
    },
    {
        "name": "phi_3_5_mini_instruct",
        "provider": "huggingface",
        "model_id": "microsoft/Phi-3.5-mini-instruct",
        "purpose": "compact open model candidate",
    },
    {
        "name": "qwen_7b_instruct",
        "provider": "huggingface",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
        "purpose": "balanced open model candidate",
    },
    {
        "name": "mistral_7b_instruct",
        "provider": "huggingface",
        "model_id": "mistralai/Mistral-7B-Instruct-v0.3",
        "purpose": "strong open 7B reference",
    },
    {
        "name": "openai_flagship_reference",
        "provider": "openai",
        "model_id": "gpt-5.5",
        "purpose": "paid quality-ceiling reference",
    },
]