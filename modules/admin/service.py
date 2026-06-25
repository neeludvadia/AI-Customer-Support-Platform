from sqlalchemy.orm import Session
from sqlalchemy import func

from modules.admin.dto.admin_dto import DashboardMetrics
from modules.knowledge_base.models import Document
from modules.chat.models import Conversation, Message
from modules.tickets.models import Ticket


class AdminService:
    def __init__(self, db: Session):
        self.db = db

    def get_metrics(self) -> DashboardMetrics:
        total_documents = self.db.query(func.count(Document.id)).scalar() or 0
        total_conversations = self.db.query(func.count(Conversation.id)).scalar() or 0
        total_messages = self.db.query(func.count(Message.id)).scalar() or 0
        total_tickets = self.db.query(func.count(Ticket.id)).scalar() or 0
        open_tickets = (
            self.db.query(func.count(Ticket.id))
            .filter(Ticket.status == "open")
            .scalar() or 0
        )

        if total_conversations > 0:
            escalation_rate = round((total_tickets / total_conversations) * 100, 2)
        else:
            escalation_rate = 0.0

        return DashboardMetrics(
            total_documents=total_documents,
            total_conversations=total_conversations,
            total_messages=total_messages,
            total_tickets=total_tickets,
            open_tickets=open_tickets,
            escalation_rate=escalation_rate,
        )
