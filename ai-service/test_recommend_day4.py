"""
Test Recommend Endpoint - Day 4 Work
Builds and validates the /recommend prompt and output structure.
"""

import json
import time
import os
from dotenv import load_dotenv
from routes.recommend import recommend_text

# Load environment
load_dotenv()

TEST_CASES = [
    {
        "id": 1,
        "name": "Login Failure Bug",
        "input": "When I try to login with my email and password, it keeps saying 'Invalid credentials' even though I'm 100% sure my credentials are correct. This happened after the latest update.",
        "expected_priority": "high"
    },
    {
        "id": 2,
        "name": "Dark Mode Feature Request",
        "input": "It would be amazing if we could have a dark mode option. Eye strain during late night usage is real. Maybe add a toggle in settings that switches between light and dark themes automatically.",
        "expected_priority": "medium"
    },
    {
        "id": 3,
        "name": "Performance Issue",
        "input": "The dashboard loads super slow. On my 5G connection it takes like 10 seconds just to see the initial content. I'm running Chrome on MacBook. The network tab shows tons of API calls happening.",
        "expected_priority": "high"
    },
    {
        "id": 4,
        "name": "Export Feature Request",
        "input": "Currently, there's no way to export my data. I need to be able to download reports as CSV or PDF format. This would help with my analysis workflow and help me share data with team members.",
        "expected_priority": "medium"
    },
    {
        "id": 5,
        "name": "UI Feedback",
        "input": "The button colors could be better. The primary action button doesn't stand out enough from the secondary buttons. I had to click around for 30 seconds to figure out which button to press for the main action.",
        "expected_priority": "low"
    }
]


def validate_response(response):
    if not isinstance(response, list):
        return False, ["Response must be a JSON array"]

    if len(response) != 3:
        return False, [f"Response array must contain exactly 3 recommendations, got {len(response)}"]

    issues = []
    for i, item in enumerate(response, 1):
        if not isinstance(item, dict):
            issues.append(f"Recommendation {i} must be an object")
            continue

        if item.get("action_type") not in ["fix", "improve", "investigate", "document", "communicate"]:
            issues.append(f"Recommendation {i} has invalid action_type: {item.get('action_type')}")

        if not isinstance(item.get("description"), str) or not item.get("description", "").strip():
            issues.append(f"Recommendation {i} has invalid description")

        if item.get("priority") not in ["high", "medium", "low"]:
            issues.append(f"Recommendation {i} has invalid priority: {item.get('priority')}")

    return len(issues) == 0, issues


def format_response(response):
    return json.dumps(response, indent=2, ensure_ascii=False)


def run_tests():
    if not os.getenv('GROQ_API_KEY'):
        print("❌ ERROR: GROQ_API_KEY not set in .env file")
        print("Please create .env file with: GROQ_API_KEY=your_key_here")
        return

    print("\n" + "="*80)
    print("🚀 RECOMMEND ENDPOINT - DAY 4 TEST SUITE")
    print("="*80)

    passed = 0
    failed = 0

    for test_case in TEST_CASES:
        print(f"\n---\nTest {test_case['id']}: {test_case['name']}")
        print(f"Input: {test_case['input'][:120]}...")

        response = recommend_text(test_case['input'])
        valid, issues = validate_response(response)

        print("Response:")
        print(format_response(response))

        if valid:
            print("✅ Structure valid")
            passed += 1
        else:
            print("❌ Structure invalid")
            for issue in issues:
                print(f"  - {issue}")
            failed += 1

        time.sleep(0.5)

    print("\n" + "="*80)
    print(f"Test results: {passed}/{len(TEST_CASES)} passed, {failed}/{len(TEST_CASES)} failed")
    print("="*80 + "\n")


if __name__ == '__main__':
    run_tests()
