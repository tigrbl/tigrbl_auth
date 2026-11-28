import React from 'react';
import { BiometricPrivacyNotice } from './';
import { HelpCircle, Key, Laptop, Tablet, Smartphone, ShieldCheck, AlertTriangle, Cpu, RefreshCw } from 'lucide-react';

interface EvidenceDetailPanelProps {
  sessionEvidence: {
    isAuthenticated: boolean;
    hasFpt: boolean;
    isTrusted: boolean;
    detectedAmrs: string[];
    provider: string;
    authTime: string;
    freshnessSeconds: number;
    uvFlag: boolean;
    directVsTransformed: 'direct' | 'transformed' | 'none';
  };
  linkedAuthenticators: Array<{
    id: string;
    name: string;
    type: string;
    enrolledAt: string;
    lastUsedAt: string;
    backupEligible: boolean;
  }>;
  onRefreshEvidence: () => void;
}

export default function EvidenceDetailPanel({ sessionEvidence, linkedAuthenticators, onRefreshEvidence }: EvidenceDetailPanelProps) {
  return (
    <div className="space-y-6" id="evidence-detail-view">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
            <Cpu className="text-sky-400 w-5 h-5" />
            Session Evidence & Authenticator Registry
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Review normalized verification signals linked to the current active environment.
          </p>
        </div>

        {sessionEvidence.isAuthenticated && (
          <button 
            onClick={onRefreshEvidence}
            className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs font-medium text-slate-300 rounded-lg transition"
          >
            <RefreshCw className="w-3 h-3 text-sky-400" />
            Refresh Freshness
          </button>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Session Evidence Card */}
        <div className="lg:col-span-7 bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4">
          <div className="border-b border-slate-900 pb-3 flex justify-between items-center">
            <h3 className="font-semibold text-slate-200 text-sm">Active Session Proof</h3>
            {sessionEvidence.isAuthenticated ? (
              <span className="bg-sky-950 text-sky-400 border border-sky-900/60 text-2xs px-2.5 py-0.5 rounded-full font-mono uppercase">
                Active Session
              </span>
            ) : (
              <span className="bg-slate-900 text-slate-500 text-2xs px-2.5 py-0.5 rounded-full font-mono uppercase">
                Unauthenticated
              </span>
            )}
          </div>

          {!sessionEvidence.isAuthenticated ? (
            <div className="h-48 flex flex-col items-center justify-center text-center p-4">
              <AlertTriangle className="text-amber-500 w-8 h-8 mb-2" />
              <p className="text-xs font-medium text-slate-400">No Active Session Evidence</p>
              <p className="text-2xs text-slate-600 mt-1 max-w-sm">
                Run a credential ceremony inside the "Ceremony Sandbox" tab first to generate and transform security evidence.
              </p>
            </div>
          ) : (
            <div className="space-y-4">
              {/* Dynamic Headline Based on Evidence Normalized Trust */}
              <div className={`p-4 rounded-xl border flex gap-3 ${
                sessionEvidence.hasFpt && sessionEvidence.isTrusted
                  ? 'bg-emerald-950/20 border-emerald-900/50'
                  : 'bg-amber-950/20 border-amber-900/50'
              }`}>
                {sessionEvidence.hasFpt && sessionEvidence.isTrusted ? (
                  <>
                    <ShieldCheck className="text-emerald-400 w-5 h-5 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-xs font-semibold text-emerald-300">Fingerprint Evidence: Verified</h4>
                      <p className="text-2xs text-slate-400 mt-1 leading-relaxed">
                        A certified native verifier or transformed provider has submitted verified evidence that a fingerprint sensor was physically engaged.
                      </p>
                    </div>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="text-amber-400 w-5 h-5 flex-shrink-0 mt-0.5" />
                    <div>
                      <h4 className="text-xs font-semibold text-amber-300">User Verified; Method Not Disclosed</h4>
                      <p className="text-2xs text-slate-400 mt-1 leading-relaxed">
                        WebAuthn User Verification (UV) succeeded. However, standard WebAuthn does not prove a fingerprint sensor was used. This credential represents generic secure lock screen authentication.
                      </p>
                    </div>
                  </>
                )}
              </div>

              {/* Data List for Audit Details */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-x-4 gap-y-3 font-mono text-xs border-t border-slate-900 pt-4">
                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Provenance Source:</span>
                  <span className="text-slate-300 font-semibold">{sessionEvidence.provider}</span>
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Normalized AMRs:</span>
                  <span className="text-slate-300 font-semibold">
                    [{sessionEvidence.detectedAmrs.join(', ')}]
                  </span>
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Direct vs Transformed:</span>
                  <span className="text-indigo-400 capitalize">{sessionEvidence.directVsTransformed}</span>
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Evidence Freshness:</span>
                  <span className="text-slate-300">{sessionEvidence.freshnessSeconds}s ago</span>
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Ceremony Timestamp:</span>
                  <span className="text-slate-300 text-2xs">{sessionEvidence.authTime}</span>
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">User Verification Flag (UV):</span>
                  <span className="text-emerald-400 font-bold">{sessionEvidence.uvFlag ? "TRUE" : "FALSE"}</span>
                </div>
              </div>
            </div>
          )}

          <div className="pt-4 border-t border-slate-900">
            <BiometricPrivacyNotice />
          </div>
        </div>

        {/* Linked Authenticators & Template Management Warning */}
        <div className="lg:col-span-5 bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4">
          <div className="border-b border-slate-900 pb-3">
            <h3 className="font-semibold text-slate-200 text-sm">Linked Authenticators</h3>
            <p className="text-xs text-slate-500 mt-1">
              Registered keys capable of satisfying passwordless prompts.
            </p>
          </div>

          <div className="space-y-3">
            {linkedAuthenticators.map((auth) => (
              <div key={auth.id} className="bg-slate-900/60 border border-slate-850 p-3 rounded-lg flex items-start gap-3">
                <div className="bg-slate-950 p-2 border border-slate-800 rounded">
                  {auth.type === 'laptop' && <Laptop className="w-4 h-4 text-sky-400" />}
                  {auth.type === 'tablet' && <Tablet className="w-4 h-4 text-emerald-400" />}
                  {auth.type === 'phone' && <Smartphone className="w-4 h-4 text-violet-400" />}
                </div>
                
                <div className="flex-1 min-w-0">
                  <div className="flex justify-between items-start">
                    <h4 className="font-semibold text-slate-200 text-xs truncate">{auth.name}</h4>
                    {auth.backupEligible && (
                      <span className="text-3xs text-slate-500 border border-slate-800 px-1 rounded uppercase font-mono">
                        Backup Eligible
                      </span>
                    )}
                  </div>
                  <p className="text-3xs text-slate-500 font-mono mt-1">
                    Enrolled: {new Date(auth.enrolledAt).toLocaleDateString()}
                  </p>
                  <p className="text-3xs text-indigo-400/90 font-mono mt-0.5">
                    Last Ceremony: {new Date(auth.lastUsedAt).toLocaleTimeString()}
                  </p>
                </div>
              </div>
            ))}
          </div>

          {/* Critical Security & Privacy Warning */}
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-4 space-y-2.5">
            <span className="text-2xs text-amber-500 font-semibold uppercase tracking-wider flex items-center gap-1">
              <AlertTriangle className="w-4 h-4 text-amber-500" />
              Sensor Template Disclaimer
            </span>
            <p className="text-3xs text-slate-400 leading-normal">
              You <strong>cannot manage or review biometric fingerprint templates</strong> in this panel. Fingerprint enrollment and template storage are handled exclusively by your machine’s secure hardware (e.g. Apple Secure Enclave or Android Titan M chip).
            </p>
            <p className="text-3xs text-slate-400 leading-normal">
              To enroll a new device biometric or delete a credential, please use your Operating System's native Settings app (TouchID / Windows Hello / Face Unlock).
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
