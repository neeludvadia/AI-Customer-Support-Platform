import os
from sqlalchemy.orm import Session
from google import genai
from google.genai import types

from config.settings import settings
from modules.chat.repository import ChatRepository
from modules.chat.models import Conversation, Message


class ChatService:
    def __init__(self, db: Session):
        self.repo = ChatRepository(db)
        
        # Initialize Gemini Client if API key is provided
        api_key = settings.GEMINI_API_KEY
        if not api_key or api_key == "your_gemini_api_key_here":
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)

    def create_conversation(self, user_id: int, title: str | None = None) -> Conversation:
        return self.repo.create_conversation(user_id, title)

    def get_conversation(self, conversation_id: int, user_id: int) -> Conversation | None:
        conversation = self.repo.get_conversation_by_id(conversation_id)
        if not conversation or conversation.user_id != user_id:
            return None
        return conversation

    def list_conversations(self, user_id: int) -> list[Conversation]:
        return self.repo.list_conversations_by_user(user_id)

    def send_message(self, conversation_id: int, user_id: int, content: str) -> Message:
        if not self.client:
            raise ValueError(
                "Gemini API key is not configured. "
                "Please configure GEMINI_API_KEY in your .env file."
            )

        # 1. Verify conversation access
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found or access denied")

        # 2. Save user message to database
        self.repo.create_message(conversation_id, sender="user", content=content)

        # 3. Fetch full message history for Gemini context
        db_messages = self.repo.list_messages_by_conversation(conversation_id)

        # 4. Construct content history for Gemini API
        # Map sender ("user" | "assistant") to Gemini roles ("user" | "model")
        contents = []
        for msg in db_messages:
            role = "user" if msg.sender == "user" else "model"
            contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part(text=msg.content)]
                )
            )

        # 5. Call Gemini API
        try:
            config = types.GenerateContentConfig(
                system_instruction="You are a helpful support assistant."
            )
            response = self.client.models.generate_content(
                model="gemini-2.5-flash",
                contents=contents,
                config=config
            )
            ai_content = response.text or "I am sorry, I could not generate a response."
        except Exception as e:
            ai_content = f"Error communicating with AI service: {str(e)}"

        # 6. Save AI reply to database
        ai_msg = self.repo.create_message(conversation_id, sender="assistant", content=ai_content)

        return ai_msg
