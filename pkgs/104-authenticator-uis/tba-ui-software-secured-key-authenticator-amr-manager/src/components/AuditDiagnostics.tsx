import React, { useState } from 'react';
import { History, Search, Download, AlertTriangle, ShieldCheck, HelpCircle } from 'lucide-react';
import { AuditEvent, StorageClassification } from '../types';

interface AuditDiagnosticsProps {
  events: AuditEvent[];
  onClearLogs: () => void;
}

export default function AuditDiagnostics({ events, onClearLogs }: AuditDiagnosticsProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');

  const filteredEvents = events.filter((e) => {
    const matchesSearch =
      e.details.toLowerCase().includes(searchTerm.toLowerCase()) ||
      e.actor.toLowerCase().includes(searchTerm.toLowerCase()) ||
      e.hash.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesType = filterType === 'all' || e.eventType === filterType;

    return matchesSearch && matchesType;
  });

  const exportAudit = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(events, null, 2));
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "swk-audit-diagnostic-logs.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  return (
    <div id="audit-diagnostics" className="bg-white border border-slate-200 rounded-xl p-5 space-y-4 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
        <div className="flex items-center gap-2">
          <History className="w-5 h-5 text-indigo-600" />
          <h4 className="font-semibold text-slate-800 text-sm">Operator Cryptographic Audit & Diagnostics</h4>
        </div>
        <div className="flex gap-2">
          <button
            onClick={exportAudit}
            id="btn-export-audit"
            className="text-xs text-slate-700 bg-slate-50 hover:bg-slate-100 border border-slate-300 rounded-lg py-1.5 px-3 flex items-center gap-1 font-semibold transition-colors cursor-pointer"
          >
            <Download className="w-3.5 h-3.5" /> Export JSON
          </button>
          <button
            onClick={onClearLogs}
            id="btn-clear-audit"
            className="text-xs text-rose-700 bg-rose-50 hover:bg-rose-100 border border-rose-200 rounded-lg py-1.5 px-3 font-semibold transition-colors cursor-pointer"
          >
            Clear Log
          </button>
        </div>
      </div>

      {/* Filter and Search controls */}
      <div className="flex flex-col sm:flex-row gap-2">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            id="input-audit-search"
            type="text"
            placeholder="Search details, actors, or hash..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full text-xs pl-9 pr-3 py-2.5 bg-slate-50 border border-slate-200 rounded-lg outline-none focus:ring-2 focus:ring-indigo-500"
          />
        </div>

        <select
          id="select-audit-filter"
          value={filterType}
          onChange={(e) => setFilterType(e.target.value)}
          className="text-xs bg-slate-50 border border-slate-200 rounded-lg px-3 py-2.5 outline-none focus:ring-2 focus:ring-indigo-500 cursor-pointer font-medium"
        >
          <option value="all">All Event Types</option>
          <option value="registration">Registration Only</option>
          <option value="proof_generation">Proof Generation</option>
          <option value="verification">Verification Check</option>
          <option value="rotation">Key Rotation</option>
          <option value="compromise">Compromise Report</option>
          <option value="policy_change">Policy Changes</option>
          <option value="error">Errors Only</option>
        </select>
      </div>

      {/* Event Timeline Table */}
      <div className="border border-slate-150 rounded-xl overflow-hidden bg-slate-50/50">
        <div className="max-h-[350px] overflow-y-auto">
          {filteredEvents.length === 0 ? (
            <div className="p-8 text-center text-xs text-slate-400 italic">
              No matching diagnostic events logged in this session.
            </div>
          ) : (
            <div className="divide-y divide-slate-150">
              {filteredEvents.map((event) => (
                <div
                  key={event.id}
                  id={`audit-row-${event.id}`}
                  className="p-4 hover:bg-white transition-colors space-y-2 text-xs"
                >
                  <div className="flex flex-wrap items-center justify-between gap-2">
                    <div className="flex items-center gap-1.5 flex-wrap">
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold font-mono ${
                        event.eventType === 'error' || event.eventType === 'compromise'
                          ? 'bg-rose-50 text-rose-700 border border-rose-200'
                          : event.eventType === 'registration' || event.eventType === 'rotation'
                          ? 'bg-indigo-50 text-indigo-700 border border-indigo-200'
                          : 'bg-slate-100 text-slate-600 border border-slate-200'
                      }`}>
                        {event.eventType.toUpperCase()}
                      </span>
                      <span className="text-slate-400 font-mono text-[10px]">
                        {new Date(event.timestamp).toLocaleTimeString()}
                      </span>
                    </div>

                    {/* Verified indicator badge */}
                    <div className="flex items-center gap-1">
                      {event.evidenceVerified ? (
                        <span className="flex items-center gap-0.5 text-emerald-600 font-semibold text-[10px]">
                          <ShieldCheck className="w-3.5 h-3.5" /> swk verified
                        </span>
                      ) : event.storageClass === 'hardware_backed' ? (
                        <span className="flex items-center gap-0.5 text-blue-600 font-semibold text-[10px]">
                          <ShieldCheck className="w-3.5 h-3.5" /> hwk verified
                        </span>
                      ) : (
                        <span className="flex items-center gap-0.5 text-slate-400 font-semibold text-[10px]">
                          <HelpCircle className="w-3.5 h-3.5" /> backing unverified
                        </span>
                      )}
                    </div>
                  </div>

                  {/* Details paragraph */}
                  <p className="text-slate-700 leading-relaxed font-sans">{event.details}</p>

                  {/* Redacted cryptographic identifiers */}
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 pt-1.5 border-t border-slate-100 text-[10px] text-slate-400 font-mono">
                    <div>
                      Actor: <span className="text-slate-600 font-semibold">{event.actor}</span> | Profile: <span className="text-slate-600 font-semibold uppercase">{event.profile}</span>
                    </div>
                    <div className="truncate max-w-xs" title={`Redacted hash: ${event.hash}`}>
                      Digest: <span className="text-slate-500">{event.hash}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
