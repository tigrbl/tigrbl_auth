import React, { useState } from 'react';
import { 
  Database, 
  Trash2, 
  Search, 
  ShieldCheck, 
  ShieldAlert, 
  Clock, 
  Info, 
  UserX, 
  Terminal,
  ChevronDown,
  ChevronUp,
  FileSpreadsheet
} from 'lucide-react';
import { AuditLog, ActiveSession } from '../types';

interface SecurityInvestigationLogsProps {
  auditLogs: AuditLog[];
  activeSessions: ActiveSession[];
  onRevokeSession: (id: string) => void;
  onClearAuditTrail: () => void;
}

export default function SecurityInvestigationLogs({
  auditLogs,
  activeSessions,
  onRevokeSession,
  onClearAuditTrail
}: SecurityInvestigationLogsProps) {
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [expandedLogId, setExpandedLogId] = useState<string | null>(null);

  // Filter audit logs based on search query
  const filteredLogs = auditLogs.filter(log => {
    const q = searchQuery.toLowerCase();
    return (
      log.subject.toLowerCase().includes(q) ||
      log.action.toLowerCase().includes(q) ||
      log.trackingId.toLowerCase().includes(q) ||
      log.decision.toLowerCase().includes(q) ||
      log.redactedEvidence.toLowerCase().includes(q)
    );
  });

  const toggleLogExpand = (logId: string) => {
    setExpandedLogId(expandedLogId === logId ? null : logId);
  };

  return (
    <div id="security-investigation-section" className="grid grid-cols-1 lg:grid-cols-3 gap-6">
      
      {/* 1. Active User Sessions context manager (P1) */}
      <div className="lg:col-span-1 rounded-2xl border border-slate-200 bg-white shadow-xs p-6 flex flex-col h-full">
        <div className="mb-4">
          <div className="flex items-center gap-2">
            <Terminal className="h-5 w-5 text-slate-700" />
            <h3 className="font-display text-lg font-bold text-slate-900 font-display">Enrolled Sessions Context</h3>
          </div>
          <p className="text-xs text-slate-500 mt-1 font-sans">
            Securely revoke or investigate active device cookies. Immediate revocation triggers step-up constraints.
          </p>
        </div>

        <div className="space-y-4 flex-1 overflow-y-auto max-h-[480px]">
          {activeSessions.length === 0 ? (
            <div className="text-center py-10 text-slate-400 text-xs font-sans">
              All active sessions successfully revoked.
            </div>
          ) : (
            activeSessions.map(session => {
              return (
                <div 
                  key={session.id} 
                  className={`p-4 rounded-xl border relative ${
                    session.riskLevel === 'critical' ? 'bg-red-50/50 border-red-100'
                    : session.riskLevel === 'medium' ? 'bg-amber-50/40 border-amber-100'
                    : 'bg-slate-50/50 border-slate-100'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-display font-bold text-xs text-slate-900 truncate block">
                      {session.device}
                    </span>
                    <span className={`text-[9px] font-mono font-medium uppercase px-2 py-0.2 rounded border ${
                      session.riskLevel === 'critical' ? 'bg-red-100 border-red-200 text-red-800'
                      : session.riskLevel === 'medium' ? 'bg-amber-100 border-amber-200 text-amber-800'
                      : 'bg-emerald-100 border-emerald-200 text-emerald-800'
                    }`}>
                      {session.riskLevel}
                    </span>
                  </div>

                  <div className="mt-3 grid grid-cols-2 gap-y-2 text-[10px] font-mono text-slate-500">
                    <div>
                      <span className="block text-slate-400">IP address:</span>
                      <span className="text-slate-800 font-semibold">{session.ipAddress}</span>
                    </div>
                    <div>
                      <span className="block text-slate-400">Location:</span>
                      <span className="text-slate-800 truncate block">{session.location}</span>
                    </div>
                    <div>
                      <span className="block text-slate-400">Started:</span>
                      <span className="text-slate-700">{session.startTime}</span>
                    </div>
                    <div>
                      <span className="block text-slate-400">AMR achieved:</span>
                      <span className="text-emerald-700 font-semibold">{session.amr.join(', ')}</span>
                    </div>
                  </div>

                  {session.signalsVerified.length > 0 && (
                    <div className="mt-3.5 pt-2 border-t border-slate-200/50">
                      <span className="block text-[9px] font-mono text-slate-400 uppercase">Verified Posture telemetry</span>
                      <div className="flex flex-wrap gap-1.5 mt-1">
                        {session.signalsVerified.map(sig => (
                          <span key={sig} className="bg-slate-100 text-slate-600 px-1.5 py-0.5 rounded text-[9px] font-mono border border-slate-200/50">
                            {sig.replace('sig_', '')}
                          </span>
                        ))}
                      </div>
                    </div>
                  )}

                  <button
                    onClick={() => onRevokeSession(session.id)}
                    className="mt-3.5 w-full flex items-center justify-center gap-1.5 rounded-lg border border-slate-200 hover:border-red-200 bg-white hover:bg-red-50 hover:text-red-700 py-1.5 text-xs font-semibold text-slate-700 transition"
                  >
                    <UserX className="h-3.5 w-3.5" />
                    <span>Revoke Access Grant</span>
                  </button>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* 2. Audit Trails & Security Investigations logs (P2) */}
      <div className="lg:col-span-2 rounded-2xl border border-slate-200 bg-white shadow-xs p-6 flex flex-col h-full">
        
        {/* Header toolbar */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-5">
          <div>
            <div className="flex items-center gap-2">
              <Database className="h-5 w-5 text-slate-700" />
              <h3 className="font-display text-lg font-bold text-slate-900">Security Audit Investigations</h3>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-sans">
              Cryptographically correlated tracking logs of user actions, decisions, and redacted signal class vectors.
            </p>
          </div>

          <button
            onClick={onClearAuditTrail}
            className="text-xs font-semibold text-slate-500 hover:text-red-600 transition flex items-center gap-1"
          >
            <Trash2 className="h-4 w-4" />
            <span>Clear Trail</span>
          </button>
        </div>

        {/* Search */}
        <div className="relative mb-4">
          <Search className="absolute left-3 top-2.5 h-4 w-4 text-slate-400" />
          <input
            type="text"
            placeholder="Search redacted evidence, decision types, or tracking reference codes..."
            value={searchQuery}
            onChange={e => setSearchQuery(e.target.value)}
            className="w-full text-xs border border-slate-200 rounded-xl pl-9 pr-4 py-2.5 bg-slate-50/50"
          />
        </div>

        {/* Table/List */}
        <div className="flex-1 overflow-y-auto max-h-[480px] space-y-2">
          {filteredLogs.length === 0 ? (
            <div className="text-center py-16 text-slate-400 text-xs font-sans">
              No audit logs matched search criteria.
            </div>
          ) : (
            filteredLogs.map(log => {
              const isExpanded = expandedLogId === log.id;
              return (
                <div 
                  key={log.id} 
                  className={`border rounded-xl transition duration-150 ${
                    isExpanded ? 'bg-slate-50 border-slate-300' : 'bg-white border-slate-200 hover:border-slate-300'
                  }`}
                >
                  {/* Top Summary row */}
                  <div 
                    onClick={() => toggleLogExpand(log.id)}
                    className="p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 cursor-pointer select-none"
                  >
                    <div className="flex items-start gap-3 min-w-0">
                      <div className={`mt-0.5 flex h-7 w-7 flex-shrink-0 items-center justify-center rounded-lg ${
                        log.decision === 'continue' ? 'bg-emerald-50 text-emerald-600'
                        : log.decision === 'step-up' ? 'bg-amber-50 text-amber-600'
                        : log.decision === 'deny' ? 'bg-rose-50 text-rose-600'
                        : 'bg-indigo-50 text-indigo-600'
                      }`}>
                        {log.decision === 'continue' ? (
                          <ShieldCheck className="h-4 w-4" />
                        ) : (
                          <ShieldAlert className="h-4 w-4" />
                        )}
                      </div>

                      <div className="min-w-0">
                        <div className="flex items-center gap-2">
                          <span className="font-display font-semibold text-xs text-slate-900 truncate">
                            {log.action}
                          </span>
                          <span className="text-[10px] font-mono bg-slate-100 text-slate-500 px-1.5 py-0.2 rounded flex-shrink-0">
                            {log.trackingId}
                          </span>
                        </div>
                        
                        <div className="flex items-center gap-3 text-[10px] font-mono text-slate-400 mt-0.5">
                          <span>{log.subject}</span>
                          <span>•</span>
                          <span>{log.timestamp.replace('T', ' ').substring(11, 19)} UTC</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex items-center gap-3 flex-shrink-0 self-end sm:self-center">
                      <div className="text-right">
                        <span className={`text-[10px] font-mono font-bold capitalize px-2 py-0.5 rounded border ${
                          log.decision === 'continue' ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
                          : log.decision === 'step-up' ? 'bg-amber-50 text-amber-700 border-amber-200'
                          : log.decision === 'deny' ? 'bg-rose-50 text-rose-700 border-rose-200'
                          : 'bg-indigo-50 text-indigo-700 border-indigo-200'
                        }`}>
                          {log.decision}
                        </span>
                      </div>

                      {isExpanded ? <ChevronUp className="h-4 w-4 text-slate-400" /> : <ChevronDown className="h-4 w-4 text-slate-400" />}
                    </div>
                  </div>

                  {/* Expanded evidence details */}
                  {isExpanded && (
                    <div className="px-4 pb-4 pt-1.5 border-t border-slate-200/60 bg-slate-50/50 rounded-b-xl space-y-3.5 text-[11px] font-mono">
                      
                      <div className="grid grid-cols-2 gap-4">
                        <div>
                          <span className="text-slate-400 block text-[9px] uppercase">RBA Policy Enforced</span>
                          <span className="text-slate-800 font-medium block mt-0.5">{log.policyVersion}</span>
                        </div>
                        <div>
                          <span className="text-slate-400 block text-[9px] uppercase">Freshness Status</span>
                          <span className={`font-semibold block mt-0.5 ${log.freshnessMet ? 'text-emerald-600' : 'text-amber-600'}`}>
                            {log.freshnessMet ? 'FRESHNESS VERIFIED ✓' : 'STALE (RE-EVAL FORCED)'}
                          </span>
                        </div>
                      </div>

                      <div>
                        <span className="text-slate-400 block text-[9px] uppercase">Active Telemetry Classes Evaluated</span>
                        <div className="flex flex-wrap gap-1.5 mt-1">
                          {log.signalClasses.length === 0 ? (
                            <span className="text-slate-500">None evaluated (Direct bypass allow)</span>
                          ) : (
                            log.signalClasses.map(sc => (
                              <span key={sc} className="bg-slate-200/70 text-slate-700 px-1.5 py-0.5 rounded text-[10px] capitalize">
                                {sc}
                              </span>
                            ))
                          )}
                        </div>
                      </div>

                      <div>
                        <span className="text-slate-400 block text-[9px] uppercase">Authentications Satisfied (AMR)</span>
                        <span className="text-slate-800 font-semibold block mt-0.5">
                          {log.achievedMethods.length > 0 ? log.achievedMethods.join(', ') : 'None (held/blocked)'}
                        </span>
                      </div>

                      <div className="bg-white p-3 rounded-lg border border-slate-200/60">
                        <span className="text-slate-400 block text-[9px] uppercase mb-1">Redacted Evidence Output</span>
                        <span className="text-slate-800 leading-relaxed font-sans text-xs">
                          {log.redactedEvidence}
                        </span>
                      </div>

                      <div className="flex justify-between items-center text-[9px] text-slate-400 pt-1.5 border-t border-slate-200/40">
                        <span>Tenant: {log.tenantId}</span>
                        <span>Crypto Signature Verified</span>
                      </div>

                    </div>
                  )}
                </div>
              );
            })
          )}
        </div>

      </div>

    </div>
  );
}
