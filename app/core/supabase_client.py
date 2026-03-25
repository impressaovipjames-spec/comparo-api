import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

def get_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    
    if not url or not key:
        # In development, we might not have these yet, so we return None or handle gracefully
        print("Warning: SUPABASE_URL or SUPABASE_KEY not found in environment.")
        
    return create_client(url, key) if url and key else None
