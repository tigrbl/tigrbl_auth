/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { TenantEvidencePolicy, TrustedProvider, AuditLogEntry } from '../types';
import { Shield, KeyRound, AlertTriangle, CheckCircle, Info, RefreshCw, Activity, Eye, Sliders, Database, Users, HelpCircle, ToggleLeft, ShieldCheck } from 'lucide-react';

interface AdminPolicyDashboardProps {
  policy: TenantEvidencePolicy;
  onUpdatePolicy: (updated: TenantEvidencePolicy) => void;
  providers: TrustedProvider[];
  onUpdateProviders: (updated: TrustedProvider[]) => void;
  auditLogs: AuditLogEntry[];
  onLogAudit: (event: string, category: any, status: 'success' | 'failure' | 'warning' | 'info', details: string) => void;
}

export const AdminPolicyDashboard: React.FC<AdminPolicyDashboardProps> = ({
  policy,
  onUpdatePolicy,
  providers,
  onUpdateProviders,
  auditLogs,
  onLogAudit
}) => {
  const [activeTab, setActiveTab] = useState<'policy' | 'providers' | 'audit'>('policy');
  const [simulateAge, setSimulateAge] = useState<number>(policy.maxEvidenceAgeSeconds);
  const [selectedLog, setSelectedLog] = useState<AuditLogEntry | null>(auditLogs[0] || null);

  // Policy Edit Handler
  const updatePolicyField = (field: keyof TenantEvidencePolicy, value: any) => {
    const updated = {
      ...policy,
      [field]: value,
      version: policy.version + 1,
      lastUpdated: new Date().toISOString(),
      lastUpdatedBy: 'admin-operator-99@company.com'
    };
    onUpdatePolicy(updated);
    onLogAudit(
      `Tenant Policy Updated`,
      'policy',
      'info',
      `Evidence validation policy version ${updated.version} created by admin-operator-99. Modified field "${String(field)}".`
    );
  };

  // Provider Health Toggle
  const toggleProviderHealth = (id: string) => {
    const updated = providers.map(p => {
      if (p.id === id) {
        const nextStatus = p.status === 'healthy' ? 'outage' : p.status === 'outage' ? 'degraded' : 'healthy';
        onLogAudit(
          `Provider Health Changed`,
          'policy',
          nextStatus === 'outage' ? 'failure' : 'success',
          `Identity provider "${p.name}" status updated to: ${nextStatus}.`
        );
        return { ...p, status: nextStatus as any };
      }
      return p;
    });
    onUpdateProviders(updated);
  };

  // Policy Impact Preview Calculator (Section 5.7)
  const calculateImpact = () => {
    let riskLevel: 'low' | 'medium' | 'high' = 'low';
    let warningMsg = '';
    let affectedPercentage = 0;

    if (policy.requireHardwareBacking && !policy.allowFederatedFace) {
      riskLevel = 'high';
      affectedPercentage = 68;
      warningMsg = 'High lockout risk! Requiring direct first-party hardware keys and blocking federated credentials will lock out mobile and remote workers lacking native infrared depth sensors.';
    } else if (policy.requireLiveness && !policy.allowFirstPartyFace) {
      riskLevel = 'medium';
      affectedPercentage = 35;
      warningMsg = 'Medium risk. Disabling direct enrollment while requiring liveness check forces all users onto upstream federated pathways. Ensure IDP supports strict AMR.';
    } else {
      riskLevel = 'low';
      warningMsg = 'Optimal coverage. Policy accommodates direct secure enclave capture, trusted enterprise IDPs, and offers WebAuthn security key fallbacks.';
    }

    return { riskLevel, warningMsg, affectedPercentage };
  };

  const impact = calculateImpact();

  return (
    <div id="admin-policy-dashboard" className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-left max-w-6xl mx-auto">
      
      {/* Top Section Tab Selectors */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between border-b border-gray-100 pb-4 mb-6 gap-4">
        <div>
          <h3 className="text-base font-bold text-gray-900 flex items-center gap-1.5">
            <Sliders className="w-5 h-5 text-indigo-600" /> Tenant Biometric & Evidence Control
          </h3>
          <p className="text-xs text-gray-500">Configure modality rules, trusted federation mappings, and audit verifier conformance.</p>
        </div>
        <div className="flex bg-gray-100 p-1 rounded-xl">
          <button
            type="button"
            onClick={() => setActiveTab('policy')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'policy' ? 'bg-white text-gray-900 shadow-xs' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Evidence Policy
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('providers')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'providers' ? 'bg-white text-gray-900 shadow-xs' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Trusted Providers ({providers.length})
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('audit')}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition ${
              activeTab === 'audit' ? 'bg-white text-gray-900 shadow-xs' : 'text-gray-500 hover:text-gray-900'
            }`}
          >
            Audit Trail Logs
          </button>
        </div>
      </div>

      {/* --- TAB 1: EVIDENCE POLICY CONFIGURATION --- */}
      {activeTab === 'policy' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Policy Inputs */}
          <div className="lg:col-span-2 space-y-5">
            <div className="bg-gray-50/50 p-5 rounded-xl border border-gray-100 space-y-4">
              <span className="text-[10px] uppercase font-bold text-indigo-600 tracking-wider font-mono">Modality Assurance Requirements</span>
              
              <div className="space-y-3 text-xs">
                {/* Allow First Party */}
                <div className="flex items-center justify-between py-1">
                  <div className="text-left">
                    <label className="font-semibold text-gray-900 block">Allow First-Party Face Authenticator</label>
                    <span className="text-gray-500 text-[11px]">Enables direct native capture enclaves inside verifier boundaries.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.allowFirstPartyFace}
                    onChange={(e) => updatePolicyField('allowFirstPartyFace', e.target.checked)}
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                </div>

                {/* Allow Federated */}
                <div className="flex items-center justify-between py-1 border-t border-gray-100 pt-3">
                  <div className="text-left">
                    <label className="font-semibold text-gray-900 block">Allow Federated Biometric Evidence</label>
                    <span className="text-gray-500 text-[11px]">Accept and parse AMR claims emitted by certified external Identity Providers.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.allowFederatedFace}
                    onChange={(e) => updatePolicyField('allowFederatedFace', e.target.checked)}
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                </div>

                {/* Require Liveness */}
                <div className="flex items-center justify-between py-1 border-t border-gray-100 pt-3">
                  <div className="text-left">
                    <label className="font-semibold text-gray-900 block">Enforce Liveness Verification (PAD)</label>
                    <span className="text-gray-500 text-[11px]">Requires challenge-response testing during verification. Rejects static files.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.requireLiveness}
                    onChange={(e) => updatePolicyField('requireLiveness', e.target.checked)}
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                </div>

                {/* Require Hardware Backing */}
                <div className="flex items-center justify-between py-1 border-t border-gray-100 pt-3">
                  <div className="text-left">
                    <label className="font-semibold text-gray-900 block">Enforce Hardware Backing</label>
                    <span className="text-gray-500 text-[11px]">Rejects verification signatures from generic webcams lacking infrared sensors.</span>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.requireHardwareBacking}
                    onChange={(e) => updatePolicyField('requireHardwareBacking', e.target.checked)}
                    className="w-4 h-4 text-indigo-600 border-gray-300 rounded focus:ring-indigo-500"
                  />
                </div>

                {/* Evidence Age Limit */}
                <div className="flex flex-col gap-1.5 border-t border-gray-100 pt-3">
                  <div className="text-left">
                    <label className="font-semibold text-gray-900 block">Max Evidence Freshness (Seconds)</label>
                    <span className="text-gray-500 text-[11px]">After this window, session assurance degrades and requires fresh step-up.</span>
                  </div>
                  <div className="flex items-center gap-3 mt-1.5">
                    <input
                      type="range"
                      min="60"
                      max="86400"
                      step="60"
                      value={policy.maxEvidenceAgeSeconds}
                      onChange={(e) => updatePolicyField('maxEvidenceAgeSeconds', Number(e.target.value))}
                      className="w-full h-1.5 bg-gray-200 rounded-lg appearance-none cursor-pointer text-indigo-600"
                    />
                    <span className="text-xs font-mono font-semibold text-gray-900 shrink-0">
                      {Math.floor(policy.maxEvidenceAgeSeconds / 60)} min ({policy.maxEvidenceAgeSeconds}s)
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Policy Impact Preview Panel (Section 5.7) */}
          <div className="lg:col-span-1 space-y-4">
            <div className="border border-gray-200 rounded-xl p-4 bg-white space-y-4">
              <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider block">Policy Publication Preview</span>
              
              <div className="space-y-1.5 text-xs text-gray-700">
                <div className="flex justify-between font-mono text-[10px]">
                  <span>Active Policy Version:</span>
                  <span className="font-bold">v{policy.version}</span>
                </div>
                <div className="flex justify-between font-mono text-[10px]">
                  <span>Modified Date:</span>
                  <span>{new Date(policy.lastUpdated).toLocaleDateString()}</span>
                </div>
                <div className="flex justify-between font-mono text-[10px] truncate">
                  <span>Author:</span>
                  <span className="text-gray-500 shrink-0">{policy.lastUpdatedBy.split('@')[0]}</span>
                </div>
              </div>

              {/* Impact Level Badge */}
              <div className={`p-3.5 rounded-xl border flex flex-col gap-1.5 ${
                impact.riskLevel === 'high' ? 'bg-red-50 border-red-200 text-red-900' :
                impact.riskLevel === 'medium' ? 'bg-amber-50 border-amber-200 text-amber-900' :
                'bg-green-50 border-green-200 text-green-900'
              }`}>
                <div className="flex items-center gap-2">
                  <AlertTriangle className={`w-4 h-4 ${impact.riskLevel === 'high' ? 'text-red-600' : impact.riskLevel === 'medium' ? 'text-amber-600' : 'text-green-600'}`} />
                  <span className="font-bold text-xs uppercase">LOCKOUT RISK ASSESSMENT: {impact.riskLevel.toUpperCase()}</span>
                </div>
                <p className="text-[11px] leading-relaxed opacity-95">{impact.warningMsg}</p>
                {impact.riskLevel !== 'low' && (
                  <div className="mt-2 text-[10px] font-semibold text-gray-600 bg-white/70 px-2 py-1 rounded">
                    Estimated Affected Users: <span className="font-bold text-gray-900">{impact.affectedPercentage}%</span>
                  </div>
                )}
              </div>

              {/* Rule constraints */}
              <div className="bg-gray-50 rounded-xl p-3 text-[11px] text-gray-500 space-y-1">
                <span className="font-semibold text-gray-700 block">Allowed Fallback Methods:</span>
                <ul className="list-disc pl-4 space-y-0.5">
                  <li>WebAuthn Passkey Token</li>
                  <li>YubiKey FIDO2 Hardware Key</li>
                  <li>Temporary Recovery Token</li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* --- TAB 2: TRUSTED PROVIDERS CONFIGURATION --- */}
      {activeTab === 'providers' && (
        <div className="space-y-6">
          <div className="bg-indigo-50/40 border border-indigo-100 rounded-xl p-4 text-xs text-indigo-900">
            <h4 className="font-bold flex items-center gap-1.5 mb-1">
              <ShieldCheck className="w-4 h-4 text-indigo-600" /> Biometric Identity Federation Authority
            </h4>
            <p className="text-indigo-800 text-[11px] leading-relaxed">
              We process external assertions only from identity providers matching an approved cryptographic Trust Profile. Claims are mapped securely, and non-conforming parameters (e.g. untrusted biometric assertions) are automatically demoted to general authentication.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {providers.map((p) => (
              <div key={p.id} className="border border-gray-200 rounded-xl p-4 bg-white flex flex-col justify-between hover:shadow-xs transition">
                <div>
                  {/* Provider Header */}
                  <div className="flex items-center justify-between border-b border-gray-50 pb-2 mb-3">
                    <span className="text-xs font-bold text-gray-900 truncate max-w-[150px]">{p.name}</span>
                    {/* Health indicator */}
                    <span className={`text-[9px] font-mono font-bold px-2 py-0.5 rounded uppercase ${
                      p.status === 'healthy' ? 'bg-green-100 text-green-800' :
                      p.status === 'degraded' ? 'bg-amber-100 text-amber-800' :
                      'bg-red-100 text-red-800 animate-pulse'
                    }`}>
                      {p.status}
                    </span>
                  </div>

                  <dl className="space-y-2 text-[10px] text-gray-600">
                    <div>
                      <span className="font-medium text-gray-400 block">Trust Rating Profile</span>
                      <span className="font-semibold text-gray-900 font-mono uppercase">{p.trustProfile.replace('_', ' ')}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-400 block">Authorized Mappings</span>
                      <span className="font-semibold text-indigo-600 font-mono">{p.allowedAmrMappings.join(', ').toUpperCase()}</span>
                    </div>
                    <div>
                      <span className="font-medium text-gray-400 block">Client ID Reference</span>
                      <span className="font-mono text-gray-800 break-all">{p.clientId}</span>
                    </div>
                  </dl>
                </div>

                {/* Health Simulation Trigger (Section 4 & 6) */}
                <div className="border-t border-gray-100 pt-3 mt-4 flex items-center justify-between text-xs">
                  <span className="text-[10px] text-gray-400 font-medium">Outage Mock:</span>
                  <button
                    type="button"
                    onClick={() => toggleProviderHealth(p.id)}
                    className="flex items-center gap-1.5 px-2 py-1 border border-gray-200 hover:bg-gray-50 rounded text-[11px] font-semibold text-gray-700 transition"
                  >
                    <Activity className="w-3.5 h-3.5 text-gray-500" />
                    Toggle Health State
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* --- TAB 3: AUDIT EVIDENCE TIMELINE LOGS --- */}
      {activeTab === 'audit' && (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Table of logs */}
          <div className="lg:col-span-2 border border-gray-200 rounded-xl overflow-hidden bg-white">
            <div className="bg-gray-50 p-3 border-b border-gray-200 flex justify-between items-center text-xs text-gray-600">
              <span className="font-bold">Security Evidence Logs ({auditLogs.length})</span>
              <span className="font-mono text-[10px]">Redacted telemetric records only</span>
            </div>

            <div className="overflow-y-auto max-h-[350px] divide-y divide-gray-100">
              {auditLogs.map((log) => (
                <button
                  type="button"
                  key={log.id}
                  onClick={() => setSelectedLog(log)}
                  className={`w-full text-left p-3 flex items-start gap-3 text-xs transition ${
                    selectedLog?.id === log.id ? 'bg-indigo-50/40' : 'hover:bg-gray-50/50'
                  }`}
                >
                  <span className={`w-2.5 h-2.5 rounded-full shrink-0 mt-1 ${
                    log.status === 'success' ? 'bg-green-500' :
                    log.status === 'failure' ? 'bg-red-500' :
                    log.status === 'warning' ? 'bg-amber-500' : 'bg-blue-500'
                  }`} />
                  
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center justify-between text-[11px] font-mono text-gray-400 mb-0.5">
                      <span className="text-gray-900 font-bold">{log.event}</span>
                      <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                    </div>
                    <p className="text-gray-600 truncate">{log.details}</p>
                    {log.provenance && (
                      <span className="inline-block bg-gray-100 text-gray-500 font-mono text-[9px] px-1.5 py-0.2 rounded mt-1">
                        Provenance: {log.provenance}
                      </span>
                    )}
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Selected log inspector (Section 4 & 5.6) */}
          <div className="lg:col-span-1 border border-gray-200 rounded-xl p-4 bg-white space-y-4">
            <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider block">Evidence Claim Inspector</span>
            
            {selectedLog ? (
              <div className="space-y-3.5 text-xs">
                <div>
                  <span className="text-gray-400 font-medium block">Audit ID</span>
                  <span className="font-semibold text-gray-900 font-mono">{selectedLog.id}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Timestamp</span>
                  <span className="font-semibold text-gray-900 font-mono">{new Date(selectedLog.timestamp).toLocaleString()}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Actor Account</span>
                  <span className="font-semibold text-indigo-600 font-mono truncate block">{selectedLog.actor}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Telemetry Context Details</span>
                  <p className="text-gray-600 text-[11px] leading-relaxed mt-1">{selectedLog.details}</p>
                </div>

                {selectedLog.provenance && (
                  <div className="bg-gray-50 border border-gray-200 rounded-lg p-2.5 font-mono text-[10px] space-y-1">
                    <span className="font-semibold text-gray-700 block text-[9px] uppercase tracking-wider">Provenance Summary</span>
                    <div>Modality AMR: {selectedLog.amrEvidence || 'None'}</div>
                    <div>Provenance: {selectedLog.provenance}</div>
                    <div>Device: {selectedLog.device || 'N/A'}</div>
                    <div>IP Context: {selectedLog.ip || 'N/A'}</div>
                  </div>
                )}
                
                <div className="bg-amber-50 text-amber-900 text-[10px] p-2.5 rounded-lg border border-amber-200">
                  <span className="font-bold block">Conformant Audit Mandate:</span>
                  Raw camera frame media buffers are purged automatically from device transient memory on execution, leaving only this verified schema log metadata.
                </div>
              </div>
            ) : (
              <p className="text-center text-gray-400 text-xs">Select a log entry from the timeline list to inspect full audit details.</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
