import React, { useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Download,
  RefreshCw,
  ShieldAlert,
  FileText,
  Search,
} from 'lucide-react';
import type {
  ChannelIncident,
  EvidenceReceipt,
  ChannelFamily,
} from '../types/communications.ts';

interface IncidentsAndEvidenceViewProps {
  incidents: ChannelIncident[];
  receipts: EvidenceReceipt[];
  onRefreshAll: () => void;
}

export const IncidentsAndEvidenceView: React.FC<IncidentsAndEvidenceViewProps> = ({
  incidents,
  receipts,
  onRefreshAll,
}) => {
  const [channelFilter, setChannelFilter] = useState<'ALL' | ChannelFamily>('ALL');
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedReceiptId, setSelectedReceiptId] = useState<string>(
    receipts[0]?.assertionId || ''
  );
  const [incidentBusyId, setIncidentBusyId] = useState<string | null>(null);

  const filteredReceipts = receipts.filter((r) => {
    const matchesChannel = channelFilter === 'ALL' || r.channelFamily === channelFilter;
    const matchesSearch =
      !searchQuery.trim() ||
      r.assertionId.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.representedIdentifier.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.actorPrincipal.toLowerCase().includes(searchQuery.toLowerCase()) ||
      r.reasonCode.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesChannel && matchesSearch;
  });

  const selectedReceipt =
    filteredReceipts.find((r) => r.assertionId === selectedReceiptId) ||
    filteredReceipts[0] ||
    receipts[0];

  const handleIncidentAction = async (
    incidentId: string,
    action: 'SUSPEND_SIGNING' | 'ROTATE_AND_RECOVER'
  ) => {
    setIncidentBusyId(incidentId);
    try {
      await fetch('/api/v1/incidents/action', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ incidentId, action }),
      });
      onRefreshAll();
    } finally {
      setIncidentBusyId(null);
    }
  };

  const downloadEvidenceReport = (receipt: EvidenceReceipt) => {
    const blob = new Blob([JSON.stringify(receipt, null, 2)], {
      type: 'application/json',
    });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${receipt.assertionId}-evidence-report.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 dark:border-slate-800">
        <div className="text-xs text-slate-500 dark:text-slate-400">
          Incident Containment, Key Rollover &amp; Content-Minimized Evidence Ledger
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-1">
          Channel Incident Response &amp; Cryptographic Evidence Center
        </h1>
        <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-3xl">
          Suspend compromised signing keys immediately while preserving point-in-time verification of historical artifacts. Evidence records store SHA-256 input/output digests and never retain raw call audio, email bodies, PDFs, or webhook payloads by default.
        </p>
      </div>

      {/* Section 1: Active Channel Incidents & Recovery */}
      <div className="space-y-4">
        <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
          Scoped Channel Incidents &amp; Point-in-Time Recovery Controls
        </h2>
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
          {incidents.map((inc) => (
            <div
              key={inc.id}
              className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-3"
            >
              <div className="flex items-start justify-between gap-3">
                <div>
                  <div className="text-xs font-mono text-slate-500">
                    {inc.id} · Severity: {inc.severity} · {inc.channelFamily}
                  </div>
                  <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                    {inc.title}
                  </h3>
                </div>
                <span
                  className={`text-xs font-mono shrink-0 font-semibold ${
                    inc.status === 'RESOLVED_HISTORICAL_PRESERVED'
                      ? 'text-emerald-700 dark:text-emerald-400'
                      : 'text-amber-700 dark:text-amber-400'
                  }`}
                >
                  {inc.status}
                </span>
              </div>

              <p className="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                {inc.summary}
              </p>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs space-y-1">
                <div className="font-semibold text-slate-900 dark:text-slate-100">
                  Point-in-Time Historical Verification Guarantee:
                </div>
                <div className="text-slate-600 dark:text-slate-400">
                  {inc.historicalVerificationRule}
                </div>
              </div>

              <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-slate-200 dark:border-slate-800">
                <div className="text-xs font-mono text-slate-500">
                  Key: {inc.affectedKeyId}
                </div>
                <div className="flex items-center gap-2">
                  <button
                    type="button"
                    onClick={() => handleIncidentAction(inc.id, 'SUSPEND_SIGNING')}
                    disabled={incidentBusyId === inc.id}
                    className="px-3 py-1.5 text-xs font-medium text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/50 hover:bg-rose-100 border border-rose-200 dark:border-rose-900 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                  >
                    Enforce Signing Suspension
                  </button>
                  <button
                    type="button"
                    onClick={() => handleIncidentAction(inc.id, 'ROTATE_AND_RECOVER')}
                    disabled={incidentBusyId === inc.id}
                    className="px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                  >
                    Rotate Key &amp; Recover Identity
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Section 2: Content-Minimized Evidence Receipt Ledger & Inspector */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
          <div className="p-4 border-b border-slate-200 dark:border-slate-800 space-y-3">
            <div className="flex flex-wrap items-center justify-between gap-2">
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                Secret-Safe Evidence Receipt Ledger
              </h2>
              <span className="text-xs font-mono text-slate-500">
                Raw Message Retention: Disabled (SHA-256 Digest Only)
              </span>
            </div>

            <div className="flex flex-col sm:flex-row gap-3">
              <div className="relative flex-1">
                <Search className="w-3.5 h-3.5 text-slate-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter by assertion ID, identity, actor, or reason code..."
                  className="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                />
              </div>
              <select
                value={channelFilter}
                onChange={(e) => setChannelFilter(e.target.value as 'ALL' | ChannelFamily)}
                className="px-3 py-1.5 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
              >
                <option value="ALL">All Channels</option>
                <option value="webhook-http-sig">RFC 9421 Webhooks</option>
                <option value="stir-shaken">STIR/SHAKEN Voice</option>
                <option value="bimi-mark">BIMI / VMC Email</option>
                <option value="smime">S/MIME 4.0 Email</option>
                <option value="document-signing">Document Signing</option>
              </select>
            </div>
          </div>

          <div className="divide-y divide-slate-200 dark:divide-slate-800">
            {filteredReceipts.map((rcp) => {
              const isSelected = selectedReceipt?.assertionId === rcp.assertionId;
              return (
                <button
                  key={rcp.assertionId}
                  type="button"
                  onClick={() => setSelectedReceiptId(rcp.assertionId)}
                  className={`w-full text-left p-4 transition-colors cursor-pointer ${
                    isSelected
                      ? 'bg-blue-50/60 dark:bg-blue-950/30'
                      : 'hover:bg-slate-50 dark:hover:bg-slate-800/40'
                  }`}
                >
                  <div className="flex items-center justify-between gap-2 text-xs">
                    <div className="flex items-center gap-2 font-mono font-semibold text-slate-900 dark:text-slate-100">
                      {rcp.verificationStatus === 'valid' ? (
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                      ) : (
                        <XCircle className="w-3.5 h-3.5 text-rose-600 shrink-0" />
                      )}
                      <span>{rcp.assertionId}</span>
                      <span className="text-slate-400">·</span>
                      <span className="text-slate-600 dark:text-slate-400">
                        {rcp.channelFamily}
                      </span>
                    </div>
                    <span className="font-mono text-slate-500 tabular-nums">
                      {rcp.timestamp} ({rcp.latencyMs}ms)
                    </span>
                  </div>
                  <div className="text-xs font-medium text-slate-800 dark:text-slate-200 mt-1">
                    {rcp.qualifiedResultLabel}
                  </div>
                  <div className="text-xs text-slate-500 font-mono mt-0.5 truncate">
                    Actor: {rcp.actorPrincipal} → Identity: {rcp.representedIdentifier}
                  </div>
                </button>
              );
            })}
          </div>
        </div>

        {/* Right 5 Columns: Selected Evidence Receipt Deep Inspector */}
        <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
          {selectedReceipt ? (
            <>
              <div className="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-slate-800">
                <div>
                  <div className="text-xs font-mono text-slate-500">
                    Receipt {selectedReceipt.assertionId}
                  </div>
                  <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                    Evidence Package &amp; Scope Separation
                  </h3>
                </div>
                <button
                  type="button"
                  onClick={() => downloadEvidenceReport(selectedReceipt)}
                  className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-200 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-md whitespace-nowrap shrink-0 cursor-pointer"
                >
                  <Download className="w-3.5 h-3.5" />
                  Export JSON Report
                </button>
              </div>

              <div className="space-y-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 p-3.5 rounded-lg border border-slate-200 dark:border-slate-800">
                <div>
                  <span className="text-slate-500">Profile:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.profileId} (v{selectedReceipt.profileVersion})
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Authority Ref:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.authorityReference}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Policy Decision:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.policyDecisionId} ({selectedReceipt.authorizationOutcome})
                  </span>
                </div>
                <div className="break-all">
                  <span className="text-slate-500">Input Digest:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.inputContentDigestSha256}
                  </span>
                </div>
                <div className="break-all">
                  <span className="text-slate-500">Signature Digest:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.signatureOutputDigestSha256}
                  </span>
                </div>
                <div>
                  <span className="text-slate-500">Covered Components:</span>{' '}
                  <span className="text-slate-900 dark:text-slate-100">
                    {selectedReceipt.coveredComponents.join(', ') || 'None (Denied)'}
                  </span>
                </div>
              </div>

              <div className="space-y-2 text-xs">
                <div className="font-semibold text-emerald-700 dark:text-emerald-400">
                  Cryptographic Proof Establishes:
                </div>
                <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                  {selectedReceipt.productPromise.establishes.map((item, i) => (
                    <li key={i}>• {item}</li>
                  ))}
                </ul>
                <div className="font-semibold text-amber-700 dark:text-amber-400 pt-2">
                  Does NOT Establish (Separated from Business/Legal Conclusions):
                </div>
                <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                  {selectedReceipt.productPromise.doesNotEstablish.map((item, i) => (
                    <li key={i}>• {item}</li>
                  ))}
                </ul>
              </div>
            </>
          ) : (
            <div className="py-12 text-center text-xs text-slate-500">
              Select an evidence receipt from the ledger to inspect its digests and scope.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
