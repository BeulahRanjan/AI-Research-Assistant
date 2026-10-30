from pydantic import BaseModel, Field


class ResearchQuestion(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=2000,
        description="The research question to answer.",
    )

    document_id: str | None = Field(
        default=None,
        description="Optional ID of the document to search.",
    )

    conversation_id: str | None = Field(
        default=None,
        description="ID used to continue an existing conversation.",
    )


class ResearchSource(BaseModel):
    source_label: str
    document_id: str
    filename: str
    page_number: int = Field(ge=1)
    text: str


class ResearchAnswer(BaseModel):
    answer: str
    sources: list[ResearchSource] = Field(default_factory=list)