import React from 'react';
import { Shield, Eye, HelpCircle, AlertCircle, RefreshCw, KeyRound, ArrowRight } from 'lucide-react';

interface LocationConsentPanelProps {
  purpose: string;
  requiredAccuracy: number; // meters
  retentionNotice: string;
  onConsentGranted: () => void;
  onConsentDeclined: () => void;
  isEvaluating: boolean;
  alternativeMethod: string;
}

export const LocationConsentPanel: React.FC<LocationConsentPanelProps> = ({
  purpose,
  requiredAccuracy,
  retentionNotice,
  onConsentGranted,
  onConsentDeclined,
  isEvaluating,
  alternativeMethod
}) => {
  return (
    <div id="consent-panel" className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden max-w-md w-full mx-auto" role="region" aria-labelledby="consent-title">
      <div className="bg-slate-50 border-b border-slate-100 p-5">
        <div className="flex items-start gap-3">
          <div className="p-2 bg-indigo-50 border border-indigo-100 text-indigo-600 rounded-lg">
            <Shield className="w-5 h-5" />
          </div>
          <div>
            <h3 id="consent-title" className="text-base font-semibold text-slate-900 font-display">
              Location Verification Consent
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Secure Context Evidence (AMR: geo)
            </p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-5">
        {/* Purpose Card */}
        <div className="space-y-1">
          <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
            Verification Purpose
          </span>
          <p className="text-sm text-slate-700 leading-relaxed font-medium">
            {purpose}
          </p>
        </div>

        {/* Technical Requirements */}
        <div className="grid grid-cols-2 gap-4 pt-2">
          <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Required Precision
            </span>
            <div className="flex items-center gap-1.5">
              <span className="text-xs font-semibold text-slate-800">
                &lt; {requiredAccuracy} meters
              </span>
              <span className="inline-flex px-1.5 py-0.5 text-[9px] font-bold bg-indigo-100 text-indigo-800 rounded uppercase">
                Precise
              </span>
            </div>
          </div>

          <div className="bg-slate-50 rounded-lg p-3 border border-slate-100">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Retention Policy
            </span>
            <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-800">
              <Eye className="w-3.5 h-3.5 text-slate-400" />
              <span>{retentionNotice}</span>
            </div>
          </div>
        </div>

        {/* Privacy Protection Statement */}
        <div className="bg-emerald-50/50 border border-emerald-100 rounded-lg p-3.5 flex gap-3 text-xs leading-normal">
          <Shield className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
          <div className="text-emerald-800">
            <strong className="font-semibold block mb-0.5">Privacy First Protection</strong>
            Your exact coordinates are processed inside a server-side cryptographically secure envelope. Real-time locations are never permanently logged or shared with third parties.
          </div>
        </div>

        {/* Warning about OS Prompts */}
        <div className="text-[11px] text-slate-500 flex items-start gap-2 bg-amber-50/40 border border-amber-100/50 rounded-lg p-3">
          <AlertCircle className="w-4 h-4 text-amber-500 mt-0.5 shrink-0" />
          <span>
            Clicking share will prompt your browser or operating system for device location permissions. We will evaluate the hardware signal for freshness and spoof prevention.
          </span>
        </div>
      </div>

      <div className="bg-slate-50 px-6 py-4 border-t border-slate-100 flex flex-col gap-2">
        <button
          id="btn-share-location"
          onClick={onConsentGranted}
          disabled={isEvaluating}
          className="w-full bg-primary-600 hover:bg-primary-700 active:bg-primary-700 text-white font-medium py-2.5 px-4 rounded-lg text-sm transition-all shadow-sm flex items-center justify-center gap-2 disabled:opacity-70 disabled:cursor-not-allowed"
        >
          {isEvaluating ? (
            <>
              <RefreshCw className="w-4 h-4 animate-spin" />
              <span>Acquiring GPS Signal...</span>
            </>
          ) : (
            <>
              <span>Share Location & Continue</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>

        <button
          id="btn-fallback-method"
          onClick={onConsentDeclined}
          disabled={isEvaluating}
          className="w-full bg-white hover:bg-slate-50 active:bg-slate-100 border border-slate-200 text-slate-700 font-medium py-2 px-4 rounded-lg text-xs transition-all flex items-center justify-center gap-1.5 disabled:opacity-50"
        >
          <KeyRound className="w-3.5 h-3.5 text-slate-400" />
          <span>Use Alternative: {alternativeMethod}</span>
        </button>
      </div>
    </div>
  );
};
