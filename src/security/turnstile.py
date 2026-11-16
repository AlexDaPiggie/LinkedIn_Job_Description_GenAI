"""Cloudflare Turnstile verification (free bot check).

Set `TURNSTILE_SECRET_KEY` to turn it on. When the key is missing the check
passes, so local development works without a Cloudflare account.
"""

import json
import os
import urllib.parse
import urllib.request

from fastapi import HTTPException

VERIFY_URL = "https://challenges.cloudflare.com/turnstile/v0/siteverify"
TIMEOUT_SECONDS = 5


def turnstile_enabled() -> bool:
    """Whether a Turnstile secret key is configured."""
    return bool(os.getenv("TURNSTILE_SECRET_KEY"))


def verify_turnstile(token: str | None, ip: str | None = None) -> None:
    """Verifies a Turnstile token with Cloudflare.

    Args:
        token: Token produced by the widget in the browser.
        ip: Client IP (optional extra signal).

    Raises:
        HTTPException: 400 if the token is missing or invalid, 503 if
            Cloudflare cannot be reached (fails closed).
    """
    secret = os.getenv("TURNSTILE_SECRET_KEY")
    if not secret:
        return
    if not token:
        raise HTTPException(status_code=400, detail="Please complete the human check and try again.")
    fields = {"secret": secret, "response": token}
    if ip and ip != "unknown":
        fields["remoteip"] = ip
    request = urllib.request.Request(
        VERIFY_URL,
        data=urllib.parse.urlencode(fields).encode(),
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            payload = json.loads(response.read().decode())
    except Exception:
        raise HTTPException(status_code=503, detail="Human check unavailable. Please try again shortly.")
    if not payload.get("success"):
        raise HTTPException(status_code=400, detail="Human check failed. Please refresh and try again.")
