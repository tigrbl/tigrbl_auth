/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Authenticator, CeremonyState, PresencePolicy, CeremonyEvidence, AuditLog } from '../types';
import { Key, ShieldAlert, CheckCircle, ShieldAlert as AlertTriangle, RefreshCw, KeyRound, ArrowRight, CornerDownRight, Landmark, Eye, Info, HelpCircle } from 'lucide-react';

interface PasskeyPromptProps {
  authenticators: Authenticator[];
  policies: PresencePolicy[];
  activeState: CeremonyState;
  onInitiateCeremony: (auth: Authenticator, policy: PresencePolicy, purpose: string) => void;
  onResetCeremony: () => void;
  evidenceResult: CeremonyEvidence | null;
  policySatisfied: boolean;
  onFallbackUsed: () => void;
  activePolicy: PresencePolicy;
  selectedAuth: Authenticator | null;
  errorMessage: string;
}

export default function PasskeyPrompt({
  authenticators,
  policies,
  activeState,
  onInitiateCeremony,
  onResetCeremony,
  evidenceResult,
  policySatisfied,
  onFallbackUsed,
  activePolicy,
  selectedAuth,
  errorMessage,
}: PasskeyPromptProps) {
  const [chosenAuthId, setChosenAuthId] = useState(authenticators[0]?.id || '');
  const [chosenPolicyId, setChosenPolicyId] = useState(policies[0]?.id || '');
  const [transactionPurpose, setTransactionPurpose] = useState('Authorize corporate account portal session');

  const currentSelectedAuth = authenticators.find(a => a.id === chosenAuthId) || authenticators[0];
  const currentSelectedPolicy = policies.find(p => p.id === chosenPolicyId) || policies[0];

  const handleStart = () => {
    if (currentSelectedAuth && currentSelectedPolicy) {
      onInitiateCeremony(currentSelectedAuth, currentSelectedPolicy, transactionPurpose);
    }
  };

  const getStatusBannerColor = () => {
    switch (activeState) {
      case CeremonyState.SUCCESS:
        return 'bg-emerald-50 border-emerald-200 text-emerald-950';
      case CeremonyState.PROCESSING:
        return 'bg-indigo-50 border-indigo-100 text-indigo-950';
      case CeremonyState.AWAITING_DEVICE:
      case CeremonyState.INSERT_GUIDANCE:
      case CeremonyState.TOUCH_GUIDANCE:
        return 'bg-amber-50 border-amber-200 text-amber-950 animate-pulse';
      case CeremonyState.IDLE:
        return 'bg-zinc-50 border-zinc-200 text-zinc-950';
      default:
        return 'bg-red-50 border-red-200 text-red-950';
    }
  };

  return (
    <div className="space-y-6">
      {/* Configuration Phase */}
      {activeState === CeremonyState.IDLE && (
        <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="font-display font-medium text-zinc-900 text-sm flex items-center gap-2">
            <Key className="w-4 h-4 text-indigo-600" />
            1. Configure Assertion Request Parameters
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Authenticator Choice */}
            <div className="space-y-1.5">
              <label className="font-sans text-xs font-semibold text-zinc-700 block">
                Select Authenticator Key
              </label>
              <select
                value={chosenAuthId}
                onChange={(e) => setChosenAuthId(e.target.value)}
                className="w-full bg-zinc-50 border border-zinc-200 hover:border-zinc-300 rounded-lg px-3 py-2 text-xs font-sans text-zinc-800 focus:outline-none focus:border-indigo-500"
              >
                {authenticators.map((auth) => (
                  <option key={auth.id} value={auth.id}>
                    {auth.name} ({auth.transport.toUpperCase()} · {auth.type === 'managed_key' ? 'Managed' : 'Passkey'})
                  </option>
                ))}
              </select>
              <span className="font-sans text-[10px] text-zinc-400 block">
                Each authenticator offers distinct evidence configurations (UP vs. UV capabilities).
              </span>
            </div>

            {/* Policy Enforcement */}
            <div className="space-y-1.5">
              <label className="font-sans text-xs font-semibold text-zinc-700 block">
                Active Verification Policy
              </label>
              <select
                value={chosenPolicyId}
                onChange={(e) => setChosenPolicyId(e.target.value)}
                className="w-full bg-zinc-50 border border-zinc-200 hover:border-zinc-300 rounded-lg px-3 py-2 text-xs font-sans text-zinc-800 focus:outline-none focus:border-indigo-500"
              >
                {policies.map((p) => (
                  <option key={p.id} value={p.id}>
                    {p.name} {p.uvRequired ? '(Requires PIN/Bio)' : '(Presence Only)'}
                  </option>
                ))}
              </select>
              <span className="font-sans text-[10px] text-zinc-400 block">
                Determines if simple User Presence (UP) is sufficient, or if User Verification (UV) is demanded.
              </span>
            </div>
          </div>

          {/* Transaction Purpose */}
          <div className="space-y-1.5">
            <label className="font-sans text-xs font-semibold text-zinc-700 block">
              Transaction Purpose / Challenge Context
            </label>
            <input
              type="text"
              value={transactionPurpose}
              onChange={(e) => setTransactionPurpose(e.target.value)}
              className="w-full bg-zinc-50 border border-zinc-200 hover:border-zinc-300 rounded-lg px-3 py-2 text-xs font-sans text-zinc-800 focus:outline-none focus:border-indigo-500"
              placeholder="e.g. Authenticate administrative root access"
            />
            <span className="font-sans text-[10px] text-zinc-500 block">
              The purpose is bound into the cryptographic client data block, preventing phishing or relay attacks.
            </span>
          </div>

          {/* Step-up Chooser / Warnings */}
          {currentSelectedPolicy && currentSelectedAuth && (
            <div className="p-3.5 rounded-xl border bg-zinc-50/50 text-xs">
              <div className="flex gap-2 items-start">
                <Info className="w-4 h-4 text-indigo-500 shrink-0 mt-0.5" />
                <div className="space-y-1">
                  <span className="font-sans font-semibold text-zinc-800">Policy Pre-check Evaluation:</span>
                  <p className="font-sans text-zinc-500 leading-relaxed">
                    You have chosen <strong className="text-zinc-700">{currentSelectedAuth.name}</strong> under policy <strong className="text-zinc-700">{currentSelectedPolicy.name}</strong>.
                  </p>
                  {currentSelectedPolicy.uvRequired && !currentSelectedAuth.uvSupported ? (
                    <div className="text-red-700 bg-red-50 border border-red-100 p-2 rounded-md mt-1.5 font-sans font-medium flex items-center gap-1.5">
                      <ShieldAlert className="w-3.5 h-3.5 text-red-600" />
                      Warning: Chosen key does not support User Verification (UV), which this policy mandates. Step-up choice or alternate factor will be required.
                    </div>
                  ) : (
                    <div className="text-emerald-700 bg-emerald-50 border border-emerald-100 p-2 rounded-md mt-1.5 font-sans font-medium flex items-center gap-1.5">
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                      Capabilities Satisfied: This authenticator matches the required verification profile.
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Action Button */}
          <button
            onClick={handleStart}
            className="w-full bg-zinc-900 hover:bg-zinc-800 text-white font-sans text-xs font-semibold py-2.5 px-4 rounded-xl transition-all shadow-md flex items-center justify-center gap-1.5"
          >
            Initiate User-Presence Ceremony
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Ceremony Active Phases */}
      {activeState !== CeremonyState.IDLE && (
        <div className={`border rounded-xl p-5 shadow-sm transition-all duration-300 ${getStatusBannerColor()}`}>
          <div className="flex items-start justify-between">
            <div className="space-y-1">
              <span className="font-mono text-[10px] uppercase font-bold tracking-wider text-indigo-600">
                ACTIVE AUTHENTICATION CEREMONY
              </span>
              <h3 className="font-display font-medium text-zinc-950 text-base">
                {selectedAuth?.name} Verification Gate
              </h3>
            </div>
            <button
              onClick={onResetCeremony}
              className="p-1.5 bg-white border border-zinc-200 hover:bg-zinc-50 rounded-lg text-zinc-600 transition-colors"
              title="Reset Ceremony"
            >
              <RefreshCw className="w-3.5 h-3.5" />
            </button>
          </div>

          {/* Core Interactive Ceremony Stage */}
          <div className="mt-4 bg-white border border-zinc-200 rounded-xl p-5 text-zinc-800 space-y-4">
            <div className="flex items-center gap-3">
              <div className="p-2.5 bg-indigo-50 text-indigo-700 rounded-lg">
                <KeyRound className="w-5 h-5" />
              </div>
              <div>
                <span className="font-sans text-[11px] text-zinc-500 block">Ceremony Binding Target</span>
                <span className="font-sans text-xs font-bold text-zinc-800">{transactionPurpose}</span>
              </div>
            </div>

            {/* Custom guidance text per transport */}
            <div className="p-3.5 bg-zinc-50 border border-zinc-100 rounded-lg space-y-2">
              <span className="font-sans text-xs font-semibold text-zinc-700 block">
                User Guidance Directions
              </span>
              <p className="font-sans text-xs text-zinc-600 leading-relaxed">
                {activeState === CeremonyState.AWAITING_DEVICE && (
                  'Browser handoff completed. Waking your security token or hardware key...'
                )}
                {activeState === CeremonyState.INSERT_GUIDANCE && (
                  'Your security key needs to be plugged in. Please connect it to your USB-C or Lightning port.'
                )}
                {activeState === CeremonyState.TOUCH_GUIDANCE && (
                  selectedAuth?.transport === 'usb'
                    ? 'Touch the flashing gold sensor circle on your physical USB key now.'
                    : 'Place your finger on the laptop Touch ID pad or follow device authentication prompts.'
                )}
                {activeState === CeremonyState.PROCESSING && (
                  'Cryptographic confirmation received. Conducting signature audit & nonce check...'
                )}
                {activeState === CeremonyState.SUCCESS && (
                  'Cryptographic handshake validated. User Presence is certified and established!'
                )}
                {activeState === CeremonyState.PRESENCE_ABSENT && (
                  'Error: Device touch sensor was not tapped. User presence was absent during this ceremony.'
                )}
                {activeState === CeremonyState.CANCELLED && (
                  'Error: Browser/OS prompt cancelled by user. The physical handoff was interrupted.'
                )}
                {activeState === CeremonyState.TIMEOUT && (
                  'Error: The device timed out waiting for touch. Please try again with shorter reaction latency.'
                )}
                {activeState === CeremonyState.DEVICE_REMOVED && (
                  'Error: Hardware key was disconnected during cryptographic negotiation.'
                )}
                {activeState === CeremonyState.TRANSPORT_UNAVAILABLE && (
                  'Error: Communication with key failed. Check USB or NFC connection.'
                )}
                {activeState === CeremonyState.REPLAY_DETECTED && (
                  'CRITICAL ERROR: Cryptographic counter mismatch. Replay signature attempt detected!'
                )}
              </p>
            </div>

            {/* Troubleshooting & Fallbacks */}
            {activeState !== CeremonyState.SUCCESS && activeState !== CeremonyState.PROCESSING && (
              <div className="flex gap-2 justify-end border-t border-zinc-100 pt-3">
                <button
                  onClick={onFallbackUsed}
                  className="bg-zinc-100 hover:bg-zinc-200 text-zinc-700 font-sans text-xs px-3 py-1.5 rounded-lg transition-colors font-medium"
                >
                  Fallback to Secondary Method
                </button>
                <button
                  onClick={handleStart}
                  className="bg-indigo-600 hover:bg-indigo-700 text-white font-sans text-xs px-3 py-1.5 rounded-lg transition-colors font-medium"
                >
                  Retry Ceremony
                </button>
              </div>
            )}
          </div>

          {/* Diagnostic Evidence Details (Visual Sheet) */}
          {evidenceResult && (
            <div className="mt-5 bg-zinc-900 text-zinc-100 border border-zinc-800 rounded-xl p-4 space-y-3 font-mono text-[11px] animate-fade-in">
              <div className="flex items-center justify-between border-b border-zinc-800 pb-2">
                <span className="text-zinc-400 font-sans font-bold text-xs flex items-center gap-1.5">
                  <span className="w-1.5 h-1.5 rounded-full bg-indigo-400" />
                  Verified Assertion Ceremony Evidence (UP/UV)
                </span>
                <span className="font-mono text-[10px] text-zinc-500 bg-zinc-800 px-2 py-0.5 rounded">
                  {evidenceResult.auditReference}
                </span>
              </div>

              <div className="grid grid-cols-2 gap-y-2 gap-x-4 border-b border-zinc-800/50 pb-3">
                <div>
                  <span className="text-zinc-500 block">PRESENCE EVIDENCE</span>
                  <span className={`text-[12px] font-bold ${evidenceResult.userPresent ? 'text-emerald-400' : 'text-red-400'}`}>
                    {evidenceResult.userPresent ? 'UP = true (USER_PRESENT)' : 'UP = false (USER_ABSENT)'}
                  </span>
                </div>
                <div>
                  <span className="text-zinc-500 block">USER VERIFICATION</span>
                  <span className={`text-[12px] font-bold ${evidenceResult.userVerified ? 'text-indigo-400' : 'text-zinc-400'}`}>
                    {evidenceResult.userVerified ? 'UV = true (USER_VERIFIED)' : 'UV = false (PRESENCE_ONLY)'}
                  </span>
                </div>
              </div>

              <div className="space-y-1 bg-zinc-950 p-2.5 rounded-lg border border-zinc-800">
                <div className="flex justify-between">
                  <span className="text-zinc-500">Device Model:</span>
                  <span className="text-zinc-300">{evidenceResult.authenticatorName}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">AAGUID Profile:</span>
                  <span className="text-zinc-300">{selectedAuth?.aaguid}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">Challenge Bound:</span>
                  <span className="text-indigo-300 truncate max-w-[200px]" title={evidenceResult.clientDataHash}>
                    {evidenceResult.clientDataHash.substring(0, 24)}...
                  </span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">Modality:</span>
                  <span className="text-zinc-300 uppercase">{evidenceResult.modality}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-zinc-500">Sign Counter:</span>
                  <span className="text-zinc-300">{evidenceResult.counter}</span>
                </div>
              </div>

              <div className="p-2.5 bg-zinc-950/60 rounded-lg flex items-start gap-2 border border-zinc-800/80">
                <Landmark className="w-4 h-4 text-zinc-500 shrink-0 mt-0.5" />
                <div className="space-y-0.5">
                  <span className="text-zinc-400 font-sans font-medium text-[10px] block">
                    Policy Satisfaction Outcome:
                  </span>
                  <span className={`font-sans font-bold block ${policySatisfied ? 'text-emerald-400' : 'text-red-400'}`}>
                    {policySatisfied
                      ? 'PASSED - All corporate rules satisfied.'
                      : 'WARNING: UV is missing. Policy demands User Verification.'}
                  </span>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
