"""Model prices for the benchmark, taken from OpenRouter's public model list.

Prices are saved to a dated snapshot file so every cost in the results can be
traced to the list price on a known day. Run this module to refresh it:

    python -m src.evaluation.pricing
"""

import json
import urllib.request
from datetime import date
from pathlib import Path

OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
PRICES_PATH = Path(__file__).resolve().parent.parent.parent / "eval_results" / "openrouter_prices.json"


def fetch_prices(model_ids: list[str]) -> dict:
    """Downloads current list prices for the given models.

    Args:
        model_ids: OpenRouter model IDs to keep.

    Returns:
        `{"fetched_on": "YYYY-MM-DD", "source": url, "usd_per_million_tokens":
        {model_id: [input, output]}}`. Models OpenRouter no longer lists are
        left out.
    """
    with urllib.request.urlopen(OPENROUTER_MODELS_URL, timeout=30) as response:
        listing = json.loads(response.read().decode("utf-8"))["data"]
    by_id = {entry["id"]: entry for entry in listing}
    prices = {}
    for model_id in model_ids:
        entry = by_id.get(model_id)
        if entry:
            pricing = entry["pricing"]
            prices[model_id] = [
                round(float(pricing["prompt"]) * 1e6, 4),
                round(float(pricing["completion"]) * 1e6, 4),
            ]
    return {
        "fetched_on": date.today().isoformat(),
        "source": OPENROUTER_MODELS_URL,
        "usd_per_million_tokens": prices,
    }


def load_prices(path: Path = PRICES_PATH) -> dict:
    """Loads the saved price snapshot (empty prices if the file is missing)."""
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {"fetched_on": None, "source": OPENROUTER_MODELS_URL, "usd_per_million_tokens": {}}


def save_prices(snapshot: dict, path: Path = PRICES_PATH) -> None:
    """Writes a price snapshot to disk."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    from src.evaluation.metrics import JUDGE_MODEL
    from src.llm.models import MODELS_TO_EVALUATE

    ids = [config["model_id"] for config in MODELS_TO_EVALUATE] + [JUDGE_MODEL]
    snapshot = fetch_prices(ids)
    save_prices(snapshot)
    missing = sorted(set(ids) - set(snapshot["usd_per_million_tokens"]))
    print(f"Saved {len(snapshot['usd_per_million_tokens'])} prices to {PRICES_PATH}")
    if missing:
        print("Not listed on OpenRouter:", ", ".join(missing))
