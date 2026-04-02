import { useState, useEffect } from 'react';
import { api, type Conversation, type DashboardMetrics } from '../../services/api';
import ConversationList from './ConversationList';
import ConversationView from './ConversationView';
import MetricsBar from './MetricsBar';
import {
  LogOut,
  MessageSquare,
  BarChart3,
  Users,
  Bell,
} from 'lucide-react';

interface DashboardProps {
  onLogout: () => void;
}

export default function Dashboard({ onLogout }: DashboardProps) {
  const [conversations, setConversations] = useState<Conversation[]>([]);
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [metrics, setMetrics] = useState<DashboardMetrics | null>(null);
  const [view, setView] = useState<'conversations' | 'analytics'>('conversations');

  useEffect(() => {
    loadData();
    const interval = setInterval(loadData, 10000); // Poll every 10s
    return () => clearInterval(interval);
  }, []);

  const loadData = async () => {
    try {
      const [convos, m] = await Promise.all([
        api.getConversations(),
        api.getMetrics(),
      ]);
      setConversations(convos);
      setMetrics(m);
    } catch {
      // API may not be running yet
    }
  };

  return (
    <div className="h-screen flex flex-col bg-gray-50">
      {/* Top Nav */}
      <header className="bg-darvix-900 text-white px-6 py-3 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 bg-darvix-500 rounded-lg flex items-center justify-center font-bold text-sm">
            D
          </div>
          <span className="text-lg font-semibold">DARVIX</span>
          <span className="text-xs bg-green-500 text-white px-2 py-0.5 rounded-full ml-2">
            Online
          </span>
        </div>

        <nav className="flex items-center gap-1">
          <button
            onClick={() => setView('conversations')}
            className={`px-3 py-1.5 rounded-lg text-sm flex items-center gap-2 transition-colors ${
              view === 'conversations'
                ? 'bg-white/20 text-white'
                : 'text-white/60 hover:text-white'
            }`}
          >
            <MessageSquare size={16} /> Conversations
          </button>
          <button
            onClick={() => setView('analytics')}
            className={`px-3 py-1.5 rounded-lg text-sm flex items-center gap-2 transition-colors ${
              view === 'analytics'
                ? 'bg-white/20 text-white'
                : 'text-white/60 hover:text-white'
            }`}
          >
            <BarChart3 size={16} /> Analytics
          </button>
        </nav>

        <div className="flex items-center gap-4">
          <button className="relative text-white/60 hover:text-white">
            <Bell size={20} />
            <span className="absolute -top-1 -right-1 w-4 h-4 bg-red-500 rounded-full text-[10px] flex items-center justify-center">
              3
            </span>
          </button>
          <button
            onClick={onLogout}
            className="text-white/60 hover:text-white flex items-center gap-1 text-sm"
          >
            <LogOut size={16} /> Logout
          </button>
        </div>
      </header>

      {/* Metrics Bar */}
      {metrics && <MetricsBar metrics={metrics} />}

      {/* Main Content */}
      <div className="flex-1 flex overflow-hidden">
        {view === 'conversations' ? (
          <>
            {/* Conversation List Sidebar */}
            <ConversationList
              conversations={conversations}
              selectedId={selectedId}
              onSelect={setSelectedId}
            />

            {/* Conversation Detail */}
            <div className="flex-1">
              {selectedId ? (
                <ConversationView
                  conversationId={selectedId}
                  onResolved={loadData}
                />
              ) : (
                <div className="h-full flex items-center justify-center text-gray-400">
                  <div className="text-center">
                    <MessageSquare size={48} className="mx-auto mb-3 opacity-50" />
                    <p className="text-lg">Select a conversation</p>
                    <p className="text-sm mt-1">Choose from the queue to begin</p>
                  </div>
                </div>
              )}
            </div>
          </>
        ) : (
          <AnalyticsView metrics={metrics} />
        )}
      </div>
    </div>
  );
}

function AnalyticsView({ metrics }: { metrics: DashboardMetrics | null }) {
  if (!metrics) return null;

  const stats = [
    { label: 'Active Conversations', value: metrics.active_conversations, color: 'blue' },
    { label: 'In Queue', value: metrics.in_queue, color: 'yellow' },
    { label: 'AI Auto-Resolved Today', value: metrics.ai_auto_resolved_today, color: 'green' },
    { label: 'AI Resolution Rate', value: `${metrics.ai_auto_resolved_pct}%`, color: 'emerald' },
    { label: 'Avg Handle Time', value: `${metrics.avg_handle_time_minutes} min`, color: 'purple' },
    { label: 'Agents Online', value: metrics.agents_online, color: 'cyan' },
    { label: 'Agents Available', value: metrics.agents_available, color: 'teal' },
    { label: 'Avg Wait Time', value: `${metrics.avg_wait_minutes} min`, color: 'orange' },
  ];

  return (
    <div className="flex-1 p-6 overflow-auto">
      <h2 className="text-xl font-semibold text-gray-800 mb-6 flex items-center gap-2">
        <BarChart3 size={24} /> Supervisor Dashboard
      </h2>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {stats.map(s => (
          <div key={s.label} className="bg-white rounded-xl p-5 shadow-sm border border-gray-100">
            <p className="text-sm text-gray-500">{s.label}</p>
            <p className="text-2xl font-bold text-gray-800 mt-1">{s.value}</p>
          </div>
        ))}
      </div>

      <div className="mt-8 bg-white rounded-xl p-6 shadow-sm border border-gray-100">
        <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
          <Users size={20} /> Agent Performance
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="text-left text-gray-500 border-b">
                <th className="pb-3 font-medium">Agent</th>
                <th className="pb-3 font-medium">Active</th>
                <th className="pb-3 font-medium">Resolved Today</th>
                <th className="pb-3 font-medium">Avg Handle Time</th>
                <th className="pb-3 font-medium">AI Assist Rate</th>
                <th className="pb-3 font-medium">Status</th>
              </tr>
            </thead>
            <tbody className="text-gray-700">
              <tr className="border-b border-gray-50">
                <td className="py-3">Marcus Chen</td>
                <td>4</td>
                <td>18</td>
                <td>4.2 min</td>
                <td>78%</td>
                <td><span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-1"></span>Online</td>
              </tr>
              <tr className="border-b border-gray-50">
                <td className="py-3">Aisha Patel</td>
                <td>6</td>
                <td>22</td>
                <td>3.1 min</td>
                <td>85%</td>
                <td><span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-1"></span>Online</td>
              </tr>
              <tr className="border-b border-gray-50">
                <td className="py-3">David Kim</td>
                <td>5</td>
                <td>15</td>
                <td>5.8 min</td>
                <td>62%</td>
                <td><span className="inline-block w-2 h-2 bg-green-500 rounded-full mr-1"></span>Online</td>
              </tr>
              <tr>
                <td className="py-3">Carlos Ruiz</td>
                <td>0</td>
                <td>12</td>
                <td>4.0 min</td>
                <td>73%</td>
                <td><span className="inline-block w-2 h-2 bg-yellow-500 rounded-full mr-1"></span>Break</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
