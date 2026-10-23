
import uuid

import chromadb

from app.config import CHROMA_PATH


client = chromadb.PersistentClient(path=str(CHROMA_PATH))

collection = client.get_or_create_collection(
    name="research_documents",
    metadata={"hnsw:space": "cosine"},
)


def add_document_chunks(
    document_id: str,
    filename: str,
    chunks: list[dict],
    embeddings: list[list[float]],
) -> int:
    """Save document chunks, embeddings, and page metadata."""

    ids = [str(uuid.uuid4()) for _ in chunks]

    collection.add(
        ids=ids,
        documents=[chunk["text"] for chunk in chunks],
        embeddings=embeddings,
        metadatas=[
            {
                "document_id": document_id,
                "filename": filename,
                "page_number": chunk["page_number"],
            }
            for chunk in chunks
        ],
    )

    return len(ids)


def search_chunks(
    query_embedding: list[float],
    document_id: str | None = None,
    limit: int = 5,
) -> list[dict]:
    """Find the most relevant passages using vector similarity."""

    total_chunks = collection.count()

    if total_chunks == 0:
        return []

    search_args = {
        "query_embeddings": [query_embedding],
        "n_results": min(limit, total_chunks),
        "include": ["documents", "metadatas", "distances"],
    }

    if document_id:
        search_args["where"] = {"document_id": document_id}

    results = collection.query(**search_args)

    matches = []

    for i, text in enumerate(results["documents"][0]):
        metadata = results["metadatas"][0][i]

        matches.append({
            "text": text,
            "filename": metadata["filename"],
            "page_number": metadata["page_number"],
            "distance": results["distances"][0][i],
            "document_id": metadata["document_id"],
        })

    return matches
