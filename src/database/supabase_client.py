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
