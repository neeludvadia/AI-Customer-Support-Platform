import os
from sqlalchemy.orm import Session

from modules.chat.repository import ChatRepository
from modules.chat.models import Conversation, Message
from modules.ai.ports import LLMProvider, VectorStoreProvider


class ChatService:
    def __init__(self, db: Session, llm: LLMProvider | None = None, vector_store: VectorStoreProvider | None = None):
        self.repo = ChatRepository(db)
        self.llm = llm
        self.vector_store = vector_store

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
        if not self.llm or not self.vector_store:
            raise ValueError("AI providers are not configured. Cannot send message.")

        # 1. Verify conversation access
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found or access denied")

        # 2. Save user message to database
        self.repo.create_message(conversation_id, sender="user", content=content)

        # 3. Fetch full message history for context
        db_messages = self.repo.list_messages_by_conversation(conversation_id)

        # 4. Search Knowledge Base using the VectorStore
        # We need an EmbeddingProvider to embed the query first
        from modules.ai.dependencies import get_embedding_provider
        embedding_provider = get_embedding_provider()
        
        try:
            query_vector = embedding_provider.embed_texts([content])[0]
            retrieved_chunks = self.vector_store.search_similar(query_vector, top_k=3)
        except Exception as e:
            print(f"Error retrieving context from vector store: {e}")
            retrieved_chunks = []

        # 5. Build conversation history as a generic list of dicts
        messages = []
        for i, msg in enumerate(db_messages):
            # Augment the last user message with context
            if i == len(db_messages) - 1 and msg.sender == "user":
                context_str = ""
                if retrieved_chunks:
                    context_str = "Relevant Context from Knowledge Base:\n"
                    for chunk in retrieved_chunks:
                        context_str += f"- From Document '{chunk['title']}': {chunk['text']}\n"
                
                augmented_text = msg.content
                if context_str:
                    augmented_text = f"{context_str}\nUser Question: {msg.content}"
                
                messages.append({"sender": msg.sender, "text": augmented_text})
            else:
                messages.append({"sender": msg.sender, "text": msg.content})

        # 6. Detect low confidence
        CONFIDENCE_THRESHOLD = 0.60
        low_confidence = (
            not retrieved_chunks
            or max(c.get("score", 0) for c in retrieved_chunks) < CONFIDENCE_THRESHOLD
        )

        ai_content = ""
        
        # 7. Generate Response using the LLM Provider
        if not low_confidence:
            system_instruction = (
                "You are a helpful support assistant. Answer the user's question "
                "using the provided context from the knowledge base. "
            )
            ai_content = self.llm.generate_response(system_instruction, messages)

        # 8. Build deduplicated citations
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

        # 9. Escalate to a ticket if low confidence
        ticket_id: int | None = None
        if low_confidence:
            ai_content = "I wasn't able to find a confident answer in our documentation. Would you like me to connect you to a support agent?"
            citations = []

        # 10. Save AI reply to database
        ai_msg = self.repo.create_message(
            conversation_id,
            sender="assistant",
            content=ai_content,
            citations=citations if citations else None,
            ticket_id=ticket_id,
        )

        return ai_msg

    def escalate_conversation(self, conversation_id: int, user_id: int) -> Message:
        conversation = self.get_conversation(conversation_id, user_id)
        if not conversation:
            raise ValueError("Conversation not found")

        # Find the last user message and last assistant message
        db_messages = self.repo.list_messages_by_conversation(conversation_id)
        last_user_msg = None
        last_assistant_msg = None
        for msg in reversed(db_messages):
            if msg.sender == "user" and not last_user_msg:
                last_user_msg = msg
            elif msg.sender == "assistant" and not last_assistant_msg:
                last_assistant_msg = msg
        
        question = last_user_msg.content if last_user_msg else "User requested escalation"

        from modules.tickets.service import TicketService
        ticket = TicketService(self.repo.db).create_ticket(
            user_id=user_id,
            question=question,
            conversation_id=conversation_id,
        )

        # Update the previous low-confidence message so the UI hides the Escalate button
        if last_assistant_msg:
            self.repo.update_message_ticket_id(last_assistant_msg.id, ticket.id)

        ai_msg = self.repo.create_message(
            conversation_id,
            sender="assistant",
            content=f"I have escalated your request to a support agent. (Ticket #{ticket.id})",
            ticket_id=ticket.id,
        )
        return ai_msg
