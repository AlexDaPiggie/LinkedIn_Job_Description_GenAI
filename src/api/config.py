"""Shared API settings: allowed web origins and redirect checks."""

from urllib.parse import urlparse

PRODUCTION_ORIGINS = [
    "https://linkedingenai.vercel.app",
    "https://linkedingenai.com",
    "https://www.linkedingenai.com",
    "https://www.linkedingenai.tech",
    "https://linkedingenai-795443191021.us-central1.run.app",
]
LOCAL_HOSTS = {"localhost", "127.0.0.1"}


def is_allowed_redirect(url: str) -> bool:
    """Whether a Stripe return URL points to this site or a local dev server.

    Stops attackers from using the checkout flow to bounce users to another
    site.

    Args:
        url: Candidate return URL.

    Returns:
        True for known production origins and localhost.
    """
    if not url:
        return False
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}"
    if origin in PRODUCTION_ORIGINS:
        return True
    hostname = parsed.hostname or ""
    if parsed.scheme == "https" and hostname.endswith(".hf.space"):
        return True
    return parsed.scheme in ("http", "https") and hostname in LOCAL_HOSTS
