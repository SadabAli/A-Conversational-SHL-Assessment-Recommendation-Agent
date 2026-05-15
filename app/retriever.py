import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

index = faiss.read_index(
    "vectorstore/shl.index"
)

with open(
    "app/catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)


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
    top_k=10
):

    embedding = model.encode([query])

    distances, indices = index.search(
        np.array(embedding).astype("float32"),
        top_k
    )

    results = []

    seen_urls = set()

    for idx in indices[0]:

        if idx < len(catalog):

            item = catalog[idx]

            if item["url"] in seen_urls:
                continue

            seen_urls.add(item["url"])

            combined_text = (
                item.get("description", "")
                + " "
                + item.get("content", "")
            )

            test_type = detect_test_type(
                combined_text
            )

            results.append({
                "name": item["name"],
                "url": item["url"],
                "description": item["description"],
                "test_type": test_type
            })

    return results