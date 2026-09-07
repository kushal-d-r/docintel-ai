import os
import json
import faiss
import numpy as np

INDEX_FILE = "outputs/faiss/document.index"
METADATA_FILE = "outputs/faiss/metadata.json"

os.makedirs("outputs/faiss", exist_ok=True)

DIMENSION = 384


class DocumentIndex:

    def __init__(self):

        if os.path.exists(INDEX_FILE):

            self.index = faiss.read_index(INDEX_FILE)

        else:

            self.index = faiss.IndexFlatIP(DIMENSION)

        if os.path.exists(METADATA_FILE):

            with open(METADATA_FILE, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        else:

            self.metadata = []

    # ---------------------------------------
    # Save FAISS index
    # ---------------------------------------

    def save(self):

        faiss.write_index(
            self.index,
            INDEX_FILE
        )

        with open(
            METADATA_FILE,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                self.metadata,
                f,
                indent=4,
                ensure_ascii=False
            )

    # ---------------------------------------
    # Add Document
    # ---------------------------------------

    def add_document(
        self,
        embedding,
        fields,
        filename
    ):

        embedding = np.array(
            [embedding],
            dtype=np.float32
        )

        self.index.add(
            embedding
        )

        self.metadata.append(
            {
                "filename": filename,
                "fields": fields
            }
        )

        self.save()

    # ---------------------------------------
    # Search
    # ---------------------------------------

    def search(
        self,
        embedding,
        top_k=5
    ):

        embedding = np.array(
            [embedding],
            dtype=np.float32
        )

        scores, indices = self.index.search(
            embedding,
            top_k
        )

        results = []

        for score, idx in zip(
            scores[0],
            indices[0]
        ):

            if idx == -1:
                continue

            results.append(
                {
                    "score": float(score),
                    "filename": self.metadata[idx]["filename"],
                    "fields": self.metadata[idx]["fields"]
                }
            )

        return results