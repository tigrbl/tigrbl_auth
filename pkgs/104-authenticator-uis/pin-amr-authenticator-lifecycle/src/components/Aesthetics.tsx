import React from 'react';
import { ShieldCheck, Info, RefreshCw, Key, HelpCircle, HardDrive, Smartphone, Sparkles, ArrowRight } from 'lucide-react';
import { AMRMode } from '../types';

// ==========================================
// CompatibilityNotice
// ==========================================
export function CompatibilityNotice() {
  return (
    <div className="flex items-center gap-2 px-3 py-1.5 rounded-full bg-slate-900/80 border border-slate-800 text-[10px] text-slate-400 font-mono tracking-wider w-fit mx-auto shadow-sm">
      <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping" />
      <span>FIDO2 / WEBAUTHN COMPLIANT ADAPTER</span>
    </div>
  );
}

// ==========================================
// AuthenticationContextSummary
// ==========================================
interface AuthenticationContextSummaryProps {
  purpose: string;
  payloadAmount?: string;
  origin?: string;
  amrMode: AMRMode;
}

export function AuthenticationContextSummary({
  purpose,
  payloadAmount,
  origin = 'https://tigrbl.secure.internal',
  amrMode,
}: AuthenticationContextSummaryProps) {
  return (
    <div className="bg-slate-950/80 border border-slate-800 p-4 rounded-xl text-left space-y-2.5 shadow-sm">
      <div className="flex justify-between items-center text-[10px] font-mono text-slate-500 uppercase tracking-widest border-b border-slate-900 pb-2">
        <span>SECURITY BOUNDARY CONTEXT</span>
        <span className="text-blue-400 font-bold">MODE: {amrMode.toUpperCase()}</span>
      </div>

      <div className="grid grid-cols-2 gap-y-2 text-xs font-mono text-slate-400">
        <div>
          <span className="text-slate-600 block text-[9px] uppercase tracking-wider">Origin URL</span>
          <span className="text-slate-300 font-medium break-all">{origin}</span>
        </div>
        <div>
          <span className="text-slate-600 block text-[9px] uppercase tracking-wider">Purpose Class</span>
          <span className="text-yellow-400 font-semibold">{purpose}</span>
        </div>
        {payloadAmount && (
          <div className="col-span-2 border-t border-slate-900 pt-2 flex justify-between items-center">
            <span className="text-slate-500 text-[9px] uppercase tracking-wider">Transaction Value</span>
            <span className="text-emerald-400 font-bold font-sans text-sm">{payloadAmount}</span>
          </div>
        )}
      </div>
    </div>
  );
}

// ==========================================
// EvidenceFreshnessBadge
// ==========================================
interface EvidenceFreshnessBadgeProps {
  timestamp: string;
  trusted: boolean;
}

export function EvidenceFreshnessBadge({ timestamp, trusted }: EvidenceFreshnessBadgeProps) {
  return (
    <div className={`flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[11px] font-mono border ${
      trusted 
        ? 'bg-emerald-950/30 border-emerald-900/50 text-emerald-400' 
        : 'bg-amber-950/20 border-amber-900/40 text-amber-400'
    }`}>
      <span className={`h-1.5 w-1.5 rounded-full ${trusted ? 'bg-emerald-500 animate-pulse' : 'bg-amber-500'}`} />
      <span>FRESHNESS: Just verified ({new Date(timestamp).toLocaleTimeString()})</span>
    </div>
  );
}

// ==========================================
// MethodSwitchMenu
// ==========================================
interface MethodSwitchMenuProps {
  currentMode: AMRMode;
  onModeChange: (mode: AMRMode) => void;
  allowedModes?: AMRMode[];
}

