/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Authenticator, AuthenticatorType, TransportType, CeremonyState } from '../types';
import { PlusCircle, Trash2, Fingerprint, Usb, Wifi, Laptop, HelpCircle, Key, CheckCircle, Info, Clipboard } from 'lucide-react';

interface EnrollmentCeremonyProps {
  authenticators: Authenticator[];
  onEnrollKey: (newAuth: Authenticator) => void;
  onRemoveKey: (id: string) => void;
  activeState: CeremonyState;
  onStartEnrollCeremony: (auth: Authenticator) => void;
}

export default function EnrollmentCeremony({
  authenticators,
  onEnrollKey,
  onRemoveKey,
  activeState,
  onStartEnrollCeremony,
}: EnrollmentCeremonyProps) {
  const [keyName, setKeyName] = useState('');
  const [keyType, setKeyType] = useState<AuthenticatorType>('passkey');
  const [keyTransport, setKeyTransport] = useState<TransportType>('internal');
  const [upSupported, setUpSupported] = useState(true);
  const [uvSupported, setUvSupported] = useState(true);
  const [hardwareBacked, setHardwareBacked] = useState(true);

  const [currentStep, setCurrentStep] = useState<'form' | 'ceremony' | 'success'>('form');
  const [pendingKey, setPendingKey] = useState<Authenticator | null>(null);

  const getTransportIcon = (transport: TransportType) => {
    switch (transport) {
      case 'internal': return <Laptop className="w-4 h-4 text-zinc-500" />;
      case 'usb': return <Usb className="w-4 h-4 text-indigo-500" />;
      case 'nfc': return <Wifi className="w-4 h-4 text-emerald-500" />;
      case 'ble': return <Wifi className="w-4 h-4 text-blue-500" />;
    }
  };

  const handleStartEnrollment = () => {
    if (!keyName.trim()) return;

    // Generate random AAGUID or use standardized ones
    const randAaguid = keyType === 'passkey' 
      ? '0263f120-e2b5-4b0d-b4f0-bc370cd60efc' 
      : keyType === 'managed_key' 
      ? '7f348e02-45a8-4441-bc19-10aa1982a17f' 
      : 'cb69481e-8e17-4dd3-97f9-2e0085a6cfbc';

    const newKey: Authenticator = {
      id: `auth-${Date.now()}`,
      name: keyName,
      type: keyType,
      transport: keyTransport,
      upSupported,
      uvSupported: keyType === 'managed_key' ? false : uvSupported, // Managed keys are often strict UP
      hardwareBacked,
      aaguid: randAaguid,
      createdAt: new Date().toISOString(),
      lastUsedAt: null,
      signatureCount: 0,
    };

    setPendingKey(newKey);
    setCurrentStep('ceremony');
    onStartEnrollCeremony(newKey);
  };

  const completeEnrollment = () => {
    if (pendingKey) {
      onEnrollKey(pendingKey);
      setCurrentStep('success');
    }
  };

  const handleReset = () => {
    setKeyName('');
    setPendingKey(null);
    setCurrentStep('form');
  };

  return (
    <div className="space-y-6">
      {/* Introduction Banner explaining UP vs UV */}
      <div className="p-4 bg-indigo-50 border border-indigo-100 rounded-xl space-y-2">
        <h4 className="font-display font-medium text-xs text-indigo-950 flex items-center gap-1.5">
          <Info className="w-4 h-4 text-indigo-600" />
          Understanding User Presence (UP) vs User Verification (UV)
        </h4>
        <p className="font-sans text-xs text-indigo-900/90 leading-relaxed">
          Enrollment registers an underlying FIDO2 credential. However, <strong className="text-indigo-950">User Presence is a dynamic, ceremony-level flag</strong>. Just because an authenticator supports biometrics does not mean a login is automatically "verified". True user presence is proven solely when the physical handoff/ceremony returns a certified hardware interaction signature.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-5">
        {/* Main Enrollment Actions (Left side) */}
        <div className="lg:col-span-7 bg-white border border-zinc-200 rounded-xl p-5 shadow-sm">
          {currentStep === 'form' && (
            <div className="space-y-4">
              <h3 className="font-display font-medium text-zinc-900 text-sm flex items-center gap-1.5">
                <PlusCircle className="w-4 h-4 text-indigo-600" />
                Register New Authenticator Key
              </h3>

              <div className="space-y-3">
                <div className="space-y-1.5">
                  <label className="font-sans text-xs font-semibold text-zinc-700 block">
                    Friendly Key Name / Label
                  </label>
                  <input
                    type="text"
                    value={keyName}
                    onChange={(e) => setKeyName(e.target.value)}
                    className="w-full bg-zinc-50 border border-zinc-200 hover:border-zinc-300 rounded-lg px-3 py-2 text-xs font-sans text-zinc-800 focus:outline-none focus:border-indigo-500"
                    placeholder="e.g. Blue YubiKey Backup, Laptop TouchID"
                  />
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div className="space-y-1.5">
                    <label className="font-sans text-xs font-semibold text-zinc-700 block">
                      Authenticator Type
                    </label>
                    <select
                      value={keyType}
                      onChange={(e) => setKeyType(e.target.value as AuthenticatorType)}
                      className="w-full bg-zinc-50 border border-zinc-200 rounded-lg px-3 py-1.5 text-xs font-sans text-zinc-800 focus:outline-none"
                    >
                      <option value="passkey">Passkey (Platform)</option>
                      <option value="security_key">FIDO2 Security Key</option>
                      <option value="managed_key">Managed Hardware Key</option>
                    </select>
                  </div>

                  <div className="space-y-1.5">
                    <label className="font-sans text-xs font-semibold text-zinc-700 block">
                      Transport Modality
                    </label>
                    <select
                      value={keyTransport}
                      onChange={(e) => setKeyTransport(e.target.value as TransportType)}
                      className="w-full bg-zinc-50 border border-zinc-200 rounded-lg px-3 py-1.5 text-xs font-sans text-zinc-800 focus:outline-none"
                    >
                      <option value="internal">Internal (Platform)</option>
                      <option value="usb">USB (Type A/C)</option>
                      <option value="nfc">NFC (Contactless)</option>
                      <option value="ble">Bluetooth (BLE)</option>
                    </select>
                  </div>
                </div>

                <div className="p-3 bg-zinc-50 rounded-xl space-y-2 border border-zinc-100">
                  <span className="font-sans text-xs font-semibold text-zinc-700 block">
                    Supported Evidence Capabilities
                  </span>
                  <div className="grid grid-cols-2 gap-2 text-xs">
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={upSupported}
                        onChange={(e) => setUpSupported(e.target.checked)}
                        className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <span>User Presence (UP)</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={uvSupported}
                        onChange={(e) => setUvSupported(e.target.checked)}
                        disabled={keyType === 'managed_key'}
                        className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <span className={keyType === 'managed_key' ? 'text-zinc-400' : ''}>User Verification (UV)</span>
                    </label>
                    <label className="flex items-center gap-2 cursor-pointer col-span-2">
                      <input
                        type="checkbox"
                        checked={hardwareBacked}
                        onChange={(e) => setHardwareBacked(e.target.checked)}
                        className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500"
                      />
                      <span>Hardware Backed / Cryptographic Attestation</span>
                    </label>
                  </div>
                </div>
              </div>

              <button
                onClick={handleStartEnrollment}
                disabled={!keyName.trim()}
                className="w-full bg-zinc-900 hover:bg-zinc-800 text-white font-sans text-xs font-semibold py-2 px-4 rounded-xl transition-all disabled:opacity-50 flex items-center justify-center gap-1.5"
              >
                Launch Device Enrollment Handoff
              </button>
            </div>
          )}

          {currentStep === 'ceremony' && (
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-display font-medium text-zinc-900 text-sm">
                  Waiting for Enrollment Ceremony Interaction...
                </h3>
                <button
                  onClick={handleReset}
                  className="text-xs text-zinc-500 hover:text-zinc-800 underline font-sans"
                >
                  Cancel
                </button>
              </div>

              <div className="p-4 bg-amber-50 border border-amber-200 text-amber-900 rounded-xl space-y-2 animate-pulse">
                <span className="font-sans font-bold text-xs block">
                  ACTION REQUIRED ON SIMULATOR / OS PROMPT
                </span>
                <p className="font-sans text-xs">
                  To complete enrollment, the user must physically insert, touch, or authenticate the device on the right hand emulator screen.
                </p>
              </div>

              {activeState === CeremonyState.SUCCESS && (
                <div className="p-4 bg-emerald-50 border border-emerald-200 text-emerald-950 rounded-xl space-y-3 animate-fade-in">
                  <span className="font-sans font-bold text-xs block flex items-center gap-1.5 text-emerald-800">
                    <CheckCircle className="w-4 h-4 text-emerald-600" />
                    Device Attestation Handshake Verified!
                  </span>
                  <p className="font-sans text-xs leading-relaxed text-emerald-700">
                    The mock server successfully checked the registration payload. AAGUID attestation reports a genuine <strong className="text-emerald-900">{pendingKey?.name}</strong>.
                  </p>
                  <button
                    onClick={completeEnrollment}
                    className="w-full bg-emerald-700 hover:bg-emerald-800 text-white font-sans text-xs font-semibold py-2 px-4 rounded-lg transition-colors"
                  >
                    Complete Registration & Record Lifecycle
                  </button>
                </div>
              )}
            </div>
          )}

          {currentStep === 'success' && (
            <div className="space-y-4 text-center py-6">
              <div className="w-12 h-12 rounded-full bg-emerald-100 flex items-center justify-center mx-auto mb-2 text-emerald-600">
                <CheckCircle className="w-6 h-6" />
              </div>
              <h3 className="font-display font-medium text-zinc-900 text-sm">
                Key Registered Successfully
              </h3>
              <p className="font-sans text-xs text-zinc-500 max-w-sm mx-auto leading-relaxed">
                Your new authenticator is registered and active inside your user context lifecycle. It is now eligible for authentication assertions!
              </p>
              <button
                onClick={handleReset}
                className="bg-zinc-900 hover:bg-zinc-800 text-white font-sans text-xs font-semibold py-1.5 px-4 rounded-xl transition-all"
              >
                Register Another Key
              </button>
            </div>
          )}
        </div>

        {/* Existing Authenticators list (Right side) */}
        <div className="lg:col-span-5 bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
          <h3 className="font-display font-medium text-zinc-900 text-sm flex items-center gap-1.5">
            <Key className="w-4 h-4 text-indigo-600" />
            Registered Keys Lifecycle
          </h3>

          <div className="space-y-3 max-h-[320px] overflow-y-auto">
            {authenticators.map((auth) => (
              <div key={auth.id} className="p-3 bg-zinc-50 border border-zinc-200/60 rounded-xl space-y-2 flex flex-col justify-between">
                <div className="flex items-start justify-between">
                  <div className="flex items-center gap-2">
                    {getTransportIcon(auth.transport)}
                    <span className="font-sans text-xs font-bold text-zinc-800 truncate max-w-[140px]" title={auth.name}>
                      {auth.name}
                    </span>
                  </div>
                  <button
                    onClick={() => onRemoveKey(auth.id)}
                    className="p-1 hover:bg-red-50 text-zinc-400 hover:text-red-500 rounded transition-colors"
                    title="Revoke / Replacement Key"
                  >
                    <Trash2 className="w-3.5 h-3.5" />
                  </button>
                </div>

                <div className="grid grid-cols-2 gap-1 font-mono text-[10px] text-zinc-500 border-t border-zinc-100 pt-2">
                  <span className="truncate">Type: {auth.type}</span>
                  <span className="text-right">Signatures: {auth.signatureCount}</span>
                  <span className="col-span-2 truncate">AAGUID: {auth.aaguid}</span>
                  <span className="col-span-2 text-[9px] text-zinc-400">Created: {new Date(auth.createdAt).toLocaleDateString()}</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
