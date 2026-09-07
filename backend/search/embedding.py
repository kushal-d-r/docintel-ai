from sentence_transformers import SentenceTransformer

# Load model only once
MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def build_document_text(fields: dict) -> str:
    """
    Convert extracted JSON into a searchable text string.
    """

    text_parts = []

    for key, value in fields.items():

        if value is None:
            continue

        value = str(value).strip()

        if value == "":
            continue

        text_parts.append(f"{key}: {value}")

    return "\n".join(text_parts)


def generate_embedding(fields: dict):
    """
    Generate embedding vector from extracted document fields.
    """

    document_text = build_document_text(fields)

    embedding = model.encode(
        document_text,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding


def generate_query_embedding(query: str):
    """
    Generate embedding for a search query.
    """

    embedding = model.encode(
        query,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embedding