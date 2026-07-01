import json
import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


CATALOG_PATH = Path("data/catalog.json")
FAISS_PATH = Path("vectorstore/faiss.index")
METADATA_PATH = Path("vectorstore/metadata.pkl")


def load_catalog():
    with open(CATALOG_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def build_text(assessment):
    """
    Convert one assessment into searchable text.
    """

    return f"""
    Name: {assessment.get('name', '')}

    Description: {assessment.get('description', '')}

    Job Levels: {' '.join(assessment.get('job_levels', []))}

    Assessment Types: {' '.join(assessment.get('keys', []))}

    Duration: {assessment.get('duration', '')}

    Remote: {assessment.get('remote', '')}

    Adaptive: {assessment.get('adaptive', '')}
    """


def main():

    print("=" * 60)
    print("Loading catalog...")
    print("=" * 60)

    catalog = load_catalog()

    print(f"Loaded {len(catalog)} assessments")

    texts = [build_text(item) for item in catalog]

    print("\nLoading embedding model...")

    model = SentenceTransformer("all-MiniLM-L6-v2")

    print("Generating embeddings...")

    embeddings = model.encode(
        texts,
        show_progress_bar=True,
        convert_to_numpy=True
    )

    embeddings = embeddings.astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(embeddings)

    faiss.write_index(index, str(FAISS_PATH))

    with open(METADATA_PATH, "wb") as file:
        pickle.dump(catalog, file)

    print("\n✅ Embeddings created successfully!")
    print(f"Vectors : {index.ntotal}")
    print("Saved:")
    print(" - vectorstore/faiss.index")
    print(" - vectorstore/metadata.pkl")


if __name__ == "__main__":
    main()