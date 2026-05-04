"""
Test Describe Endpoint - Test with 5 Real Inputs
Day 2 Work: Test and Refine Prompt Template
"""

import json
import time
from routes.describe import describe_text

# Test inputs with realistic scenarios
TEST_CASES = [
    {
        "id": 1,
        "name": "Login Failure Bug",
        "input": "When I try to login with my email and password, it keeps saying 'Invalid credentials' even though I'm 100% sure my credentials are correct. This happened after the latest update. Also, the error message doesn't help at all. I've tried resetting my password but still getting the same error. Works fine on mobile app though.",
        "expected_severity": "high"
    },
    {
        "id": 2,
        "name": "Dark Mode Feature Request",
        "input": "It would be amazing if we could have a dark mode option. Eye strain during late night usage is real. Maybe add a toggle in settings that switches between light and dark themes automatically based on system preference?",
        "expected_severity": "low"
    },
    {
        "id": 3,
        "name": "Performance Issue",
        "input": "The dashboard loads super slow. On my 5G connection it takes like 10 seconds just to see the initial content. I'm running Chrome on MacBook. The network tab shows tons of API calls happening. Can you optimize the data loading or implement caching?",
        "expected_severity": "medium"
    },
    {
        "id": 4,
        "name": "Documentation Confusion",
        "input": "The settings page is really confusing. Where do I find the API key? The documentation says 'Check your profile settings' but I only see account preferences there. Also, the buttons are unlabeled. Is that button for generating a new key or viewing existing keys?",
        "expected_severity": "medium"
    },
    {
        "id": 5,
        "name": "Security Vulnerability",
        "input": "CRITICAL: I found that if you intercept the network request during login, you can modify the user ID in the JSON payload and login as any user. I tested this multiple times and it works. This is a serious security issue. Please fix ASAP before someone exploits this.",
        "expected_severity": "critical"
    }
]


def format_output(result, test_num):
    """Format test output for readability"""
    print(f"\n{'='*80}")
    print(f"TEST {test_num}: {TEST_CASES[test_num-1]['name']}")
    print(f"{'='*80}")
    print(f"\n📝 INPUT:\n{TEST_CASES[test_num-1]['input']}\n")
    print(f"{'─'*80}")
    print(f"📊 OUTPUT:\n")
    
    if isinstance(result, dict):
        if "error" in result:
            print(f"❌ ERROR: {result['error']}")
        else:
            print(f"✅ Title: {result.get('title', 'N/A')}")
            print(f"📌 Type: {result.get('type', 'N/A')}")
            print(f"🔴 Severity: {result.get('severity', 'N/A')}")
            print(f"\n📄 Description:\n{result.get('description', 'N/A')}")
            print(f"\n🎯 Key Points:")
            for i, point in enumerate(result.get('key_points', []), 1):
                print(f"   {i}. {point}")
    else:
        print(json.dumps(result, indent=2))


def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*80)
    print("🧪 DESCRIBE ENDPOINT - PROMPT REFINEMENT TEST SUITE")
    print("="*80)
    
    results = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"\n⏳ Running Test {i}/5...")
        time.sleep(0.5)  # Small delay between API calls
        
        result = describe_text(test_case["input"])
        format_output(result, i)
        
        results.append({
            "test_num": i,
            "test_name": test_case["name"],
            "expected_severity": test_case["expected_severity"],
            "actual_result": result
        })
    
    # Summary Report
    print(f"\n\n{'='*80}")
    print("📋 TEST SUMMARY REPORT")
    print(f"{'='*80}\n")
    
    severity_matches = 0
    for result in results:
        expected = result["expected_severity"]
        actual = result["actual_result"].get("severity", "unknown")
        match = "✅ PASS" if expected == actual else f"⚠️ MISMATCH (expected: {expected}, got: {actual})"
        print(f"Test {result['test_num']} ({result['test_name']}): {match}")
        if expected == actual:
            severity_matches += 1
    
    print(f"\n📊 Severity Accuracy: {severity_matches}/5 ({(severity_matches/5)*100:.0f}%)")
    
    # Quality Checks
    print(f"\n{'─'*80}")
    print("🔍 OUTPUT QUALITY CHECKS:\n")
    
    for i, result in enumerate(results, 1):
        res = result["actual_result"]
        checks = []
        
        # Check title length
        title_len = len(res.get('title', ''))
        if 5 <= title_len <= 80:
            checks.append("✅ Title length appropriate")
        else:
            checks.append(f"⚠️ Title length issue ({title_len} chars)")
        
        # Check description
        desc = res.get('description', '')
        sentences = len([s for s in desc.split('.') if s.strip()])
        if 2 <= sentences <= 4:
            checks.append("✅ Description sentence count good")
        else:
            checks.append(f"⚠️ Description has {sentences} sentences")
        
        # Check key points
        key_points = res.get('key_points', [])
        if 3 <= len(key_points) <= 5:
            checks.append("✅ Key points count appropriate")
        else:
            checks.append(f"⚠️ Key points count is {len(key_points)}")
        
        # Check markdown (should not be present)
        full_response = json.dumps(res)
        has_markdown = any(char in full_response for char in ['**', '__', '##', '```', '- ', '* '])
        if not has_markdown:
            checks.append("✅ No markdown formatting")
        else:
            checks.append("❌ Contains markdown formatting")
        
        print(f"Test {i}:")
        for check in checks:
            print(f"  {check}")
    
    return results


if __name__ == '__main__':
    # Load environment and initialize
    import os
    from dotenv import load_dotenv
    
    load_dotenv()
    
    if not os.getenv('GROQ_API_KEY'):
        print("❌ ERROR: GROQ_API_KEY not set in .env file")
        print("Please create .env file with: GROQ_API_KEY=your_key_here")
        exit(1)
    
    # Run tests
    results = run_all_tests()
    
    print(f"\n{'='*80}")
    print("✅ TEST RUN COMPLETE")
    print("="*80)
