/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { CeremonyContext, FaceAuthenticator, BiometricEvidence } from '../types';
import { BiometricPrivacyNotice } from './BiometricPrivacyNotice';
import { FaceCapturePreflight } from './FaceCapturePreflight';
import { FaceCaptureShell } from './FaceCaptureShell';
import { BiometricEvidenceQualifier } from './BiometricEvidenceQualifier';
import { EvidenceProvenancePanel } from './EvidenceProvenancePanel';
import { ShieldCheck, Info, Key, ExternalLink, HelpCircle, CheckCircle, RefreshCw, AlertTriangle, AlertOctagon, Undo2, ArrowRight } from 'lucide-react';

interface ActiveCeremonyWizardProps {
  onAddAuthenticator: (newAuth: FaceAuthenticator) => void;
  onLogAudit: (event: string, category: any, status: 'success' | 'failure' | 'warning', details: string, amr?: string, provenance?: string) => void;
  onSetVerifiedEvidence: (evidence: BiometricEvidence | null) => void;
  policyAllowFirstParty: boolean;
  policyAllowFederated: boolean;
}

export const ActiveCeremonyWizard: React.FC<ActiveCeremonyWizardProps> = ({
  onAddAuthenticator,
  onLogAudit,
  onSetVerifiedEvidence,
  policyAllowFirstParty,
  policyAllowFederated
}) => {
  const [ceremonyType, setCeremonyType] = useState<'enrollment' | 'login' | 'none'>('none');
  const [step, setStep] = useState<number>(1);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [isSpoofDetected, setIsSpoofDetected] = useState(false);
  const [authLabel, setAuthLabel] = useState('My Work Station - Face Authenticator');
  const [consentVersion, setConsentVersion] = useState('');
  
  // Active enrollment template preview (Section 5.1.9)
  const [enrolledTemplate, setEnrolledTemplate] = useState<FaceAuthenticator | null>(null);

  // Active verified evidence output
  const [emittedEvidence, setEmittedEvidence] = useState<BiometricEvidence | null>(null);

  // Passkey Assertion state
  const [passkeyState, setPasskeyState] = useState<'idle' | 'awaiting' | 'verified_uv' | 'verified_face'>('idle');

  // Federation redirect progress state
  const [federatedState, setFederatedState] = useState<'idle' | 'redirecting' | 'callback' | 'completed'>('idle');
  const [selectedFederatedProvider, setSelectedFederatedProvider] = useState<string>('');

  const resetCeremony = () => {
    setCeremonyType('none');
    setStep(1);
    setErrorMsg(null);
    setIsSpoofDetected(false);
    setEnrolledTemplate(null);
    setEmittedEvidence(null);
    setPasskeyState('idle');
    setFederatedState('idle');
  };

  const startCeremony = (type: 'enrollment' | 'login') => {
    setCeremonyType(type);
    setStep(1);
    setErrorMsg(null);
    setIsSpoofDetected(false);
    setEnrolledTemplate(null);
    setEmittedEvidence(null);
    setPasskeyState('idle');
    setFederatedState('idle');
  };

  // --- ENROLLMENT STEPS HANDLERS ---
  const handleConsentAccepted = (version: string) => {
    setConsentVersion(version);
    setStep(2); // Advance to Preflight Compatibility
    onLogAudit('Biometric Privacy Consent Accepted', 'consent', 'success', `User accepted biometric consent version ${version}.`);
  };

  const handlePreflightCompleted = () => {
    setStep(3); // Advance to Active Capture
    onLogAudit('Biometric Preflight Completed', 'enrollment', 'success', 'All device sensory capabilities and enclave tunnels validated.');
  };

  const handlePreflightFailed = (reason: string) => {
    setErrorMsg(reason);
    onLogAudit('Biometric Preflight Blocked', 'enrollment', 'warning', `Preflight failed: ${reason}`);
  };

  const handleCaptureSuccess = (evidenceData: any) => {
    // Generate new secure authenticator mock template
    const newAuth: FaceAuthenticator = {
      id: `auth-${Math.floor(Math.random() * 90000) + 10000}`,
      label: authLabel,
      status: 'active',
      verifierProfile: 'verifier-f1-secure-v2',
      createdDate: new Date().toISOString(),
      lastUsedDate: new Date().toISOString(),
      consentVersion: consentVersion,
      consentDate: new Date().toISOString(),
      retentionPolicy: 'Local verifier enclave partition. Purged 24 hours after deletion activation.',
      recoveryPostured: true,
      recoveryMethod: 'Hardware Security Key (YubiKey)',
      deviceProjection: 'Enterprise Laptop Enclave Terminal'
    };

    setEnrolledTemplate(newAuth);
    setStep(4); // Advance to Activation Review
    onLogAudit(
      'Biometric Enrollment Verified', 
      'enrollment', 
      'success', 
      `Facial presentation liveness approved. Biometric template reference created safely.`,
      'face',
      'face_verified'
    );
  };

  const handleCaptureFailure = (reason: string, isSpoof: boolean) => {
    setErrorMsg(reason);
    setIsSpoofDetected(isSpoof);
    onLogAudit(
      isSpoof ? 'Biometric Spoof Attempt Suspected' : 'Biometric Capture Quality Failed',
      'enrollment',
      isSpoof ? 'warning' : 'warning',
      `Capture failed: ${reason}`
    );
  };

  const activateAuthenticator = () => {
    if (enrolledTemplate) {
      onAddAuthenticator(enrolledTemplate);
      onLogAudit(
        'Authenticator Active', 
        'lifecycle', 
        'success', 
        `Face Authenticator "${enrolledTemplate.label}" has been officially activated.`
      );
      setStep(5); // Completion Screen
    }
  };

  // --- VERIFICATION (LOGIN/STEP-UP) HANDLERS ---
  const handleDirectFaceVerified = (evidenceData: any) => {
    // Create face_verified evidence
    const evidence: BiometricEvidence = {
      amr: 'face',
      provenance: 'face_verified',
      issuer: 'approved-native-enclave-v4',
      verificationTime: new Date().toISOString(),
      freshnessSeconds: 1,
      confidenceRating: 'high_attested',
      isHardwareBacked: true,
      isLivenessProtected: true,
      auditReference: `aud-ev-direct-${Math.random().toString(36).substring(7)}`,
      redactedRawClaims: {}
    };

    setEmittedEvidence(evidence);
    onSetVerifiedEvidence(evidence);
    setStep(3); // Success Screen
    onLogAudit(
      'Biometric Evidence Emitted', 
      'authentication', 
      'success', 
      'Direct Face authenticator successfully validated and active evidence generated.',
      'face',
      'face_verified'
    );
  };

  // WebAuthn Passkey Simulator (Section 5.4)
  const triggerPasskeyAssertion = (withModality: 'uv' | 'face') => {
    setPasskeyState('awaiting');
    onLogAudit('WebAuthn Assertion Initialized', 'authentication', 'info', 'Awaiting system browser WebAuthn prompt gesture...');
    
    setTimeout(() => {
      if (withModality === 'face') {
        setPasskeyState('verified_face');
        const evidence: BiometricEvidence = {
          amr: 'face',
          provenance: 'upstream_face_trusted',
          issuer: 'FIDO2-Authenticator-Hardware-Profile',
          verificationTime: new Date().toISOString(),
          freshnessSeconds: 2,
          confidenceRating: 'high_attested',
          isHardwareBacked: true,
          isLivenessProtected: true,
          auditReference: `aud-webauthn-${Math.random().toString(36).substring(7)}`,
          redactedRawClaims: {}
        };
        setEmittedEvidence(evidence);
        onSetVerifiedEvidence(evidence);
        setStep(3); // Success Screen
        onLogAudit(
          'FIDO2 Assertion Authenticated',
          'authentication',
          'success',
          'Passkey signature verified with attested face biometric modality mapping.',
          'face',
          'upstream_face_trusted'
        );
      } else {
        setPasskeyState('verified_uv');
        // WebAuthn UV returns ONLY general user verification, NOT face evidence directly
        const evidence: BiometricEvidence = {
          amr: 'uv',
          provenance: 'user_verified_modality_unknown',
          issuer: 'Browser-WebAuthn-Generic-Key',
          verificationTime: new Date().toISOString(),
          freshnessSeconds: 3,
          confidenceRating: 'medium_reported',
          isHardwareBacked: false,
          isLivenessProtected: false,
          auditReference: `aud-webauthn-uv-${Math.random().toString(36).substring(7)}`,
          redactedRawClaims: {}
        };
        setEmittedEvidence(evidence);
        onSetVerifiedEvidence(evidence);
        setStep(3); // Success Screen
        onLogAudit(
          'FIDO2 User Verification Received',
          'authentication',
          'success',
          'Passkey signature validated. Modality unknown (uv flag processed). Generic authentication established.',
          'uv',
          'user_verified_modality_unknown'
        );
      }
    }, 1800);
  };

  // Federated IDP Redirect flow (Section 5.5)
  const triggerFederatedRedirect = (providerName: string) => {
    setSelectedFederatedProvider(providerName);
    setFederatedState('redirecting');
    onLogAudit(
      'Federated Auth Redirected',
      'authentication',
      'info',
      `Control handoff to configured provider: ${providerName}. Transaction boundary preserved.`
    );

    setTimeout(() => {
      setFederatedState('callback');
      onLogAudit('Federated Auth Callback Received', 'authentication', 'info', `Verifying raw upstream callback assertions for ${providerName}...`);

      setTimeout(() => {
        setFederatedState('completed');
        const evidence: BiometricEvidence = {
          amr: 'face',
          provenance: 'upstream_face_trusted',
          issuer: providerName,
          verificationTime: new Date().toISOString(),
          freshnessSeconds: 4,
          confidenceRating: 'medium_reported',
          isHardwareBacked: true,
          isLivenessProtected: true,
          auditReference: `aud-fed-${Math.random().toString(36).substring(7)}`,
          redactedRawClaims: {}
        };
        setEmittedEvidence(evidence);
        onSetVerifiedEvidence(evidence);
        setStep(3); // Success
        onLogAudit(
          'Federated Evidence Processed',
          'authentication',
          'success',
          `Successfully transformed and validated biometric claims from ${providerName}.`,
          'face',
          'upstream_face_trusted'
        );
      }, 1500);
    }, 2000);
  };

  return (
    <div id="active-ceremony-wizard-card" className="max-w-xl mx-auto">
      {/* Starting Screen Selection */}
      {ceremonyType === 'none' && (
        <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm text-center">
          <ShieldCheck className="w-12 h-12 text-indigo-600 mx-auto mb-4" />
          <h2 className="text-xl font-bold text-gray-900 mb-2">Secure Biometric Ceremony sandbox</h2>
          <p className="text-xs text-gray-500 mb-6 max-w-md mx-auto leading-relaxed">
            Test the entire biometric lifecycle step-by-step. Simulate the first-party enrollment process, positioning guides, active liveness challenges, and multi-factor logins.
          </p>

          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button
              type="button"
              onClick={() => startCeremony('enrollment')}
              className="px-5 py-3 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm transition"
            >
              Simulate Secure Face Enrollment
            </button>
            <button
              type="button"
              onClick={() => startCeremony('login')}
              className="px-5 py-3 border border-gray-200 hover:bg-gray-50 text-gray-700 rounded-xl text-xs font-semibold shadow-xs transition"
            >
              Simulate Active Login & Step-Up
            </button>
          </div>
        </div>
      )}

      {/* ========================================================= */}
      {/* --- ENROLLMENT FLOW STEPS --- */}
      {/* ========================================================= */}
      {ceremonyType === 'enrollment' && (
        <div className="space-y-4 text-center">
          
          {/* Step tracker */}
          <div className="flex justify-between text-[10px] font-mono font-bold text-gray-400 max-w-sm mx-auto mb-2 uppercase">
            <span className={step >= 1 ? 'text-indigo-600' : ''}>1. Consent</span>
            <span>•</span>
            <span className={step >= 2 ? 'text-indigo-600' : ''}>2. Preflight</span>
            <span>•</span>
            <span className={step >= 3 ? 'text-indigo-600' : ''}>3. Capture</span>
            <span>•</span>
            <span className={step >= 4 ? 'text-indigo-600' : ''}>4. Review</span>
          </div>

          {/* STEP 1: Biometric privacy and consent notice */}
          {step === 1 && (
            <BiometricPrivacyNotice
              onAccept={handleConsentAccepted}
              onDecline={resetCeremony}
            />
          )}

          {/* STEP 2: Eligibility / Compatibility / Preflight checks */}
          {step === 2 && (
            <div>
              {errorMsg ? (
                <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
                  <div className="p-3 bg-red-50 text-red-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    <AlertOctagon className="w-6 h-6" />
                  </div>
                  <h4 className="text-base font-bold text-gray-900">Preflight Check Blocked</h4>
                  <p className="text-xs text-gray-600 mt-2 leading-relaxed bg-red-50 p-3 rounded-lg border border-red-100 text-left">
                    {errorMsg}
                  </p>
                  <div className="flex gap-3 justify-end mt-5">
                    <button
                      type="button"
                      onClick={() => setErrorMsg(null)}
                      className="px-4 py-2 border border-gray-200 hover:bg-gray-50 rounded-xl text-xs font-semibold"
                    >
                      Configure Simulation & Retry
                    </button>
                    <button
                      type="button"
                      onClick={resetCeremony}
                      className="px-4 py-2 text-gray-500 hover:underline text-xs"
                    >
                      Use Alternative Auth
                    </button>
                  </div>
                </div>
              ) : (
                <FaceCapturePreflight
                  onPreflightComplete={handlePreflightCompleted}
                  onPreflightFailed={handlePreflightFailed}
                  onUseFallback={resetCeremony}
                />
              )}
            </div>
          )}

          {/* STEP 3: Active capture with correct position & blink instructions */}
          {step === 3 && (
            <div>
              {errorMsg ? (
                <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm">
                  <div className="p-3 bg-red-50 text-red-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    {isSpoofDetected ? <AlertOctagon className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
                  </div>
                  <h4 className="text-base font-bold text-gray-900">
                    {isSpoofDetected ? 'Liveness Spoof Detected' : 'Biometric Quality Failure'}
                  </h4>
                  <p className="text-xs text-gray-600 mt-2 leading-relaxed bg-red-50 p-3 rounded-lg border border-red-100 text-left">
                    {errorMsg}
                  </p>
                  {isSpoofDetected && (
                    <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3.5 rounded-xl text-left text-[11px] mt-4">
                      <span className="font-bold block">Strict Anti-Spoof Warning:</span>
                      Under corporate policy, repeated presentation failures trigger a temporary security lockout audit and disable face verification registration.
                    </div>
                  )}
                  <div className="flex gap-3 justify-end mt-5">
                    <button
                      type="button"
                      onClick={() => {
                        setErrorMsg(null);
                        setIsSpoofDetected(false);
                      }}
                      className="px-4 py-2 border border-indigo-200 text-indigo-700 bg-indigo-50/50 hover:bg-indigo-50 rounded-xl text-xs font-semibold"
                    >
                      Try Capture Again
                    </button>
                    <button
                      type="button"
                      onClick={resetCeremony}
                      className="px-4 py-2 text-gray-500 hover:underline text-xs"
                    >
                      Choose Alternative Method
                    </button>
                  </div>
                </div>
              ) : (
                <FaceCaptureShell
                  purpose="enrollment"
                  challenge="enr_chal_e20fea675118"
                  onSuccess={handleCaptureSuccess}
                  onFailure={handleCaptureFailure}
                  onCancel={resetCeremony}
                />
              )}
            </div>
          )}

          {/* STEP 4: Activation Review (Section 5.1.9) */}
          {step === 4 && enrolledTemplate && (
            <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-left">
              <div className="flex items-start gap-4 mb-5 border-b border-gray-100 pb-4">
                <div className="p-3 bg-green-50 text-green-600 rounded-xl">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-gray-900">Biometric Template Review</h3>
                  <p className="text-[11px] text-gray-400 font-mono mt-0.5">Template reference prepared inside verifier enclave boundary.</p>
                </div>
              </div>

              {/* Secure Label Edit */}
              <div className="mb-4">
                <label className="block text-xs font-semibold text-gray-600 mb-1.5 uppercase tracking-wider">Provide Authenticator Label</label>
                <input
                  type="text"
                  value={authLabel}
                  onChange={(e) => setAuthLabel(e.target.value)}
                  className="w-full bg-gray-50 border border-gray-200 rounded-xl p-2.5 text-xs font-semibold text-gray-900 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                />
                <span className="text-[10px] text-gray-400 mt-1 block">Choose a friendly label. The actual biometric coordinates are sealed.</span>
              </div>

              <div className="grid grid-cols-2 gap-4 text-[11px] bg-gray-50 p-3.5 rounded-xl border border-gray-200/50 mb-5">
                <div>
                  <span className="text-gray-400 font-medium block">Consent Version</span>
                  <span className="font-semibold text-gray-900 font-mono">{enrolledTemplate.consentVersion}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Verifier Engine</span>
                  <span className="font-semibold text-gray-900 font-mono">{enrolledTemplate.verifierProfile}</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Retention Boundary</span>
                  <span className="font-semibold text-gray-900">Strict Local Purge Only</span>
                </div>
                <div>
                  <span className="text-gray-400 font-medium block">Backup Recovery Setup</span>
                  <span className="font-semibold text-green-700">Active (YubiKey Key)</span>
                </div>
              </div>

              {/* Warning about no face avatar */}
              <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-3 flex items-start gap-2.5 text-xs text-indigo-900 mb-5">
                <Info className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                <p className="text-[11px] leading-relaxed">
                  <strong className="font-semibold text-indigo-900 block">Security Redaction Rule:</strong>
                  Your actual facial photograph or facial map is never stored or used as an account avatar. It exists solely as an encrypted template sealed inside hardware.
                </p>
              </div>

              <div className="flex gap-3 justify-end">
                <button
                  type="button"
                  onClick={resetCeremony}
                  className="px-4 py-2 border border-gray-200 text-gray-700 rounded-xl text-xs font-semibold hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button
                  type="button"
                  onClick={activateAuthenticator}
                  className="px-5 py-2 bg-indigo-600 hover:bg-indigo-700 text-white rounded-xl text-xs font-semibold shadow-sm"
                >
                  Confirm & Activate Profile
                </button>
              </div>
            </div>
          )}

          {/* STEP 5: Success completion */}
          {step === 5 && (
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm">
              <div className="p-3 bg-green-50 text-green-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                <CheckCircle className="w-6 h-6" />
              </div>
              <h4 className="text-base font-bold text-gray-900">Activation Successful!</h4>
              <p className="text-xs text-gray-500 mt-2 max-w-sm mx-auto leading-relaxed">
                Your first-party face authenticator has been safely registered on the verifier boundary. Backup recovery configuration is active.
              </p>
              <button
                type="button"
                onClick={resetCeremony}
                className="px-5 py-2.5 bg-gray-900 hover:bg-black text-white text-xs font-semibold rounded-xl transition mt-5"
              >
                Return to Ceremony Menu
              </button>
            </div>
          )}
        </div>
      )}

      {/* ========================================================= */}
      {/* --- AUTHENTICATION (LOGIN/STEP-UP) FLOW --- */}
      {/* ========================================================= */}
      {ceremonyType === 'login' && (
        <div className="space-y-4">
          
          {/* STEP 1: Method Chooser (Section 5.2.1 & 6) */}
          {step === 1 && (
            <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-left">
              <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-4">
                <div>
                  <h4 className="text-sm font-bold text-gray-900">Select Step-Up Method</h4>
                  <p className="text-[10px] text-gray-500">Satisfies security validation policy for administrative step-up.</p>
                </div>
              </div>

              <div className="space-y-3">
                {/* METHOD 1: First-Party Face Authenticator */}
                {policyAllowFirstParty ? (
                  <button
                    type="button"
                    onClick={() => setStep(2)}
                    className="w-full text-left p-3.5 border border-indigo-200 hover:border-indigo-400 hover:bg-indigo-50/20 rounded-xl transition flex justify-between items-center"
                  >
                    <div>
                      <span className="font-semibold text-xs text-indigo-900 block">Use local Face Recognition</span>
                      <span className="text-[10px] text-gray-500">First-party challenge-bound liveness check.</span>
                    </div>
                    <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded bg-indigo-100 text-indigo-800 uppercase tracking-wider">
                      DIRECT ENCLAVE
                    </span>
                  </button>
                ) : (
                  <div className="p-3.5 border border-gray-100 bg-gray-50/50 text-gray-400 rounded-xl text-xs flex justify-between items-center">
                    <div>
                      <span className="font-semibold block">Local Face Recognition</span>
                      <span className="text-[10px]">Disabled by active tenant evidence policy.</span>
                    </div>
                    <span className="text-[9px] font-mono font-bold px-2 py-0.5 rounded bg-gray-100 uppercase tracking-wider">
                      DISABLED
                    </span>
                  </div>
                )}

                {/* METHOD 2: WebAuthn Passkey (Simulate either UV-only or verified face modal) */}
                <div className="border border-gray-100 rounded-xl p-3.5 bg-gray-50/20">
                  <span className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider block mb-2">WebAuthn passkey adapters</span>
                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                    <button
                      type="button"
                      onClick={() => triggerPasskeyAssertion('uv')}
                      className="text-left p-2.5 bg-white border border-gray-200 hover:border-gray-300 rounded-lg text-xs transition"
                    >
                      <span className="font-semibold text-gray-900 block">Passkey: Generic UV</span>
                      <span className="text-[10px] text-gray-400">Modality remains unknown.</span>
                    </button>
                    <button
                      type="button"
                      onClick={() => triggerPasskeyAssertion('face')}
                      className="text-left p-2.5 bg-white border border-gray-200 hover:border-gray-300 rounded-lg text-xs transition"
                    >
                      <span className="font-semibold text-gray-900 block">Passkey: Attested Face</span>
                      <span className="text-[10px] text-gray-400">Claims upstream face modality.</span>
                    </button>
                  </div>
                  <span className="text-[10px] text-gray-400 block mt-2">
                    * Supports general platform credentials. Modality unknown UV returns generic user flags.
                  </span>
                </div>

                {/* METHOD 3: Federated Identity Providers */}
                {policyAllowFederated ? (
                  <div className="border border-gray-100 rounded-xl p-3.5 bg-gray-50/20">
                    <span className="text-[10px] font-mono font-bold text-gray-400 uppercase tracking-wider block mb-2">Configure Trusted Upstream Provider</span>
                    <div className="flex flex-wrap gap-2">
                      <button
                        type="button"
                        onClick={() => triggerFederatedRedirect('Microsoft Entra ID')}
                        className="px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-100 rounded-lg text-xs font-semibold text-gray-700 transition"
                      >
                        Microsoft Entra ID
                      </button>
                      <button
                        type="button"
                        onClick={() => triggerFederatedRedirect('Okta Enterprise')}
                        className="px-3 py-1.5 bg-white border border-gray-200 hover:bg-gray-100 rounded-lg text-xs font-semibold text-gray-700 transition"
                      >
                        Okta Enterprise
                      </button>
                    </div>
                  </div>
                ) : null}
              </div>

              {/* Cancel button */}
              <div className="flex justify-end mt-4 pt-3 border-t border-gray-100">
                <button
                  type="button"
                  onClick={resetCeremony}
                  className="px-4 py-2 text-xs font-semibold text-gray-500 hover:text-gray-700"
                >
                  Cancel Handoff
                </button>
              </div>
            </div>
          )}

          {/* STEP 2: First-Party Face challenge active */}
          {step === 2 && (
            <div>
              {errorMsg ? (
                <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-center">
                  <div className="p-3 bg-red-50 text-red-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-4">
                    {isSpoofDetected ? <AlertOctagon className="w-6 h-6" /> : <AlertTriangle className="w-6 h-6" />}
                  </div>
                  <h4 className="text-base font-bold text-gray-900">
                    {isSpoofDetected ? 'Liveness Spoof Detected' : 'No Match Found'}
                  </h4>
                  <p className="text-xs text-gray-600 mt-2 leading-relaxed bg-red-50 p-3 rounded-lg border border-red-100 text-left">
                    {errorMsg}
                  </p>
                  <div className="flex gap-3 justify-end mt-5">
                    <button
                      type="button"
                      onClick={() => {
                        setErrorMsg(null);
                        setIsSpoofDetected(false);
                      }}
                      className="px-4 py-2 border border-indigo-200 text-indigo-700 bg-indigo-50/50 hover:bg-indigo-50 rounded-xl text-xs font-semibold"
                    >
                      Try Face Check Again
                    </button>
                    <button
                      type="button"
                      onClick={() => setStep(1)}
                      className="px-4 py-2 text-gray-500 hover:underline text-xs font-semibold"
                    >
                      Try Alternative Method
                    </button>
                  </div>
                </div>
              ) : (
                <FaceCaptureShell
                  purpose="login"
                  challenge="log_chal_90914160447"
                  onSuccess={handleDirectFaceVerified}
                  onFailure={handleCaptureFailure}
                  onCancel={resetCeremony}
                />
              )}
            </div>
          )}

          {/* STEP 3: Complete Success / Evidence Detail View (Section 4 & 5.6) */}
          {step === 3 && emittedEvidence && (
            <div className="space-y-6">
              <div className="bg-white border border-gray-200 rounded-2xl p-6 shadow-sm text-center">
                <div className="p-3 bg-green-50 text-green-600 rounded-full w-12 h-12 flex items-center justify-center mx-auto mb-3">
                  <ShieldCheck className="w-6 h-6" />
                </div>
                <h4 className="text-base font-bold text-gray-900">Ceremony Success Result</h4>
                <p className="text-xs text-gray-500 mt-1 max-w-sm mx-auto leading-relaxed">
                  The biometric challenge signature has been verified and evidence qualification logged in active headers.
                </p>

                <div className="mt-4 pt-4 border-t border-gray-100 flex justify-center">
                  <BiometricEvidenceQualifier
                    provenance={emittedEvidence.provenance}
                    evidence={emittedEvidence}
                  />
                </div>
              </div>

              {/* Provenance details panel */}
              <EvidenceProvenancePanel
                evidence={emittedEvidence}
              />

              <div className="flex justify-end gap-3">
                <button
                  type="button"
                  onClick={resetCeremony}
                  className="px-5 py-2 bg-gray-900 hover:bg-black text-white text-xs font-semibold rounded-xl transition"
                >
                  Close & Clear Session
                </button>
              </div>
            </div>
          )}

          {/* PENDING AWAITING SYSTEM PROCESSORS FOR PASSKEY OR REDIRECT MOCK */}
          {passkeyState === 'awaiting' && (
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm text-center">
              <RefreshCw className="w-10 h-10 text-indigo-600 animate-spin mx-auto mb-4" />
              <h4 className="text-sm font-bold text-gray-900">Awaiting Browser Passkey Ceremony</h4>
              <p className="text-xs text-gray-500 mt-1.5 max-w-xs mx-auto leading-relaxed">
                The operating system is displaying its native credential picker prompt. Please perform your local biometric key gesture.
              </p>
            </div>
          )}

          {federatedState === 'redirecting' && (
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm text-center">
              <RefreshCw className="w-10 h-10 text-indigo-600 animate-spin mx-auto mb-4" />
              <h4 className="text-sm font-bold text-gray-900">Redirecting to {selectedFederatedProvider}...</h4>
              <p className="text-xs text-gray-500 mt-1.5 max-w-xs mx-auto">
                Transferring verification credentials. Handshaking transaction parameters...
              </p>
            </div>
          )}

          {federatedState === 'callback' && (
            <div className="bg-white border border-gray-200 rounded-2xl p-8 shadow-sm text-center">
              <RefreshCw className="w-10 h-10 text-indigo-600 animate-spin mx-auto mb-4" />
              <h4 className="text-sm font-bold text-gray-900">Extracting Federated AMR Claim...</h4>
              <p className="text-xs text-gray-500 mt-1.5 max-w-xs mx-auto">
                Parsing response attributes. Validating provider claim signatures...
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};
