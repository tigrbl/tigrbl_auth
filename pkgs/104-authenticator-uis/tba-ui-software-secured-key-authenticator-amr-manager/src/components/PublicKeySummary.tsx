import React, { useState } from 'react';
import { Key, Copy, Check, Info } from 'lucide-react';

interface PublicKeySummaryProps {
  publicKeyJwk: string;
  fingerprint: string;
  algorithm: string;
}

export default function PublicKeySummary({
  publicKeyJwk,
  fingerprint,
  algorithm
}: PublicKeySummaryProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(publicKeyJwk);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  let parsedJwk: any = {};
  try {
    parsedJwk = JSON.parse(publicKeyJwk);
  } catch {
    parsedJwk = { error: "Failed to parse public JWK structure" };
  }

  return (
    <div id="public-key-summary" className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3.5">
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
        <div className="flex items-center gap-1.5 font-bold text-indigo-400 text-xs uppercase tracking-wide">
          <Key className="w-3.5 h-3.5" />
          <span>Public Key Materials (JWK)</span>
        </div>
        <button
          onClick={handleCopy}
          className="text-[10px] text-slate-400 hover:text-slate-200 font-bold flex items-center gap-1 bg-slate-850 px-2 py-1 rounded border border-slate-800 transition-colors"
        >
          {copied ? (
            <>
              <Check className="w-3 h-3 text-emerald-400" />
              <span className="text-emerald-400">Copied!</span>
            </>
          ) : (
            <>
              <Copy className="w-3 h-3" />
              <span>Copy JWK</span>
            </>
          )}
        </button>
      </div>

      <div className="space-y-2">
        <div className="p-3 bg-slate-950/80 rounded-lg border border-slate-850 font-mono text-[10px] text-slate-300 leading-normal max-h-[140px] overflow-y-auto">
          <pre>{JSON.stringify(parsedJwk, null, 2)}</pre>
        </div>

        <div className="space-y-1">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block">SHA256 FINGERPRINT</span>
          <div className="p-2 bg-slate-950/40 rounded-lg border border-slate-850 text-[10px] font-mono text-slate-400 select-all break-all leading-normal">
            {fingerprint}
          </div>
        </div>
      </div>
    </div>
  );
}
