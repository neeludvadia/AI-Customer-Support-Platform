export interface LoginCredentials {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
}

export interface ErrorResponse {
  detail: string;
}
