import json
import ollama
import os


OLLAMA_HOST = os.getenv(
    "OLLAMA_HOST",
    "http://localhost:11434"
)

client = ollama.Client(
    host=OLLAMA_HOST
)

from backend.document_schema import DOCUMENT_SCHEMAS
MODEL_NAME = "gemma3:4b"


# ------------------------------------------------------
# Get schema
# ------------------------------------------------------
def get_schema(document_type: str):
    return DOCUMENT_SCHEMAS.get(document_type.upper(), {})


# ------------------------------------------------------
# Detect document type
# ------------------------------------------------------
def detect_document_type(ocr_text: str):

    prompt = f"""
You are an expert document classifier.

Identify the document type from the OCR text.

Possible document types:

AADHAAR
PAN
PASSPORT
DRIVING_LICENSE
VOTER_ID

Rules:

Return ONLY one of the above words.

No explanation.

OCR TEXT:

{ocr_text}
"""

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    document_type = (
        response["message"]["content"]
        .strip()
        .upper()
        .replace(" ", "_")
    )

    if document_type not in DOCUMENT_SCHEMAS:
        document_type = "AADHAAR"

    return document_type


# ------------------------------------------------------
# Extract Information
# ------------------------------------------------------
def extract_using_llm(ocr_text: str):

    document_type = detect_document_type(ocr_text)

    schema = get_schema(document_type)

    prompt = f"""
You are an expert AI Document Information Extraction System.

The uploaded document has already been classified as:

{document_type}

Your job is to extract ONLY the fields listed below.

Return ONLY valid JSON.

Do NOT write markdown.

Do NOT write explanations.

If a value is unavailable return "".

Schema:

{json.dumps(schema, indent=4)}

OCR TEXT:

{ocr_text}
"""

    response = client.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        options={
            "temperature": 0
        }
    )

    content = response["message"]["content"].strip()

    # Remove markdown if present
    if content.startswith("```json"):
        content = content.replace("```json", "")

    if content.startswith("```"):
        content = content.replace("```", "")

    content = content.replace("```", "").strip()

    try:

        data = json.loads(content)

    except Exception:

        print("\n========== GEMMA RAW OUTPUT ==========\n")
        print(content)
        print("\n======================================\n")

        data = schema.copy()

    # Guarantee all fields exist
    for key in schema:
        if key not in data:
            data[key] = ""

    data["document_type"] = document_type

    return data