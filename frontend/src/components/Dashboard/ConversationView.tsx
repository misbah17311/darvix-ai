import { useState, useEffect, useRef } from 'react';
import { api, type Conversation, type Message } from '../../services/api';
import {
  Send,
  CheckCircle,
  Bot,
  User,
  Headphones,
  Sparkles,
  MessageSquare,
  Mail,
  Globe,
  Phone,
} from 'lucide-react';

interface ConversationViewProps {
  conversationId: string;
  onResolved: () => void;
}

const channelLabels: Record<string, { icon: React.ReactNode; label: string }> = {
  whatsapp: { icon: <MessageSquare size={14} />, label: 'WhatsApp' },
  email: { icon: <Mail size={14} />, label: 'Email' },
  webchat: { icon: <Globe size={14} />, label: 'Web Chat' },
  voice: { icon: <Phone size={14} />, label: 'Voice' },
};

export default function ConversationView({ conversationId, onResolved }: ConversationViewProps) {
  const [conversation, setConversation] = useState<Conversation | null>(null);
  const [input, setInput] = useState('');
  const [sending, setSending] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    loadConversation();
    const interval = setInterval(loadConversation, 5000);
    return () => clearInterval(interval);
  }, [conversationId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [conversation?.messages]);

  const loadConversation = async () => {
    try {
      const c = await api.getConversation(conversationId);
      setConversation(c);
    } catch {
      // Handle error
    }
  };

  const handleSend = async () => {
    if (!input.trim() || sending) return;
    setSending(true);
    try {
      await api.sendAgentMessage(conversationId, input, '');
      setInput('');
      await loadConversation();
    } catch {
      // Handle error
    } finally {
      setSending(false);
    }
  };

  const handleResolve = async () => {
    try {
      await api.resolveConversation(conversationId);
      onResolved();
      await loadConversation();
    } catch {
      // Handle error
    }
  };

  const handleUseSuggestion = (content: string) => {
    setInput(content);
  };

  if (!conversation) {
    return <div className="flex-1 flex items-center justify-center text-gray-400">Loading...</div>;
  }

  const messages = conversation.messages || [];
  const aiSuggestions = messages.filter(m => m.sender === 'ai' && m.ai_suggested);
  const displayMessages = messages.filter(m => !(m.sender === 'ai' && m.ai_suggested));
  const channel = channelLabels[conversation.channel] || channelLabels.webchat;

  return (
    <div className="h-full flex">
      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Conversation Header */}
        <div className="px-5 py-3 bg-white border-b border-gray-200 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2">
              <span className="font-semibold text-gray-800">
                Customer {conversation.customer_id.slice(0, 8)}
              </span>
              <span className="flex items-center gap-1 text-xs text-gray-400 bg-gray-100 px-2 py-0.5 rounded">
                {channel.icon} {channel.label}
              </span>
              {conversation.intent && (
                <span className="text-xs text-darvix-600 bg-darvix-50 px-2 py-0.5 rounded">
                  {conversation.intent}
                </span>
              )}
            </div>
            <div className="flex items-center gap-3 mt-1 text-xs text-gray-400">
              {conversation.sentiment_score !== null && (
                <span>
                  Sentiment: {conversation.sentiment_score > 0.3 ? '😊' : conversation.sentiment_score < -0.3 ? '😟' : '😐'}
                  {' '}{(conversation.sentiment_score * 100).toFixed(0)}%
                </span>
              )}
              <span>Urgency: {'🔴'.repeat(Math.min(conversation.urgency, 5))}</span>
              {conversation.intent_confidence !== null && (
                <span>AI Confidence: {(conversation.intent_confidence * 100).toFixed(0)}%</span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2">
            {conversation.status !== 'resolved' && (
              <button
                onClick={handleResolve}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-green-500 hover:bg-green-600 text-white text-sm rounded-lg transition-colors"
              >
                <CheckCircle size={14} /> Resolve
              </button>
            )}
          </div>
        </div>

        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 bg-gray-50">
          {displayMessages.map(msg => (
            <MessageBubble key={msg.id} message={msg} />
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        {conversation.status !== 'resolved' && (
          <div className="p-4 bg-white border-t border-gray-200">
            {/* AI Suggestion Banner */}
            {aiSuggestions.length > 0 && (
              <div className="mb-3 p-3 bg-blue-50 border border-blue-200 rounded-lg">
                <div className="flex items-center gap-1.5 text-xs text-blue-600 font-medium mb-1">
                  <Sparkles size={12} /> AI Suggestion
                  {aiSuggestions[aiSuggestions.length - 1].ai_confidence !== null && (
                    <span className="text-blue-400 ml-1">
                      ({(aiSuggestions[aiSuggestions.length - 1].ai_confidence! * 100).toFixed(0)}% confident)
                    </span>
                  )}
                </div>
                <p className="text-sm text-gray-700">
                  {aiSuggestions[aiSuggestions.length - 1].content}
                </p>
                <div className="mt-2 flex gap-2">
                  <button
                    onClick={() => handleUseSuggestion(aiSuggestions[aiSuggestions.length - 1].content)}
                    className="text-xs bg-blue-500 text-white px-2.5 py-1 rounded hover:bg-blue-600"
                  >
                    Use This
                  </button>
                  <button className="text-xs text-gray-500 px-2.5 py-1 rounded hover:bg-gray-100">
                    Dismiss
                  </button>
                </div>
              </div>
            )}

            <div className="flex gap-2">
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === 'Enter' && !e.shiftKey && handleSend()}
                className="flex-1 px-4 py-2.5 border border-gray-300 rounded-lg focus:ring-2 focus:ring-darvix-500 focus:border-transparent outline-none text-sm"
                placeholder="Type a message..."
              />
              <button
                onClick={handleSend}
                disabled={!input.trim() || sending}
                className="px-4 py-2.5 bg-darvix-600 hover:bg-darvix-700 text-white rounded-lg transition-colors disabled:opacity-50 flex items-center gap-1.5"
              >
                <Send size={16} />
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Right Sidebar — Customer Context */}
      <CustomerContextPanel conversation={conversation} />
    </div>
  );
}

function MessageBubble({ message: msg }: { message: Message }) {
  const isCustomer = msg.sender === 'customer';
  const isAI = msg.sender === 'ai';
  const isAgent = msg.sender === 'agent';

  const channelInfo = channelLabels[msg.channel];

  return (
    <div className={`flex ${isCustomer ? 'justify-start' : 'justify-end'}`}>
      <div className={`max-w-[70%] ${isCustomer ? '' : ''}`}>
        <div className="flex items-center gap-1.5 mb-1">
          {isCustomer && <User size={12} className="text-gray-400" />}
          {isAI && <Bot size={12} className="text-green-500" />}
          {isAgent && <Headphones size={12} className="text-blue-500" />}
          <span className="text-[10px] text-gray-400">
            {isCustomer ? 'Customer' : isAI ? 'AI' : 'You'}
            {channelInfo && ` via ${channelInfo.label}`}
            {' · '}
            {new Date(msg.created_at).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
          </span>
        </div>
        <div
          className={`px-4 py-2.5 rounded-2xl text-sm ${
            isCustomer
              ? 'bg-white border border-gray-200 text-gray-800 rounded-tl-sm'
              : isAI
              ? 'bg-green-50 border border-green-200 text-gray-800 rounded-tr-sm'
              : 'bg-darvix-600 text-white rounded-tr-sm'
          }`}
        >
          {msg.content}
        </div>
      </div>
    </div>
  );
}

function CustomerContextPanel({ conversation }: { conversation: Conversation }) {
  const c = conversation.customer;

  return (
    <div className="w-72 bg-white border-l border-gray-200 p-4 overflow-y-auto shrink-0">
      <h3 className="font-semibold text-gray-800 text-sm mb-4">Customer Context</h3>

      {c ? (
        <div className="space-y-4">
          <div>
            <p className="font-medium text-gray-800">{c.name || 'Unknown'}</p>
            {c.email && <p className="text-xs text-gray-400">{c.email}</p>}
            {c.phone && <p className="text-xs text-gray-400">{c.phone}</p>}
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div className="bg-gray-50 rounded-lg p-2.5">
              <p className="text-[10px] text-gray-400">Segment</p>
              <p className="text-sm font-medium text-gray-800 capitalize">{c.segment}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-2.5">
              <p className="text-[10px] text-gray-400">Lifetime Value</p>
              <p className="text-sm font-medium text-gray-800">${c.lifetime_value.toLocaleString()}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-2.5">
              <p className="text-[10px] text-gray-400">CSAT</p>
              <p className="text-sm font-medium text-gray-800">{c.csat_avg ? `${c.csat_avg}/5` : 'N/A'}</p>
            </div>
            <div className="bg-gray-50 rounded-lg p-2.5">
              <p className="text-[10px] text-gray-400">Since</p>
              <p className="text-sm font-medium text-gray-800">
                {new Date(c.created_at).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      ) : (
        <p className="text-sm text-gray-400">No customer data available</p>
      )}

      {/* AI Analysis */}
      <div className="mt-6">
        <h4 className="font-semibold text-gray-800 text-sm mb-3 flex items-center gap-1.5">
          <Bot size={14} /> AI Analysis
        </h4>
        <div className="space-y-2">
          <InfoRow label="Intent" value={conversation.intent || 'Analyzing...'} />
          <InfoRow
            label="Confidence"
            value={conversation.intent_confidence ? `${(conversation.intent_confidence * 100).toFixed(0)}%` : '—'}
          />
          <InfoRow
            label="Sentiment"
            value={
              conversation.sentiment_score !== null
                ? `${conversation.sentiment_score > 0 ? '+' : ''}${(conversation.sentiment_score * 100).toFixed(0)}%`
                : '—'
            }
          />
          <InfoRow label="Urgency" value={`${'●'.repeat(conversation.urgency)}${'○'.repeat(5 - conversation.urgency)}`} />
        </div>
      </div>

      {/* Quick Actions */}
      {conversation.status !== 'resolved' && (
        <div className="mt-6">
          <h4 className="font-semibold text-gray-800 text-sm mb-3">Quick Actions</h4>
          <div className="space-y-1.5">
            {['Create Ticket', 'Issue Refund', 'Escalate', 'Transfer'].map(action => (
              <button
                key={action}
                className="w-full text-left px-3 py-2 text-xs text-gray-600 hover:bg-gray-50 rounded-lg transition-colors border border-gray-100"
              >
                {action}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

function InfoRow({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex items-center justify-between text-xs">
      <span className="text-gray-400">{label}</span>
      <span className="text-gray-700 font-medium">{value}</span>
    </div>
  );
}
