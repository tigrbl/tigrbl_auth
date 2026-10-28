import React, { useState } from 'react';
import { ShieldCheck, Info, CheckCircle2, ChevronRight, Scale, FileText, AlertCircle } from 'lucide-react';

interface VoiceConsentRecordProps {
  onConsentGranted: (signerName: string, consentVersion: string) => void;
  onConsentDeclined: () => void;
  initialSignerName?: string;
  consentVersion?: string;
}

export default function VoiceConsentRecord({
  onConsentGranted,
  onConsentDeclined,
  initialSignerName = '',
  consentVersion = 'v1.4-VBM-PRIVACY',
}: VoiceConsentRecordProps) {
  const [signerName, setSignerName] = useState(initialSignerName);
  const [checkedClauses, setCheckedClauses] = useState({
    processing: false,
    retention: false,
    revocation: false,
    alternatives: false,
  });
  const [activeTab, setActiveTab] = useState<'summary' | 'legal'>('summary');
  const [error, setError] = useState('');

  const allChecked = Object.values(checkedClauses).every(Boolean);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!allChecked) {
      setError('Please read and acknowledge all compliance and privacy clauses below.');
      return;
    }
    if (!signerName.trim()) {
      setError('Electronic signature required. Please type your full legal name.');
      return;
    }
    setError('');
    onConsentGranted(signerName.trim(), consentVersion);
  };

  const toggleClause = (key: keyof typeof checkedClauses) => {
    setCheckedClauses((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-2xl mx-auto" id="consent-container">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-xl">
            <ShieldCheck className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-sans font-semibold tracking-tight text-slate-100 text-lg">Biometric Consent & Disclosure</h3>
            <p className="font-mono text-xs text-slate-400">AMR: vbm | Version {consentVersion}</p>
          </div>
        </div>
        <div className="flex bg-slate-950/60 p-0.5 rounded-lg border border-slate-800 text-xs">
          <button
            type="button"
            onClick={() => setActiveTab('summary')}
            className={`px-3 py-1.5 rounded-md transition-colors ${
              activeTab === 'summary' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            Summary
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('legal')}
            className={`px-3 py-1.5 rounded-md transition-colors ${
              activeTab === 'legal' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            Legal Terms
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="p-6 space-y-6">
        {/* Main Info */}
        {activeTab === 'summary' ? (
          <div className="space-y-4">
            <div className="bg-slate-950/40 border border-slate-800 p-4 rounded-xl flex gap-3 text-slate-300 text-sm leading-relaxed">
              <Info className="w-5 h-5 text-emerald-400 shrink-0 mt-0.5" />
              <div>
                <span className="font-semibold text-slate-100">Why does this app use Voice Biometrics?</span>
                <p className="mt-1 text-slate-400 text-xs">
                  Voice Biometrics (`vbm`) converts the physical qualities of your speech into a mathematical voice vector (template). It protects against phishing and credential stuffing with high liveness detection parameters.
                </p>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
              <div className="bg-slate-950/20 border border-slate-800/60 p-3 rounded-xl">
                <span className="font-semibold text-slate-200 block mb-1">🔐 Secure Vectors Only</span>
                <p className="text-slate-400">Raw audio recordings are parsed inside a transient sandbox and deleted immediately. We store only mathematical vectors—never your raw voice file.</p>
              </div>
              <div className="bg-slate-950/20 border border-slate-800/60 p-3 rounded-xl">
                <span className="font-semibold text-slate-200 block mb-1">⏱️ 180-Day Lifecycle</span>
                <p className="text-slate-400">Templates automatically expire or delete after 180 days of non-usage or immediately upon explicit withdrawal/revocation requests.</p>
              </div>
            </div>
          </div>
        ) : (
          <div className="max-h-56 overflow-y-auto bg-slate-950 border border-slate-800 p-4 rounded-xl space-y-4 text-xs text-slate-400 leading-relaxed font-mono">
            <div className="flex gap-2 items-start border-b border-slate-900 pb-3">
              <Scale className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-300">1. Compliance & Authority</strong>
                <p className="mt-1">
                  This Consent governs the collection and use of biometric identifiers under the Illinois Biometric Information Privacy Act (BIPA), Texas CIPA, Washington H.B. 1493, and EU GDPR.
                </p>
              </div>
            </div>
            <div className="flex gap-2 items-start border-b border-slate-900 pb-3">
              <FileText className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-300">2. Processing Sandboxing</strong>
                <p className="mt-1">
                  Audio signals are sampled on-device via WebAudio APIs, secured using TLS, and analyzed in real-time within the isolated region of the SentryVoice Verifier. Feature extraction vectors are generated and encrypted at rest with AES-256 GCM.
                </p>
              </div>
            </div>
            <div className="flex gap-2 items-start">
              <CheckCircle2 className="w-4 h-4 text-slate-500 shrink-0 mt-0.5" />
              <div>
                <strong className="text-slate-300">3. Non-Transferability</strong>
                <p className="mt-1">
                  We guarantee zero-sharing of biometric data with third parties, brokers, or training algorithms. Biometric data is stored solely for authenticating your user identity for your chosen scope of actions.
                </p>
              </div>
            </div>
          </div>
        )}

        {/* Declarative Consent Items */}
        <div className="space-y-3">
          <h4 className="font-sans text-xs font-semibold text-slate-300 uppercase tracking-wider">Required Compliance Checklist</h4>
          
          <label className="flex items-start gap-3 bg-slate-950/30 hover:bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 transition-colors cursor-pointer group">
            <input
              type="checkbox"
              checked={checkedClauses.processing}
              onChange={() => toggleClause('processing')}
              className="mt-0.5 accent-emerald-500 h-4 w-4 rounded text-emerald-500 border-slate-800 bg-slate-900"
              id="chk-consent-processing"
            />
            <div className="text-xs">
              <span className="font-semibold text-slate-200 group-hover:text-slate-100 transition-colors">I consent to voice biometric processing</span>
              <p className="text-slate-400 mt-0.5">I permit the collection, extraction, and generation of a mathematical voice template from my spoken words to enable passwordless logins.</p>
            </div>
          </label>

          <label className="flex items-start gap-3 bg-slate-950/30 hover:bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 transition-colors cursor-pointer group">
            <input
              type="checkbox"
              checked={checkedClauses.retention}
              onChange={() => toggleClause('retention')}
              className="mt-0.5 accent-emerald-500 h-4 w-4 rounded text-emerald-500 border-slate-800 bg-slate-900"
              id="chk-consent-retention"
            />
            <div className="text-xs">
              <span className="font-semibold text-slate-200 group-hover:text-slate-100 transition-colors">I acknowledge the retention and security policy</span>
              <p className="text-slate-400 mt-0.5">I agree that my voice biometric template will be stored securely for up to 180 days of inactivity, after which it is subject to automatic permanent purge.</p>
            </div>
          </label>

          <label className="flex items-start gap-3 bg-slate-950/30 hover:bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 transition-colors cursor-pointer group">
            <input
              type="checkbox"
              checked={checkedClauses.revocation}
              onChange={() => toggleClause('revocation')}
              className="mt-0.5 accent-emerald-500 h-4 w-4 rounded text-emerald-500 border-slate-800 bg-slate-900"
              id="chk-consent-revocation"
            />
            <div className="text-xs">
              <span className="font-semibold text-slate-200 group-hover:text-slate-100 transition-colors">I understand my revocation and deletion rights</span>
              <p className="text-slate-400 mt-0.5">I know I can delete my biometric record and revoke this consent instantly inside my account dashboard, which initiates a hard purge from the verifier database.</p>
            </div>
          </label>

          <label className="flex items-start gap-3 bg-slate-950/30 hover:bg-slate-950/60 p-3 rounded-xl border border-slate-800/80 transition-colors cursor-pointer group">
            <input
              type="checkbox"
              checked={checkedClauses.alternatives}
              onChange={() => toggleClause('alternatives')}
              className="mt-0.5 accent-emerald-500 h-4 w-4 rounded text-emerald-500 border-slate-800 bg-slate-900"
              id="chk-consent-alternatives"
            />
            <div className="text-xs">
              <span className="font-semibold text-slate-200 group-hover:text-slate-100 transition-colors">I recognize speech/accessibility alternatives</span>
              <p className="text-slate-400 mt-0.5">I am aware that enrolling is entirely voluntary and that secure alternative sign-in options (such as FIDO passkeys, PINs, or tokens) are available unconditionally.</p>
            </div>
          </label>
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs px-4 py-3 rounded-xl flex items-center gap-2">
            <AlertCircle className="w-4 h-4 shrink-0" />
            <span>{error}</span>
          </div>
        )}

        {/* Signature Box */}
        <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-3">
          <div>
            <label className="block text-xs font-mono text-slate-400 uppercase tracking-wider mb-1">
              Electronic Signature (Type Full Name)
            </label>
            <input
              type="text"
              value={signerName}
              onChange={(e) => setSignerName(e.target.value)}
              placeholder="e.g. Jean-Luc Picard"
              className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-sm text-slate-100 focus:outline-none focus:border-emerald-500 transition-colors placeholder:text-slate-600 font-sans"
              id="input-consent-signature"
            />
          </div>
          <p className="text-[10px] text-slate-500 leading-tight">
            By typing my name, checking the boxes above, and clicking &ldquo;Accept and Continue,&rdquo; I verify my identity, authorize biometric processing as described, and provide an electronic signature equivalent to a wet signature.
          </p>
        </div>

        {/* Action Controls */}
        <div className="flex gap-3 justify-end pt-2 border-t border-slate-800">
          <button
            type="button"
            onClick={onConsentDeclined}
            className="px-4 py-2 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 rounded-lg text-sm transition-all"
            id="btn-consent-decline"
          >
            Decline
          </button>
          <button
            type="submit"
            disabled={!allChecked || !signerName.trim()}
            className={`px-5 py-2 rounded-lg text-sm font-medium transition-all flex items-center gap-1.5 ${
              allChecked && signerName.trim()
                ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/10 hover:bg-emerald-400'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
            id="btn-consent-accept"
          >
            <span>Accept & Continue</span>
            <ChevronRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
