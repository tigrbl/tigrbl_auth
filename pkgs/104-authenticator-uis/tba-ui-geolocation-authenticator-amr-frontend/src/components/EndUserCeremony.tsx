import React, { useState, useEffect } from 'react';
import { LocationConsentPanel } from './LocationConsentPanel';
import { LocationEvidenceSummary } from './LocationEvidenceSummary';
import { LocationSourceBadge } from './LocationSourceBadge';
import { 
  ShieldCheck, ShieldAlert, KeyRound, Smartphone, Mail, Clock, RefreshCw, 
  MapPin, Ban, CheckCircle2, UserCheck, AlertTriangle, Compass, 
  User, Info, ChevronRight
} from 'lucide-react';

export type AMRState =
  | 'initializing'
  | 'evaluating'
  | 'consent required'
  | 'awaiting permission'
  | 'permission granted'
  | 'denied'
  | 'unavailable'
  | 'low accuracy'
  | 'stale'
  | 'source conflict'
  | 'spoof suspected'
  | 'submitting'
  | 'step-up required'
  | 'provider unavailable'
  | 'retryable failure'
  | 'blocked'
  | 'expired'
  | 'cancelled'
  | 'success'
  | 'success requiring another step';

interface EndUserCeremonyProps {
  onSuccess: (auditRecord: any) => void;
  selectedSimulationProfile: any;
}

