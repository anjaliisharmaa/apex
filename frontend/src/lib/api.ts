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

export interface OTPRequest {
  email: string;
  password: string;
}

export interface OTPVerification {
  email: string;
  otp_code: string;
}

export interface OTPResponse {
  message: string;
  otp_sent: boolean;
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

export interface AdminStats {
  total_cases: number;
  total_pending: number;
  total_approved: number;
  total_rejected: number;
  new_today: number;
  active_users: number;
  avg_response_time: number;
  success_rate: number;
}

export interface CaseData {
  id: string;
  user_name: string;
  user_email: string;
  case_type: string;
  title: string;
  submitted_date: string;
  status: 'pending' | 'approved' | 'rejected' | 'under_review';
  priority: 'high' | 'medium' | 'low';
  description: string;
  department: string;
  created_at: string;
  updated_at: string;
  attachments?: Array<{
    filename: string;
    size: number;
    uploaded_at: string;
  }>;
  history?: Array<{
    action: string;
    timestamp: string;
    user: string;
    notes: string;
  }>;
}

export interface CasesResponse {
  cases: CaseData[];
  total: number;
  has_more: boolean;
}

export interface StatusUpdateRequest {
  status: string;
  notes?: string;
}

export interface AnalyticsData {
  case_types: Array<{
    name: string;
    value: number;
    percentage: number;
  }>;
  cases_by_department: Array<{
    department: string;
    pending: number;
    total: number;
  }>;
  monthly_trends: Array<{
    month: string;
    submitted: number;
    resolved: number;
  }>;
}

export interface RecentActivity {
  activities: Array<{
    id: number;
    type: string;
    message: string;
    timestamp: string;
    case_id: string;
  }>;
}

export interface EmployeeDetails {
  name: string;
  email: string;
  employee_id: string;
  department: string;
  role: string;
  join_date: string;
  phone: string;
  supervisor: string;
  location: string;
  security_clearance: string;
  specialization: string;
  cases: Array<{
    id: string;
    case_type: string;
    title: string;
    submitted_date: string;
    status: string;
    priority: string;
  }>;
  performance_summary: {
    total_cases: number;
    pending_cases: number;
    average_resolution_time: string;
    last_case_date: string;
  };
}

export interface ForumData {
  id: string;
  name: string;
  description: string;
  member_count: number;
  is_private: boolean;
  recent_activity: string;
  category: string;
}

export interface ForumMessage {
  id: string;
  forum_id: string;
  author: string;
  author_anonymous: boolean;
  author_id: string;
  content: string;
  timestamp: string;
  replies: number;
  likes: number;
  is_pinned: boolean;
}

export interface MessageReply {
  id: string;
  message_id: string;
  author: string;
  author_anonymous: boolean;
  author_id: string;
  content: string;
  timestamp: string;
  likes: number;
}

export interface NewForumData {
  name: string;
  description: string;
  is_private: boolean;
  category: string;
}

export interface NewMessageData {
  content: string;
  anonymous: boolean;
}

export interface NewReplyData {
  content: string;
  anonymous: boolean;
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
   * Request OTP for login
   */
  async requestOTP(otpRequest: OTPRequest): Promise<OTPResponse> {
    return this.request<OTPResponse>('/api/request-otp', {
      method: 'POST',
      body: JSON.stringify(otpRequest),
    });
  }

  /**
   * Verify OTP and login
   */
  async verifyOTP(otpVerification: OTPVerification): Promise<Token> {
    const token = await this.request<Token>('/api/verify-otp', {
      method: 'POST',
      body: JSON.stringify(otpVerification),
    });
    
    // Store token in localStorage
    this.setStoredToken(token.access_token);
    return token;
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

  // Admin API methods
  /**
   * Get admin dashboard statistics
   */
  async getAdminStats(): Promise<AdminStats> {
    return this.request<AdminStats>('/api/admin/stats');
  }

  /**
   * Get all cases for admin
   */
  async getAdminCases(status?: string, limit: number = 100, offset: number = 0): Promise<CasesResponse> {
    const params = new URLSearchParams();
    if (status && status !== 'all') {
      params.append('status', status);
    }
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    
    const queryString = params.toString();
    const url = `/api/admin/cases${queryString ? `?${queryString}` : ''}`;
    
    return this.request<CasesResponse>(url);
  }

  /**
   * Update case status
   */
  async updateCaseStatus(caseId: string, statusUpdate: StatusUpdateRequest): Promise<any> {
    return this.request(`/api/admin/cases/${caseId}/status`, {
      method: 'PUT',
      body: JSON.stringify(statusUpdate),
    });
  }

  /**
   * Get detailed case information
   */
  async getCaseDetails(caseId: string): Promise<CaseData> {
    return this.request<CaseData>(`/api/admin/cases/${caseId}`);
  }

  /**
   * Get analytics data for charts
   */
  async getAdminAnalytics(): Promise<AnalyticsData> {
    return this.request<AnalyticsData>('/api/admin/analytics');
  }

  /**
   * Get recent activity feed
   */
  async getRecentActivity(): Promise<RecentActivity> {
    return this.request<RecentActivity>('/api/admin/recent-activity');
  }

  /**
   * Get employee details and case history
   */
  async getEmployeeDetails(employeeEmail: string): Promise<EmployeeDetails> {
    return this.request<EmployeeDetails>(`/api/admin/employee/${encodeURIComponent(employeeEmail)}`);
  }

  // Community Forum API methods
  /**
   * Get all community forums
   */
  async getCommunityForums(): Promise<{ forums: ForumData[] }> {
    return this.request<{ forums: ForumData[] }>('/api/community/forums');
  }

  /**
   * Get messages from a specific forum
   */
  async getForumMessages(forumId: string, limit: number = 50, offset: number = 0): Promise<{ messages: ForumMessage[], total: number, has_more: boolean }> {
    const params = new URLSearchParams();
    params.append('limit', limit.toString());
    params.append('offset', offset.toString());
    
    const queryString = params.toString();
    const url = `/api/community/forums/${forumId}/messages${queryString ? `?${queryString}` : ''}`;
    
    return this.request<{ messages: ForumMessage[], total: number, has_more: boolean }>(url);
  }

  /**
   * Post a new message to a forum
   */
  async postForumMessage(forumId: string, messageData: NewMessageData): Promise<any> {
    return this.request(`/api/community/forums/${forumId}/messages`, {
      method: 'POST',
      body: JSON.stringify(messageData),
    });
  }

  /**
   * Create a new forum
   */
  async createForum(forumData: NewForumData): Promise<any> {
    return this.request('/api/community/forums', {
      method: 'POST',
      body: JSON.stringify(forumData),
    });
  }

  /**
   * Join a forum
   */
  async joinForum(forumId: string): Promise<any> {
    return this.request(`/api/community/forums/${forumId}/join`, {
      method: 'POST',
    });
  }

  /**
   * Get replies to a message
   */
  async getMessageReplies(forumId: string, messageId: string): Promise<{ replies: MessageReply[] }> {
    return this.request<{ replies: MessageReply[] }>(`/api/community/forums/${forumId}/messages/${messageId}/replies`);
  }

  /**
   * Post a reply to a message
   */
  async postMessageReply(forumId: string, messageId: string, replyData: NewReplyData): Promise<any> {
    return this.request(`/api/community/forums/${forumId}/messages/${messageId}/replies`, {
      method: 'POST',
      body: JSON.stringify(replyData),
    });
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