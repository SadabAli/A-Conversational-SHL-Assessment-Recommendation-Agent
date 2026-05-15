def get_latest_user_message(messages):

    for msg in reversed(messages):

        if msg["role"] == "user":

            return msg["content"]

    return ""


def detect_intent(message):

    message = message.lower()

    comparison_keywords = [
        "compare",
        "difference",
        "vs",
        "versus"
    ]

    refinement_keywords = [
        "also",
        "add",
        "include",
        "instead",
        "change"
    ]

    off_topic_keywords = [
        "movie",
        "politics",
        "legal",
        "weather",
        "cricket"
    ]

    for word in comparison_keywords:

        if word in message:

            return "comparison"

    for word in refinement_keywords:

        if word in message:

            return "refinement"

    for word in off_topic_keywords:

        if word in message:

            return "off_topic"

    if len(message.split()) < 4:

        return "clarification"

    return "recommendation"


def needs_clarification(messages):

    user_text = " ".join([
        msg["content"]
        for msg in messages
        if msg["role"] == "user"
    ]).lower()

    important_keywords = [
        "developer",
        "engineer",
        "manager",
        "sales",
        "leadership",
        "java",
        "python",
        "communication",
        "analyst",
        "personality"
    ]

    score = 0

    for word in important_keywords:

        if word in user_text:

            score += 1

    return score < 2


def generate_clarification_question(messages):

    user_text = " ".join([
        msg["content"]
        for msg in messages
        if msg["role"] == "user"
    ]).lower()

    if "developer" in user_text:

        return (
            "What programming languages "
            "or technologies are required?"
        )

    if "manager" in user_text:

        return (
            "Are you looking for leadership, "
            "personality, or cognitive "
            "assessments?"
        )

    return (
        "Can you share more details about "
        "the role, seniority level, "
        "and required skills?"
    )


def is_prompt_injection(message):

    message = message.lower()

    injection_patterns = [
        "ignore previous instructions",
        "ignore all instructions",
        "act as",
        "system prompt",
        "reveal prompt",
        "bypass",
        "pretend"
    ]

    for pattern in injection_patterns:

        if pattern in message:

            return True

    return False