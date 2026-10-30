from fastapi import APIRouter, HTTPException

from app.schemas.research import ResearchQuestion
from app.services.rag_service import answer_research_question

router = APIRouter(prefix="/api/research", tags=["Research"])


@router.post("/ask")
def ask_question(request: ResearchQuestion):
    try:
        result = answer_research_question(
            question=request.question,
            document_id=request.document_id,
        )
        return result

    except Exception as exc:
        print(
            f"RESEARCH ERROR: {type(exc).__name__}: {exc}",
            flush=True,
        )
        raise HTTPException(
            status_code=502,
            detail=f"{type(exc).__name__}: {exc}",
        ) from exc