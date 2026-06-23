from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    status: str
    extracted_text: str | None
    uploaded_by: int
    created_at: datetime

    model_config = {"from_attributes": True}


class DocumentUploadResponse(BaseModel):
    id: int
    title: str
    original_filename: str
    status: str
    message: str
