/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { FaceAuthenticator, DeletionJobStatus } from '../types';
import { KeyRound, Shield, AlertTriangle, ShieldCheck, Trash2, PauseCircle, PlayCircle, Eye, RefreshCw, CheckCircle, Info, FileX } from 'lucide-react';

interface AccountDashboardProps {
  authenticators: FaceAuthenticator[];
  onUpdateAuthenticators: (updated: FaceAuthenticator[]) => void;
  onInitiateRetrain: (id: string) => void;
  onLogAudit: (event: string, category: 'lifecycle' | 'consent', status: 'success' | 'failure' | 'warning', details: string) => void;
}

export const AccountDashboard: React.FC<AccountDashboardProps> = ({
  authenticators,
  onUpdateAuthenticators,
  onInitiateRetrain,
  onLogAudit
}) => {
  const [selectedAuthId, setSelectedAuthId] = useState<string | null>(authenticators[0]?.id || null);
  const [deletingId, setDeletingId] = useState<string | null>(null);

  const selectedAuth = authenticators.find(a => a.id === selectedAuthId);

  // Toggle Suspend / Resume
  const toggleSuspend = (id: string) => {
    const updated = authenticators.map(auth => {
      if (auth.id === id) {
        const nextStatus = auth.status === 'suspended' ? 'active' : 'suspended';
        onLogAudit(
          `Authenticator Status Changed`,
          'lifecycle',
          nextStatus === 'suspended' ? 'warning' : 'success',
          `Face Authenticator "${auth.label}" status updated to: ${nextStatus}.`
        );
        return { ...auth, status: nextStatus };
      }
      return auth;
    });
    onUpdateAuthenticators(updated);
  };

  // Permanent Revocation
  const revokeAuthenticator = (id: string) => {
    const updated = authenticators.map(auth => {
      if (auth.id === id) {
        onLogAudit(
          `Authenticator Revoked`,
          'lifecycle',
          'warning',
          `Face Authenticator "${auth.label}" was permanently revoked.`
        );
        return { ...auth, status: 'revoked' as const };
      }
      return auth;
    });
    onUpdateAuthenticators(updated);
  };

  // Initiate Biometric Template Deletion Request (Section 5.3 & 6)
  const triggerTemplateDeletion = (id: string) => {
    // Before actual deletion, transition state to pending
    const updated = authenticators.map(auth => {
      if (auth.id === id) {
        const deletionJobId = `job-del-${Math.floor(Math.random() * 90000) + 10000}`;
        onLogAudit(
          `Template Deletion Requested`,
          'lifecycle',
          'warning',
          `Asynchronous template erasure initialized for ID: ${auth.id}. Job Reference: ${deletionJobId}.`
        );
        return { 
          ...auth, 
          deletionStatus: 'pending' as DeletionJobStatus,
          deletionJobId,
          deletionLogs: [
            `[${new Date().toISOString()}] Job scheduled on isolated verifier core.`,
            `[${new Date().toISOString()}] Removing keys from enclave memory partition.`
          ]
        };
      }
      return auth;
    });
    onUpdateAuthenticators(updated);
  };

  // Simulate progress of the asynchronous Deletion job
  const simulateDeletionProgress = (id: string, outcome: 'completed' | 'failed') => {
    const updated = authenticators.map(auth => {
      if (auth.id === id) {
        const logTime = new Date().toISOString();
        const nextLogs = [
          ...(auth.deletionLogs || []),
          outcome === 'completed'
            ? `[${logTime}] Permanent cryptographic erasure complete. Cryptocertificate signed by enclave.`
            : `[${logTime}] Deletion failed: Partition locked due to concurrent re-enrollment block.`
        ];
        
        onLogAudit(
          outcome === 'completed' ? `Template Deletion Completed` : `Template Deletion Failed`,
          'lifecycle',
          outcome === 'completed' ? 'success' : 'failure',
          outcome === 'completed' 
            ? `Template completely scrubbed for ID: ${auth.id}.`
            : `Deletion failed for ID: ${auth.id}. Escalated to manual verification.`
        );

        return { 
          ...auth, 
          deletionStatus: outcome as DeletionJobStatus,
          status: outcome === 'completed' ? 'revoked' as const : auth.status,
          deletionLogs: nextLogs
        };
      }
      return auth;
    });
    onUpdateAuthenticators(updated);
  };

  return (
    <div id="account-biometrics-dashboard" className="grid grid-cols-1 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
      
      {/* Left Column: Registered Authenticators List */}
      <div className="lg:col-span-1 bg-white border border-gray-200 rounded-2xl p-5 shadow-sm">
        <div className="flex items-center gap-2 mb-4 border-b border-gray-100 pb-3">
          <KeyRound className="w-5 h-5 text-indigo-600" />
          <h3 className="font-bold text-gray-900 text-sm">Face Authenticators</h3>
        </div>

        <div className="space-y-3">
          {authenticators.map((auth) => (
            <button
              type="button"
              key={auth.id}
              onClick={() => setSelectedAuthId(auth.id)}
              className={`w-full text-left p-3.5 rounded-xl border transition flex flex-col gap-1.5 ${
                selectedAuthId === auth.id
                  ? 'border-indigo-600 bg-indigo-50/40 shadow-sm'
                  : 'border-gray-200 hover:bg-gray-50/70'
              }`}
            >
              <div className="flex items-center justify-between">
                <span className="font-semibold text-xs text-gray-900 truncate max-w-[150px]">
                  {auth.label}
                </span>
                
                {/* Status badges */}
                <span className={`text-[9px] font-bold px-2 py-0.5 rounded uppercase ${
                  auth.status === 'active' ? 'bg-green-100 text-green-800' :
                  auth.status === 'suspended' ? 'bg-amber-100 text-amber-800' :
                  auth.status === 'replacement_required' ? 'bg-indigo-100 text-indigo-800' :
                  'bg-red-100 text-red-800'
                }`}>
                  {auth.status.replace('_', ' ')}
                </span>
              </div>

              <div className="flex justify-between items-center text-[10px] text-gray-400 font-mono">
                <span>Used: {new Date(auth.lastUsedDate).toLocaleDateString()}</span>
                <span>HW: {auth.deviceProjection.includes('MacBook') || auth.deviceProjection.includes('Pixel') ? 'Attested' : 'Lax'}</span>
              </div>

              {/* Pending deletion flash bar */}
              {auth.deletionStatus === 'pending' && (
                <div className="w-full bg-amber-100 text-amber-900 text-[9px] px-1.5 py-0.5 rounded font-bold animate-pulse mt-1 flex items-center gap-1">
                  <RefreshCw className="w-2.5 h-2.5 animate-spin" /> Deletion Job Pending
                </div>
              )}
            </button>
          ))}
        </div>

        <div className="bg-gray-50 border border-gray-100 rounded-xl p-3.5 mt-5 text-xs text-left">
          <h4 className="font-bold text-gray-800 flex items-center gap-1.5 mb-1">
            <Shield className="w-4 h-4 text-indigo-600" /> Recovery Readiness
          </h4>
          <p className="text-gray-600 text-[11px] leading-relaxed">
            Biometric recovery mechanisms are active. If your device camera is damaged, you will be prompted for your security key fallback without weakening security posture.
          </p>
        </div>
      </div>

      {/* Right 2 Columns: Selected Authenticator Detail & Management Action Center */}
      <div className="lg:col-span-2 space-y-6">
        {selectedAuth ? (
          <>
            {/* Authenticator Detail Card */}
            <div id={`detail-card-${selectedAuth.id}`} className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-left">
              <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between border-b border-gray-100 pb-4 mb-4 gap-3">
                <div>
                  <span className="text-[10px] font-mono uppercase font-bold text-gray-400">Authenticator Profile details</span>
                  <h3 className="text-lg font-bold text-gray-900 tracking-tight">{selectedAuth.label}</h3>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => onInitiateRetrain(selectedAuth.id)}
                    className="flex items-center gap-1 px-3 py-1.5 border border-indigo-200 text-indigo-700 bg-indigo-50/50 hover:bg-indigo-50 rounded-lg text-xs font-semibold transition"
                  >
                    <RefreshCw className="w-3.5 h-3.5" /> Retrain/Replace Template
                  </button>
                </div>
              </div>

              {/* Specifications List */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-700 bg-gray-50/50 p-4 rounded-xl border border-gray-100 mb-5">
                <div>
                  <span className="text-gray-400 font-medium block">Verifier Engine Profile</span>
                  <span className="font-semibold text-gray-900 font-mono">{selectedAuth.verifierProfile}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Consent Version Binding</span>
                  <span className="font-semibold text-gray-900 font-mono">{selectedAuth.consentVersion} ({new Date(selectedAuth.consentDate).toLocaleDateString()})</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Device Hardware Projection</span>
                  <span className="font-semibold text-gray-900 font-mono">{selectedAuth.deviceProjection}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Active Recovery Posture</span>
                  <span className="font-semibold text-gray-900 font-mono text-indigo-600">{selectedAuth.recoveryMethod}</span>
                </div>
                <div className="md:col-span-2 pt-2 border-t border-gray-100 text-[11px] text-gray-500">
                  <strong className="text-gray-700 block mb-0.5">Template Retention Policy:</strong>
                  {selectedAuth.retentionPolicy}
                </div>
              </div>

              {/* Warning box if replacement required */}
              {selectedAuth.status === 'replacement_required' && (
                <div className="bg-amber-50 border border-amber-200 text-amber-900 p-4 rounded-xl text-xs mb-5 flex gap-2">
                  <AlertTriangle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold">Biometric Profile Update Required:</span> This face template is using a legacy signature verifier profile. To satisfy current tenant security policies, please retrain the authenticator by initiating a new secure biometric capture ceremony.
                  </div>
                </div>
              )}

              {/* Lifecycle Controls */}
              <div className="border-t border-gray-100 pt-5 space-y-4">
                <h4 className="text-xs font-bold text-gray-400 uppercase tracking-wider mb-2">Authenticator Lifecycle Management</h4>
                <div className="flex flex-wrap gap-2.5">
                  
                  {/* Suspend / Resume button */}
                  {selectedAuth.status !== 'revoked' && (
                    <button
                      type="button"
                      onClick={() => toggleSuspend(selectedAuth.id)}
                      className="flex items-center gap-1.5 px-3 py-2 border border-gray-200 hover:border-gray-300 rounded-lg text-xs font-semibold text-gray-700 bg-white hover:bg-gray-50 transition"
                    >
                      {selectedAuth.status === 'suspended' ? (
                        <>
                          <PlayCircle className="w-4 h-4 text-green-600" /> Resume Authenticator
                        </>
                      ) : (
                        <>
                          <PauseCircle className="w-4 h-4 text-amber-600" /> Suspend Authenticator
                        </>
                      )}
                    </button>
                  )}

                  {/* Revoke button */}
                  {selectedAuth.status !== 'revoked' && (
                    <button
                      type="button"
                      onClick={() => revokeAuthenticator(selectedAuth.id)}
                      className="flex items-center gap-1.5 px-3 py-2 border border-red-200 text-red-700 hover:bg-red-50 rounded-lg text-xs font-semibold bg-white transition"
                    >
                      <Shield className="w-4 h-4" /> Permanent Revocation
                    </button>
                  )}

                  {/* Deletion job button */}
                  {(!selectedAuth.deletionStatus || selectedAuth.deletionStatus === 'none') ? (
                    <button
                      type="button"
                      onClick={() => triggerTemplateDeletion(selectedAuth.id)}
                      className="flex items-center gap-1.5 px-3 py-2 border border-dashed border-red-300 text-red-600 hover:bg-red-50 rounded-lg text-xs font-semibold bg-white transition ml-auto"
                    >
                      <Trash2 className="w-4 h-4" /> Request Biometric Deletion
                    </button>
                  ) : null}
                </div>

                <p className="text-[10px] text-gray-400">
                  * Suspension stops active logins temporarily but retains recovery configuration. Revocation disables the device profile permanently.
                </p>
              </div>
            </div>

            {/* Biometric Template Deletion Status Box (Section 4 & 5.3) */}
            {selectedAuth.deletionStatus && selectedAuth.deletionStatus !== 'none' && (
              <div id={`deletion-tracker-${selectedAuth.id}`} className="bg-white border border-gray-200 rounded-2xl p-5 shadow-sm text-left">
                <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-3">
                  <h4 className="text-sm font-bold text-gray-900 flex items-center gap-1.5">
                    <FileX className="w-4 h-4 text-amber-600" /> Biometric Template Deletion Tracker
                  </h4>
                  <span className={`text-[10px] font-mono font-bold px-2.5 py-0.5 rounded ${
                    selectedAuth.deletionStatus === 'pending' ? 'bg-amber-100 text-amber-800 animate-pulse' :
                    selectedAuth.deletionStatus === 'completed' ? 'bg-green-100 text-green-800' :
                    'bg-red-100 text-red-800'
                  }`}>
                    STATUS: {selectedAuth.deletionStatus.toUpperCase()}
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs mb-4">
                  <div>
                    <span className="text-gray-400 font-medium block">Async Deletion Job ID</span>
                    <span className="font-semibold text-gray-900 font-mono">{selectedAuth.deletionJobId || 'Not Assigned'}</span>
                  </div>
                  <div>
                    <span className="text-gray-400 font-medium block">Audit Proof Reference</span>
                    <span className="font-semibold text-indigo-600 font-mono">aud-del-verify-09c31</span>
                  </div>
                </div>

                {/* Audit Logs inside Deletion tracking */}
                <div className="bg-gray-950 text-gray-300 p-3 rounded-xl font-mono text-[10px] space-y-1 max-h-[100px] overflow-y-auto mb-4">
                  {selectedAuth.deletionLogs?.map((log, i) => (
                    <div key={i}>{log}</div>
                  ))}
                </div>

                {/* Simulation Control over Async Job */}
                {selectedAuth.deletionStatus === 'pending' && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 flex items-center justify-between text-xs text-amber-950">
                    <div className="flex items-center gap-2">
                      <RefreshCw className="w-4 h-4 text-amber-600 animate-spin" />
                      <span>Simulate async verifier response:</span>
                    </div>
                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => simulateDeletionProgress(selectedAuth.id, 'completed')}
                        className="px-2.5 py-1 bg-green-600 text-white font-semibold rounded text-[10px] hover:bg-green-700"
                      >
                        Succeed Erasure
                      </button>
                      <button
                        type="button"
                        onClick={() => simulateDeletionProgress(selectedAuth.id, 'failed')}
                        className="px-2.5 py-1 bg-red-600 text-white font-semibold rounded text-[10px] hover:bg-red-700"
                      >
                        Fail Erasure
                      </button>
                    </div>
                  </div>
                )}

                {selectedAuth.deletionStatus === 'completed' && (
                  <div className="bg-green-50 border border-green-200 text-green-900 p-3 rounded-xl text-xs flex gap-2">
                    <CheckCircle className="w-4 h-4 text-green-600 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold block">Biometric Erasure Confirmed</span>
                      The server-enclave verifier has successfully shredded all physical neural templates matching this authenticator and emitted cryptographic proof certificate <span className="font-mono text-green-700">del-proof-77112</span>. No active face matching models exist for this channel.
                    </div>
                  </div>
                )}

                {selectedAuth.deletionStatus === 'failed' && (
                  <div className="bg-red-50 border border-red-200 text-red-900 p-3 rounded-xl text-xs flex gap-2 items-start">
                    <AlertTriangle className="w-4 h-4 text-red-600 shrink-0 mt-0.5" />
                    <div className="flex-1">
                      <span className="font-bold block">Erasure Job Failed</span>
                      Enclave failed to wipe memory blocks due to verification state-lock.
                      <div className="mt-2.5 flex gap-2">
                        <button
                          type="button"
                          onClick={() => triggerTemplateDeletion(selectedAuth.id)}
                          className="px-2 py-1 bg-red-600 hover:bg-red-700 text-white rounded text-[10px] font-semibold"
                        >
                          Retry Erasure Job
                        </button>
                        <button
                          type="button"
                          onClick={() => {
                            simulateDeletionProgress(selectedAuth.id, 'completed');
                          }}
                          className="px-2 py-1 border border-red-300 text-red-700 rounded text-[10px] hover:bg-red-100 font-semibold"
                        >
                          Escalate to Manual Verification
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            )}
          </>
        ) : (
          <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm text-center text-gray-500">
            <Info className="w-8 h-8 text-gray-400 mx-auto mb-2" />
            No face authenticators registered or active on this account profile.
          </div>
        )}
      </div>
    </div>
  );
};
