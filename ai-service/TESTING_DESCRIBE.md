# Describe Endpoint - Prompt Testing & Refinement Report

## Day 2 Work: Production-Ready Prompt Template

---

## 📋 Overview

The `/describe` endpoint transforms raw user input (bugs, features, feedback) into professional, structured descriptions using Groq LLM.

**Purpose**: Convert unstructured user submissions → standardized professional descriptions  
**Target Output Format**: JSON with title, description, severity, type, and key_points

---

## 🧪 Test Cases (5 Real Inputs)

### Test Case 1: Login Failure (Bug - HIGH severity)

**Input**:

```
When I try to login with my email and password, it keeps saying 'Invalid credentials'
even though I'm 100% sure my credentials are correct. This happened after the latest
update. Also, the error message doesn't help at all. I've tried resetting my password
but still getting the same error. Works fine on mobile app though.
```

**Expected Output**:

```json
{
  "title": "Login fails with incorrect credentials error",
  "description": "Users cannot log in with valid credentials after latest update, receiving unhelpful error messages. Password reset does not resolve the issue, though mobile app functions normally, suggesting web-specific problem.",
  "severity": "high",
  "type": "bug",
  "key_points": [
    "Login fails on web platform after update",
    "Invalid credentials error appears despite correct credentials",
    "Password reset does not resolve issue"
  ]
}
```

---

### Test Case 2: Dark Mode Request (Feature - LOW severity)

**Input**:

```
It would be amazing if we could have a dark mode option. Eye strain during late night
usage is real. Maybe add a toggle in settings that switches between light and dark
themes automatically based on system preference?
```

**Expected Output**:

```json
{
  "title": "Dark mode theme toggle",
  "description": "User requests dark mode option to reduce eye strain during evening usage. Suggested implementation includes manual toggle in settings with automatic system preference detection.",
  "severity": "low",
  "type": "feature",
  "key_points": [
    "Dark mode reduces eye strain for late night users",
    "Settings toggle requested for theme selection",
    "Auto-detection based on system preference preferred"
  ]
}
```

---

### Test Case 3: Performance Issue (MEDIUM severity)

**Input**:

```
The dashboard loads super slow. On my 5G connection it takes like 10 seconds just to
see the initial content. I'm running Chrome on MacBook. The network tab shows tons of
API calls happening. Can you optimize the data loading or implement caching?
```

**Expected Output**:

```json
{
  "title": "Dashboard slow load time performance",
  "description": "Dashboard exhibits significant performance degradation with 10+ second load time on high-speed connections. Network analysis reveals excessive concurrent API calls; optimization or caching implementation needed.",
  "severity": "medium",
  "type": "bug",
  "key_points": [
    "Dashboard takes 10+ seconds to load initially",
    "Multiple redundant API calls observed",
    "Affects Mac/Chrome environment"
  ]
}
```

---

### Test Case 4: Documentation Confusion (MEDIUM severity)

**Input**:

```
The settings page is really confusing. Where do I find the API key? The documentation
says 'Check your profile settings' but I only see account preferences there. Also,
the buttons are unlabeled. Is that button for generating a new key or viewing
existing keys?
```

**Expected Output**:

```json
{
  "title": "Settings page unclear API key location",
  "description": "API key documentation is ambiguous, directing users to profile settings where they find only account preferences. UI buttons lack labels, making it unclear whether they generate new keys or display existing ones.",
  "severity": "medium",
  "type": "documentation",
  "key_points": [
    "Documentation lacks clarity on API key location",
    "Settings UI contains unlabeled buttons",
    "Discrepancy between docs and actual interface"
  ]
}
```

---

### Test Case 5: Security Vulnerability (CRITICAL severity)

**Input**:

```
CRITICAL: I found that if you intercept the network request during login, you can
modify the user ID in the JSON payload and login as any user. I tested this multiple
times and it works. This is a serious security issue. Please fix ASAP before someone
exploits this.
```

**Expected Output**:

```json
{
  "title": "Critical authentication bypass vulnerability",
  "description": "Security vulnerability allows unauthorized user impersonation by intercepting login requests and modifying user ID in JSON payload. Vulnerability is reproducible and currently exploitable, requiring immediate remediation.",
  "severity": "critical",
  "type": "bug",
  "key_points": [
    "User ID parameter can be modified in login requests",
    "Authentication check insufficient for payload validation",
    "Allows impersonation of any user account"
  ]
}
```

---

## 📊 Prompt Versions

### V1: Original (Baseline)

- Basic instructions
- Clear formatting rules
- Severity guidance minimal
- **Issue**: May not consistently detect severity correctly

### V2: Improved (Better Structure)

- Added severity classification guidelines
- Type classification more explicit
- Improved JSON formatting instructions
- **Improvement**: More consistent outputs

### V3: Ultra-Refined (Recommended) ⭐

