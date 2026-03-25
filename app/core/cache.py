import os
import redis
from dotenv import load_dotenv

load_dotenv()

_redis_client = None

def get_cache():
    global _redis_client
    if _redis_client is None:
        redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
        _redis_client = redis.from_url(redis_url, decode_responses=True)
    return _redis_client

def get(key):
    try:
        return get_cache().get(key)
    except Exception:
        return None

def setex(key, value, ttl=600):
    try:
        get_cache().setex(key, ttl, value)
        return True
    except Exception:
        return False
