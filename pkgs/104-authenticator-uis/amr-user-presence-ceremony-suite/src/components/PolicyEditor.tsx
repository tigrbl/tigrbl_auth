/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { PresencePolicy, ManagedKeyProfile, TransportType } from '../types';
import { Shield, Settings, Sliders, ToggleLeft, ClipboardCheck, Lock, Eye, CheckCircle, Smartphone, AlertOctagon } from 'lucide-react';

interface PolicyEditorProps {
  policies: PresencePolicy[];
  managedProfiles: ManagedKeyProfile[];
  onUpdatePolicy: (policy: PresencePolicy) => void;
  onUpdateProfile: (profile: ManagedKeyProfile) => void;
}

export default function PolicyEditor({
  policies,
  managedProfiles,
  onUpdatePolicy,
  onUpdateProfile,
}: PolicyEditorProps) {
  const [selectedPolicyId, setSelectedPolicyId] = useState(policies[0]?.id || '');
  const [selectedProfileId, setSelectedProfileId] = useState(managedProfiles[0]?.id || '');

  const activePolicy = policies.find(p => p.id === selectedPolicyId) || policies[0];
  const activeProfile = managedProfiles.find(p => p.id === selectedProfileId) || managedProfiles[0];

  const handlePolicyChange = (field: keyof PresencePolicy, value: any) => {
    if (activePolicy) {
      onUpdatePolicy({
        ...activePolicy,
        [field]: value,
      });
    }
  };

  const handleProfileChange = (field: keyof ManagedKeyProfile, value: any) => {
    if (activeProfile) {
      onUpdateProfile({
        ...activeProfile,
        [field]: value,
      });
    }
  };

  const handleTransportToggle = (transport: TransportType) => {
    if (!activeProfile) return;
    const current = activeProfile.allowedTransports;
    const updated = current.includes(transport)
      ? current.filter(t => t !== transport)
      : [...current, transport];
    handleProfileChange('allowedTransports', updated);
  };

  return (
    <div className="space-y-6">
      {/* Intro Context */}
      <div className="p-4 bg-zinc-50 border border-zinc-200 rounded-xl space-y-1">
        <h4 className="font-display font-medium text-xs text-zinc-950 flex items-center gap-1.5">
          <Shield className="w-4 h-4 text-zinc-700" />
          Enterprise Presence & Verification Policy Manager (P2 Admin)
        </h4>
        <p className="font-sans text-xs text-zinc-500 leading-relaxed">
          Administer FIDO2 user-presence policies, set up mandatory hardware profiles, and configure contextual step-up parameters. Edits are immediately compiled and enforced on the active ceremony loop.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
        {/* Verification Policy Block */}
        <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-3">
            <h3 className="font-display font-medium text-zinc-900 text-sm flex items-center gap-1.5">
              <Sliders className="w-4 h-4 text-indigo-600" />
              Ceremony Verification Policy
            </h3>
            <select
              value={selectedPolicyId}
              onChange={(e) => setSelectedPolicyId(e.target.value)}
              className="bg-zinc-100 border border-zinc-200 rounded-lg text-xs px-2.5 py-1 font-sans text-zinc-800"
            >
              {policies.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          {activePolicy && (
            <div className="space-y-4 animate-fade-in">
              {/* Presence Required toggle */}
              <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-50 border border-zinc-100">
                <div className="space-y-0.5">
                  <span className="font-sans text-xs font-semibold text-zinc-800 block">Require User Presence (UP)</span>
                  <span className="font-sans text-[11px] text-zinc-500 block">Enforces touch-ceremony confirmation flag from the authenticator.</span>
                </div>
                <input
                  type="checkbox"
                  checked={activePolicy.presenceRequired}
                  onChange={(e) => handlePolicyChange('presenceRequired', e.target.checked)}
                  className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                />
              </div>

              {/* UV Required toggle */}
              <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-50 border border-zinc-100">
                <div className="space-y-0.5">
                  <span className="font-sans text-xs font-semibold text-zinc-800 block">Require User Verification (UV)</span>
                  <span className="font-sans text-[11px] text-zinc-500 block">Demands PIN or biometric confirmation (not just a physical touch).</span>
                </div>
                <input
                  type="checkbox"
                  checked={activePolicy.uvRequired}
                  onChange={(e) => handlePolicyChange('uvRequired', e.target.checked)}
                  className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                />
              </div>

              {/* Hardware backing enforcement */}
              <div className="flex items-center justify-between p-3 rounded-lg bg-zinc-50 border border-zinc-100">
                <div className="space-y-0.5">
                  <span className="font-sans text-xs font-semibold text-zinc-800 block">Cryptographic Hardware-Backing Mandate</span>
                  <span className="font-sans text-[11px] text-zinc-500 block">Blocks software/simulation keys. Requires hardware secure enclave.</span>
                </div>
                <input
                  type="checkbox"
                  checked={activePolicy.hardwareBacked}
                  onChange={(e) => handlePolicyChange('hardwareBacked', e.target.checked)}
                  className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500 w-4 h-4"
                />
              </div>

              {/* Max Age Freshness policy */}
              <div className="space-y-1.5 p-3 rounded-lg bg-zinc-50 border border-zinc-100">
                <div className="flex justify-between items-center">
                  <label className="font-sans text-xs font-semibold text-zinc-800">
                    Maximum Evidence Age (Freshness Gate)
                  </label>
                  <span className="font-mono text-xs font-bold text-indigo-600 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded">
                    {activePolicy.maxAuthAgeSeconds} seconds
                  </span>
                </div>
                <input
                  type="range"
                  min="60"
                  max="86400"
                  step="60"
                  value={activePolicy.maxAuthAgeSeconds}
                  onChange={(e) => handlePolicyChange('maxAuthAgeSeconds', parseInt(e.target.value))}
                  className="w-full accent-indigo-600 h-1 bg-zinc-200 rounded-lg cursor-pointer"
                />
                <span className="font-sans text-[10px] text-zinc-400 block mt-1">
                  Re-verifies physical presence if previous ceremony age exceeds this time threshold.
                </span>
              </div>
            </div>
          )}
        </div>

        {/* Corporate Managed-Key Profile Block */}
        <div className="bg-white border border-zinc-200 rounded-xl p-5 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-zinc-100 pb-3">
            <h3 className="font-display font-medium text-zinc-900 text-sm flex items-center gap-1.5">
              <Lock className="w-4 h-4 text-indigo-600" />
              Corporate Managed-Key Profiles
            </h3>
            <select
              value={selectedProfileId}
              onChange={(e) => setSelectedProfileId(e.target.value)}
              className="bg-zinc-100 border border-zinc-200 rounded-lg text-xs px-2.5 py-1 font-sans text-zinc-800"
            >
              {managedProfiles.map(p => (
                <option key={p.id} value={p.id}>{p.name}</option>
              ))}
            </select>
          </div>

          {activeProfile && (
            <div className="space-y-4 animate-fade-in">
              {/* Allowed Transports */}
              <div className="p-3.5 bg-zinc-50 border border-zinc-100 rounded-xl space-y-2">
                <span className="font-sans text-xs font-semibold text-zinc-800 block">
                  Allowed Physical Key Transports
                </span>
                <div className="grid grid-cols-2 gap-2 text-xs">
                  {['usb', 'nfc', 'ble', 'internal'].map((transport) => {
                    const isChecked = activeProfile.allowedTransports.includes(transport as TransportType);
                    return (
                      <label key={transport} className="flex items-center gap-2 cursor-pointer">
                        <input
                          type="checkbox"
                          checked={isChecked}
                          onChange={() => handleTransportToggle(transport as TransportType)}
                          className="rounded border-zinc-300 text-indigo-600 focus:ring-indigo-500"
                        />
                        <span className="capitalize">{transport}</span>
                      </label>
                    );
                  })}
                </div>
              </div>

              {/* Strict AAGUID Registry checks */}
              <div className="p-3.5 bg-zinc-50 border border-zinc-100 rounded-xl space-y-2">
                <span className="font-sans text-xs font-semibold text-zinc-800 block">
                  Allowed Manufacturer Registry (AAGUID verification)
                </span>
                <p className="font-sans text-[11px] text-zinc-500 leading-relaxed">
                  Only authenticators from certified enterprise manufacturers are authorized for access under this profile:
                </p>
                <div className="space-y-1.5 max-h-[100px] overflow-y-auto">
                  {activeProfile.allowedAaguids.map((guid, idx) => (
                    <div key={idx} className="bg-white p-1.5 rounded border border-zinc-200 font-mono text-[9px] text-zinc-600 truncate flex items-center justify-between">
                      <span>{guid}</span>
                      <span className="text-[8px] bg-indigo-50 text-indigo-700 px-1 py-0.5 rounded font-sans uppercase">
                        AUTHORIZED
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              {/* Safe policy failure feedback */}
              <div className="p-3 bg-amber-50 border border-amber-100 rounded-xl flex items-start gap-2">
                <AlertOctagon className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <div className="space-y-0.5">
                  <span className="font-sans font-bold text-[11px] text-amber-950 block">Conformance Note:</span>
                  <p className="font-sans text-[11px] text-amber-900/90 leading-relaxed">
                    Devices failing to match AAGUID registries will trigger an <strong className="text-amber-950">Unsupported Environment / Device Blocked</strong> exception midway during assertion.
                  </p>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
