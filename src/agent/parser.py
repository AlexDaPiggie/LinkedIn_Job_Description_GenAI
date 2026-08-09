import json
import re
from pydantic import ValidationError
from src.schema.job_description import JobDescriptionDraft

def strip_json (text: str): 
    '''
    This function is simply to strip the important information from the json output
    '''
    stripped = text.strip()
    match = re.search(r"```(?:json)?\s*(.*?)\s*```", stripped, flags=re.DOTALL)
    if match: 
        return match.group (1).strip()
    return stripped

def parse_job_description(text: str): 
    '''
    This function is simply to parse the content from the json file to Job Description in dictionary format
    '''
    raw = strip_json(text)
    try: 
        data = json.loads(raw)
        return JobDescriptionDraft.model_validate(data)
    except (json.JSONDecodeError, ValidationError) as exc:
        raise ValueError(f"Invalid job description JSON: {exc}") from exc