import React from 'react';
import { Shield, ShieldAlert, ShieldCheck } from 'lucide-react';
import { StorageClassification } from '../types';

interface KeyBackingBadgeProps {
  storageClass: StorageClassification;
  hasVerifiedEvidence: boolean;
  className?: string;
}

export default function KeyBackingBadge({
  storageClass,
  hasVerifiedEvidence,
  className = ''
}: KeyBackingBadgeProps) {
  if (storageClass === 'software_secured') {
    if (hasVerifiedEvidence) {
      return (
        <span
          className={`inline-flex items-center gap-1 bg-indigo-500/10 text-indigo-400 border border-indigo-500/25 px-2 py-1 rounded-md text-xs font-semibold tracking-wide ${className}`}
        >
          <ShieldCheck className="w-3.5 h-3.5" />
          <span>swk verified</span>
        </span>
      );
    }
    return (
      <span
        className={`inline-flex items-center gap-1 bg-amber-500/10 text-amber-500 border border-amber-500/20 px-2 py-1 rounded-md text-xs font-semibold tracking-wide ${className}`}
      >
        <ShieldAlert className="w-3.5 h-3.5" />
        <span>swk unverified</span>
      </span>
    );
  }

  if (storageClass === 'hardware_backed') {
    return (
      <span
        className={`inline-flex items-center gap-1 bg-emerald-500/10 text-emerald-400 border border-emerald-500/25 px-2 py-1 rounded-md text-xs font-semibold tracking-wide ${className}`}
      >
        <Shield className="w-3.5 h-3.5" />
        <span>hwk hardware</span>
      </span>
    );
  }

  return (
    <span
      className={`inline-flex items-center gap-1 bg-slate-500/10 text-slate-400 border border-slate-700 px-2 py-1 rounded-md text-xs font-semibold tracking-wide ${className}`}
    >
      <ShieldAlert className="w-3.5 h-3.5" />
      <span>unverified</span>
    </span>
  );
}
