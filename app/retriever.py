import json

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

with open(
    "app/catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

documents = []

for item in catalog:

    text = f"""
    {item.get('name', '')}
    {item.get('description', '')}
    {item.get('content', '')}
    """

    documents.append(text)

vectorizer = TfidfVectorizer(
    stop_words="english"
)

tfidf_matrix = vectorizer.fit_transform(
    documents
)


def detect_test_type(text):

    text = text.lower()

    if "personality" in text:
        return "P"

    if "cognitive" in text:
        return "C"

    if "technical" in text:
        return "T"

    if "behavior" in text:
        return "B"

    return "A"


def search_assessments(
    query,
    top_k=5
):

    query_vector = vectorizer.transform(
        [query]
    )

    similarities = cosine_similarity(
        query_vector,
        tfidf_matrix
    ).flatten()

    top_indices = similarities.argsort()[
        ::-1
    ][:top_k]

    results = []

    seen_urls = set()

    for idx in top_indices:

        item = catalog[idx]

        if item["url"] in seen_urls:
            continue

        seen_urls.add(item["url"])

        combined_text = (
            item.get("description", "")
            + " "
            + item.get("content", "")
        )

        results.append({
            "name": item["name"],
            "url": item["url"],
            "description": item["description"],
            "test_type": detect_test_type(
                combined_text
            )
        })

    return results