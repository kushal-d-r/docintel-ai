def classify_document(text):

    text = text.lower()

    if "aadhaar" in text or "government of india" in text:
        return "Aadhaar Card"

    elif "income tax department" in text:
        return "PAN Card"

    elif "passport" in text:
        return "Passport"

    elif "invoice" in text:
        return "Invoice"

    elif "driving licence" in text or "driving license" in text:
        return "Driving License"

    return "Unknown"