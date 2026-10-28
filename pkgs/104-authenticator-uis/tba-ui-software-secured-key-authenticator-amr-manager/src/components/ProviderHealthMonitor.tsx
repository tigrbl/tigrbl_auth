import React from 'react';
import { Activity, HeartPulse, CheckCircle, AlertTriangle, XCircle, RefreshCw } from 'lucide-react';
import { ProviderHealth } from '../types';

interface ProviderHealthMonitorProps {
  providers: ProviderHealth[];
  onToggleStatus: (id: string) => void;
  onRefreshAll: () => void;
}

export default function ProviderHealthMonitor({
  providers,
  onToggleStatus,
  onRefreshAll,
}: ProviderHealthMonitorProps) {
  return (
    <div id="provider-health-monitor" className="bg-white border border-slate-200 rounded-xl p-5 space-y-4 shadow-sm">
      <div className="flex items-center justify-between border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <HeartPulse className="w-5 h-5 text-indigo-600" />
          <h4 className="font-semibold text-slate-800 text-sm">Provider & Keystore Health Monitor</h4>
        </div>
        <button
          onClick={onRefreshAll}
          id="btn-refresh-health-telemetry"
          className="text-xs text-indigo-600 hover:text-indigo-800 flex items-center gap-1 font-semibold p-1.5 transition-colors cursor-pointer"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          Refresh Stats
        </button>
      </div>

      <p className="text-xs text-slate-500 leading-relaxed">
        Active drivers and validator engines registered on this tenant gateway. Use the status pill buttons to simulate keystore provider failures and test resilient fallback workflows.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {providers.map((p) => (
          <div
            key={p.id}
            id={`provider-health-card-${p.id}`}
            className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3 relative overflow-hidden"
          >
            <div className="flex items-start justify-between">
              <div>
                <h5 className="font-bold text-slate-800 text-xs">{p.name}</h5>
                <span className="text-[10px] text-slate-400 font-mono">
                  Driver v{p.version} · {p.type.toUpperCase()}
                </span>
              </div>

              {/* Status Toggle Button */}
              <button
                onClick={() => onToggleStatus(p.id)}
                id={`btn-toggle-health-${p.id}`}
                className={`px-2 py-1 rounded text-[10px] font-bold border transition-all flex items-center gap-1 cursor-pointer hover:shadow-sm ${
                  p.status === 'healthy'
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-700 hover:bg-emerald-100'
                    : p.status === 'degraded'
                    ? 'bg-amber-50 border-amber-200 text-amber-700 hover:bg-amber-100'
                    : 'bg-rose-50 border-rose-200 text-rose-700 hover:bg-rose-100'
                }`}
                title="Click to toggle health simulation state"
              >
                {p.status === 'healthy' && (
                  <>
                    <CheckCircle className="w-3 h-3 text-emerald-500" /> Operational
                  </>
                )}
                {p.status === 'degraded' && (
                  <>
                    <AlertTriangle className="w-3 h-3 text-amber-500" /> Degraded
                  </>
                )}
                {p.status === 'unavailable' && (
                  <>
                    <XCircle className="w-3 h-3 text-rose-500" /> Offline
                  </>
                )}
              </button>
            </div>

            <div className="flex items-center justify-between text-[11px] pt-1.5 border-t border-slate-200/50">
              <span className="text-slate-500">Latency telemetry</span>
              <span className={`font-mono font-semibold ${
                p.latencyMs > 100 ? 'text-amber-600 font-bold' : 'text-slate-600'
              }`}>
                {p.latencyMs} ms
              </span>
            </div>

            {/* Check Date */}
            <div className="text-[9px] text-slate-400 flex items-center justify-between">
              <span>Last checked:</span>
              <span className="font-mono">{new Date(p.lastChecked).toLocaleTimeString()}</span>
            </div>

            {/* Visual health line indicator */}
            <div className={`absolute bottom-0 inset-x-0 h-1 ${
              p.status === 'healthy' ? 'bg-emerald-500' : p.status === 'degraded' ? 'bg-amber-500' : 'bg-rose-500'
            }`} />
          </div>
        ))}
      </div>
    </div>
  );
}
