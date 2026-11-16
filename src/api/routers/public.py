"""Public, read-only endpoints for the /eval page."""

from fastapi import APIRouter

from src.api.schemas import DEFAULT_MODEL
from src.evaluation.summary import load_summary

router = APIRouter()


@router.get("/api/eval-summary")
def eval_summary():
    """Returns per-model quality, speed and cost from the evaluation harness, plus the model in use."""
    summary = load_summary()
    summary["chosen_model"] = DEFAULT_MODEL
    return summary
