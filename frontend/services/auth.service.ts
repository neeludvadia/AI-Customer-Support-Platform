import { API_BASE_URL, authRoutes } from "@/constants/api";
import { LoginCredentials, TokenResponse, RegisterCredentials, UserResponse } from "@/types/auth";

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

  register: async (credentials: RegisterCredentials): Promise<UserResponse> => {
    try {
      const response = await fetch(`${API_BASE_URL}${authRoutes.register}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Accept: "application/json",
        },
        body: JSON.stringify({
          username: credentials.username,
          email: credentials.email,
          password: credentials.password,
        }),
      });

      if (response.ok) {
        return response.json();
      } else {
        const errorResponse = await response.json();
        return Promise.reject(errorResponse?.detail || "Registration failed. Please try again.");
      }
    } catch (error) {
      console.error("Error registering:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },

  logout: async (): Promise<void> => {
    try {
      await fetch(`${API_BASE_URL}${authRoutes.logout}`, {
        method: "POST",
        credentials: "include",
      });
    } catch (error) {
      console.error("Error logging out:", error);
    }
  },
};
