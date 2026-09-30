import os

from fastapi import APIRouter
from pydantic import BaseModel
from dotenv import load_dotenv
from google import genai

load_dotenv()

router = APIRouter()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


class LegalQuestion(BaseModel):
    question: str
    country: str = ""
    state: str = ""


@router.post("/api/ask")
def ask_legal_question(data: LegalQuestion):

    prompt = f"""
You are LegalEaseAI, an AI legal information assistant.

The user has asked this legal question:

{data.question}

Country: {data.country}
State: {data.state}

Provide clear, simple, general legal information.
Explain the possible options and steps the user can consider.
Do not claim to be a lawyer.
Mention that laws can vary depending on the user's country or state.
If important information is missing, explain what additional information would be useful.
"""
    print("GEMINI CALL STARTED")

    try:
        response = client.models.generate_content(
            model="gemini-3.5-flash",
            contents=prompt
        )

        return {
            "question": data.question,
            "answer": response.text
        }

    except Exception as e:
        return {
            "error": str(e)
        }