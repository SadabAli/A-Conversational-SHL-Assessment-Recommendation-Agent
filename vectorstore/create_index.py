import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

with open(
    "app/catalog.json",
    "r",
    encoding="utf-8"
) as f:

    catalog = json.load(f)

texts = []

for item in catalog:

    text = f"""
    Assessment Name:
    {item.get("name", "")}

    Description:
    {item.get("description", "")}

    Content:
    {item.get("content", "")}
    """

    texts.append(text)

print("Creating embeddings...")

embeddings = model.encode(
    texts,
    show_progress_bar=True
)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(
    np.array(embeddings).astype("float32")
)

faiss.write_index(
    index,
    "vectorstore/shl.index"
)

print("FAISS index saved")