export interface TicketResponse {
  id: number;
  user_id: number;
  conversation_id?: number | null;
  message_id?: number | null;
  question: string;
  status: string;
  created_at: string;
}
