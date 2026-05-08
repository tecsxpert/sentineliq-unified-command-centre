"""
Day 13: Enhanced Cache Service with Redis Verification
Includes connection verification, error handling, and fallback to in-memory cache
"""
try:
    import redis
except ImportError:
    redis = None

import hashlib
import json
import os
import time
from dotenv import load_dotenv

load_dotenv()

# ==================== REDIS CONNECTION ====================

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
REDIS_DB = int(os.getenv("REDIS_DB", 0))
CACHE_TTL = int(os.getenv("CACHE_TTL_SECONDS", 3600))  # 1 hour

r = None
if redis is not None:
    try:
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
    except Exception:
        r = None

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
        if r is None:
            raise RuntimeError("Redis client not available")

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
    except (AttributeError, RuntimeError, Exception) as e:
        redis_available = False
        message = str(e)
        print(f"[Cache] ✗ Redis connection failed: {message}")
        print("[Cache] ⚠ Falling back to in-memory cache (not recommended for production)")
        return {
            "status": "failed",
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "error": message,
            "message": "Redis unavailable, using in-memory fallback cache",
            "fallback": True
        }


def generate_key(prompt):
    return hashlib.sha256(prompt.encode()).hexdigest()


def _cleanup_memory_cache():
    now = time.time()
    expired = [key for key, expiry in _memory_cache_ttl.items() if expiry <= now]
    for key in expired:
        _memory_cache.pop(key, None)
        _memory_cache_ttl.pop(key, None)


def get_cache(prompt):
    global cache_hits, cache_misses, redis_available

    _cleanup_memory_cache()
    key = generate_key(prompt)
    data = None

    if redis_available:
        try:
            data = r.get(key)
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"[Cache] Redis read failed: {str(e)}")
            redis_available = False

    if data:
        cache_hits += 1
        return json.loads(data)

    # Fallback in-memory cache
    if not redis_available and key in _memory_cache:
        cache_hits += 1
        return _memory_cache[key]

    cache_misses += 1
    return None


def set_cache(prompt, response):
    global redis_available
    key = generate_key(prompt)

    if redis_available:
        try:
            r.setex(key, CACHE_TTL, json.dumps(response))
            return
        except (redis.ConnectionError, redis.TimeoutError) as e:
            print(f"[Cache] Redis write failed: {str(e)}")
            redis_available = False

    # Fallback in-memory cache
    _memory_cache[key] = response
    _memory_cache_ttl[key] = time.time() + CACHE_TTL


def get_cache_stats():
    return {
        "hits": cache_hits,
        "misses": cache_misses
    }