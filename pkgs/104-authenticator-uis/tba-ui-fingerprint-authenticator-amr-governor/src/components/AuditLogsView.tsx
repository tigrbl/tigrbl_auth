import React, { useState } from 'react';
import { AuditEvent } from '../types';
import { ShieldAlert, CheckCircle, XCircle, FileText, Search, Filter, Eye, AlertCircle, Info } from 'lucide-react';

interface AuditLogsViewProps {
  logs: AuditEvent[];
}

export default function AuditLogsView({ logs }: AuditLogsViewProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'approved' | 'blocked' | 'fallback'>('all');
  const [selectedEvent, setSelectedEvent] = useState<AuditEvent | null>(null);

  const filteredLogs = logs.filter(log => {
    const matchesSearch = 
      log.username.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.sourceProvider.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.auditReference.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.description.toLowerCase().includes(searchTerm.toLowerCase());
      
    const matchesStatus = statusFilter === 'all' || log.status === statusFilter;
    
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="space-y-6" id="audit-logs-panel">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
            <FileText className="text-sky-400 w-5 h-5" />
            Security Evidence Audit Logs
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Redacted biometric provenance ledger. Tracks real-time verification status and cryptographic signature records.
          </p>
        </div>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-slate-950 border border-slate-900 rounded-xl p-4 flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search by username, provider, reference hash..." 
            className="w-full bg-slate-900 border border-slate-800 rounded-lg pl-9 pr-4 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500 font-mono"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
        
        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-500" />
          <select 
            className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-300 focus:outline-none focus:border-indigo-500"
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as any)}
          >
            <option value="all">All Outcomes</option>
            <option value="approved">Approved</option>
            <option value="blocked">Blocked</option>
            <option value="fallback">Fallback Routed</option>
          </select>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Ledger Table */}
        <div className="lg:col-span-8 bg-slate-950 border border-slate-900 rounded-xl overflow-hidden">
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs text-slate-400">
              <thead className="bg-slate-900/50 text-slate-300 uppercase font-mono text-3xs border-b border-slate-900">
                <tr>
                  <th className="p-3">Timestamp / Ref</th>
                  <th className="p-3">Subject</th>
                  <th className="p-3">Outcome</th>
                  <th className="p-3">Source & AMRs</th>
                  <th className="p-3 text-right">Details</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-900">
                {filteredLogs.length === 0 ? (
                  <tr>
                    <td colSpan={5} className="p-8 text-center text-slate-500">
                      No matching audit logs found under the current filters.
                    </td>
                  </tr>
                ) : (
                  filteredLogs.map((log) => (
                    <tr 
                      key={log.id} 
                      className={`hover:bg-slate-900/40 transition-colors cursor-pointer ${
                        selectedEvent?.id === log.id ? 'bg-indigo-950/10 border-l-2 border-indigo-500' : ''
                      }`}
                      onClick={() => setSelectedEvent(log)}
                    >
                      <td className="p-3 font-mono">
                        <div className="text-slate-300 text-2xs">
                          {new Date(log.timestamp).toLocaleTimeString()}
                        </div>
                        <div className="text-slate-600 text-3xs truncate w-24">
                          {log.auditReference}
                        </div>
                      </td>
                      <td className="p-3 font-medium text-slate-300">
                        {log.username}
                      </td>
                      <td className="p-3">
                        {log.status === 'approved' && (
                          <span className="bg-emerald-950/40 text-emerald-400 border border-emerald-900/50 px-2 py-0.5 rounded-full text-3xs font-semibold uppercase">
                            Approved
                          </span>
                        )}
                        {log.status === 'blocked' && (
                          <span className="bg-rose-950/40 text-rose-400 border border-rose-900/50 px-2 py-0.5 rounded-full text-3xs font-semibold uppercase">
                            Blocked
                          </span>
                        )}
                        {log.status === 'fallback' && (
                          <span className="bg-amber-950/40 text-amber-400 border border-amber-900/50 px-2 py-0.5 rounded-full text-3xs font-semibold uppercase">
                            Fallback
                          </span>
                        )}
                      </td>
                      <td className="p-3 font-mono">
                        <div className="text-slate-400 text-2xs truncate max-w-[140px]">
                          {log.sourceProvider}
                        </div>
                        <div className="flex gap-1 mt-1 flex-wrap">
                          {log.detectedAmrs.map((amr) => (
                            <span 
                              key={amr} 
                              className={`text-3xs px-1 rounded font-mono uppercase ${
                                amr === 'fpt' 
                                  ? 'bg-indigo-950 text-indigo-400 border border-indigo-900/40' 
                                  : 'bg-slate-900 text-slate-500 border border-slate-850'
                              }`}
                            >
                              {amr}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="p-3 text-right">
                        <button 
                          onClick={(e) => {
                            e.stopPropagation();
                            setSelectedEvent(log);
                          }}
                          className="p-1 bg-slate-900 hover:bg-slate-800 text-slate-400 hover:text-slate-200 rounded transition"
                        >
                          <Eye className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>

        {/* Selected Event details & Redacted Provenance Panel */}
        <div className="lg:col-span-4 bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4">
          <div className="border-b border-slate-900 pb-3">
            <h3 className="font-semibold text-slate-200 text-sm">
              Redacted Provenance Analysis
            </h3>
            <p className="text-2xs text-slate-500 mt-1">
              Select any event log row on the left to examine normalized signatures and diagnostic proofs.
            </p>
          </div>

          {selectedEvent ? (
            <div className="space-y-4 text-xs font-mono" id="provenance-detail-box">
              {/* Event title */}
              <div className="bg-slate-900 p-3 rounded-lg border border-slate-850">
                <span className="text-slate-500 text-3xs uppercase block font-mono">Event Narrative</span>
                <p className="text-xs font-sans text-slate-200 font-medium mt-1">
                  {selectedEvent.description}
                </p>
              </div>

              {/* Status parameters */}
              <div className="space-y-2">
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">Audit Hash Ref:</span>
                  <span className="text-slate-300 select-all truncate max-w-[150px]">{selectedEvent.auditReference}</span>
                </div>
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">Method Provider:</span>
                  <span className="text-slate-300">{selectedEvent.sourceProvider}</span>
                </div>
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">User Verified (UV):</span>
                  <span className="text-slate-300">{selectedEvent.userVerificationFlag ? "TRUE" : "FALSE"}</span>
                </div>
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">Fingerprint Evidence:</span>
                  <span className={selectedEvent.normalizedEvidence.hasFpt ? "text-emerald-400 font-bold" : "text-amber-500"}>
                    {selectedEvent.normalizedEvidence.hasFpt ? "fpt AMR Present" : "Absent / Incomplete"}
                  </span>
                </div>
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">Direct vs Transformed:</span>
                  <span className="text-slate-300 capitalize">{selectedEvent.normalizedEvidence.directVsTransformed}</span>
                </div>
                <div className="flex justify-between border-b border-slate-900 py-1">
                  <span className="text-slate-500">Evidence Freshness:</span>
                  <span className="text-slate-300">{selectedEvent.freshnessSeconds} seconds</span>
                </div>
              </div>

              {/* Redacted Hardware Metadata Panel */}
              <div className="bg-rose-950/10 border border-rose-950/60 p-4 rounded-xl space-y-2 font-sans text-xs">
                <div className="flex items-center gap-1.5 text-rose-400 font-semibold text-2xs uppercase tracking-wider">
                  <ShieldAlert className="w-4 h-4 flex-shrink-0" />
                  <span>Biometric Data Sanitization Summary</span>
                </div>
                <p className="text-3xs text-slate-400 leading-normal">
                  In compliance with regional biometric safety laws, raw hardware identifiers and sensor capture files have been permanently scrubbed.
                </p>
                
                <div className="font-mono text-2xs space-y-1 bg-slate-950/80 p-2.5 rounded border border-slate-900 mt-2 text-slate-400">
                  <div className="flex justify-between">
                    <span>Upstream Raw Claims:</span>
                    <span className="text-emerald-500">REDACTED_SUCCESS</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Template Match Score:</span>
                    <span className="text-slate-500">NOT_COLLECTED (0x00)</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Device Fingerprint Class:</span>
                    <span className="text-slate-300">{selectedEvent.redactedProvenance.deviceClass}</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Authentic Channel:</span>
                    <span className="text-slate-300">{selectedEvent.redactedProvenance.authChannel}</span>
                  </div>
                </div>
              </div>
            </div>
          ) : (
            <div className="h-64 bg-slate-900/20 border border-slate-900 border-dashed rounded-lg flex flex-col items-center justify-center p-6 text-center text-slate-500">
              <Info className="w-8 h-8 text-slate-600 mb-2" />
              <p className="text-xs">No event selected</p>
              <p className="text-3xs text-slate-600 mt-1 max-w-[200px]">
                Click the eyeball icon on any ledger event row to review cryptographic proofs.
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
