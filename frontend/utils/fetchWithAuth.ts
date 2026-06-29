import { API_BASE_URL, authRoutes } from "@/constants/api";

let isRefreshing = false;
let refreshSubscribers: ((token: boolean) => void)[] = [];

const subscribeTokenRefresh = (cb: (token: boolean) => void) => {
  refreshSubscribers.push(cb);
};

const onRefreshed = (success: boolean) => {
  refreshSubscribers.forEach((cb) => cb(success));
  refreshSubscribers = [];
};

export const fetchWithAuth = async (url: string, options: RequestInit = {}): Promise<Response> => {
  // Check if body is FormData
  const isFormData = options.body instanceof FormData;

  // Build headers
  const headers: HeadersInit = {
    Accept: "application/json",
    ...options.headers,
  };

  if (!isFormData) {
    (headers as Record<string, string>)["Content-Type"] = "application/json";
  }

  // Ensure credentials are included so cookies are sent
  const fetchOptions: RequestInit = {
    ...options,
    credentials: "include",
    headers,
  };

  const response = await fetch(url, fetchOptions);

  if (response.status === 401) {
    if (!isRefreshing) {
      isRefreshing = true;

      try {
        const refreshResponse = await fetch(`${API_BASE_URL}${authRoutes.refresh}`, {
          method: "POST",
          credentials: "include",
          headers: {
            "Content-Type": "application/json",
            Accept: "application/json",
          },
        });

        if (refreshResponse.ok) {
          isRefreshing = false;
          onRefreshed(true);
          // Retry the original request
          return fetch(url, fetchOptions);
        } else {
          isRefreshing = false;
          onRefreshed(false);
          // Refresh failed, redirect to login
          if (typeof window !== "undefined") {
            window.location.href = "/login";
          }
          return response;
        }
      } catch (error) {
        isRefreshing = false;
        onRefreshed(false);
        if (typeof window !== "undefined") {
          window.location.href = "/login";
        }
        return response;
      }
    } else {
      // If a refresh is already in progress, wait for it to complete
      return new Promise((resolve) => {
        subscribeTokenRefresh((success) => {
          if (success) {
            resolve(fetch(url, fetchOptions));
          } else {
            resolve(response);
          }
        });
      });
    }
  }

  return response;
};
