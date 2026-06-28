export interface ConversationResponse {
  id: number;
  user_id: number;
  title: string | null;
  created_at: string;
  updated_at: string;
}

export interface Citation {
  document_id: number;
  title: string;
  filename: string;
  page: number;
}

export interface MessageResponse {
  id: number;
  conversation_id: number;
  sender: string;
  content: string;
  citations: Citation[];
  ticket_id: number | null;
  created_at: string;
}

export interface ConversationDetailResponse extends ConversationResponse {
  messages: MessageResponse[];
}
