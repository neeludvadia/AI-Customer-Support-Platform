export interface DocumentResponse {
  id: number;
  title: string;
  original_filename: string;
  status: string;
  extracted_text: string | null;
  uploaded_by: number;
  created_at: string;
}

export interface DocumentUploadResponse {
  id: number;
  title: string;
  original_filename: string;
  status: string;
  message: string;
}