export const EndUserCeremony: React.FC<EndUserCeremonyProps> = ({
  onSuccess,
  selectedSimulationProfile
}) => {
  const [email, setEmail] = useState('jick.68.0@gmail.com');
  const [currentStep, setCurrentStep] = useState<'email' | 'amr_sequence'>('email');
  const [amrState, setAmrState] = useState<AMRState>('initializing');
  const [otpCode, setOtpCode] = useState('');
  const [selectedMethod, setSelectedMethod] = useState<'passkey' | 'otp' | null>(null);
  const [passkeyChecking, setPasskeyChecking] = useState(false);

  const amrStateDescriptions: Record<AMRState, { title: string; desc: string; badge: string }> = {
    'initializing': { title: 'Initializing Context', desc: 'Starting secure background telemetry handoff.', badge: 'bg-slate-100 text-slate-800' },
    'evaluating': { title: 'Evaluating Context', desc: 'Analyzing coarse network paths and enterprise Wi-Fi nodes.', badge: 'bg-indigo-100 text-indigo-800' },
    'consent required': { title: 'Consent Required', desc: 'Requesting permission statement to verify GPS hardware signal.', badge: 'bg-purple-100 text-purple-800' },
    'awaiting permission': { title: 'Awaiting Permission', desc: 'OS level hardware GPS modal is currently open.', badge: 'bg-amber-100 text-amber-800' },
    'permission granted': { title: 'Permission Granted', desc: 'Secure coordinate payload signed and verified.', badge: 'bg-emerald-100 text-emerald-800' },
    'denied': { title: 'Permission Denied', desc: 'User blocked GPS. Falling back to coarse network policy.', badge: 'bg-rose-100 text-rose-800' },
    'unavailable': { title: 'Signal Unavailable', desc: 'Hardware satellite telemetry is obstructed or timed out.', badge: 'bg-orange-100 text-orange-800' },
    'low accuracy': { title: 'Low Signal Accuracy', desc: 'Acquired accuracy bounds exceed the geofence policy threshold.', badge: 'bg-yellow-100 text-yellow-800' },
    'stale': { title: 'Stale Evidence Claim', desc: 'Telemetry age exceeds the freshness limit defined in policy.', badge: 'bg-stone-100 text-stone-800' },
    'source conflict': { title: 'Telemetry Conflict', desc: 'GPS coordinates mismatch network ISP regional location.', badge: 'bg-red-100 text-red-800' },
    'spoof suspected': { title: 'Spoof Suspected', desc: 'Mock location engines or proxy tunnels detected.', badge: 'bg-rose-200 text-rose-900 border border-rose-300' },
    'submitting': { title: 'Submitting Evidence', desc: 'Gateway is processing cryptographically enclosed package.', badge: 'bg-sky-100 text-sky-800' },
    'step-up required': { title: 'Step-Up Verification', desc: 'Authentication policy mandates secondary physical challenge.', badge: 'bg-teal-100 text-teal-800' },
    'provider unavailable': { title: 'Provider Outage', desc: 'Verification gateway is offline. Falling back to secure block.', badge: 'bg-amber-200 text-amber-900' },
    'retryable failure': { title: 'Acquisition Failure', desc: 'Failed to acquire location. Allows user-initiated retry.', badge: 'bg-slate-200 text-slate-700' },
    'blocked': { title: 'Access Denied', desc: 'Unresolved high risk posture causes transaction block.', badge: 'bg-red-600 text-white font-semibold' },
    'expired': { title: 'Session Expired', desc: 'Cryptographic challenge timed out. Fresh request required.', badge: 'bg-gray-400 text-white' },
    'cancelled': { title: 'Transaction Cancelled', desc: 'Login terminated by user request.', badge: 'bg-gray-100 text-gray-800' },
    'success': { title: 'Access Allowed', desc: 'Location coordinates matches physical geofence perfectly.', badge: 'bg-emerald-600 text-white font-semibold' },
    'success requiring another step': { title: 'Verified, Step-Up Appended', desc: 'Location matches, but core rules request OTP for this session.', badge: 'bg-indigo-600 text-white font-semibold' },
  };

  const handleInitiateLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !email.includes('@')) return;
    setCurrentStep('amr_sequence');
    setAmrState('initializing');

    setTimeout(() => {
      setAmrState('evaluating');
      setTimeout(() => {
        if (selectedSimulationProfile.permissionGranted) {
          setAmrState('consent required');
        } else {
          setAmrState('denied');
        }
      }, 1000);
    }, 800);
  };

  const handleShareLocation = () => {
    setAmrState('awaiting permission');
    setTimeout(() => {
      if (selectedSimulationProfile.providerStatus === 'offline') {
        setAmrState('provider unavailable');
        return;
      }
      if (selectedSimulationProfile.mockLocationActive || selectedSimulationProfile.vpnActive) {
        setAmrState('spoof suspected');
        return;
      }
      if (selectedSimulationProfile.accuracy > 100) {
        setAmrState('low accuracy');
        return;
      }

      setAmrState('permission granted');
      setTimeout(() => {
        setAmrState('submitting');
        setTimeout(() => {
          const isHq = selectedSimulationProfile.lat >= 30.2670 && selectedSimulationProfile.lat <= 30.2674;
          const isIpApproved = selectedSimulationProfile.ipAddress.startsWith('192.168.') || selectedSimulationProfile.ipAddress.startsWith('10.');

          if (isHq && isIpApproved) {
            setAmrState('success');
            triggerCompletion('Allow', 'Enterprise Headquarters Access Verified');
          } else {
            setAmrState('step-up required');
          }
        }, 1000);
      }, 800);
    }, 1200);
  };

  const handleDeclineLocation = () => {
    setAmrState('denied');
  };

  const triggerPasskeyChallenge = () => {
    setPasskeyChecking(true);
    setTimeout(() => {
      setPasskeyChecking(false);
      setAmrState('success');
      triggerCompletion('Step-Up', 'Domestic Regional Access Match', 'Passkey Verified');
    }, 1500);
  };

  const verifyOTP = () => {
    if (otpCode === '2026') {
      setAmrState('success');
      triggerCompletion('Step-Up', 'Domestic Regional Access Match', 'SMS OTP Verified');
    } else {
      alert('Invalid Verification Code (Use Code: 2026)');
    }
  };

  const triggerCompletion = (decision: 'Allow' | 'Step-Up' | 'Deny', policyName: string, fallbackUsed?: string) => {
    const record = {
      id: `aud-${Date.now()}`,
      timestamp: new Date().toISOString(),
      userEmail: email,
      sourceType: selectedSimulationProfile.permissionGranted ? 'Device GPS' : 'Carrier IP Geo-Database',
      granularity: selectedSimulationProfile.permissionGranted ? 'precise' : 'coarse',
      policyName: policyName,
      policyVersion: 'v2.4.0',
      decision: decision,
      deviceOS: selectedSimulationProfile.deviceOS,
      accuracy: selectedSimulationProfile.permissionGranted ? selectedSimulationProfile.accuracy : 8500,
      isStale: false,
      spoofSuspected: selectedSimulationProfile.mockLocationActive || selectedSimulationProfile.vpnActive,
      providerStatus: selectedSimulationProfile.providerStatus,
      auditReference: `tx_${Math.random().toString(16).substring(2, 18)}`,
      fallbackUsed: fallbackUsed
    };
    onSuccess(record);
  };

  const handleRestart = () => {
    setCurrentStep('email');
    setAmrState('initializing');
    setOtpCode('');
    setSelectedMethod(null);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start w-full">
      {/* State controller sidebar */}
      <div className="lg:col-span-4 bg-slate-900 border border-slate-800 rounded-xl p-5 shadow-sm text-slate-100 flex flex-col justify-between">
        <div className="space-y-4">
          <div className="flex items-center gap-1.5 font-mono text-[10px] text-slate-400">
            <Compass className="w-4 h-4 text-indigo-400 animate-spin" />
            <span>AMR STATE EXPLORER</span>
          </div>
          <p className="text-xs text-slate-400 leading-normal">
            Choose any of the <strong>20 canonical location states</strong> to force-render its interface instantly.
          </p>

          <div className="space-y-1 max-h-[360px] overflow-y-auto border border-slate-800 rounded-lg p-2 bg-slate-950/50">
            {(Object.keys(amrStateDescriptions) as AMRState[]).map((state) => {
              const isActive = amrState === state;
              const config = amrStateDescriptions[state];
              return (
                <button
                  key={state}
                  onClick={() => {
                    setCurrentStep('amr_sequence');
                    setAmrState(state);
                  }}
                  className={`w-full text-left p-1.5 rounded flex items-center justify-between text-xs transition-all ${
                    isActive 
                      ? 'bg-indigo-600 text-white font-semibold shadow' 
                      : 'hover:bg-slate-800/60 text-slate-300'
                  }`}
                >
                  <div className="truncate">
                    <span className="font-semibold block truncate text-[11px]">{config.title}</span>
                    <span className={`text-[9px] ${isActive ? 'text-indigo-200' : 'text-slate-500'} block truncate`}>
                      {config.desc}
                    </span>
                  </div>
                  <ChevronRight className="w-3 h-3 shrink-0 ml-1" />
                </button>
              );
            })}
          </div>
        </div>
      </div>

      {/* Ceremony card display */}
      <div className="lg:col-span-8 bg-white border border-slate-200 rounded-xl p-6 shadow-sm min-h-[480px] flex flex-col justify-center items-center relative overflow-hidden">
        {currentStep === 'email' ? (
          <div className="max-w-md w-full space-y-5 text-center">
            <div className="mx-auto w-12 h-12 bg-indigo-50 border border-indigo-150 rounded-xl flex items-center justify-center text-indigo-600">
              <UserCheck className="w-6 h-6" />
            </div>
            <div className="space-y-1">
              <h3 className="text-base font-bold text-slate-900 font-display">
                Corporate Identity Portal
              </h3>
              <p className="text-xs text-slate-500">
                Secure Enterprise Connection (AMR Verification)
              </p>
            </div>

            <form onSubmit={handleInitiateLogin} className="space-y-3 text-left">
              <div className="space-y-1">
                <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
                  Workspace Email Address
                </label>
                <div className="relative">
                  <User className="absolute left-3 top-2.5 w-4.5 h-4.5 text-slate-400" />
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    placeholder="name@company.com"
                    className="w-full bg-white border border-slate-200 rounded-lg pl-10 pr-4 py-2 text-sm focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              <button
                type="submit"
                className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold py-2 rounded-lg text-sm transition-all shadow-sm flex items-center justify-center gap-2"
              >
                <span>Initiate Secure Authentication</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </form>
          </div>
        ) : (
          <div className="w-full max-w-md space-y-4">
            <div className="flex items-center justify-between border-b border-slate-200 pb-3">
              <button
                onClick={handleRestart}
                className="text-xs text-slate-500 hover:text-slate-800 flex items-center gap-1 font-semibold"
              >
                ← Restart
              </button>
              <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-mono font-bold tracking-wide uppercase ${
                amrStateDescriptions[amrState]?.badge
              }`}>
                {amrStateDescriptions[amrState]?.title}
              </span>
            </div>

            {/* Render sub views based on state */}
            {amrState === 'initializing' && (
              <div className="text-center py-10 space-y-3">
                <RefreshCw className="w-8 h-8 animate-spin text-indigo-500 mx-auto" />
                <h4 className="text-xs font-semibold text-slate-800">Bootstrapping Security Envelope...</h4>
              </div>
            )}

            {amrState === 'evaluating' && (
              <div className="text-center py-10 space-y-3">
                <Compass className="w-8 h-8 animate-spin text-indigo-500 mx-auto" />
                <h4 className="text-xs font-semibold text-slate-800">Analyzing Network Routing Path...</h4>
              </div>
            )}

            {amrState === 'consent required' && (
              <LocationConsentPanel
                purpose="Corporate guidelines require proximity confirmation before authorizing a secure workspace connection."
                requiredAccuracy={30}
                retentionNotice="7 Days"
                onConsentGranted={handleShareLocation}
                onConsentDeclined={handleDeclineLocation}
                isEvaluating={false}
                alternativeMethod="SMS Code Fallback"
              />
            )}

            {amrState === 'awaiting permission' && (
              <div className="text-center py-10 space-y-4">
                <MapPin className="w-10 h-10 text-amber-500 mx-auto animate-pulse" />
                <h4 className="text-xs font-semibold text-slate-800">Awaiting Hardware Consent Modal</h4>
                <p className="text-[11px] text-slate-500 max-w-xs mx-auto">
                  Please approve the location permission request in your browser toolbar.
                </p>
              </div>
            )}

            {amrState === 'permission granted' && (
              <div className="text-center py-10 space-y-2">
                <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto" />
                <h4 className="text-xs font-semibold text-slate-800">Permission Confirmed</h4>
              </div>
            )}

            {amrState === 'denied' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
                <div className="flex gap-3">
                  <Ban className="w-5 h-5 text-rose-500 shrink-0" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Geolocation Permission Denied</h4>
                    <p className="text-[11px] text-slate-500 leading-relaxed mt-1">
                      You declined location sharing. Please verify using an alternative authenticator or enable location permissions in browser settings.
                    </p>
                  </div>
                </div>
                <div className="bg-white border border-slate-150 rounded-lg p-3 text-[11px] text-slate-600 space-y-1">
                  <strong>How to restore browser permissions:</strong>
                  <p>• Click the lock icon in the address bar → toggle Location to "Allow".</p>
                  <p>• System Settings → Privacy & Security → Location Services.</p>
                </div>
                <div className="flex gap-2">
                  <button onClick={() => setAmrState('step-up required')} className="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-xs py-2 rounded-lg">
                    Approved Fallback Method
                  </button>
                  <button onClick={handleShareLocation} className="border border-slate-200 hover:bg-slate-100 text-slate-700 font-semibold text-xs py-2 px-3 rounded-lg">
                    Retry GPS
                  </button>
                </div>
              </div>
            )}

            {amrState === 'unavailable' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-4">
                <div className="flex gap-3">
                  <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Hardware GPS Signal Obstructed</h4>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Unable to lock satellite coordinates. Please retry or continue using secondary authentication.
                    </p>
                  </div>
                </div>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Solve Secondary Authenticator
                </button>
              </div>
            )}

            {amrState === 'low accuracy' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
                <AlertTriangle className="w-5 h-5 text-amber-500 mx-auto" />
                <h4 className="text-xs font-bold text-center text-slate-900">Low Accuracy Signal Detected</h4>
                <p className="text-[11px] text-slate-500 text-center leading-relaxed">
                  Calculated radius is {selectedSimulationProfile.accuracy}m. Enterprise policies require precision &lt; 30m.
                </p>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Fallback Verification Method
                </button>
              </div>
            )}

            {amrState === 'stale' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-center space-y-3">
                <Clock className="w-6 h-6 text-slate-400 mx-auto" />
                <h4 className="text-xs font-bold text-slate-900">Cached Location Claim Expired</h4>
                <button onClick={handleShareLocation} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Query Fresh Coordinates
                </button>
              </div>
            )}

            {amrState === 'source conflict' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
                <ShieldAlert className="w-6 h-6 text-rose-500 mx-auto" />
                <h4 className="text-xs font-bold text-center text-slate-950">Evidence Disagreement Detected</h4>
                <p className="text-[11px] text-slate-500 text-center">
                  GPS signal coordinates mismatch carrier network regional telemetry.
                </p>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Resolve Hardware Step-Up
                </button>
              </div>
            )}

            {amrState === 'spoof suspected' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
                <ShieldAlert className="w-6 h-6 text-rose-500 mx-auto" />
                <h4 className="text-xs font-bold text-slate-900 text-center">Inconsistent Telemetry Profile</h4>
                <p className="text-[11px] text-slate-500 text-center">
                  Mock coordinates or proxy tunnels detected. Hard physical check is required.
                </p>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Complete Verification Challenge
                </button>
              </div>
            )}

            {amrState === 'submitting' && (
              <div className="text-center py-10 space-y-2">
                <RefreshCw className="w-8 h-8 animate-spin text-indigo-500 mx-auto" />
                <h4 className="text-xs font-semibold text-slate-800">Transmitting Cryptographic Envelope...</h4>
              </div>
            )}

            {amrState === 'step-up required' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3">
                <div className="flex gap-2">
                  <KeyRound className="w-5 h-5 text-indigo-500 shrink-0" />
                  <div>
                    <h4 className="text-xs font-bold text-slate-900">Verification Step-Up Mandated</h4>
                    <p className="text-[11px] text-slate-500">Please solve a supplementary physical challenge.</p>
                  </div>
                </div>

                {!selectedMethod ? (
                  <div className="space-y-2 pt-2">
                    <button onClick={() => { setSelectedMethod('passkey'); triggerPasskeyChallenge(); }} className="w-full text-left p-3 bg-white border border-slate-200 rounded-lg hover:border-indigo-500 transition-all">
                      <span className="text-xs font-bold text-slate-800 block">FIDO2 Biometric Passkey</span>
                      <span className="text-[10px] text-slate-400 block">Hardware device authentication</span>
                    </button>
                    <button onClick={() => setSelectedMethod('otp')} className="w-full text-left p-3 bg-white border border-slate-200 rounded-lg hover:border-indigo-500 transition-all">
                      <span className="text-xs font-bold text-slate-800 block">SMS One-Time Passcode</span>
                      <span className="text-[10px] text-slate-400 block">4-digit code delivered to mobile device</span>
                    </button>
                  </div>
                ) : selectedMethod === 'passkey' ? (
                  <div className="py-4 text-center">
                    {passkeyChecking ? (
                      <RefreshCw className="w-6 h-6 animate-spin text-indigo-500 mx-auto" />
                    ) : (
                      <CheckCircle2 className="w-6 h-6 text-emerald-500 mx-auto" />
                    )}
                  </div>
                ) : (
                  <div className="space-y-3 pt-1">
                    <input
                      type="text"
                      maxLength={4}
                      value={otpCode}
                      onChange={(e) => setOtpCode(e.target.value)}
                      placeholder="Use Code: 2026"
                      className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-center font-mono text-sm focus:outline-none"
                    />
                    <button onClick={verifyOTP} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                      Verify OTP Passcode
                    </button>
                  </div>
                )}
              </div>
            )}

            {amrState === 'provider unavailable' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 space-y-3 text-center">
                <AlertTriangle className="w-6 h-6 text-rose-500 mx-auto" />
                <h4 className="text-xs font-bold text-slate-900">Verification Infrastructure Outage</h4>
                <p className="text-[11px] text-slate-500">
                  Services are unreachable. System failed-securely. Secondary check required.
                </p>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Continue to Step-Up Auth
                </button>
              </div>
            )}

            {amrState === 'retryable failure' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-center space-y-3">
                <h4 className="text-xs font-bold text-slate-900">Gateway Timeout</h4>
                <button onClick={handleShareLocation} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Retry Handshake
                </button>
              </div>
            )}

            {amrState === 'blocked' && (
              <div className="bg-rose-50 border border-rose-200 rounded-xl p-5 text-center space-y-3">
                <Ban className="w-8 h-8 text-rose-500 mx-auto" />
                <h4 className="text-xs font-bold text-rose-900">Access Policy Denied</h4>
                <p className="text-[11px] text-rose-700">
                  Connection blocked in accordance with geographic rules. Contact IT helpdesk.
                </p>
                <button onClick={handleRestart} className="bg-slate-900 text-white text-xs py-2 px-4 rounded-lg font-semibold">
                  Return
                </button>
              </div>
            )}

            {amrState === 'expired' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-center space-y-3">
                <Clock className="w-6 h-6 text-slate-400 mx-auto" />
                <h4 className="text-xs font-bold text-slate-900">Session Request Expired</h4>
                <button onClick={handleRestart} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  New Challenge Request
                </button>
              </div>
            )}

            {amrState === 'cancelled' && (
              <div className="text-center py-6 space-y-3">
                <h4 className="text-xs font-semibold text-slate-800">Connection Canceled</h4>
                <button onClick={handleRestart} className="bg-indigo-600 text-white text-xs py-1.5 px-3 rounded-lg font-semibold">
                  Restart
                </button>
              </div>
            )}

            {amrState === 'success' && (
              <div className="bg-emerald-50 border border-emerald-100 rounded-xl p-6 text-center space-y-4">
                <UserCheck className="w-10 h-10 text-emerald-600 mx-auto" />
                <h4 className="text-base font-bold text-emerald-900 font-display">Authenticated Securely</h4>
                <div className="bg-white border border-emerald-200 rounded-lg p-3 text-left font-mono text-[10px] text-slate-600 space-y-1">
                  <div>SUBJECT: {email}</div>
                  <div>METHOD: AMR Location Confirmed</div>
                </div>
                <button onClick={handleRestart} className="w-full bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs py-2 rounded-lg">
                  Return to Portal Login
                </button>
              </div>
            )}

            {amrState === 'success requiring another step' && (
              <div className="bg-slate-50 border border-slate-200 rounded-xl p-5 text-center space-y-3">
                <CheckCircle2 className="w-8 h-8 text-emerald-500 mx-auto animate-pulse" />
                <h4 className="text-xs font-bold text-slate-900">Location Acceptable</h4>
                <p className="text-[11px] text-slate-500">Corporate policy triggers a supplementary OTP verification.</p>
                <button onClick={() => setAmrState('step-up required')} className="w-full bg-indigo-600 text-white text-xs py-2 rounded-lg font-semibold">
                  Continue to OTP Challenge
                </button>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
