import { API_BASE_URL, adminRoutes } from "@/constants/api";
import { DashboardMetrics } from "@/types/admin";

export const adminService = {
  getMetrics: async (): Promise<DashboardMetrics> => {
    try {
      const response = await fetch(`${API_BASE_URL}${adminRoutes.metrics}`, {
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
        return Promise.reject(errorResponse?.detail || "Failed to fetch admin metrics.");
      }
    } catch (error) {
      console.error("Error fetching metrics:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },
};
