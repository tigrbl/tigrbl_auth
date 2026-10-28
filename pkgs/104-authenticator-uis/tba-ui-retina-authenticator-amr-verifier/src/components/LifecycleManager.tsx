import React, { useState } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { KeyRound, ShieldAlert, Trash2, RotateCcw, Ban, CheckCircle, Clock, FileLock2, Lock } from 'lucide-react';
import { RetinaEnrollment, DeletionJob, AuditLog, BiometricStatus } from '../types';

interface LifecycleManagerProps {
  enrollment: RetinaEnrollment | null;
  onEnrollmentStatusChange: (newStatus: BiometricStatus) => void;
  onTriggerReEnrollment: () => void;
  onWithdrawConsent: () => void;
  onAddAlternativeFactor: () => void;
  hasOtherFactors: boolean;
  auditLogs: AuditLog[];
}

export default function LifecycleManager({
  enrollment,
  onEnrollmentStatusChange,
  onTriggerReEnrollment,
  onWithdrawConsent,
  onAddAlternativeFactor,
  hasOtherFactors,
  auditLogs,
}: LifecycleManagerProps) {
  const [showDeletionConfirm, setShowDeletionConfirm] = useState(false);
  const [deletionStatus, setDeletionStatus] = useState<'none' | 'pending' | 'completed' | 'failed'>('none');
  const [deletionJob, setDeletionJob] = useState<DeletionJob | null>(null);
  const [authVerifyPassword, setAuthVerifyPassword] = useState('');
  const [authError, setAuthError] = useState('');
  const [isDeleting, setIsDeleting] = useState(false);

  const handleStatusToggle = (action: 'suspend' | 'activate') => {
    if (!enrollment) return;
    if (action === 'suspend') {
      onEnrollmentStatusChange('suspended');
    } else {
      onEnrollmentStatusChange('active');
    }
  };

  const handleRevocation = () => {
    if (window.confirm('Are you absolutely sure you want to revoke this retina authenticator? This will immediately lock access and render existing device templates useless.')) {
      onEnrollmentStatusChange('revoked');
    }
  };

  const handleRequestDeletion = () => {
    if (!enrollment) return;
    if (!hasOtherFactors) {
      setAuthError('CRITICAL LOCKOUT WARNING: This is your only remaining high-assurance authentication factor. Deletion is blocked until you register an alternative key (FIDO2 or TOTP).');
      return;
    }
    setAuthError('');
    setShowDeletionConfirm(true);
  };

  const executeTemplateDeletion = (e: React.FormEvent) => {
    e.preventDefault();
    if (authVerifyPassword !== 'security123') {
      setAuthError('Invalid administrator or user session verification password (enter "security123" to authorize)');
      return;
    }

    setAuthError('');
    setIsDeleting(true);
    setDeletionStatus('pending');

    const job: DeletionJob = {
      id: `job_${Math.random().toString(36).substr(2, 9)}`,
      templateId: enrollment?.id || 'unknown_id',
      status: 'pending',
      requestedAt: new Date().toISOString(),
      completedAt: null,
      auditReference: `AUDIT-DEL-${Math.random().toString(36).substr(2, 6).toUpperCase()}`,
      evidenceRedacted: true,
    };
    setDeletionJob(job);

    // Simulate specialized verifier template shredding job (takes 2.5 seconds)
    setTimeout(() => {
      setDeletionStatus('completed');
      setDeletionJob(prev => prev ? {
        ...prev,
        status: 'completed',
        completedAt: new Date().toISOString(),
      } : null);
      setIsDeleting(false);
      setShowDeletionConfirm(false);
      onWithdrawConsent(); // Clear the active enrollment state on success
    }, 2500);
  };

  // Filter audit logs pertaining to this specific enrollment subject
  const userLogs = auditLogs.filter(log => log.subjectId === 'SUBJ-USR-773');

  return (
    <div id="lifecycle-container" className="max-w-4xl mx-auto space-y-6">
      <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
        
        {/* Left Column: Active Authenticator Profile */}
        <div className="md:col-span-7 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div className="flex items-center justify-between border-b border-slate-800 pb-4">
            <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider">
              Biometric Authenticator Detail
            </h3>
            {enrollment ? (
              <span className={`text-[10px] font-mono font-bold uppercase px-2.5 py-0.5 rounded border ${
                enrollment.status === 'active' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                enrollment.status === 'suspended' ? 'bg-amber-500/10 text-amber-400 border-amber-500/20' :
                'bg-red-500/10 text-red-400 border-red-500/20'
              }`}>
                {enrollment.status.toUpperCase()}
              </span>
            ) : (
              <span className="text-[10px] font-mono text-slate-500 border border-slate-800 px-2 py-0.5 rounded">
                NOT ENROLLED
              </span>
            )}
          </div>

          {enrollment ? (
            <div className="space-y-6">
              {/* Authenticator Profile Details Grid */}
              <div className="grid grid-cols-2 gap-4 text-xs font-mono">
                <div className="p-3 bg-slate-950/40 rounded-lg border border-slate-800">
                  <span className="text-slate-500 block">ENROLLED ON STATION</span>
                  <span className="text-slate-300 font-semibold">RP-H100-B3</span>
                </div>
                <div className="p-3 bg-slate-950/40 rounded-lg border border-slate-800">
                  <span className="text-slate-500 block">CONSENT VERSION</span>
                  <span className="text-slate-300 font-semibold">v{enrollment.consentVersion}</span>
                </div>
                <div className="p-3 bg-slate-950/40 rounded-lg border border-slate-800">
                  <span className="text-slate-500 block">ACTIVATED DATE</span>
                  <span className="text-slate-300 font-semibold">{new Date(enrollment.enrolledAt).toLocaleDateString()}</span>
                </div>
                <div className="p-3 bg-slate-950/40 rounded-lg border border-slate-800">
                  <span className="text-slate-500 block">BIOMETRIC EXPIRED</span>
                  <span className="text-slate-400 font-semibold">{new Date(enrollment.expiresAt).toLocaleDateString()}</span>
                </div>
                <div className="col-span-2 p-3 bg-slate-950/40 rounded-lg border border-slate-800">
                  <div className="flex justify-between items-center">
                    <div>
                      <span className="text-slate-500 block">LAST VERIFIED TRANSACTION</span>
                      <span className="text-slate-300 font-semibold">{new Date(enrollment.lastUsedAt).toLocaleString()}</span>
                    </div>
                    <span className="text-[10px] bg-cyan-500/10 text-cyan-400 border border-cyan-500/20 px-2 py-0.5 rounded">
                      MATCH: 99.4%
                    </span>
                  </div>
                </div>
              </div>

              {/* Status Management Actions */}
              <div className="pt-4 border-t border-slate-800 space-y-3">
                <h4 className="text-xs font-mono uppercase text-slate-400 tracking-wider">Device Level Operations</h4>
                
                <div className="flex flex-wrap gap-2.5">
                  {enrollment.status === 'active' ? (
                    <button
                      id="btn-lifecycle-suspend"
                      onClick={() => handleStatusToggle('suspend')}
                      className="px-3.5 py-1.5 rounded bg-slate-950 hover:bg-slate-800 border border-slate-800 text-amber-400 font-mono text-xs flex items-center gap-1.5 cursor-pointer"
                    >
                      <Ban className="w-3.5 h-3.5" />
                      Suspend Use
                    </button>
                  ) : enrollment.status === 'suspended' ? (
                    <button
                      id="btn-lifecycle-activate"
                      onClick={() => handleStatusToggle('activate')}
                      className="px-3.5 py-1.5 rounded bg-emerald-500/10 hover:bg-emerald-500/20 border border-emerald-500/20 text-emerald-400 font-mono text-xs flex items-center gap-1.5 cursor-pointer"
                    >
                      <CheckCircle className="w-3.5 h-3.5" />
                      Activate Credentials
                    </button>
                  ) : null}

                  <button
                    id="btn-lifecycle-re-enroll"
                    onClick={onTriggerReEnrollment}
                    className="px-3.5 py-1.5 rounded bg-slate-950 hover:bg-slate-800 border border-slate-800 text-cyan-400 font-mono text-xs flex items-center gap-1.5 cursor-pointer"
                  >
                    <RotateCcw className="w-3.5 h-3.5" />
                    Replace / Retrain
                  </button>

                  <button
                    id="btn-lifecycle-revoke"
                    onClick={handleRevocation}
                    className="px-3.5 py-1.5 rounded bg-red-950/20 hover:bg-red-950/40 border border-red-900/40 text-red-400 font-mono text-xs flex items-center gap-1.5 cursor-pointer"
                  >
                    <ShieldAlert className="w-3.5 h-3.5" />
                    Revoke immediately
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <div className="flex flex-col items-center justify-center py-10 text-center space-y-4">
              <div className="w-12 h-12 rounded-full bg-slate-950 border border-slate-800 flex items-center justify-center text-slate-500">
                <KeyRound className="w-6 h-6" />
              </div>
              <div className="max-w-xs text-xs space-y-1">
                <p className="font-semibold text-slate-300">No Retinal Template Enrolled</p>
                <p className="text-slate-500 font-sans leading-normal">
                  You have not registered biometric retina credentials. Complete the enrollment wizard to get started.
                </p>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Template Deletion Tracker & Last Factor Safety Lock */}
        <div className="md:col-span-5 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
          <div className="border-b border-slate-800 pb-4 flex items-center justify-between">
            <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider">
              Privacy Request & Erasure
            </h3>
            <Trash2 className="w-4 h-4 text-slate-400" />
          </div>

          <div className="text-xs space-y-4">
            <p className="text-slate-400 leading-relaxed font-sans">
              Under compliance guidelines, you possess the absolute right to demand the destruction of 
              your biometric templates. Once authorized, a verifier job will shred all stored reference patterns.
            </p>

            {enrollment && deletionStatus === 'none' && !showDeletionConfirm && (
              <button
                id="btn-lifecycle-request-delete"
                onClick={handleRequestDeletion}
                className="w-full py-2 bg-red-950/20 hover:bg-red-950/40 border border-red-900/40 text-red-400 font-mono text-xs font-bold rounded uppercase tracking-wider transition-colors flex items-center justify-center gap-2 cursor-pointer"
              >
                <Trash2 className="w-4 h-4" />
                Request Biometric Template Deletion
              </button>
            )}

            {/* Locked Alternative Factor Check */}
            {authError && (
              <div className="bg-red-950/20 border border-red-900/50 rounded-lg p-3.5 space-y-2 text-red-400 font-mono">
                <div className="flex items-start gap-2 text-xs">
                  <Lock className="w-4 h-4 mt-0.5 shrink-0 text-red-400 animate-pulse" />
                  <div>
                    <p className="font-bold uppercase tracking-wider">Safety Lockout Warning</p>
                    <p className="text-slate-400 font-sans mt-1 leading-normal text-[11px]">{authError}</p>
                  </div>
                </div>
                {!hasOtherFactors && (
                  <button
                    id="btn-add-factor-recovery"
                    onClick={onAddAlternativeFactor}
                    className="w-full mt-2 py-1.5 bg-cyan-500/10 hover:bg-cyan-500/20 border border-cyan-500/20 text-cyan-400 text-[10px] font-mono rounded uppercase tracking-wider transition-colors cursor-pointer"
                  >
                    Register Alternative Factor Now
                  </button>
                )}
              </div>
            )}

            {/* Interactive password re-auth confirm panel */}
            <AnimatePresence>
              {showDeletionConfirm && (
                <motion.form
                  id="form-confirm-deletion"
                  onSubmit={executeTemplateDeletion}
                  initial={{ height: 0, opacity: 0 }}
                  animate={{ height: 'auto', opacity: 1 }}
                  exit={{ height: 0, opacity: 0 }}
                  className="bg-slate-950 border border-slate-800 rounded-xl p-4 space-y-4 overflow-hidden"
                >
                  <p className="text-[11px] text-amber-400 font-mono uppercase font-bold tracking-wider">
                    Confirm Biometric Deletion ID Check
                  </p>
                  <div className="space-y-1.5">
                    <label className="text-[10px] text-slate-500 font-mono uppercase">
                      Confirm Session Authorization (Enter "security123"):
                    </label>
                    <input
                      id="input-delete-reauth"
                      type="password"
                      value={authVerifyPassword}
                      onChange={(e) => setAuthVerifyPassword(e.target.value)}
                      placeholder="••••••••••••"
                      className="w-full bg-slate-900 text-slate-100 border border-slate-800 rounded px-2.5 py-1.5 text-xs font-mono focus:border-red-500 focus:outline-none"
                    />
                  </div>
                  <div className="flex gap-2">
                    <button
                      id="btn-confirm-delete-submit"
                      type="submit"
                      className="flex-1 py-1.5 bg-red-600 hover:bg-red-500 text-white font-mono text-xs font-bold rounded uppercase tracking-wider transition-colors cursor-pointer"
                    >
                      Erase Reference
                    </button>
                    <button
                      id="btn-confirm-delete-cancel"
                      type="button"
                      onClick={() => {
                        setShowDeletionConfirm(false);
                        setAuthVerifyPassword('');
                        setAuthError('');
                      }}
                      className="px-3 py-1.5 bg-slate-900 border border-slate-800 text-slate-400 font-mono text-xs rounded uppercase tracking-wider hover:text-slate-200 cursor-pointer"
                    >
                      Cancel
                    </button>
                  </div>
                </motion.form>
              )}
            </AnimatePresence>

            {/* Erasure Progress / Status tracker */}
            {deletionStatus !== 'none' && deletionJob && (
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4.5 space-y-3.5 font-mono text-xs">
                <div className="flex justify-between items-center border-b border-slate-800/80 pb-2">
                  <span className="text-slate-500 uppercase text-[10px]">Deletion Job Status:</span>
                  <span className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded ${
                    deletionStatus === 'completed' ? 'bg-emerald-500/10 text-emerald-400' :
                    deletionStatus === 'pending' ? 'bg-cyan-500/10 text-cyan-400 animate-pulse' :
                    'bg-red-500/10 text-red-400'
                  }`}>
                    {deletionStatus.toUpperCase()}
                  </span>
                </div>

                {/* Progress Visual Tracker */}
                <div className="relative pl-6 space-y-4 border-l border-slate-800">
                  {/* Step 1: Requested */}
                  <div className="relative">
                    <div className="absolute -left-[30px] w-4 h-4 rounded-full bg-slate-900 border-2 border-emerald-400 flex items-center justify-center text-[8px] text-emerald-400">
                      ✓
                    </div>
                    <div>
                      <p className="text-slate-200 font-semibold text-[11px]">User Consent Revocation Registered</p>
                      <p className="text-[10px] text-slate-500">{new Date(deletionJob.requestedAt).toLocaleTimeString()}</p>
                    </div>
                  </div>

                  {/* Step 2: Enclave Job Shredding */}
                  <div className="relative">
                    <div className={`absolute -left-[30px] w-4 h-4 rounded-full flex items-center justify-center text-[8px] ${
                      deletionStatus === 'completed' ? 'bg-slate-900 border-2 border-emerald-400 text-emerald-400' :
                      deletionStatus === 'pending' ? 'bg-slate-900 border-2 border-cyan-400 text-cyan-400 animate-spin' :
                      'bg-slate-900 border-2 border-slate-800 text-slate-500'
                    }`}>
                      {deletionStatus === 'completed' ? '✓' : '⟳'}
                    </div>
                    <div>
                      <p className="text-slate-200 font-semibold text-[11px]">Enclave Physical Template Shredding</p>
                      <p className="text-[10px] text-slate-500">Secure zeros overwriting flash pattern registers.</p>
                    </div>
                  </div>

                  {/* Step 3: Audit Reference Published */}
                  <div className="relative">
                    <div className={`absolute -left-[30px] w-4 h-4 rounded-full flex items-center justify-center text-[8px] ${
                      deletionStatus === 'completed' ? 'bg-slate-900 border-2 border-emerald-400 text-emerald-400' : 'bg-slate-900 border-2 border-slate-800 text-slate-500'
                    }`}>
                      {deletionStatus === 'completed' ? '✓' : '•'}
                    </div>
                    <div>
                      <p className="text-slate-200 font-semibold text-[11px]">Shred Certificate Broadcasted</p>
                      <p className="text-[10px] text-cyan-400 font-semibold uppercase">{deletionJob.auditReference}</p>
                    </div>
                  </div>
                </div>

                {deletionStatus === 'completed' && (
                  <p className="text-[10px] text-slate-400 leading-normal bg-emerald-500/5 border border-emerald-500/10 rounded p-2 text-center font-sans">
                    🌱 Reference data fully erased. Secure Enclave certificate emitted.
                  </p>
                )}
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Audit Trail Redacted Events log */}
      <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl">
        <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider border-b border-slate-800 pb-3 mb-4">
          Personal Biometric Audit Trail (Session Trace)
        </h3>
        
        <div className="overflow-x-auto">
          <table className="w-full text-left font-mono text-xs text-slate-300">
            <thead>
              <tr className="text-slate-500 border-b border-slate-800/60 pb-2">
                <th className="py-2">TIMESTAMP</th>
                <th className="py-2">EVENT TYPE</th>
                <th className="py-2">VERIFIER STATION</th>
                <th className="py-2">LIVENESS CLASS</th>
                <th className="py-2">OUTCOME badge</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/40">
              {userLogs.slice(0, 6).map((log) => (
                <tr id={`log-row-${log.id}`} key={log.id} className="hover:bg-slate-950/20">
                  <td className="py-2.5 text-slate-500 text-[11px]">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </td>
                  <td className="py-2.5 font-semibold text-slate-200">{log.eventType.toUpperCase()}</td>
                  <td className="py-2.5 text-slate-400">{log.deviceId}</td>
                  <td className="py-2.5 text-cyan-400 text-[11px]">{log.livenessClass}</td>
                  <td className="py-2.5">
                    <span className={`text-[9px] px-1.5 py-0.5 rounded border ${
                      log.outcome === 'success' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                      log.outcome === 'failed' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                      'bg-amber-500/10 text-amber-400 border-amber-500/20'
                    }`}>
                      {log.outcome.toUpperCase()}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
