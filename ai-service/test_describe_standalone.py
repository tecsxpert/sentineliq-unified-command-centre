"""
Standalone Test for Describe Prompt Template
Day 2 Work: Test and Refine Prompt - Runs independently of Flask
"""

import json
import time
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment
load_dotenv()

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

# V1 Prompt Template (Current)
DESCRIBE_PROMPT_V1 = """
You are a technical documentation expert. Generate a professional, detailed description 
based on the provided text. The description should be:
- Clear and concise (2-3 sentences)
- Technical but accessible
- Include key technical details if present
- Highlight the main issue/feature/topic
- Written in active voice

STRICT RULES:
- Do NOT use markdown formatting (no **, #, etc)
- Do NOT use bullet points or lists
- Do NOT use code blocks
- Return ONLY valid JSON
- Do NOT add any extra text or explanations

Input Text:
{input_text}

Format your response EXACTLY as:
{{
    "title": "Professional short title (under 10 words)",
    "description": "2-3 sentence professional description",
    "severity": "low|medium|high|critical",
    "type": "bug|feature|feedback|enhancement|documentation",
    "key_points": ["point 1", "point 2", "point 3"]
}}
"""


def test_prompt(prompt_template, version_name):
    """Test prompt template with all 5 test cases"""
    
    api_key = os.getenv('GROQ_API_KEY')
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not set in .env file")
        print("Please create .env file with: GROQ_API_KEY=your_key_here")
        return None
    
    client = Groq(api_key=api_key)
    
    print(f"\n{'='*80}")
    print(f"🧪 TESTING {version_name}")
    print(f"{'='*80}\n")
    
    results = []
    severity_matches = 0
    quality_issues = []
    
    for i, test_case in enumerate(TEST_CASES, 1):
        print(f"⏳ Test {i}/5: {test_case['name']}...", end=" ", flush=True)
        
        try:
            prompt = prompt_template.format(input_text=test_case["input"])
            
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=500
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Try to parse JSON
            try:
                result = json.loads(response_text)
            except json.JSONDecodeError:
                # Try to extract JSON from response
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                if start >= 0 and end > start:
                    result = json.loads(response_text[start:end])
                else:
                    result = {"error": "Could not parse JSON", "raw": response_text}
            
            # Check severity match
            expected_sev = test_case["expected_severity"]
            actual_sev = result.get("severity", "unknown")
            
            if expected_sev == actual_sev:
                severity_matches += 1
                print("✅")
            else:
                print(f"⚠️ (sev: {actual_sev})")
                quality_issues.append(f"Test {i}: Expected {expected_sev}, got {actual_sev}")
            
            results.append({
                "test_num": i,
                "test_name": test_case["name"],
                "expected_severity": expected_sev,
                "result": result
            })
            
            time.sleep(0.3)  # Rate limiting
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            results.append({
                "test_num": i,
                "test_name": test_case["name"],
                "error": str(e),
                "result": None
            })
    
    # Print detailed results
    print(f"\n{'─'*80}")
    print("📊 DETAILED RESULTS:\n")
    
    for result in results:
        print(f"Test {result['test_num']}: {result['test_name']}")
        if "error" not in result and result["result"]:
            res = result["result"]
            if "error" not in res:
                print(f"  Title: {res.get('title', 'N/A')}")
                print(f"  Type: {res.get('type', 'N/A')}")
                print(f"  Severity: {res.get('severity', 'N/A')} (expected: {result['expected_severity']})")
                print(f"  Description: {res.get('description', 'N/A')[:100]}...")
                points = res.get('key_points', [])
                if points:
                    print(f"  Key Points: {', '.join(points[:3])}")
            else:
                print(f"  ERROR: {res.get('error')}")
        else:
            print(f"  ERROR: {result.get('error')}")
        print()
    
    # Summary
    print(f"{'─'*80}")
    print(f"📈 RESULTS SUMMARY:")
    print(f"   Severity Accuracy: {severity_matches}/5 ({(severity_matches/5)*100:.0f}%)")
    print(f"   Response Rate: {len([r for r in results if 'result' in r and r['result']])}/5")
    
    if quality_issues:
        print(f"\n⚠️ Quality Issues Found:")
        for issue in quality_issues:
            print(f"   - {issue}")
    
    return {
        "version": version_name,
        "severity_accuracy": severity_matches,
        "total_tests": len(results),
        "results": results,
        "quality_issues": quality_issues
    }


if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 DESCRIBE ENDPOINT - PROMPT REFINEMENT TEST SUITE")
    print("="*80)
    print("Testing prompt template with 5 real-world inputs...")
    
    # Test V1 (Current)
    v1_results = test_prompt(DESCRIBE_PROMPT_V1, "PROMPT V1 (Current)")
    
    print(f"\n{'='*80}")
    print("✅ TEST RUN COMPLETE")
    print("="*80)
    
    if v1_results:
        print(f"\n📊 FINAL SCORE: {v1_results['severity_accuracy']}/{v1_results['total_tests']} tests passed")
        if v1_results['severity_accuracy'] < 4:
            print("\n💡 Recommendation: Refine prompt for better severity detection")
        else:
            print("\n✅ Prompt is performing well!")
