
from fastapi import APIRouter, HTTPException

from app.schemas.research import ResearchQuestion
from app.services.rag_service import answer_research_question


router = APIRouter(prefix="/api/research", tags=["Research"])


@router.post("/ask")
def ask_question(request: ResearchQuestion):
    """Answer a question using retrieved document passages."""

    try:
        result = answer_research_question(
            question=request.question,
            document_id=request.document_id,
        )

        return result

    except Exception as exc:
        raise HTTPException(
            status_code=502,
            detail=(
                "The research request failed. Check your API key, "
                "API usage, and backend logs."
            ),
        ) from exc
