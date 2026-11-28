import React, { useState, useEffect, useRef } from 'react';
import { 
  Fingerprint, 
  KeyRound, 
  Smartphone, 
  Clock, 
  Mail, 
  MessageSquare, 
  Shield, 
  ShieldAlert, 
  ShieldCheck, 
  AlertTriangle, 
  XCircle, 
  CheckCircle2, 
  ArrowRight, 
  Lock, 
  RefreshCw, 
  Info, 
  HelpCircle, 
  Activity, 
  UserX,
  X,
  Laptop,
  Check,
  Send,
  AlertCircle
} from 'lucide-react';
import { RiskDecision, RiskLevel, AuthMethod, RiskSignal, ActiveSession } from '../types';

interface AdaptiveUserCeremonyProps {
  activeDecision: RiskDecision;
  riskLevel: RiskLevel;
  activeSignals: RiskSignal[];
  eligibleMethods: string[];
  fallbackMethod: string;
  allMethods: AuthMethod[];
  onTriggerAudit: (action: string, decision: RiskDecision, achieved: string[], evidence: string) => void;
  onRefreshEvaluation: () => void;
  activeSession: ActiveSession;
  onRevokeSession: (id: string) => void;
  onReportUnfamiliarActivity: (id: string) => void;
  isEvaluating: boolean;
  setIsEvaluating: (val: boolean) => void;
}

