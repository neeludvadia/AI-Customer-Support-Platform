export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:3456";

export const authRoutes = {
  login: "/auth/login",
  register: "/auth/register",
  logout: "/auth/logout",
  me: "/auth/me",
};
