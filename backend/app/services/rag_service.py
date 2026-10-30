from app.repositories.vector_repository import (
    add_document_chunks,
    search_chunks,
)

from app.services.llm_service import (
    create_embeddings,
    generate_answer,
)


def index_document(
    document_id: str,
    filename: str,
    chunks: list[dict],
) -> int:
    """
    Generate embeddings for document chunks and store them in ChromaDB.
    """

    batch_size = 32
    total_saved = 0

    for start in range(0, len(chunks), batch_size):
        batch = chunks[start:start + batch_size]

        embeddings = create_embeddings(
            [chunk["text"] for chunk in batch]
        )

        total_saved += add_document_chunks(
            document_id=document_id,
            filename=filename,
            chunks=batch,
            embeddings=embeddings,
        )

    return total_saved


def answer_research_question(
    question: str,
    document_id: str | None = None,
) -> dict:
    """
    Retrieve relevant document passages and generate an answer.
    """

    query_embedding = create_embeddings([question])[0]

    matches = search_chunks(
        query_embedding=query_embedding,
        document_id=document_id,
        limit=5,
    )

    if not matches:
        return {
            "answer": (
                "I couldn't find any indexed passages. "
                "Please upload a readable PDF before asking a question."
            ),
            "sources": [],
        }

    # Remove exact duplicate passages while preserving their order.
    unique_matches = []
    seen_texts = set()

    for match in matches:
        normalized_text = " ".join(match["text"].split())

        if not normalized_text or normalized_text in seen_texts:
            continue

        seen_texts.add(normalized_text)
        unique_matches.append(match)

    if not unique_matches:
        return {
            "answer": (
                "No usable text was found in the retrieved passages."
            ),
            "sources": [],
        }

    # Build the context and assign consistent source labels.
    context_parts = []
    sources = []

    for index, match in enumerate(unique_matches, start=1):
        source_label = f"Source {index}"

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

    context = "\n\n".join(context_parts)

    # Generate the answer through the dedicated LLM service.
    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }