import React from 'react';
import { Shield, Check, Award, Lock } from 'lucide-react';

interface CeremonyShellProps {
  title: string;
  subtitle?: string;
  steps: string[];
  currentStep: number; // 0-indexed
  children: React.ReactNode;
  isSimulatingNativeAuth?: boolean;
  onSimulateAuthSuccess?: () => void;
  onSimulateAuthFail?: () => void;
}

export default function CeremonyShell({
  title,
  subtitle,
  steps,
  currentStep,
  children,
  isSimulatingNativeAuth = false,
  onSimulateAuthSuccess,
  onSimulateAuthFail,
}: CeremonyShellProps) {
  return (
    <div id="ceremony-shell" className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden relative">
      {/* Decorative top accent */}
      <div className="bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 h-1.5 w-full" />

      {/* Header */}
      <div className="px-6 py-5 border-b border-slate-100 bg-slate-50/50 flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div className="space-y-1">
          <div className="flex items-center gap-2">
            <div className="p-1.5 bg-indigo-50 text-indigo-600 rounded-lg shrink-0">
              <Shield className="w-4 h-4" />
            </div>
            <h3 className="font-bold text-slate-900 text-lg tracking-tight leading-none">{title}</h3>
          </div>
          {subtitle && <p className="text-xs text-slate-500 pl-8 leading-relaxed">{subtitle}</p>}
        </div>

        {/* Step Indicators */}
        <div className="flex items-center gap-1.5 text-xs font-semibold pl-8 md:pl-0">
          <span className="text-slate-400">Step</span>
          <span className="text-indigo-600 font-bold bg-indigo-50 px-2 py-0.5 rounded-full">
            {currentStep + 1}
          </span>
          <span className="text-slate-400">of</span>
          <span className="text-slate-700 font-bold bg-slate-100 px-2 py-0.5 rounded-full">
            {steps.length}
          </span>
        </div>
      </div>

      {/* Steps horizontal list */}
      <div className="px-6 py-3 border-b border-slate-100 bg-slate-50/20 hidden md:flex items-center justify-between gap-2 overflow-x-auto">
        {steps.map((step, idx) => {
          const isDone = idx < currentStep;
          const isCurrent = idx === currentStep;

          return (
            <div key={idx} className="flex items-center gap-2 text-xs font-semibold whitespace-nowrap">
              <div className={`w-5 h-5 rounded-full flex items-center justify-center text-[10px] ${
                isDone
                  ? 'bg-emerald-500 text-white'
                  : isCurrent
                  ? 'bg-indigo-600 text-white ring-4 ring-indigo-50 shadow'
                  : 'bg-slate-100 text-slate-400'
              }`}>
                {isDone ? <Check className="w-3 h-3" /> : idx + 1}
              </div>
              <span className={isCurrent ? 'text-indigo-600 font-bold' : isDone ? 'text-slate-700' : 'text-slate-400'}>
                {step}
              </span>
              {idx < steps.length - 1 && <span className="text-slate-200">→</span>}
            </div>
          );
        })}
      </div>

      {/* Main Form/Content Frame */}
      <div className="p-6">
        {children}
      </div>

      {/* Embedded Native Authentication Prompt Simulator Modal */}
      {isSimulatingNativeAuth && (
        <div id="native-auth-overlay" className="absolute inset-0 bg-slate-900/40 backdrop-blur-xs flex items-center justify-center p-4 z-50">
          <div className="bg-white border border-slate-200/80 rounded-2xl shadow-2xl max-w-sm w-full overflow-hidden animate-in fade-in zoom-in duration-200 text-center p-6 space-y-4">
            <div className="mx-auto w-12 h-12 bg-slate-900 text-slate-200 rounded-full flex items-center justify-center shadow-lg">
              <Lock className="w-5 h-5" />
            </div>

            <div className="space-y-1">
              <h4 className="font-bold text-slate-800 text-base">Key Authorization Required</h4>
              <p className="text-xs text-slate-500 leading-relaxed px-2">
                Your operating system is prompting authorization to sign with your software-secured cryptographic key.
              </p>
            </div>

            {/* Simulated Fingerprint / PIN */}
            <div className="bg-slate-50 border border-slate-100 rounded-xl p-3.5 space-y-2 text-left">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wide">Secure Prompt Detail</div>
              <div className="text-xs text-slate-700 font-medium">Application: <span className="font-mono text-slate-900 bg-slate-200 px-1 rounded">SWK_AMR_Portal</span></div>
              <div className="text-xs text-slate-700 font-medium">Action: <span className="font-semibold text-indigo-700">ECDSA-ES256 Private-Key Signature</span></div>
            </div>

            <div className="flex gap-2.5 pt-2">
              <button
                type="button"
                id="btn-simulate-auth-fail"
                onClick={onSimulateAuthFail}
                className="flex-1 bg-slate-100 hover:bg-slate-200 text-slate-700 py-2 px-3 rounded-lg text-xs font-semibold transition-colors cursor-pointer"
              >
                Deny Prompt
              </button>
              <button
                type="button"
                id="btn-simulate-auth-success"
                onClick={onSimulateAuthSuccess}
                className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-2 px-3 rounded-lg text-xs font-semibold transition-colors shadow-sm cursor-pointer"
              >
                Authorize OK
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
