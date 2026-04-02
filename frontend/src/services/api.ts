const API_BASE = '/api';

export interface Conversation {
  id: string;
  customer_id: string;
  agent_id: string | null;
  channel: string;
  status: string;
  intent: string | null;
  intent_confidence: number | null;
  sentiment_score: number | null;
  urgency: number;
  ai_auto_resolved: boolean;
  summary: string | null;
  created_at: string;
  updated_at: string;
  customer?: Customer;
  messages?: Message[];
}

export interface Customer {
  id: string;
  name: string | null;
  email: string | null;
  phone: string | null;
  segment: string;
  lifetime_value: number;
  csat_avg: number | null;
  created_at: string;
}

export interface Message {
  id: string;
  conversation_id: string;
  sender: 'customer' | 'agent' | 'ai' | 'system';
  channel: string;
  content: string;
  content_type: string;
  ai_confidence: number | null;
  ai_intent: string | null;
  ai_sentiment: number | null;
  ai_suggested: boolean;
  created_at: string;
}

export interface DashboardMetrics {
  active_conversations: number;
  in_queue: number;
  avg_wait_minutes: number;
  ai_auto_resolved_today: number;
  ai_auto_resolved_pct: number;
  avg_handle_time_minutes: number;
  csat_today: number | null;
  agents_online: number;
  agents_available: number;
}

async function apiFetch<T>(url: string, options?: RequestInit): Promise<T> {
  const token = localStorage.getItem('darvix_token');
  const res = await fetch(`${API_BASE}${url}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options?.headers,
    },
  });
  if (!res.ok) {
    const error = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(error.detail || `HTTP ${res.status}`);
  }
  return res.json();
}

export const api = {
  // Auth
  login: (email: string, password: string) =>
    apiFetch<{ access_token: string }>('/agents/login', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    }),

  register: (data: { name: string; email: string; password: string; role?: string; skills?: string[] }) =>
    apiFetch('/agents/register', {
      method: 'POST',
      body: JSON.stringify(data),
    }),

  // Conversations
  getConversations: (status?: string) =>
    apiFetch<Conversation[]>(`/conversations${status ? `?status=${status}` : ''}`),

  getConversation: (id: string) =>
    apiFetch<Conversation>(`/conversations/${id}`),

  resolveConversation: (id: string) =>
    apiFetch(`/conversations/${id}/resolve`, { method: 'POST' }),

  // Messages
  sendAgentMessage: (conversationId: string, content: string, agentId: string) =>
    apiFetch<Message>(`/messages/agent-send/${conversationId}`, {
      method: 'POST',
      body: JSON.stringify({ content, agent_id: agentId }),
    }),

  // Dashboard
  getMetrics: () => apiFetch<DashboardMetrics>('/dashboard/metrics'),

  // Agents
  getAgents: (onlineOnly = false) =>
    apiFetch(`/agents/?online_only=${onlineOnly}`),

  getMe: () => apiFetch('/agents/me'),
};
