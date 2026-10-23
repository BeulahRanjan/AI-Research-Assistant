
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.services.pdf_service import (
    extract_pdf_pages,
    split_into_chunks,
)
from app.services.rag_service import index_document


router = APIRouter(prefix="/api/documents", tags=["Documents"])

MAX_FILE_SIZE = 15 * 1024 * 1024  # 15 MB


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload a PDF, extract its text, and index its contents."""

    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Please upload a PDF file.",
        )

    pdf_bytes = await file.read()

    if not pdf_bytes:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    if len(pdf_bytes) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="The PDF must be 15 MB or smaller.",
        )

    try:
        pages = extract_pdf_pages(pdf_bytes)
        chunks = split_into_chunks(pages)
    except Exception as exc:
        raise HTTPException(
            status_code=400,
            detail=f"Could not process the PDF: {exc}",
        ) from exc

    document_id = str(uuid4())

    try:
        total_chunks = index_document(
            document_id=document_id,
            filename=file.filename,
            chunks=chunks,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "Could not create embeddings or save the document. "
                "Check your API key, API usage, and server logs."
            ),
        ) from exc

    return {
        "message": "Document uploaded and indexed successfully.",
        "document_id": document_id,
        "filename": file.filename,
        "pages_processed": len(pages),
        "chunks_indexed": total_chunks,
    }
