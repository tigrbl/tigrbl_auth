import React, { useState } from 'react';
import { Eye, EyeOff, Copy, Check, ShieldAlert } from 'lucide-react';

interface OneTimeSecretRevealProps {
  secret: string;
  label: string;
}

export default function OneTimeSecretReveal({
  secret,
  label
}: OneTimeSecretRevealProps) {
  const [revealed, setRevealed] = useState(false);
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(secret);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div id="one-time-secret-reveal" className="bg-amber-500/10 border border-amber-500/20 rounded-xl p-4 space-y-3">
      <div className="flex items-center gap-1.5 text-amber-800 text-xs font-bold uppercase tracking-wider">
        <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0" />
        <span>{label}</span>
      </div>

      <p className="text-xs text-amber-700/90 leading-relaxed">
        This single-use backup token is generated inside the isolated client. Store this token securely; it cannot be recovered or displayed again.
      </p>

      <div className="flex items-center gap-2 bg-white/60 border border-amber-200/55 rounded-xl p-3 shadow-inner">
        <div className="flex-1 font-mono text-sm tracking-widest font-bold text-slate-800 break-all select-all">
          {revealed ? secret : '••••••••••••••••••••••••'}
        </div>

        <div className="flex items-center gap-1 shrink-0">
          <button
            type="button"
            onClick={() => setRevealed(!revealed)}
            className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-200/50 rounded-lg transition-colors cursor-pointer"
            title={revealed ? 'Obscure Token' : 'Reveal Token'}
          >
            {revealed ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
          </button>

          <button
            type="button"
            onClick={handleCopy}
            className="p-2 text-slate-500 hover:text-slate-700 hover:bg-slate-200/50 rounded-lg transition-colors cursor-pointer"
            title="Copy to Clipboard"
          >
            {copied ? <Check className="w-4 h-4 text-emerald-600" /> : <Copy className="w-4 h-4" />}
          </button>
        </div>
      </div>
    </div>
  );
}
