from sqlalchemy.orm import Session
from modules.chat.models import Conversation, Message


class ChatRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_conversation(self, user_id: int, title: str | None = None) -> Conversation:
        conversation = Conversation(
            user_id=user_id,
            title=title or "New Conversation"
        )
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def get_conversation_by_id(self, conversation_id: int) -> Conversation | None:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()

    def list_conversations_by_user(self, user_id: int) -> list[Conversation]:
        return self.db.query(Conversation).filter(Conversation.user_id == user_id).order_by(Conversation.updated_at.desc()).all()

    def create_message(self, conversation_id: int, sender: str, content: str) -> Message:
        message = Message(
            conversation_id=conversation_id,
            sender=sender,
            content=content
        )
        self.db.add(message)
        
        # Also update conversation's updated_at timestamp
        conversation = self.get_conversation_by_id(conversation_id)
        if conversation:
            from sqlalchemy.sql import func
            conversation.updated_at = func.now()
            
        self.db.commit()
        self.db.refresh(message)
        return message

    def list_messages_by_conversation(self, conversation_id: int) -> list[Message]:
        return self.db.query(Message).filter(Message.conversation_id == conversation_id).order_by(Message.created_at.asc()).all()
