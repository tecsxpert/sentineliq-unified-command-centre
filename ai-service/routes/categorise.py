from fastapi import APIRouter
from services.groq_client import GroqClient

router = APIRouter()
client = GroqClient()

@router.post("/categorise")
def categorise_api(data: dict):
    text = data.get("text", "")

    prompt = f"Categorise this into bug, feature or feedback: {text}"

    result = client.generate_response(prompt)

    response = result.get("response", "")
    meta = result.get("meta", {})

    return {
        "response": response,
        "meta": meta
    }