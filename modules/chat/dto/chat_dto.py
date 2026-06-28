from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class ConversationCreateRequest(BaseModel):
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MessageCreateRequest(BaseModel):
    conversation_id: int
    content: str


class EscalateRequest(BaseModel):
    conversation_id: int


class Citation(BaseModel):
    document_id: int
    title: str
    filename: str
    page: int


class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender: str
    content: str
    citations: Optional[List[Citation]] = None
    ticket_id: Optional[int] = None
    created_at: datetime

    model_config = {"from_attributes": True}


class ConversationDetailResponse(ConversationResponse):
    messages: List[MessageResponse] = []

    model_config = {"from_attributes": True}
