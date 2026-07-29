import csv
import json
from pathlib import Path

from src.agent.job_agent import JobAgent
from src.evaluation.metrics import check_expected_terms, score_schema_result
from src.evaluation.scenarios import EVALUATION_SCENARIOS
from src.llm.client import generate_text
from src.llm.models import MODELS_TO_EVALUATE
from src.schema.job_info import JobInfo

def run_single_evaluation (
    model_config: dict, 
    scenario: dict,
    generate_text_fn = generate_text
):

    agent = JobAgent(generate_text_fn = generate_text_fn)
    job_info = JobInfo.model_validate(scenario["job_info"])
    rows = []

    generated = agent.generated_draft (
        job_info,
        provider = model_config["provider"],
        model = model_config ["model_id"],
    )