export default function AdaptiveUserCeremony({
  activeDecision,
  riskLevel,
  activeSignals,
  eligibleMethods,
  fallbackMethod,
  allMethods,
  onTriggerAudit,
  onRefreshEvaluation,
  activeSession,
  onRevokeSession,
  onReportUnfamiliarActivity,
  isEvaluating,
  setIsEvaluating
}: AdaptiveUserCeremonyProps) {
  // Navigation & interaction states
  const [evaluationStage, setEvaluationStage] = useState<'idle' | 'running' | 'complete'>('idle');
  const [ceremonyState, setCeremonyState] = useState<'intro' | 'method_selection' | 'active_ceremony' | 'reevaluating' | 'result_success' | 'result_fail' | 'recovery_flow'>('intro');
  const [selectedMethodId, setSelectedMethodId] = useState<string>('');
  
  // Ceremony animation states
  const [passkeyPopupState, setPasskeyPopupState] = useState<'none' | 'prompt' | 'verifying' | 'success'>('none');
  const [yubikeyTouched, setYubikeyTouched] = useState<boolean>(false);
  const [yubikeyPrompt, setYubikeyPrompt] = useState<boolean>(false);
  const [pushCountdown, setPushCountdown] = useState<number>(45);
  const [pushStatus, setPushStatus] = useState<'pending' | 'approved'>('pending');
  const [totpDigits, setTotpDigits] = useState<string[]>(['', '', '', '', '', '']);
  const [totpError, setTotpError] = useState<string>('');
  const [otpSent, setOtpSent] = useState<boolean>(false);
  const [otpDigits, setOtpDigits] = useState<string[]>(['', '', '', '', '', '', '', '']);
  const [otpError, setOtpError] = useState<string>('');

  // Recovery interaction states
  const [recoveryStep, setRecoveryStep] = useState<number>(1);
  const [recoveryEvidence, setRecoveryEvidence] = useState({
    pukCode: '',
    governmentId: '',
    offlineProof: ''
  });
  const [recoverySuccess, setRecoverySuccess] = useState<boolean>(false);

  // References for interactive elements
  const totpRefs = useRef<(HTMLInputElement | null)[]>([]);
  const otpRefs = useRef<(HTMLInputElement | null)[]>([]);

  // Generate dynamic Tracking ID
  const [trackingId] = useState(() => 'TRK-' + Math.random().toString(36).substring(2, 8).toUpperCase() + '-' + Math.random().toString(36).substring(2, 6).toUpperCase());

  // Evaluate risk signals sequence simulation
  useEffect(() => {
    if (isEvaluating) {
      setEvaluationStage('running');
      setCeremonyState('intro');
      setSelectedMethodId('');
      
      const timer = setTimeout(() => {
        setEvaluationStage('complete');
        setIsEvaluating(false);
        
        if (activeDecision === 'continue') {
          setCeremonyState('result_success');
          onTriggerAudit('Login context evaluation bypass step-up', 'continue', ['password'], 'Direct allow: Low overall risk computed.');
        } else if (activeDecision === 'step-up') {
          setCeremonyState('method_selection');
          // Auto-select first eligible method
          if (eligibleMethods.length > 0) {
            setSelectedMethodId(eligibleMethods[0]);
          } else {
            setSelectedMethodId(fallbackMethod);
          }
        } else if (activeDecision === 'review') {
          onTriggerAudit('Login blocked - flagged for ops review', 'review', [], 'Automated trigger: Flagged signals requires manual approval.');
        } else if (activeDecision === 'deny') {
          onTriggerAudit('Access denied outright - posture violation', 'deny', [], 'Automated lockout: Critical hardware compromise or travel vector.');
        } else if (activeDecision === 'recover') {
          setCeremonyState('recovery_flow');
          onTriggerAudit('Access diverted - recovery requested', 'recover', [], 'Automated routing: Missing credentials/enclave attestation.');
        }
      }, 2400);

      return () => clearTimeout(timer);
    }
  }, [isEvaluating, activeDecision]);

  // Countdown timer for push notification simulation
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (selectedMethodId === 'auth_app_push' && ceremonyState === 'active_ceremony' && pushCountdown > 0 && pushStatus === 'pending') {
      interval = setInterval(() => {
        setPushCountdown(prev => {
          if (prev <= 1) {
            clearInterval(interval);
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    }
    return () => clearInterval(interval);
  }, [selectedMethodId, ceremonyState, pushCountdown, pushStatus]);

  // Reset TOTP/OTP inputs when starting
  const startMethodCeremony = (methodId: string) => {
    setSelectedMethodId(methodId);
    setCeremonyState('active_ceremony');
    setTotpDigits(['', '', '', '', '', '']);
    setOtpDigits(['', '', '', '', '', '', '', '']);
    setTotpError('');
    setOtpError('');
    setYubikeyTouched(false);
    setYubikeyPrompt(false);
    setPushCountdown(45);
    setPushStatus('pending');
    setOtpSent(false);

    if (methodId === 'auth_passkey') {
      setPasskeyPopupState('prompt');
    } else if (methodId === 'auth_hardware_key') {
      setYubikeyPrompt(true);
    } else if (methodId === 'auth_email_otp' || methodId === 'auth_sms_otp') {
      setOtpSent(true);
    }
  };

  // Passkey trigger
  const handlePasskeyVerify = () => {
    setPasskeyPopupState('verifying');
    setTimeout(() => {
      setPasskeyPopupState('success');
      setTimeout(() => {
        setPasskeyPopupState('none');
        completeCeremonySuccessfully('auth_passkey');
      }, 1200);
    }, 1800);
  };

  // YubiKey touch trigger
  const handleYubikeyTouch = () => {
    setYubikeyTouched(true);
    setTimeout(() => {
      setYubikeyPrompt(false);
      completeCeremonySuccessfully('auth_hardware_key');
    }, 1000);
  };

  // Push approval simulation
  const handleSimulatePushApprove = () => {
    setPushStatus('approved');
    setTimeout(() => {
      completeCeremonySuccessfully('auth_app_push');
    }, 1000);
  };

  // TOTP digital entry
  const handleTotpChange = (index: number, val: string) => {
    if (!/^\d*$/.test(val)) return;
    const newDigits = [...totpDigits];
    newDigits[index] = val.substring(val.length - 1);
    setTotpDigits(newDigits);

    if (val && index < 5) {
      totpRefs.current[index + 1]?.focus();
    }

    // Auto verify when filled
    if (newDigits.every(d => d !== '') && index === 5) {
      const code = newDigits.join('');
      verifyTotpCode(code);
    }
  };

  const handleTotpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !totpDigits[index] && index > 0) {
      totpRefs.current[index - 1]?.focus();
    }
  };

  const verifyTotpCode = (code: string) => {
    // Correct simulation code: let's treat any 6-digit number as valid unless it starts with '9'
    if (code.startsWith('9')) {
      setTotpError('Cryptographic drift mismatch. Out-of-sync code. Please wait for the next rotation.');
      onTriggerAudit('TOTP Verification Failed', 'step-up', [], 'Security check failed: Cryptographic drift mismatch.');
    } else {
      completeCeremonySuccessfully('auth_totp');
    }
  };

  // OTP (SMS / Email) digital entry
  const handleOtpChange = (index: number, val: string) => {
    if (!/^\d*$/.test(val)) return;
    const newDigits = [...otpDigits];
    newDigits[index] = val.substring(val.length - 1);
    setOtpDigits(newDigits);

    if (val && index < 7) {
      otpRefs.current[index + 1]?.focus();
    }

    if (newDigits.every(d => d !== '') && index === 7) {
      const code = newDigits.join('');
      verifyOtpCode(code);
    }
  };

  const handleOtpKeyDown = (index: number, e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Backspace' && !otpDigits[index] && index > 0) {
      otpRefs.current[index - 1]?.focus();
    }
  };

  const verifyOtpCode = (code: string) => {
    if (code.startsWith('0')) {
      setOtpError('Invalid passcode. Enforced temporal limit expired.');
      onTriggerAudit('OOB Passcode Verification Failed', 'step-up', [], 'Security check failed: Out-of-band temporal limit mismatch.');
    } else {
      completeCeremonySuccessfully(selectedMethodId);
    }
  };

  // Finish successfully
  const completeCeremonySuccessfully = (methodId: string) => {
    setCeremonyState('reevaluating');
    const methodObj = allMethods.find(m => m.id === methodId);
    const methodName = methodObj ? methodObj.name : methodId;
    
    setTimeout(() => {
      setCeremonyState('result_success');
      onTriggerAudit(
        `Step-up verified with ${methodName}`, 
        'continue', 
        ['password', methodId], 
        `Adaptive proof supplied. High-assurance step-up satisfied. Dynamic security context promoted.`
      );
    }, 1800);
  };

  // Recovery Ceremony
  const handleRecoverySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!recoveryEvidence.pukCode) return;
    
    setRecoverySuccess(true);
    onTriggerAudit(
      'Account governance recovery initiated', 
      'recover', 
      [], 
      'User supplied Master PUK Code. Enforced 24h freeze. Operations email dispatched.'
    );
  };

  // Reset and try login again
  const triggerNewSessionSimulation = () => {
    onRefreshEvaluation();
  };

  return (
    <div id="user-ceremony-card" className="flex flex-col h-full rounded-2xl border border-slate-200 bg-white shadow-md overflow-hidden">
      {/* Visual Identity Strip */}
      <div className="bg-slate-900 px-6 py-4 flex items-center justify-between text-white">
        <div className="flex items-center gap-2">
          <Activity className="h-4 w-4 text-emerald-400" />
          <span className="font-display font-medium text-sm tracking-wide uppercase text-slate-300">Target Session Environment</span>
        </div>
        <div className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2 py-0.5 rounded border border-slate-700">
          SECURE TRANSACT: {trackingId}
        </div>
      </div>

      {/* Main interactive area */}
      <div className="p-6 flex-1 flex flex-col justify-center">

        {/* 1. Evaluation State: Holding Server evaluating Risk */}
        {evaluationStage === 'running' && (
          <div id="evaluation-hold-screen" className="py-12 text-center flex flex-col items-center justify-center">
            <div className="relative mb-6">
              <div className="h-16 w-16 rounded-full border-4 border-slate-100 border-t-slate-900 animate-spin"></div>
              <Lock className="absolute inset-0 m-auto h-6 w-6 text-slate-800" />
            </div>
            <h3 className="font-display text-lg font-bold text-slate-900">Evaluating Session Authenticity</h3>
            <p className="max-w-md mx-auto mt-2 text-sm text-slate-500 font-sans">
              Analyzing residential IP, hardware integrity, and typing dynamics against current policy threshold...
            </p>

            <div className="mt-8 w-full max-w-xs space-y-2.5">
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-400">Travel Velocity check:</span>
                <span className="text-emerald-500 font-medium animate-pulse">Scanning...</span>
              </div>
              <div className="w-full bg-slate-100 h-1.5 rounded-full overflow-hidden">
                <div className="bg-slate-900 h-full w-2/3 rounded-full animate-infinite-pulse"></div>
              </div>
              <div className="flex justify-between items-center text-xs font-mono">
                <span className="text-slate-400">Secure Enclave check:</span>
                <span className="text-emerald-500 font-medium">Verified (99% conf)</span>
              </div>
            </div>
          </div>
        )}

        {/* 2. Idle State - Initial Request */}
        {evaluationStage === 'idle' && (
          <div id="idle-ceremony-screen" className="py-8 text-center flex flex-col items-center">
            <div className="h-14 w-14 rounded-2xl bg-slate-50 border border-slate-200 flex items-center justify-center text-slate-900 mb-4 shadow-xs">
              <Shield className="h-7 w-7 text-slate-700" />
            </div>
            <h3 className="font-display text-xl font-bold text-slate-900">Adaptive Authentication Gate</h3>
            <p className="max-w-md mx-auto mt-2 text-sm text-slate-500 font-sans">
              Simulate a sign-in or high-privilege action to test how the server evaluates context, computes risk rules, and demands adaptive credentials.
            </p>

            <div className="mt-6 p-4 rounded-xl border border-slate-100 bg-slate-50 text-left w-full">
              <span className="text-xs font-mono font-medium text-slate-500 block mb-2">PROPOSED CONTEXT</span>
              <div className="grid grid-cols-2 gap-y-2 gap-x-4 text-xs font-mono text-slate-600">
                <div>Device: <span className="text-slate-900">MacBook Safari</span></div>
                <div>Risk Scenario: <span className="text-slate-900 font-medium">{riskLevel.toUpperCase()}</span></div>
                <div>User ID: <span className="text-slate-900">jick.68@gmail.com</span></div>
                <div>Target AMR: <span className="text-slate-900">rba (adaptive)</span></div>
              </div>
            </div>

            <button
              onClick={onRefreshEvaluation}
              className="mt-8 flex items-center justify-center gap-2 w-full max-w-sm rounded-xl bg-slate-900 py-3.5 px-4 text-sm font-semibold text-white hover:bg-slate-800 transition duration-150 shadow-sm"
            >
              <span>Trigger Evaluated Action</span>
              <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        )}

        {/* 3. Decision Outcomes - Step-Up Intro & Method Chooser */}
        {evaluationStage === 'complete' && ceremonyState === 'method_selection' && (
          <div id="stepup-chooser-screen" className="space-y-6">
            <div className="rounded-xl bg-amber-50 border border-amber-200 p-4 flex gap-3">
              <AlertTriangle className="h-5 w-5 text-amber-600 flex-shrink-0 mt-0.5" />
              <div>
                <h4 className="font-display font-bold text-sm text-amber-950">We need another verification step</h4>
                <p className="mt-1 text-xs text-amber-800 font-sans leading-relaxed">
                  To complete this action safely, please provide supplementary authentication. Our server requires high-assurance proof to verify your device context.
                </p>
              </div>
            </div>

            <div>
              <label className="block text-xs font-mono font-medium text-slate-500 uppercase tracking-wider mb-3">
                Eligible Verification Methods ({eligibleMethods.length})
              </label>
              
              <div className="space-y-3">
                {allMethods
                  .filter(m => eligibleMethods.includes(m.id) || m.id === fallbackMethod)
                  .map(method => {
                    const isEligible = eligibleMethods.includes(method.id);
                    const isSelected = selectedMethodId === method.id;
                    const IconComp = method.id === 'auth_passkey' ? Fingerprint 
                      : method.id === 'auth_hardware_key' ? KeyRound
                      : method.id === 'auth_app_push' ? Smartphone
                      : method.id === 'auth_totp' ? Clock
                      : method.id === 'auth_email_otp' ? Mail
                      : MessageSquare;

                    return (
                      <div
                        key={method.id}
                        onClick={() => startMethodCeremony(method.id)}
                        className={`group relative flex items-center gap-4 rounded-xl border p-4 cursor-pointer transition-all duration-150 hover:border-slate-400 ${
                          isSelected 
                            ? 'border-slate-900 bg-slate-50 ring-1 ring-slate-950' 
                            : 'border-slate-200 bg-white'
                        } ${!isEligible ? 'opacity-60 hover:opacity-100' : ''}`}
                      >
                        <div className={`flex h-10 w-10 items-center justify-center rounded-lg ${
                          isSelected ? 'bg-slate-900 text-white' : 'bg-slate-100 text-slate-600'
                        }`}>
                          <IconComp className="h-5 w-5" />
                        </div>
                        
                        <div className="flex-1">
                          <div className="flex items-center gap-1.5">
                            <span className="font-display font-semibold text-sm text-slate-900">{method.name}</span>
                            {!isEligible && (
                              <span className="inline-flex items-center rounded-sm bg-slate-100 px-1.5 py-0.2 text-[10px] font-mono text-slate-500 font-medium">
                                Fallback Channel
                              </span>
                            )}
                          </div>
                          <p className="text-xs text-slate-500 mt-0.5 leading-normal">{method.description}</p>
                        </div>

                        <div className="text-slate-400 group-hover:text-slate-900 transition">
                          <ArrowRight className="h-4 w-4" />
                        </div>
                      </div>
                    );
                  })}
              </div>
            </div>

            <div className="flex justify-between items-center text-xs font-mono pt-4 border-t border-slate-100">
              <span className="text-slate-400">Policy: RBA-v1.4.2</span>
              <button 
                onClick={() => setCeremonyState('recovery_flow')}
                className="text-slate-600 hover:text-slate-900 underline font-medium"
              >
                In trouble? Launch recovery
              </button>
            </div>
          </div>
        )}

        {/* 4. Authenticator Ceremony Interactive States */}
        {evaluationStage === 'complete' && ceremonyState === 'active_ceremony' && (
          <div id="authenticator-ceremony-screen" className="space-y-6">
            <button
              onClick={() => setCeremonyState('method_selection')}
              className="inline-flex items-center gap-1.5 text-xs font-mono text-slate-500 hover:text-slate-900"
            >
              <X className="h-3 w-3" />
              <span>Cancel &amp; Switch Method</span>
            </button>

            {/* A. Passkey Mock System Modal */}
            {selectedMethodId === 'auth_passkey' && (
              <div className="border border-slate-200 rounded-xl bg-slate-50 p-6 text-center space-y-4">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-900 text-emerald-400 shadow-xs">
                  <Fingerprint className="h-7 w-7" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-slate-900">Verify your Identity</h4>
                  <p className="text-xs text-slate-500 max-w-xs mx-auto mt-1">
                    Your browser is prompting for face, fingerprint, or PIN lock via FIDO2 WebAuthn.
                  </p>
                </div>

                {passkeyPopupState === 'prompt' && (
                  <button
                    onClick={handlePasskeyVerify}
                    className="mx-auto flex items-center justify-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 transition"
                  >
                    <span>Activate Biometric Prompter</span>
                  </button>
                )}

                {passkeyPopupState === 'verifying' && (
                  <div className="flex flex-col items-center gap-2">
                    <RefreshCw className="h-5 w-5 text-slate-600 animate-spin" />
                    <span className="text-xs font-mono text-slate-600">Reading biometric secure enclave...</span>
                  </div>
                )}

                {passkeyPopupState === 'success' && (
                  <div className="flex flex-col items-center gap-1.5 text-emerald-600">
                    <CheckCircle2 className="h-6 w-6" />
                    <span className="text-xs font-mono font-medium">Attestation Signature Verified!</span>
                  </div>
                )}
              </div>
            )}

            {/* B. YubiKey hardware interactive prompt */}
            {selectedMethodId === 'auth_hardware_key' && (
              <div className="border border-slate-200 rounded-xl bg-slate-50 p-6 text-center space-y-4">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-amber-500 border border-slate-200 shadow-xs animate-pulse">
                  <KeyRound className="h-7 w-7" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-slate-900">Insert &amp; Tap Security Key</h4>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                    Connect your physical FIDO2 key (like YubiKey) and touch the gold contact sensor.
                  </p>
                </div>

                {yubikeyPrompt && (
                  <div className="relative inline-block mt-4">
                    <button
                      onClick={handleYubikeyTouch}
                      className={`relative z-10 mx-auto flex items-center gap-3 rounded-xl border px-6 py-4 transition-all duration-200 ${
                        yubikeyTouched 
                          ? 'border-emerald-500 bg-emerald-50 text-emerald-700 shadow-emerald-100' 
                          : 'border-slate-300 bg-white text-slate-700 hover:border-amber-400 shadow-sm'
                      }`}
                    >
                      <span className="flex h-3.5 w-3.5 items-center justify-center rounded-full bg-amber-400 animate-ping"></span>
                      <span className="font-mono text-xs font-semibold">
                        {yubikeyTouched ? 'Key Verified ✓' : 'TAP GOLD SENSOR'}
                      </span>
                    </button>
                    
                    {/* Glowing effect around the touch sensor mock */}
                    {!yubikeyTouched && (
                      <div className="absolute inset-0 bg-amber-400 opacity-20 blur-xl rounded-full scale-125 animate-pulse"></div>
                    )}
                  </div>
                )}
              </div>
            )}

            {/* C. Secure Push simulation */}
            {selectedMethodId === 'auth_app_push' && (
              <div className="border border-slate-200 rounded-xl bg-slate-50 p-6 text-center space-y-4">
                <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-slate-100 text-blue-500 border border-slate-200 shadow-xs">
                  <Smartphone className="h-7 w-7" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-slate-900">Awaiting App Approval</h4>
                  <p className="text-xs text-slate-500 max-w-sm mx-auto mt-1">
                    Sent cryptographic verification prompt to user's enrolled device: <span className="font-semibold text-slate-700">Pixel 8 Pro</span>.
                  </p>
                </div>

                <div className="flex justify-center items-center gap-4 py-2">
                  <div className="text-slate-400 text-xs font-mono">
                    Expires in: <span className="font-semibold text-slate-900">{pushCountdown}s</span>
                  </div>
                  <span className="h-4 w-px bg-slate-200"></span>
                  <div className="text-xs font-mono text-slate-600">
                    Status: <span className="font-semibold animate-pulse text-amber-600">{pushStatus.toUpperCase()}</span>
                  </div>
                </div>

                {pushStatus === 'pending' && (
                  <button
                    onClick={handleSimulatePushApprove}
                    className="mx-auto flex items-center justify-center gap-2 rounded-lg bg-slate-900 px-5 py-2.5 text-xs font-semibold text-white hover:bg-slate-800 transition shadow-sm"
                  >
                    <span>Simulate Approve on Pixel 8 Pro</span>
                  </button>
                )}

                {pushStatus === 'approved' && (
                  <div className="text-emerald-600 flex items-center justify-center gap-1.5 text-xs font-mono font-medium">
                    <CheckCircle2 className="h-5 w-5" />
                    <span>Cryptographic push accepted!</span>
                  </div>
                )}
              </div>
            )}

            {/* D. TOTP 6-digit numeric keypad entry */}
            {selectedMethodId === 'auth_totp' && (
              <div className="space-y-4">
                <div className="text-center">
                  <h4 className="font-display font-bold text-sm text-slate-950">Enter Google Authenticator Token</h4>
                  <p className="text-xs text-slate-500 mt-1">
                    Submit the 6-digit rotation passcode currently visible in your authenticator application.
                  </p>
                </div>

                <div className="flex justify-center gap-2">
                  {totpDigits.map((digit, idx) => (
                    <input
                      key={idx}
                      type="text"
                      maxLength={1}
                      ref={el => { totpRefs.current[idx] = el; }}
                      value={digit}
                      onChange={e => handleTotpChange(idx, e.target.value)}
                      onKeyDown={e => handleTotpKeyDown(idx, e)}
                      className="w-10 h-12 text-center text-lg font-mono font-semibold border border-slate-200 rounded-lg bg-white shadow-xs focus:ring-1 focus:ring-slate-950 focus:border-slate-950 outline-hidden"
                    />
                  ))}
                </div>

                {totpError && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs font-mono leading-normal">
                    {totpError}
                  </div>
                )}

                <div className="bg-slate-50 border border-slate-100 rounded-xl p-3 text-[11px] text-slate-500 space-y-1">
                  <p className="font-semibold font-mono text-slate-700">💡 SIMULATOR DRIFT HINT:</p>
                  <p>Type any digits (e.g. 123456) to verify instantly. Typing a code starting with "9" (e.g. 999123) triggers a drift mismatch failure.</p>
                </div>
              </div>
            )}

            {/* E. Email or SMS 8-digit OTP code input */}
            {(selectedMethodId === 'auth_email_otp' || selectedMethodId === 'auth_sms_otp') && (
              <div className="space-y-4">
                <div className="text-center">
                  <h4 className="font-display font-bold text-sm text-slate-950">
                    Verify {selectedMethodId === 'auth_email_otp' ? 'Email secure code' : 'SMS passcode'}
                  </h4>
                  <p className="text-xs text-slate-500 mt-1">
                    We've dispatched an out-of-band 8-digit token to your registered {selectedMethodId === 'auth_email_otp' ? 'mailbox' : 'mobile phone'}.
                  </p>
                </div>

                <div className="flex justify-center gap-1.5">
                  {otpDigits.map((digit, idx) => (
                    <input
                      key={idx}
                      type="text"
                      maxLength={1}
                      ref={el => { otpRefs.current[idx] = el; }}
                      value={digit}
                      onChange={e => handleOtpChange(idx, e.target.value)}
                      onKeyDown={e => handleOtpKeyDown(idx, e)}
                      className="w-8 h-11 text-center text-base font-mono font-semibold border border-slate-200 rounded-lg bg-white shadow-xs focus:ring-1 focus:ring-slate-950 focus:border-slate-950 outline-hidden"
                    />
                  ))}
                </div>

                {otpError && (
                  <div className="p-3 bg-red-50 border border-red-200 rounded-lg text-red-600 text-xs font-mono">
                    {otpError}
                  </div>
                )}

                <div className="bg-slate-50 border border-slate-100 rounded-xl p-3 text-[11px] text-slate-500 space-y-1">
                  <p className="font-semibold font-mono text-slate-700">💡 SIMULATOR OTP HINT:</p>
                  <p>Type any digits to verify instantly. Typing a code starting with "0" (e.g. 0824921) triggers a temporal expiry check fail.</p>
                </div>
              </div>
            )}
          </div>
        )}

        {/* 5. Reevaluating State */}
        {evaluationStage === 'complete' && ceremonyState === 'reevaluating' && (
          <div id="reevaluating-screen" className="py-12 text-center space-y-4 flex flex-col items-center">
            <RefreshCw className="h-10 w-10 text-slate-900 animate-spin" />
            <div>
              <h4 className="font-display font-bold text-slate-900">Re-evaluating Authentication Context</h4>
              <p className="text-xs text-slate-500 mt-1">
                Submitting adaptive proof, correlating signals, and updating policy enforcement token...
              </p>
            </div>
          </div>
        )}

        {/* 6. Ultimate Success / Return to Action state */}
        {evaluationStage === 'complete' && ceremonyState === 'result_success' && (
          <div id="ceremony-success-screen" className="text-center py-6 space-y-5">
            <div className="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-50 text-emerald-600 border border-emerald-200 shadow-xs">
              <ShieldCheck className="h-8 w-8" />
            </div>
            
            <div>
              <h3 className="font-display text-lg font-bold text-slate-900">Verification Complete</h3>
              <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto font-sans leading-relaxed">
                Adaptive evaluation satisfied. We have promoting this session to high-assurance and authorized your request.
              </p>
            </div>

            <div className="rounded-xl border border-slate-100 bg-slate-50 p-4 text-left space-y-3">
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">AMR Evidence:</span>
                <span className="font-semibold text-slate-900">pwd, rba (adaptive)</span>
              </div>
              <div className="h-px bg-slate-200"></div>
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">Confidence Index:</span>
                <span className="font-semibold text-emerald-600">99.8% Perfect Match</span>
              </div>
              <div className="h-px bg-slate-200"></div>
              <div className="flex justify-between text-xs font-mono">
                <span className="text-slate-400">Security Rule Met:</span>
                <span className="font-semibold text-slate-800">Normal-Access Override</span>
              </div>
            </div>

            <button
              onClick={triggerNewSessionSimulation}
              className="w-full max-w-xs mx-auto flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 bg-white py-2 px-4 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition shadow-xs"
            >
              <RefreshCw className="h-3 w-3" />
              <span>Simulate Next Event</span>
            </button>
          </div>
        )}

        {/* 7. Review Pending State (Automated Review Block) */}
        {evaluationStage === 'complete' && activeDecision === 'review' && (
          <div id="ops-review-screen" className="space-y-6 py-4">
            <div className="rounded-xl bg-slate-900 border border-slate-800 p-5 text-white flex gap-3.5">
              <Activity className="h-5 w-5 text-indigo-400 flex-shrink-0 mt-0.5 animate-pulse" />
              <div>
                <h4 className="font-display font-bold text-sm">Automated Security Review Triggered</h4>
                <p className="mt-1.5 text-xs text-slate-400 font-sans leading-relaxed">
                  Our continuous behavioral detectors flagged a discrepancy. An administrator has been notified to audit this context manually. Access is held.
                </p>
              </div>
            </div>

            <div className="border border-slate-200 rounded-xl bg-slate-50 p-4 space-y-3.5 text-xs font-mono">
              <div className="flex justify-between">
                <span className="text-slate-500">Support Reference:</span>
                <span className="font-semibold text-slate-900 select-all">REF-2938-K84</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Manual Review SLA:</span>
                <span className="font-semibold text-indigo-600">&lt; 3 minutes</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Signal Anomaly Class:</span>
                <span className="text-slate-800 font-medium">Keystroke speed deviation</span>
              </div>
            </div>

            <div className="rounded-lg bg-indigo-50 border border-indigo-100 p-3.5 text-xs text-indigo-800 space-y-2">
              <p className="font-semibold flex items-center gap-1">
                <Info className="h-4 w-4" />
                <span>Governance Recovery Pathway</span>
              </p>
              <p className="font-sans leading-relaxed text-indigo-700">
                You can bypass this delay by validating through an alternate out-of-band corporate device attestation or contact the SecOps center directly.
              </p>
            </div>

            <button
              onClick={() => setCeremonyState('recovery_flow')}
              className="w-full flex items-center justify-center gap-2 rounded-xl bg-slate-900 py-3 text-xs font-semibold text-white hover:bg-slate-800 transition"
            >
              <span>Initiate Governance Recovery</span>
            </button>
          </div>
        )}

        {/* 8. Deny State (Red Lockout) */}
        {evaluationStage === 'complete' && activeDecision === 'deny' && (
          <div id="access-denied-screen" className="space-y-6 py-4">
            <div className="rounded-xl bg-rose-50 border border-rose-200 p-5 flex gap-3.5">
              <XCircle className="h-6 w-6 text-rose-600 flex-shrink-0" />
              <div>
                <h4 className="font-display font-bold text-sm text-rose-950">Access Temporarily Blocked</h4>
                <p className="mt-1.5 text-xs text-rose-800 font-sans leading-relaxed">
                  Authentication request refused outright. This device environment failed critical security posture compliance policies.
                </p>
              </div>
            </div>

            <p className="text-xs text-slate-500 font-sans leading-relaxed">
              To protect your credentials and corporate assets, we have isolated your session. Detector internals and scores are redacted to prevent malicious bypass logic probes.
            </p>

            <div className="border border-slate-200 rounded-xl bg-slate-50 p-4 space-y-2.5 text-xs font-mono">
              <div className="flex justify-between">
                <span className="text-slate-500">Incident Reference:</span>
                <span className="font-semibold text-slate-900 select-all">INC-{trackingId}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-slate-500">Audit Provenance ID:</span>
                <span className="font-mono text-slate-800">AUTH-PROV-9238120</span>
              </div>
            </div>

            <div className="flex flex-col gap-2">
              <button
                onClick={() => setCeremonyState('recovery_flow')}
                className="w-full flex items-center justify-center gap-2 rounded-xl bg-rose-600 hover:bg-rose-700 py-3 text-xs font-semibold text-white transition shadow-sm"
              >
                <span>Report Attack / Lock Account Immediately</span>
              </button>
              <button
                onClick={triggerNewSessionSimulation}
                className="w-full flex items-center justify-center gap-1.5 rounded-lg border border-slate-300 bg-white py-2 px-4 text-xs font-semibold text-slate-700 hover:bg-slate-50 transition"
              >
                <RefreshCw className="h-3.5 w-3.5" />
                <span>Simulate Alternate Scenario</span>
              </button>
            </div>
          </div>
        )}

        {/* 9. Recovery Workspaces (Offline/Gov proof) */}
        {ceremonyState === 'recovery_flow' && (
          <div id="recovery-flow-workspace" className="space-y-5 py-2">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-1.5">
                <KeyRound className="h-4.5 w-4.5 text-slate-700" />
                <h4 className="font-display font-bold text-slate-950">Governed Recovery Workspace</h4>
              </div>
              <button
                onClick={() => setCeremonyState('method_selection')}
                className="text-xs text-slate-500 hover:text-slate-900"
              >
                Cancel
              </button>
            </div>

            {!recoverySuccess ? (
              <form onSubmit={handleRecoverySubmit} className="space-y-4">
                <p className="text-xs text-slate-500 font-sans leading-relaxed">
                  Restore account access through governed cryptographic override. Never bypasses signal logging. All actions audited.
                </p>

                {recoveryStep === 1 ? (
                  <div className="space-y-3.5">
                    <div>
                      <label className="block text-xs font-mono font-medium text-slate-500 mb-1.5 uppercase">
                        Master PUK Override Code (24 digits)
                      </label>
                      <input
                        type="password"
                        required
                        placeholder="••••-••••-••••-••••-••••"
                        value={recoveryEvidence.pukCode}
                        onChange={e => setRecoveryEvidence({ ...recoveryEvidence, pukCode: e.target.value })}
                        className="w-full text-sm font-mono tracking-widest border border-slate-200 rounded-lg p-2.5 bg-white outline-hidden focus:ring-1 focus:ring-slate-950"
                      />
                    </div>
                    <div className="bg-amber-50 border border-amber-100 rounded-lg p-3 text-xs text-amber-800">
                      Warning: Submitting an override PUK locks all other associated platform authentication devices for 24 hours.
                    </div>
                    <button
                      type="button"
                      onClick={() => setRecoveryStep(2)}
                      disabled={!recoveryEvidence.pukCode}
                      className="w-full flex items-center justify-center gap-1 rounded-lg bg-slate-900 py-2.5 text-xs font-semibold text-white disabled:opacity-50"
                    >
                      <span>Continue to Attestation</span>
                      <ArrowRight className="h-4 w-4" />
                    </button>
                  </div>
                ) : (
                  <div className="space-y-3.5">
                    <div>
                      <label className="block text-xs font-mono font-medium text-slate-500 mb-1 uppercase">
                        Select Gov-Attested ID Document
                      </label>
                      <select
                        value={recoveryEvidence.governmentId}
                        onChange={e => setRecoveryEvidence({ ...recoveryEvidence, governmentId: e.target.value })}
                        className="w-full text-xs border border-slate-200 rounded-lg p-2 bg-white"
                      >
                        <option value="">-- Choose verified document on file --</option>
                        <option value="passport">Biometric Passport (United States)</option>
                        <option value="driver">Digital Driver's License (WA state)</option>
                      </select>
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setRecoveryStep(1)}
                        className="flex-1 rounded-lg border border-slate-200 py-2 text-xs font-semibold text-slate-700 bg-white"
                      >
                        Back
                      </button>
                      <button
                        type="submit"
                        disabled={!recoveryEvidence.governmentId}
                        className="flex-1 rounded-lg bg-emerald-600 hover:bg-emerald-700 py-2 text-xs font-semibold text-white disabled:opacity-50"
                      >
                        Submit Overrides
                      </button>
                    </div>
                  </div>
                )}
              </form>
            ) : (
              <div className="text-center py-4 space-y-4">
                <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-emerald-100 text-emerald-600">
                  <Check className="h-6 w-6" />
                </div>
                <div>
                  <h4 className="font-display font-bold text-slate-900">Governance Claim Submitted</h4>
                  <p className="text-xs text-slate-500 mt-1 font-sans">
                    Your attestation proofs have been dispatched to manual security reviewers. Ref ID: {trackingId}.
                  </p>
                </div>
                <button
                  onClick={triggerNewSessionSimulation}
                  className="rounded-lg bg-slate-900 text-white py-2 px-4 text-xs font-semibold hover:bg-slate-800 transition"
                >
                  Return to Sandbox
                </button>
              </div>
            )}
          </div>
        )}

      </div>

      {/* P1 Section — Active User Session Context */}
      <div id="session-context-drawer" className="border-t border-slate-200 bg-slate-50 p-4">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-1.5">
            <Laptop className="h-4 w-4 text-slate-500" />
            <h4 className="text-xs font-semibold text-slate-900 font-display">Active Session Context (P1)</h4>
          </div>
          <span className="text-[10px] font-mono bg-slate-200 px-1.5 py-0.5 rounded text-slate-600">
            Current IP: {activeSession.ipAddress}
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-[11px] font-mono text-slate-600">
          <div className="bg-white p-2 rounded border border-slate-100">
            <span className="text-slate-400 block text-[9px] uppercase">Device Class</span>
            <span className="text-slate-800 truncate block mt-0.5">{activeSession.device}</span>
          </div>
          <div className="bg-white p-2 rounded border border-slate-100">
            <span className="text-slate-400 block text-[9px] uppercase">Geolocation Context</span>
            <span className="text-slate-800 truncate block mt-0.5">{activeSession.location}</span>
          </div>
        </div>

        <div className="mt-3 flex gap-2">
          <button
            onClick={() => onReportUnfamiliarActivity(activeSession.id)}
            className="flex-1 flex items-center justify-center gap-1 rounded-lg border border-red-200 bg-red-50 text-red-700 py-1.5 px-3 text-xs font-semibold hover:bg-red-100 transition duration-150"
          >
            <UserX className="h-3.5 w-3.5" />
            <span>Unfamiliar? Report Anomaly</span>
          </button>
          
          <button
            onClick={() => onRevokeSession(activeSession.id)}
            className="rounded-lg border border-slate-200 bg-white hover:bg-slate-100 py-1.5 px-3 text-xs font-semibold text-slate-700 transition"
          >
            Revoke Session
          </button>
        </div>
      </div>
    </div>
  );
}
