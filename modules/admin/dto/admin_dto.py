from pydantic import BaseModel


class DashboardMetrics(BaseModel):
    total_documents: int
    total_conversations: int
    total_messages: int
    total_tickets: int
    open_tickets: int
    escalation_rate: float  # (total_tickets / total_conversations) * 100
