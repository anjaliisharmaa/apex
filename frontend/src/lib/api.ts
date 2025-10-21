// API Client for APEX Backend Integration
// Connects Next.js frontend to FastAPI orchestrator backend

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://127.0.0.1:8000';

export interface ChatRequest {
  message: string;
  conversation_id?: string;
  anonymous?: boolean;
}

export interface ChatResponse {
  response: string;
  agent_used: string;
  conversation_id: string;
  timestamp: string;
  workflow_type?: string;
  conversation_state?: string;
  intent_analysis?: {
    primary_intent: string;
    confidence: number;
    needs_multiple_agents: boolean;
  };
  individual_responses?: Array<{
    success: boolean;
    response: string;
    agent_used: string;
  }>;
}

export interface DocumentRequest {
  document_type: string;
  user_data: Record<string, any>;
}

export interface DocumentResponse {
  document_content: string;
  document_type: string;
  generated_at: string;
}

export interface AgentStatus {
  orchestrator: {
    status: string;
    description: string;
  };
  asha: {
    status: string;
    description: string;
  };
  athena: {
    status: string;
    description: string;
  };
  scribe: {
    status: string;
    description: string;
  };
}

// Authentication interfaces
export interface UserRegister {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

export interface UserLogin {
  username: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface UserResponse {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  created_at: string;
}

class APEXAPIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  private async request<T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    console.log('Making API request to:', url); // Debug log
    
    const defaultHeaders: Record<string, string> = {
      'Content-Type': 'application/json',
      ...(options.headers as Record<string, string>),
    };

    // Add JWT token if available
    const token = this.getStoredToken();
    if (token) {
      defaultHeaders['Authorization'] = `Bearer ${token}`;
    }

    const response = await fetch(url, {
      ...options,
      headers: defaultHeaders,
    });

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText} for URL: ${url}`); // Debug log
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    const data = await response.json();
    console.log('API Response data:', data); // Debug log to see actual response
    return data;
  }

  // Token management methods
  private getStoredToken(): string | null {
    if (typeof window !== 'undefined') {
      return localStorage.getItem('apex_auth_token');
    }
    return null;
  }

  private setStoredToken(token: string): void {
    if (typeof window !== 'undefined') {
      localStorage.setItem('apex_auth_token', token);
    }
  }

  private removeStoredToken(): void {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('apex_auth_token');
    }
  }

  /**
   * Send a chat message to the orchestrator
   */
  async sendChatMessage(request: ChatRequest): Promise<ChatResponse> {
    return this.request<ChatResponse>('/api/chat', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Generate a document using the orchestrator
   */
  async generateDocument(request: DocumentRequest): Promise<DocumentResponse> {
    return this.request<DocumentResponse>('/api/forms/generate', {
      method: 'POST',
      body: JSON.stringify(request),
    });
  }

  /**
   * Get the status of all agents
   */
  async getAgentStatus(): Promise<AgentStatus> {
    return this.request<AgentStatus>('/api/agents/status');
  }

  /**
   * Get conversation history
   */
  async getConversation(conversationId: string): Promise<any> {
    return this.request(`/api/conversations/${conversationId}`);
  }

  /**
   * Get available resources
   */
  async getResources(): Promise<any> {
    return this.request('/api/resources');
  }

  /**
   * Get user cases
   */
  async getCases(): Promise<any> {
    return this.request('/api/cases');
  }

  /**
   * Upload a file
   */
  async uploadFile(file: File): Promise<any> {
    const formData = new FormData();
    formData.append('file', file);

    return this.request('/api/upload', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for multipart/form-data
      body: formData,
    });
  }

  /**
   * Health check
   */
  async healthCheck(): Promise<any> {
    return this.request('/');
  }

  // Authentication methods
  /**
   * Register a new user
   */
  async register(userData: UserRegister): Promise<UserResponse> {
    return this.request<UserResponse>('/api/register', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  /**
   * Login user
   */
  async login(credentials: UserLogin): Promise<Token> {
    const token = await this.request<Token>('/api/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
    
    // Store token in localStorage
    this.setStoredToken(token.access_token);
    return token;
  }

  /**
   * Logout user
   */
  async logout(): Promise<any> {
    try {
      const result = await this.request('/api/logout', {
        method: 'POST',
      });
      return result;
    } finally {
      // Always remove token, even if API call fails
      this.removeStoredToken();
    }
  }

  /**
   * Get current user profile
   */
  async getUserProfile(): Promise<UserResponse> {
    return this.request<UserResponse>('/api/user/profile');
  }

  /**
   * Check if user is authenticated
   */
  isAuthenticated(): boolean {
    return this.getStoredToken() !== null;
  }
}

// Create singleton instance
export const apiClient = new APEXAPIClient();

// Utility functions for frontend
export const formatAgentName = (agentName: string): string => {
  const names = {
    'asha': 'ASHA (Emotional Support)',
    'athena': 'Athena (Legal Guidance)', 
    'scribe': 'Scribe (Document Generation)',
    'orchestrator': 'APEX Orchestrator'
  };
  return names[agentName as keyof typeof names] || agentName.toUpperCase();
};

export const getWorkflowDescription = (workflowType?: string): string => {
  const descriptions = {
    'single_agent': 'Specialist Assistant',
    'multi_agent': 'Coordinated Multi-Specialist Support',
    'harassment_support': 'Legal + Emotional Support',
    'legal_documentation': 'Legal Guidance + Document Creation',
    'employment_comprehensive': 'Complete Employment Support',
    'maternity_support': 'Comprehensive Maternity Assistance'
  };
  return descriptions[workflowType as keyof typeof descriptions] || 'AI Assistant';
};

export const getIntentColor = (intent?: string): string => {
  const colors = {
    'legal': 'text-blue-600',
    'emotional': 'text-green-600',
    'documentation': 'text-purple-600',
    'general': 'text-gray-600'
  };
  return colors[intent as keyof typeof colors] || 'text-gray-600';
};

export default APEXAPIClient;