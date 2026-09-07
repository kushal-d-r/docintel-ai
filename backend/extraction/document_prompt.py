import json

def build_prompt(document_type, schema, ocr_text):

    return f"""
You are an expert Document AI extraction system.

The uploaded document is:

{document_type}

Extract ONLY the information requested below.

Rules:

1. Return ONLY valid JSON.
2. Do NOT explain anything.
3. Missing fields -> empty string.
4. Do not create fields outside the schema.

JSON Schema

{json.dumps(schema, indent=4)}

OCR TEXT

{ocr_text}
"""