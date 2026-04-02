import type { Conversation } from '../../services/api';
import {
  MessageSquare,
  Mail,
  Phone,
  Globe,
  Share2,
} from 'lucide-react';

interface ConversationListProps {
  conversations: Conversation[];
  selectedId: string | null;
  onSelect: (id: string) => void;
}

const channelIcons: Record<string, React.ReactNode> = {
  whatsapp: <MessageSquare size={14} className="text-green-500" />,
  email: <Mail size={14} className="text-blue-500" />,
  webchat: <Globe size={14} className="text-purple-500" />,
  voice: <Phone size={14} className="text-orange-500" />,
  social_fb: <Share2 size={14} className="text-blue-600" />,
  social_ig: <Share2 size={14} className="text-pink-500" />,
  social_x: <Share2 size={14} className="text-gray-700" />,
};

const urgencyColors: Record<number, string> = {
  1: 'bg-gray-300',
  2: 'bg-green-400',
  3: 'bg-yellow-400',
  4: 'bg-orange-500',
  5: 'bg-red-500',
};

const statusLabels: Record<string, { text: string; color: string }> = {
  active: { text: 'Active', color: 'text-blue-600 bg-blue-50' },
  waiting_agent: { text: 'Waiting', color: 'text-yellow-700 bg-yellow-50' },
  waiting_customer: { text: 'Replied', color: 'text-green-700 bg-green-50' },
  escalated: { text: 'Escalated', color: 'text-red-700 bg-red-50' },
  resolved: { text: 'Resolved', color: 'text-gray-500 bg-gray-50' },
};

export default function ConversationList({ conversations, selectedId, onSelect }: ConversationListProps) {
  const activeConvos = conversations.filter(c => c.status !== 'resolved');
  const resolvedConvos = conversations.filter(c => c.status === 'resolved');

  return (
    <div className="w-80 bg-white border-r border-gray-200 flex flex-col shrink-0">
      <div className="p-4 border-b border-gray-100">
        <h2 className="font-semibold text-gray-800">Queue</h2>
        <p className="text-xs text-gray-400 mt-0.5">{activeConvos.length} active conversations</p>
      </div>

      <div className="flex-1 overflow-y-auto">
        {activeConvos.length === 0 && resolvedConvos.length === 0 && (
          <div className="p-6 text-center text-gray-400 text-sm">
            No conversations yet
          </div>
        )}

        {activeConvos.map(c => (
          <ConversationItem
            key={c.id}
            conversation={c}
            isSelected={c.id === selectedId}
            onClick={() => onSelect(c.id)}
          />
        ))}

        {resolvedConvos.length > 0 && (
          <>
            <div className="px-4 py-2 text-xs text-gray-400 font-medium bg-gray-50 border-y border-gray-100">
              Resolved ({resolvedConvos.length})
            </div>
            {resolvedConvos.slice(0, 10).map(c => (
              <ConversationItem
                key={c.id}
                conversation={c}
                isSelected={c.id === selectedId}
                onClick={() => onSelect(c.id)}
              />
            ))}
          </>
        )}
      </div>
    </div>
  );
}

function ConversationItem({
  conversation: c,
  isSelected,
  onClick,
}: {
  conversation: Conversation;
  isSelected: boolean;
  onClick: () => void;
}) {
  const statusInfo = statusLabels[c.status] || statusLabels.active;
  const timeDiff = getTimeDiff(c.updated_at);

  return (
    <button
      onClick={onClick}
      className={`w-full p-3 text-left border-b border-gray-50 hover:bg-gray-50 transition-colors ${
        isSelected ? 'bg-blue-50 border-l-2 border-l-darvix-500' : ''
      }`}
    >
      <div className="flex items-start justify-between">
        <div className="flex items-center gap-2">
          <span className={`w-2.5 h-2.5 rounded-full ${urgencyColors[c.urgency] || 'bg-gray-300'}`} />
          <span className="font-medium text-sm text-gray-800 truncate max-w-[140px]">
            {c.customer_id.slice(0, 8)}...
          </span>
        </div>
        <span className="text-[10px] text-gray-400">{timeDiff}</span>
      </div>

      <div className="mt-1.5 flex items-center gap-2">
        {channelIcons[c.channel] || <Globe size={14} />}
        <span className="text-xs text-gray-500 truncate">
          {c.intent || 'Analyzing...'}
        </span>
      </div>

      <div className="mt-1.5 flex items-center gap-2">
        <span className={`text-[10px] px-1.5 py-0.5 rounded ${statusInfo.color}`}>
          {statusInfo.text}
        </span>
        {c.ai_auto_resolved && (
          <span className="text-[10px] px-1.5 py-0.5 rounded bg-emerald-50 text-emerald-700">
            AI Resolved
          </span>
        )}
        {c.sentiment_score !== null && c.sentiment_score < -0.3 && (
          <span className="text-[10px]">😟</span>
        )}
      </div>
    </button>
  );
}

function getTimeDiff(dateStr: string): string {
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return 'now';
  if (mins < 60) return `${mins}m`;
  const hours = Math.floor(mins / 60);
  if (hours < 24) return `${hours}h`;
  return `${Math.floor(hours / 24)}d`;
}
