import React from 'react';
import { Network, Server, ShieldCheck, ShieldAlert, AlertOctagon } from 'lucide-react';

interface KeyDependencyImpactProps {
  dependencies: string[];
  status: string;
  keyName: string;
}

export default function KeyDependencyImpact({
  dependencies,
  status,
  keyName
}: KeyDependencyImpactProps) {
  const isCompromised = status === 'compromised';
  const isRevoked = status === 'revoked';
  const isActive = status === 'active';

  return (
    <div id="key-dependency-impact" className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 space-y-3.5">
      <div className="flex items-center gap-2 border-b border-slate-800/80 pb-2">
        <Network className="w-4 h-4 text-indigo-400" />
        <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Dependent Systems Impact ({dependencies.length})</span>
      </div>

      <div className="space-y-3">
        <p className="text-[11px] text-slate-400 leading-normal">
          The following core services rely on cryptographic signatures backed by <strong className="font-semibold text-slate-200">{keyName}</strong>:
        </p>

        <div className="space-y-2 max-h-[140px] overflow-y-auto">
          {dependencies.map((dep, index) => (
            <div
              key={dep + index}
              className={`p-2.5 rounded-lg border flex items-center justify-between text-xs transition-colors ${
                isCompromised
                  ? 'bg-rose-950/20 border-rose-900/60'
                  : isRevoked
                  ? 'bg-slate-950/40 border-slate-800/80'
                  : 'bg-slate-950/20 border-slate-850'
              }`}
            >
              <div className="flex items-center gap-2">
                <Server className={`w-3.5 h-3.5 ${isCompromised ? 'text-rose-400' : isRevoked ? 'text-slate-500' : 'text-indigo-400'}`} />
                <span className={`font-mono text-[11px] font-semibold ${isCompromised ? 'text-rose-300' : isRevoked ? 'text-slate-400' : 'text-slate-300'}`}>
                  {dep}
                </span>
              </div>

              {isCompromised ? (
                <span className="inline-flex items-center gap-1 text-[9px] font-extrabold uppercase bg-rose-950/80 text-rose-400 border border-rose-900/60 px-1.5 py-0.5 rounded animate-pulse">
                  <AlertOctagon className="w-2.5 h-2.5" /> Blocked
                </span>
              ) : isRevoked ? (
                <span className="inline-flex items-center gap-1 text-[9px] font-extrabold uppercase bg-slate-850 text-slate-500 border border-slate-800 px-1.5 py-0.5 rounded">
                  Retired
                </span>
              ) : (
                <span className="inline-flex items-center gap-1 text-[9px] font-extrabold uppercase bg-emerald-950/40 text-emerald-400 border border-emerald-900/40 px-1.5 py-0.5 rounded">
                  <ShieldCheck className="w-2.5 h-2.5" /> Enforced
                </span>
              )}
            </div>
          ))}
        </div>

        {isCompromised && (
          <div className="bg-rose-950/40 border border-rose-900/60 rounded-lg p-3 text-[11px] leading-relaxed text-rose-300">
            <strong>CRITICAL OUTAGE WARNING:</strong> Gateway proxy is dropping all inbound traffic signed by this credential to protect against key compromise exfiltration.
          </div>
        )}
      </div>
    </div>
  );
}
