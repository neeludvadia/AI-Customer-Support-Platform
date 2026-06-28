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
        retrieved_chunks: list[dict] = []

        for i, msg in enumerate(db_messages):
            role = "user" if msg.sender == "user" else "model"

            # Augment the last user message with relevant context from the knowledge base
            if i == len(db_messages) - 1 and role == "user":
                context_str = ""
                try:
                    from modules.knowledge_base.vector_store import VectorStoreHelper
                    vector_store = VectorStoreHelper()
                    query_vector = vector_store.embed_query(content)
                    retrieved_chunks = vector_store.search_similar_chunks(query_vector, top_k=3)
                    if retrieved_chunks:
                        context_str = "Relevant Context from Knowledge Base:\n"
                        for chunk in retrieved_chunks:
                            context_str += f"- From Document '{chunk['title']}': {chunk['text']}\n"
                except Exception as e:
                    print(f"Error retrieving context from vector store: {e}")

                augmented_text = msg.content
                if context_str:
                    augmented_text = f"{context_str}\nUser Question: {msg.content}"

                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=augmented_text)]
                    )
                )
            else:
                contents.append(
                    types.Content(
                        role=role,
                        parts=[types.Part(text=msg.content)]
                    )
                )

        # 5. Detect low confidence BEFORE calling Gemini
        CONFIDENCE_THRESHOLD = 0.60
        low_confidence = (
            not retrieved_chunks
            or max(c.get("score", 0) for c in retrieved_chunks) < CONFIDENCE_THRESHOLD
        )

        ai_content = ""
        
        # 6. Call Gemini API ONLY if we have confident context
        if not low_confidence:
            try:
                config = types.GenerateContentConfig(
                    system_instruction=(
                        "You are a helpful support assistant. Answer the user's question "
                        "using the provided context from the knowledge base. "
                    )
                )
                response = self.client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=contents,
                    config=config
                )
                ai_content = response.text or "I am sorry, I could not generate a response."
            except Exception as e:
                ai_content = f"Error communicating with AI service: {str(e)}"

        # 7. Build deduplicated citations from retrieved chunks
        seen: set[tuple] = set()
        citations: list[dict] = []
        for chunk in retrieved_chunks:
            doc_id = chunk.get("document_id")
            page = chunk.get("page_number")
            filename = chunk.get("original_filename")
            title = chunk.get("title")
            if doc_id is None or page is None:
                continue
            key = (doc_id, page)
            if key not in seen:
                seen.add(key)
                citations.append({
                    "document_id": doc_id,
                    "title": title or "",
                    "filename": filename or "",
                    "page": page,
                })

        # 8. Escalate to a ticket if low confidence
        ticket_id: int | None = None
        if low_confidence:
            try:
                from modules.tickets.service import TicketService
                ticket = TicketService(self.repo.db).create_ticket(
                    user_id=user_id,
                    question=content,
                    conversation_id=conversation_id,
                )
                ticket_id = ticket.id
                ai_content = (
                    "I wasn't able to find a confident answer in our documentation. "
                    "To ensure you get the right help, I have automatically escalated this to a support agent. "
                    f"(Ticket #{ticket_id})"
                )
            except Exception as te:
                print(f"Error creating escalation ticket: {te}")
                ai_content = "I couldn't find an answer in the documentation, and there was an error creating a support ticket. Please try again later."

        # 8. Save AI reply to database (with citations + optional ticket_id)
        ai_msg = self.repo.create_message(
            conversation_id,
            sender="assistant",
            content=ai_content,
            citations=citations if citations else None,
            ticket_id=ticket_id,
        )

        return ai_msg

