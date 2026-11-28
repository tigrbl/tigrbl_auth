import React from 'react';
import { ProviderHealth, ProviderHealthState } from '../types';
import { Activity, CheckCircle, AlertTriangle, XCircle, Clock, Percent } from 'lucide-react';

interface HealthProps {
  providers: ProviderHealth[];
  onToggleStatus: (id: string) => void;
}

export const ChannelProviderHealthGrid: React.FC<HealthProps> = ({ providers, onToggleStatus }) => {
  const getStatusIcon = (status: ProviderHealthState) => {
    switch (status) {
      case 'operational':
        return <CheckCircle className="h-4 w-4 text-emerald-400 animate-pulse" />;
      case 'degraded':
        return <AlertTriangle className="h-4 w-4 text-amber-400" />;
      case 'outage':
        return <XCircle className="h-4 w-4 text-rose-400 font-bold" />;
    }
  };

  const getStatusBadge = (status: ProviderHealthState) => {
    switch (status) {
      case 'operational':
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-emerald-500/10 px-2 py-0.5 text-[10px] font-medium text-emerald-400 border border-emerald-500/20">
            Operational
          </span>
        );
      case 'degraded':
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-amber-500/10 px-2 py-0.5 text-[10px] font-medium text-amber-400 border border-amber-500/20 animate-pulse">
            Degraded Latency
          </span>
        );
      case 'outage':
        return (
          <span className="inline-flex items-center gap-1 rounded-md bg-rose-500/10 px-2 py-0.5 text-[10px] font-medium text-rose-400 border border-rose-500/20">
            Outage / Offline
          </span>
        );
    }
  };

  return (
    <div className="space-y-3" id="provider-health-dashboard">
      <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
        <div>
          <h3 className="font-semibold text-zinc-100 flex items-center gap-2 text-sm">
            <Activity className="h-4 w-4 text-emerald-500" />
            Channel Provider Health
          </h3>
          <p className="text-[11px] text-zinc-400 mt-0.5">
            Simulate network status by clicking a card to toggle between states.
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
        {providers.map((p) => (
          <div
            key={p.id}
            onClick={() => onToggleStatus(p.id)}
            className={`group relative cursor-pointer overflow-hidden rounded-xl bg-zinc-900 border transition-all p-3 space-y-2 select-none hover:translate-y-[-2px] ${
              p.status === 'operational'
                ? 'border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900/80'
                : p.status === 'degraded'
                ? 'border-amber-900/40 bg-amber-950/5 hover:border-amber-800'
                : 'border-rose-900/40 bg-rose-950/5 hover:border-rose-800'
            }`}
            id={`provider-card-${p.id}`}
          >
            <div className="flex items-start justify-between">
              <div>
                <h4 className="font-medium text-zinc-200 text-xs group-hover:text-white transition">
                  {p.name}
                </h4>
                <p className="text-zinc-500 text-[10px] font-mono mt-0.5 uppercase tracking-wider">
                  Type: {p.type}
                </p>
              </div>
              <div className="flex items-center gap-1.5">
                {getStatusIcon(p.status)}
              </div>
            </div>

            <div className="flex items-center justify-between pt-1">
              {getStatusBadge(p.status)}

              <div className="flex items-center gap-2.5 text-[10px] font-mono text-zinc-400">
                <span className="flex items-center gap-1">
                  <Clock className="h-3 w-3 text-zinc-500" />
                  {p.status === 'outage' ? '—' : `${p.latencyMs}ms`}
                </span>
                <span className="flex items-center gap-1">
                  <Percent className="h-3 w-3 text-zinc-500" />
                  {p.reliability}%
                </span>
              </div>
            </div>

            {/* Glowing indicator line on the side */}
            <div className={`absolute top-0 bottom-0 left-0 w-[3px] ${
              p.status === 'operational' ? 'bg-emerald-500' : p.status === 'degraded' ? 'bg-amber-500' : 'bg-rose-500'
            }`} />
          </div>
        ))}
      </div>
    </div>
  );
};
