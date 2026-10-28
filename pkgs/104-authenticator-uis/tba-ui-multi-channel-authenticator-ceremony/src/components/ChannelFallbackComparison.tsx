import React from 'react';
import { AuthenticatorMethod, Policy } from '../types';
import { ShieldCheck, ShieldAlert, ArrowRight, HelpCircle } from 'lucide-react';

interface FallbackProps {
  policy: Policy;
  selectedMethods: AuthenticatorMethod[];
}

export const ChannelFallbackComparison: React.FC<FallbackProps> = ({ policy, selectedMethods }) => {
  const getMethodAesthetic = (method: AuthenticatorMethod) => {
    switch (method) {
      case 'passkey':
        return { name: 'Hardware Passkey (WebAuthn)', level: 'High Assurance', color: 'text-sky-400 border-sky-500/20 bg-sky-500/5' };
      case 'smartcard':
        return { name: 'Smart Card (FIV/PIV)', level: 'High Assurance', color: 'text-indigo-400 border-indigo-500/20 bg-indigo-500/5' };
      case 'totp':
        return { name: 'Software TOTP (RFC 6238)', level: 'Medium Assurance', color: 'text-purple-400 border-purple-500/20 bg-purple-500/5' };
      case 'push':
        return { name: 'OOB Push (Native Device)', level: 'Medium-High Assurance', color: 'text-fuchsia-400 border-fuchsia-500/20 bg-fuchsia-500/5' };
      case 'email':
        return { name: 'Email Magic OTP', level: 'Low Assurance', color: 'text-amber-400 border-amber-500/20 bg-amber-500/5' };
      case 'sms':
        return { name: 'SMS Cellular OTP', level: 'Low Assurance (SIM-Swap risk)', color: 'text-rose-400 border-rose-500/20 bg-rose-500/5' };
      case 'voice':
        return { name: 'Voice Telephone Ring', level: 'Low Assurance', color: 'text-orange-400 border-orange-500/20 bg-orange-500/5' };
    }
  };

  const isIndependenceCompromised = () => {
    // Check if the selected methods are SMS and Voice (both belong to the same Telecom network channel)
    const active = selectedMethods.filter((m) => m !== null);
    if (active.includes('sms') && active.includes('voice')) {
      return true;
    }
    return false;
  };

  return (
    <div className="bg-zinc-950/40 rounded-xl border border-zinc-800 p-4 space-y-3.5" id="fallback-comparison">
      <div className="flex items-center gap-2 border-b border-zinc-900 pb-2.5">
        <ShieldCheck className="h-4 w-4 text-emerald-400" />
        <h4 className="font-semibold text-zinc-100 text-sm">Policy Assurance & Fallback Analyzer</h4>
      </div>

      <div className="space-y-3">
        {/* Status indicator */}
        {isIndependenceCompromised() ? (
          <div className="rounded-lg bg-rose-500/10 border border-rose-500/25 p-3 flex gap-2.5 items-start">
            <ShieldAlert className="h-4.5 w-4.5 text-rose-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <h5 className="text-xs font-semibold text-rose-300">Channel Independence Compromised</h5>
              <p className="text-[11px] text-rose-400/90 leading-relaxed">
                Combining <strong>SMS OTP</strong> and <strong>Voice Verification</strong> relies entirely on the same telecom carrier cellular channel. A single carrier compromise or SIM swap will intercept both tokens.
              </p>
            </div>
          </div>
        ) : (
          <div className="rounded-lg bg-emerald-500/5 border border-emerald-500/15 p-3 flex gap-2.5 items-start">
            <ShieldCheck className="h-4.5 w-4.5 text-emerald-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <h5 className="text-xs font-semibold text-emerald-300">Policy Constraints Satisfied</h5>
              <p className="text-[11px] text-emerald-400/80 leading-relaxed">
                All selected channels operate across strictly disjoint boundaries (e.g., local cryptographic hardware mixed with remote cellular or mail relays).
              </p>
            </div>
          </div>
        )}

        {/* Method list */}
        <div className="space-y-2">
          <span className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
            Current Combination Evaluation:
          </span>
          <div className="grid grid-cols-1 gap-2">
            {selectedMethods.map((m, idx) => {
              if (!m) return null;
              const meta = getMethodAesthetic(m);
              return (
                <div
                  key={m + idx}
                  className={`flex items-center justify-between border rounded-lg p-2.5 ${meta.color}`}
                >
                  <div className="flex items-center gap-2">
                    <span className="text-2xs font-mono bg-zinc-950 px-1.5 py-0.5 text-zinc-400 rounded-md border border-zinc-800">
                      Step {idx + 1}
                    </span>
                    <span className="text-xs font-medium">{meta.name}</span>
                  </div>
                  <span className="text-[10px] font-mono tracking-wider opacity-80 uppercase">
                    {meta.level}
                  </span>
                </div>
              );
            })}
          </div>
        </div>

        {/* Fallback settings brief */}
        <div className="border-t border-zinc-900 pt-2.5 flex items-start gap-2 text-[11px] text-zinc-400 leading-relaxed font-mono">
          <HelpCircle className="h-3.5 w-3.5 text-zinc-500 shrink-0 mt-0.5" />
          <div className="space-y-0.5">
            <span>Fallback Eligibility: {policy.allowFallback ? 'Enabled' : 'Disabled'}</span>
            <span className="block text-[10px] text-zinc-500">
              {policy.allowFallback
                ? `Authorized backup sequence: ${policy.fallbackCombination.join(' → ').toUpperCase()}`
                : 'Security policy strictly forbids credential substitution.'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};
