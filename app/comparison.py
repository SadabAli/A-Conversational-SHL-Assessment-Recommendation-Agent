from app.retriever import search_assessments

from app.llm_service import generate_reply


def compare_assessments(query):

    results = search_assessments(
        query,
        top_k=2
    )

    if len(results) < 2:

        return (
            "Unable to compare "
            "assessments."
        )

    comparison_data = ""

    for item in results:

        comparison_data += f"""
Name:
{item['name']}

Description:
{item['description']}

URL:
{item['url']}

------------------------
"""

    response = generate_reply(
        query,
        comparison_data
    )

    return response