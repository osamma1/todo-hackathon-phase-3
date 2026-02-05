// API client with auto JWT handling from Better Auth
import { createAuthClient } from 'better-auth/client';

// Define types for our API responses
export interface User {
  id: string | number;
  email: string;
  name?: string;
  created_at: string;
  updated_at: string;
}

export interface Task {
  id: number | string;
  title: string;
  description?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
  user_id: string | number;
}

export interface TaskSummary {
  total: number;
  pending: number;
  completed: number;
  overdue: number;
  message: string;
}
// Initialize the auth client
const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
});

class ApiClient {
  private baseUrl: string;
  private token: string | null = null;

  constructor() {
    let url = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
    // Ensure the URL ends with /api for the ApiClient
    if (!url.endsWith('/api')) {
      url = url.replace(/\/$/, '') + '/api';
    }
    this.baseUrl = url;
  }

  // Set the JWT token for subsequent requests
  setToken(token: string) {
    this.token = token;
  }

  // Get the JWT token from local storage
  async getToken(): Promise<string | null> {
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('auth_token');
      console.log('🔑 getToken from localStorage:', token ? 'Found' : 'Missing');
      return token;
    }
    return null;
  }

  // Generic request method with JWT handling
  async request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
    // Robustly join base URL and endpoint (avoid double slashes or missing slashes)
    const normalizedBase = this.baseUrl.replace(/\/$/, '');
    const normalizedEndpoint = endpoint.startsWith('/') ? endpoint : `/${endpoint}`;
    const url = `${normalizedBase}${normalizedEndpoint}`;

    // Get token for this request
    const token = await this.getToken();

    const headers = {
      'Content-Type': 'application/json',
      ...(token && { 'Authorization': `Bearer ${token}` }),
      ...options.headers,
    } as Record<string, string>;

    const config: RequestInit = {
      ...options,
      headers,
    };

    console.log(`🚀 API Request: ${config.method || 'GET'} ${url}`, {
      headers: { ...headers, Authorization: token ? 'Bearer [HIDDEN]' : 'none' },
      body: config.body ? JSON.parse(config.body as string) : null
    });

    try {
      const response = await fetch(url, config);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ API Error (${response.status}):`, errorText);
        let errorData = {};
        try {
          errorData = JSON.parse(errorText);
        } catch (e) {
          errorData = { message: errorText };
        }
        throw new Error((errorData as any).message || (errorData as any).detail || `API request failed: ${response.status} ${response.statusText}`);
      }

      // For 204 No Content responses, return null
      if (response.status === 204) {
        return null as T;
      }

      const data = await response.json();
      console.log(`✅ API Success: ${url}`, data);
      return data;
    } catch (error: any) {
      console.error(`💥 Fetch Exception for ${url}:`, {
        name: error.name,
        message: error.message,
        stack: error.stack
      });

      // Handle network errors
      if (error instanceof TypeError && error.message.includes('fetch')) {
        throw new Error('Network error: Unable to reach the backend server. Please ensure the backend is running at ' + this.baseUrl);
      }
      throw error;
    }
  }

  // Authentication endpoints
  async signup(userData: { email: string; password: string; name?: string }) {
    return this.request<User>('/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async signin(credentials: { email: string; password: string }) {
    return this.request<{ user: User; token: string }>('/auth/signin', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  async getAuthUser() {
    return this.request<{ user_id: string; email: string; name: string; is_authenticated: boolean }>('/auth/me');
  }

  // Task endpoints
  async getTasks(params?: { status?: 'all' | 'pending' | 'completed'; sort?: 'created' | 'title' | 'due_date' }) {
    const searchParams = new URLSearchParams();
    if (params?.status) searchParams.append('status', params.status);
    if (params?.sort) searchParams.append('sort', params.sort);

    const queryString = searchParams.toString();
    const endpoint = `/tasks${queryString ? `?${queryString}` : ''}`;

    return this.request<Task[]>(endpoint);
  }

  async createTask(taskData: { title: string; description?: string }) {
    return this.request<Task>('/tasks', {
      method: 'POST',
      body: JSON.stringify(taskData),
    });
  }

  async getTask(taskId: string) {
    return this.request<Task>(`/tasks/${taskId}`);
  }

  async updateTask(taskId: string, taskData: Partial<Task>) {
    return this.request<Task>(`/tasks/${taskId}`, {
      method: 'PUT',
      body: JSON.stringify(taskData),
    });
  }

  async deleteTask(taskId: string) {
    return this.request<null>(`/tasks/${taskId}`, {
      method: 'DELETE',
    });
  }

  async toggleTaskCompletion(taskId: string) {
    return this.request<Task>(`/tasks/${taskId}/complete`, {
      method: 'PATCH',
    });
  }

  async getTaskSummary() {
    return this.request<TaskSummary>('/tasks/summary');
  }
}

// Create a singleton instance
export const apiClient = new ApiClient();

// Export individual methods for convenience, binding them to the instance
export const signup = apiClient.signup.bind(apiClient);
export const signin = apiClient.signin.bind(apiClient);
export const getAuthUser = apiClient.getAuthUser.bind(apiClient);
export const getTasks = apiClient.getTasks.bind(apiClient);
export const createTask = apiClient.createTask.bind(apiClient);
export const getTask = apiClient.getTask.bind(apiClient);
export const updateTask = apiClient.updateTask.bind(apiClient);
export const deleteTask = apiClient.deleteTask.bind(apiClient);
export const toggleTaskCompletion = apiClient.toggleTaskCompletion.bind(apiClient);
export const getTaskSummary = apiClient.getTaskSummary.bind(apiClient);