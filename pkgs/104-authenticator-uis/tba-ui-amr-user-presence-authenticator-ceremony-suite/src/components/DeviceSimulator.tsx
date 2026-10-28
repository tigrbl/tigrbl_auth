/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { CeremonyState, Authenticator } from '../types';
import { Shield, Fingerprint, Usb, Wifi, Laptop, KeyRound, AlertTriangle, CheckCircle, Smartphone } from 'lucide-react';

interface DeviceSimulatorProps {
  activeAuthenticator: Authenticator | null;
  activeState: CeremonyState;
  onTouch: (presenceSuccess: boolean, uvSuccess: boolean, pinValue?: string) => void;
  onTriggerError: (errorState: CeremonyState) => void;
  isPinRequired: boolean;
  isKeyInserted: boolean;
  onInsertToggle: () => void;
  onNfcTap: () => void;
  ceremonyPurpose: string;
}

export default function DeviceSimulator({
  activeAuthenticator,
  activeState,
  onTouch,
  onTriggerError,
  isPinRequired,
  isKeyInserted,
  onNfcTap,
  onInsertToggle,
  ceremonyPurpose,
}: DeviceSimulatorProps) {
  const [pin, setPin] = useState('');
  const [pinError, setPinError] = useState('');

  const handleTouchSensor = () => {
    if (isPinRequired && !pin) {
      setPinError('PIN is required for User Verification (UV) policy.');
      return;
    }
    setPinError('');
    onTouch(true, isPinRequired ? true : (activeAuthenticator?.uvSupported || false), pin);
  };

  const getTransportIcon = (auth: Authenticator) => {
    switch (auth.transport) {
      case 'internal': return <Laptop className="w-5 h-5 text-zinc-500" />;
      case 'usb': return <Usb className="w-5 h-5 text-indigo-500" />;
      case 'nfc': return <Wifi className="w-5 h-5 text-emerald-500 animate-pulse" />;
      case 'ble': return <Wifi className="w-5 h-5 text-blue-500" />;
    }
  };

  const isInteractionPending = [
    CeremonyState.AWAITING_DEVICE,
    CeremonyState.INSERT_GUIDANCE,
    CeremonyState.TOUCH_GUIDANCE,
    CeremonyState.PROCESSING
  ].includes(activeState);

  return (
    <div className="bg-zinc-50 border border-zinc-200/80 rounded-2xl p-5 flex flex-col justify-between h-full shadow-sm">
      {/* Simulator Header */}
      <div>
        <div className="flex items-center justify-between mb-4">
          <div className="flex items-center gap-2">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-ping" />
            <h3 className="font-display font-medium text-sm text-zinc-800 tracking-tight">
              Physical Ceremony Simulator
            </h3>
          </div>
          <span className="font-mono text-[10px] px-2 py-0.5 bg-zinc-200/60 rounded-full text-zinc-600">
            Hardware Emulator v1.1
          </span>
        </div>

        {/* Device Canvas */}
        <div className="border border-dashed border-zinc-300 rounded-xl bg-white p-6 flex flex-col items-center justify-center min-h-[220px] relative overflow-hidden">
          {activeAuthenticator ? (
            <div className="w-full flex flex-col items-center text-center animate-fade-in">
              {/* Device Visual Representation */}
              {activeAuthenticator.type === 'passkey' && activeAuthenticator.transport === 'internal' && (
                <div className="flex flex-col items-center">
                  <div className="relative w-28 h-20 bg-zinc-800 rounded-lg p-2 flex flex-col justify-between shadow-lg border border-zinc-700">
                    <div className="w-full h-1 bg-zinc-600 rounded-full mx-auto" />
                    <div className="flex justify-center items-center h-10">
                      <Fingerprint className={`w-8 h-8 ${isInteractionPending ? 'text-indigo-400 animate-pulse glow-pulse' : 'text-zinc-600'}`} />
                    </div>
                    <div className="w-5 h-5 rounded-full bg-zinc-700/60 border border-zinc-600 mx-auto" />
                  </div>
                  <span className="font-mono text-xs text-zinc-500 mt-3">Platform Touch ID / FaceID</span>
                </div>
              )}

              {activeAuthenticator.type === 'security_key' && activeAuthenticator.transport === 'usb' && (
                <div className="flex flex-col items-center">
                  <div className="flex items-center gap-1">
                    {/* USB Port Slot */}
                    <div className="w-6 h-8 bg-zinc-300 rounded-l flex items-center justify-center border-y border-l border-zinc-400">
                      <Usb className="w-3.5 h-3.5 text-zinc-600" />
                    </div>
                    {/* YubiKey Body */}
                    <div className={`w-28 h-12 ${isKeyInserted ? 'bg-zinc-900' : 'bg-zinc-700/50 border-dashed'} rounded-r-lg relative flex items-center justify-between px-3 shadow-md border border-zinc-800 transition-all duration-300`}>
                      <span className="text-[10px] text-zinc-500 font-mono font-bold">FIDO2</span>
                      {/* Capacitive Touch Sensor */}
                      <button
                        onClick={handleTouchSensor}
                        disabled={!isKeyInserted || !isInteractionPending}
                        className={`w-6 h-6 rounded-full border flex items-center justify-center transition-all ${
                          isKeyInserted && isInteractionPending
                            ? 'bg-amber-400 border-amber-300 hover:scale-110 cursor-pointer animate-pulse shadow-md shadow-amber-400/50'
                            : 'bg-zinc-800 border-zinc-700 text-zinc-600 cursor-not-allowed'
                        }`}
                        title="Capacitive Presence Sensor"
                      >
                        <div className="w-2 h-2 rounded-full bg-zinc-900" />
                      </button>
                    </div>
                  </div>
                  <div className="flex gap-2 mt-3 items-center">
                    <span className="font-mono text-xs text-zinc-500">USB Key State:</span>
                    <button
                      onClick={onInsertToggle}
                      className={`text-[10px] font-medium px-2 py-0.5 rounded-full border transition-colors ${
                        isKeyInserted
                          ? 'bg-indigo-50 border-indigo-200 text-indigo-700'
                          : 'bg-amber-50 border-amber-200 text-amber-700 animate-bounce'
                      }`}
                    >
                      {isKeyInserted ? 'Disconnect USB Key' : 'Insert USB Key'}
                    </button>
                  </div>
                </div>
              )}

              {activeAuthenticator.type === 'security_key' && activeAuthenticator.transport === 'nfc' && (
                <div className="flex flex-col items-center">
                  <div className="relative w-20 h-32 bg-indigo-900 text-white rounded-xl p-3 flex flex-col justify-between shadow-xl border border-indigo-800">
                    <div className="flex justify-between items-center">
                      <Wifi className="w-4 h-4 text-indigo-300 rotate-90" />
                      <span className="font-mono text-[8px] tracking-widest text-indigo-300">NFC</span>
                    </div>
                    <div className="flex justify-center my-2">
                      <div className="w-8 h-8 rounded-full bg-indigo-800/80 border border-indigo-700 flex items-center justify-center">
                        <KeyRound className="w-4 h-4 text-white" />
                      </div>
                    </div>
                    <div className="text-center">
                      <div className="w-full h-1 bg-amber-400 rounded-full mb-1 animate-pulse" />
                      <span className="font-mono text-[8px] text-zinc-400">ROAMING TOKEN</span>
                    </div>
                  </div>
                  <button
                    onClick={onNfcTap}
                    disabled={!isInteractionPending}
                    className={`mt-3 text-[10px] font-medium px-2 py-0.5 rounded-full border transition-colors ${
                      isInteractionPending
                        ? 'bg-emerald-50 border-emerald-200 text-emerald-700 animate-pulse cursor-pointer hover:bg-emerald-100'
                        : 'bg-zinc-100 border-zinc-200 text-zinc-400 cursor-not-allowed'
                    }`}
                  >
                    Tap Key to NFC Reader
                  </button>
                </div>
              )}

              {activeAuthenticator.type === 'managed_key' && (
                <div className="flex flex-col items-center">
                  <div className="relative w-32 h-14 bg-zinc-900 border-2 border-indigo-500 rounded-xl flex items-center justify-between px-3 shadow-xl">
                    <div className="flex flex-col text-left">
                      <span className="font-mono text-[8px] text-zinc-500">MANAGED HW</span>
                      <span className="font-mono text-[10px] font-bold text-white tracking-tight">FEITIAN PRO</span>
                    </div>
                    {/* Dual presence/touch indicator */}
                    <button
                      onClick={handleTouchSensor}
                      disabled={!isKeyInserted || !isInteractionPending}
                      className={`w-6 h-6 rounded-full border flex items-center justify-center transition-all ${
                        isKeyInserted && isInteractionPending
                          ? 'bg-emerald-400 border-emerald-300 hover:scale-110 cursor-pointer animate-pulse'
                          : 'bg-zinc-800 border-zinc-700 text-zinc-600 cursor-not-allowed'
                      }`}
                    >
                      <Fingerprint className="w-3.5 h-3.5 text-zinc-950" />
                    </button>
                  </div>
                  <div className="flex gap-2 mt-3 items-center">
                    <span className="font-mono text-xs text-zinc-500">Managed Connection:</span>
                    <button
                      onClick={onInsertToggle}
                      className={`text-[10px] font-medium px-2 py-0.5 rounded-full border transition-colors ${
                        isKeyInserted ? 'bg-indigo-50 border-indigo-200 text-indigo-700' : 'bg-zinc-100 border-zinc-200 text-zinc-600'
                      }`}
                    >
                      {isKeyInserted ? 'Disconnect Key' : 'Connect Key'}
                    </button>
                  </div>
                </div>
              )}

              {/* Ceremony Detail / Instructions */}
              <div className="mt-4 p-2 bg-zinc-50 rounded-lg w-full border border-zinc-100">
                <span className="font-sans text-[11px] font-medium text-zinc-700 block">
                  Purpose: <span className="font-mono text-indigo-600">{ceremonyPurpose || 'General Auth'}</span>
                </span>
                <span className="font-sans text-[11px] text-zinc-500 mt-1 block">
                  {activeState === CeremonyState.AWAITING_DEVICE && 'Waiting for device initialization...'}
                  {activeState === CeremonyState.INSERT_GUIDANCE && 'Please insert or connect your security token.'}
                  {activeState === CeremonyState.TOUCH_GUIDANCE && 'Touch the capacitive golden sensor or trigger biometric read.'}
                  {activeState === CeremonyState.PROCESSING && 'Processing cryptographic signature...'}
                  {activeState === CeremonyState.SUCCESS && 'Ceremony completed successfully! Flag UP set.'}
                </span>
              </div>
            </div>
          ) : (
            <div className="text-center p-4">
              <Shield className="w-8 h-8 text-zinc-400 mx-auto mb-2" />
              <p className="font-sans text-xs text-zinc-500">
                No active ceremony. Initiating an enrollment or authentication workflow will wake the device simulator.
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Simulator Actions / Inject Error Cases */}
      <div className="mt-4 border-t border-zinc-200/60 pt-4">
        <h4 className="font-display font-medium text-xs text-zinc-700 mb-2.5 flex items-center gap-1.5">
          <AlertTriangle className="w-3.5 h-3.5 text-amber-500" />
          Inject Client/Device Failure States
        </h4>
        <div className="grid grid-cols-2 gap-1.5">
          <button
            onClick={() => onTriggerError(CeremonyState.PRESENCE_ABSENT)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>Presence Absent (UP=0)</span>
          </button>
          <button
            onClick={() => onTriggerError(CeremonyState.CANCELLED)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>User Cancelled</span>
          </button>
          <button
            onClick={() => onTriggerError(CeremonyState.TIMEOUT)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>Device Timeout</span>
          </button>
          <button
            onClick={() => onTriggerError(CeremonyState.DEVICE_REMOVED)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>Device Removed</span>
          </button>
          <button
            onClick={() => onTriggerError(CeremonyState.TRANSPORT_UNAVAILABLE)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>Transport Fault</span>
          </button>
          <button
            onClick={() => onTriggerError(CeremonyState.REPLAY_DETECTED)}
            disabled={!isInteractionPending}
            className="text-[10px] text-left bg-white border border-zinc-200 hover:bg-zinc-50 text-zinc-700 py-1.5 px-2.5 rounded-lg font-mono flex items-center justify-between disabled:opacity-50 disabled:hover:bg-white"
          >
            <span>Replay Signature</span>
          </button>
        </div>

        {/* User Verification Pin Entry */}
        {isPinRequired && activeAuthenticator && (
          <div className="mt-4 p-3 bg-indigo-50 border border-indigo-100 rounded-xl animate-fade-in">
            <span className="font-sans text-[11px] font-medium text-indigo-950 flex items-center gap-1.5 mb-1.5">
              <KeyRound className="w-3.5 h-3.5 text-indigo-600" />
              User Verification Required (PIN)
            </span>
            <div className="flex gap-2">
              <input
                type="password"
                placeholder="Enter authenticator PIN"
                value={pin}
                onChange={(e) => {
                  setPin(e.target.value);
                  if (e.target.value) setPinError('');
                }}
                disabled={!isInteractionPending}
                className="bg-white border border-indigo-200 text-xs rounded-lg px-2 py-1 flex-1 font-mono focus:outline-none focus:border-indigo-400 focus:ring-1 focus:ring-indigo-400"
              />
              <button
                onClick={handleTouchSensor}
                disabled={!isInteractionPending}
                className="bg-indigo-600 hover:bg-indigo-700 text-white font-sans text-xs px-3 py-1 rounded-lg transition-colors font-medium disabled:opacity-50"
              >
                Submit PIN
              </button>
            </div>
            {pinError && <span className="text-[10px] text-red-600 mt-1 block font-sans">{pinError}</span>}
          </div>
        )}
      </div>
    </div>
  );
}
