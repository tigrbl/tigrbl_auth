import React, { useState, useEffect, useRef } from 'react';
import { SmsCeremonySession, SmsPolicy, Country, EnrolledPhone, SmsLog } from '../types';
import { Shield, Smartphone, Key, RefreshCw, Check, ArrowRight, AlertTriangle, ShieldAlert, Sparkles, Copy, X, Phone, UserCheck, ShieldCheck, Trash2, HelpCircle } from 'lucide-react';

interface CeremonyWizardProps {
  session: SmsCeremonySession | null;
  policy: SmsPolicy;
  countries: Country[];
  enrolledPhones: EnrolledPhone[];
  logs: SmsLog[];
  onStartEnrollment: () => void;
  onStartLogin: () => void;
  onStartStepUp: () => void;
  onStartReplacement: (phoneId: string) => void;
  onStartRecovery: () => void;
  onCancelSession: () => void;
  onSubmitPhoneNumber: (countryCode: string, dialCode: string, rawNumber: string) => void;
  onSendCode: () => void;
  onVerifyCode: (code: string) => void;
  onSaveEnrollment: (label: string) => void;
  onReplacePhone: (oldId: string, label: string) => void;
  onDeletePhone: (id: string) => void;
  simSwapRisk: 'low' | 'medium' | 'high';
  networkCondition: 'good' | 'congested' | 'outage';
}

