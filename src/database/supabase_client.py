import os 
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(override=True) #override the local .env var with the global env 

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

#Check if the key exists 
if not SUPABASE_ANON_KEY or not SUPABASE_URL:
    raise RuntimeError ("The URL and KEY of supabase are empty")

#Intialize a client in supabase
supabase: Client = create_client(
    supabase_url=SUPABASE_URL,
    supabase_key=SUPABASE_ANON_KEY,
)