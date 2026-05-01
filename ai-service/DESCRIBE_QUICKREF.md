# POST /describe - Quick Reference Card

## One-Liner

Transform raw user input into professional descriptions with severity/type classification.

---

## Endpoint

```http
POST http://localhost:5000/api/ai/describe
```

---

## Request

```json
{
  "text": "String 5-5000 characters",
  "use_cache": true
}
```

---

## Response (200 OK)

```json
{
  "title": "String (max 80 chars)",
  "description": "2-3 sentences, no markdown",
  "severity": "critical|high|medium|low",
  "type": "bug|feature|feedback|enhancement|documentation",
  "key_points": ["Point 1", "Point 2", "Point 3"],
  "metadata": {
    "generated_at": "2026-05-01T10:30:45.123456+00:00",
    "processing_ms": 1234,
    "cached": false
  }
}
```

---

## Severity Levels

| Level        | Use Case                                     |
| ------------ | -------------------------------------------- |
| **critical** | Security, crash, auth failure, data loss     |
| **high**     | Major feature broken, login issues, >5s load |
| **medium**   | Partial broken, confusing UX, 2-5s load      |
| **low**      | Visual glitch, minor suggestion, single user |

---

## Type Classification

| Type              | Use Case                                    |
| ----------------- | ------------------------------------------- |
| **bug**           | Something broken or not working             |
| **feature**       | Request for new functionality               |
| **feedback**      | UX observation or suggestion                |
| **enhancement**   | Performance or existing feature improvement |
| **documentation** | Clarity or missing docs issue               |

---

## cURL Examples

### Basic Request

```bash
curl -X POST http://localhost:5000/api/ai/describe \
  -H "Content-Type: application/json" \
  -d '{"text": "Login button not working"}'
```

### With Cache Disabled

```bash
curl -X POST http://localhost:5000/api/ai/describe \
  -H "Content-Type: application/json" \
  -d '{"text": "Please add dark mode", "use_cache": false}'
```

### Pretty Print Response

```bash
curl -s -X POST http://localhost:5000/api/ai/describe \
  -H "Content-Type: application/json" \
  -d '{"text": "App crashes on startup"}' | python -m json.tool
```

---

## Error Responses

| Status  | Scenario                                   |
| ------- | ------------------------------------------ |
| **400** | Missing text, too short (<5), invalid JSON |
| **413** | Text too long (>5000)                      |
| **500** | Server error, Groq API error               |

---

## Response Times

| Scenario     | Time   |
| ------------ | ------ |
| Cold (first) | 1-3s   |
| Cached       | <100ms |
| Validation   | <50ms  |
| Error        | <10ms  |

---

## Python Usage

```python
import requests
import json

url = "http://localhost:5000/api/ai/describe"
payload = {
    "text": "The app crashes when I press save",
    "use_cache": True
}

response = requests.post(url, json=payload)
data = response.json()

print(f"Title: {data.get('title')}")
print(f"Severity: {data.get('severity')}")
print(f"Type: {data.get('type')}")
print(f"Generated: {data['metadata']['generated_at']}")
```

---

## JavaScript Usage

```javascript
const response = await fetch("http://localhost:5000/api/ai/describe", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    text: "Add export to CSV feature",
    use_cache: true,
  }),
});

const data = await response.json();
console.log(`${data.severity.toUpperCase()}: ${data.title}`);
```

---

## Java Usage

```java
RestTemplate rest = new RestTemplate();
Map<String, String> body = new HashMap<>();
body.put("text", "Dashboard too slow");
body.put("use_cache", "true");

ResponseEntity<Map> resp = rest.postForEntity(
  "http://localhost:5000/api/ai/describe",
  body, Map.class
);

if (resp.getStatusCode().is2xxSuccessful()) {
  Map data = resp.getBody();
  System.out.println("Severity: " + data.get("severity"));
}
```

---

## Testing

```bash
# Validate structure
python test_describe_day3.py

# Windows: Full API test suite
describe_api_tests.bat

# Manual test
curl -X POST http://localhost:5000/api/ai/describe \
  -H "Content-Type: application/json" \
  -d '{"text": "Test input here"}'
```

---

## Key Features

✅ Input validation (5-5000 chars)  
✅ Professional prompt template  
✅ Groq LLM integration  
✅ ISO-8601 timestamps  
✅ Response caching  
✅ Quality metrics  
✅ Error handling  
✅ Metadata tracking

---

## Files

| File                         | Purpose                 |
| ---------------------------- | ----------------------- |
| `routes/describe.py`         | Endpoint implementation |
| `prompts/describe_prompt.py` | LLM prompt template     |
| `test_describe_day3.py`      | Validation tests        |
| `describe_api_tests.bat`     | cURL test suite         |
| `API_DESCRIBE_REFERENCE.md`  | Full documentation      |
| `DAY3_WORK_SUMMARY.md`       | Complete summary        |

---

## Status

🟢 **PRODUCTION READY**

---

## See Also

- [API_DESCRIBE_REFERENCE.md](API_DESCRIBE_REFERENCE.md) - Complete API reference
- [DAY3_WORK_SUMMARY.md](DAY3_WORK_SUMMARY.md) - Full implementation summary
- [README.md](README.md) - Project overview
- [app.py](app.py) - Flask application
