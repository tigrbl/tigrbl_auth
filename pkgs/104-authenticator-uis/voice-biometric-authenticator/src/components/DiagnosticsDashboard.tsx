import React, { useState } from 'react';
import { Activity, ShieldAlert, CheckCircle2, AlertTriangle, Info, Clock, Calendar, Search, Filter } from 'lucide-react';
import { AuditLog, DiagnosticsSummary } from '../types';

interface DiagnosticsDashboardProps {
  summary: DiagnosticsSummary;
  logs: AuditLog[];
  onClearLogs: () => void;
}

export default function DiagnosticsDashboard({
  summary,
  logs,
  onClearLogs,
}: DiagnosticsDashboardProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterStatus, setFilterStatus] = useState<'all' | 'success' | 'failure' | 'warning'>('all');

  const filteredLogs = logs.filter((log) => {
    const matchesSearch =
      log.action.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.details.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (log.id && log.id.toLowerCase().includes(searchTerm.toLowerCase()));
    
    if (filterStatus === 'all') return matchesSearch;
    return log.status === filterStatus && matchesSearch;
  });

  const successRate = summary.totalAttempts > 0 
    ? Math.round((summary.successCount / summary.totalAttempts) * 100) 
    : 0;

  // Render SVG Ring calculations
  const radius = 34;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (successRate / 100) * circumference;

  return (
    <div className="space-y-6 max-w-4xl mx-auto" id="diagnostics-dashboard-container">
      {/* Metrics Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* Verification Success Rate Ring Chart */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex items-center gap-4 shadow-xl">
          <div className="relative flex items-center justify-center h-16 w-16 shrink-0">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="32"
                cy="32"
                r={radius}
                className="stroke-slate-800 fill-none"
                strokeWidth="6"
              />
              <circle
                cx="32"
                cy="32"
                r={radius}
                className="stroke-emerald-500 fill-none transition-all duration-1000"
                strokeWidth="6"
                strokeDasharray={circumference}
                strokeDashoffset={strokeDashoffset}
                strokeLinecap="round"
              />
            </svg>
            <span className="absolute font-mono text-sm font-bold text-slate-100">{successRate}%</span>
          </div>
          <div>
            <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500 block">Match Success</span>
            <span className="font-sans text-xl font-bold text-slate-200">{summary.successCount}</span>
            <span className="text-[10px] text-slate-400 block mt-0.5">out of {summary.totalAttempts} total logs</span>
          </div>
        </div>

        {/* Spoof Rejected */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex items-center gap-4 shadow-xl">
          <div className="h-12 w-12 bg-rose-500/10 border border-rose-500/20 text-rose-400 rounded-xl flex items-center justify-center shrink-0">
            <ShieldAlert className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500 block">Spoofs Blocked</span>
            <span className="font-sans text-xl font-bold text-rose-400">
              {summary.spoofAttempts.replay + summary.spoofAttempts.synthetic}
            </span>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              {summary.spoofAttempts.replay} replay | {summary.spoofAttempts.synthetic} synt.
            </span>
          </div>
        </div>

        {/* Ambient Noise Retries */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex items-center gap-4 shadow-xl">
          <div className="h-12 w-12 bg-amber-500/10 border border-amber-500/20 text-amber-400 rounded-xl flex items-center justify-center shrink-0">
            <AlertTriangle className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500 block">Noise Purges</span>
            <span className="font-sans text-xl font-bold text-amber-400">{summary.noiseFailures}</span>
            <span className="text-[10px] text-slate-400 block mt-0.5">Exceeded db criteria</span>
          </div>
        </div>

        {/* Average Response Time */}
        <div className="bg-slate-900 border border-slate-800 p-4 rounded-2xl flex items-center gap-4 shadow-xl">
          <div className="h-12 w-12 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl flex items-center justify-center shrink-0">
            <Clock className="w-5 h-5" />
          </div>
          <div>
            <span className="text-[10px] uppercase font-mono tracking-wider text-slate-500 block">Response Latency</span>
            <span className="font-sans text-xl font-bold text-indigo-300">{summary.averageResponseTimeMs} ms</span>
            <span className="text-[10px] text-slate-400 block mt-0.5">Verifier extraction avg</span>
          </div>
        </div>
      </div>

      {/* Bar Chart & Category Breakdown */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Failure Category columns */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl md:col-span-1 space-y-4">
          <div>
            <h4 className="font-sans font-semibold text-slate-200 text-xs uppercase tracking-wider">Verifier Fault Classification</h4>
            <p className="text-[10px] text-slate-500 mt-0.5">Failure reason analysis breakdown</p>
          </div>

          <div className="space-y-3.5 pt-2">
            {/* Replay */}
            <div className="space-y-1 text-xs">
              <div className="flex justify-between font-mono text-[10px]">
                <span className="text-slate-400">Replay Signature</span>
                <span className="text-rose-400">{summary.spoofAttempts.replay} failures</span>
              </div>
              <div className="h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-rose-500"
                  style={{ width: `${Math.min(100, (summary.spoofAttempts.replay / (summary.failureCount || 1)) * 100)}%` }}
                />
              </div>
            </div>

            {/* Synthetic */}
            <div className="space-y-1 text-xs">
              <div className="flex justify-between font-mono text-[10px]">
                <span className="text-slate-400">Deepfake/Synthetic</span>
                <span className="text-rose-400">{summary.spoofAttempts.synthetic} failures</span>
              </div>
              <div className="h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-rose-500/80"
                  style={{ width: `${Math.min(100, (summary.spoofAttempts.synthetic / (summary.failureCount || 1)) * 100)}%` }}
                />
              </div>
            </div>

            {/* Noise */}
            <div className="space-y-1 text-xs">
              <div className="flex justify-between font-mono text-[10px]">
                <span className="text-slate-400">Ambient Noise Purge</span>
                <span className="text-amber-400">{summary.noiseFailures} failures</span>
              </div>
              <div className="h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-amber-500"
                  style={{ width: `${Math.min(100, (summary.noiseFailures / (summary.failureCount || 1)) * 100)}%` }}
                />
              </div>
            </div>

            {/* No Speech */}
            <div className="space-y-1 text-xs">
              <div className="flex justify-between font-mono text-[10px]">
                <span className="text-slate-400">Silence/No Speech</span>
                <span className="text-indigo-400">{summary.noSpeechFailures} failures</span>
              </div>
              <div className="h-1.5 bg-slate-950 rounded-full overflow-hidden">
                <div
                  className="h-full bg-indigo-500"
                  style={{ width: `${Math.min(100, (summary.noSpeechFailures / (summary.failureCount || 1)) * 100)}%` }}
                />
              </div>
            </div>
          </div>

          <div className="border-t border-slate-950 pt-3 text-[10px] text-slate-500 leading-normal flex gap-1.5 items-start font-sans">
            <Info className="w-3.5 h-3.5 text-indigo-400 shrink-0 mt-0.5" />
            <span>Spikes in Replay signatures can indicate targeted credential farming attempts. Review policy confidence constraints.</span>
          </div>
        </div>

        {/* Audit Search & list log */}
        <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl md:col-span-2 space-y-4">
          <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
            <div>
              <h4 className="font-sans font-semibold text-slate-200 text-xs uppercase tracking-wider">Enterprise Audit Logs</h4>
              <p className="text-[10px] text-slate-500 mt-0.5">Biometric action, authorization, and exception trail</p>
            </div>
            <button
              type="button"
              onClick={onClearLogs}
              className="text-[10px] font-mono text-slate-500 hover:text-rose-400 hover:bg-rose-500/5 px-2 py-1 rounded border border-slate-800 transition-colors cursor-pointer"
              id="btn-diagnostics-clear-logs"
            >
              Clear Local Logs
            </button>
          </div>

          {/* Search Bar & Status filter bar */}
          <div className="flex flex-col sm:flex-row gap-2">
            <div className="relative flex-1">
              <Search className="w-3.5 h-3.5 text-slate-500 absolute left-3 top-1/2 -translate-y-1/2" />
              <input
                type="text"
                placeholder="Search events, tokens, or IP..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full bg-slate-950 border border-slate-850 rounded-lg pl-9 pr-3 py-1.5 text-xs text-slate-300 placeholder:text-slate-600 focus:outline-none focus:border-indigo-500"
                id="input-diagnostics-search"
              />
            </div>
            <div className="flex gap-1 bg-slate-950 p-1 rounded-lg border border-slate-850 text-[10px]">
              <button
                type="button"
                onClick={() => setFilterStatus('all')}
                className={`px-2 py-1 rounded transition-colors ${filterStatus === 'all' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'}`}
              >
                All
              </button>
              <button
                type="button"
                onClick={() => setFilterStatus('success')}
                className={`px-2 py-1 rounded transition-colors ${filterStatus === 'success' ? 'bg-emerald-500/10 text-emerald-400' : 'text-slate-500 hover:text-slate-300'}`}
              >
                Passes
              </button>
              <button
                type="button"
                onClick={() => setFilterStatus('warning')}
                className={`px-2 py-1 rounded transition-colors ${filterStatus === 'warning' ? 'bg-amber-500/10 text-amber-400' : 'text-slate-500 hover:text-slate-300'}`}
              >
                Retries
              </button>
              <button
                type="button"
                onClick={() => setFilterStatus('failure')}
                className={`px-2 py-1 rounded transition-colors ${filterStatus === 'failure' ? 'bg-rose-500/10 text-rose-400' : 'text-slate-500 hover:text-slate-300'}`}
              >
                Spoofs
              </button>
            </div>
          </div>

          {/* Scrollable Logs box */}
          <div className="max-h-64 overflow-y-auto space-y-2 pr-1 scrollbar-thin">
            {filteredLogs.length === 0 ? (
              <div className="text-center py-10 text-slate-600 text-xs font-mono">
                Zero matching logs registered in current partition.
              </div>
            ) : (
              filteredLogs.map((log) => (
                <div
                  key={log.id}
                  className="bg-slate-950/60 p-3 rounded-xl border border-slate-850 flex flex-col sm:flex-row justify-between gap-2 text-xs"
                >
                  <div className="space-y-1.5 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                      <span className="font-mono text-[10px] bg-slate-900 px-1.5 py-0.5 rounded text-slate-400 border border-slate-800">
                        {log.action}
                      </span>
                      <span className={`h-2 w-2 rounded-full ${
                        log.status === 'success' 
                          ? 'bg-emerald-500' 
                          : log.status === 'warning' 
                          ? 'bg-amber-500' 
                          : 'bg-rose-500'
                      }`} />
                      <span className="font-mono text-[9px] text-slate-500">{new Date(log.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-slate-300 text-[11px] leading-relaxed font-sans">{log.details}</p>
                    
                    {log.amrToken && (
                      <div className="bg-slate-950 p-1.5 rounded font-mono text-[9px] text-slate-500 break-all select-all">
                        AMR Token: {log.amrToken}
                      </div>
                    )}
                  </div>
                  
                  <div className="flex sm:flex-col items-start sm:items-end justify-between sm:justify-start font-mono text-[9px] text-slate-500 border-t sm:border-t-0 border-slate-900 pt-1.5 sm:pt-0 shrink-0">
                    <span>ID: {log.id}</span>
                    <span>IP: {log.ipAddress}</span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
