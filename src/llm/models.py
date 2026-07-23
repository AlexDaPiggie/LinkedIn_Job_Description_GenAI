MODELS_TO_EVALUATE = [
    # ----------HUGGING FACE---------------
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
    # ----------OPENAI---------------
    {
        "name": "openai_gpt_4o_mini",
        "provider": "openai",
        "model_id": "gpt-4o-mini",
        "purpose": "fastest, cost-effective model",
    },
    {
        "name": "openai_gpt_4o",
        "provider": "openai",
        "model_id": "gpt-4o",
        "purpose": "flagship high-reasoning openAI reference",
    },
    # ----------GEMINI---------------
    {
        "name": "gemini_2_5_flash",
        "provider": "gemini",
        "model_id": "gemini-2.5-flash",
        "purpose": "ultra-fast, next-gen Gemini model",
    },
    {
        "name": "gemini_1_5_flash",
        "provider": "gemini",
        "model_id": "gemini-1.5-flash",
        "purpose": "lightweight Gemini baseline",
    },
    {
        "name": "gemini_1_5_pro",
        "provider": "gemini",
        "model_id": "gemini-1.5-pro",
        "purpose": "complex reasoning & multi-modal Gemini model",
    },        
    # ----------DEEPSEEK---------------
    {
        "name": "deepseek_v3_chat",
        "provider": "deepseek",
        "model_id": "deepseek-chat",
        "purpose": "ultra-fast, low-cost DeepSeek V3 chat model",
    },
    {
        "name": "deepseek_r1_reasoner",
        "provider": "deepseek",
        "model_id": "deepseek-reasoner",
        "purpose": "advanced chain-of-thought reasoning DeepSeek R1 model",
    },
]