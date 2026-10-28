import React, { useState } from 'react';
import { AuditEvent } from '../types';
import { Search, Terminal, AlertTriangle, CheckCircle, Info, ChevronDown, ChevronUp, RefreshCw, Eye } from 'lucide-react';

interface DiagnosticsProps {
  events: AuditEvent[];
  onClear: () => void;
}

export const DiagnosticsTimeline: React.FC<DiagnosticsProps> = ({ events, onClear }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState<'all' | 'orchestration' | 'policy' | 'provider' | 'enrollment'>('all');
  const [expandedEventId, setExpandedEventId] = useState<string | null>(null);

  const filteredEvents = events.filter((e) => {
    const matchesSearch = e.message.toLowerCase().includes(searchTerm.toLowerCase()) || 
      (e.details && JSON.stringify(e.details).toLowerCase().includes(searchTerm.toLowerCase()));
    const matchesCategory = selectedCategory === 'all' || e.category === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  const getLevelIcon = (level: AuditEvent['level']) => {
    switch (level) {
      case 'success':
        return <CheckCircle className="h-4 w-4 text-emerald-400" />;
      case 'warn':
        return <AlertTriangle className="h-4 w-4 text-amber-400" />;
      case 'error':
        return <AlertTriangle className="h-4 w-4 text-rose-400" />;
      case 'info':
      default:
        return <Info className="h-4 w-4 text-sky-400" />;
    }
  };

  const getCategoryColor = (category: AuditEvent['category']) => {
    switch (category) {
      case 'orchestration':
        return 'bg-purple-500/10 text-purple-400 border border-purple-500/20';
      case 'policy':
        return 'bg-blue-500/10 text-blue-400 border border-blue-500/20';
      case 'provider':
        return 'bg-amber-500/10 text-amber-400 border border-amber-500/20';
      case 'enrollment':
        return 'bg-teal-500/10 text-teal-400 border border-teal-500/20';
    }
  };

  const toggleExpand = (id: string) => {
    setExpandedEventId(expandedEventId === id ? null : id);
  };

  return (
    <div className="space-y-3 bg-zinc-950/60 rounded-xl border border-zinc-800 p-4" id="diagnostics-timeline">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-zinc-800 pb-3">
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-zinc-400" />
          <div>
            <h3 className="font-semibold text-zinc-100 text-sm">Security Correlation & Diagnostics</h3>
            <p className="text-[11px] text-zinc-400 mt-0.5">Real-time orchestrated cryptographically-signed audit trace.</p>
          </div>
        </div>
        <button
          onClick={onClear}
          className="text-2xs text-zinc-500 hover:text-zinc-300 transition font-mono border border-zinc-800 rounded-md px-2 py-1 self-start sm:self-auto hover:bg-zinc-900"
        >
          Clear Logs
        </button>
      </div>

      {/* Filter Bar */}
      <div className="flex flex-col gap-2">
        <div className="relative">
          <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-zinc-500" />
          <input
            type="text"
            placeholder="Search trace details, message, or payload hashes..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full bg-zinc-900/60 border border-zinc-800 rounded-lg pl-8 pr-3 py-1.5 text-xs text-zinc-200 placeholder-zinc-500 focus:outline-none focus:border-zinc-700 font-mono"
          />
        </div>

        <div className="flex flex-wrap gap-1">
          {(['all', 'orchestration', 'policy', 'provider', 'enrollment'] as const).map((cat) => (
            <button
              key={cat}
              onClick={() => setSelectedCategory(cat)}
              className={`px-2.5 py-1 rounded-md text-[10px] font-mono capitalize border transition ${
                selectedCategory === cat
                  ? 'bg-zinc-800 text-zinc-100 border-zinc-700'
                  : 'bg-zinc-900/30 text-zinc-500 border-transparent hover:border-zinc-800 hover:text-zinc-400'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </div>

      {/* Timeline container */}
      <div className="max-h-[300px] overflow-y-auto space-y-2 pr-1 custom-scrollbar">
        {filteredEvents.length === 0 ? (
          <div className="text-center py-8 text-zinc-600 text-xs font-mono">
            No diagnostic events matching the filter criteria.
          </div>
        ) : (
          filteredEvents.map((e) => {
            const isExpanded = expandedEventId === e.id;
            return (
              <div
                key={e.id}
                className={`border rounded-lg transition-all ${
                  isExpanded ? 'bg-zinc-900/40 border-zinc-700' : 'bg-zinc-900/20 border-zinc-800/80 hover:bg-zinc-900/30'
                }`}
                id={`audit-event-${e.id}`}
              >
                <div
                  onClick={() => toggleExpand(e.id)}
                  className="flex items-start gap-2.5 p-2.5 cursor-pointer select-none"
                >
                  <div className="mt-0.5 shrink-0">{getLevelIcon(e.level)}</div>
                  <div className="flex-1 min-w-0 space-y-1">
                    <div className="flex flex-wrap items-center gap-x-2 gap-y-1">
                      <span className="text-[10px] text-zinc-500 font-mono shrink-0">
                        {new Date(e.timestamp).toLocaleTimeString([], { hour12: false })}
                      </span>
                      <span className={`text-[9px] px-1.5 py-0.2 rounded-full font-mono font-medium tracking-wide uppercase shrink-0 ${getCategoryColor(e.category)}`}>
                        {e.category}
                      </span>
                      <span className="text-[10px] text-zinc-500 font-mono shrink-0 truncate max-w-[100px]">
                        ID: {e.ceremonyId.slice(0, 6)}...
                      </span>
                    </div>
                    <p className="text-xs text-zinc-300 font-mono leading-relaxed break-words">
                      {e.message}
                    </p>
                  </div>
                  <div className="text-zinc-500 hover:text-zinc-300 transition self-center p-0.5">
                    {isExpanded ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                  </div>
                </div>

                {isExpanded && e.details && (
                  <div className="border-t border-zinc-800 bg-black/40 p-3 rounded-b-lg font-mono text-[10px] text-emerald-400/90 overflow-x-auto space-y-2 max-w-full">
                    <div className="flex items-center justify-between text-[9px] text-zinc-500 uppercase font-bold tracking-wider border-b border-zinc-800 pb-1 mb-2">
                      <span>Cryptographic Evidence Payload</span>
                      <span className="text-emerald-500 font-normal">verified-by-server ●</span>
                    </div>
                    <pre className="whitespace-pre-wrap leading-relaxed">
                      {JSON.stringify(e.details, null, 2)}
                    </pre>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
