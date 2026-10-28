import React from 'react';
import { Shield, ShieldCheck, HelpCircle, KeyRound, AlertTriangle, Cpu, Terminal, Sparkles } from 'lucide-react';
import { HardwareAuthenticator } from './types';

// KeyBackingBadge renders the evidence-driven HWK status
export const KeyBackingBadge: React.FC<{ backing: 'verified_hwk' | 'unverified' | 'software_only' | 'unavailable' }> = ({ backing }) => {
  switch (backing) {
    case 'verified_hwk':
      return (
        <span className="inline-flex items-center gap-1 bg-emerald-500/10 text-emerald-400 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border border-emerald-500/20 shadow-[0_0_8px_rgba(16,185,129,0.1)]">
          <ShieldCheck className="w-3 h-3 text-emerald-400" />
          hwk:verified
        </span>
      );
    case 'unverified':
      return (
        <span className="inline-flex items-center gap-1 bg-amber-500/10 text-amber-400 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border border-amber-500/20">
          <AlertTriangle className="w-3 h-3 text-amber-400" />
          hwk:unverified
        </span>
      );
    case 'software_only':
      return (
        <span className="inline-flex items-center gap-1 bg-blue-500/10 text-blue-400 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border border-blue-500/20">
          <HelpCircle className="w-3 h-3 text-blue-400" />
          software_only
        </span>
      );
    case 'unavailable':
    default:
      return (
        <span className="inline-flex items-center gap-1 bg-slate-500/10 text-slate-400 px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-wider border border-slate-500/20">
          evidence_unavailable
        </span>
      );
  }
};

// TransportBadge renders an icon representing transport
export const TransportBadge: React.FC<{ transport: string }> = ({ transport }) => {
  return (
    <span className="bg-white/5 border border-white/10 text-slate-300 font-mono text-[10px] px-1.5 py-0.5 rounded">
      {transport.toUpperCase()}
    </span>
  );
};

// TrustRootBadge renders certification details
export const TrustRootBadge: React.FC<{ level: string }> = ({ level }) => {
  const colorClass = level === 'L3' ? 'text-emerald-400 border-emerald-500/20 bg-emerald-500/5' :
                     level === 'L2' ? 'text-blue-400 border-blue-500/20 bg-blue-500/5' :
                     'text-slate-400 border-slate-500/20 bg-slate-500/5';
  return (
    <span className={`border px-1.5 py-0.5 rounded text-[9px] font-mono font-bold ${colorClass}`}>
      FIDO {level}
    </span>
  );
};

// CLICommandOutput simulates code/CLI output
export const CLICommandOutput: React.FC<{ command: string; output: string }> = ({ command, output }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(output);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="bg-black/40 rounded-xl border border-white/5 overflow-hidden font-mono text-xs text-slate-300 shadow-inner">
      <div className="bg-slate-900/80 px-4 py-2 border-b border-white/5 flex justify-between items-center">
        <span className="flex items-center gap-2 text-slate-400 text-[10px]">
          <Terminal className="w-3 h-3 text-emerald-400" />
          DIAGNOSTIC TERMINAL
        </span>
        <button 
          onClick={handleCopy}
          className="text-[10px] hover:text-white bg-white/5 px-2 py-0.5 rounded transition"
        >
          {copied ? 'Copied!' : 'Copy Output'}
        </button>
      </div>
      <div className="p-4 space-y-2 max-h-[220px] overflow-y-auto whitespace-pre-wrap leading-relaxed">
        <div className="text-emerald-400 select-none">$ {command}</div>
        <div className="text-slate-300">{output}</div>
      </div>
    </div>
  );
};

// Device status bar indicators
export const StatusIndicator: React.FC<{ status: 'active' | 'suspended' | 'revoked' }> = ({ status }) => {
  switch (status) {
    case 'active':
      return (
        <span className="flex items-center gap-1 text-emerald-400 text-xs">
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
          Active
        </span>
      );
    case 'suspended':
      return (
        <span className="flex items-center gap-1 text-amber-400 text-xs">
          <span className="w-1.5 h-1.5 rounded-full bg-amber-500"></span>
          Suspended
        </span>
      );
    case 'revoked':
      return (
        <span className="flex items-center gap-1 text-red-400 text-xs">
          <span className="w-1.5 h-1.5 rounded-full bg-red-500"></span>
          Revoked
        </span>
      );
  }
};
