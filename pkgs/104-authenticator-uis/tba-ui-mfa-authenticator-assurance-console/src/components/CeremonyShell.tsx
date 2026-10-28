/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  Key, 
  Smartphone, 
  Mail, 
  Lock, 
  RefreshCw, 
  Fingerprint, 
  AlertTriangle, 
  CheckCircle, 
  Info, 
  AlertCircle, 
  ChevronRight, 
  Clock, 
  Copy, 
  Check, 
  ArrowLeft,
  Loader2
} from 'lucide-react';
import { MfaFactor, MfaPolicy, MfaCeremony, FactorType, AuditEvent } from '../types';

interface CeremonyShellProps {
  policy: MfaPolicy;
  enrolledFactors: MfaFactor[];
  onCeremonyComplete: (amr: string[], auditRef: string) => void;
  onCancel: () => void;
  addAuditEvent: (event: Omit<AuditEvent, 'id' | 'timestamp'>) => void;
  providerHealth: Record<string, 'operational' | 'degraded' | 'outage'>;
}

export default function CeremonyShell({
  policy,
  enrolledFactors,
  onCeremonyComplete,
  onCancel,
  addAuditEvent,
  providerHealth,
}: CeremonyShellProps) {
  // Scenario Configs
  const [transactionType, setTransactionType] = useState<'signin' | 'wire' | 'ssh'>('wire');
  const [useRecovery, setUseRecovery] = useState(false);
  
  // Ceremony State
  const [step, setStep] = useState<'intro' | 'chooser' | 'challenge' | 'external_wait' | 'success' | 'failed_blocked'>('intro');
  const [achievedClasses, setAchievedClasses] = useState<string[]>(['Knowledge']); // assumed pwd verified first
  const [amr, setAmr] = useState<string[]>(['pwd']);
  const [selectedFactor, setSelectedFactor] = useState<MfaFactor | null>(null);
  
  // Challenge inputs & status
  const [otpValue, setOtpValue] = useState<string[]>(['', '', '', '', '', '']);
  const [inputError, setInputError] = useState<string | null>(null);
  const [attemptsRemaining, setAttemptsRemaining] = useState(policy.lockoutThreshold);
  const [expiryTime, setExpiryTime] = useState(120); // 2 minutes
  const [pushStatus, setPushStatus] = useState<'idle' | 'sent' | 'approved' | 'timed_out'>('idle');
  const [emailOtpSent, setEmailOtpSent] = useState(false);
  const [correctOtp, setCorrectOtp] = useState('123456');
  const [isVerifying, setIsVerifying] = useState(false);
  const [copiedAuditRef, setCopiedAuditRef] = useState(false);
  
  // Session details
  const [auditRef, setAuditRef] = useState(`tx_amr_${Math.random().toString(36).substring(2, 9).toUpperCase()}`);

  const otpInputsRef = useRef<(HTMLInputElement | null)[]>([]);

  // Timer effect for challenge expiry
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (step === 'challenge' || step === 'external_wait') {
      interval = setInterval(() => {
        setExpiryTime((prev) => {
          if (prev <= 1) {
            setInputError('Challenge expired. Please request a new challenge.');
            setStep('chooser');
            addAuditEvent({
              eventType: 'CHALLENGE_EXPIRED',
              subject: 'jane.doe@acme.com',
              status: 'warning',
              factorType: selectedFactor?.type,
              policyVersion: policy.version,
              detail: `MFA challenge expired for factor: ${selectedFactor?.name || 'unknown'}`,
              ipAddress: '192.168.1.45',
              userAgent: navigator.userAgent,
            });
            return 120;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [step, selectedFactor, policy.version]);

  // Simulate TOTP Code rotation
  const [totpCountdown, setTotpCountdown] = useState(18);
  useEffect(() => {
    const timer = setInterval(() => {
      setTotpCountdown((prev) => {
        if (prev <= 1) {
          // Rotate code
          const newCode = Math.floor(100000 + Math.random() * 900000).toString();
          setCorrectOtp(newCode);
          return 30;
        }
        return prev - 1;
      });
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  const getRequiredFactorClasses = () => {
    if (transactionType === 'signin') {
      return ['Possession']; // Require single second factor class
    } else if (transactionType === 'wire') {
      return ['Possession', 'Inherence']; // require multi-factor class independence
    } else {
      return ['Possession', 'Inherence']; // SSH requires phishing resistant + multi-factor
    }
  };

  const requiredClasses = getRequiredFactorClasses();

  // Reset Ceremony on Scenario Change
  const initCeremony = (type: 'signin' | 'wire' | 'ssh') => {
    setTransactionType(type);
    setStep('intro');
    setAchievedClasses(['Knowledge']);
    setAmr(['pwd']);
    setSelectedFactor(null);
    setInputError(null);
    setAttemptsRemaining(policy.lockoutThreshold);
    setExpiryTime(120);
    setPushStatus('idle');
    setUseRecovery(false);
    setOtpValue(['', '', '', '', '', '']);
    setAuditRef(`tx_amr_${Math.random().toString(36).substring(2, 9).toUpperCase()}`);
    
    addAuditEvent({
      eventType: 'CEREMONY_RECONFIGURED',
      subject: 'jane.doe@acme.com',
      status: 'info',
      policyVersion: policy.version,
      detail: `Ceremony scenario switched to: ${type === 'signin' ? 'Regular Sign-in' : type === 'wire' ? 'High-Value Wire Transfer' : 'SSH Key Injection'}`,
      ipAddress: '192.168.1.45',
      userAgent: navigator.userAgent,
    });
  };

  const handleSelectFactor = (factor: MfaFactor) => {
    // Check provider health
    if (providerHealth[factor.type] === 'outage') {
      setInputError(`Provider Outage: The ${factor.type.toUpperCase()} authenticator system is currently offline.`);
      return;
    }

    setSelectedFactor(factor);
    setInputError(null);
    setExpiryTime(120);
    setOtpValue(['', '', '', '', '', '']);
    
    // Set dummy expected codes
    if (factor.type === 'totp') {
      setCorrectOtp(Math.floor(100000 + Math.random() * 900000).toString());
    } else if (factor.type === 'email_otp') {
      setCorrectOtp('882941');
      setEmailOtpSent(true);
    }

    if (factor.type === 'push') {
      setStep('external_wait');
      setPushStatus('sent');
      // Simulate external push notification latency
      setTimeout(() => {
        // Auto-approve after 3.5 seconds
        setPushStatus('approved');
      }, 3500);
    } else {
      setStep('challenge');
    }

    addAuditEvent({
      eventType: 'FACTOR_SELECTED',
      subject: 'jane.doe@acme.com',
      status: 'info',
      factorType: factor.type,
      factorClass: factor.factorClass,
      policyVersion: policy.version,
      detail: `Selected factor: ${factor.name} (${factor.factorClass})`,
      ipAddress: '192.168.1.45',
      userAgent: navigator.userAgent,
    });
  };

  const handleVerifyOtp = (customOtp?: string) => {
    const code = customOtp || otpValue.join('');
    if (code.length < 6) {
      setInputError('Please enter a complete 6-digit verification code.');
      return;
    }

    setIsVerifying(true);
    setInputError(null);

    setTimeout(() => {
      setIsVerifying(false);
      if (code === correctOtp || code === '999999' || useRecovery) {
        // Success
        handleFactorSuccess();
      } else {
        const remaining = attemptsRemaining - 1;
        setAttemptsRemaining(remaining);
        
        addAuditEvent({
          eventType: 'CHALLENGE_FAILED',
          subject: 'jane.doe@acme.com',
          status: 'failure',
          factorType: selectedFactor?.type,
          factorClass: selectedFactor?.factorClass,
          policyVersion: policy.version,
          detail: `Incorrect verification code. Attempts remaining: ${remaining}`,
          ipAddress: '192.168.1.45',
          userAgent: navigator.userAgent,
        });

        if (remaining <= 0) {
          setStep('failed_blocked');
          addAuditEvent({
            eventType: 'ACCOUNT_LOCKED_MFA',
            subject: 'jane.doe@acme.com',
            status: 'warning',
            policyVersion: policy.version,
            detail: `MFA rate limits exhausted. Safe lockout applied. Session terminated.`,
            ipAddress: '192.168.1.45',
            userAgent: navigator.userAgent,
          });
        } else {
          setInputError(`Verification code incorrect. ${remaining} attempts remaining.`);
          setOtpValue(['', '', '', '', '', '']);
          if (otpInputsRef.current[0]) otpInputsRef.current[0].focus();
        }
      }
    }, 800);
  };

  const handlePushApprove = () => {
    setPushStatus('approved');
    handleFactorSuccess();
  };

  const handlePushReject = () => {
    setPushStatus('idle');
    setInputError('Push notification approval was rejected by your device.');
    setStep('chooser');
    
    addAuditEvent({
      eventType: 'PUSH_REJECTED',
      subject: 'jane.doe@acme.com',
      status: 'warning',
      factorType: 'push',
      factorClass: 'Possession',
      policyVersion: policy.version,
      detail: 'Interactive push approval dismissed/denied by user device.',
      ipAddress: '192.168.1.45',
      userAgent: navigator.userAgent,
    });
  };

  const handlePasskeyVerify = () => {
    setIsVerifying(true);
    setInputError(null);

    // Simulate WebAuthn browser API call
    setTimeout(() => {
      setIsVerifying(false);
      handleFactorSuccess();
    }, 1500);
  };

  const handleFactorSuccess = () => {
    const factor = selectedFactor || (useRecovery ? enrolledFactors.find(f => f.type === 'recovery') : null);
    if (!factor) return;

    // Check phishing resistance if policy enforces it
    if (policy.enforcePhishingResistant && !factor.phishingResistant && transactionType === 'ssh') {
      setInputError('This factor does not satisfy the phishing-resistant policy rule required for SSH credentials.');
      setStep('chooser');
      return;
    }

    const updatedAchieved = Array.from(new Set([...achievedClasses, factor.factorClass]));
    setAchievedClasses(updatedAchieved);

    const amrCodes = [...amr];
    if (factor.type === 'passkey' || factor.type === 'security_key') {
      amrCodes.push('fido2', 'hw');
    } else if (factor.type === 'totp') {
      amrCodes.push('otp');
    } else if (factor.type === 'push') {
      amrCodes.push('push');
    } else if (factor.type === 'email_otp') {
      amrCodes.push('otp', 'mail');
    } else if (factor.type === 'recovery') {
      amrCodes.push('recovery_bypass');
    }
    setAmr(amrCodes);

    addAuditEvent({
      eventType: 'FACTOR_VERIFIED',
      subject: 'jane.doe@acme.com',
      status: 'success',
      factorType: factor.type,
      factorClass: factor.factorClass,
      policyVersion: policy.version,
      detail: `Successfully verified factor: ${factor.name} (${factor.factorClass}). AMR update: ${amrCodes.join(', ')}`,
      ipAddress: '192.168.1.45',
      userAgent: navigator.userAgent,
    });

    // Check if the overall policy is satisfied:
    // Independence check: we need all of requiredClasses to be in achievedClasses
    const allSatisfied = requiredClasses.every(cls => updatedAchieved.includes(cls));

    if (allSatisfied) {
      setStep('success');
      addAuditEvent({
        eventType: 'CEREMONY_COMPLETE',
        subject: 'jane.doe@acme.com',
        status: 'success',
        policyVersion: policy.version,
        detail: `All factor policies satisfied (${requiredClasses.join(' + ')}). Issuing AMR token: mfa + ${amrCodes.join(' + ')}`,
        ipAddress: '192.168.1.45',
        userAgent: navigator.userAgent,
      });
    } else {
      // Need another factor!
      setInputError(`Excellent. Verified ${factor.factorClass} class. Remaining security requirements: ${requiredClasses.filter(c => !updatedAchieved.includes(c)).join(', ')}`);
      setStep('chooser');
      setSelectedFactor(null);
    }
  };

  const handleOtpChange = (index: number, val: string) => {
    if (/^[0-9]$/.test(val) || val === '') {
      const nextOtp = [...otpValue];
      nextOtp[index] = val;
      setOtpValue(nextOtp);

      // Focus next input
      if (val !== '' && index < 5) {
        if (otpInputsRef.current[index + 1]) {
          otpInputsRef.current[index + 1]?.focus();
        }
      }
    }
  };

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && otpValue[index] === '' && index > 0) {
      const nextOtp = [...otpValue];
      nextOtp[index - 1] = '';
      setOtpValue(nextOtp);
      if (otpInputsRef.current[index - 1]) {
        otpInputsRef.current[index - 1]?.focus();
      }
    }
  };

  const triggerRecoveryCode = () => {
    setUseRecovery(true);
    setSelectedFactor(enrolledFactors.find(f => f.type === 'recovery') || null);
    setInputError(null);
    setExpiryTime(120);
    setOtpValue(['', '', '', '', '', '']);
    setStep('challenge');
  };

  const handleResetCeremony = () => {
    initCeremony(transactionType);
  };

  // Helper to get relative style/colors per factor
  const getFactorIcon = (type: FactorType) => {
    switch (type) {
      case 'passkey': return <Fingerprint className="w-5 h-5" />;
      case 'security_key': return <Key className="w-5 h-5" />;
      case 'totp': return <Shield className="w-5 h-5" />;
      case 'push': return <Smartphone className="w-5 h-5" />;
      case 'email_otp': return <Mail className="w-5 h-5" />;
      default: return <Lock className="w-5 h-5" />;
    }
  };

  const renderScenarioTabs = () => {
    return (
      <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200 mb-6 w-full text-xs" id="scenario-selector">
        <button
          onClick={() => initCeremony('signin')}
          className={`flex-1 py-1.5 px-3 rounded-md font-medium transition-all ${transactionType === 'signin' ? 'bg-white text-slate-800 shadow-xs border border-slate-200/50' : 'text-slate-500 hover:text-slate-700'}`}
        >
          Sign-in (P1 class required)
        </button>
        <button
          onClick={() => initCeremony('wire')}
          className={`flex-1 py-1.5 px-3 rounded-md font-medium transition-all ${transactionType === 'wire' ? 'bg-white text-slate-800 shadow-xs border border-slate-200/50' : 'text-slate-500 hover:text-slate-700'}`}
        >
          Wire Transfer (P1 + P3 required)
        </button>
        <button
          onClick={() => initCeremony('ssh')}
          className={`flex-1 py-1.5 px-3 rounded-md font-medium transition-all ${transactionType === 'ssh' ? 'bg-white text-slate-800 shadow-xs border border-slate-200/50' : 'text-slate-500 hover:text-slate-700'}`}
        >
          SSH Admin Key (Strict Phishing Resistant)
        </button>
      </div>
    );
  };

  return (
    <div className="flex-1 flex flex-col overflow-y-auto" id="ceremony-container">
      {/* Top Banner indicating Simulation Scenario */}
      <div className="bg-slate-50 border-b border-slate-200 p-4 shrink-0 flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <span className="text-[10px] font-bold uppercase tracking-wider text-slate-400">Ceremony Scenario</span>
          <h2 className="text-sm font-semibold text-slate-800 flex items-center gap-2">
            {transactionType === 'signin' && '🔐 Standard Core Application Login'}
            {transactionType === 'wire' && '💸 High-Value ACH Wire Outflow ($50,000.00)'}
            {transactionType === 'ssh' && '🛠️ Production SSH Keys Injection / Cluster Re-config'}
            <span className="px-2 py-0.5 bg-indigo-50 text-indigo-700 text-[10px] rounded border border-indigo-200/50">
              AMR: {amr.join(', ')}
            </span>
          </h2>
        </div>
        <div className="text-[11px] text-slate-500 flex items-center gap-2">
          <span>Bound transaction ID:</span>
          <code className="bg-white border border-slate-200 px-2 py-0.5 rounded text-indigo-600 font-mono font-bold text-xs">{auditRef}</code>
        </div>
      </div>

      <div className="p-6 max-w-2xl mx-auto w-full flex-1 flex flex-col justify-center">
        {/* Scenario controls */}
        {renderScenarioTabs()}

        {/* Dynamic Step Renderer */}
        {step === 'intro' && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in" id="step-intro">
            <div className="text-center mb-6">
              <div className="w-14 h-14 bg-indigo-50 border border-indigo-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-indigo-600 shadow-xs">
                <Shield className="w-8 h-8" />
              </div>
              <h1 className="text-xl font-bold text-slate-900 tracking-tight">Additional Verification Required</h1>
              <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
                Security policy for <strong>{transactionType === 'wire' ? 'ACH transfers' : transactionType === 'ssh' ? 'SSH key updates' : 'Secure Core sign-in'}</strong> requires a stronger assurance level.
              </p>
            </div>

            {/* Assurance Matrix visualizer */}
            <div className="bg-white border border-slate-200 rounded-xl p-4 mb-6 shadow-xs">
              <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider mb-3">Assurance Objective Verification</h3>
              <div className="space-y-3">
                {/* 1. Knowledge class */}
                <div className="flex items-center justify-between border-b border-slate-50 pb-2.5">
                  <div className="flex items-center gap-2">
                    <div className="w-6 h-6 rounded-md bg-emerald-50 text-emerald-700 flex items-center justify-center text-xs font-bold">1</div>
                    <div>
                      <div className="text-xs font-semibold text-slate-800">Knowledge Class</div>
                      <div className="text-[10px] text-slate-400 font-mono">pwd verified (Password)</div>
                    </div>
                  </div>
                  <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold rounded-full border border-emerald-100">
                    ACHIEVED
                  </span>
                </div>

                {/* 2. Possession class */}
                <div className="flex items-center justify-between border-b border-slate-50 pb-2.5">
                  <div className="flex items-center gap-2">
                    <div className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold ${requiredClasses.includes('Possession') ? 'bg-indigo-50 text-indigo-600' : 'bg-slate-100 text-slate-400'}`}>2</div>
                    <div>
                      <div className={`text-xs font-semibold ${requiredClasses.includes('Possession') ? 'text-slate-800' : 'text-slate-400'}`}>Possession Class</div>
                      <div className="text-[10px] text-slate-400 font-mono">WebAuthn token, Push callback, or OTP</div>
                    </div>
                  </div>
                  {achievedClasses.includes('Possession') ? (
                    <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold rounded-full border border-emerald-100">ACHIEVED</span>
                  ) : requiredClasses.includes('Possession') ? (
                    <span className="px-2 py-0.5 bg-amber-50 text-amber-700 text-[10px] font-bold rounded-full border border-amber-100 animate-pulse">PENDING</span>
                  ) : (
                    <span className="px-2 py-0.5 bg-slate-50 text-slate-400 text-[10px] font-bold rounded-full border border-slate-100">OPTIONAL</span>
                  )}
                </div>

                {/* 3. Inherence class */}
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2">
                    <div className={`w-6 h-6 rounded-md flex items-center justify-center text-xs font-bold ${requiredClasses.includes('Inherence') ? 'bg-indigo-50 text-indigo-600' : 'bg-slate-100 text-slate-400'}`}>3</div>
                    <div>
                      <div className={`text-xs font-semibold ${requiredClasses.includes('Inherence') ? 'text-slate-800' : 'text-slate-400'}`}>Inherence Class</div>
                      <div className="text-[10px] text-slate-400 font-mono">Biometric Passkey / Device Hello</div>
                    </div>
                  </div>
                  {achievedClasses.includes('Inherence') ? (
                    <span className="px-2 py-0.5 bg-emerald-50 text-emerald-700 text-[10px] font-bold rounded-full border border-emerald-100">ACHIEVED</span>
                  ) : requiredClasses.includes('Inherence') ? (
                    <span className="px-2 py-0.5 bg-amber-50 text-amber-700 text-[10px] font-bold rounded-full border border-amber-100 animate-pulse">PENDING</span>
                  ) : (
                    <span className="px-2 py-0.5 bg-slate-50 text-slate-400 text-[10px] font-bold rounded-full border border-slate-100">OPTIONAL</span>
                  )}
                </div>
              </div>
            </div>

            {/* Phishing Resistant Highlight */}
            {transactionType === 'ssh' && (
              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800 flex items-start gap-2 mb-6">
                <AlertCircle className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  <strong className="font-semibold block">Strict Cryptographic Mandate</strong>
                  The tenant policy dictates that SSH credentials MUST be validated via hardware-bound phishing-resistant key tokens only. Standard SMS or email codes are locked out for this transaction.
                </div>
              </div>
            )}

            <button
              onClick={() => setStep('chooser')}
              className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2.5 rounded-lg text-sm shadow-md transition-all flex items-center justify-center gap-2"
            >
              Initiate Multi-Factor Ceremony <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        )}

        {step === 'chooser' && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in" id="step-chooser">
            <div className="mb-5 flex justify-between items-center">
              <div>
                <h1 className="text-lg font-bold text-slate-900">Choose Verification Factor</h1>
                <p className="text-xs text-slate-500">Select one of your policy-approved security tokens below.</p>
              </div>
              <span className="text-[10px] font-bold bg-slate-100 text-slate-600 border border-slate-200 px-2 py-0.5 rounded uppercase">
                {requiredClasses.filter(c => !achievedClasses.includes(c)).length} Factor(s) Remaining
              </span>
            </div>

            {inputError && (
              <div className="mb-4 bg-rose-50 border border-rose-200 text-rose-800 p-3 rounded-lg text-xs flex items-start gap-2">
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
                <span>{inputError}</span>
              </div>
            )}

            <div className="space-y-3 mb-6 max-h-[320px] overflow-y-auto pr-1">
              {enrolledFactors.map((factor) => {
                // Determine eligibility based on policy rules
                const isPhishingResistantRequirementMet = !policy.enforcePhishingResistant || factor.phishingResistant || transactionType !== 'ssh';
                const isFactorAlreadyUsed = amr.includes(factor.type === 'passkey' ? 'fido2' : factor.type === 'totp' ? 'otp' : factor.type);
                const isOfflineRecovery = factor.type === 'recovery';
                
                // Allow fallback if provider health is degraded, but NOT if it is "outage"
                const providerStatus = providerHealth[factor.type] || 'operational';
                const isOutage = providerStatus === 'outage';

                const isEligible = isPhishingResistantRequirementMet && !isFactorAlreadyUsed && !isOfflineRecovery && !isOutage;

                // Skip showing recovery code in general factor list
                if (isOfflineRecovery) return null;

                return (
                  <div
                    key={factor.id}
                    onClick={() => isEligible && handleSelectFactor(factor)}
                    className={`p-3.5 bg-white border rounded-xl flex items-center justify-between transition-all ${
                      isEligible 
                        ? 'hover:border-indigo-500 cursor-pointer border-slate-200 hover:shadow-xs group' 
                        : 'opacity-50 cursor-not-allowed border-slate-200 bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <div className={`w-9 h-9 rounded-full flex items-center justify-center ${
                        isEligible 
                          ? 'bg-indigo-50 text-indigo-600 group-hover:bg-indigo-100' 
                          : 'bg-slate-100 text-slate-400'
                      }`}>
                        {getFactorIcon(factor.type)}
                      </div>
                      <div className="text-left">
                        <div className="font-bold text-xs text-slate-800 flex items-center gap-1.5">
                          {factor.name}
                          {factor.phishingResistant && (
                            <span className="px-1 py-0.2 bg-emerald-100 text-emerald-800 text-[8px] font-bold rounded-xs uppercase tracking-tight">
                              Phishing Resistant
                            </span>
                          )}
                          {providerStatus === 'degraded' && (
                            <span className="px-1 py-0.2 bg-amber-100 text-amber-800 text-[8px] font-bold rounded-xs uppercase">
                              Degraded
                            </span>
                          )}
                        </div>
                        <div className="text-[10px] text-slate-500 mt-0.5">
                          {factor.factorClass} • {factor.deviceName || 'Hardware device'} • Last active {factor.lastUsedAt ? 'recently' : 'never'}
                        </div>
                      </div>
                    </div>
                    <div>
                      {isEligible ? (
                        <ChevronRight className="w-4 h-4 text-slate-400 group-hover:text-indigo-500" />
                      ) : (
                        <div className="flex items-center gap-1 text-[10px] text-slate-400 font-medium bg-slate-100 px-2 py-0.5 rounded border border-slate-200">
                          <Lock className="w-3 h-3 shrink-0" />
                          {!isPhishingResistantRequirementMet ? 'Policy Blocked' : isOutage ? 'Outage' : 'Already Used'}
                        </div>
                      )}
                    </div>
                  </div>
                );
              })}
            </div>

            <div className="flex items-center justify-between border-t border-slate-200 pt-4 mt-auto">
              <button
                onClick={triggerRecoveryCode}
                className="text-xs font-semibold text-slate-500 hover:text-indigo-600 hover:underline flex items-center gap-1"
              >
                <AlertTriangle className="w-3.5 h-3.5" />
                Use emergency recovery bypass
              </button>
              <button
                onClick={onCancel}
                className="px-4 py-2 text-xs font-bold text-slate-600 hover:bg-slate-100 rounded-lg transition-colors"
              >
                Cancel Ceremony
              </button>
            </div>
          </div>
        )}

        {step === 'challenge' && selectedFactor && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in" id="step-challenge">
            <div className="flex items-center gap-2 text-xs text-slate-400 font-semibold mb-4 cursor-pointer hover:text-slate-600" onClick={() => setStep('chooser')}>
              <ArrowLeft className="w-3.5 h-3.5" /> Back to Factors
            </div>

            <div className="text-center mb-6">
              <div className="w-12 h-12 bg-indigo-50 text-indigo-600 rounded-xl flex items-center justify-center mx-auto mb-3 shadow-xs">
                {getFactorIcon(selectedFactor.type)}
              </div>
              <h1 className="text-base font-bold text-slate-900">Verify Identity via {selectedFactor.name}</h1>
              <p className="text-xs text-slate-500 mt-0.5">
                Factor Class: <span className="font-semibold text-indigo-600">{selectedFactor.factorClass}</span> • Session binds: <code className="bg-slate-100 px-1 py-0.2 rounded font-mono text-[10px]">{auditRef.slice(0, 8)}</code>
              </p>
            </div>

            {inputError && (
              <div className="mb-4 bg-rose-50 border border-rose-200 text-rose-800 p-2.5 rounded-lg text-xs flex items-start gap-2">
                <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                <span>{inputError}</span>
              </div>
            )}

            {/* TOTP / Email OTP verification interface */}
            {(selectedFactor.type === 'totp' || selectedFactor.type === 'email_otp' || selectedFactor.type === 'recovery') && (
              <div className="bg-white border border-slate-200 rounded-xl p-5 mb-6 shadow-xs text-center">
                <div className="text-xs text-slate-500 mb-4 font-medium">
                  {selectedFactor.type === 'totp' && 'Enter the rotating 6-digit code from your authenticator app.'}
                  {selectedFactor.type === 'email_otp' && 'A secure 6-digit pin has been transmitted to your registered corporate address.'}
                  {selectedFactor.type === 'recovery' && 'Verify your emergency master recovery code below to bypass traditional factors.'}
                </div>

                {/* Simulated Device Code Help Box */}
                {selectedFactor.type === 'totp' && (
                  <div className="bg-indigo-50/50 border border-indigo-100 rounded-lg p-2.5 mb-5 text-[11px] text-indigo-800 flex items-center justify-between">
                    <span className="flex items-center gap-1">
                      <Clock className="w-3.5 h-3.5 shrink-0 text-indigo-500" />
                      Dynamic Code rotates in <strong>{totpCountdown}s</strong>
                    </span>
                    <span className="flex items-center gap-1">
                      Expected code: <code className="bg-white border border-indigo-200 px-1.5 py-0.5 rounded font-mono font-bold text-slate-700">{correctOtp}</code>
                      <button 
                        onClick={() => {
                          setOtpValue(correctOtp.split(''));
                          addAuditEvent({
                            eventType: 'AUTOFILL_OTP',
                            subject: 'jane.doe@acme.com',
                            status: 'info',
                            policyVersion: policy.version,
                            detail: 'Developer tools: auto-populated current simulated TOTP code',
                            ipAddress: '192.168.1.45',
                            userAgent: navigator.userAgent,
                          });
                        }} 
                        className="text-xs text-indigo-600 underline font-bold ml-1"
                      >
                        Autofill
                      </button>
                    </span>
                  </div>
                )}

                {selectedFactor.type === 'email_otp' && (
                  <div className="bg-slate-50 border border-slate-200 rounded-lg p-2.5 mb-5 text-left text-[11px]">
                    <div className="font-bold text-slate-700 mb-1 flex items-center gap-1.5">
                      <Mail className="w-3.5 h-3.5 text-indigo-500" />
                      Virtual Corporate Mail Inbox
                    </div>
                    <div className="bg-white p-2 rounded border border-slate-100 font-mono text-slate-600 leading-tight">
                      <div><strong>Subject:</strong> Acme MFA Challenge code</div>
                      <div><strong>To:</strong> j***@acme.com</div>
                      <div className="mt-1.5 text-slate-800 font-sans border-t border-slate-100 pt-1.5">
                        Your multi-factor one-time security challenge pin is: <strong className="font-mono text-xs text-indigo-600 bg-indigo-50 px-1 rounded">{correctOtp}</strong>
                      </div>
                    </div>
                  </div>
                )}

                {selectedFactor.type === 'recovery' && (
                  <div className="bg-amber-50 border border-amber-200 rounded-lg p-2.5 mb-5 text-left text-[11px] text-amber-800">
                    <div className="font-bold mb-1 flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5 shrink-0" />
                      Reduced Assurance Warning
                    </div>
                    Bypassing MFA using recovery codes satisfies authentication but marks the session as <strong>REDUCED ASSURANCE</strong>. Sensitive actions may still require full administrative review.
                    <div className="mt-2 text-[10px] text-slate-600 font-mono bg-white p-1.5 rounded border border-slate-200">
                      Master recovery bypass code is: <code className="font-bold text-amber-700">999999</code>
                    </div>
                  </div>
                )}

                {/* Interactive Code Fields */}
                <div className="flex gap-2.5 justify-center mb-5">
                  {otpValue.map((num, i) => (
                    <input
                      key={i}
                      ref={(el) => { otpInputsRef.current[i] = el; }}
                      type="text"
                      maxLength={1}
                      value={num}
                      onChange={(e) => handleOtpChange(i, e.target.value)}
                      onKeyDown={(e) => handleOtpKeyDown(i, e)}
                      className="w-10 h-12 text-center text-lg font-bold text-indigo-600 bg-slate-50 border border-slate-300 rounded-lg focus:outline-hidden focus:ring-2 focus:ring-indigo-500 focus:bg-white"
                    />
                  ))}
                </div>

                <div className="flex gap-3">
                  <button
                    onClick={() => {
                      setOtpValue(['', '', '', '', '', '']);
                      if (otpInputsRef.current[0]) otpInputsRef.current[0].focus();
                    }}
                    className="flex-1 py-2 border border-slate-200 rounded-lg text-xs font-bold text-slate-600 hover:bg-slate-50 transition-colors"
                  >
                    Reset Code
                  </button>
                  <button
                    onClick={() => handleVerifyOtp()}
                    disabled={isVerifying}
                    className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white rounded-lg text-xs font-bold shadow-xs transition-colors flex items-center justify-center gap-1.5"
                  >
                    {isVerifying && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                    Confirm Verification Pin
                  </button>
                </div>
              </div>
            )}

            {/* Passkey / Security Key Biometric Animation Screen */}
            {(selectedFactor.type === 'passkey' || selectedFactor.type === 'security_key') && (
              <div className="bg-white border border-slate-200 rounded-xl p-6 mb-6 shadow-xs text-center flex flex-col items-center">
                <div className="text-xs text-slate-500 mb-6 max-w-sm">
                  {selectedFactor.type === 'passkey' 
                    ? 'Acme Authentication Engine is interfacing with your web browser biometric credentials. Please scan your Face/Fingerprint when prompted by the operating system.' 
                    : 'Insert your physical security token into your USB port and tap the gold contact ring when flashing.'
                  }
                </div>

                {/* Animated Fingerprint Scan Container */}
                <div className="relative mb-6">
                  <div className={`w-24 h-24 rounded-full border-2 flex items-center justify-center ${isVerifying ? 'border-indigo-600 bg-indigo-50' : 'border-slate-200 bg-slate-50'} transition-all`}>
                    <Fingerprint className={`w-14 h-14 ${isVerifying ? 'text-indigo-600 animate-pulse' : 'text-slate-400'}`} />
                  </div>
                  {isVerifying && (
                    <span className="absolute inset-x-0 -bottom-2 mx-auto bg-indigo-600 text-white font-bold text-[9px] uppercase px-2 py-0.5 rounded-full tracking-wider animate-bounce">
                      Interfacing...
                    </span>
                  )}
                </div>

                <div className="w-full flex gap-3">
                  <button
                    onClick={handlePasskeyVerify}
                    disabled={isVerifying}
                    className="flex-1 py-2.5 bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg text-xs font-bold shadow-md shadow-indigo-100 transition-all flex items-center justify-center gap-1.5"
                  >
                    {isVerifying && <Loader2 className="w-3.5 h-3.5 animate-spin" />}
                    Trigger Device {selectedFactor.type === 'passkey' ? 'Biometrics' : 'Hardware Tap'}
                  </button>
                </div>
              </div>
            )}

            {/* General Info / Details */}
            <div className="text-center text-[10px] text-slate-400">
              Your connection is cryptographically signed and bound to <code className="bg-slate-100 px-1.5 py-0.5 rounded">ECDSA-SHA256</code>
            </div>
          </div>
        )}

        {step === 'external_wait' && selectedFactor && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in text-center" id="step-external-wait">
            <div className="w-14 h-14 bg-indigo-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-indigo-600 shadow-xs relative">
              <Smartphone className="w-8 h-8 animate-bounce" />
              <div className="absolute top-0 right-0 w-3 h-3 bg-indigo-500 rounded-full border-2 border-white animate-ping"></div>
            </div>

            <h1 className="text-base font-bold text-slate-900">Awaiting External Mobile Approval</h1>
            <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
              A push notification has been delivered to your registered mobile device: <strong>iPhone 15 Pro</strong>. Tap Approve to authorize this transaction.
            </p>

            {/* Mobile device simulator card */}
            <div className="bg-slate-950 text-white w-64 rounded-3xl mx-auto my-6 p-4 border-4 border-slate-800 shadow-xl relative overflow-hidden text-left">
              <div className="w-16 h-4 bg-slate-800 rounded-full mx-auto mb-4"></div>
              <div className="text-[10px] text-indigo-400 font-bold uppercase tracking-wider mb-1">Acme Secure SSO</div>
              <div className="text-xs font-bold leading-tight">Verify Transaction?</div>
              <p className="text-[9px] text-slate-400 mt-1 mb-4 leading-normal">
                <strong>Action:</strong> {transactionType === 'wire' ? 'Transfer $50,000.00' : 'Secure System Access'}<br />
                <strong>Reference:</strong> {auditRef.slice(0, 8)}
              </p>

              {pushStatus === 'sent' ? (
                <div className="flex gap-2 mt-2">
                  <button
                    onClick={handlePushReject}
                    className="flex-1 bg-rose-600 hover:bg-rose-700 text-white text-[9px] font-bold py-1.5 rounded-md text-center"
                  >
                    Reject
                  </button>
                  <button
                    onClick={handlePushApprove}
                    className="flex-1 bg-emerald-600 hover:bg-emerald-700 text-white text-[9px] font-bold py-1.5 rounded-md text-center"
                  >
                    Approve
                  </button>
                </div>
              ) : pushStatus === 'approved' ? (
                <div className="bg-emerald-950/50 border border-emerald-800 rounded-lg p-2 flex items-center gap-1.5 text-[10px] text-emerald-400 font-bold">
                  <CheckCircle className="w-3.5 h-3.5 shrink-0" /> Verified via Mobile Push Callback
                </div>
              ) : (
                <div className="text-slate-500 text-[9px] text-center italic py-2">Challenge complete</div>
              )}
            </div>

            <div className="flex items-center justify-center gap-4 text-xs text-slate-500">
              <div className="flex items-center gap-1">
                <Clock className="w-3.5 h-3.5 animate-spin text-indigo-500" />
                Waiting for callback...
              </div>
              <button
                onClick={() => setStep('chooser')}
                className="text-xs font-bold text-indigo-600 hover:underline"
              >
                Switch factor method
              </button>
            </div>
          </div>
        )}

        {step === 'success' && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in text-center" id="step-success">
            <div className="w-14 h-14 bg-emerald-50 rounded-2xl flex items-center justify-center mx-auto mb-4 text-emerald-600 border border-emerald-100 shadow-xs">
              <CheckCircle className="w-8 h-8" />
            </div>

            <h1 className="text-lg font-bold text-slate-900">MFA Ceremony Complete</h1>
            <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
              The independence evaluator has verified the security evidence classes. AMR claims successfully formulated and emitted.
            </p>

            <div className="my-5 bg-white border border-slate-200 rounded-xl p-4 text-left max-w-md mx-auto shadow-xs">
              <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Cryptographic Token Issuance (AMR)</div>
              <div className="flex flex-wrap gap-1.5 mb-3.5">
                {amr.map((token, i) => (
                  <span key={i} className="px-2 py-0.5 bg-indigo-50 border border-indigo-100 text-indigo-700 font-mono text-[10px] font-bold rounded">
                    {token}
                  </span>
                ))}
              </div>

              <div className="h-[1px] bg-slate-100 w-full mb-3"></div>

              <div className="space-y-1.5 text-xs">
                <div className="flex justify-between">
                  <span className="text-slate-400 font-medium">Assurance Evaluation:</span>
                  <span className="font-bold text-emerald-600 flex items-center gap-1">
                    <Check className="w-3.5 h-3.5" /> Satisfied
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 font-medium">Policy Conformance:</span>
                  <span className="font-medium text-slate-700">Strict-v2.4 (FIDO2)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-400 font-medium">Audit Reference ID:</span>
                  <span className="font-mono text-slate-700 font-bold">{auditRef}</span>
                </div>
              </div>
            </div>

            <div className="flex gap-3 justify-center max-w-sm mx-auto">
              <button
                onClick={handleResetCeremony}
                className="px-4 py-2 text-xs font-bold text-slate-600 border border-slate-200 hover:bg-slate-50 rounded-lg transition-all"
              >
                Restart Simulation
              </button>
              <button
                onClick={() => onCeremonyComplete(amr, auditRef)}
                className="px-6 py-2 text-xs font-bold bg-indigo-600 hover:bg-indigo-700 text-white rounded-lg shadow-md transition-all flex items-center gap-1"
              >
                Proceed with Transaction <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}

        {step === 'failed_blocked' && (
          <div className="flex-1 flex flex-col justify-center animate-fade-in text-center" id="step-failed-blocked">
            <div className="w-14 h-14 bg-rose-50 border border-rose-100 rounded-2xl flex items-center justify-center mx-auto mb-4 text-rose-600 shadow-xs">
              <AlertTriangle className="w-8 h-8 animate-pulse" />
            </div>

            <h1 className="text-lg font-bold text-slate-900">Session Securely Blocked</h1>
            <p className="text-xs text-slate-500 mt-1 max-w-md mx-auto">
              Too many incorrect multi-factor challenge attempts. Your account session has been locked out to protect against credential stuffing.
            </p>

            <div className="bg-rose-50 border border-rose-200 text-rose-800 rounded-lg p-3 text-xs text-left max-w-md mx-auto my-5">
              <div className="font-bold flex items-center gap-1.5 mb-1">
                <AlertCircle className="w-4 h-4" /> Locked Out for Lockout Threshold
              </div>
              Acme policy prohibits additional verification attempts for this session. A helpdesk agent or tenant administrator must execute a secure factor reset before authentication is permitted again.
            </div>

            <div className="flex gap-3 justify-center">
              <button
                onClick={handleResetCeremony}
                className="px-5 py-2 text-xs font-bold bg-slate-900 text-white rounded-lg shadow-xs hover:bg-slate-800 transition-colors"
              >
                Reset Verification Attempts (Helpdesk Bypass)
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