export function MethodSwitchMenu({ currentMode, onModeChange, allowedModes = ['first-party', 'device-local', 'authenticator-pin', 'trusted-upstream'] }: MethodSwitchMenuProps) {
  const modes: { id: AMRMode; label: string; icon: React.ReactNode; desc: string }[] = [
    {
      id: 'first-party',
      label: 'First-Party Account PIN',
      icon: <ShieldCheck size={16} />,
      desc: 'TIGRBL-owned secure database credential.',
    },
    {
      id: 'device-local',
      label: 'OS/Platform Unlock',
      icon: <Smartphone size={16} />,
      desc: 'Device-local FaceID/TouchID or system PIN.',
    },
    {
      id: 'authenticator-pin',
      label: 'Security Key / Card PIN',
      icon: <Key size={16} />,
      desc: 'External FIDO2 key or PIV smart card.',
    },
    {
      id: 'trusted-upstream',
      label: 'Trusted Upstream PIN',
      icon: <RefreshCw size={16} />,
      desc: 'Federated identity provider verifier evidence.',
    }
  ];

  return (
    <div className="space-y-2">
      <label className="text-[10px] font-bold text-slate-500 uppercase tracking-widest block text-center">
        AUTHENTICATION METHOD REFERENCE (AMR) MODES
      </label>
      <div className="grid grid-cols-2 gap-2">
        {modes.map((m) => {
          const isAllowed = allowedModes.includes(m.id);
          const isSelected = currentMode === m.id;
          return (
            <button
              key={m.id}
              type="button"
              disabled={!isAllowed}
              onClick={() => onModeChange(m.id)}
              className={`p-3 rounded-xl border text-left flex flex-col space-y-1 transition-all ${
                isSelected
                  ? 'bg-blue-950/40 border-blue-500 text-blue-200 ring-1 ring-blue-500/20'
                  : isAllowed
                    ? 'bg-slate-900/60 border-slate-800 text-slate-400 hover:bg-slate-800/80 cursor-pointer'
                    : 'bg-slate-950/40 border-slate-900/80 text-slate-600 cursor-not-allowed opacity-50'
              }`}
            >
              <div className="flex items-center gap-1.5 font-bold text-xs">
                {m.icon}
                <span>{m.label}</span>
              </div>
              <p className="text-[10px] text-slate-500 font-sans leading-relaxed">{m.desc}</p>
            </button>
          );
        })}
      </div>
    </div>
  );
}

// ==========================================
// ExternalPinGuidance
// ==========================================
export function ExternalPinGuidance({ type }: { type: 'passkey' | 'roaming-key' | 'smart-card' | 'native-biometric' }) {
  const steps = {
    'passkey': [
      'Your browser will launch a native system dialog.',
      'Authenticate with Windows Hello, Apple TouchID, or Android unlock.',
      'The raw PIN/biometric is NOT disclosed to this application.'
    ],
    'roaming-key': [
      'Insert your security key (e.g., YubiKey) into a USB port.',
      'Touch the flashing metal contact on your hardware key.',
      'If prompted by the operating system, type your Security Key PIN.',
      'Your PIN remains safely inside the secure hardware enclave.'
    ],
    'smart-card': [
      'Insert your PIV smart card into the external card reader.',
      'The OS middleware will present a prompt requesting your smart card PIN.',
      'Verify that the green status light on your reader is flashing.'
    ],
    'native-biometric': [
      'Position your finger or look directly into your camera/scanner.',
      'The native device security daemon will verify your biometric pattern.',
      'Only a signed cryptographic credential challenge returns to the app.'
    ]
  };

  const currentSteps = steps[type] || steps['roaming-key'];

  return (
    <div className="bg-slate-900/40 border border-slate-800/60 p-4 rounded-xl text-left space-y-3">
      <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-slate-300">
        <HardDrive size={14} className="text-cyan-400 animate-pulse" />
        SECURE HARDWARE HANDOFF DIRECTIVES
      </div>
      <ol className="space-y-2">
        {currentSteps.map((step, i) => (
          <li key={i} className="flex gap-2.5 text-[11px] leading-relaxed text-slate-400">
            <span className="font-mono text-cyan-400 font-bold bg-slate-950/80 h-5 w-5 rounded-full flex items-center justify-center border border-slate-800 shrink-0">
              {i + 1}
            </span>
            <span className="pt-0.5">{step}</span>
          </li>
        ))}
      </ol>
      <div className="bg-slate-950/60 p-2.5 rounded-lg border border-slate-900 text-[10px] text-slate-500 leading-normal font-mono">
        🛡️ <span className="text-slate-400">SECURE PARADIGM:</span> This application does NOT collect or proxy your external key/card PIN. We receive only standard WebAuthn signature proofs.
      </div>
    </div>
  );
}

// ==========================================
// DeviceBlockedHelp
// ==========================================
export function DeviceBlockedHelp() {
  return (
    <div className="bg-red-950/20 border border-red-900/30 p-4 rounded-xl text-left space-y-3.5">
      <div className="flex items-center gap-2 text-xs font-bold uppercase tracking-wider text-red-400">
        <HelpCircle size={15} />
        EXTERNAL HARDWARE BLOCKED / LOCKED OUT
      </div>
      <p className="text-xs text-red-300/80 leading-relaxed">
        The connected hardware authenticator or operating system credential store has been locked due to excessive invalid PIN attempts.
      </p>
      <div className="space-y-2 text-xs text-slate-400">
        <p className="font-semibold text-slate-300 uppercase tracking-wide text-[10px]">How to recover:</p>
        <ul className="list-disc list-inside space-y-1 text-[11px]">
          <li>Use your device manufacturer's companion application (e.g., Yubico Authenticator).</li>
          <li>Insert the hardware key, select PIN settings, and use the PUK (PIN Unlock Key) if configured.</li>
          <li>For OS Hello/Passkeys, use your cloud account recovery or wait for the system cooling-off lock timer.</li>
        </ul>
      </div>
    </div>
  );
}
