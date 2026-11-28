import React, { useState } from 'react';
import { Key, ShieldAlert, CheckCircle, RefreshCw, AlertCircle } from 'lucide-react';

interface PinResetArtifactStateProps {
  onInitiateReset: () => void;
  onVerifyArtifact: (artifact: string) => boolean;
  onCompleteNewPin: (newPin: string) => void;
  activeArtifact: string | null;
  errorMsg: string | null;
  successMsg: string | null;
}

export function PinResetArtifactState({
  onInitiateReset,
  onVerifyArtifact,
  onCompleteNewPin,
  activeArtifact,
  errorMsg,
  successMsg,
}: PinResetArtifactStateProps) {
  const [artifactInput, setArtifactInput] = useState('');
  const [verified, setVerified] = useState(false);
  const [newPin, setNewPin] = useState('');
  const [newConfirm, setNewConfirm] = useState('');
  const [localError, setLocalError] = useState<string | null>(null);

  const handleVerify = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    if (!artifactInput.trim()) {
      setLocalError('Please enter a recovery artifact.');
      return;
    }
    const success = onVerifyArtifact(artifactInput.trim());
    if (success) {
      setVerified(true);
    }
  };

  const handleComplete = (e: React.FormEvent) => {
    e.preventDefault();
    setLocalError(null);
    if (newPin.length < 6) {
      setLocalError('New PIN must be at least 6 digits.');
      return;
    }
    if (newPin !== newConfirm) {
      setLocalError('PIN confirmation does not match.');
      return;
    }
    onCompleteNewPin(newPin);
    // Reset local state
    setArtifactInput('');
    setVerified(false);
    setNewPin('');
    setNewConfirm('');
  };

  return (
    <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-2xl text-left space-y-4">
      <div className="flex items-center gap-1.5 border-b border-slate-800 pb-3">
        <Key size={14} className="text-yellow-400 animate-spin-slow" />
        <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300">
          First-Party Secure Recovery & Reset Boundary
        </h3>
      </div>

      {successMsg && (
        <div className="bg-emerald-950/20 text-emerald-400 text-xs p-3 rounded-lg border border-emerald-900/40 flex items-start gap-2">
          <CheckCircle size={15} className="mt-0.5 shrink-0" />
          <span>{successMsg}</span>
        </div>
      )}

      {errorMsg && (
        <div className="bg-red-950/20 text-red-400 text-xs p-3 rounded-lg border border-red-900/40 flex items-start gap-2">
          <ShieldAlert size={15} className="mt-0.5 shrink-0" />
          <span>{errorMsg}</span>
        </div>
      )}

      {localError && (
        <div className="bg-red-950/20 text-red-400 text-xs p-3 rounded-lg border border-red-900/40 flex items-start gap-2">
          <AlertCircle size={15} className="mt-0.5 shrink-0" />
          <span>{localError}</span>
        </div>
      )}

      {!activeArtifact && !verified && (
        <div className="space-y-3">
          <p className="text-xs text-slate-400 leading-relaxed">
            Forgot your PIN or blocked due to too many attempts? You can initiate a cryptographically bound recovery ceremony.
          </p>
          <button
            type="button"
            onClick={onInitiateReset}
            className="w-full py-2 px-4 rounded-xl bg-yellow-950 border border-yellow-800 text-yellow-300 font-semibold text-xs tracking-wider uppercase shadow-md hover:bg-yellow-900 hover:text-yellow-200 transition-all cursor-pointer flex items-center justify-center gap-1.5"
          >
            <RefreshCw size={13} />
            Generate Recovery Secret Artifact
          </button>
        </div>
      )}

      {activeArtifact && !verified && (
        <form onSubmit={handleVerify} className="space-y-3.5">
          <div className="bg-slate-950 p-3 rounded-xl border border-slate-800 font-mono text-center space-y-1">
            <span className="text-[9px] text-slate-500 uppercase block tracking-wider">ACTIVE RECOVERY ARTIFACT TOKEN (DO NOT DISCLOSE)</span>
            <span className="text-sm text-yellow-400 font-bold select-all tracking-wider">{activeArtifact}</span>
          </div>

          <div className="space-y-1">
            <label className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
              Enter Recovery Artifact
            </label>
            <input
              type="text"
              value={artifactInput}
              onChange={(e) => setArtifactInput(e.target.value)}
              placeholder="e.g. TIGRBL-REC-..."
              className="w-full text-xs font-mono py-2.5 px-3 rounded-xl bg-slate-950 border border-slate-850 text-slate-100 placeholder-slate-700 focus:outline-none focus:ring-1 focus:ring-yellow-500"
            />
          </div>

          <button
            type="submit"
            className="w-full py-2 rounded-xl bg-yellow-600 hover:bg-yellow-500 text-white font-semibold text-xs tracking-wider uppercase transition-all cursor-pointer"
          >
            Verify Recovery Artifact Code
          </button>
        </form>
      )}

      {verified && (
        <form onSubmit={handleComplete} className="space-y-4">
          <div className="bg-emerald-950/20 text-emerald-400 text-xs p-3 rounded-lg border border-emerald-900/40">
            ✓ Recovery Artifact successfully verified. Complete your new PIN enrollment below.
          </div>

          <div className="space-y-3">
            <div className="space-y-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
                New PIN (Numbers only)
              </label>
              <input
                type="password"
                pattern="[0-9]*"
                inputMode="numeric"
                maxLength={12}
                value={newPin}
                onChange={(e) => setNewPin(e.target.value.replace(/[^0-9]/g, ''))}
                placeholder="••••••"
                className="w-full text-center tracking-[0.3em] font-mono text-base py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-100"
              />
            </div>

            <div className="space-y-1">
              <label className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">
                Confirm New PIN
              </label>
              <input
                type="password"
                pattern="[0-9]*"
                inputMode="numeric"
                maxLength={12}
                value={newConfirm}
                onChange={(e) => setNewConfirm(e.target.value.replace(/[^0-9]/g, ''))}
                placeholder="••••••"
                className="w-full text-center tracking-[0.3em] font-mono text-base py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-100"
              />
            </div>
          </div>

          <button
            type="submit"
            className="w-full py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold text-xs tracking-wider uppercase transition-all cursor-pointer shadow-md"
          >
            Activate New PIN Verifier
          </button>
        </form>
      )}
    </div>
  );
}
