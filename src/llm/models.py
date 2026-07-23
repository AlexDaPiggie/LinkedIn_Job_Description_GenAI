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
        "name": "llama_3_1_8b_instruct",
        "provider": "huggingface",
        "model_id": "meta-llama/Meta-Llama-3.1-8B-Instruct",
        "purpose": "state-of-the-art 8B candidate",
    },
    {
        "name": "qwen_7b_instruct",
        "provider": "huggingface",
        "model_id": "Qwen/Qwen2.5-7B-Instruct",
        "purpose": "balanced open model candidate",
    },
    {
        "name": "mistral_7b_instruct_v0_2",
        "provider": "huggingface",
        "model_id": "mistralai/Mistral-7B-Instruct-v0.2",
        "purpose": "strong open 7B reference",
    },
    {
        "name": "gemma_2_9b_it",
        "provider": "huggingface",
        "model_id": "google/gemma-2-9b-it",
        "purpose": "high reasoning 9B candidate",
    },
    {
        "name": "zephyr_7b_beta",
        "provider": "huggingface",
        "model_id": "HuggingFaceH4/zephyr-7b-beta",
        "purpose": "chat fine-tuned 7B candidate",
    },
    {
        "name": "openai_flagship_reference",
        "provider": "openai",
        "model_id": "gpt-5.5",
        "purpose": "paid quality-ceiling reference",
    },
]