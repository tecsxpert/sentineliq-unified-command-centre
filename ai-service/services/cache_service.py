"""
Day 13: Enhanced Cache Service with Redis Verification
Includes connection verification, error handling, and fallback to in-memory cache
"""
import redis
import hashlib
import json
import os
from dotenv import load_dotenv

load_dotenv()

# ==================== REDIS CONNECTION ====================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 3600))  # 1 hour

# Connection pool for better performance
redis_pool = redis.ConnectionPool(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB,
    decode_responses=True,
    max_connections=10,
    socket_connect_timeout=5,
    socket_keepalive=True,
    socket_keepalive_options={1: 1, 2: 3, 3: 3}
)

r = redis.Redis(connection_pool=redis_pool)

# Fallback in-memory cache (used if Redis unavailable)
_memory_cache = {}
_memory_cache_ttl = {}

# Counters
cache_hits = 0
cache_misses = 0
redis_available = False


def verify_redis_connection():
    """
    Verify Redis connection at startup
    
    Returns:
        dict: Connection status info
    """
    global redis_available
    
    try:
        print("[Cache] Verifying Redis connection...")
        r.ping()
        redis_available = True
        print("[Cache] ✓ Redis connection verified successfully")
        return {
            "status": "connected",
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "message": "Redis is available and working"
        }
    except (redis.ConnectionError, redis.TimeoutError) as e:
        redis_available = False
        print(f"[Cache] ✗ Redis connection failed: {str(e)}")
        print("[Cache] ⚠ Falling back to in-memory cache (not recommended for production)")
        return {
            "status": "failed",
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "error": str(e),
            "message": "Redis unavailable, using in-memory fallback cache",
            "fallback": True
        }
    except Exception as e:
        redis_available = False
        print(f"[Cache] ✗ Unexpected error: {str(e)}")
        return {
            "status": "error",
            "error": str(e),
            "message": "Unexpected error during Redis verification",
            "fallback": True
        }


def generate_key(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()


def get_cache(prompt):
    global cache_hits, cache_misses

    key = generate_key(prompt)
    data = r.get(key)

    if data:
        cache_hits += 1
        return json.loads(data)

    cache_misses += 1
    return None


def set_cache(prompt, response):
    key = generate_key(prompt)
    r.setex(key, CACHE_TTL, json.dumps(response))


def get_cache_stats():
    return {
        "hits": cache_hits,
        "misses": cache_misses
    }