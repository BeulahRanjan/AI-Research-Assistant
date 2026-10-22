
import fitz


def extract_pdf_pages(pdf_bytes: bytes) -> list[dict]:
    """Extract text from a PDF while preserving page numbers."""

    pages = []

    with fitz.open(stream=pdf_bytes, filetype="pdf") as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                pages.append({
                    "page_number": page_number,
                    "text": text,
                })

    if not pages:
        raise ValueError(
            "No readable text found. This PDF may be scanned or empty."
        )

    return pages


def split_into_chunks(
    pages: list[dict],
    chunk_size: int = 1000,
    overlap: int = 150,
) -> list[dict]:
    """Split page text into smaller overlapping pieces."""

    if chunk_size <= 0 or overlap < 0 or overlap >= chunk_size:
        raise ValueError("Invalid chunk size or overlap.")

    chunks = []

    for page in pages:
        text = page["text"]
        start = 0

        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk_text = text[start:end].strip()

            if chunk_text:
                chunks.append({
                    "page_number": page["page_number"],
                    "text": chunk_text,
                })

            if end == len(text):
                break

            start = end - overlap

    return chunks
