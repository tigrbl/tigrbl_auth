/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { 
  Phone, Plus, ShieldCheck, Trash2, ShieldAlert, CheckCircle, 
  X, RefreshCw, Volume2, UserCheck, Shield, ChevronRight, 
  HelpCircle, Eye, EyeOff, Info, AlertTriangle, ArrowRight 
} from 'lucide-react';
import { PhoneAuthenticator, CallContext, TelephonePolicy, ProviderConfig } from '../types';
import { COUNTRIES, formatPhoneNumber, maskPhoneNumber } from '../data';

interface AuthCeremonyProps {
  enrolledPhones: PhoneAuthenticator[];
  setEnrolledPhones: React.Dispatch<React.SetStateAction<PhoneAuthenticator[]>>;
  activeCall: CallContext | null;
  startCall: (
    type: 'enrollment' | 'login' | 'step_up', 
    rawNumber: string, 
    label?: string,
    ivrMode?: 'code_read' | 'approval_press',
    purpose?: string
  ) => void;
  cancelCall: () => void;
  logEvent: (type: string, details: string, status: 'success' | 'failure' | 'warning' | 'info') => void;
  policy: TelephonePolicy;
  provider: ProviderConfig;
  onSuccessfulAuthentication: (amrResult: any) => void;
}

