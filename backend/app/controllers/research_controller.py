from app.services.research_service import answer_question


def process_research_question(
    question: str,
    document_id: str | None = None,
) -> dict:
    """
    Coordinate processing of a research question.
    """

    return answer_question(
        question=question,
        document_id=document_id,
    )