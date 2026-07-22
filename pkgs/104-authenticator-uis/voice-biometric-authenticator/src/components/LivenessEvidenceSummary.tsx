import React from 'react';
import { Award, ShieldAlert, CheckCircle2, Cpu, Calendar, Clock, Fingerprint, Lock, Copy } from 'lucide-react';

interface LivenessEvidenceSummaryProps {
  amrToken: string;
  livenessClass: string;
  confidenceScore: number;
  timeFreshnessMs: number;
  nonce: string;
  onClose?: () => void;
}

export default function LivenessEvidenceSummary({
  amrToken,
  livenessClass,
  confidenceScore,
  timeFreshnessMs,
  nonce,
  onClose,
}: LivenessEvidenceSummaryProps) {
  const getLivenessStatus = () => {
    switch (livenessClass) {
      case 'live':
        return {
          color: 'text-emerald-400 bg-emerald-500/10 border-emerald-500/20',
          title: 'Genuine speech (Liveness verified)',
          desc: 'Phase coherence, acoustic formant jitter, and thermal noise patterns confirm organic vocal generation.',
          icon: CheckCircle2,
        };
      case 'synthetic':
        return {
          color: 'text-rose-400 bg-rose-500/10 border-rose-500/20',
          title: 'Spoof Suspected: Synthetic Voice/AI',
          desc: 'High vocoder phase regularity, missing high-frequency micro-tremors, or uniform spectral patterns suggest AI-synthesized deepfake audio.',
          icon: ShieldAlert,
        };
      case 'replay':
        return {
          color: 'text-amber-400 bg-amber-500/10 border-amber-500/20',
          title: 'Spoof Suspected: Replay Signature',
          desc: 'Background room reverberation convolution or hardware speaker characteristics match a replayed recording signature.',
          icon: ShieldAlert,
        };
      case 'excessive_noise':
        return {
          color: 'text-indigo-400 bg-indigo-500/10 border-indigo-500/20',
          title: 'Acoustic Failure: Excessive Noise',
          desc: 'Signal-to-noise ratio drops below standard matching envelope. Features are unextractable.',
          icon: ShieldAlert,
        };
      default:
        return {
          color: 'text-slate-400 bg-slate-500/10 border-slate-500/20',
          title: 'Unknown Liveness Outcome',
          desc: 'An unexpected verifier condition prevented complete analysis.',
          icon: ShieldAlert,
        };
    }
  };

  const status = getLivenessStatus();
  const StatusIcon = status.icon;

  const handleCopyToken = () => {
    navigator.clipboard.writeText(amrToken);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-xl mx-auto" id="evidence-summary-container">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Fingerprint className="w-5 h-5 text-indigo-400" />
          <div>
            <h4 className="font-sans font-semibold text-slate-100 text-sm">Biometric Evidence Log</h4>
            <p className="font-mono text-[10px] text-slate-500">Method identifier: vbm (Voice Biometric Method)</p>
          </div>
        </div>
        <span className="font-mono text-[10px] bg-slate-950 px-2.5 py-1 rounded-md text-slate-400 border border-slate-850">
          SECURE ENVELOPE
        </span>
      </div>

      <div className="p-6 space-y-5">
        {/* Liveness Outcome */}
        <div className={`p-4 rounded-xl border ${status.color} space-y-1.5`}>
          <div className="flex items-center gap-2 font-sans font-semibold text-sm">
            <StatusIcon className="w-4 h-4 shrink-0" />
            <span>{status.title}</span>
          </div>
          <p className="text-xs text-slate-400 leading-normal pl-6 font-sans">
            {status.desc}
          </p>
        </div>

        {/* Diagnostic Metadata Grid */}
        <div className="grid grid-cols-2 gap-3 text-xs">
          <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/80">
            <span className="text-[10px] font-mono text-slate-500 block uppercase mb-1">AMR EVIDENCE FLAG</span>
            <div className="flex items-center gap-2">
              <Award className="w-4 h-4 text-indigo-400" />
              <span className="font-mono font-medium text-slate-200">vbm (Voice match)</span>
            </div>
          </div>
          <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/80">
            <span className="text-[10px] font-mono text-slate-500 block uppercase mb-1">MATCHER CONFIDENCE</span>
            <div className="flex items-center gap-2">
              <Cpu className="w-4 h-4 text-emerald-400" />
              <span className="font-mono font-semibold text-slate-100">{confidenceScore}%</span>
            </div>
          </div>
          <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/80">
            <span className="text-[10px] font-mono text-slate-500 block uppercase mb-1">CAPTURE FRESHNESS</span>
            <div className="flex items-center gap-2">
              <Clock className="w-4 h-4 text-indigo-400" />
              <span className="font-mono font-medium text-slate-200">{(timeFreshnessMs / 1000).toFixed(2)}s latency</span>
            </div>
          </div>
          <div className="bg-slate-950/40 p-3 rounded-xl border border-slate-800/80">
            <span className="text-[10px] font-mono text-slate-500 block uppercase mb-1">REGIONAL PROCESSING</span>
            <div className="flex items-center gap-2">
              <Calendar className="w-4 h-4 text-indigo-400" />
              <span className="font-mono font-medium text-slate-200">US-EAST-1 (Isolated)</span>
            </div>
          </div>
        </div>

        {/* Nonce & Token Payload block */}
        <div className="bg-slate-950 rounded-xl p-4 border border-slate-850 space-y-2.5">
          <div className="flex justify-between items-center">
            <span className="text-[10px] font-mono text-slate-500 uppercase tracking-wider flex items-center gap-1">
              <Lock className="w-3 h-3 text-emerald-500" />
              <span>Signed Verification Token</span>
            </span>
            <button
              type="button"
              onClick={handleCopyToken}
              className="text-slate-500 hover:text-slate-300 p-1 rounded hover:bg-slate-900 transition-colors"
              title="Copy token to clipboard"
              id="btn-evidence-copy"
            >
              <Copy className="w-3.5 h-3.5" />
            </button>
          </div>
          <div className="bg-slate-900/50 p-2.5 rounded-lg border border-slate-850/60 font-mono text-[10px] text-slate-400 break-all leading-normal select-all">
            {amrToken}
          </div>
          <div className="flex justify-between text-[9px] text-slate-600 font-mono">
            <span>Nonce: {nonce}</span>
            <span>Alg: RS256 | JWT signed by SentryVoice</span>
          </div>
        </div>

        {/* Policy limitations disclosure */}
        <p className="text-[10px] text-slate-500 text-center leading-normal">
          This biometric authentication token conforms with the active organization scope. It constitutes high-entropy evidence of matching (`vbm`), stored for non-repudiation inside the auditable identity trail for 180 days.
        </p>

        {onClose && (
          <div className="flex justify-end pt-2 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="w-full bg-slate-800 hover:bg-slate-750 text-slate-200 font-medium text-xs py-2 rounded-lg transition-colors cursor-pointer"
              id="btn-evidence-close"
            >
              Acknowledge & Continue
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
