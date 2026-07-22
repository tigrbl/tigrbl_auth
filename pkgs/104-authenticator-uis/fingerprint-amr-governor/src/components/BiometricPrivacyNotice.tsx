import React from 'react';
import { ShieldCheck, EyeOff, KeyRound } from 'lucide-react';

export default function BiometricPrivacyNotice() {
  return (
    <div id="privacy-notice" className="bg-slate-900 border border-slate-800 rounded-xl p-5 text-sm text-slate-300 shadow-md">
      <div className="flex items-center gap-3 border-b border-slate-800 pb-3 mb-3">
        <ShieldCheck className="text-emerald-400 w-5 h-5 flex-shrink-0" id="shield-icon" />
        <h4 className="font-semibold text-slate-100" id="privacy-title">Biometric Cryptographic Verification Protocol</h4>
      </div>
      
      <p className="mb-3 text-slate-400 leading-relaxed">
        This platform uses cryptographic evidence to certify user verification. We enforce absolute privacy:
      </p>

      <ul className="space-y-2 text-slate-300">
        <li className="flex items-start gap-2" id="privacy-item-1">
          <EyeOff className="text-amber-400 w-4 h-4 mt-0.5 flex-shrink-0" />
          <span>
            <strong>No Sensor Capture:</strong> Physical biometric templates, prints, or images are never recorded, cached, or seen by the application.
          </span>
        </li>
        <li className="flex items-start gap-2" id="privacy-item-2">
          <KeyRound className="text-sky-400 w-4 h-4 mt-0.5 flex-shrink-0" />
          <span>
            <strong>Cryptographic Evidence Only:</strong> The system validates normalized <code>AMR</code> references transformed through trusted providers or secure hardware enclaves.
          </span>
        </li>
      </ul>
      
      <div className="mt-4 pt-3 border-t border-slate-800 text-xs text-slate-500">
        Governed by Biometric Evidence Privacy Directive (AMR-FPT-2026).
      </div>
    </div>
  );
}
