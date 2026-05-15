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
- Recommend ONLY assessments provided in catalog data.
- NEVER invent assessment names.
- NEVER invent URLs.
- ONLY use retrieved catalog information.
- Refuse unrelated requests.
- Keep answers concise and professional.
- Explain recommendations clearly.
"""


def generate_reply(user_query, retrieved_data):

    prompt = f"""
{SYSTEM_PROMPT}

USER QUERY:
{user_query}

RETRIEVED SHL ASSESSMENTS:
{retrieved_data}

TASK:
- Explain why these assessments fit.
- Stay grounded in retrieved data.
- Keep response under 150 words.
"""

    response = model.generate_content(prompt)

    return response.text