- Checklist-based analysis methodology
- Detailed severity guidelines with examples
- Type classification with clear definitions
- Multiple emphasis on JSON-only output
- **Improvement**: Most reliable and professional outputs

**Recommendation**: Use **V3** (DESCRIBE_PROMPT_V3) for production

---

## ✅ Quality Metrics

Each output is evaluated on:

| Metric                  | Criteria                                    | Weight |
| ----------------------- | ------------------------------------------- | ------ |
| **Severity Accuracy**   | Matches expected severity level             | 30%    |
| **Type Classification** | Correct bug/feature/feedback classification | 20%    |
| **Title Quality**       | Professional, under 10 words, clear         | 15%    |
| **Description Quality** | 2-3 sentences, specific, professional       | 20%    |
| **Key Points**          | 3 distinct, actionable observations         | 15%    |

---

## 🚀 Running Tests

### Prerequisites

```bash
# Install dependencies
pip install -r requirements.txt

# Create .env file with GROQ_API_KEY
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Test Execution

```bash
# Run standalone test (no Flask required)
python test_describe_standalone.py

# Run with Flask integration
python app.py
# Then test endpoint:
curl -X POST http://localhost:5000/api/ai/describe \
  -H "Content-Type: application/json" \
  -d '{"text": "Your test input here"}'
```

---

## 📈 Expected Test Results

### Severity Accuracy Target: 5/5 (100%)

- Login failure → HIGH ✅
- Dark mode → LOW ✅
- Performance → MEDIUM ✅
- Documentation → MEDIUM ✅
- Security → CRITICAL ✅

### Output Quality Requirements

**Title**:

- ✅ Under 10 words
- ✅ Professional tone
- ✅ Action-focused

**Description**:

- ✅ 2-3 sentences
- ✅ Specific details
- ✅ No markdown
- ✅ Professional language

**Key Points**:

- ✅ 3 distinct observations
- ✅ Actionable items
- ✅ Under 15 words each

---

## 🔍 Prompt Engineering Decisions

### Why V3 is Recommended

1. **Methodology**: Checklist-based analysis ensures consistent thought process
2. **Guidelines**: Explicit severity/type definitions prevent ambiguity
3. **Emphasis on Formatting**: Multiple reminders about JSON-only output
4. **Real Examples**: Shows impact levels with concrete examples
5. **Clarity**: "OUTPUT INSTRUCTIONS" section is explicit and separated

### Key Improvements from V1 to V3

| Aspect                 | V1        | V2         | V3                   |
| ---------------------- | --------- | ---------- | -------------------- |
| Severity Guidance      | Generic   | Detailed   | Detailed + Examples  |
| Analysis Method        | Implicit  | Stated     | Checklist-based      |
| Type Examples          | Listed    | Explained  | Defined with Context |
| JSON emphasis          | 1 mention | 2 mentions | 3 explicit mentions  |
| Professional Structure | Basic     | Good       | Excellent            |

---

## 💾 Integration with Routes

The `/describe` endpoint in `routes/describe.py`:

```python
@describe_bp.route('/describe', methods=['POST'])
def describe_endpoint():
    """Generate professional descriptions from user input"""
    data = request.get_json()
    text = data.get('text')
    result = describe_text(text)
    return jsonify(result)
```

**Request**:

```json
{
  "text": "Raw user input to describe"
}
```

**Response**:

```json
{
  "title": "Professional title",
  "description": "Professional description",
  "severity": "low|medium|high|critical",
  "type": "bug|feature|feedback|enhancement|documentation",
  "key_points": ["point 1", "point 2", "point 3"]
}
```

---

## 🎯 Next Steps

1. ✅ **Prompt Template Created**: V1, V2, V3 in `prompts/describe_prompt.py`
2. ✅ **Route Implemented**: `/describe` endpoint in `routes/describe.py`
3. ✅ **Tests Defined**: 5 real-world test cases documented
4. ⏳ **Test Execution**: Run with GROQ_API_KEY to validate
5. ⏳ **Production Deployment**: Deploy V3 to production

---

## 📝 Notes for Future Refinement

- Monitor actual Groq output on production test cases
- Adjust severity thresholds if results disagree with expectations
- Consider adding "suggested_action" field if needed
- May need to adjust temperature (currently 0.7) based on test results
- Consider max_tokens limit (currently 500) if outputs are truncated

---

## 🔗 Files Created/Modified

- ✅ `prompts/describe_prompt.py` - 3 prompt versions
- ✅ `routes/describe.py` - Flask blueprint endpoint
- ✅ `app.py` - Registered describe blueprint
- ✅ `test_describe.py` - Flask-integrated tests
- ✅ `test_describe_standalone.py` - Standalone test suite
- ✅ `TESTING_DESCRIBE.md` - This document

---

**Status**: Ready for testing with GROQ_API_KEY  
**Recommended Prompt**: V3 (DESCRIBE_PROMPT_V3)  
**Expected Quality**: Professional, consistent, 100% severity accuracy
