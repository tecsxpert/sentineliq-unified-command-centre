import requests

BASE_URL = "http://127.0.0.1:8000"

# 30 demo inputs
test_inputs = [
    "App crashes when login",
    "Add dark mode",
    "UI looks clean",
    "App is slow",
    "Notification feature needed",
    "Login button not working",
    "Improve dashboard",
    "App freezes",
    "Add multi-language",
    "Performance bad",

    "Search not working",
    "Payment failed",
    "App closes automatically",
    "Add user profile",
    "Settings page broken",
    "Loading takes time",
    "Add logout option",
    "App lagging",
    "Improve UX",
    "Add themes",

    "Bug in login",
    "Feature request for reports",
    "UI improvement needed",
    "Crash on startup",
    "Add export feature",
    "Slow response",
    "Improve speed",
    "App hangs",
    "Add analytics",
    "Error in signup"
]


def test_categorise():
    print("\n===== CATEGORY QA =====\n")
    for text in test_inputs:
        res = requests.post(f"{BASE_URL}/categorise", json={"text": text})
        print(f"Input: {text}")
        print("Output:", res.json())
        print("-" * 40)


def test_query():
    print("\n===== QUERY QA =====\n")
    for text in test_inputs:
        res = requests.post(f"{BASE_URL}/query", json={"question": text})
        print(f"Input: {text}")
        print("Output:", res.json())
        print("-" * 40)


if __name__ == "__main__":
    test_categorise()
    test_query()