/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { FileText, ShieldAlert, CheckCircle, AlertTriangle, Search, Filter } from 'lucide-react';
import { AuditLog } from '../types';

interface SecurityAuditLogsProps {
  logs: AuditLog[];
}

export default function SecurityAuditLogs({ logs }: SecurityAuditLogsProps) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterType, setFilterType] = useState<string>('all');

  const filteredLogs = logs.filter((log) => {
    const matchesSearch =
      log.summary.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.details.toLowerCase().includes(searchTerm.toLowerCase()) ||
      log.actor.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesFilter = filterType === 'all' || log.eventType === filterType;

    return matchesSearch && matchesFilter;
  });

  return (
    <div id="security-audit-logs" className="bg-white rounded-2xl border border-slate-200 p-6 space-y-4 shadow-sm">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
        <div>
          <h3 className="font-display font-semibold text-slate-800 text-lg flex items-center gap-2">
            <FileText className="w-5 h-5 text-slate-600" />
            Security Audit Logs & Telemetry
          </h3>
          <p className="text-xs text-slate-500">Immutable log of Windows Integrated Authentication handshakes, mapping linking events, and policy adjustments.</p>
        </div>
      </div>

      {/* Filter and Search */}
      <div className="flex flex-col sm:flex-row gap-3">
        <div className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            placeholder="Search audit records (e.g. Actor, Summary, SID)..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            className="w-full pl-9 pr-4 py-2 text-xs rounded-lg border border-slate-200 outline-none focus:border-blue-500"
          />
        </div>

        <div className="flex gap-2">
          <Filter className="w-4 h-4 text-slate-400 self-center" />
          <select
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            className="px-2.5 py-2 text-xs rounded-lg border border-slate-200 bg-white"
          >
            <option value="all">All Events</option>
            <option value="discovery">Discovery</option>
            <option value="negotiation">Negotiation</option>
            <option value="token_validation">Validation</option>
            <option value="account_link">Linking</option>
            <option value="policy_update">Policy Updates</option>
            <option value="health_alert">Health Alerts</option>
            <option value="error">Errors</option>
          </select>
        </div>
      </div>

      {/* Logs Table */}
      <div className="overflow-x-auto border border-slate-100 rounded-xl">
        <div className="divide-y divide-slate-100 max-h-96 overflow-y-auto scrollbar-thin">
          {filteredLogs.length > 0 ? (
            filteredLogs.map((log) => (
              <div key={log.id} className="p-4 hover:bg-slate-50/50 flex flex-col md:flex-row md:items-start justify-between gap-4 text-xs">
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2.5">
                    <span className={`text-[9px] font-semibold font-mono px-2 py-0.5 rounded border ${
                      log.status === 'success' ? 'bg-emerald-50 text-emerald-700 border-emerald-150' :
                      log.status === 'warning' ? 'bg-amber-50 text-amber-700 border-amber-150' :
                      'bg-rose-50 text-rose-700 border-rose-150'
                    }`}>
                      {log.eventType.toUpperCase()}
                    </span>
                    <span className="text-slate-400 font-mono text-[10px]">{log.timestamp}</span>
                    <span className="text-slate-500 font-medium font-mono">Actor: {log.actor}</span>
                  </div>

                  <p className="font-semibold text-slate-800 leading-snug">{log.summary}</p>
                  <p className="text-slate-600 leading-relaxed font-sans text-[11px] bg-slate-50 p-2 rounded border border-slate-100 font-mono break-all whitespace-pre-wrap">{log.details}</p>

                  {log.amr && (
                    <div className="flex gap-1.5 items-center pt-1">
                      <span className="text-[10px] text-slate-400 font-mono">AMR Evidence:</span>
                      {log.amr.map((val, i) => (
                        <span key={i} className="bg-slate-100 text-slate-700 px-1.5 py-0.2 rounded text-[10px] font-mono border border-slate-200">
                          {val}
                        </span>
                      ))}
                    </div>
                  )}
                </div>

                <div className="text-right shrink-0 flex flex-col items-end justify-between self-stretch text-[10px] text-slate-400 font-mono space-y-2">
                  <div className="flex items-center gap-1.5">
                    {log.status === 'success' ? (
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                    ) : log.status === 'warning' ? (
                      <AlertTriangle className="w-4 h-4 text-amber-500" />
                    ) : (
                      <ShieldAlert className="w-4 h-4 text-rose-600" />
                    )}
                  </div>
                  <div className="space-y-0.5">
                    <p className="truncate max-w-[150px]">IP: {log.ipAddress}</p>
                    <p className="truncate max-w-[150px]" title={log.userAgent}>UA: {log.userAgent.split(' ')[0]}</p>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <div className="p-8 text-center text-slate-400 italic">
              No matching security audit logs found. Try adjusting filters or performing authentications.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
