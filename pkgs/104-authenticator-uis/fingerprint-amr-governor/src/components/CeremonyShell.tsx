import React, { useState, useEffect } from 'react';
import { CeremonyState, CeremonyType, BiometricErrorType, PolicyConfig } from '../types';
import { Fingerprint, Key, Shield, Layers, HelpCircle, AlertTriangle, AlertCircle, CheckCircle, RefreshCw, Smartphone, Laptop, Sparkles, Send } from 'lucide-react';

interface CeremonyShellProps {
  onSuccess: (evidence: {
    hasFpt: boolean;
    isTrusted: boolean;
    detectedAmrs: string[];
    provider: string;
    directVsTransformed: 'direct' | 'transformed' | 'none';
    description: string;
    outcomeStatus: 'approved' | 'blocked' | 'fallback';
  }) => void;
  policy: PolicyConfig;
  providers: Array<{ id: string; name: string; issuerUrl: string; status: 'online' | 'degraded' | 'outage' }>;
}

export default function CeremonyShell({ onSuccess, policy, providers }: CeremonyShellProps) {
  const [activeCeremony, setActiveCeremony] = useState<CeremonyType>('passkey_login');
  const [state, setState] = useState<CeremonyState>('idle');
  const [outcome, setOutcome] = useState<string | null>(null);
  
  // Custom simulation configs
  const [uvType, setUvType] = useState<'fpt_proven' | 'generic_uv' | 'cancelled' | 'lockout' | 'unavailable' | 'unsupported'>('fpt_proven');
  const [selectedFederatedProvider, setSelectedFederatedProvider] = useState<string>(providers[0]?.id || '');
  const [transactionAmount, setTransactionAmount] = useState<number>(6500); // Trigger step-up if policy require
  
  // Progress timer for animations
  const [progress, setProgress] = useState(0);

  // Restart/reset ceremony
  const resetCeremony = () => {
    setState('idle');
    setOutcome(null);
    setProgress(0);
  };

  useEffect(() => {
    resetCeremony();
  }, [activeCeremony]);

  // Start Ceremony Step-by-Step
  const startCeremony = () => {
    if (activeCeremony === 'federated_login') {
      const selectedP = providers.find(p => p.id === selectedFederatedProvider);
      if (selectedP && selectedP.status === 'outage') {
        setState('error');
        setOutcome(`Identity Provider (${selectedP.name}) is currently offline. Federation tunnel severed.`);
        onSuccess({
          hasFpt: false,
          isTrusted: false,
          detectedAmrs: [],
          provider: selectedP.name,
          directVsTransformed: 'none',
          description: `Federation attempted with offline IdP: ${selectedP.name}. Action aborted.`,
          outcomeStatus: 'blocked'
        });
        return;
      }
    }

    setState('initializing');
    setProgress(15);
    
    setTimeout(() => {
      setState('ready');
      setProgress(40);
      
      // Auto open system OS prompt simulator if not manual selection
      setTimeout(() => {
        setState('prompt');
        setProgress(70);
      }, 700);
    }, 800);
  };

  // User interacts with simulated OS Prompt
  const handleOSPromptOutcome = (success: boolean, error?: BiometricErrorType) => {
    setState('submitting');
    setProgress(90);

    setTimeout(() => {
      if (!success) {
        setState('error');
        if (error === 'lockout') {
          setOutcome("Sensor locked out. Too many failed attempts. Device PIN or recovery phrase is required to unlock biometric services.");
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: ["hw", "user"],
            provider: activeCeremony === 'native_handoff' ? "Native Android Verifier" : "WebAuthn Windows Hello",
            directVsTransformed: 'none',
            description: "Biometric sensor lockout triggered during local authentication ceremony.",
            outcomeStatus: 'fallback'
          });
        } else if (error === 'sensor_unavailable') {
          setOutcome("Fingerprint sensor is not responding or hardware was disconnected.");
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: ["hw", "user"],
            provider: "Generic OS Client",
            directVsTransformed: 'none',
            description: "Sensor unavailable error received during passkey prompt.",
            outcomeStatus: 'fallback'
          });
        } else if (error === 'cancelled') {
          setOutcome("Authentication ceremony cancelled by the user.");
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: [],
            provider: "Browser Agent",
            directVsTransformed: 'none',
            description: "Authentication ceremony cancelled by subject.",
            outcomeStatus: 'blocked'
          });
        } else if (error === 'unsupported_environment') {
          setOutcome("Security error: current iframe context or browser flags do not support passwordless biometric credentials.");
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: [],
            provider: "Iframe Sandbox Agent",
            directVsTransformed: 'none',
            description: "Unsupported biometric browser context.",
            outcomeStatus: 'blocked'
          });
        }
        return;
      }

      // Success branch
      setState('success');
      setProgress(100);

      if (activeCeremony === 'passkey_login') {
        if (uvType === 'fpt_proven') {
          setOutcome("Assertion submitted and approved! Server verified custom direct hardware attestations.");
          onSuccess({
            hasFpt: true,
            isTrusted: true,
            detectedAmrs: ["hw", "user", "uv", "fpt"],
            provider: "iOS Platform Agent v2",
            directVsTransformed: 'direct',
            description: "Passkey verification succeeded with trusted direct Fingerprint AMR evidence.",
            outcomeStatus: 'approved'
          });
        } else if (uvType === 'generic_uv') {
          setOutcome("Assertion approved! User presence verified (uv=true). Modality remains concealed.");
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: ["hw", "user", "uv"],
            provider: "WebAuthn Generic RP",
            directVsTransformed: 'none',
            description: "Passkey assertion completed. Generic user-verification (UV) verified, but modality is unproven.",
            outcomeStatus: policy.requireFingerprint ? 'fallback' : 'approved'
          });
        }
      } else if (activeCeremony === 'federated_login') {
        const selectedP = providers.find(p => p.id === selectedFederatedProvider);
        const providerName = selectedP ? selectedP.name : "Okta Enterprise Gate";
        
        if (uvType === 'fpt_proven') {
          setOutcome(`Federation handshake finalized. Upstream claims successfully transformed into fpt.`);
          onSuccess({
            hasFpt: true,
            isTrusted: true,
            detectedAmrs: ["hw", "user", "uv", "fpt"],
            provider: providerName,
            directVsTransformed: 'transformed',
            description: `Federated login via ${providerName}. Upstream credentials transformed with trusted FPT AMR.`,
            outcomeStatus: 'approved'
          });
        } else {
          setOutcome(`Federation complete. Provider supplied general verification tokens only.`);
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: ["hw", "user", "uv"],
            provider: providerName,
            directVsTransformed: 'none',
            description: `Federated login via ${providerName} completed with generic non-biometric credentials.`,
            outcomeStatus: policy.requireFingerprint ? 'fallback' : 'approved'
          });
        }
      } else if (activeCeremony === 'step_up') {
        if (uvType === 'fpt_proven') {
          setOutcome(`Step-up authentication verified for action. Fingerprint signature stored.`);
          onSuccess({
            hasFpt: true,
            isTrusted: true,
            detectedAmrs: ["hw", "user", "uv", "fpt"],
            provider: "Corporate Key Broker",
            directVsTransformed: 'direct',
            description: `High value step-up auth ($${transactionAmount.toLocaleString()}) satisfied with physical fingerprint evidence.`,
            outcomeStatus: 'approved'
          });
        } else {
          setOutcome(`Step-up completed but lacked physical fingerprint proof.`);
          onSuccess({
            hasFpt: false,
            isTrusted: false,
            detectedAmrs: ["hw", "user", "uv"],
            provider: "Corporate Key Broker",
            directVsTransformed: 'none',
            description: `Step-up auth ($${transactionAmount.toLocaleString()}) attempted but rejected/redirected because only generic UV was offered.`,
            outcomeStatus: 'fallback'
          });
        }
      } else if (activeCeremony === 'native_handoff') {
        setOutcome(`Native device contract handoff finalized. Fingerprint AMR verified directly from trusted platform.`);
        onSuccess({
          hasFpt: true,
          isTrusted: true,
          detectedAmrs: ["hw", "user", "uv", "fpt"],
          provider: "Android Biometric SDK",
          directVsTransformed: 'direct',
          description: "Completed secure Native SDK handoff ceremony with verified FPT AMR evidence.",
          outcomeStatus: 'approved'
        });
      }
    }, 1200);
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-6" id="ceremony-shell-workspace">
      {/* Control / Chooser Panel */}
      <div className="lg:col-span-5 bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-5">
        <div>
          <h3 className="font-semibold text-slate-200 text-sm">Choose Ceremony Flow</h3>
          <p className="text-2xs text-slate-500 mt-0.5">
            Select the verification ceremony context to run. Primary labels are strictly passwordless.
          </p>
        </div>

        {/* Primary Method Buttons */}
        <div className="space-y-2">
          {/* Option 1: Passkey */}
          <button
            type="button"
            onClick={() => setActiveCeremony('passkey_login')}
            className={`w-full text-left p-3 rounded-lg border transition duration-150 flex items-start gap-3 ${
              activeCeremony === 'passkey_login'
                ? 'bg-indigo-950/20 border-indigo-700 text-slate-200'
                : 'bg-slate-900/40 border-slate-900 text-slate-400 hover:bg-slate-900'
            }`}
          >
            <Key className="w-5 h-5 text-indigo-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-xs block text-slate-200">Sign in with Passkey / Security Key</span>
              <span className="text-3xs text-slate-500 block mt-0.5">
                Your device may ask for a fingerprint, face, PIN, or another unlock method.
              </span>
            </div>
          </button>

          {/* Option 2: Federated Login */}
          <button
            type="button"
            onClick={() => setActiveCeremony('federated_login')}
            className={`w-full text-left p-3 rounded-lg border transition duration-150 flex items-start gap-3 ${
              activeCeremony === 'federated_login'
                ? 'bg-sky-950/20 border-sky-700 text-slate-200'
                : 'bg-slate-900/40 border-slate-900 text-slate-400 hover:bg-slate-900'
            }`}
          >
            <Layers className="w-5 h-5 text-sky-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-xs block text-slate-200">Sign in with Federated Provider</span>
              <span className="text-3xs text-slate-500 block mt-0.5">
                Redirects user to upstream IdP with claim transformation configured.
              </span>
            </div>
          </button>

          {/* Option 3: MFA / Step-up */}
          <button
            type="button"
            onClick={() => setActiveCeremony('step_up')}
            className={`w-full text-left p-3 rounded-lg border transition duration-150 flex items-start gap-3 ${
              activeCeremony === 'step_up'
                ? 'bg-violet-950/20 border-violet-700 text-slate-200'
                : 'bg-slate-900/40 border-slate-900 text-slate-400 hover:bg-slate-900'
            }`}
          >
            <Shield className="w-5 h-5 text-violet-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-xs block text-slate-200">Secure Transaction Step-up</span>
              <span className="text-3xs text-slate-500 block mt-0.5">
                Prompts for explicit verified fingerprint confirmation before processing payment.
              </span>
            </div>
          </button>

          {/* Option 4: Native biometric handoff */}
          <button
            type="button"
            onClick={() => setActiveCeremony('native_handoff')}
            className={`w-full text-left p-3 rounded-lg border transition duration-150 flex items-start gap-3 ${
              activeCeremony === 'native_handoff'
                ? 'bg-emerald-950/20 border-emerald-700 text-slate-200'
                : 'bg-slate-900/40 border-slate-900 text-slate-400 hover:bg-slate-900'
            }`}
          >
            <Smartphone className="w-5 h-5 text-emerald-400 flex-shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-xs block text-slate-200">Native Biometric SDK Handoff</span>
              <span className="text-3xs text-slate-500 block mt-0.5">
                Launches external platform contract verifier to emit dedicated FPT proof.
              </span>
            </div>
          </button>
        </div>

        {/* Simulation Configuration Inputs */}
        <div className="border-t border-slate-900 pt-4 space-y-3">
          <span className="text-2xs font-bold text-slate-400 uppercase block font-mono">Simulation Parameters</span>

          {/* Federated Provider dropdown if relevant */}
          {activeCeremony === 'federated_login' && (
            <div className="space-y-1">
              <label className="text-3xs text-slate-500 uppercase font-mono block">Selected Federated Gateway:</label>
              <select
                className="w-full bg-slate-900 border border-slate-800 rounded px-2.5 py-1.5 text-xs text-slate-300"
                value={selectedFederatedProvider}
                onChange={(e) => setSelectedFederatedProvider(e.target.value)}
              >
                {providers.map(p => (
                  <option key={p.id} value={p.id}>{p.name} ({p.status})</option>
                ))}
              </select>
            </div>
          )}

          {/* Step Up Transaction Amount if relevant */}
          {activeCeremony === 'step_up' && (
            <div className="space-y-1">
              <label className="text-3xs text-slate-500 uppercase font-mono block">Transaction Value:</label>
              <div className="flex gap-2">
                <input
                  type="number"
                  className="bg-slate-900 border border-slate-800 rounded px-2.5 py-1 text-xs text-slate-300 w-full font-mono"
                  value={transactionAmount}
                  onChange={(e) => setTransactionAmount(parseInt(e.target.value) || 0)}
                />
                <span className="bg-slate-900 border border-slate-800 px-3 py-1 rounded text-3xs flex items-center text-slate-500 font-mono">
                  USD
                </span>
              </div>
            </div>
          )}

          {/* Outcome Toggle (What type of verification the user does on the OS/Browser) */}
          <div className="space-y-1">
            <label className="text-3xs text-slate-500 uppercase font-mono block">Simulated Device State:</label>
            <div className="grid grid-cols-2 gap-1.5 text-3xs font-mono">
              <button
                type="button"
                onClick={() => setUvType('fpt_proven')}
                className={`p-1.5 rounded border text-center transition ${
                  uvType === 'fpt_proven'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                Fingerprint Proven
              </button>
              
              <button
                type="button"
                disabled={activeCeremony === 'native_handoff'}
                onClick={() => setUvType('generic_uv')}
                className={`p-1.5 rounded border text-center transition disabled:opacity-30 ${
                  uvType === 'generic_uv'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                Generic UV Only
              </button>

              <button
                type="button"
                onClick={() => setUvType('cancelled')}
                className={`p-1.5 rounded border text-center transition ${
                  uvType === 'cancelled'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                User Cancelled
              </button>

              <button
                type="button"
                onClick={() => setUvType('lockout')}
                className={`p-1.5 rounded border text-center transition ${
                  uvType === 'lockout'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                Sensor Lockout
              </button>

              <button
                type="button"
                onClick={() => setUvType('unavailable')}
                className={`p-1.5 rounded border text-center transition ${
                  uvType === 'unavailable'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                Sensor Missing
              </button>

              <button
                type="button"
                onClick={() => setUvType('unsupported')}
                className={`p-1.5 rounded border text-center transition ${
                  uvType === 'unsupported'
                    ? 'bg-indigo-950/35 border-indigo-700 text-indigo-300 font-bold'
                    : 'bg-slate-900 border-slate-850 text-slate-500 hover:border-slate-800'
                }`}
              >
                Unsupported Env
              </button>
            </div>
          </div>
        </div>

        {/* Start Button */}
        <button
          onClick={startCeremony}
          disabled={state !== 'idle' && state !== 'error' && state !== 'success'}
          className="w-full py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:bg-slate-900 disabled:text-slate-600 text-white font-medium rounded-lg text-xs transition duration-200 flex justify-center items-center gap-2"
        >
          {state === 'idle' || state === 'error' || state === 'success' ? (
            <>
              <Send className="w-3.5 h-3.5" />
              <span>Launch Ceremony Stream</span>
            </>
          ) : (
            <>
              <RefreshCw className="w-3.5 h-3.5 animate-spin" />
              <span>Processing...</span>
            </>
          )}
        </button>
      </div>

      {/* Ceremony Screen & Visual Player State Machine */}
      <div className="lg:col-span-7 flex flex-col justify-between bg-slate-950 border border-slate-900 rounded-xl p-6 relative overflow-hidden min-h-[360px]">
        
        {/* Background Ambient Aura based on state */}
        <div className={`absolute inset-0 opacity-10 pointer-events-none transition-all duration-700 ${
          state === 'prompt' ? 'bg-indigo-500' :
          state === 'success' ? 'bg-emerald-500' :
          state === 'error' ? 'bg-rose-500' : 'bg-transparent'
        }`} />

        {/* Status indicator bar */}
        <div className="flex justify-between items-center border-b border-slate-900 pb-3 z-10">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-2xs font-mono text-slate-400">Ceremony Console</span>
          </div>

          <div className="text-3xs font-mono bg-slate-900 border border-slate-800 rounded px-2 py-0.5 text-slate-400 uppercase">
            Active: {activeCeremony.replace('_', ' ')}
          </div>
        </div>

        {/* Core Screen Space */}
        <div className="flex-1 flex flex-col items-center justify-center p-6 z-10 text-center relative">
          
          {/* STATE: IDLE */}
          {state === 'idle' && (
            <div className="space-y-4 max-w-sm">
              <div className="w-16 h-16 rounded-full border border-slate-800 bg-slate-900/60 flex items-center justify-center mx-auto text-slate-500">
                <Fingerprint className="w-8 h-8" />
              </div>
              <div>
                <h4 className="text-xs font-semibold text-slate-200">Device Ready to Initiate</h4>
                <p className="text-3xs text-slate-500 mt-1 leading-relaxed">
                  Configure your device biometric profile on the left, then click "Launch Ceremony Stream" to start the cryptographic exchange.
                </p>
              </div>
            </div>
          )}

          {/* STATE: INITIALIZING */}
          {state === 'initializing' && (
            <div className="space-y-4">
              <RefreshCw className="w-8 h-8 text-indigo-400 animate-spin mx-auto" />
              <div>
                <h4 className="text-xs font-semibold text-slate-300">Initializing Session Context...</h4>
                <p className="text-3xs text-slate-500">Generating cryptographic nonce and challenge contract.</p>
              </div>
            </div>
          )}

          {/* STATE: READY */}
          {state === 'ready' && (
            <div className="space-y-4">
              <div className="w-3 h-3 rounded-full bg-indigo-500 animate-ping mx-auto" />
              <div>
                <h4 className="text-xs font-semibold text-slate-200">Handoff Acknowledged</h4>
                <p className="text-3xs text-slate-500">Preparing system-owned hardware prompt modal...</p>
              </div>
            </div>
          )}

          {/* STATE: PROMPT (SIMULATING OS PROMPT MODAL) */}
          {state === 'prompt' && (
            <div className="bg-slate-900/90 border border-slate-800 rounded-2xl p-6 shadow-xl max-w-xs w-full space-y-4 mx-auto animate-fade-in relative">
              <div className="absolute top-2.5 right-3 text-3xs font-mono text-slate-600">
                System Prompt
              </div>

              <div className="w-12 h-12 rounded-full border border-indigo-800/80 bg-indigo-950/20 flex items-center justify-center mx-auto animate-pulse">
                <Fingerprint className="w-6 h-6 text-indigo-400" />
              </div>

              <div className="space-y-1">
                <h5 className="text-xs font-bold text-slate-200">Verify Your Identity</h5>
                <p className="text-3xs text-slate-400 leading-normal">
                  {activeCeremony === 'step_up' 
                    ? `Confirm payment of $${transactionAmount.toLocaleString()} to Enterprise Corp.` 
                    : "Touch the physical fingerprint sensor or complete face unlock to continue."}
                </p>
              </div>

              {/* Action Buttons mimicking standard Chrome/Safari system WebAuthn sheet */}
              <div className="flex flex-col gap-1.5 text-3xs font-mono pt-2 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => handleOSPromptOutcome(true)}
                  className="w-full py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg transition"
                >
                  [Simulate Touch / Verification Success]
                </button>
                <button
                  type="button"
                  onClick={() => {
                    if (uvType === 'cancelled') handleOSPromptOutcome(false, 'cancelled');
                    else if (uvType === 'lockout') handleOSPromptOutcome(false, 'lockout');
                    else if (uvType === 'unavailable') handleOSPromptOutcome(false, 'sensor_unavailable');
                    else if (uvType === 'unsupported') handleOSPromptOutcome(false, 'unsupported_environment');
                    else handleOSPromptOutcome(false, 'cancelled'); // Default to Cancelled
                  }}
                  className="w-full py-1.5 bg-slate-950 hover:bg-slate-800 text-slate-400 rounded-lg transition"
                >
                  Cancel / Reject Prompt
                </button>
              </div>
            </div>
          )}

          {/* STATE: SUBMITTING */}
          {state === 'submitting' && (
            <div className="space-y-4">
              <RefreshCw className="w-8 h-8 text-sky-400 animate-spin mx-auto" />
              <div>
                <h4 className="text-xs font-semibold text-slate-300">Evaluating Verification Evidence...</h4>
                <p className="text-3xs text-slate-500">Transmitting signed challenge and computing AMR mappings.</p>
              </div>
            </div>
          )}

          {/* STATE: SUCCESS */}
          {state === 'success' && (
            <div className="space-y-4 max-w-sm animate-scale-up">
              <div className="w-12 h-12 rounded-full bg-emerald-950/40 border border-emerald-900/60 flex items-center justify-center mx-auto text-emerald-400">
                <CheckCircle className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-emerald-400">Ceremony Authenticated Successfully</h4>
                <p className="text-3xs text-slate-400 mt-2 leading-relaxed font-mono">
                  {outcome}
                </p>
                <div className="mt-4 flex justify-center gap-2">
                  <button 
                    onClick={resetCeremony}
                    className="px-3 py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-3xs font-medium text-slate-300 rounded transition"
                  >
                    Reset Console
                  </button>
                </div>
              </div>
            </div>
          )}

          {/* STATE: ERROR */}
          {state === 'error' && (
            <div className="space-y-4 max-w-sm">
              <div className="w-12 h-12 rounded-full bg-rose-950/40 border border-rose-900/60 flex items-center justify-center mx-auto text-rose-400">
                <AlertCircle className="w-6 h-6" />
              </div>
              <div>
                <h4 className="text-xs font-bold text-rose-400">Ceremony Handshake Blocked</h4>
                <p className="text-3xs text-slate-400 mt-2 leading-relaxed">
                  {outcome}
                </p>
                <div className="mt-4 flex justify-center gap-2">
                  <button 
                    onClick={resetCeremony}
                    className="px-3 py-1 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-3xs font-medium text-slate-300 rounded transition"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </div>
          )}

        </div>

        {/* Progress Bar (at the bottom) */}
        <div className="w-full bg-slate-900 h-1 rounded-full overflow-hidden z-10 mt-auto">
          <div 
            className="h-full bg-indigo-500 transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      </div>
    </div>
  );
}
