import re

def extract_fields(text):
    data = {
        "document_type": None,
        "name": None,
        "dob": None,
        "gender": None,
        "aadhaar_number": None,
        "address": None
    }

    lines = [line.strip() for line in text.split("\n") if line.strip()]

    # Document Type
    if "Government of India" in text:
        data["document_type"] = "Aadhaar"

    # DOB
    dob = re.search(r"\d{2}/\d{2}/\d{4}", text)
    if dob:
        data["dob"] = dob.group()

    # Gender
    if "Male" in text:
        data["gender"] = "Male"
    elif "Female" in text:
        data["gender"] = "Female"

    # Aadhaar Number
    aadhaar = re.search(r"\d{4}\s\d{4}\s\d{4}", text)
    if aadhaar:
        data["aadhaar_number"] = aadhaar.group()

    # Name (simple heuristic)
    for i, line in enumerate(lines):
        if "Government of India" in line and i + 1 < len(lines):
            data["name"] = lines[i + 1]
            break

    return data