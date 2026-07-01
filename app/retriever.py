import pickle
from pathlib import Path

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


FAISS_PATH = Path("vectorstore/faiss.index")
METADATA_PATH = Path("vectorstore/metadata.pkl")


class Retriever:

    def __init__(self):
        print("Loading embedding model...")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        print("Loading FAISS index...")
        self.index = faiss.read_index(str(FAISS_PATH))

        print("Loading metadata...")
        with open(METADATA_PATH, "rb") as file:
            self.metadata = pickle.load(file)

        print("Retriever Ready!")

    def search(self, query, top_k=5):

        query_embedding = self.model.encode(
            [query],
            convert_to_numpy=True
        ).astype(np.float32)

        distances, indices = self.index.search(query_embedding, top_k)

        results = []

        for idx in indices[0]:
            results.append(self.metadata[idx])

        return results


def main():

    retriever = Retriever()

    print("\n" + "=" * 60)

    query = input("Ask your question: ")

    results = retriever.search(query)

    print("\nTop Results")
    print("=" * 60)

    for i, item in enumerate(results, start=1):

        print(f"\n{i}. {item['name']}")
        print(f"Duration : {item['duration']}")
        print(f"Remote   : {item['remote']}")
        print(f"URL      : {item['link']}")


if __name__ == "__main__":
    main()