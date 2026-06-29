import { API_BASE_URL, systemRoutes } from "@/constants/api";
import { HealthResponse } from "@/types/system";
import { fetchWithAuth } from "@/utils/fetchWithAuth";

export const systemService = {
  getHealth: async (): Promise<HealthResponse> => {
    try {
      const response = await fetchWithAuth(`${API_BASE_URL}${systemRoutes.health}`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
      });

      if (response.ok) {
        return response.json();
      } else {
        const errorResponse = await response.json();
        return Promise.reject(errorResponse?.detail || "Failed to fetch system health.");
      }
    } catch (error) {
      console.error("Error fetching system health:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },
};
