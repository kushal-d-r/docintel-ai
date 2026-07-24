from fastapi import APIRouter, UploadFile, File
import os
import shutil
import json

from backend.qa.qa import answer_question
from backend.schemas import QuestionRequest

from backend.ocr import extract_text, extract_text_with_boxes
from backend.extraction.parser import extract_fields

router = APIRouter()

UPLOAD_FOLDER = "backend/uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    # Save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(filepath, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Perform OCR
    words, boxes = extract_text_with_boxes(filepath)

    text = " ".join(words)

    # Extract structured fields
    fields = extract_fields(text)
    
    
    # Create output directory
    OUTPUT_FOLDER = "outputs/json"
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Save extracted fields as JSON
    json_filename = os.path.splitext(file.filename)[0] + ".json"
    json_path = os.path.join(OUTPUT_FOLDER, json_filename)

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(fields, f, indent=4, ensure_ascii=False)
    
    # Return response
    return {
    "ocr_text": text,
    "words": words,
    "boxes": boxes,
    "fields": fields
}
    
    
@router.post("/ask")
async def ask_question(request: QuestionRequest):

    answer = answer_question(
        request.question,
        request.fields
    )

    return {
        "question": request.question,
        "answer": answer
    }