
from fastapi import APIRouter

router = APIRouter(tags=["Health"])


@router.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Research Assistant API",
    }
