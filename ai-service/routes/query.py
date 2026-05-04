from fastapi import APIRouter
from services.groq_client import GroqClient

router = APIRouter()
client = GroqClient()

@router.post("/query")
def query_api(data: dict):
    user_question = data.get("question", "")

    context = "The app crashes when I login. The UI looks clean and modern. Feature request: add dark mode."

    prompt = f"""
    You are an AI assistant.

    STRICT RULES:
    - Answer ONLY using the provided context
    - If answer is not found, say: "No relevant information found"
    - Do NOT guess or assume
    - Keep answer short and clear

    Context:
    {context}

    Question:
    {user_question}

    Return only the answer.
    """

    result = client.generate_response(prompt)

    answer = result.get("response", "")
    meta = result.get("meta", {})

    sources = [
        "The app crashes when I login",
        "The UI looks clean and modern",
        "Feature request: add dark mode"
    ]

    return {
        "answer": answer,
        "sources": sources,
        "meta": meta
    }