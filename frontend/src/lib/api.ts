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
    
    const defaultHeaders = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    const response = await fetch(url, {
      ...options,
      headers: defaultHeaders,
    });

    if (!response.ok) {
      console.error(`API Error: ${response.status} ${response.statusText} for URL: ${url}`); // Debug log
      throw new Error(`API Error: ${response.status} ${response.statusText}`);
    }

    return response.json();
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