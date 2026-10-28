import React from 'react';
import { Check, X, ShieldAlert } from 'lucide-react';
import { FirstPartyPolicy } from '../types';
import { checkDisallowedPatterns } from '../mockServer';

interface PinRequirementsProps {
  pin: string;
  policy: FirstPartyPolicy;
}

export function PinRequirements({ pin, policy }: PinRequirementsProps) {
  const isMinLength = pin.length >= policy.minLength;
  const isMaxLength = pin.length <= policy.maxLength;
  const isNumericOnly = !policy.allowAlpha ? /^\d*$/.test(pin) : true;
  
  // Check common bad patterns
  const isNotCommon = !policy.disallowedPatterns.includes(pin);
  const isNotSequentialAsc = !/^(012345|123456|234567|345678|456789|567890)/.test(pin);
  const isNotSequentialDesc = !/^(987654|876543|765432|654321|543210)/.test(pin);
  const isNotRepeating = !/^(\d)\1{5,}$/.test(pin) || pin.length < 6;

  const requirements = [
    {
      label: `Length: ${policy.minLength} to ${policy.maxLength} digits`,
      satisfied: isMinLength && isMaxLength && pin.length > 0,
      checked: pin.length > 0,
    },
    {
      label: 'Only numeric digits (0-9)',
      satisfied: isNumericOnly,
      checked: pin.length > 0,
    },
    {
      label: 'No simple repeating digits (e.g. 111111)',
      satisfied: isNotRepeating,
      checked: pin.length >= 6,
    },
    {
      label: 'No simple sequential runs (e.g. 123456 or 654321)',
      satisfied: isNotSequentialAsc && isNotSequentialDesc,
      checked: pin.length >= 6,
    },
    {
      label: 'Not in blocklisted common patterns list',
      satisfied: isNotCommon,
      checked: pin.length > 0,
    }
  ];

  const errors = checkDisallowedPatterns(pin, policy);

  return (
    <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 space-y-3">
      <div className="flex items-center gap-1.5 text-xs font-semibold uppercase tracking-wider text-slate-400">
        <ShieldAlert size={14} className="text-amber-500 animate-pulse" />
        CRYPTOGRAPHIC SECURITY POLICY RULES
      </div>

      <ul className="space-y-2">
        {requirements.map((req, idx) => (
          <li key={idx} className="flex items-start gap-2 text-xs">
            {req.checked ? (
              req.satisfied ? (
                <Check size={14} className="text-emerald-400 mt-0.5 shrink-0" />
              ) : (
                <X size={14} className="text-red-400 mt-0.5 shrink-0" />
              )
            ) : (
              <div className="h-3.5 w-3.5 rounded-full border border-slate-700 mt-0.5 shrink-0" />
            )}
            <span className={req.checked && !req.satisfied ? 'text-red-300 font-medium' : req.satisfied ? 'text-emerald-300' : 'text-slate-400'}>
              {req.label}
            </span>
          </li>
        ))}
      </ul>

      {pin.length > 0 && errors && (
        <div className="bg-red-950/20 text-red-400 text-[11px] p-2 rounded-lg border border-red-900/40 mt-2 font-mono">
          <span className="font-bold">POLICY ERROR:</span> {errors}
        </div>
      )}
    </div>
  );
}
