def answer_question(question, fields):

    question = question.lower()

    if "name" in question:
        return fields.get("name")

    elif "dob" in question or "birth" in question:
        return fields.get("dob")

    elif "gender" in question:
        return fields.get("gender")

    elif "aadhaar" in question:
        return fields.get("aadhaar_number")

    elif "address" in question:
        return fields.get("address")

    elif "document" in question:
        return fields.get("document_type")

    return "Sorry, I don't know."