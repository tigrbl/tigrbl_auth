/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { ShieldCheck, ArrowRight, Laptop, Globe, AlertCircle } from 'lucide-react';
import { SimConfig } from '../types';

interface EnterpriseMethodCardProps {
  onStartAuth: (bypassIntro: boolean) => void;
  simConfig: SimConfig;
  orgName: string;
}

export default function EnterpriseMethodCard({
  onStartAuth,
  simConfig,
  orgName,
}: EnterpriseMethodCardProps) {
  const [emailInput, setEmailInput] = useState('');
  const [showIntro, setShowIntro] = useState(false);
  const [isAutoPending, setIsAutoPending] = useState(false);

  const getBrowserCompatibilityLabel = () => {
    switch (simConfig.browserType) {
      case 'Chrome_Managed':
      case 'Edge_Enterprise':
        return { label: 'Managed Corporate Browser', color: 'text-emerald-700 bg-emerald-50 border-emerald-100' };
      case 'Firefox_Unmanaged':
        return { label: 'Unmanaged Browser', color: 'text-amber-700 bg-amber-50 border-amber-100' };
      case 'Safari_Private':
        return { label: 'Private / Restricted Browser', color: 'text-rose-700 bg-rose-50 border-rose-100' };
      case 'Native_App':
        return { label: 'Native Workplace App', color: 'text-blue-700 bg-blue-50 border-blue-100' };
    }
  };

  const currentNetworkLabel = simConfig.isCorpNetwork
    ? { label: 'Corporate Network (Active Directory Realm)', color: 'text-emerald-700 bg-emerald-50' }
    : { label: 'External / Unmanaged Network', color: 'text-amber-700 bg-amber-50' };

  const compat = getBrowserCompatibilityLabel();

  const handleDiscoverySubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!emailInput) return;
    // Check if the domain is enterprise eligible (for demo, any @corp or @enterprise or general submit shows intro/wia option)
    setShowIntro(true);
  };

  const triggerAutoSignOn = () => {
    setIsAutoPending(true);
    setTimeout(() => {
      onStartAuth(true); // Automatically attempts silently
      setIsAutoPending(false);
    }, 600);
  };

  return (
    <div id="enterprise-method-card" className="w-full max-w-md bg-white rounded-2xl border border-slate-200/80 shadow-xl overflow-hidden transition-all duration-300 hover:shadow-2xl">
      {/* Visual Header */}
      <div className="p-6 pb-4 bg-gradient-to-br from-slate-900 to-slate-950 text-white relative">
        <div className="absolute top-4 right-4 bg-white/10 px-2 py-1 rounded text-[10px] font-mono tracking-wider text-slate-300 uppercase">
          AMR: wia
        </div>
        <div className="w-12 h-12 rounded-xl bg-blue-600/20 border border-blue-400/30 flex items-center justify-center mb-4 text-blue-400 shadow-inner">
          <ShieldCheck className="w-6 h-6" />
        </div>
        <h2 className="font-display text-2xl font-semibold tracking-tight">
          {orgName} Sign In
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Workstation Credential Gateway
        </p>
      </div>

      {/* Discovery / Selection Body */}
      <div className="p-6 space-y-6">
        {!showIntro ? (
          <div className="space-y-5">
            <p className="text-sm text-slate-600 leading-relaxed">
              Enter your corporate email address to automatically route to your organization's secure sign-on provider.
            </p>

            <form onSubmit={handleDiscoverySubmit} className="space-y-4">
              <div>
                <label htmlFor="email" className="block text-xs font-medium text-slate-700 uppercase tracking-wider mb-2">
                  Work Account Email
                </label>
                <div className="relative">
                  <input
                    type="email"
                    id="email"
                    required
                    value={emailInput}
                    onChange={(e) => setEmailInput(e.target.value)}
                    placeholder="e.g. employee@corp.enterprise.local"
                    className="w-full px-4 py-3 rounded-lg border border-slate-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm placeholder-slate-400 transition-all font-sans outline-none"
                  />
                </div>
              </div>

              <button
                type="submit"
                id="btn-discover"
                className="w-full py-3 px-4 bg-slate-900 hover:bg-slate-800 text-white rounded-lg text-sm font-medium transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-md"
              >
                Discover Organization Account
                <ArrowRight className="w-4 h-4" />
              </button>
            </form>

            <div className="relative flex py-2 items-center">
              <div className="flex-grow border-t border-slate-200"></div>
              <span className="flex-shrink mx-4 text-xs text-slate-400 uppercase tracking-widest font-mono">Or use active session</span>
              <div className="flex-grow border-t border-slate-200"></div>
            </div>

            {/* Use Work Account Button */}
            <button
              onClick={() => setShowIntro(true)}
              id="btn-use-work-account"
              className="w-full py-4 px-4 bg-blue-50 hover:bg-blue-100/80 text-blue-700 border border-blue-200/60 rounded-xl transition-all duration-200 flex items-center justify-between text-left group cursor-pointer"
            >
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-lg bg-blue-600 text-white flex items-center justify-center shadow-md">
                  <Laptop className="w-5 h-5" />
                </div>
                <div>
                  <p className="text-sm font-semibold tracking-tight">Use your work account</p>
                  <p className="text-xs text-blue-600/70">Sign in using current Windows session</p>
                </div>
              </div>
              <ArrowRight className="w-4 h-4 text-blue-500 transition-transform group-hover:translate-x-1" />
            </button>
          </div>
        ) : (
          <div className="space-y-5 animate-fadeIn">
            <div className="bg-slate-50 border border-slate-100 rounded-xl p-4 space-y-3">
              <h3 className="text-xs font-semibold uppercase tracking-wider text-slate-600">
                Integrated Authentication Policy
              </h3>
              <p className="text-xs text-slate-600 leading-relaxed">
                We will attempt to verify your identities using Windows Integrated Authentication (WIA / Negotiate).
              </p>

              <div className="grid grid-cols-2 gap-2 pt-1">
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 flex flex-col justify-between">
                  <span className="text-[10px] text-slate-400 uppercase font-mono">Environment Context</span>
                  <span className={`text-[11px] font-medium truncate mt-1 ${compat.color} px-1.5 py-0.5 rounded inline-block text-center border`}>
                    {compat.label}
                  </span>
                </div>
                <div className="p-2 bg-white rounded-lg border border-slate-200/60 flex flex-col justify-between">
                  <span className="text-[10px] text-slate-400 uppercase font-mono">Network Scope</span>
                  <span className={`text-[11px] font-medium truncate mt-1 ${currentNetworkLabel.color} px-1.5 py-0.5 rounded inline-block text-center`}>
                    {simConfig.isCorpNetwork ? 'Intranet Realm' : 'External Net'}
                  </span>
                </div>
              </div>
            </div>

            <div className="space-y-2">
              <button
                onClick={triggerAutoSignOn}
                disabled={isAutoPending}
                id="btn-wia-negotiate"
                className="w-full py-3 px-4 bg-blue-600 hover:bg-blue-700 text-white rounded-lg text-sm font-semibold transition-colors flex items-center justify-center gap-2 cursor-pointer shadow-md shadow-blue-500/10 disabled:opacity-50"
              >
                {isAutoPending ? 'Contacting Local KDC...' : 'Sign In Automatically'}
                {!isAutoPending && <ShieldCheck className="w-4 h-4" />}
              </button>

              <div className="flex justify-between items-center px-1">
                <button
                  type="button"
                  onClick={() => setShowIntro(false)}
                  className="text-xs font-medium text-slate-500 hover:text-slate-800 transition-colors"
                >
                  Change Account
                </button>
                <span className="text-[10px] font-mono text-slate-400">Realm: {orgName.toLowerCase().replace(/\s+/g, '')}.local</span>
              </div>
            </div>

            {!simConfig.isCorpNetwork && (
              <div className="p-3 bg-amber-50 border border-amber-200/60 rounded-xl flex gap-2.5">
                <AlertCircle className="w-5 h-5 text-amber-600 shrink-0 mt-0.5" />
                <div className="space-y-0.5">
                  <p className="text-xs font-semibold text-amber-800">Unmanaged / External Network</p>
                  <p className="text-[11px] text-amber-700 leading-relaxed">
                    Direct Kerberos Negotiate cannot reach KDCs outside corporate bounds. System will automatically evaluate and route to federation backup if allowed.
                  </p>
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Security notice footer */}
      <div className="px-6 py-4 bg-slate-50 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
        <span className="flex items-center gap-1">
          <Globe className="w-3.5 h-3.5" /> Secure Channel Binding Active
        </span>
        <span className="font-mono">FIPS 140-2</span>
      </div>
    </div>
  );
}
