def detect_intent(message):

    message = message.lower()

    if "difference" in message or "compare" in message:
        return "comparison"

    if len(message.split()) < 3:
        return "clarification"

    return "recommendation"