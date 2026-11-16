"""In-memory rate limits and a global daily spend cap.

State lives in process memory: it resets when the server restarts and is
per container. That is fine for a single Hugging Face Space and costs
nothing. For several replicas, move the counters to Redis or Supabase.
"""

import hashlib
import os
import threading
import time
from collections import defaultdict, deque
from datetime import date

from fastapi import HTTPException, Request

GUEST_DAILY_LIMIT = int(os.getenv("GUEST_DAILY_LIMIT", "10"))
GLOBAL_DAILY_LLM_CALLS = int(os.getenv("GLOBAL_DAILY_LLM_CALLS", "3000"))
USER_HOURLY_LIMIT = int(os.getenv("USER_HOURLY_LIMIT", "60"))
TRUSTED_PROXY_HOPS = int(os.getenv("TRUSTED_PROXY_HOPS", "1"))

_lock = threading.Lock()
_guest_counts: dict[tuple[str, date], int] = defaultdict(int)
_global_counts: dict[date, int] = defaultdict(int)
_user_hits: dict[str, deque] = defaultdict(deque)


def client_ip(request: Request) -> str:
    """Returns the client IP, trusting only the configured number of proxies.

    `X-Forwarded-For` can be forged by the caller, but each trusted proxy
    appends the address it saw to the right end. Reading `TRUSTED_PROXY_HOPS`
    entries from the right skips anything the caller wrote.

    Args:
        request: Incoming request.

    Returns:
        The best-known client IP, or "unknown".
    """
    forwarded = request.headers.get("x-forwarded-for", "")
    parts = [part.strip() for part in forwarded.split(",") if part.strip()]
    if TRUSTED_PROXY_HOPS > 0 and len(parts) >= TRUSTED_PROXY_HOPS:
        return parts[-TRUSTED_PROXY_HOPS]
    if request.client:
        return request.client.host
    return "unknown"


def _hash_ip(ip: str) -> str:
    """Hashes an IP so raw addresses are not kept in memory dumps or logs."""
    return hashlib.sha256(ip.encode()).hexdigest()[:16]


def check_global_cap() -> None:
    """Counts one LLM call against the daily cap.

    Raises:
        HTTPException: 503 when the daily cap is reached (kill switch).
    """
    today = date.today()
    with _lock:
        for old_day in [day for day in _global_counts if day != today]:
            del _global_counts[old_day]
        if _global_counts[today] >= GLOBAL_DAILY_LLM_CALLS:
            raise HTTPException(
                status_code=503,
                detail="Daily capacity reached. Please try again tomorrow.",
            )
        _global_counts[today] += 1


def check_guest_limit(request: Request) -> None:
    """Counts one guest LLM call against the per-IP daily limit.

    Raises:
        HTTPException: 429 when the IP used its daily free runs.
    """
    key = (_hash_ip(client_ip(request)), date.today())
    with _lock:
        for old_key in [k for k in _guest_counts if k[1] != key[1]]:
            del _guest_counts[old_key]
        if _guest_counts[key] >= GUEST_DAILY_LIMIT:
            raise HTTPException(
                status_code=429,
                detail=f"Free limit of {GUEST_DAILY_LIMIT} per day reached. Sign in to continue, or come back tomorrow.",
            )
        _guest_counts[key] += 1


def check_user_limit(user_id: str) -> None:
    """Applies a per-user hourly limit (sliding window) to LLM calls.

    Raises:
        HTTPException: 429 when the user sends too many requests.
    """
    now = time.time()
    with _lock:
        hits = _user_hits[user_id]
        while hits and now - hits[0] > 3600:
            hits.popleft()
        if len(hits) >= USER_HOURLY_LIMIT:
            raise HTTPException(status_code=429, detail="Too many requests. Please slow down.")
        hits.append(now)


def reset_for_tests() -> None:
    """Clears all counters (used by tests)."""
    with _lock:
        _guest_counts.clear()
        _global_counts.clear()
        _user_hits.clear()
