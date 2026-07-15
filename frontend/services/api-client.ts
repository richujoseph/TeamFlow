import axios, { AxiosError, InternalAxiosRequestConfig } from "axios";

// Create Axios instance with base URL
export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1",
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
  // Crucial for sending HttpOnly Secure cookies to the backend
  withCredentials: true,
});

// Request Interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // CSRF token attachment could be handled here if Django requires it,
    // though for JWT in HttpOnly cookies, Django Ninja handles auth silently.
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    return response.data;
  },
  (error: AxiosError) => {
    const customError = {
      message: "An unexpected error occurred",
      status: error.response?.status,
      data: error.response?.data,
    };

    if (error.response?.status === 401) {
      // Handle unauthorized access (e.g., redirect to login)
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(customError);
  }
);
