from app.repositories.vector_repository import search_chunks
from app.services.llm_service import create_embeddings


def search_document(
    question: str,
    document_id: str | None = None,
    limit: int = 5,
) -> list[dict]:
    """
    Find document passages relevant to a question.
    """

    if not question.strip():
        return []

    query_embedding = create_embeddings([question])[0]

    return search_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        limit=limit,
    )


def get_document_context(
    question: str,
    document_id: str | None = None,
    limit: int = 5,
) -> dict:
    """
    Retrieve relevant passages and format them as research context.
    """

    matches = search_document(
        question=question,
        document_id=document_id,
        limit=limit,
    )

    if not matches:
        return {
            "context": "",
            "sources": [],
        }

    context_parts = []
    sources = []
    seen_texts = set()

    for match in matches:
        normalized_text = " ".join(match["text"].split())

        if not normalized_text or normalized_text in seen_texts:
            continue

        seen_texts.add(normalized_text)
        source_label = f"Source {len(sources) + 1}"

        context_parts.append(
            f"[{source_label}: {match['filename']}, "
            f"page {match['page_number']}]\n"
            f"{match['text']}"
        )

        sources.append(
            {
                "source_label": source_label,
                "document_id": match["document_id"],
                "filename": match["filename"],
                "page_number": match["page_number"],
                "text": match["text"],
            }
        )

    return {
        "context": "\n\n".join(context_parts),
        "sources": sources,
    }