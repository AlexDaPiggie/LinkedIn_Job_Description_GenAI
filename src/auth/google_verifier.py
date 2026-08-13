import os
from google.oauth2 import id_token
from google.auth.transport import requests
from dotenv import load_dotenv

load_dotenv(override=True) #Load global environment variables to local environment
GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")

def verify_google_id_token(token: str):
    if not GOOGLE_CLIENT_ID:
        raise ValueError ("GOOGLE_CLIENT_ID is not configured in environment!")

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            requests.Request(),
            GOOGLE_CLIENT_ID,
        )
        if id_info['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError["Wrong issuer."]

        return id_info['email']

    except Exception as e:
        raise ValueError(f"Invalid Google token: {e}")
    
