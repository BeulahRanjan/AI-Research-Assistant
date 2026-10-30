from uuid import uuid4

from fastapi import APIRouter, HTTPException

from app.schemas.research import ResearchQuestion
from app.services.rag_service import answer_research_question
from app.repositories.conversation_repository import (
    save_message,
    get_conversation_history,
)

router = APIRouter(prefix="/api/research", tags=["Research"])


@router.post("/ask")
def ask_question(request: ResearchQuestion):
    conversation_id = request.conversation_id or str(uuid4())

    try:
        # Save the user's question.
        save_message(
            conversation_id=conversation_id,
            role="user",
            content=request.question,
        )

        # Retrieve relevant document passages and generate an answer.
        result = answer_research_question(
            question=request.question,
            document_id=request.document_id,
        )

        answer = result["answer"]

        # Save the assistant's answer.
        save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=answer,
        )

        # Return the answer, sources, and conversation ID.
        return {
            "conversation_id": conversation_id,
            "answer": answer,
            "sources": result.get("sources", []),
        }

    except Exception as exc:
        print(
            f"RESEARCH ERROR: {type(exc).__name__}: {exc}",
            flush=True,
        )

        raise HTTPException(
            status_code=502,
            detail="The research request could not be completed. Please try again.",
        ) from exc


@router.get("/history/{conversation_id}")
def get_history(conversation_id: str):
    try:
        history = get_conversation_history(conversation_id)

        return {
            "conversation_id": conversation_id,
            "messages": history,
        }

    except Exception as exc:
        print(
            f"HISTORY ERROR: {type(exc).__name__}: {exc}",
            flush=True,
        )

        raise HTTPException(
            status_code=500,
            detail="Could not retrieve conversation history.",
        ) from exc