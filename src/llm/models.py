MODEL_FALLBACKS = {
    "google/gemini-2.5-flash-lite": [
        "openai/gpt-4o",
        "openai/gpt-4o-mini",
        "mistralai/mistral-small-24b-instruct-2501",
    ]
}

MODELS_TO_EVALUATE = [
    {
        "name": "openrouter_gpt_4o_mini",
        "provider": "openrouter",
        "model_id": "openai/gpt-4o-mini",
        "purpose": "Very cheap, fast, and highly reliable structured outputs",
    },
        {
        "name": "openrouter_gpt_4o",
        "provider": "openrouter",
        "model_id": "openai/gpt-4o",
        "purpose": "A better sidekick of gpt-4o-mini",
    },
    {
        "name": "openrouter_deepseek_v3.1",
        "provider": "openrouter",
        "model_id": "deepseek/deepseek-chat-v3.1",
        "purpose": "Incredibly cheap, high-intelligence chat and coding model",
    },
    {
        "name": "openrouter_deepseek_r1",
        "provider": "openrouter",
        "model_id": "deepseek/deepseek-r1",
        "purpose": "SOTA open reasoning model for text generating tasks",
    },    
    {
        "name": "gemini_2_5_Pro",
        "provider": "openrouter",
        "model_id": "google/gemini-2.5-pro",
        "purpose": "High-intelligence reasoning and documenting abilties"
    },
    {
        "name": "gemini_2_5_lite",
        "provider": "openrouter",
        "model_id": "google/gemini-2.5-flash-lite",
        "purpose": "A smaller versin of gemini 2.5 with the same possession of skillset",
    },
    {
        "name": "openrouter_command_r",
        "provider": "openrouter",
        "model_id": "cohere/command-r-08-2024",
        "purpose": "highly cost-effective document model"
    },
    {
        "name": "openrouter_command_r_plus",
        "provider": "openrouter",
        "model_id": "cohere/command-r-plus-08-2024",
        "purpose": "Optimized sidekick of command-r for business document drafting"
    },
    {
        "name": "openrouter_llama_3_3_70b",
        "provider": "openrouter",
        "model_id": "meta-llama/llama-3.3-70b-instruct",
        "purpose": "High-quality, low-cost open weights model",
    },
    {
        "name": "openrouter_llama_3_1_8b",
        "provider": "openrouter",
        "model_id": "meta-llama/llama-3.1-8b-instruct",
        "purpose": "Ultra cheap and fast model for text generating",
    },        
    {
        "name": "openrouter_llama_3_1_70b",
        "provider": "openrouter",
        "model_id": "meta-llama/llama-3.1-70b-instruct",
        "purpose": "Highly compatible model",
    },      
    {
        "name": "openrouter_qwen_2_5_72b",
        "provider": "openrouter",
        "model_id": "qwen/qwen-2.5-72b-instruct",
        "purpose": "Budget-friendly open-weights model with excellent multi-lingual & formatting skills",
    },
    {
        "name": "openrouter_qwen_2_5_coder_32b",
        "provider": "openrouter",
        "model_id": "qwen/qwen-2.5-coder-32b-instruct",
        "purpose": "Fine-tuned coder version of the 32b version for fomratting complexed structures",
    },
    {
        "name": "openrouter_qwen_2_5_7b",
        "provider": "openrouter",
        "model_id": "qwen/qwen-2.5-7b-instruct",
        "purpose": "Fast and cheap model with great structural data support",
    },    
    {
        "name": "openrouter_qwen_2_5_7b",
        "provider": "openrouter",
        "model_id": "qwen/qwen-2.5-7b-instruct",
        "purpose": "Fast and cheap model with great structural data support",
    },    
    {
        "name": "openrouter_qwen_3_5_flash",
        "provider": "openrouter",
        "model_id": "qwen/qwen3.5-flash-02-23",
        "purpose": "Fast model from qwen with decenet text generating abiltity",
    },        
    {
        "name": "openrouter_mistral_small",
        "provider": "openrouter",
        "model_id": "mistralai/mistral-small-24b-instruct-2501",
        "purpose": "Ultra-fast, low-cost model optimized for structured prompt adherence",
    },
    {
        "name": "openrouter_mixtral_8x22b",
        "provider": "openrouter",
        "model_id": "mistralai/mixtral-8x22b-instruct",
        "purpose": "Well-balanced mixture of differnt aspects a model needs",
    },    
    {
        "name": "openrouter_nemotron_3_nano_30b",
        "provider": "openrouter",
        "model_id": "nvidia/nemotron-3-nano-30b-a3b",
        "purpose": "Nvidia cost-effective model optimized for text2text purposes",
    },        
    {
        "name": "openrouter_nemotron_3_super-120b",
        "provider": "openrouter",
        "model_id": "nvidia/nemotron-3-super-120b-a12b",
        "purpose": "Nvidia heavire model optimized for text2text purposes, potentially be a better sidekick for the nano version",
    },            
    {
        "name": "openrouter_wizardlm_2_8x22b",
        "provider": "openrouter",
        "model_id": "microsoft/wizardlm-2-8x22b",
        "purpose": "A very cheap and speedy model open weighted from microsoft",
    },  
    {
        "name": "openrouter_claude_3_haiku",
        "provider": "openrouter",
        "model_id": "anthropic/claude-3-haiku",
        "purpose": "Lightweight, highly accurate structured JSON generator",
    },
]