export default function AuthCeremony({
  enrolledPhones,
  setEnrolledPhones,
  activeCall,
  startCall,
  cancelCall,
  logEvent,
  policy,
  provider,
  onSuccessfulAuthentication
}: AuthCeremonyProps) {
  // Navigation Tabs: 'auth' (P0) or 'lifecycle' (P1)
  const [activeTab, setActiveTab] = useState<'auth' | 'lifecycle'>('auth');
  
  // Auth flow sub-states
  const [authStep, setAuthStep] = useState<'chooser' | 'calling' | 'success' | 'failed'>('chooser');
  const [selectedPhone, setSelectedPhone] = useState<PhoneAuthenticator | null>(enrolledPhones[0] || null);
  const [stepUpPurpose, setStepUpPurpose] = useState<string>('Standard Identity MFA Verification');
  const [stepUpAmount, setStepUpAmount] = useState<string>('5000');
  const [mfaType, setMfaType] = useState<'login' | 'step_up'>('login');
  
  // Manual OTP verification (for 'code_read' and 'both' modes)
  const [otpValue, setOtpValue] = useState<string>('');
  const [otpError, setOtpError] = useState<string | null>(null);

  // Enrollment (P1) Sub-states
  const [enrollStep, setEnrollStep] = useState<'intro' | 'form' | 'verifying' | 'naming' | 'complete'>('intro');
  const [countryCode, setCountryCode] = useState('US');
  const [phoneNumber, setPhoneNumber] = useState('');
  const [consentChecked, setConsentChecked] = useState(false);
  const [enrollLabel, setEnrollLabel] = useState('Primary Personal Mobile');
  const [accessibilityMode, setAccessibilityMode] = useState<'standard' | 'slower_speech' | 'text_relay'>('standard');
  const [showRawNumber, setShowRawNumber] = useState(false);
  const [tempEnrolledPhone, setTempEnrolledPhone] = useState<{ raw: string; country: string } | null>(null);

  // Replacement Flow States
  const [isReplacing, setIsReplacing] = useState(false);
  const [phoneToReplace, setPhoneToReplace] = useState<PhoneAuthenticator | null>(null);

  // Recovery Flow States
  const [showRecoveryScreen, setShowRecoveryScreen] = useState(false);
  const [recoveryCode, setRecoveryCode] = useState('');
  const [recoveryStatus, setRecoveryStatus] = useState<'idle' | 'success' | 'error'>('idle');

  // Sync selected phone when enrolled changes
  useEffect(() => {
    if (enrolledPhones.length > 0 && !selectedPhone) {
      setSelectedPhone(enrolledPhones[0]);
    }
  }, [enrolledPhones]);

  // Sync state with activeCall status
  useEffect(() => {
    if (!activeCall) {
      if (authStep === 'calling') {
        setAuthStep('chooser');
      }
      if (enrollStep === 'verifying') {
        setEnrollStep('form');
      }
      return;
    }

    if (activeCall.type === 'login' || activeCall.type === 'step_up') {
      setAuthStep('calling');
      if (activeCall.status === 'completed') {
        // If requireApprovalMode is ivr_keypad only, we succeed immediately!
        if (policy.requireApprovalMode === 'ivr_keypad' || policy.requireApprovalMode === 'any') {
          handleAuthSuccess();
        }
      } else if (['busy', 'no_answer', 'voicemail', 'failed', 'rejected'].includes(activeCall.status)) {
        setAuthStep('failed');
      }
    } else if (activeCall.type === 'enrollment') {
      setEnrollStep('verifying');
      if (activeCall.status === 'completed') {
        if (policy.requireApprovalMode === 'ivr_keypad' || policy.requireApprovalMode === 'any') {
          setEnrollStep('naming');
        }
      } else if (['busy', 'no_answer', 'voicemail', 'failed', 'rejected'].includes(activeCall.status)) {
        setEnrollStep('form');
        logEvent('TEL_ENROLLMENT_FAILED', `Enrollment call failed with reason: ${activeCall.status}`, 'failure');
      }
    }
  }, [activeCall, activeCall?.status]);

  const handleAuthSuccess = () => {
    setAuthStep('success');
    logEvent('TEL_AUTH_SUCCESS', `MFA verified using telephone confirmation. Destination: ${selectedPhone?.maskedNumber || 'Unknown'}`, 'success');
    
    // Provide official AMR token evidence back
    onSuccessfulAuthentication({
      amr: 'tel',
      maskedDestination: selectedPhone?.maskedNumber,
      authenticatedAt: new Date().toISOString(),
      providerUsed: provider.activeProvider,
      transactionBounded: activeCall?.type === 'step_up',
      purpose: activeCall?.transactionPurpose,
      assuranceLevel: 'lower_assurance (Telephone channel confirmation only; no voice biometrics)',
    });
  };

  // Process OTP code entry
  const handleVerifyOtp = (e: React.FormEvent) => {
    e.preventDefault();
    if (!activeCall) return;

    if (otpValue === activeCall.verificationCode) {
      setOtpError(null);
      setOtpValue('');
      
      if (activeCall.type === 'enrollment') {
        setEnrollStep('naming');
        logEvent('TEL_ENROLL_OTP_MATCH', `Ownership test code matched during enrollment call for +${activeCall.destination}`, 'success');
      } else {
        handleAuthSuccess();
      }
    } else {
      setOtpError('Invalid confirmation code. Please listen carefully and try again.');
      logEvent('TEL_OTP_MISMATCH', `User submitted incorrect confirmation OTP code.`, 'warning');
    }
  };

  // Launch login or step-up call
  const triggerAuthCall = () => {
    if (!selectedPhone) return;
    
    // Determine required modes based on policy
    const ivrMode = policy.requireApprovalMode === 'web_otp_only' || policy.requireApprovalMode === 'both'
      ? 'code_read' 
      : 'approval_press';

    const purpose = mfaType === 'step_up' 
      ? `Step-up authentication: authorize wire transfer of $${stepUpAmount} USD` 
      : 'Secure System Access Verification';

    startCall(mfaType === 'step_up' ? 'step_up' : 'login', selectedPhone.rawNumber, selectedPhone.label, ivrMode, purpose);
    logEvent('TEL_CHALLENGE_START', `Auth challenge call triggered to ${selectedPhone.maskedNumber}. Context: ${mfaType}`, 'info');
  };

  // Enrollment Wizard Operations
  const startEnrollmentCall = (e: React.FormEvent) => {
    e.preventDefault();
    if (!phoneNumber) return;
    if (!consentChecked) return;

    const country = COUNTRIES.find(c => c.code === countryCode) || COUNTRIES[0];
    const rawNumber = country.prefix + phoneNumber.replace(/\D/g, '');

    // Accessibility profiles can adjust text to speech behavior
    const voiceMod = accessibilityMode === 'slower_speech' ? ' (Slower Speech)' : '';
    setTempEnrolledPhone({ raw: rawNumber, country: countryCode });

    startCall(
      'enrollment', 
      rawNumber, 
      enrollLabel, 
      'code_read', 
      `Telephone verification ownership test ${voiceMod}`
    );
    logEvent('TEL_ENROLLMENT_START', `Enrollment verification call initiated to ${rawNumber}`, 'info');
  };

  const saveNewAuthenticator = () => {
    if (!tempEnrolledPhone) return;
    
    const masked = maskPhoneNumber(tempEnrolledPhone.raw, tempEnrolledPhone.country);
    const newAuth: PhoneAuthenticator = {
      id: `auth-${Date.now()}`,
      label: enrollLabel,
      rawNumber: tempEnrolledPhone.raw,
      maskedNumber: masked,
      countryCode: tempEnrolledPhone.country,
      verifiedAt: new Date().toISOString(),
      createdAt: new Date().toISOString(),
      lastUsedAt: new Date().toISOString(),
      status: 'active',
    };

    setEnrolledPhones(prev => {
      // If we are performing replacement, retire the old phone
      if (isReplacing && phoneToReplace) {
        logEvent('TEL_REPLACE_COMPLETE', `Successfully replaced authenticator "${phoneToReplace.label}" with "${newAuth.label}"`, 'success');
        setIsReplacing(false);
        setPhoneToReplace(null);
        return prev.filter(p => p.id !== phoneToReplace.id).concat(newAuth);
      }
      return [...prev, newAuth];
    });

    logEvent('TEL_ENROLLMENT_COMPLETE', `Successfully activated new phone authenticator "${newAuth.label}" (${newAuth.maskedNumber})`, 'success');
    setEnrollStep('complete');
  };

  // Actions for Phone Lifecycles
  const togglePhoneStatus = (id: string) => {
    setEnrolledPhones(prev => prev.map(p => {
      if (p.id === id) {
        const nextStatus = p.status === 'active' ? 'suspended' : 'active';
        logEvent('TEL_LIFECYCLE_UPDATE', `Authenticator "${p.label}" state changed to ${nextStatus.toUpperCase()}`, nextStatus === 'active' ? 'info' : 'warning');
        return { ...p, status: nextStatus };
      }
      return p;
    }));
  };

  const removePhone = (id: string) => {
    const phone = enrolledPhones.find(p => p.id === id);
    if (!phone) return;

    // Check if this is the last phone authenticator
    if (enrolledPhones.length === 1) {
      alert("Security policy restriction: Cannot remove last remaining telephone authenticator without adding a fallback factor first.");
      logEvent('TEL_POLICY_BREACH', `Removal of "${phone.label}" blocked: Last remaining factor.`, 'failure');
      return;
    }

    setEnrolledPhones(prev => prev.filter(p => p.id !== id));
    logEvent('TEL_LIFECYCLE_REMOVE', `Deactivated and removed telephone authenticator "${phone.label}"`, 'warning');
  };

  const triggerReplacement = (phone: PhoneAuthenticator) => {
    setPhoneToReplace(phone);
    setIsReplacing(true);
    setActiveTab('lifecycle');
    setEnrollStep('intro');
    setPhoneNumber('');
  };

  const handleRecoverySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (recoveryCode.trim() === '999-888-777') {
      setRecoveryStatus('success');
      logEvent('TEL_RECOVERY_SUCCESS', `Bypassed telephone verification using active offline paper recovery seed. Policy issued reduced assurance token.`, 'warning');
      
      onSuccessfulAuthentication({
        amr: 'tel_recovery',
        authenticatedAt: new Date().toISOString(),
        assuranceLevel: 'lowest_assurance (Offline security seed fallback; reduced posture)',
      });
    } else {
      setRecoveryStatus('error');
      logEvent('TEL_RECOVERY_FAILED', `Failed offline recovery seed validation attempt.`, 'failure');
    }
  };

  return (
    <div className="flex flex-col h-full">
      {/* Tab Selectors */}
      <div className="flex border-b border-zinc-900 bg-zinc-950/40 p-1">
        <button
          onClick={() => { setActiveTab('auth'); setShowRecoveryScreen(false); }}
          className={`flex-1 py-2.5 text-xs font-semibold rounded-lg transition-all cursor-pointer flex items-center justify-center space-x-1.5 ${
            activeTab === 'auth' && !showRecoveryScreen
              ? 'bg-zinc-900 border border-zinc-900 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <Shield className="w-3.5 h-3.5" />
          <span>P0 — Live Authentication</span>
        </button>
        <button
          onClick={() => { setActiveTab('lifecycle'); setShowRecoveryScreen(false); }}
          className={`flex-1 py-2.5 text-xs font-semibold rounded-lg transition-all cursor-pointer flex items-center justify-center space-x-1.5 ${
            activeTab === 'lifecycle' && !showRecoveryScreen
              ? 'bg-zinc-900 border border-zinc-900 text-white shadow-sm'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <Plus className="w-3.5 h-3.5" />
          <span>P1 — Enrollment & Lifecycle</span>
        </button>
        <button
          onClick={() => { setShowRecoveryScreen(true); }}
          className={`px-3 py-2.5 text-xs font-semibold rounded-lg transition-all cursor-pointer flex items-center justify-center space-x-1.5 ${
            showRecoveryScreen
              ? 'bg-amber-500/10 border border-amber-500/20 text-amber-300'
              : 'text-zinc-400 hover:text-zinc-200'
          }`}
        >
          <span>Recovery</span>
        </button>
      </div>

      {/* Main Container Area */}
      <div className="flex-1 p-6 overflow-y-auto">

        {/* RECOVERY BEYOND TELEPHONE */}
        {showRecoveryScreen && (
          <div className="space-y-5">
            <div className="bg-amber-500/5 border border-amber-500/20 rounded-2xl p-4 flex items-start space-x-3">
              <ShieldAlert className="w-5 h-5 text-amber-400 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-sm font-semibold text-amber-300">Offline Recovery Protocol</h4>
                <p className="text-xs text-zinc-400 leading-relaxed mt-1">
                  If you have lost your physical telephone line, cannot receive IVR authentication calls, or find yourself locked out due to high regional fraud rate limits, use your offline cryptographic master seed key.
                </p>
              </div>
            </div>

            {recoveryStatus !== 'success' ? (
              <form onSubmit={handleRecoverySubmit} className="bg-zinc-900 border border-zinc-900 rounded-2xl p-5 space-y-4">
                <div>
                  <label className="block text-xs font-mono font-medium uppercase text-zinc-400 mb-1.5">Enter Master Recovery Seed Code</label>
                  <input
                    type="text"
                    required
                    placeholder="999-888-777"
                    value={recoveryCode}
                    onChange={(e) => setRecoveryCode(e.target.value)}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-xl px-4 py-3 text-sm font-mono text-white focus:outline-none focus:border-amber-500 transition-colors"
                  />
                  <span className="text-[10px] text-zinc-500 mt-1 block">Test Code: <span className="font-mono text-zinc-400 select-all">999-888-777</span></span>
                </div>

                {recoveryStatus === 'error' && (
                  <div className="p-3 bg-red-500/5 border border-red-500/20 rounded-xl text-xs text-red-400 flex items-center space-x-2">
                    <X className="w-4 h-4" />
                    <span>Cryptographic seed does not match escrow profile.</span>
                  </div>
                )}

                <button
                  type="submit"
                  className="w-full bg-amber-500 hover:bg-amber-600 font-semibold text-xs text-slate-950 py-3 rounded-xl transition-all cursor-pointer flex items-center justify-center space-x-1.5"
                >
                  <UserCheck className="w-4 h-4" />
                  <span>Verify Recovery Seed & Sign In</span>
                </button>
              </form>
            ) : (
              <div className="bg-zinc-900 border border-zinc-900 rounded-2xl p-6 text-center space-y-4">
                <div className="w-12 h-12 bg-amber-500/10 border border-amber-500/20 rounded-2xl flex items-center justify-center mx-auto">
                  <CheckCircle className="w-6 h-6 text-amber-400" />
                </div>
                <div>
                  <h3 className="text-sm font-semibold text-white">Emergency Recovery Triggered</h3>
                  <p className="text-xs text-zinc-400 max-w-sm mx-auto mt-1 leading-relaxed">
                    Identity verified using reduced assurance escrow keys. Access granted. Telephony methods are currently suspended for safety. Please enroll a new number instantly.
                  </p>
                </div>
                <button
                  onClick={() => { setRecoveryStatus('idle'); setRecoveryCode(''); setShowRecoveryScreen(false); setActiveTab('lifecycle'); setEnrollStep('intro'); }}
                  className="px-4 py-2 border border-zinc-900 rounded-xl text-xs font-semibold text-zinc-300 hover:text-white transition-colors cursor-pointer"
                >
                  Go Enroll New Device
                </button>
              </div>
            )}
          </div>
        )}

        {/* TAB: P0 AUTHENTICATION CEREMONY */}
        {activeTab === 'auth' && !showRecoveryScreen && (
          <div className="space-y-6">

            {/* Sub-State: chooser */}
            {authStep === 'chooser' && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-sm font-bold text-white tracking-wide uppercase font-mono">Telephone Confirmation Ceremony</h2>
                  <p className="text-xs text-zinc-400 mt-1">
                    Select your registered line to initiate the out-of-band telephone verification process.
                  </p>
                </div>

                {/* Switch between Standard Login or High-Risk Step-up */}
                <div className="bg-zinc-950/40 p-1 border border-zinc-900 rounded-xl flex">
                  <button
                    onClick={() => setMfaType('login')}
                    className={`flex-1 py-1.5 text-[11px] font-semibold rounded-lg transition-colors cursor-pointer ${
                      mfaType === 'login' ? 'bg-zinc-900 text-white' : 'text-zinc-500 hover:text-zinc-300'
                    }`}
                  >
                    Standard MFA Login
                  </button>
                  <button
                    onClick={() => setMfaType('step_up')}
                    className={`flex-1 py-1.5 text-[11px] font-semibold rounded-lg transition-colors cursor-pointer ${
                      mfaType === 'step_up' ? 'bg-zinc-900 text-white' : 'text-zinc-500 hover:text-zinc-300'
                    }`}
                  >
                    High-Risk Step-Up
                  </button>
                </div>

                {/* Step-up parameters (Dynamic UI testing) */}
                {mfaType === 'step_up' && (
                  <div className="bg-amber-500/5 border border-amber-500/15 rounded-xl p-4 space-y-3">
                    <div className="flex items-center space-x-2">
                      <ShieldAlert className="w-4 h-4 text-amber-400" />
                      <span className="text-xs font-semibold text-amber-300">Step-Up Authorization Context</span>
                    </div>
                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-[10px] text-zinc-500 font-mono block mb-1">Transaction Target</label>
                        <select
                          value={stepUpPurpose}
                          onChange={(e) => setStepUpPurpose(e.target.value)}
                          className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300 focus:outline-none"
                        >
                          <option value="Wire Transfer approval">Wire Transfer Out</option>
                          <option value="SSH Public Key Deployment">Deploy Admin SSH Key</option>
                          <option value="Database Cluster Deletion">Delete DB Cluster</option>
                        </select>
                      </div>
                      <div>
                        <label className="text-[10px] text-zinc-500 font-mono block mb-1">Value Limit (USD)</label>
                        <input
                          type="number"
                          value={stepUpAmount}
                          onChange={(e) => setStepUpAmount(e.target.value)}
                          className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-1.5 text-xs text-zinc-300 focus:outline-none"
                        />
                      </div>
                    </div>
                  </div>
                )}

                {/* Method Chooser Grid */}
                <div className="space-y-2.5">
                  <span className="text-[10px] font-mono font-medium text-zinc-500 uppercase">Available Enrolled Telephone Authenticators</span>
                  
                  {enrolledPhones.length === 0 ? (
                    <div className="border-2 border-dashed border-zinc-900 rounded-2xl p-6 text-center space-y-3">
                      <Phone className="w-8 h-8 text-zinc-600 mx-auto" />
                      <div className="space-y-1">
                        <p className="text-xs font-semibold text-zinc-400">No active telephone methods enrolled</p>
                        <p className="text-[10px] text-zinc-500 max-w-xs mx-auto">Please select the Enrollment tab to register and confirm your physical phone line first.</p>
                      </div>
                      <button
                        onClick={() => { setActiveTab('lifecycle'); setEnrollStep('intro'); }}
                        className="px-3 py-1.5 bg-zinc-900 border border-zinc-900 rounded-lg text-xs font-semibold text-zinc-300 hover:text-white transition-colors cursor-pointer"
                      >
                        Enroll Now
                      </button>
                    </div>
                  ) : (
                    enrolledPhones.map(phone => (
                      <button
                        key={phone.id}
                        disabled={phone.status === 'suspended'}
                        onClick={() => setSelectedPhone(phone)}
                        className={`w-full text-left p-4 rounded-xl border transition-all cursor-pointer flex items-center justify-between relative overflow-hidden ${
                          phone.status === 'suspended'
                            ? 'opacity-40 border-zinc-950 bg-zinc-950/20 cursor-not-allowed'
                            : selectedPhone?.id === phone.id
                              ? 'border-emerald-500/25 bg-emerald-500/5 shadow-sm'
                              : 'border-zinc-900 bg-zinc-950/20 hover:border-zinc-900 hover:bg-zinc-900/10'
                        }`}
                      >
                        <div className="flex items-center space-x-3.5">
                          <div className={`w-10 h-10 rounded-xl flex items-center justify-center shrink-0 border ${
                            selectedPhone?.id === phone.id
                              ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                              : 'bg-zinc-900 border-zinc-900 text-zinc-400'
                          }`}>
                            <Phone className="w-5 h-5" />
                          </div>
                          <div>
                            <div className="flex items-center space-x-1.5">
                              <span className="text-xs font-semibold text-white">{phone.label}</span>
                              {phone.status === 'suspended' && (
                                <span className="text-[8px] font-mono px-1.5 py-0.5 rounded bg-zinc-800 text-zinc-400 uppercase">Suspended</span>
                              )}
                            </div>
                            <span className="text-xs font-mono text-zinc-400 block mt-0.5">{phone.maskedNumber}</span>
                          </div>
                        </div>

                        <div className="flex items-center space-x-2">
                          <span className="text-[10px] text-zinc-500 font-mono uppercase">MFA Method</span>
                          <div className={`w-4 h-4 rounded-full border flex items-center justify-center shrink-0 ${
                            selectedPhone?.id === phone.id 
                              ? 'border-emerald-500 bg-emerald-500 text-slate-950' 
                              : 'border-zinc-900 bg-zinc-900'
                          }`}>
                            {selectedPhone?.id === phone.id && <div className="w-1.5 h-1.5 rounded-full bg-slate-950"></div>}
                          </div>
                        </div>
                      </button>
                    ))
                  )}
                </div>

                {/* CTA Action button to dial call */}
                {selectedPhone && (
                  <button
                    onClick={triggerAuthCall}
                    className="w-full bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-xs py-3.5 rounded-xl transition-all shadow-md shadow-emerald-500/15 cursor-pointer flex items-center justify-center space-x-1.5"
                  >
                    <Phone className="w-4 h-4 shrink-0" />
                    <span>Initiate Verification Call Handshake</span>
                  </button>
                )}

                <div className="bg-zinc-900/60 border border-zinc-900 rounded-xl p-3.5 flex items-start space-x-2.5">
                  <Info className="w-4 h-4 text-zinc-400 shrink-0 mt-0.5" />
                  <p className="text-[10px] text-zinc-400 leading-normal">
                    This telephone authenticator performs out-of-band callback checks to prove physical telephone channel access. Calls are monitored by local administrative anti-replay and rate limiters.
                  </p>
                </div>
              </div>
            )}

            {/* Sub-State: calling / waiting */}
            {authStep === 'calling' && activeCall && (
              <div className="space-y-6">
                <div className="text-center py-4">
                  <div className="w-14 h-14 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3 animate-pulse">
                    <RefreshCw className="w-6 h-6 text-emerald-400 animate-spin" />
                  </div>
                  <h3 className="text-sm font-semibold tracking-wider text-zinc-300 uppercase font-mono">Out-of-Band Call Live</h3>
                  <p className="text-xs text-zinc-500 mt-1 font-mono">
                    Session ID: <span className="text-zinc-400">{activeCall.id}</span>
                  </p>
                </div>

                {/* Connection Status and Instruction Alerts */}
                <div className="bg-zinc-950/60 border border-zinc-900 rounded-2xl p-4.5 space-y-4">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] font-mono font-medium text-zinc-400 uppercase tracking-wider">Line Status</span>
                    <span className={`text-[10px] font-mono font-bold px-2 py-0.5 rounded-md uppercase ${
                      activeCall.status === 'ringing' 
                        ? 'bg-blue-500/10 text-blue-400 animate-pulse'
                        : activeCall.status === 'connected' || activeCall.status === 'ivr_active'
                          ? 'bg-emerald-500/10 text-emerald-400'
                          : 'bg-zinc-800 text-zinc-400'
                    }`}>
                      {activeCall.status}
                    </span>
                  </div>

                  {/* Progressive visual indicators of telephone lifecycle state */}
                  <div className="grid grid-cols-4 gap-1.5 h-1.5">
                    <div className="h-full bg-emerald-500 rounded-full"></div>
                    <div className={`h-full rounded-full transition-all duration-350 ${['ringing', 'connected', 'ivr_active', 'awaiting_code'].includes(activeCall.status) ? 'bg-emerald-500' : 'bg-zinc-800'}`}></div>
                    <div className={`h-full rounded-full transition-all duration-350 ${['connected', 'ivr_active', 'awaiting_code'].includes(activeCall.status) ? 'bg-emerald-500' : 'bg-zinc-800'}`}></div>
                    <div className={`h-full rounded-full transition-all duration-350 ${['ivr_active', 'awaiting_code'].includes(activeCall.status) ? 'bg-emerald-500' : 'bg-zinc-800'}`}></div>
                  </div>

                  <div className="space-y-2 border-t border-zinc-900 pt-3">
                    <span className="text-[10px] font-mono font-medium text-zinc-500 uppercase">IVR Directives</span>
                    <div className="bg-zinc-900 border border-zinc-900/40 rounded-xl p-3 flex items-start space-x-2.5">
                      <Volume2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                      <div className="text-xs text-zinc-300 leading-normal font-medium">
                        {activeCall.ivrMode === 'code_read' ? (
                          <span>Listen closely to the spoken code in the simulator and type it below.</span>
                        ) : (
                          <span>Press <span className="font-bold text-white">[ 1 ]</span> on the phone dialpad simulator to approve the ceremony.</span>
                        )}
                      </div>
                    </div>
                  </div>
                </div>

                {/* Timer/Countdown Indicator */}
                <div className="flex items-center justify-between px-2 text-xs">
                  <span className="text-zinc-500">Call Expiration Countdown</span>
                  <span className={`font-mono font-bold ${activeCall.timer < 15 ? 'text-red-400 animate-pulse' : 'text-zinc-300'}`}>
                    {activeCall.timer} seconds
                  </span>
                </div>

                {/* OTP Entry Code field if code_read is active or policy requires OTP */}
                {(activeCall.ivrMode === 'code_read' || policy.requireApprovalMode === 'both') && (
                  <form onSubmit={handleVerifyOtp} className="space-y-4">
                    <div>
                      <label className="block text-[10px] font-mono text-zinc-400 uppercase tracking-wider mb-2 text-center">Enter Spoken Confirmation Code</label>
                      <div className="flex justify-center space-x-3">
                        <input
                          type="text"
                          maxLength={3}
                          placeholder="•••"
                          value={otpValue}
                          onChange={(e) => setOtpValue(e.target.value.replace(/\D/g, '').slice(0, 3))}
                          className="w-28 text-center bg-zinc-950 border-2 border-zinc-900 focus:border-emerald-500 focus:outline-none rounded-xl text-xl py-2 font-mono tracking-widest text-white shadow-inner"
                        />
                      </div>
                      <span className="text-[9px] text-zinc-500 text-center block mt-1.5 font-mono">Check physical simulator caption for the code.</span>
                    </div>

                    {otpError && (
                      <p className="text-[11px] text-red-400 text-center bg-red-500/5 py-2 px-3 border border-red-500/10 rounded-lg">{otpError}</p>
                    )}

                    <button
                      type="submit"
                      disabled={otpValue.length < 3}
                      className="w-full bg-zinc-900 border border-zinc-900 hover:border-zinc-900 hover:text-white text-zinc-300 font-bold text-xs py-3 rounded-xl transition-all cursor-pointer disabled:opacity-40 disabled:cursor-not-allowed"
                    >
                      Confirm Handshake Code
                    </button>
                  </form>
                )}

                {/* Cancel Trigger */}
                <button
                  onClick={cancelCall}
                  className="w-full bg-zinc-950 hover:bg-red-500/5 hover:text-red-400 border border-zinc-900 py-3 rounded-xl text-xs font-semibold text-zinc-400 transition-all cursor-pointer"
                >
                  Cancel Call Ceremony
                </button>
              </div>
            )}

            {/* Sub-State: success */}
            {authStep === 'success' && (
              <div className="space-y-5 text-center py-4">
                <div className="w-16 h-16 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3">
                  <CheckCircle className="w-9 h-9 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-base font-bold text-white font-mono tracking-wider">AMR ISSUED: [TEL]</h3>
                  <p className="text-xs text-zinc-400 mt-1 max-w-sm mx-auto">
                    Out-of-band telephone verification verified successfully. Evidence structure has been dispatched to the credential scope.
                  </p>
                </div>

                {/* Evidence structure break down */}
                <div className="bg-zinc-950/80 border border-zinc-900 rounded-2xl p-4 text-left space-y-3 font-mono">
                  <span className="text-[10px] text-emerald-400 uppercase font-semibold tracking-widest">Authentication Proof Structure</span>
                  <div className="space-y-2 text-[10px] text-zinc-400 leading-relaxed border-t border-zinc-900 pt-2.5">
                    <div className="flex justify-between"><span className="text-zinc-500">AMR claim:</span> <span className="text-white font-bold">tel</span></div>
                    <div className="flex justify-between"><span className="text-zinc-500">Masked destination:</span> <span className="text-white">{selectedPhone?.maskedNumber}</span></div>
                    <div className="flex justify-between"><span className="text-zinc-500">Provider signaling:</span> <span className="text-zinc-300">{provider.activeProvider}</span></div>
                    <div className="flex justify-between"><span className="text-zinc-500">Biometric bound:</span> <span className="text-amber-400 font-semibold">false (tel distinct from vbm)</span></div>
                    <div className="flex justify-between"><span className="text-zinc-500">IP assurance:</span> <span className="text-zinc-300">198.51.100.42</span></div>
                  </div>
                </div>

                <button
                  onClick={() => setAuthStep('chooser')}
                  className="w-full bg-zinc-900 border border-zinc-900 hover:text-white py-3 rounded-xl text-xs font-semibold text-zinc-300 transition-all cursor-pointer"
                >
                  Initiate New Ceremony
                </button>
              </div>
            )}

            {/* Sub-State: failed */}
            {authStep === 'failed' && activeCall && (
              <div className="space-y-5">
                <div className="text-center">
                  <div className="w-14 h-14 bg-red-500/10 border border-red-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3">
                    <ShieldAlert className="w-7 h-7 text-red-400" />
                  </div>
                  <h3 className="text-sm font-bold text-white tracking-wider font-mono uppercase">Call Handshake Failed</h3>
                  <p className="text-xs text-zinc-400 mt-1 max-w-sm mx-auto">
                    The out-of-band telephone gateway reported a connection failure.
                  </p>
                </div>

                {/* Signaling Breakdown */}
                <div className="bg-red-500/5 border border-red-500/15 rounded-2xl p-4 space-y-3">
                  <span className="text-[10px] font-mono font-medium text-red-400 uppercase tracking-widest block">Telephony Return State</span>
                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between"><span className="text-zinc-500">Exception state:</span> <span className="text-red-400 font-mono font-bold uppercase">{activeCall.status}</span></div>
                    <div className="flex justify-between"><span className="text-zinc-500">Reason code:</span> <span className="text-zinc-300 font-mono">
                      {activeCall.status === 'busy' && 'Line Busy (CARRIER_SIGNAL_BUSY)'}
                      {activeCall.status === 'no_answer' && 'No Answer Timeout (CARRIER_SIGNAL_NO_ANSWER)'}
                      {activeCall.status === 'voicemail' && 'Voicemail detected (SECURITY_MUTE)'}
                      {activeCall.status === 'rejected' && 'Rejected on keypad (USER_TERMINATED)'}
                      {activeCall.status === 'failed' && 'Gateway/Route failure (PROVIDER_TIMEOUT)'}
                    </span></div>
                  </div>
                </div>

                {/* Failsafe warning copy */}
                <p className="text-[10px] text-zinc-500 leading-normal">
                  To protect the profile against robotic replay abuse, voicemail delivery is explicitly filtered and treated as a security failure. Destination numbers cannot be verified without real-time human interaction.
                </p>

                {/* Failover Actions */}
                <div className="space-y-2">
                  <button
                    onClick={() => { setAuthStep('chooser'); triggerAuthCall(); }}
                    className="w-full bg-zinc-900 border border-zinc-900 hover:border-zinc-900 hover:text-white py-3 rounded-xl text-xs font-semibold text-zinc-300 transition-colors cursor-pointer"
                  >
                    Attempt Fallback Dialing Route
                  </button>
                  <button
                    onClick={() => setAuthStep('chooser')}
                    className="w-full bg-zinc-950 border border-zinc-900 hover:bg-zinc-900/35 py-3 rounded-xl text-xs font-semibold text-zinc-400 transition-colors cursor-pointer"
                  >
                    Select Alternative Phone Authenticator
                  </button>
                </div>
              </div>
            )}

          </div>
        )}

        {/* TAB: P1 ENROLLMENT & LIFECYCLE */}
        {activeTab === 'lifecycle' && !showRecoveryScreen && (
          <div className="space-y-6">

            {/* Sub-State: Intro */}
            {enrollStep === 'intro' && (
              <div className="space-y-5">
                <div>
                  <h2 className="text-sm font-bold text-white tracking-wide uppercase font-mono">
                    {isReplacing ? `Replace Authenticator` : `Enroll New Telephone Authenticator`}
                  </h2>
                  <p className="text-xs text-zinc-400 mt-1">
                    {isReplacing 
                      ? `You are replacing "${phoneToReplace?.label}". The existing key remains active until the new device passes ownership validation.`
                      : `Link your physical mobile or office phone line to complete out-of-band identity verification challenges.`
                    }
                  </p>
                </div>

                {/* Detailed disclosure card (Required in design Brief) */}
                <div className="bg-zinc-950/60 border border-zinc-900 rounded-2xl p-4.5 space-y-3.5">
                  <span className="text-[10px] font-mono font-medium text-emerald-400 uppercase tracking-widest block">Telephony Enrollment Disclosures</span>
                  <div className="space-y-2.5 text-xs text-zinc-400 leading-normal">
                    <p>
                      <strong>• Call Costs:</strong> Carrier network messaging or toll rates may apply. Out-of-band confirmation transmits only secure numeric dtmf handshakes.
                    </p>
                    <p>
                      <strong>• Caller Caveats:</strong> Verification calls will originate from approved gateways. Be alert to caller ID spoofing; do not approve unsolicited prompts.
                    </p>
                    <p>
                      <strong>• Privacy policy:</strong> Numbers are normalized, masked inside profile metadata, and never exposed to support tools or standard databases.
                    </p>
                  </div>
                </div>

                {/* Accessibility Options */}
                <div className="space-y-2.5">
                  <span className="text-[10px] font-mono font-medium text-zinc-500 uppercase">Accessibility & TDD Preferences</span>
                  <div className="grid grid-cols-3 gap-2">
                    {[
                      { key: 'standard', label: 'Standard TTS' },
                      { key: 'slower_speech', label: 'Slower Voice' },
                      { key: 'text_relay', label: 'Keypad Only' }
                    ].map(opt => (
                      <button
                        key={opt.key}
                        onClick={() => setAccessibilityMode(opt.key as any)}
                        className={`text-[10px] font-mono py-2 rounded-lg border text-center transition-all cursor-pointer ${
                          accessibilityMode === opt.key
                            ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300 font-semibold'
                            : 'bg-zinc-950/30 border-zinc-900 text-zinc-500 hover:border-zinc-900'
                        }`}
                      >
                        {opt.label}
                      </button>
                    ))}
                  </div>
                </div>

                <button
                  onClick={() => setEnrollStep('form')}
                  className="w-full bg-zinc-900 border border-zinc-900 hover:text-white py-3 rounded-xl text-xs font-semibold text-zinc-300 transition-colors cursor-pointer flex items-center justify-center space-x-1.5"
                >
                  <span>Accept and Continue</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            )}

            {/* Sub-State: Form phone entry */}
            {enrollStep === 'form' && (
              <form onSubmit={startEnrollmentCall} className="space-y-5">
                <div>
                  <h3 className="text-xs font-bold text-white font-mono tracking-wider uppercase mb-1">Enter Destination & Label</h3>
                  <p className="text-[11px] text-zinc-500">Provide telephone details. We will dial a test call with a 3-digit verification code.</p>
                </div>

                {/* Country dropdown */}
                <div className="grid grid-cols-3 gap-2">
                  <div className="col-span-2">
                    <label className="text-[10px] text-zinc-500 font-mono block mb-1">Country/Region</label>
                    <select
                      value={countryCode}
                      onChange={(e) => setCountryCode(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2.5 text-xs text-zinc-300 focus:outline-none"
                    >
                      {COUNTRIES.map(c => (
                        <option key={c.code} value={c.code}>{c.name} ({c.prefix})</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="text-[10px] text-zinc-500 font-mono block mb-1">Line Label</label>
                    <input
                      type="text"
                      value={enrollLabel}
                      onChange={(e) => setEnrollLabel(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2.5 text-xs text-zinc-300 focus:outline-none"
                    />
                  </div>
                </div>

                {/* Number input and raw reveal */}
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Raw Number</label>
                  <div className="relative">
                    <input
                      type="tel"
                      required
                      placeholder="5550198"
                      value={phoneNumber}
                      onChange={(e) => setPhoneNumber(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2.5 text-sm text-white focus:outline-none tracking-wide"
                    />
                    <button
                      type="button"
                      onClick={() => setShowRawNumber(!showRawNumber)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-zinc-500 hover:text-zinc-300 cursor-pointer"
                    >
                      {showRawNumber ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                    </button>
                  </div>
                  {showRawNumber && phoneNumber && (
                    <span className="text-[9px] font-mono text-zinc-500 mt-1 block">Normalized format: {formatPhoneNumber(phoneNumber, countryCode)}</span>
                  )}
                </div>

                {/* User consent */}
                <label className="flex items-start space-x-2.5 cursor-pointer">
                  <input
                    type="checkbox"
                    required
                    checked={consentChecked}
                    onChange={(e) => setConsentChecked(e.target.checked)}
                    className="mt-0.5 rounded border-zinc-900 bg-zinc-950 text-emerald-500 focus:ring-emerald-500/20"
                  />
                  <span className="text-[11px] text-zinc-400 leading-normal">
                    I explicitly consent to receive an automated verification call on this device to verify profile ownership. I accept standard carrier network rates if applicable.
                  </span>
                </label>

                {/* Dial call button */}
                <button
                  type="submit"
                  disabled={!consentChecked || !phoneNumber}
                  className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:opacity-40 disabled:cursor-not-allowed text-slate-950 font-bold text-xs py-3.5 rounded-xl transition-all shadow-md shadow-emerald-500/15 cursor-pointer flex items-center justify-center space-x-1.5"
                >
                  <Phone className="w-4 h-4 shrink-0" />
                  <span>Dial Enrollment Test Call</span>
                </button>

                {isReplacing && (
                  <button
                    type="button"
                    onClick={() => { setIsReplacing(false); setPhoneToReplace(null); setEnrollStep('intro'); }}
                    className="w-full text-center text-xs text-zinc-500 hover:text-zinc-400 py-1 transition-colors"
                  >
                    Cancel Replacement Flow
                  </button>
                )}
              </form>
            )}

            {/* Sub-State: Verifying OTP from the enrollment call */}
            {enrollStep === 'verifying' && activeCall && (
              <div className="space-y-6">
                <div className="text-center py-4">
                  <div className="w-12 h-12 bg-blue-500/10 border border-blue-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3 animate-pulse">
                    <RefreshCw className="w-5 h-5 text-blue-400 animate-spin" />
                  </div>
                  <h3 className="text-xs font-semibold tracking-wider text-zinc-300 uppercase font-mono">Verifying Ownership Handshake</h3>
                  <p className="text-[11px] text-zinc-500 mt-1 leading-relaxed">
                    We dialed <span className="font-mono text-zinc-300">{activeCall.destination}</span>. Answer the call simulator on the right to hear the code.
                  </p>
                </div>

                <form onSubmit={handleVerifyOtp} className="space-y-5 bg-zinc-950/60 border border-zinc-900 rounded-2xl p-5">
                  <div>
                    <label className="block text-[10px] font-mono text-zinc-400 uppercase tracking-wider mb-2.5 text-center">Spoken Enrollment Code</label>
                    <div className="flex justify-center space-x-3">
                      <input
                        type="text"
                        maxLength={3}
                        required
                        placeholder="•••"
                        value={otpValue}
                        onChange={(e) => setOtpValue(e.target.value.replace(/\D/g, '').slice(0, 3))}
                        className="w-28 text-center bg-zinc-950 border-2 border-zinc-900 focus:border-blue-500 focus:outline-none rounded-xl text-xl py-2 font-mono tracking-widest text-white"
                      />
                    </div>
                  </div>

                  {otpError && (
                    <p className="text-[11px] text-red-400 text-center bg-red-500/5 py-2 px-3 border border-red-500/10 rounded-lg">{otpError}</p>
                  )}

                  <button
                    type="submit"
                    disabled={otpValue.length < 3}
                    className="w-full bg-blue-500 hover:bg-blue-600 disabled:opacity-40 disabled:cursor-not-allowed text-white font-bold text-xs py-3 rounded-xl transition-all cursor-pointer"
                  >
                    Submit Handshake Code
                  </button>
                </form>

                <button
                  onClick={cancelCall}
                  className="w-full bg-zinc-950 hover:bg-red-500/5 hover:text-red-400 border border-zinc-900 py-3 rounded-xl text-xs font-semibold text-zinc-400 transition-all cursor-pointer"
                >
                  Cancel Enrollment Call
                </button>
              </div>
            )}

            {/* Sub-State: Naming validation / activate */}
            {enrollStep === 'naming' && (
              <div className="space-y-5">
                <div className="text-center py-4">
                  <div className="w-14 h-14 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3">
                    <UserCheck className="w-7 h-7 text-emerald-400" />
                  </div>
                  <h3 className="text-sm font-semibold text-white tracking-wider font-mono">Device Verification Confirmed</h3>
                  <p className="text-xs text-zinc-400 mt-1 max-w-sm mx-auto">
                    Physical ownership proven. Choose an identifiable custom name to finalize enrollment.
                  </p>
                </div>

                <div className="space-y-4 bg-zinc-900 border border-zinc-900 rounded-2xl p-5">
                  <div>
                    <label className="text-[10px] text-zinc-500 font-mono block mb-1">Friendly Label</label>
                    <input
                      type="text"
                      value={enrollLabel}
                      onChange={(e) => setEnrollLabel(e.target.value)}
                      className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2.5 text-xs text-white focus:outline-none"
                    />
                  </div>

                  <button
                    onClick={saveNewAuthenticator}
                    className="w-full bg-emerald-500 hover:bg-emerald-600 font-bold text-xs text-slate-950 py-3 rounded-xl transition-all cursor-pointer"
                  >
                    Finalize & Activate authenticator
                  </button>
                </div>
              </div>
            )}

            {/* Sub-State: Complete card */}
            {enrollStep === 'complete' && (
              <div className="space-y-5 text-center py-4">
                <div className="w-14 h-14 bg-emerald-500/10 border border-emerald-500/20 rounded-2xl flex items-center justify-center mx-auto mb-3">
                  <CheckCircle className="w-7 h-7 text-emerald-400" />
                </div>
                <div>
                  <h3 className="text-sm font-bold text-white font-mono tracking-wider uppercase">Enrollment Complete</h3>
                  <p className="text-xs text-zinc-400 mt-1 max-w-sm mx-auto">
                    New telephone authenticator is now configured in the profile. Notifications of registration have been broadcasted to existing security channels.
                  </p>
                </div>

                <button
                  onClick={() => { setEnrollStep('intro'); setActiveTab('auth'); setAuthStep('chooser'); }}
                  className="w-full bg-zinc-900 border border-zinc-900 hover:text-white py-3 rounded-xl text-xs font-semibold text-zinc-300 transition-colors cursor-pointer"
                >
                  Return to Login Ceremonies
                </button>
              </div>
            )}

            {/* LIFECYCLE MANAGEMENT LIST (Always accessible below lifecycle flow) */}
            {enrollStep === 'intro' && (
              <div className="border-t border-zinc-900 pt-6 space-y-4">
                <div className="flex justify-between items-center">
                  <span className="text-[11px] font-mono font-bold text-zinc-400 uppercase tracking-wider">Active Authenticators Profile ({enrolledPhones.length})</span>
                </div>

                <div className="space-y-3">
                  {enrolledPhones.map(phone => (
                    <div 
                      key={phone.id} 
                      className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4 flex flex-col justify-between space-y-3"
                    >
                      <div className="flex justify-between items-start">
                        <div className="flex items-start space-x-3">
                          <div className={`w-9 h-9 rounded-lg flex items-center justify-center shrink-0 border ${
                            phone.status === 'active' 
                              ? 'bg-zinc-900 border-zinc-900 text-zinc-300' 
                              : 'bg-zinc-950 border-zinc-900 text-zinc-500'
                          }`}>
                            <Phone className="w-4 h-4" />
                          </div>
                          <div>
                            <div className="flex items-center space-x-1.5">
                              <span className="text-xs font-semibold text-white">{phone.label}</span>
                              <span className={`text-[8px] font-mono font-bold px-1.5 py-0.5 rounded uppercase ${
                                phone.status === 'active' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-zinc-800 text-zinc-400'
                              }`}>{phone.status}</span>
                            </div>
                            <span className="text-xs font-mono text-zinc-400 block mt-0.5">{phone.maskedNumber}</span>
                          </div>
                        </div>

                        {/* Interactive operations */}
                        <div className="flex space-x-1.5">
                          <button
                            title={phone.status === 'active' ? 'Suspend factor' : 'Activate factor'}
                            onClick={() => togglePhoneStatus(phone.id)}
                            className="p-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-900 hover:border-zinc-900 text-zinc-400 hover:text-white rounded-lg transition-all cursor-pointer"
                          >
                            <Shield className="w-3.5 h-3.5" />
                          </button>
                          <button
                            title="Replace authenticator"
                            onClick={() => triggerReplacement(phone)}
                            className="p-1.5 bg-zinc-900 hover:bg-zinc-800 border border-zinc-900 hover:border-zinc-900 text-zinc-400 hover:text-white rounded-lg transition-all cursor-pointer"
                          >
                            <RefreshCw className="w-3.5 h-3.5" />
                          </button>
                          <button
                            title="Deactivate and remove factor"
                            onClick={() => removePhone(phone.id)}
                            className="p-1.5 bg-zinc-900 hover:bg-red-500/10 border border-zinc-900 hover:border-red-500/20 text-zinc-400 hover:text-red-400 rounded-lg transition-all cursor-pointer"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>

                      <div className="grid grid-cols-2 gap-3 text-[10px] text-zinc-500 border-t border-zinc-900 pt-3">
                        <div>
                          <span className="block font-mono">ENROLLED DATE:</span>
                          <span className="text-zinc-400 font-mono">{new Date(phone.createdAt).toLocaleDateString()}</span>
                        </div>
                        <div>
                          <span className="block font-mono">LAST USED DATE:</span>
                          <span className="text-zinc-400 font-mono">{phone.lastUsedAt ? new Date(phone.lastUsedAt).toLocaleDateString() : 'Never'}</span>
                        </div>
                      </div>

                    </div>
                  ))}
                </div>
              </div>
            )}

          </div>
        )}

      </div>
    </div>
  );
}
