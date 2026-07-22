import React from 'react';
import { PolicyConfig } from '../types';
import { Shield, CheckCircle, XCircle, AlertTriangle, Play, HelpCircle } from 'lucide-react';

interface PolicyEditorProps {
  policy: PolicyConfig;
  onChangePolicy: (updated: PolicyConfig) => void;
  issuers: string[];
}

export default function PolicyEditor({ policy, onChangePolicy, issuers }: PolicyEditorProps) {
  // Preset simulation scenarios for testing the rules instantly
  const testScenarios = [
    {
      name: "Absent Evidence",
      description: "User is not logged in or has zero security evidence.",
      evidence: { hasAmrs: false, detectedAmrs: [], provider: "", age: 0, isTrusted: false }
    },
    {
      name: "Generic WebAuthn UV Only",
      description: "User verified via face/PIN/fingerprint on standard WebAuthn. (uv=true but no proof of fingerprint)",
      evidence: { hasAmrs: true, detectedAmrs: ["hw", "user", "uv"], provider: "WebAuthn Chrome RP", age: 10, isTrusted: false }
    },
    {
      name: "Verified Trusted Fingerprint",
      description: "Trusted Native iOS Platform Agent certifies fingerprint use (fpt AMR exists & trusted).",
      evidence: { hasAmrs: true, detectedAmrs: ["hw", "user", "uv", "fpt"], provider: "iOS Platform Agent v2", age: 5, isTrusted: true }
    },
    {
      name: "Stale Fingerprint Assertion",
      description: "Trusted fingerprint evidence exists but age (300 sec) exceeds maximum limit.",
      evidence: { hasAmrs: true, detectedAmrs: ["hw", "user", "uv", "fpt"], provider: "Android Biometric SDK", age: 300, isTrusted: true }
    },
    {
      name: "Conflicting / Untrusted Claim",
      description: "An untrusted external provider claims fingerprint verification but isn't on the allowed list.",
      evidence: { hasAmrs: true, detectedAmrs: ["hw", "user", "uv", "fpt"], provider: "Untrusted Outpost IdP", age: 2, isTrusted: false }
    }
  ];

  const [activeScenario, setActiveScenario] = React.useState<typeof testScenarios[0]>(testScenarios[1]);

  const evaluateScenario = (sc: typeof testScenarios[0]) => {
    if (!sc.evidence.hasAmrs) {
      return {
        status: 'REJECTED' as const,
        reason: "No authentication credentials or evidence detected in session context.",
        remediation: "Direct user to complete initial passkey or provider ceremony."
      };
    }

    const hasFpt = sc.evidence.detectedAmrs.includes('fpt');
    const isIssuerAllowed = policy.allowedIssuers.includes(sc.evidence.provider);
    const isFresh = sc.evidence.age <= policy.maxAgeSeconds;

    if (policy.requireFingerprint) {
      if (!hasFpt) {
        return {
          status: 'REJECTED_FALLBACK' as const,
          reason: "Fingerprint AMR (fpt) is strictly required by policy, but session contains only generic User Verification (UV).",
          remediation: `Trigger fallback method: [${policy.fallbackMethod.toUpperCase()}] or complete biometric step-up.`
        };
      }

      if (!isIssuerAllowed && sc.evidence.isTrusted === false) {
        return {
          status: 'REJECTED' as const,
          reason: `Evidence provider [${sc.evidence.provider}] is not registered as a trusted fingerprint verifier.`,
          remediation: "Tenant administrator must explicitly configure provider transform profile."
        };
      }

      if (!isFresh) {
        return {
          status: 'REJECTED_FALLBACK' as const,
          reason: `Verified Fingerprint AMR age (${sc.evidence.age}s) exceeds the strict policy limit of ${policy.maxAgeSeconds}s.`,
          remediation: `Force re-authentication (fresh prompt) or fallback to [${policy.fallbackMethod.toUpperCase()}].`
        };
      }

      return {
        status: 'APPROVED' as const,
        reason: "Valid, trusted, and fresh fingerprint evidence (fpt) matches all policy conditions.",
        remediation: "Grant access to highly secure scope immediately."
      };
    } else {
      // Policy doesn't strictly require fingerprint, any generic UV is accepted
      const hasUv = sc.evidence.detectedAmrs.includes('uv') || sc.evidence.detectedAmrs.includes('user');
      if (!hasUv) {
        return {
          status: 'REJECTED' as const,
          reason: "Session lacks active user verification or presence confirmation.",
          remediation: "Require standard passwordless prompt."
        };
      }

      if (!isFresh) {
        return {
          status: 'REJECTED_FALLBACK' as const,
          reason: `Verification age (${sc.evidence.age}s) is older than allowed window.`,
          remediation: `Trigger fallback or re-auth.`
        };
      }

      return {
        status: 'APPROVED' as const,
        reason: "Policy allows general passwordless verification; generic WebAuthn UV satisfies condition.",
        remediation: "Grant access."
      };
    }
  };

  const currentResult = evaluateScenario(activeScenario);

  const toggleIssuer = (iss: string) => {
    const list = [...policy.allowedIssuers];
    if (list.includes(iss)) {
      onChangePolicy({ ...policy, allowedIssuers: list.filter(x => x !== iss) });
    } else {
      onChangePolicy({ ...policy, allowedIssuers: [...list, iss] });
    }
  };

  return (
    <div className="space-y-6" id="policy-editor-panel">
      <div>
        <h2 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
          <Shield className="text-violet-400 w-5 h-5" />
          Evidence Policy Administrator
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Enforce biometric specific rules, maximum session tolerances, and secondary recovery routing.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Policy Editor Controls */}
        <div className="lg:col-span-7 bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-5">
          <h3 className="font-semibold text-slate-200 text-sm border-b border-slate-900 pb-2 mb-2">
            Active Governance Rules
          </h3>

          {/* Toggle Rule */}
          <div className="space-y-2">
            <div className="flex items-center justify-between">
              <div>
                <label className="text-sm font-medium text-slate-200 block">Strict Fingerprint AMR Constraint</label>
                <span className="text-xs text-slate-500">
                  Reject generic user verification (such as face ID, PIN, or pattern) if "fpt" evidence is missing.
                </span>
              </div>
              <button 
                onClick={() => onChangePolicy({ ...policy, requireFingerprint: !policy.requireFingerprint })}
                className={`w-12 h-6 flex items-center rounded-full p-1 transition-all duration-300 ${
                  policy.requireFingerprint ? 'bg-indigo-600 justify-end' : 'bg-slate-800 justify-start'
                }`}
              >
                <div className="bg-white w-4 h-4 rounded-full shadow-md" />
              </button>
            </div>
          </div>

          {/* Slider for Freshness */}
          <div className="space-y-2 pt-3 border-t border-slate-900">
            <div className="flex justify-between items-center">
              <div>
                <label className="text-sm font-medium text-slate-200 block">Maximum Evidence Age (Seconds)</label>
                <span className="text-xs text-slate-500">
                  Maximum elapsed seconds since physical sensor touch was performed on the device.
                </span>
              </div>
              <span className="bg-indigo-950/40 text-indigo-400 px-3 py-1 rounded font-mono text-xs border border-indigo-900/50">
                {policy.maxAgeSeconds}s
              </span>
            </div>
            <input 
              type="range" 
              min={10} 
              max={600} 
              step={10}
              className="w-full accent-indigo-500 bg-slate-800 rounded-lg cursor-pointer"
              value={policy.maxAgeSeconds}
              onChange={(e) => onChangePolicy({ ...policy, maxAgeSeconds: parseInt(e.target.value) })}
            />
          </div>

          {/* Trusted Fingerprint Issuers */}
          <div className="space-y-2 pt-3 border-t border-slate-900">
            <label className="text-sm font-medium text-slate-200 block">Trusted Evidence Providers</label>
            <span className="text-xs text-slate-500 block mb-2">
              Select which native enclaves and transformed federated identity providers satisfy fingerprint assurance.
            </span>
            
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 text-xs">
              {issuers.map((iss) => {
                const isChecked = policy.allowedIssuers.includes(iss);
                return (
                  <label 
                    key={iss} 
                    className={`flex items-center gap-2.5 p-2 rounded-lg border cursor-pointer transition ${
                      isChecked 
                        ? 'bg-indigo-950/20 border-indigo-800/80 text-indigo-200' 
                        : 'bg-slate-900/60 border-slate-800/60 text-slate-400 hover:border-slate-700'
                    }`}
                  >
                    <input 
                      type="checkbox" 
                      checked={isChecked} 
                      onChange={() => toggleIssuer(iss)}
                      className="rounded border-slate-800 text-indigo-600 focus:ring-0" 
                    />
                    <span className="font-mono truncate">{iss}</span>
                  </label>
                );
              })}
            </div>
          </div>

          {/* Rescue Fallback Method */}
          <div className="space-y-2 pt-3 border-t border-slate-900">
            <label className="text-sm font-medium text-slate-200 block">Rescue Fallback Policy</label>
            <span className="text-xs text-slate-500 block">
              Routing fallback when fingerprint evidence fails verification constraints or the sensor is locked out.
            </span>
            
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 text-xs">
              {['pin', 'security_key', 'mfa_redirect', 'fail_closed'].map((method) => (
                <button
                  key={method}
                  type="button"
                  onClick={() => onChangePolicy({ ...policy, fallbackMethod: method as any })}
                  className={`py-2 px-3 rounded-lg border text-center transition font-medium capitalize ${
                    policy.fallbackMethod === method
                      ? 'bg-violet-950/30 border-violet-800 text-violet-200'
                      : 'bg-slate-900/60 border-slate-800 text-slate-400 hover:border-slate-700'
                  }`}
                >
                  {method.replace('_', ' ')}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* Live Simulation Sandbox & Impact Preview */}
        <div className="lg:col-span-5 flex flex-col gap-4">
          {/* Scenarios Selector */}
          <div className="bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-3">
            <h3 className="font-semibold text-slate-200 text-sm flex items-center gap-1.5">
              <Play className="text-indigo-400 w-4 h-4" />
              Policy Sandbox Scenarios
            </h3>
            <p className="text-xs text-slate-400">
              Select an active token assertion payload state to run through the current validation rules:
            </p>

            <div className="space-y-1.5" id="sandbox-scenarios">
              {testScenarios.map((sc) => {
                const isSelected = activeScenario.name === sc.name;
                return (
                  <button
                    key={sc.name}
                    onClick={() => setActiveScenario(sc)}
                    className={`w-full text-left p-2.5 rounded-lg border text-xs transition duration-150 flex flex-col gap-1 ${
                      isSelected 
                        ? 'bg-slate-900 border-indigo-700 text-slate-100' 
                        : 'bg-slate-900/40 border-slate-850 text-slate-400 hover:bg-slate-900/80 hover:border-slate-800'
                    }`}
                  >
                    <span className="font-semibold text-slate-200">{sc.name}</span>
                    <span className="text-2xs text-slate-500 line-clamp-1">{sc.description}</span>
                  </button>
                );
              })}
            </div>
          </div>

          {/* Sandbox Evaluation Output */}
          <div className="bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4 flex-1">
            <div className="flex justify-between items-center border-b border-slate-900 pb-2">
              <span className="text-2xs text-slate-500 uppercase tracking-widest font-mono">Policy Sandbox Output</span>
              
              {currentResult.status === 'APPROVED' && (
                <span className="bg-emerald-950/50 border border-emerald-900 text-emerald-400 text-2xs font-semibold uppercase px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <CheckCircle className="w-3.5 h-3.5" /> Approved
                </span>
              )}
              {currentResult.status === 'REJECTED' && (
                <span className="bg-rose-950/50 border border-rose-900 text-rose-400 text-2xs font-semibold uppercase px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <XCircle className="w-3.5 h-3.5" /> Rejected
                </span>
              )}
              {currentResult.status === 'REJECTED_FALLBACK' && (
                <span className="bg-amber-950/50 border border-amber-900 text-amber-400 text-2xs font-semibold uppercase px-2.5 py-0.5 rounded-full flex items-center gap-1">
                  <AlertTriangle className="w-3.5 h-3.5" /> Fallback Routed
                </span>
              )}
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div>
                <span className="text-slate-500 block text-2xs uppercase font-sans">Active Test Input:</span>
                <span className="text-slate-200 font-sans font-semibold">{activeScenario.name}</span>
              </div>

              <div>
                <span className="text-slate-500 block text-2xs uppercase font-sans">Extracted AMRs:</span>
                <span className="text-slate-300">
                  {activeScenario.evidence.detectedAmrs.length > 0 
                    ? `[${activeScenario.evidence.detectedAmrs.join(', ')}]` 
                    : 'None (Unauthenticated)'}
                </span>
              </div>

              <div>
                <span className="text-slate-500 block text-2xs uppercase font-sans">Claim Source:</span>
                <span className="text-slate-300">{activeScenario.evidence.provider || "N/A"}</span>
              </div>

              <div>
                <span className="text-slate-500 block text-2xs uppercase font-sans">Asserted Age / Freshness Limit:</span>
                <span className="text-slate-300">
                  {activeScenario.evidence.hasAmrs ? `${activeScenario.evidence.age} seconds / max ${policy.maxAgeSeconds} seconds` : 'N/A'}
                </span>
              </div>

              <div className="bg-slate-900/80 p-3 rounded-lg border border-slate-850 space-y-1.5 font-sans">
                <span className="text-2xs text-slate-500 block uppercase font-mono">Evaluation details:</span>
                <p className="text-xs text-slate-200 font-medium leading-relaxed">{currentResult.reason}</p>
                <div className="text-2xs text-indigo-400 font-semibold mt-1">
                  💡 Action Required: {currentResult.remediation}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
