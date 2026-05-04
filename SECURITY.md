# Security Documentation - SentinelIQ AI Gateway

## 1. Overview
This document outlines the security architecture and measures implemented for the AI Gateway service, which integrates LLM capabilities into the SentinelIQ Unified Command Centre.

## 2. OWASP Top 10 Risks for LLMs
We have addressed the following risks specific to LLMs:
- **LLM01: Prompt Injection**: Prevented via robust middleware detection patterns.
- **LLM02: Insecure Output Handling**: Mitigated by sanitizing AI responses and enforcing structured JSON.
- **LLM06: Sensitive Information Disclosure**: Prevented via PII scrubbing and secure logging practices.
- **LLM07: Insecure Plugin Design**: The AI service operates in a restricted environment with no direct database access.

## 3. Attack Scenarios & Mitigations

| Attack Scenario | Mitigation Strategy |
| --- | --- |
| **XSS via AI Output** | Sanitization of special characters (`<`, `>`, `"`, etc.) in middleware. |
| **Prompt Injection** | RegEx-based detection of "ignore previous instructions" and other patterns. |
| **PII Leakage** | Automated scrubbing of emails, phone numbers, and IPs before calling the AI. |
| **Denial of Service** | Rate limiting (30 req/min default, 10 req/min for report generation). |
| **Unauthorized Access** | JWT validation required for all endpoints (except `/health`). |

## 4. Mitigation Strategies (Detailed)
### Input Sanitisation
All incoming POST requests are processed by a `security_middleware` that strips dangerous characters and detects malicious prompt engineering.

### Rate Limiting
Implemented using `flask-limiter` with a memory-backed store (scalable to Redis). Limits are applied per client IP address.

### PII Scrubbing
A dedicated utility replaces sensitive data patterns with placeholders like `[EMAIL]` or `[PHONE]` to ensure no PII is sent to external LLM providers (Groq).

## 5. Testing Results
- **XSS**: Passed (Sanitizer successfully strips tags).
- **Injection**: Passed (Blocked with 400 Bad Request).
- **Auth**: Passed (401 returned without valid JWT).
- **PII**: Passed (Sensitive data scrubbed in requests).
- **Rate Limit**: Passed (429 returned on excess requests).

## 6. Residual Risks
- **Evolving Injections**: New prompt injection techniques may bypass static RegEx. Continuous monitoring and model-based detection are recommended.
- **Third-party Dependency**: Reliance on Groq API availability. Mitigated by circuit breaker logic in the Spring Boot client.
- **Redis Security**: Ensure the Redis instance is password-protected and not exposed to the public internet.
