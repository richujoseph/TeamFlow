export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: {
    id: string;
    name: string;
    slug: string;
  };
  is_active: bool;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  items: T[];
  meta: {
    page: number;
    size: number;
    total: number;
    pages: number;
  };
}

export interface ErrorResponse {
  error: string;
  code: string;
  details?: Record<string, string[]>;
}
