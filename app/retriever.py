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

    for idx in indices[0]:

        if idx < len(catalog):

            item = catalog[idx]

            results.append({
                "name": item["name"],
                "url": item["url"],
                "description": item["description"]
            })

    return results