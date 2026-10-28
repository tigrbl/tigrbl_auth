import React, { useState } from 'react';
import { Trash2, ShieldAlert, CheckCircle2, Clock, FileText, ArrowRight, RefreshCw, HelpCircle } from 'lucide-react';
import { DeletionStatus } from '../types';

interface BiometricDeletionStatusProps {
  status: DeletionStatus;
  txHash?: string;
  requestTime?: string;
  onInitiateDelete: (forceFail?: boolean) => void;
  onResetStatus: () => void;
}

export default function BiometricDeletionStatus({
  status,
  txHash,
  requestTime,
  onInitiateDelete,
  onResetStatus,
}: BiometricDeletionStatusProps) {
  const [forceFailSim, setForceFailSim] = useState(false);
  const [isHovering, setIsHovering] = useState(false);

  const getStepStatus = (step: number) => {
    if (status === 'none') return 'pending';
    if (status === 'completed') return 'success';
    
    if (status === 'pending') {
      if (step === 1) return 'success';
      if (step === 2) return 'active';
      return 'pending';
    }

    if (status === 'failed') {
      if (step === 1) return 'success';
      if (step === 2) return 'failed';
      return 'pending';
    }
    return 'pending';
  };

  const getStepClass = (step: number) => {
    const s = getStepStatus(step);
    if (s === 'success') return 'border-emerald-500 bg-emerald-500/5 text-emerald-400';
    if (s === 'active') return 'border-indigo-500 bg-indigo-500/5 text-indigo-400 animate-pulse';
    if (s === 'failed') return 'border-rose-500 bg-rose-500/5 text-rose-400';
    return 'border-slate-800 bg-slate-950/20 text-slate-500';
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-xl mx-auto animate-fade-in" id="deletion-status-container">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Trash2 className="w-5 h-5 text-rose-400" />
          <div>
            <h4 className="font-sans font-semibold text-slate-100 text-sm">Biometric Purge & Erasure Panel</h4>
            <p className="font-mono text-[10px] text-slate-500">Compliance: GDPR Article 17 | CCPA Section 1798.105</p>
          </div>
        </div>
        <span className="font-mono text-[10px] bg-rose-950/40 text-rose-400 px-2 py-0.5 rounded border border-rose-900/40">
          HARD DELETE
        </span>
      </div>

      <div className="p-6 space-y-6">
        {status === 'none' ? (
          <div className="space-y-4">
            <div className="bg-rose-500/5 border border-rose-500/10 p-4 rounded-xl flex gap-3">
              <ShieldAlert className="w-5 h-5 text-rose-400 shrink-0 mt-0.5" />
              <div className="text-xs space-y-1 text-slate-300">
                <span className="font-sans font-bold text-rose-400">Irreversible Action Warning</span>
                <p className="text-slate-400 leading-normal font-sans">
                  Initiating a purge request permanently revokes your signed voice biometric profile. 
                  The underlying SentryVoice mathematical feature vector is unrecoverable. 
                  Any subsequent login will require re-enrollment or alternative authentication factors.
                </p>
              </div>
            </div>

            {/* Simulated Deletion Toggle */}
            <div className="flex items-center justify-between bg-slate-950/40 border border-slate-850 p-3 rounded-lg text-xs">
              <div className="flex items-center gap-2">
                <HelpCircle className="w-4 h-4 text-slate-500" />
                <span className="text-slate-300 font-mono">Force Deletion Failure (Simulate Timeout)</span>
              </div>
              <input
                type="checkbox"
                checked={forceFailSim}
                onChange={() => setForceFailSim(!forceFailSim)}
                className="accent-rose-500 h-4 w-4 rounded"
                id="chk-sim-delete-fail"
              />
            </div>

            <button
              type="button"
              onClick={() => onInitiateDelete(forceFailSim)}
              className="w-full bg-rose-500 hover:bg-rose-400 text-slate-950 font-sans font-semibold text-xs py-2.5 rounded-lg transition-all shadow-lg shadow-rose-500/10"
              id="btn-delete-initiate"
            >
              Confirm and Purge Voice Profile
            </button>
          </div>
        ) : (
          <div className="space-y-5">
            {/* Erasure Tracker Stepper */}
            <div className="space-y-3">
              {/* Step 1 */}
              <div className={`p-3 border rounded-xl flex items-center justify-between text-xs transition-colors ${getStepClass(1)}`}>
                <div className="flex items-center gap-3">
                  <span className="font-mono bg-slate-950/60 rounded h-5 w-5 flex items-center justify-center border border-slate-800">1</span>
                  <div>
                    <span className="font-semibold block font-sans text-slate-200">Consent Revocation Block</span>
                    <p className="text-slate-500 mt-0.5">Biometric profile vbm flag set to &ldquo;revoked&rdquo; in primary directory.</p>
                  </div>
                </div>
                <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
              </div>

              {/* Step 2 */}
              <div className={`p-3 border rounded-xl flex items-center justify-between text-xs transition-colors ${getStepClass(2)}`}>
                <div className="flex items-center gap-3">
                  <span className="font-mono bg-slate-950/60 rounded h-5 w-5 flex items-center justify-center border border-slate-800">2</span>
                  <div>
                    <span className="font-semibold block font-sans text-slate-200">Verifier Node Vector Purge</span>
                    <p className="text-slate-500 mt-0.5">Contacting active SentryVoice verifier at US-EAST-1 cluster.</p>
                  </div>
                </div>
                {getStepStatus(2) === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                {getStepStatus(2) === 'active' && <RefreshCw className="w-4 h-4 text-indigo-400 animate-spin shrink-0" />}
                {getStepStatus(2) === 'failed' && <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" />}
              </div>

              {/* Step 3 */}
              <div className={`p-3 border rounded-xl flex items-center justify-between text-xs transition-colors ${getStepClass(3)}`}>
                <div className="flex items-center gap-3">
                  <span className="font-mono bg-slate-950/60 rounded h-5 w-5 flex items-center justify-center border border-slate-800">3</span>
                  <div>
                    <span className="font-semibold block font-sans text-slate-200">Audit Receipt & Certificate generation</span>
                    <p className="text-slate-500 mt-0.5">Creating decentralized compliance record of deletion.</p>
                  </div>
                </div>
                {getStepStatus(3) === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
              </div>
            </div>

            {/* Outcome message blocks */}
            {status === 'completed' && (
              <div className="bg-emerald-500/5 border border-emerald-500/10 p-4 rounded-xl space-y-2.5">
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5 font-sans">
                  <CheckCircle2 className="w-4 h-4" />
                  <span>Permanent Erasure Certified</span>
                </span>
                <p className="text-[11px] text-slate-400 leading-normal font-sans">
                  The SentryVoice biometric engine successfully cleared all voice vectors. Regional backup databases synchronized and deleted corresponding nodes. Consent log archived as compliance receipt.
                </p>
                {txHash && (
                  <div className="bg-slate-950 p-2 rounded border border-slate-900 flex justify-between items-center font-mono text-[9px] text-slate-500">
                    <span>Tx Hash: {txHash}</span>
                    <span>{requestTime}</span>
                  </div>
                )}
              </div>
            )}

            {status === 'failed' && (
              <div className="bg-rose-500/5 border border-rose-500/10 p-4 rounded-xl space-y-2.5">
                <span className="text-xs font-semibold text-rose-400 flex items-center gap-1.5 font-sans">
                  <ShieldAlert className="w-4 h-4" />
                  <span>Purge Failed: Verifier Node Offline</span>
                </span>
                <p className="text-[11px] text-slate-400 leading-normal font-sans">
                  The SentryVoice verifier returned a timeout connection (error 504 Gateway Timeout). Under privacy guidelines, this request is queued for automatic retries every 3 hours. Biometric authentication remains locked in secondary protection boundaries.
                </p>
                <div className="flex justify-end gap-2 pt-1">
                  <button
                    type="button"
                    onClick={onResetStatus}
                    className="text-slate-400 hover:text-slate-200 text-[10px] font-mono px-3 py-1 bg-slate-950 border border-slate-800 rounded transition-colors cursor-pointer"
                    id="btn-delete-failed-reset"
                  >
                    Reset Deletion Panel
                  </button>
                  <button
                    type="button"
                    onClick={() => onInitiateDelete(false)}
                    className="text-indigo-400 hover:text-indigo-300 text-[10px] font-mono px-3 py-1 bg-indigo-500/5 border border-indigo-500/20 rounded transition-colors cursor-pointer"
                    id="btn-delete-failed-retry"
                  >
                    Retry Purge
                  </button>
                </div>
              </div>
            )}

            {status === 'completed' && (
              <button
                type="button"
                onClick={onResetStatus}
                className="w-full bg-slate-800 hover:bg-slate-750 text-slate-200 text-xs py-2 rounded-lg transition-colors font-sans font-medium cursor-pointer"
                id="btn-delete-reset-complete"
              >
                Acknowledge Compliance Certificate
              </button>
            )}
          </div>
        )}
      </div>
    </div>
  );
}
