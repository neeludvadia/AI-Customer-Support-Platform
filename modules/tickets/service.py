from sqlalchemy.orm import Session
from modules.tickets.models import Ticket
from modules.tickets.repository import TicketRepository


class TicketService:
    def __init__(self, db: Session):
        self.repo = TicketRepository(db)

    def create_ticket(
        self,
        user_id: int,
        question: str,
        conversation_id: int | None = None,
        message_id: int | None = None,
    ) -> Ticket:
        """Create an escalation ticket when the AI cannot answer with confidence."""
        return self.repo.create(
            user_id=user_id,
            question=question,
            conversation_id=conversation_id,
            message_id=message_id,
        )

    def get_ticket(self, ticket_id: int) -> Ticket | None:
        return self.repo.get_by_id(ticket_id)

    def list_tickets(self, user_id: int) -> list[Ticket]:
        return self.repo.list_by_user(user_id)
