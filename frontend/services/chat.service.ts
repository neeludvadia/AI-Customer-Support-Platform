import { API_BASE_URL, chatRoutes } from "@/constants/api";
import { ConversationResponse, ConversationDetailResponse, MessageResponse } from "@/types/chat";

export const chatService = {
  createConversation: async (title?: string): Promise<ConversationResponse> => {
    const response = await fetch(`${API_BASE_URL}${chatRoutes.conversation}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ title }),
    });
    if (!response.ok) throw new Error("Failed to create conversation");
    return response.json();
  },

  sendMessage: async (conversationId: number, content: string): Promise<MessageResponse> => {
    const response = await fetch(`${API_BASE_URL}${chatRoutes.message}`, {
      method: "POST",
      credentials: "include",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ conversation_id: conversationId, content }),
    });
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.detail || "Failed to send message");
    }
    return response.json();
  },

  getHistory: async (): Promise<ConversationResponse[]> => {
    const response = await fetch(`${API_BASE_URL}${chatRoutes.history}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) throw new Error("Failed to load history");
    return response.json();
  },

  getConversationDetail: async (id: number): Promise<ConversationDetailResponse> => {
    const response = await fetch(`${API_BASE_URL}${chatRoutes.history}/${id}`, {
      method: "GET",
      credentials: "include",
    });
    if (!response.ok) throw new Error("Failed to load conversation details");
    return response.json();
  },
};
