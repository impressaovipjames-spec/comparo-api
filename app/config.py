import os
from dotenv import load_dotenv

load_dotenv()

ENABLE_FAKE_ADAPTERS = os.environ.get("ENABLE_FAKE_ADAPTERS", "False").lower() == "true"
