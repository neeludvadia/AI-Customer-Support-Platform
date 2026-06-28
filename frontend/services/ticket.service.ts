import { API_BASE_URL, ticketRoutes } from "@/constants/api";
import { TicketResponse } from "@/types/ticket";

export const ticketService = {
  getTickets: async (): Promise<TicketResponse[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}${ticketRoutes.list}`, {
        method: "GET",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      if (response.ok) {
        return response.json();
      } else {
        const errorResponse = await response.json();
        return Promise.reject(errorResponse?.detail || "Failed to fetch tickets.");
      }
    } catch (error) {
      console.error("Error fetching tickets:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },
};
