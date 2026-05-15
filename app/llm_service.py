import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)

SYSTEM_PROMPT = """
You are an SHL assessment recommendation assistant.

STRICT RULES:
- Recommend ONLY assessments provided.
- NEVER invent assessment names.
- NEVER invent URLs.
- Keep responses concise.
"""


def generate_reply(user_query, retrieved_data):

    prompt = f"""
{SYSTEM_PROMPT}

USER QUERY:
{user_query}

RETRIEVED DATA:
{retrieved_data}

TASK:
Explain why these assessments fit.
"""

    try:

        response = model.generate_content(
            prompt
        )

        return response.text

    except Exception as e:

        print(f"Gemini Error: {e}")

        return (
            "Based on your hiring requirements, "
            "these SHL assessments are recommended."
        )