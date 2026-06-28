from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional

from database.database import get_db
from modules.auth.dependencies import get_current_user
from modules.auth.models import User
from modules.chat.dto import (
    ConversationResponse,
    ConversationDetailResponse,
    ConversationCreateRequest,
    MessageCreateRequest,
    MessageResponse,
    EscalateRequest
)
from modules.chat.service import ChatService

router = APIRouter(prefix="/chat", tags=["Chat"])


@router.post("/conversation", response_model=ConversationResponse, status_code=status.HTTP_201_CREATED)
def create_conversation(
    payload: Optional[ConversationCreateRequest] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    title = payload.title if payload else None
    service = ChatService(db)
    return service.create_conversation(user_id=current_user.id, title=title)


@router.post("/message", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def send_message(
    payload: MessageCreateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ChatService(db)
    try:
        ai_msg = service.send_message(
            conversation_id=payload.conversation_id,
            user_id=current_user.id,
            content=payload.content
        )
        return ai_msg
    except ValueError as e:
        # Check if it was an invalid conversation or missing API key
        if "API key" in str(e):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/escalate", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def escalate_conversation(
    payload: EscalateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ChatService(db)
    try:
        return service.escalate_conversation(
            conversation_id=payload.conversation_id,
            user_id=current_user.id
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/history", response_model=List[ConversationResponse])
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ChatService(db)
    return service.list_conversations(user_id=current_user.id)


@router.get("/history/{conversation_id}", response_model=ConversationDetailResponse)
def get_conversation_detail(
    conversation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    service = ChatService(db)
    conversation = service.get_conversation(conversation_id=conversation_id, user_id=current_user.id)
    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")
    return conversation
