from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil
import json

from backend.qa.qa import answer_question
from backend.schemas import QuestionRequest
from backend.ocr import extract_text_with_boxes
from backend.extraction.llm_extractor import extract_using_llm
from backend.utils.visualizer import draw_boxes

from backend.search.embedding import (
    generate_embedding,
    generate_query_embedding
)
from backend.search.faiss_index import DocumentIndex


router = APIRouter()

# ==========================================================
# Initialize FAISS
# ==========================================================

document_index = DocumentIndex()

# ==========================================================
# Folders
# ==========================================================

UPLOAD_FOLDER = "backend/uploads"
OUTPUT_FOLDER = "outputs/json"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================================================
# Upload API
# ==========================================================

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):

    try:

        # --------------------------------------------------
        # Save Uploaded File
        # --------------------------------------------------

        filepath = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(
                file.file,
                buffer
            )

        # --------------------------------------------------
        # OCR
        # --------------------------------------------------

        words, boxes = extract_text_with_boxes(filepath)

        ocr_text = " ".join(words)

        # --------------------------------------------------
        # LLM Extraction
        # --------------------------------------------------

        fields = extract_using_llm(ocr_text)

        # --------------------------------------------------
        # Generate Embedding
        # --------------------------------------------------

        embedding = generate_embedding(fields)

        # --------------------------------------------------
        # Add Document to FAISS
        # --------------------------------------------------

        document_index.add_document(
            embedding=embedding,
            fields=fields,
            filename=file.filename
        )

        # --------------------------------------------------
        # Highlight Extracted Fields
        # --------------------------------------------------

        highlighted_image = draw_boxes(
            image_path=filepath,
            boxes=boxes,
            words=words,
            fields=fields
        )

        # --------------------------------------------------
        # Save JSON
        # --------------------------------------------------

        json_filename = (
            os.path.splitext(file.filename)[0]
            + ".json"
        )

        json_path = os.path.join(
            OUTPUT_FOLDER,
            json_filename
        )

        with open(
            json_path,
            "w",
            encoding="utf-8"
        ) as f:

            json.dump(
                fields,
                f,
                indent=4,
                ensure_ascii=False
            )

        # --------------------------------------------------
        # Response
        # --------------------------------------------------

        return {

            "filename": file.filename,

            "ocr_text": ocr_text,

            "words": words,

            "boxes": boxes,

            "fields": fields,

            "highlighted_image": highlighted_image

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Question Answering API
# ==========================================================

@router.post("/ask")
async def ask_question(request: QuestionRequest):

    try:

        answer = answer_question(
            request.question,
            request.fields
        )

        return {

            "question": request.question,

            "answer": answer

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Semantic Search API
# ==========================================================

@router.get("/search")
async def search_documents(query: str):

    try:

        embedding = generate_query_embedding(query)

        results = document_index.search(
            embedding,
            top_k=5
        )

        return {

            "query": query,

            "results": results

        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )