"""Public, read-only endpoints for the /eval page."""

from fastapi import APIRouter

from src.evaluation.summary import load_summary

router = APIRouter()


@router.get("/api/eval-summary")
def eval_summary():
    """Returns per-model quality, speed and cost from the evaluation harness."""
    return load_summary()
