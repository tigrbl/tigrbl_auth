import React, { useState } from 'react';
import { ShieldCheck, FileText, ChevronRight, HelpCircle } from 'lucide-react';
import { BiometricConsentRecord } from '../types';

interface BiometricConsentProps {
  currentVersion: string;
  onConsentGiven: (record: BiometricConsentRecord) => void;
  onConsentDeclined: (alternative: string) => void;
}

export default function BiometricConsent({
  currentVersion,
  onConsentGiven,
  onConsentDeclined,
}: BiometricConsentProps) {
  const [hasReadPrivacy, setHasReadPrivacy] = useState(false);
  const [hasAgreedRetention, setHasAgreedRetention] = useState(false);
  const [hasAgreedEncryption, setHasAgreedEncryption] = useState(false);
  const [selectedAlternative, setSelectedAlternative] = useState<string>('auth_app');
  const [showAlternativeHelp, setShowAlternativeHelp] = useState(false);

  const isConsentValid = hasReadPrivacy && hasAgreedRetention && hasAgreedEncryption;

  const handleAccept = () => {
    if (!isConsentValid) return;
    const record: BiometricConsentRecord = {
      id: `consent_${Math.random().toString(36).substr(2, 9)}`,
      version: currentVersion,
      timestamp: new Date().toISOString(),
      purpose: 'Establish secure cryptographic biometric authentication credentials tied exclusively to this secure physical verifier.',
      status: 'accepted',
      retentionDays: 180,
      alternativeSelected: null,
    };
    onConsentGiven(record);
  };

  const handleDecline = () => {
    onConsentDeclined(selectedAlternative);
  };

  return (
    <div id="consent-container" className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 max-w-4xl mx-auto shadow-2xl overflow-hidden relative">
      <div className="absolute top-0 right-0 w-64 h-64 bg-emerald-500/5 rounded-full blur-3xl pointer-events-none" />
      <div className="absolute bottom-0 left-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

      {/* Header */}
      <div className="flex items-center gap-4 border-b border-slate-800 pb-6 mb-6">
        <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-emerald-400">
          <ShieldCheck className="w-8 h-8" />
        </div>
        <div>
          <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider">Security Gate</span>
          <h1 className="text-2xl font-semibold text-slate-100 tracking-tight">Biometric Consent & Privacy Declaration</h1>
          <p className="text-sm text-slate-400">Version {currentVersion} • Retina AMR Verification</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Educational Content */}
        <div className="lg:col-span-7 space-y-6">
          <div className="space-y-4 text-slate-300 text-sm leading-relaxed">
            <p>
              To complete highly secure transaction verifications, our system supports 
              <strong> Retina Authentication Method (AMR)</strong>. Retina scanning maps the unique, 
              unchanging blood vessel patterns of your retina. This offers the absolute highest class 
              of biometric assurance available.
            </p>
            
            <div className="bg-slate-950/60 border border-slate-800/80 rounded-xl p-4 space-y-3 font-mono text-xs">
              <div className="flex items-start gap-2 text-cyan-400">
                <FileText className="w-4 h-4 shrink-0 mt-0.5" />
                <span>DATA EXCLUSIVITY & CRYPTOGRAPHIC ZERO-TRUST</span>
              </div>
              <p className="text-slate-400">
                Our first-party retina enrollment performs all templates and match evaluations 
                strictly within the secure enclave of the hardware verifier boundary. 
                <span className="text-emerald-400 font-medium"> RAW IMAGES AND TEMPLATES NEVER LEAVE THE DEVICE.</span> 
                The verifier outputs only a signed cryptographic proof of success, shielding your 
                biometric details from the internet.
              </p>
            </div>
          </div>

          {/* Key Disclosures */}
          <div className="space-y-3">
            <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider">Key Commitments & Rights</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              <div className="bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <p className="text-xs font-semibold text-slate-200">1. Data Minimization</p>
                <p className="text-[11px] text-slate-400 mt-1">No feature vectors, scores, or photos are ever saved in browser storage, logs, or backups.</p>
              </div>
              <div className="bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <p className="text-xs font-semibold text-slate-200">2. Voluntary Enlistment</p>
                <p className="text-[11px] text-slate-400 mt-1">Enrollment is fully optional. If declined, you can still sign in using traditional fallbacks.</p>
              </div>
              <div className="bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <p className="text-xs font-semibold text-slate-200">3. Absolute Erasure</p>
                <p className="text-[11px] text-slate-400 mt-1">You hold the right to revoke consent and trigger immediate, verified template destruction.</p>
              </div>
              <div className="bg-slate-950/40 p-3 rounded-lg border border-slate-800">
                <p className="text-xs font-semibold text-slate-200">4. 180-Day Lifecycle</p>
                <p className="text-[11px] text-slate-400 mt-1">Enrollment templates expire in 180 days and require re-enrollment to continue.</p>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Consent Checkboxes */}
        <div className="lg:col-span-5 bg-slate-950/40 border border-slate-800 rounded-xl p-5 space-y-6">
          <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider border-b border-slate-800 pb-2">Required Agreements</h3>
          
          <div className="space-y-4">
            <label id="checkbox-privacy-label" className="flex items-start gap-3 cursor-pointer group">
              <input
                id="checkbox-privacy"
                type="checkbox"
                checked={hasReadPrivacy}
                onChange={(e) => setHasReadPrivacy(e.target.checked)}
                className="w-4 h-4 mt-0.5 rounded border-slate-700 text-emerald-500 bg-slate-900 focus:ring-emerald-500/20 focus:ring-offset-slate-900 focus:ring-2 animate-pulse"
              />
              <div className="text-xs">
                <p className="font-medium text-slate-200 group-hover:text-emerald-400 transition-colors">I accept the biometric privacy policy</p>
                <p className="text-slate-400 mt-0.5">I have read the policy explaining how retinal vascular patterns are computed local-only.</p>
              </div>
            </label>

            <label id="checkbox-retention-label" className="flex items-start gap-3 cursor-pointer group">
              <input
                id="checkbox-retention"
                type="checkbox"
                checked={hasAgreedRetention}
                onChange={(e) => setHasAgreedRetention(e.target.checked)}
                className="w-4 h-4 mt-0.5 rounded border-slate-700 text-emerald-500 bg-slate-900 focus:ring-emerald-500/20 focus:ring-offset-slate-900 focus:ring-2"
              />
              <div className="text-xs">
                <p className="font-medium text-slate-200 group-hover:text-emerald-400 transition-colors">I approve the 180-day retention limit</p>
                <p className="text-slate-400 mt-0.5">My biometric blueprint will auto-expire in 180 days from enrollment, or upon earlier deletion request.</p>
              </div>
            </label>

            <label id="checkbox-encryption-label" className="flex items-start gap-3 cursor-pointer group">
              <input
                id="checkbox-encryption"
                type="checkbox"
                checked={hasAgreedEncryption}
                onChange={(e) => setHasAgreedEncryption(e.target.checked)}
                className="w-4 h-4 mt-0.5 rounded border-slate-700 text-emerald-500 bg-slate-900 focus:ring-emerald-500/20 focus:ring-offset-slate-900 focus:ring-2"
              />
              <div className="text-xs">
                <p className="font-medium text-slate-200 group-hover:text-emerald-400 transition-colors">I authorize Secure Enclave mapping</p>
                <p className="text-slate-400 mt-0.5">I authorize hardware-level mapping, and understand my raw samples are converted to signatures without server upload.</p>
              </div>
            </label>
          </div>

          <div className="pt-4 border-t border-slate-800 space-y-4">
            <button
              id="btn-consent-accept"
              onClick={handleAccept}
              disabled={!isConsentValid}
              className={`w-full py-2.5 px-4 rounded-lg font-mono text-xs font-semibold uppercase tracking-wider flex items-center justify-center gap-2 transition-all duration-200 ${
                isConsentValid
                  ? 'bg-emerald-500 hover:bg-emerald-400 text-slate-950 shadow-lg shadow-emerald-500/10 cursor-pointer'
                  : 'bg-slate-800 text-slate-500 border border-slate-700/50 cursor-not-allowed'
              }`}
            >
              <span>Accept & Proceed to Preflight</span>
              <ChevronRight className="w-4 h-4" />
            </button>

            <div className="relative border border-dashed border-slate-800 rounded-lg p-3 bg-slate-950/20">
              <div className="flex justify-between items-center mb-2">
                <span className="text-[10px] font-mono text-slate-400">OR DECLINE AND USE FALLBACK:</span>
                <button
                  id="btn-alternative-help"
                  type="button"
                  onClick={() => setShowAlternativeHelp(!showAlternativeHelp)}
                  className="text-slate-400 hover:text-slate-200"
                >
                  <HelpCircle className="w-3.5 h-3.5" />
                </button>
              </div>

              {showAlternativeHelp && (
                <p className="text-[10px] text-cyan-400 font-mono mb-2">
                  Declining the retina method routes your authentication through a fallback factor. 
                  No penalty or restriction applies other than meeting company compliance policies.
                </p>
              )}

              <select
                id="select-alternative-factor"
                value={selectedAlternative}
                onChange={(e) => setSelectedAlternative(e.target.value)}
                className="w-full bg-slate-900 text-slate-200 border border-slate-800 rounded px-2.5 py-1.5 text-xs font-mono focus:border-cyan-500 focus:outline-none"
              >
                <option value="auth_app">Authenticator App (TOTP Code)</option>
                <option value="hardware_key">FIDO2 Hardware Key (WebAuthn / YubiKey)</option>
                <option value="supervised_recovery">Supervised Operator Recovery Session</option>
              </select>

              <button
                id="btn-consent-decline"
                onClick={handleDecline}
                className="w-full mt-2.5 py-1.5 px-3 rounded bg-red-950/30 hover:bg-red-950/50 border border-red-900/40 hover:border-red-900/80 text-red-400 font-mono text-xs font-semibold uppercase tracking-wider transition-colors cursor-pointer"
              >
                Decline & Use Alternative
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
