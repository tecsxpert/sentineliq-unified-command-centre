"""
Query Response Prompt Template
Used for generating contextual answers based on document retrieval
"""

QUERY_PROMPT = """
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{user_question}

STRICT RULES:
- Do NOT use markdown
- Do NOT use ```
- Do NOT add extra explanation
- Use only the context
- Return ONLY valid JSON

Format:
{{
    "answer": ""
}}
"""
