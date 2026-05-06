"""
Describe Prompt Template - Professional Text Description Generation
Production-grade prompt template for standardizing user submissions
"""

# ==================== PRODUCTION PROMPT (V4: FINAL - DAY 3 RELEASE) ====================
DESCRIBE_PROMPT = """
You are a professional technical support classification system. Analyze the user input below 
and generate a standardized, professional description in strict JSON format.

YOUR TASK:
1. Classify the submission type (bug, feature, feedback, enhancement, or documentation)
2. Assess severity based on impact scope and urgency
3. Extract a concise professional title (max 80 characters)
4. Write a clear, specific description (2-3 sentences)
5. Identify 3 key actionable points

SEVERITY CLASSIFICATION RULES:
- CRITICAL: Security vulnerability, data loss, complete app crash, authentication failure
- HIGH: Major feature broken, login/payment issues, significant performance degradation (>5s load)
- MEDIUM: Partial functionality broken, confusing UX, moderate slowness (2-5s), impacting multiple users
- LOW: Visual glitch, minor UX suggestion, cosmetic issue, affecting single user or niche use case

TYPE CLASSIFICATION RULES:
- BUG: System malfunction, unexpected behavior, error message shown
- FEATURE: Request for new capability, new endpoint, new system
- FEEDBACK: User experience observation, quality suggestion, general comment
- ENHANCEMENT: Performance improvement, code cleanup, existing feature improvement
- DOCUMENTATION: Clarity issue, missing documentation, confusing instructions

KEY REQUIREMENTS:
- Output ONLY valid JSON, absolutely no other text
- NO markdown formatting (no **, #, etc)
- NO bullet points or lists in descriptions
- Each title under 80 characters, each description 2-3 sentences
- Key_points array with exactly 3 strings, each under 15 words
- Ensure professional tone throughout

User Submission:
{input_text}

Return this exact JSON structure with no additional text:
{{
    "title": "Concise professional title under 80 characters",
    "description": "First sentence describing what happened. Second sentence describing impact or context. Third sentence with relevant detail if needed.",
    "severity": "critical|high|medium|low",
    "type": "bug|feature|feedback|enhancement|documentation",
    "key_points": [
        "Specific actionable first observation",
        "Specific actionable second observation",
        "Specific actionable third observation"
    ]
}}

Remember: Output ONLY the JSON object, nothing else.
"""