export const CeremonyWizard: React.FC<CeremonyWizardProps> = ({
  session,
  policy,
  countries,
  enrolledPhones,
  logs,
  onStartEnrollment,
  onStartLogin,
  onStartStepUp,
  onStartReplacement,
  onStartRecovery,
  onCancelSession,
  onSubmitPhoneNumber,
  onSendCode,
  onVerifyCode,
  onSaveEnrollment,
  onReplacePhone,
  onDeletePhone,
  simSwapRisk,
  networkCondition,
}) => {
  // Input states
  const [phoneNumberInput, setPhoneNumberInput] = useState('');
  const [selectedCountryCode, setSelectedCountryCode] = useState('US');
  const [countrySearch, setCountrySearch] = useState('');
  const [showCountryDropdown, setShowCountryDropdown] = useState(false);
  const [consentChecked, setConsentChecked] = useState(false);
  const [otpInput, setOtpInput] = useState('');
  const [labelInput, setLabelInput] = useState('My Personal Mobile');
  const [selectedPhoneForAuth, setSelectedPhoneForAuth] = useState<string>('');

  // Auto-fill indicator state
  const [showAutofillBanner, setShowAutofillBanner] = useState(false);
  const [autofillCode, setAutofillCode] = useState('');

  // Refs
  const dropdownRef = useRef<HTMLDivElement>(null);

  // Close dropdown on click outside
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowCountryDropdown(false);
      }
    }
    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  // Sync selected phone for auth if available
  useEffect(() => {
    if (enrolledPhones.length > 0 && !selectedPhoneForAuth) {
      setSelectedPhoneForAuth(enrolledPhones[0].id);
    }
  }, [enrolledPhones, selectedPhoneForAuth]);

  // Autofill trigger detection
  useEffect(() => {
    if (session?.state === 'otp_waiting' && logs.length > 0) {
      // Find latest log for this active ceremony
      const latestLog = logs[0];
      if (latestLog && latestLog.state !== 'failed' && latestLog.code) {
        setAutofillCode(latestLog.code);
        setShowAutofillBanner(true);
      }
    } else {
      setShowAutofillBanner(false);
    }
  }, [session?.state, logs]);

  const selectedCountry = countries.find(c => c.code === selectedCountryCode) || countries[0];

  // Search filtered countries
  const filteredCountries = countries.filter(c =>
    c.name.toLowerCase().includes(countrySearch.toLowerCase()) ||
    c.dialCode.includes(countrySearch) ||
    c.code.toLowerCase().includes(countrySearch.toLowerCase())
  );

  // Simple E.164 normalization preview
  const formatPhoneNumberPreview = (raw: string, dial: string) => {
    const cleaned = raw.replace(/\D/g, '');
    if (!cleaned) return '';
    if (cleaned.length <= 3) {
      return `${dial} (${cleaned})`;
    }
    if (cleaned.length <= 6) {
      return `${dial} (${cleaned.slice(0, 3)}) ${cleaned.slice(3)}`;
    }
    return `${dial} (${cleaned.slice(0, 3)}) ${cleaned.slice(3, 6)}-${cleaned.slice(6, 10)}`;
  };

  const normalizedPreview = formatPhoneNumberPreview(phoneNumberInput, selectedCountry.dialCode);

  const handleCountrySelect = (code: string) => {
    setSelectedCountryCode(code);
    setShowCountryDropdown(false);
  };

  const handlePhoneSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!phoneNumberInput.replace(/\D/g, '')) return;
    if (!consentChecked) return;
    onSubmitPhoneNumber(selectedCountry.code, selectedCountry.dialCode, phoneNumberInput);
  };

  const triggerAutofill = () => {
    setOtpInput(autofillCode);
    setShowAutofillBanner(false);
    // Simulate real autofill submit delay
    setTimeout(() => {
      onVerifyCode(autofillCode);
    }, 400);
  };

  return (
    <div id="ceremony-container" className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative min-h-[480px] flex flex-col justify-between">
      {/* Native Autofill Banner Overlay */}
      {showAutofillBanner && (
        <div id="autofill-banner" className="absolute top-4 left-4 right-4 bg-indigo-950 border border-indigo-500 rounded-xl p-3 shadow-lg z-30 flex items-center justify-between animate-bounce">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-400" />
            <div>
              <p className="text-xs font-semibold text-slate-100">SMS Verification Autofill</p>
              <p className="text-[10px] text-indigo-300">Code <span className="font-mono font-bold text-white bg-indigo-900 px-1 py-0.5 rounded">{autofillCode}</span> received from carrier.</p>
            </div>
          </div>
          <button
            onClick={triggerAutofill}
            className="bg-indigo-600 hover:bg-indigo-500 text-white text-[11px] font-semibold px-2.5 py-1 rounded-lg transition"
          >
            Autofill Code
          </button>
        </div>
      )}

      {/* Header */}
      <div className="border-b border-slate-800 pb-3 mb-4 flex justify-between items-center">
        <div>
          <span className="text-[10px] uppercase font-mono bg-slate-950 text-indigo-400 border border-indigo-900/40 px-2 py-0.5 rounded-full">
            {session ? `${session.type.toUpperCase()} CEREMONY` : 'AUTHENTICATOR TERMINAL'}
          </span>
          <h3 className="text-lg font-bold font-display text-slate-100 mt-1">
            {session ? (
              session.type === 'enroll' ? 'Enroll New Phone' :
              session.type === 'login' ? 'SMS MFA Login' :
              session.type === 'step-up' ? 'Secure Step-Up challenge' :
              'Phone Authenticator'
            ) : 'Interactive Authenticator Hub'}
          </h3>
        </div>
        {session && (
          <button
            onClick={onCancelSession}
            className="p-1 rounded-full text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition"
            title="Cancel Ceremony"
          >
            <X className="w-4 h-4" />
          </button>
        )}
      </div>

      {/* Main Body */}
      <div className="flex-1 flex flex-col justify-center">
        {/* IDLE SCREEN (Hub of options) */}
        {!session && (
          <div className="space-y-4">
            <p className="text-xs text-slate-400 leading-relaxed">
              SMS acts as an identity channel to dispatch One-Time Passcodes (OTPs). Select a cryptographic workflow below to run the step-by-step ceremony.
            </p>

            {/* Scenarios / Trigger Buttons */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 mt-2">
              <button
                onClick={onStartEnrollment}
                className="p-4 rounded-xl border border-slate-800 hover:border-indigo-500/50 bg-slate-950 hover:bg-slate-800/30 text-left transition group"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <Smartphone className="w-4 h-4 text-indigo-400" />
                  <span className="text-xs font-bold text-slate-200">First-Party Enrollment</span>
                </div>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Go through the complete enrollment, country checks, E.164 verification, naming, and activation.
                </p>
              </button>

              <button
                onClick={onStartLogin}
                disabled={enrolledPhones.length === 0}
                className={`p-4 rounded-xl border text-left transition group ${enrolledPhones.length === 0 ? 'border-slate-800 opacity-50 cursor-not-allowed bg-slate-900/10' : 'border-slate-800 hover:border-indigo-500/50 bg-slate-950 hover:bg-slate-800/30'}`}
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <Key className="w-4 h-4 text-indigo-400" />
                  <span className="text-xs font-bold text-slate-200">SMS MFA / Login</span>
                </div>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Authenticate with an enrolled mobile phone. Authenticates with masked destination routing.
                </p>
              </button>

              <button
                onClick={onStartStepUp}
                disabled={enrolledPhones.length === 0}
                className={`p-4 rounded-xl border text-left transition group ${enrolledPhones.length === 0 ? 'border-slate-800 opacity-50 cursor-not-allowed bg-slate-900/10' : 'border-slate-800 hover:border-indigo-500/50 bg-slate-950 hover:bg-slate-800/30'}`}
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <ShieldCheck className="w-4 h-4 text-emerald-400" />
                  <span className="text-xs font-bold text-slate-200">Secure Step-Up</span>
                </div>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Requires fresh SMS challenge to confirm high-sensitivity administrative actions.
                </p>
              </button>

              <button
                onClick={onStartRecovery}
                className="p-4 rounded-xl border border-slate-800 hover:border-indigo-500/50 bg-slate-950 hover:bg-slate-800/30 text-left transition group"
              >
                <div className="flex items-center gap-2 mb-1.5">
                  <ShieldAlert className="w-4 h-4 text-amber-400" />
                  <span className="text-xs font-bold text-slate-200">Reduced Recovery</span>
                </div>
                <p className="text-[10px] text-slate-400 leading-relaxed">
                  Simulate account recovery utilizing lower-assurance phone channel with user alerts.
                </p>
              </button>
            </div>

            {/* Enrolled Authenticator Registry List */}
            <div className="mt-4 pt-4 border-t border-slate-800">
              <h4 className="text-xs font-semibold text-slate-200 mb-2 flex items-center gap-1">
                <Smartphone className="w-3.5 h-3.5 text-indigo-400" /> Enrolled Authenticators ({enrolledPhones.length})
              </h4>
              {enrolledPhones.length === 0 ? (
                <div className="p-4 bg-slate-950 border border-slate-800 rounded-xl text-center text-[11px] text-slate-500">
                  No active first-party authenticators found. Complete enrollment to register a phone.
                </div>
              ) : (
                <div className="space-y-2 max-h-32 overflow-y-auto">
                  {enrolledPhones.map(phone => (
                    <div key={phone.id} className="bg-slate-950 border border-slate-850 p-2.5 rounded-lg flex justify-between items-center text-xs">
                      <div className="flex items-center gap-2">
                        <div className="w-2 h-2 rounded-full bg-emerald-500" />
                        <div>
                          <span className="font-semibold text-slate-200">{phone.label}</span>
                          <span className="text-slate-400 font-mono text-[10px] ml-2">{phone.maskedNumber}</span>
                        </div>
                      </div>
                      <div className="flex gap-2">
                        <button
                          onClick={() => onStartReplacement(phone.id)}
                          className="text-[10px] text-indigo-400 hover:text-indigo-300 font-medium"
                        >
                          Replace
                        </button>
                        <button
                          onClick={() => onDeletePhone(phone.id)}
                          className="text-[10px] text-rose-400 hover:text-rose-300 font-medium"
                        >
                          Remove
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        )}

        {/* SCREEN 1: ENROLLMENT INTRODUCTION */}
        {session && session.state === 'introduction' && (
          <div className="space-y-4">
            <div className="bg-amber-950/20 border border-amber-500/20 p-3.5 rounded-xl flex gap-3">
              <ShieldAlert className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
              <div>
                <h4 className="text-xs font-bold text-slate-100">Lower Assurance Channel Notice</h4>
                <p className="text-[10px] text-slate-300 mt-0.5 leading-relaxed">
                  SMS is inherently <strong>not phishing resistant</strong> and is vulnerable to SIM-swapping, carrier routing hijacks, and baseband interception. FIDO2 Passkeys or App-based TOTP are recommended for high-assurance protection.
                </p>
              </div>
            </div>

            <div className="space-y-2 text-[11px] text-slate-400 pl-2">
              <p className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" /> Standard carrier messaging/roaming charges may apply.
              </p>
              <p className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" /> Phone number is strictly bound to tenant and transaction.
              </p>
              <p className="flex items-center gap-2">
                <Check className="w-3.5 h-3.5 text-emerald-400 shrink-0" /> SIM swaps or carrier port-outs are analyzed to block access.
              </p>
            </div>

            <div className="mt-4 pt-3 flex gap-2">
              <button
                onClick={onCancelSession}
                className="flex-1 py-2 bg-slate-800 hover:bg-slate-750 text-xs font-semibold rounded-xl text-slate-300 transition"
              >
                Go Back
              </button>
              <button
                onClick={() => {
                  if (session) onSubmitPhoneNumber('', '', ''); // progress to entry
                }}
                className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition flex items-center justify-center gap-1"
              >
                Accept &amp; Begin <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* SCREEN 2: PHONE ENTRY & COUNTRY SELECTION */}
        {session && session.state === 'entry' && (
          <div className="space-y-4">
            <p className="text-xs text-slate-400 leading-relaxed">
              Enter your mobile destination. We normalized the format to prevent SMS routing failures or bypasses.
            </p>

            <form onSubmit={handlePhoneSubmit} className="space-y-4">
              <div className="relative" ref={dropdownRef}>
                <label className="text-[10px] uppercase font-mono text-slate-400 block mb-1">Country / Regional Code</label>
                <button
                  type="button"
                  onClick={() => setShowCountryDropdown(!showCountryDropdown)}
                  className="w-full bg-slate-950 border border-slate-800 rounded-xl px-3.5 py-2.5 text-xs text-slate-200 flex justify-between items-center focus:outline-none focus:border-indigo-500"
                >
                  <span className="flex items-center gap-2">
                    <span className="text-base">{selectedCountry.flag}</span>
                    <span>{selectedCountry.name} ({selectedCountry.dialCode})</span>
                  </span>
                  <span className="text-slate-400">▼</span>
                </button>

                {showCountryDropdown && (
                  <div className="absolute top-full left-0 right-0 mt-2 bg-slate-950 border border-slate-800 rounded-xl shadow-2xl z-40 p-2 max-h-52 overflow-y-auto">
                    <input
                      type="text"
                      placeholder="Search country..."
                      value={countrySearch}
                      onChange={(e) => setCountrySearch(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg px-2.5 py-1.5 text-xs text-slate-100 focus:outline-none mb-2 font-mono"
                    />
                    <div className="space-y-1">
                      {filteredCountries.map(c => (
                        <button
                          key={c.code}
                          type="button"
                          onClick={() => handleCountrySelect(c.code)}
                          className={`w-full text-left p-2 rounded text-xs flex justify-between items-center ${c.code === selectedCountryCode ? 'bg-indigo-950/40 text-indigo-400 font-semibold' : 'hover:bg-slate-900 text-slate-300'}`}
                        >
                          <span className="flex items-center gap-2">
                            <span>{c.flag}</span>
                            <span>{c.name} ({c.dialCode})</span>
                          </span>
                          {!c.isAllowed && (
                            <span className="text-[9px] font-mono bg-rose-950 text-rose-400 px-1.5 py-0.5 rounded">BLOCKED BY POLICY</span>
                          )}
                        </button>
                      ))}
                    </div>
                  </div>
                )}
              </div>

              <div>
                <label className="text-[10px] uppercase font-mono text-slate-400 block mb-1">Mobile Phone Number</label>
                <div className="relative">
                  <input
                    type="tel"
                    placeholder="e.g. 555-019-2831"
                    value={phoneNumberInput}
                    onChange={(e) => setPhoneNumberInput(e.target.value)}
                    className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-10 pr-4 py-2.5 text-xs text-slate-200 font-mono focus:outline-none focus:border-indigo-500"
                    required
                  />
                  <Phone className="w-4 h-4 text-slate-500 absolute left-3.5 top-3" />
                </div>
              </div>

              {/* Normalization Preview */}
              {phoneNumberInput && (
                <div className="bg-slate-950 border border-slate-850 rounded-xl p-2.5">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-slate-400 font-mono">E.164 Clean Format:</span>
                    <span className="text-indigo-400 font-mono text-xs font-semibold">{normalizedPreview}</span>
                  </div>
                  {!selectedCountry.isAllowed && (
                    <div className="mt-1.5 flex items-center gap-1.5 text-rose-400 text-[10px] font-mono">
                      <AlertTriangle className="w-3.5 h-3.5" /> Regional security policy blocks dispatch.
                    </div>
                  )}
                </div>
              )}

              {/* Consent Notice */}
              <div className="flex items-start gap-2.5">
                <input
                  type="checkbox"
                  id="consentCheckbox"
                  checked={consentChecked}
                  onChange={(e) => setConsentChecked(e.target.checked)}
                  className="mt-1 accent-indigo-500"
                  required
                />
                <label htmlFor="consentCheckbox" className="text-[10px] text-slate-400 leading-relaxed cursor-pointer">
                  I consent to receive high-frequency security codes. I acknowledge that authentication records are audited, and SMS channel features lower assurance guarantees.
                </label>
              </div>

              <div className="pt-2 flex gap-2">
                <button
                  type="button"
                  onClick={onCancelSession}
                  className="flex-1 py-2 bg-slate-850 hover:bg-slate-800 text-xs font-semibold rounded-xl text-slate-400 transition"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={!phoneNumberInput || !consentChecked || !selectedCountry.isAllowed}
                  className={`flex-1 py-2 text-xs font-semibold rounded-xl text-white transition flex items-center justify-center gap-1 ${(!phoneNumberInput || !consentChecked || !selectedCountry.isAllowed) ? 'bg-slate-800 text-slate-500 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500'}`}
                >
                  Continue <ArrowRight className="w-3.5 h-3.5" />
                </button>
              </div>
            </form>
          </div>
        )}

        {/* SCREEN 3: VERIFICATION SEND CONFIRMATION */}
        {session && session.state === 'send_pending' && (
          <div className="space-y-4">
            <div className="text-center py-4">
              <div className="w-12 h-12 bg-indigo-950 border border-indigo-500 rounded-full flex items-center justify-center mx-auto mb-3 text-indigo-400">
                <Phone className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-slate-100">Confirm Mobile Destination</h4>
              <p className="text-xs text-slate-400 mt-1">Ready to dispatch challenge credentials to:</p>
              <p className="text-lg font-mono font-bold text-slate-200 mt-2 bg-slate-950 border border-slate-850 inline-block px-4 py-1.5 rounded-xl">
                {session.maskedNumber}
              </p>
            </div>

            <div className="bg-slate-950 border border-slate-850 p-3 rounded-xl space-y-2 text-[10px] font-mono text-slate-400">
              <div className="flex justify-between">
                <span>SMS Channel:</span>
                <span className="text-slate-300">Lower Assurance</span>
              </div>
              <div className="flex justify-between">
                <span>SIM Swap Query:</span>
                <span className={`${simSwapRisk === 'high' ? 'text-rose-400 font-bold' : 'text-emerald-400'}`}>
                  {simSwapRisk === 'high' ? 'CRITICAL SIGNAL BLOCK' : 'Verified (IMSI Cleared)'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Network Routing:</span>
                <span className="text-indigo-400">Dynamic Provider Allocation</span>
              </div>
            </div>

            {simSwapRisk === 'high' && (
              <div className="bg-rose-950/20 border border-rose-500/20 p-3 rounded-xl text-[10px] text-rose-300 flex gap-2">
                <ShieldAlert className="w-4 h-4 text-rose-500 shrink-0" />
                <span>
                  <strong>Carrier Threat Signal Raised:</strong> Our platform detected recent SIM swap or port activity for this IMSI. Dispatch blocked to prevent account takeover.
                </span>
              </div>
            )}

            <div className="pt-2 flex gap-2">
              <button
                onClick={onCancelSession}
                className="flex-1 py-2 bg-slate-850 hover:bg-slate-800 text-xs font-semibold rounded-xl text-slate-400 transition"
              >
                Change Number
              </button>
              <button
                onClick={onSendCode}
                disabled={simSwapRisk === 'high'}
                className={`flex-1 py-2 text-xs font-semibold rounded-xl text-white transition flex items-center justify-center gap-1 ${simSwapRisk === 'high' ? 'bg-slate-800 text-slate-600 cursor-not-allowed' : 'bg-indigo-600 hover:bg-indigo-500'}`}
              >
                Send Secure Code
              </button>
            </div>
          </div>
        )}

        {/* SCREEN 4: SMS OTP WAITING / CHALLENGE (P0 Release Gate) */}
        {session && session.state === 'otp_waiting' && (
          <div className="space-y-4">
            <div className="bg-slate-950 border border-slate-850 p-3 rounded-xl text-[11px]">
              <div className="flex justify-between items-center">
                <span className="text-slate-400">Recipient:</span>
                <span className="font-mono text-slate-200 font-bold">{session.maskedNumber}</span>
              </div>
              {/* Delivery progress flow */}
              <div className="mt-3.5">
                <div className="flex justify-between items-center text-[9px] uppercase font-mono text-slate-500 mb-1.5">
                  <span>Routing Progress</span>
                  <span className={`${session.subState === 'failed' ? 'text-rose-400' : 'text-indigo-400'}`}>
                    {session.subState.toUpperCase()}
                  </span>
                </div>
                <div className="grid grid-cols-3 gap-1">
                  <div className={`h-1 rounded ${session.subState === 'queued' || session.subState === 'delivered' || session.subState === 'delayed' ? 'bg-indigo-500 animate-pulse' : 'bg-slate-800'}`} />
                  <div className={`h-1 rounded ${session.subState === 'delayed' ? 'bg-amber-500 animate-pulse' : session.subState === 'delivered' ? 'bg-indigo-500' : 'bg-slate-800'}`} />
                  <div className={`h-1 rounded ${session.subState === 'delivered' ? 'bg-emerald-500' : session.subState === 'failed' ? 'bg-rose-500' : 'bg-slate-800'}`} />
                </div>
                
                {/* Specific Delivery State Status Texts */}
                <div className="mt-2 text-[10px] text-slate-400 font-mono">
                  {session.subState === 'queued' && (
                    <span className="text-blue-400 flex items-center gap-1">
                      <RefreshCw className="w-3.5 h-3.5 animate-spin" /> Enqueued on carrier gateway. Dispatching...
                    </span>
                  )}
                  {session.subState === 'delivered' && (
                    <span className="text-emerald-400 flex items-center gap-1">
                      <Check className="w-3.5 h-3.5" /> SMS received by carrier tower. Code is bound.
                    </span>
                  )}
                  {session.subState === 'delayed' && (
                    <span className="text-amber-400 flex items-center gap-1">
                      <AlertTriangle className="w-3.5 h-3.5" /> Gateway delay reported (Congested). Retry later.
                    </span>
                  )}
                  {session.subState === 'failed' && (
                    <span className="text-rose-400 flex items-center gap-1">
                      <ShieldAlert className="w-3.5 h-3.5" /> Handshake failed. Provider offline or number blocked.
                    </span>
                  )}
                </div>
              </div>
            </div>

            <div className="text-center space-y-1">
              <label htmlFor="otpCodeField" className="text-xs font-semibold text-slate-300">Enter Challenge Code</label>
              <div className="relative max-w-[240px] mx-auto">
                <input
                  id="otpCodeField"
                  type="text"
                  maxLength={6}
                  placeholder="••••••"
                  value={otpInput}
                  onChange={(e) => setOtpInput(e.target.value.replace(/\D/g, ''))}
                  className="w-full text-center bg-slate-950 border-2 border-slate-800 focus:border-indigo-500 rounded-xl py-3 text-2xl font-mono tracking-[0.5em] focus:outline-none"
                  autoFocus
                  autoComplete="one-time-code"
                />
              </div>
              <p className="text-[10px] text-slate-400 mt-1 font-mono">
                Code expires in: <span className="text-indigo-400">{session.expiryCountdown}s</span>
              </p>
            </div>

            {/* Error notifications (Invalid/expired/rate-limited) */}
            {session.attemptsCount > 0 && (
              <div className="bg-rose-950/20 border border-rose-500/20 p-2.5 rounded-xl text-[10px] text-rose-300 flex items-center gap-2">
                <ShieldAlert className="w-4 h-4 text-rose-400 shrink-0" />
                <span>
                  Incorrect credentials. Attempt {session.attemptsCount} of {policy.maxAttempts}. Unlocked countdown locks number.
                </span>
              </div>
            )}

            {/* Unsafe destination mutation blocks check */}
            <div className="text-center text-[10px] text-slate-500 bg-slate-950 p-2 rounded-lg font-mono">
              🔒 Destination modification locked during verification.
            </div>

            {/* Resend Control */}
            <div className="flex flex-col items-center gap-1 pb-1">
              {session.resendCountdown > 0 ? (
                <span className="text-[10px] text-slate-500 font-mono">
                  Resend available in <strong className="text-slate-400">{session.resendCountdown}s</strong>
                </span>
              ) : (
                <button
                  type="button"
                  onClick={onSendCode}
                  className="text-xs text-indigo-400 hover:text-indigo-300 font-semibold hover:underline flex items-center gap-1"
                >
                  <RefreshCw className="w-3 h-3" /> Resend Verification Code
                </button>
              )}
            </div>

            <div className="flex gap-2">
              <button
                type="button"
                onClick={onCancelSession}
                className="flex-1 py-2 bg-slate-850 hover:bg-slate-800 text-xs font-semibold rounded-xl text-slate-400 transition"
              >
                Switch Method
              </button>
              <button
                type="button"
                onClick={() => onVerifyCode(otpInput)}
                disabled={otpInput.length !== 6 || session.subState === 'failed'}
                className={`flex-1 py-2 text-xs font-semibold rounded-xl text-white transition ${otpInput.length === 6 && session.subState !== 'failed' ? 'bg-indigo-600 hover:bg-indigo-500' : 'bg-slate-800 text-slate-500 cursor-not-allowed'}`}
              >
                Submit Code
              </button>
            </div>
          </div>
        )}

        {/* SCREEN 5: ENROLLMENT COMPLETION & NAMING */}
        {session && session.state === 'completed' && session.type === 'enroll' && (
          <div className="space-y-4">
            <div className="text-center py-4">
              <div className="w-12 h-12 bg-emerald-950 border border-emerald-500 rounded-full flex items-center justify-center mx-auto mb-3 text-emerald-400">
                <UserCheck className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-slate-100">Phone Ownership Verified</h4>
              <p className="text-xs text-slate-400 mt-1">Successfully linked {session.maskedNumber}</p>
            </div>

            <div className="space-y-3 bg-slate-950 border border-slate-850 p-4 rounded-xl">
              <div>
                <label htmlFor="authenticatorLabelField" className="text-[10px] uppercase font-mono text-slate-400 block mb-1">Friendly Label / Device Name</label>
                <input
                  id="authenticatorLabelField"
                  type="text"
                  value={labelInput}
                  onChange={(e) => setLabelInput(e.target.value)}
                  placeholder="e.g. Work Cell, Secondary SIM"
                  className="w-full bg-slate-900 border border-slate-800 rounded-lg px-3 py-2 text-xs text-slate-200 focus:outline-none focus:border-indigo-500"
                />
              </div>

              <div className="p-2.5 bg-indigo-950/20 border border-indigo-500/10 rounded-lg text-[10px] text-indigo-300 leading-relaxed">
                ℹ️ <strong>Stronger Factor Advisory:</strong> Your account now contains an SMS Authenticator. To prevent phishing bypasses, configure an authenticator app (TOTP) or hardware key as primary login.
              </div>
            </div>

            <button
              type="button"
              onClick={() => onSaveEnrollment(labelInput)}
              className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition flex items-center justify-center gap-1"
            >
              Activate Authenticator
            </button>
          </div>
        )}

        {/* SCREEN 6: SMS LOGIN MFA METHOD SELECTION AND DISPATCH */}
        {session && (session.type === 'login' || session.type === 'step-up') && session.state === 'introduction' && (
          <div className="space-y-4">
            <p className="text-xs text-slate-400 leading-relaxed">
              Verify your identity. Select your enrolled phone authenticator to receive an SMS confirmation.
            </p>

            <div className="space-y-2">
              {enrolledPhones.map(phone => (
                <button
                  key={phone.id}
                  onClick={() => setSelectedPhoneForAuth(phone.id)}
                  className={`w-full text-left p-3 rounded-xl border transition flex items-center justify-between ${selectedPhoneForAuth === phone.id ? 'bg-indigo-950/20 border-indigo-500/60 text-indigo-300' : 'bg-slate-950 border-slate-850 text-slate-300 hover:bg-slate-900'}`}
                >
                  <div className="flex items-center gap-3">
                    <Smartphone className="w-5 h-5 opacity-80" />
                    <div>
                      <p className="text-xs font-semibold text-slate-200">{phone.label}</p>
                      <p className="text-[10px] text-slate-400 font-mono mt-0.5">{phone.maskedNumber}</p>
                    </div>
                  </div>
                  <div className={`w-4 h-4 rounded-full border flex items-center justify-center ${selectedPhoneForAuth === phone.id ? 'border-indigo-400 bg-indigo-600' : 'border-slate-700'}`}>
                    {selectedPhoneForAuth === phone.id && <Check className="w-2.5 h-2.5 text-white" />}
                  </div>
                </button>
              ))}
            </div>

            {session.type === 'step-up' && (
              <div className="bg-amber-950/20 border border-amber-500/20 p-2.5 rounded-lg text-[10px] text-amber-300 flex gap-2">
                <ShieldAlert className="w-4 h-4 text-amber-400 shrink-0" />
                <span>
                  <strong>Step-Up Authentication Required:</strong> You are accessing secure policy resources. A fresh verification code will validate session context.
                </span>
              </div>
            )}

            <div className="pt-2 flex gap-2">
              <button
                onClick={onCancelSession}
                className="flex-1 py-2 bg-slate-850 hover:bg-slate-800 text-xs font-semibold rounded-xl text-slate-400 transition"
              >
                Go Back
              </button>
              <button
                onClick={() => {
                  const p = enrolledPhones.find(x => x.id === selectedPhoneForAuth);
                  if (p) onSubmitPhoneNumber(p.countryCode, '', p.number);
                }}
                className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition flex items-center justify-center gap-1"
              >
                Dispatch OTP SMS <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* SCREEN 7: SUCCESS EVIDENCE & SECURITY ARTIFACTS DETAIL (Verification Success) */}
        {session && session.state === 'completed' && (session.type === 'login' || session.type === 'step-up') && (
          <div className="space-y-4">
            <div className="text-center py-2">
              <div className="w-12 h-12 bg-emerald-950 border border-emerald-500 rounded-full flex items-center justify-center mx-auto mb-2 text-emerald-400">
                <Shield className="w-5 h-5 animate-pulse" />
              </div>
              <h4 className="text-sm font-bold text-slate-100">Identity Cryptographic Verified</h4>
              <p className="text-xs text-slate-400 mt-0.5">Success next-factor tokens compiled.</p>
            </div>

            <div className="bg-slate-950 border border-slate-850 rounded-xl p-3.5 space-y-3">
              <div className="flex justify-between items-center pb-2 border-b border-slate-850">
                <span className="text-[10px] uppercase font-mono text-slate-400">Verification Evidence</span>
                <span className="text-[9px] font-mono text-emerald-400 bg-emerald-950 px-2 py-0.5 rounded border border-emerald-500/20">OTP MATCHED</span>
              </div>

              <div className="space-y-2 font-mono text-[10px] text-slate-300">
                <div className="flex justify-between">
                  <span className="text-slate-500">Channel Type:</span>
                  <span>SMS/OTP (Lower Assurance)</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Destination:</span>
                  <span>{session.maskedNumber}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Server Time:</span>
                  <span className="text-slate-400">{new Date().toISOString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Gateway Path:</span>
                  <span className="text-indigo-400">{session.providerId || 'Tier-1-Direct'}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-slate-500">Token Expiry:</span>
                  <span className="text-amber-400">Freshness &lt; 1s ago</span>
                </div>
              </div>

              <div className="p-2 bg-slate-900 rounded text-[9px] text-slate-400 leading-relaxed">
                ⚠️ <strong>Phishing Advisory:</strong> This evidence token was issued via lower-assurance SMS fallback. In high-risk environments, step-up requirements or hardware keys are recommended.
              </div>
            </div>

            <button
              onClick={onCancelSession}
              className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition"
            >
              Return to Hub
            </button>
          </div>
        )}

        {/* SCREEN 8: GENERAL FAILURE STALL SCREEN */}
        {session && session.state === 'failed' && (
          <div className="space-y-4">
            <div className="text-center py-4">
              <div className="w-12 h-12 bg-rose-950 border border-rose-500 rounded-full flex items-center justify-center mx-auto mb-3 text-rose-400">
                <ShieldAlert className="w-5 h-5" />
              </div>
              <h4 className="text-sm font-bold text-slate-100">Ceremony Aborted</h4>
              <p className="text-xs text-rose-400 mt-1">
                {session.subState === 'blocked' ? 'Blocked due to anti-fraud policy' : 'Too many invalid attempts or session expired'}
              </p>
            </div>

            <p className="text-xs text-slate-400 leading-relaxed text-center px-4">
              To defend against SMS toll fraud, premium toll pumping, or SIM swap hijacking, authentication sessions are locked on failure. Prior codes are permanently invalidated.
            </p>

            <div className="bg-slate-950 border border-slate-850 p-3 rounded-xl space-y-2 text-[10px] font-mono text-slate-400">
              <div className="flex justify-between">
                <span>Reason:</span>
                <span className="text-rose-400">
                  {session.subState === 'blocked' ? 'Threat/SIM swap risk flagged' : 'Credential exhaustion'}
                </span>
              </div>
              <div className="flex justify-between">
                <span>Remediation:</span>
                <span className="text-slate-300">Contact Tenant Support Desk</span>
              </div>
            </div>

            <button
              onClick={onCancelSession}
              className="w-full py-2 bg-slate-800 hover:bg-slate-750 text-xs font-semibold rounded-xl text-slate-300 transition"
            >
              Restart Ceremony
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
