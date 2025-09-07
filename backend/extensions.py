import os
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# Load environment variables from .env file
load_dotenv()

# Initialize SQLAlchemy
db = SQLAlchemy()

# Get Supabase credentials from environment variables (optional)
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_SERVICE_KEY")

# Create Supabase client only if credentials are available
supabase = None
if url and key:
    try:
        from supabase import create_client, Client
        supabase: Client = create_client(url, key)
        print("✅ Supabase client initialized successfully!")
    except Exception as e:
        print(f"Warning: Could not initialize Supabase client: {e}")
        supabase = None
else:
    print("Warning: Supabase credentials not found. Running without Supabase integration.")
    print(f"URL: {url}")
    print(f"Key: {'SET' if key else 'NOT SET'}")