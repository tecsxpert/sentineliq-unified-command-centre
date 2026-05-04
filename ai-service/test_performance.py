import requests
import time
import statistics

URLS = {
    "categorise": "http://127.0.0.1:8000/categorise",
    "query": "http://127.0.0.1:8000/query",
    "report": "http://127.0.0.1:8000/generate-report"
}

def measure(url, payload):
    times = []

    for _ in range(50):
        start = time.time()

        try:
            requests.post(url, json=payload)
        except:
            continue

        end = time.time()
        times.append((end - start) * 1000)  # ms

    return times


def calculate_metrics(times):
    return {
        "p50": round(statistics.median(times), 2),
        "p95": round(sorted(times)[int(len(times)*0.95)], 2),
        "p99": round(sorted(times)[int(len(times)*0.99)], 2)
    }


def run_test():
    print("\n===== PERFORMANCE TEST =====\n")

    # Categorise
    cat_times = measure(URLS["categorise"], {"text": "App crashes"})
    print("Categorise:", calculate_metrics(cat_times))

    # Query
    query_times = measure(URLS["query"], {"question": "App crashes"})
    print("Query:", calculate_metrics(query_times))

    # Report
    report_times = measure(URLS["report"], {"data": "Test"})
    print("Report:", calculate_metrics(report_times))


if __name__ == "__main__":
    run_test()