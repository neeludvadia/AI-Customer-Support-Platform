import { API_BASE_URL, authRoutes } from "@/constants/api";
import { LoginCredentials, TokenResponse } from "@/types/auth";

export const authService = {
  login: async (credentials: LoginCredentials): Promise<TokenResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}${authRoutes.login}`, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          email: credentials.email,
          password: credentials.password,
        }),
      });

      if (response.ok) {
        return response.json();
      } else {
        const errorResponse = await response.json();
        return Promise.reject(errorResponse?.detail || "Invalid credentials. Please try again.");
      }
    } catch (error) {
      console.error("Error logging in:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },
};
