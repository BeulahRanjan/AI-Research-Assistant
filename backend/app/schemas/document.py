from pydantic import BaseModel, Field


class DocumentUploadResponse(BaseModel):
    message: str
    document_id: str
    filename: str
    pages_processed: int = Field(ge=0)
    chunks_indexed: int = Field(ge=0)


class DocumentSource(BaseModel):
    source_label: str
    document_id: str
    filename: str
    page_number: int = Field(ge=1)
    text: str