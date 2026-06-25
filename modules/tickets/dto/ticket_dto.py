from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TicketResponse(BaseModel):
    id: int
    user_id: int
    conversation_id: Optional[int] = None
    message_id: Optional[int] = None
    question: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}
