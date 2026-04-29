import time
from services.chroma_service import collection

# Track app start time
start_time = time.time()

# Store last 10 response times
response_times = []

def record_response_time(duration):
    response_times.append(duration)
    if len(response_times) > 10:
        response_times.pop(0)

def get_health():
    try:
        model_name = "llama-3.3-70b-versatile"

        avg_time = sum(response_times) / len(response_times) if response_times else 0

        chroma_count = collection.count()

        uptime = time.time() - start_time

        cache_stats = {
            "cached_items": len(response_times)
        }

        return {
            "model": model_name,
            "avg_response_time": round(avg_time, 4),
            "chroma_docs": chroma_count,
            "uptime_seconds": round(uptime, 2),
            "cache": cache_stats
        }

    except Exception as e:
        return {
            "error": str(e)
        }