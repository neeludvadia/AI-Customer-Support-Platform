from sqlalchemy.orm import Session
from modules.tickets.models import Ticket


class TicketRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        user_id: int,
        question: str,
        conversation_id: int | None = None,
        message_id: int | None = None,
    ) -> Ticket:
        ticket = Ticket(
            user_id=user_id,
            conversation_id=conversation_id,
            message_id=message_id,
            question=question,
            status="open",
        )
        self.db.add(ticket)
        self.db.commit()
        self.db.refresh(ticket)
        return ticket

    def get_by_id(self, ticket_id: int) -> Ticket | None:
        return self.db.query(Ticket).filter(Ticket.id == ticket_id).first()

    def list_by_user(self, user_id: int) -> list[Ticket]:
        return (
            self.db.query(Ticket)
            .filter(Ticket.user_id == user_id)
            .order_by(Ticket.created_at.desc())
            .all()
        )
