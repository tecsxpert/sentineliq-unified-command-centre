import redis
import hashlib
import json

# Connect to Redis
r = redis.Redis(host="localhost", port=6379, db=0, decode_responses=True)

CACHE_TTL = 900  # 15 minutes

# Counters
cache_hits = 0
cache_misses = 0


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