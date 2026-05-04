import threading
import time
import uuid
import requests

# store jobs
jobs = {}

WEBHOOK_URL = "https://webhook.site/c1497919-b7c2-4732-97eb-5566f372aae1"


def generate_report(job_id, data):
    # simulate processing
    time.sleep(5)

    result = {
        "summary": f"Processed report for: {data}"
    }

    jobs[job_id]["status"] = "completed"
    jobs[job_id]["result"] = result

    # send webhook
    try:
        requests.post(WEBHOOK_URL, json={
            "job_id": job_id,
            "status": "completed",
            "result": result
        })
    except Exception as e:
        print("Webhook failed:", e)


def start_job(data):
    job_id = str(uuid.uuid4())

    jobs[job_id] = {
        "status": "processing",
        "result": None
    }

    thread = threading.Thread(target=generate_report, args=(job_id, data))
    thread.start()

    return job_id