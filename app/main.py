from fastapi import FastAPI

from app.schemas import ChatRequest

from app.retriever import search_assessments

from app.conversation import (
    detect_intent,
    needs_clarification,
    generate_clarification_question,
    is_prompt_injection
)

from app.comparison import compare_assessments

from app.llm_service import generate_reply

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "SHL Assessment API Running"
    }


@app.get("/health")
def health():

    return {
        "status": "ok"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    messages = [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in request.messages
    ]

    latest_message = messages[-1]["content"]

    intent = detect_intent(latest_message)

    # PROMPT INJECTION

    if is_prompt_injection(latest_message):

        return {
            "reply": (
                "I can only assist with "
                "SHL assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # OFF TOPIC

    if intent == "off_topic":

        return {
            "reply": (
                "I can only help with "
                "SHL assessment recommendations."
            ),
            "recommendations": [],
            "end_of_conversation": False
        }

    # COMPARISON

    if intent == "comparison":

        comparison = compare_assessments(
            latest_message
        )

        return {
            "reply": comparison,
            "recommendations": [],
            "end_of_conversation": False
        }

    # CLARIFICATION

    if needs_clarification(messages):

        clarification = (
            generate_clarification_question(
                messages
            )
        )

        return {
            "reply": clarification,
            "recommendations": [],
            "end_of_conversation": False
        }

    # RETRIEVAL

    combined_query = " ".join([
        msg["content"]
        for msg in messages
        if msg["role"] == "user"
    ])

    results = search_assessments(
        combined_query,
        top_k=5
    )

    recommendations = []

    retrieved_text = ""

    for item in results:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": item["test_type"]
        })

        retrieved_text += f"""
Name:
{item['name']}

Description:
{item['description']}

URL:
{item['url']}

----------------------
"""

    reply = generate_reply(
        combined_query,
        retrieved_text
    )

    return {
        "reply": reply,
        "recommendations": recommendations,
        "end_of_conversation": True
    }