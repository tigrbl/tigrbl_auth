import React, { useEffect, useState } from 'react';
import { Smartphone, RefreshCw, Check, X, AlertCircle, Clock } from 'lucide-react';

interface ExternalApprovalWaitProps {
  method: 'push' | 'voice';
  destination: string;
  expirySeconds: number;
  onApprove: () => void;
  onReject: (reason: string) => void;
  onCancel: () => void;
  onResend: () => void;
  canResend: boolean;
}

export const ExternalApprovalWait: React.FC<ExternalApprovalWaitProps> = ({
  method,
  destination,
  expirySeconds,
  onApprove,
  onReject,
  onCancel,
  onResend,
  canResend,
}) => {
  const [timeLeft, setTimeLeft] = useState(expirySeconds);
  const [status, setStatus] = useState<'pending' | 'polling' | 'success' | 'rejected'>('pending');

  useEffect(() => {
    setTimeLeft(expirySeconds);
    setStatus('pending');
  }, [method, destination, expirySeconds]);

  useEffect(() => {
    if (timeLeft <= 0) {
      onReject('Out-of-band waiting period expired (timeout)');
      return;
    }

    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
      // Simple visual toggle for polling indicator
      setStatus((prev) => (prev === 'pending' || prev === 'polling' ? 'polling' : prev));
    }, 1000);

    return () => clearInterval(timer);
  }, [timeLeft, onReject]);

  const handleSimulateUserApproval = () => {
    setStatus('success');
    setTimeout(() => {
      onApprove();
    }, 800);
  };

  const handleSimulateUserRejection = () => {
    setStatus('rejected');
    setTimeout(() => {
      onReject('User explicitly rejected approval request on external device.');
    }, 800);
  };

  return (
    <div className="bg-zinc-950/40 rounded-xl border border-zinc-800 p-4 space-y-4" id="external-approval-wait">
      <div className="flex items-center gap-3">
        <div className="bg-purple-500/15 text-purple-400 p-2.5 rounded-lg border border-purple-500/20 animate-pulse">
          <Smartphone className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <h4 className="font-semibold text-zinc-100 text-sm">
            Pending Out-of-Band Channel Verification
          </h4>
          <p className="text-[11px] text-zinc-400">
            Securely awaiting response on second-party device for target destination: <span className="font-mono text-zinc-300">{destination}</span>
          </p>
        </div>
      </div>

      {/* Progress Polling Indicator */}
      <div className="bg-zinc-900/60 rounded-xl border border-zinc-800 p-4 text-center space-y-3">
        <div className="flex justify-center items-center gap-2">
          <RefreshCw className="h-4 w-4 text-purple-400 animate-spin" />
          <span className="text-xs text-purple-300 font-mono tracking-wider uppercase font-medium">
            Polling secure callback correlation channel...
          </span>
        </div>

        <div className="flex items-center justify-center gap-4 py-1">
          <div className="flex items-center gap-1.5 text-zinc-400 text-xs font-mono bg-zinc-950 px-2.5 py-1 rounded-md border border-zinc-800">
            <Clock className="h-3.5 w-3.5 text-zinc-500" />
            <span>Time Left: {timeLeft}s</span>
          </div>
          <span className="text-2xs text-zinc-600 uppercase tracking-widest font-bold">
            Method: {method === 'push' ? 'Native Mobile Push' : 'Voice Callback Ring'}
          </span>
        </div>

        <div className="w-full bg-zinc-950 h-1.5 rounded-full overflow-hidden border border-zinc-900">
          <div
            className="bg-gradient-to-r from-purple-500 to-indigo-500 h-full transition-all duration-1000 ease-linear"
            style={{ width: `${(timeLeft / expirySeconds) * 100}%` }}
          />
        </div>
      </div>

      {/* Interactive Simulator Controls */}
      <div className="bg-zinc-900/40 rounded-lg p-3 border border-dashed border-zinc-800 space-y-2.5">
        <div className="flex items-center justify-between">
          <span className="text-[10px] text-zinc-400 uppercase font-mono tracking-wider font-semibold">
            Interactive OOB Simulated Device
          </span>
          <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-ping" />
        </div>
        <p className="text-[11px] text-zinc-500">
          Since the preview iframe operates standalone, simulate how an OOB device responds over the secure callback webhook:
        </p>
        <div className="grid grid-cols-2 gap-2">
          <button
            onClick={handleSimulateUserApproval}
            className="flex items-center justify-center gap-1.5 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 hover:text-white border border-emerald-500/20 hover:border-emerald-500/40 rounded-lg py-2 text-xs font-medium font-mono transition"
            id="simulate-approve-btn"
          >
            <Check className="h-3.5 w-3.5" />
            Simulate Approve
          </button>
          <button
            onClick={handleSimulateUserRejection}
            className="flex items-center justify-center gap-1.5 bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 hover:text-white border border-rose-500/20 hover:border-rose-500/40 rounded-lg py-2 text-xs font-medium font-mono transition"
            id="simulate-reject-btn"
          >
            <X className="h-3.5 w-3.5" />
            Simulate Reject
          </button>
        </div>
      </div>

      {/* Primary flow buttons (Cancel / Resend) */}
      <div className="flex items-center justify-between border-t border-zinc-900 pt-3">
        <button
          onClick={onCancel}
          className="text-2xs text-zinc-400 hover:text-zinc-200 bg-zinc-900 border border-zinc-800 rounded-lg px-3 py-1.5 font-medium transition hover:bg-zinc-800"
          id="cancel-oob-btn"
        >
          Cancel Waiting
        </button>

        <button
          onClick={onResend}
          disabled={!canResend}
          className={`flex items-center gap-1 text-2xs rounded-lg px-3 py-1.5 font-medium transition font-mono ${
            canResend
              ? 'bg-purple-600/20 hover:bg-purple-600/30 text-purple-300 border border-purple-500/30 hover:border-purple-500/50 cursor-pointer'
              : 'bg-zinc-900 text-zinc-600 border border-zinc-950 cursor-not-allowed'
          }`}
          id="resend-oob-btn"
        >
          <RefreshCw className="h-3 w-3" />
          Resend Message
        </button>
      </div>
    </div>
  );
};
