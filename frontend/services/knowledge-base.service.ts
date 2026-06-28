import { API_BASE_URL, knowledgeBaseRoutes } from "@/constants/api";
import { DocumentResponse, DocumentUploadResponse } from "@/types/knowledge-base";

export const knowledgeBaseService = {
  getDocuments: async (): Promise<DocumentResponse[]> => {
    try {
      const response = await fetch(`${API_BASE_URL}${knowledgeBaseRoutes.list}`, {
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
        return Promise.reject(errorResponse?.detail || "Failed to fetch documents.");
      }
    } catch (error) {
      console.error("Error fetching documents:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },

  uploadDocument: async (file: File): Promise<DocumentUploadResponse> => {
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_BASE_URL}${knowledgeBaseRoutes.upload}`, {
        method: "POST",
        credentials: "include",
        // Note: Do not set Content-Type header when sending FormData.
        // The browser will automatically set it to multipart/form-data with the correct boundary.
        body: formData,
      });

      if (response.ok) {
        return response.json();
      } else {
        const errorResponse = await response.json();
        return Promise.reject(errorResponse?.detail || "Failed to upload document.");
      }
    } catch (error) {
      console.error("Error uploading document:", error);
      return Promise.reject("Network error. Please try again later.");
    }
  },
};
