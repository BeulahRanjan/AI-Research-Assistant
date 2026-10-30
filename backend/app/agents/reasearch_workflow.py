from app.agents.tools import get_document_context
from app.services.llm_service import generate_answer


def run_research_workflow(
    question: str,
    document_id: str | None = None,
) -> dict:
    """
    Retrieve relevant document passages and generate a grounded answer.
    """

    if not question or len(question.strip()) < 3:
        raise ValueError("Please enter a question containing at least 3 characters.")

    retrieval = get_document_context(
        question=question,
        document_id=document_id,
        limit=5,
    )

    context = retrieval["context"]
    sources = retrieval["sources"]

    if not context:
        return {
            "answer": (
                "I couldn't find relevant passages in the indexed documents. "
                "Please upload a readable PDF or try another question."
            ),
            "sources": [],
        }

    answer = generate_answer(
        question=question,
        context=context,
    )

    return {
        "answer": answer,
        "sources": sources,
    }