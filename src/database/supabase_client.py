"""Shared Supabase client, configured from environment variables."""

import os

from dotenv import load_dotenv
from supabase import Client, create_client

# Override the local .env values with the global environment.
load_dotenv(override=True)

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Fail fast when credentials are missing.
if not SUPABASE_ANON_KEY or not SUPABASE_URL:
    raise RuntimeError("The URL and KEY of supabase are empty")

# Client used across the app (anon key; row-level security applies).
supabase: Client = create_client(
    supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_ANON_KEY,
)


_service_client: Client | None = None


def get_service_client() -> Client:
    """Returns a Supabase client that uses the service-role key.

    Needed for the credit ledger functions, which are locked away from the
    public anon key so nobody can grant themselves credits. Keep the
    service-role key on the server only.

    Raises:
        RuntimeError: If `SUPABASE_SERVICE_ROLE_KEY` is not set.
    """
    global _service_client
    if _service_client is None:
        key = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
        if not key:
            raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is not set (needed for credits)")
        _service_client = create_client(supabase_url=SUPABASE_URL, supabase_key=key)
    return _service_client
