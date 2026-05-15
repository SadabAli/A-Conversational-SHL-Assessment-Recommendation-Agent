from fastapi import FastAPI

from app.schemas import ChatRequest
from app.retriever import search_assessments
from app.conversation import detect_intent

app = FastAPI()


@app.get("/health")
def health():

    return {"status": "ok"}


@app.post("/chat")
def chat(request: ChatRequest):

    messages = request.messages

    latest_message = messages[-1].content

    intent = detect_intent(latest_message)

    if intent == "clarification":

        return {
            "reply": "Can you share more details about the role and skills needed?",
            "recommendations": [],
            "end_of_conversation": False
        }

    results = search_assessments(latest_message)

    recommendations = []

    for item in results[:5]:

        recommendations.append({
            "name": item["name"],
            "url": item["url"],
            "test_type": "A"
        })

    return {
        "reply": "Here are recommended SHL assessments.",
        "recommendations": recommendations,
        "end_of_conversation": True
    }