/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { ShieldCheck, ToggleLeft, ShieldAlert, CheckCircle2, AlertTriangle, HelpCircle, ToggleRight } from 'lucide-react';
import { BrowserPolicy } from '../types';

interface BrowserCompatibilityMatrixProps {
  policy: BrowserPolicy;
  onUpdatePolicy: (policy: BrowserPolicy) => void;
}

export default function BrowserCompatibilityMatrix({
  policy,
  onUpdatePolicy,
}: BrowserCompatibilityMatrixProps) {

  const handleToggleWiaEnabled = () => {
    onUpdatePolicy({ ...policy, wiaEnabled: !policy.wiaEnabled });
  };

  const handleTogglePrivateBrowsing = () => {
    onUpdatePolicy({ ...policy, allowPrivateBrowsingWia: !policy.allowPrivateBrowsingWia });
  };

  const handleToggleIntranetZone = () => {
    onUpdatePolicy({ ...policy, intranetZoneOnly: !policy.intranetZoneOnly });
  };

  const handleToggleChannelBinding = () => {
    onUpdatePolicy({ ...policy, requireChannelBinding: !policy.requireChannelBinding });
  };

  const handleExtendedProtectionChange = (val: 'Off' | 'WhenSupported' | 'Required') => {
    onUpdatePolicy({ ...policy, extendedProtection: val });
  };

  return (
    <div id="browser-compatibility-matrix" className="bg-white rounded-2xl border border-slate-200 p-6 space-y-6 shadow-sm">
      <div className="border-b border-slate-100 pb-4">
        <h3 className="font-display font-semibold text-slate-800 text-lg flex items-center gap-2">
          <ShieldCheck className="w-5 h-5 text-slate-600" />
          Browser & Device GPO Policy Engine
        </h3>
        <p className="text-xs text-slate-500">Configure Group Policies (GPO) and local intranet zoning enforced when workstation browsers request SPNs.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Policy toggles */}
        <div className="space-y-4">
          <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Device Policy Controls</h4>

          <div className="space-y-3.5">
            {/* WIA Enabled */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50/50">
              <div>
                <p className="text-xs font-semibold text-slate-800">Negotiate Authentication Status</p>
                <p className="text-[11px] text-slate-500">Allow browsers to negotiate Kerberos handshakes automatically.</p>
              </div>
              <button onClick={handleToggleWiaEnabled} className="cursor-pointer">
                {policy.wiaEnabled ? (
                  <ToggleRight className="w-10 h-10 text-blue-600" />
                ) : (
                  <ToggleLeft className="w-10 h-10 text-slate-400" />
                )}
              </button>
            </div>

            {/* Intranet Zone Check */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50/50">
              <div>
                <p className="text-xs font-semibold text-slate-800">Restrict to Intranet Zoning</p>
                <p className="text-[11px] text-slate-500">Only trigger WIA if browser reports site resides inside the local Intranet Zone.</p>
              </div>
              <button onClick={handleToggleIntranetZone} className="cursor-pointer">
                {policy.intranetZoneOnly ? (
                  <ToggleRight className="w-10 h-10 text-blue-600" />
                ) : (
                  <ToggleLeft className="w-10 h-10 text-slate-400" />
                )}
              </button>
            </div>

            {/* Private Browsing allowed? */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50/50">
              <div>
                <p className="text-xs font-semibold text-slate-800">Allow WIA in Ephemeral/Private Windows</p>
                <p className="text-[11px] text-slate-500">Allow automatic authentication inside Incognito or Private tabs.</p>
              </div>
              <button onClick={handleTogglePrivateBrowsing} className="cursor-pointer">
                {policy.allowPrivateBrowsingWia ? (
                  <ToggleRight className="w-10 h-10 text-blue-600" />
                ) : (
                  <ToggleLeft className="w-10 h-10 text-slate-400" />
                )}
              </button>
            </div>

            {/* Channel Binding check */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50/50">
              <div>
                <p className="text-xs font-semibold text-slate-800">Enforce Extended Protection for Authentication (EPA)</p>
                <p className="text-[11px] text-slate-500">Require client channel bindings (hash of SSL cert) in Kerberos AP-REQ token.</p>
              </div>
              <button onClick={handleToggleChannelBinding} className="cursor-pointer">
                {policy.requireChannelBinding ? (
                  <ToggleRight className="w-10 h-10 text-blue-600" />
                ) : (
                  <ToggleLeft className="w-10 h-10 text-slate-400" />
                )}
              </button>
            </div>

            {/* EPA Level dropdown */}
            <div className="flex items-center justify-between p-3 rounded-xl border border-slate-100 bg-slate-50/50">
              <div>
                <p className="text-xs font-semibold text-slate-800">EPA Extended Protection Level</p>
                <p className="text-[11px] text-slate-500">Level of channel binding and target SPN validation enforcement.</p>
              </div>
              <select
                value={policy.extendedProtection}
                onChange={(e: any) => handleExtendedProtectionChange(e.target.value)}
                className="px-2 py-1.5 text-xs rounded border border-slate-300 bg-white"
              >
                <option value="Off">Disabled (Off)</option>
                <option value="WhenSupported">When Supported (Optional)</option>
                <option value="Required">Required (Always Enforce)</option>
              </select>
            </div>
          </div>
        </div>

        {/* Compatibility Matrix List */}
        <div className="space-y-4">
          <h4 className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Environment Compatibility Profile</h4>

          <div className="space-y-3 font-sans">
            {policy.supportedBrowsers.map((browserItem, idx) => (
              <div key={idx} className="flex items-center justify-between p-3 rounded-xl border border-slate-150">
                <div className="flex items-center gap-3">
                  <div className={`w-8 h-8 rounded-lg flex items-center justify-center ${browserItem.supported ? 'bg-emerald-50 text-emerald-600' : 'bg-rose-50 text-rose-600'}`}>
                    {browserItem.supported ? (
                      <CheckCircle2 className="w-4 h-4" />
                    ) : (
                      <ShieldAlert className="w-4 h-4" />
                    )}
                  </div>
                  <div>
                    <p className="text-xs font-semibold text-slate-800">{browserItem.browser}</p>
                    <p className="text-[10px] text-slate-400 font-mono">Platform: {browserItem.os}</p>
                  </div>
                </div>

                <div className="text-right">
                  <span className={`text-[10px] font-mono px-2 py-0.5 rounded ${
                    browserItem.supported ? 'bg-emerald-50 text-emerald-700' : 'bg-rose-50 text-rose-700'
                  }`}>
                    {browserItem.supported ? 'SUPPORTED' : 'RESTRICTED'}
                  </span>
                  <p className="text-[9px] text-slate-400 mt-1 font-mono">Status: {browserItem.policyStatus}</p>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
