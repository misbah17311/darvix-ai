import type { DashboardMetrics } from '../../services/api';
import { Activity, Clock, Bot, Users } from 'lucide-react';

interface MetricsBarProps {
  metrics: DashboardMetrics;
}

export default function MetricsBar({ metrics }: MetricsBarProps) {
  return (
    <div className="bg-white border-b border-gray-200 px-6 py-2.5 flex items-center gap-6 text-sm shrink-0 overflow-x-auto">
      <Metric
        icon={<Activity size={14} className="text-blue-500" />}
        label="Active"
        value={metrics.active_conversations}
      />
      <Metric
        icon={<Clock size={14} className="text-yellow-500" />}
        label="In Queue"
        value={metrics.in_queue}
        alert={metrics.in_queue > 10}
      />
      <Metric
        icon={<Bot size={14} className="text-green-500" />}
        label="AI Resolved"
        value={`${metrics.ai_auto_resolved_today} (${metrics.ai_auto_resolved_pct}%)`}
      />
      <Metric
        icon={<Clock size={14} className="text-purple-500" />}
        label="Avg Handle"
        value={`${metrics.avg_handle_time_minutes}m`}
      />
      <Metric
        icon={<Users size={14} className="text-cyan-500" />}
        label="Agents"
        value={`${metrics.agents_available} avail / ${metrics.agents_online} online`}
      />
    </div>
  );
}

function Metric({
  icon,
  label,
  value,
  alert = false,
}: {
  icon: React.ReactNode;
  label: string;
  value: string | number;
  alert?: boolean;
}) {
  return (
    <div className={`flex items-center gap-2 whitespace-nowrap ${alert ? 'text-red-600 font-medium' : 'text-gray-600'}`}>
      {icon}
      <span className="text-gray-400">{label}:</span>
      <span className="font-semibold">{value}</span>
    </div>
  );
}
