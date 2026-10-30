from app.services.pdf_service import extract_pdf_pages, split_into_chunks
from app.services.rag_service import index_document


def process_document(
    document_id: str,
    filename: str,
    pdf_bytes: bytes,
) -> dict:
    """
    Extract PDF text, split it into chunks, and index the chunks.
    """

    pages = extract_pdf_pages(pdf_bytes)
    chunks = split_into_chunks(pages)

    total_chunks = index_document(
        document_id=document_id,
        filename=filename,
        chunks=chunks,
    )

    return {
        "document_id": document_id,
        "filename": filename,
        "pages_processed": len(pages),
        "chunks_indexed": total_chunks,
    }