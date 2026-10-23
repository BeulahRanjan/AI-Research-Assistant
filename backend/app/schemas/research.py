
from pydantic import BaseModel, Field


class ResearchQuestion(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=2000,
    )

    document_id: str | None = None
