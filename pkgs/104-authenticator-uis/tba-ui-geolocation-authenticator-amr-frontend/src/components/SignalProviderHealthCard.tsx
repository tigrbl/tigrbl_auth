import React from 'react';
import { ProviderHealth } from '../types';
import { Activity, RefreshCw, AlertTriangle, ShieldCheck, HelpCircle, HardDrive } from 'lucide-react';

interface SignalProviderHealthCardProps {
  providers: ProviderHealth[];
  onRefreshProvider: (id: string) => void;
  onUpdateStatus: (id: string, status: ProviderHealth['status']) => void;
}

export const SignalProviderHealthCard: React.FC<SignalProviderHealthCardProps> = ({
  providers,
  onRefreshProvider,
  onUpdateStatus
}) => {
  return (
    <div className="space-y-4" role="region" aria-label="Signal Provider Registry and Health monitor">
      <div className="flex items-center justify-between">
        <div>
          <h4 className="text-sm font-semibold text-slate-900 font-display">
            Signal Provider Infrastructure
          </h4>
          <p className="text-xs text-slate-500">
            Real-time status, dataset synchronizations, and latency bounds
          </p>
        </div>
        <span className="inline-flex items-center gap-1.5 px-2 py-1 text-xs font-semibold bg-emerald-50 text-emerald-700 border border-emerald-100 rounded-md">
          <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse"></span>
          <span>Gateway Active</span>
        </span>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
        {providers.map((provider) => {
          const isHealthy = provider.status === 'healthy';
          const isDegraded = provider.status === 'degraded';
          const isOffline = provider.status === 'offline';

          return (
            <div
              key={provider.id}
              className={`bg-white border rounded-xl p-5 shadow-sm transition-all flex flex-col justify-between ${
                isHealthy ? 'border-slate-200 hover:border-slate-300' :
                isDegraded ? 'border-amber-200 bg-amber-50/20' : 'border-rose-200 bg-rose-50/10'
              }`}
            >
              <div className="space-y-4">
                {/* Header */}
                <div className="flex items-start justify-between">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={`w-2 h-2 rounded-full ${
                        isHealthy ? 'bg-emerald-500' : isDegraded ? 'bg-amber-500' : 'bg-rose-500'
                      }`}></span>
                      <h5 className="text-xs font-bold text-slate-800 tracking-wide font-mono">
                        {provider.name}
                      </h5>
                    </div>
                    <p className="text-[11px] text-slate-400">
                      Channel Type: <span className="font-semibold text-slate-600">{provider.type}</span>
                    </p>
                  </div>

                  {/* Status Badges & Controls */}
                  <div className="flex items-center gap-1">
                    <select
                      value={provider.status}
                      onChange={(e) => onUpdateStatus(provider.id, e.target.value as ProviderHealth['status'])}
                      className="bg-slate-50 border border-slate-200 text-slate-600 text-[10px] font-semibold rounded px-1.5 py-0.5 focus:outline-none focus:border-indigo-500"
                    >
                      <option value="healthy">Healthy</option>
                      <option value="degraded">Degraded</option>
                      <option value="offline">Offline</option>
                    </select>

                    <button
                      title="Force Refresh Metrics"
                      onClick={() => onRefreshProvider(provider.id)}
                      className="p-1 hover:bg-slate-100 rounded text-slate-400 hover:text-slate-700 transition-colors"
                    >
                      <RefreshCw className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {/* Metrics Grid */}
                <div className="grid grid-cols-3 gap-2.5 bg-slate-50/50 p-3 rounded-lg border border-slate-100/80">
                  <div>
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block">
                      Response Latency
                    </span>
                    <span className="text-xs font-mono font-bold text-slate-800">
                      {provider.latency}ms
                    </span>
                  </div>

                  <div>
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block">
                      Packet Error Rate
                    </span>
                    <span className={`text-xs font-mono font-bold ${provider.errorRate > 5 ? 'text-amber-600' : 'text-slate-800'}`}>
                      {provider.errorRate.toFixed(1)}%
                    </span>
                  </div>

                  <div>
                    <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block">
                      Provider State
                    </span>
                    <span className={`text-xs font-semibold uppercase ${
                      isHealthy ? 'text-emerald-600' : isDegraded ? 'text-amber-600' : 'text-rose-600'
                    }`}>
                      {provider.status}
                    </span>
                  </div>
                </div>

                {/* Dataset & Sync Sync Metadata */}
                <div className="flex items-center justify-between text-[11px] text-slate-500 pt-1">
                  <span className="flex items-center gap-1">
                    <HardDrive className="w-3.5 h-3.5 text-slate-400" />
                    <span>Dataset: <strong className="font-semibold font-mono text-slate-600">{provider.datasetVersion}</strong></span>
                  </span>
                  <span>
                    Last Sync: {new Date(provider.lastSync).toLocaleTimeString()}
                  </span>
                </div>
              </div>

              {/* Warnings */}
              {!isHealthy && (
                <div className={`mt-3 p-2.5 rounded text-[11px] border flex gap-2 items-start ${
                  isDegraded ? 'bg-amber-50/60 border-amber-100 text-amber-800' : 'bg-rose-50 border-rose-100 text-rose-800'
                }`}>
                  <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                  <span>
                    {isDegraded 
                      ? 'MDM latency bounds exceeded. Triggering soft-fallback policy (Step-Up authentication required).'
                      : 'Signal Channel is completely offline. Any policy requiring this provider will fall back to secure OTP.'}
                  </span>
                </div>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
