/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  Settings, Shield, Activity, HelpCircle, Save, Check, RefreshCw, 
  Clock, AlertOctagon, Globe, Volume2, CloudLightning, ShieldAlert 
} from 'lucide-react';
import { TelephonePolicy, ProviderConfig, CallStats } from '../types';
import { COUNTRIES } from '../data';

interface AdminConsoleProps {
  policy: TelephonePolicy;
  setPolicy: React.Dispatch<React.SetStateAction<TelephonePolicy>>;
  provider: ProviderConfig;
  setProvider: React.Dispatch<React.SetStateAction<ProviderConfig>>;
  stats: CallStats;
  setStats: React.Dispatch<React.SetStateAction<CallStats>>;
  logEvent: (type: string, details: string, status: 'success' | 'failure' | 'warning' | 'info') => void;
}

export default function AdminConsole({
  policy,
  setPolicy,
  provider,
  setProvider,
  stats,
  setStats,
  logEvent
}: AdminConsoleProps) {
  // Tabs inside Admin panel: 'policy', 'providers', 'diagnostics'
  const [adminTab, setAdminTab] = useState<'policy' | 'providers' | 'diagnostics'>('policy');
  const [isSaved, setIsSaved] = useState(false);

  const handleSave = (tab: string) => {
    setIsSaved(true);
    logEvent('TEL_ADMIN_UPDATE', `Administrative settings modified in ${tab.toUpperCase()} category.`, 'info');
    setTimeout(() => setIsSaved(false), 2000);
  };

  const handleRegionToggle = (countryCode: string) => {
    setPolicy(prev => {
      const allowed = prev.allowedRegions.includes(countryCode)
        ? prev.allowedRegions.filter(c => c !== countryCode)
        : [...prev.allowedRegions, countryCode];
      return { ...prev, allowedRegions: allowed };
    });
  };

  // Direct mock simulation to trigger a fake carrier outage
  const triggerProviderFailover = () => {
    setProvider(prev => {
      const original = prev.activeProvider;
      const next = prev.fallbackProvider;
      logEvent('TEL_PROVIDER_FAILOVER', `Simulated outage on ${original}. Initiated carrier failover to fallback gateway ${next}`, 'warning');
      return {
        ...prev,
        activeProvider: next,
        fallbackProvider: original
      };
    });
  };

  const resetStats = () => {
    setStats({
      totalCalls: 0,
      completed: 0,
      abandoned: 0,
      busyNoAnswer: 0,
      voicemailBlocked: 0,
      fraudAlerts: 0,
      estimatedCost: 0
    });
    logEvent('TEL_STATS_RESET', `Operational telemetry dashboard metrics flushed.`, 'warning');
  };

  return (
    <div className="flex flex-col h-full">
      {/* Sub tabs header */}
      <div className="flex border-b border-zinc-900 bg-zinc-950/20 px-4 py-2">
        <div className="flex space-x-1">
          {[
            { id: 'policy', label: 'Safety Policies', icon: Shield },
            { id: 'providers', label: 'Provider Gateways', icon: Settings },
            { id: 'diagnostics', label: 'Carrier Diagnostics', icon: Activity },
          ].map(tab => {
            const Icon = tab.icon;
            return (
              <button
                key={tab.id}
                onClick={() => setAdminTab(tab.id as any)}
                className={`flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold transition-all cursor-pointer ${
                  adminTab === tab.id
                    ? 'bg-zinc-905 border border-zinc-900 text-white shadow-sm'
                    : 'text-zinc-400 hover:text-zinc-200'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                <span>{tab.label}</span>
              </button>
            );
          })}
        </div>
      </div>

      {/* Admin content area */}
      <div className="flex-1 p-6 overflow-y-auto">

        {/* TAB: SAFETY POLICIES */}
        {adminTab === 'policy' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-bold text-white tracking-wide uppercase font-mono">Fraud & Access Safety Policy</h3>
              <p className="text-xs text-zinc-400 mt-1">Configure compliance rules, dialing rate limits, and access hour locks to curb call-pumping fraud.</p>
            </div>

            {/* Allowed Regions */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-3.5">
              <div>
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Whitelisted Signaling Regions</span>
                <p className="text-[10px] text-zinc-500 mt-0.5">Unchecked regions are instantly blocked during phone entries to mitigate spam pumping.</p>
              </div>

              <div className="grid grid-cols-2 gap-2">
                {COUNTRIES.map(country => {
                  const isChecked = policy.allowedRegions.includes(country.code);
                  return (
                    <label 
                      key={country.code}
                      className={`flex items-center justify-between p-2.5 rounded-lg border text-xs cursor-pointer transition-all ${
                        isChecked 
                          ? 'bg-zinc-900 border-zinc-900 text-zinc-200' 
                          : 'bg-zinc-950/20 border-zinc-900 text-zinc-500 hover:border-zinc-900'
                      }`}
                    >
                      <div className="flex items-center space-x-2">
                        <span className="font-mono text-[10px] font-bold text-zinc-400">{country.prefix}</span>
                        <span>{country.name}</span>
                      </div>
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => handleRegionToggle(country.code)}
                        className="rounded border-zinc-900 bg-zinc-950 text-emerald-500 focus:ring-emerald-500/20"
                      />
                    </label>
                  );
                })}
              </div>
            </div>

            {/* Rate limiting controls */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-4">
              <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Telephony Throttling & Attempts</span>
              
              <div className="grid grid-cols-3 gap-4">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Max Tries Before Lock</label>
                  <input
                    type="number"
                    value={policy.maxAttempts}
                    onChange={(e) => setPolicy({ ...policy, maxAttempts: parseInt(e.target.value) || 3 })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs font-mono text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Call Duration (Sec)</label>
                  <input
                    type="number"
                    value={policy.callDurationSeconds}
                    onChange={(e) => setPolicy({ ...policy, callDurationSeconds: parseInt(e.target.value) || 60 })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs font-mono text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Lockout Period (Min)</label>
                  <input
                    type="number"
                    value={policy.lockoutDurationMinutes}
                    onChange={(e) => setPolicy({ ...policy, lockoutDurationMinutes: parseInt(e.target.value) || 15 })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs font-mono text-white"
                  />
                </div>
              </div>
            </div>

            {/* Interactive policy check boxes */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-3.5">
              <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Security & Out-of-band Verification Posture</span>
              
              <div className="space-y-3 text-xs">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1.5">Verification Ceremony Mode</label>
                  <select
                    value={policy.requireApprovalMode}
                    onChange={(e) => setPolicy({ ...policy, requireApprovalMode: e.target.value as any })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300"
                  >
                    <option value="any">Accept either IVR keypad press OR Web confirmation code</option>
                    <option value="ivr_keypad">IVR Keypad confirmation only (No OTP entry on web)</option>
                    <option value="web_otp_only">Web OTP entry only (Read code to user via Voice)</option>
                    <option value="both">Mutual Handshake (Require IVR keypad [1], and Web OTP entry)</option>
                  </select>
                </div>

                <label className="flex items-center justify-between p-2 bg-zinc-900 border border-zinc-900 rounded-lg cursor-pointer">
                  <div className="flex items-start space-x-2.5">
                    <Clock className="w-4 h-4 text-zinc-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold text-zinc-200 block">Quiet Hours Restriction</span>
                      <span className="text-[10px] text-zinc-500 leading-none">Block non-critical automated calls between 22:00 - 07:00.</span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-1.5">
                    <span className="text-[10px] font-mono text-zinc-500">22:00-07:00</span>
                    <input
                      type="checkbox"
                      checked={policy.quietHoursStart === '22:00'}
                      onChange={(e) => setPolicy({ ...policy, quietHoursStart: e.target.checked ? '22:00' : '00:00', quietHoursEnd: e.target.checked ? '07:00' : '00:00' })}
                      className="rounded border-zinc-900 bg-zinc-950 text-emerald-500"
                    />
                  </div>
                </label>

                <label className="flex items-center justify-between p-2 bg-zinc-900 border border-zinc-900 rounded-lg cursor-pointer">
                  <div className="flex items-start space-x-2.5">
                    <AlertOctagon className="w-4 h-4 text-zinc-400 shrink-0 mt-0.5" />
                    <div>
                      <span className="font-semibold text-zinc-200 block">Active Voicemail Signaling Reject</span>
                      <span className="text-[10px] text-zinc-500 leading-none">Reject callbacks instantly if voicemail signals (beeps) are detected.</span>
                    </div>
                  </div>
                  <input
                    type="checkbox"
                    checked={policy.enableVoicemailDetection}
                    onChange={(e) => setPolicy({ ...policy, enableVoicemailDetection: e.target.checked })}
                    className="rounded border-zinc-900 bg-zinc-950 text-emerald-500"
                  />
                </label>
              </div>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => handleSave('policy')}
                className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-xs py-2.5 px-5 rounded-lg flex items-center space-x-1.5 transition-colors cursor-pointer"
              >
                {isSaved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
                <span>{isSaved ? 'Safety Policies Persisted' : 'Persist Safety Policies'}</span>
              </button>
            </div>
          </div>
        )}

        {/* TAB: PROVIDERS & ROUTING */}
        {adminTab === 'providers' && (
          <div className="space-y-6">
            <div>
              <h3 className="text-sm font-bold text-white tracking-wide uppercase font-mono">Gateway Providers & Carrier Routing</h3>
              <p className="text-xs text-zinc-400 mt-1">Configure Trunking partners, Caller ID credentials, and routing fallbacks to defend against gateway outages.</p>
            </div>

            {/* Provider Settings Form */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-4">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Primary Trunk Carrier</label>
                  <select
                    value={provider.activeProvider}
                    onChange={(e) => setProvider({ ...provider, activeProvider: e.target.value })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300"
                  >
                    <option value="twilio_telecom">Twilio Telecom Inc.</option>
                    <option value="infobip_voice">Infobip Voice Cloud</option>
                    <option value="custom_sip">Custom SIP Enterprise Trunks</option>
                  </select>
                </div>
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Failover Secondary Gate</label>
                  <select
                    value={provider.fallbackProvider}
                    onChange={(e) => setProvider({ ...provider, fallbackProvider: e.target.value })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300"
                  >
                    <option value="twilio_telecom">Twilio Telecom Inc.</option>
                    <option value="infobip_voice">Infobip Voice Cloud</option>
                    <option value="custom_sip">Custom SIP Enterprise Trunks</option>
                  </select>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Caller ID Display Name</label>
                  <input
                    type="text"
                    value={provider.callerIdName}
                    onChange={(e) => setProvider({ ...provider, callerIdName: e.target.value })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-white"
                  />
                </div>
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Outbound Caller Number</label>
                  <input
                    type="text"
                    value={provider.callerIdNumber}
                    onChange={(e) => setProvider({ ...provider, callerIdNumber: e.target.value })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-white font-mono"
                  />
                </div>
              </div>
            </div>

            {/* Voice & Locales */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-4">
              <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Neural Text-To-Speech Synthesis</span>
              
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">TTS Speech Language</label>
                  <select
                    value={provider.language}
                    onChange={(e) => setProvider({ ...provider, language: e.target.value })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300"
                  >
                    <option value="en-US">English (US)</option>
                    <option value="es-ES">Spanish (ES)</option>
                    <option value="fr-FR">French (FR)</option>
                    <option value="de-DE">German (DE)</option>
                  </select>
                </div>
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Acoustic Model Voice</label>
                  <select
                    value={provider.voiceType}
                    onChange={(e) => setProvider({ ...provider, voiceType: e.target.value as any })}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-xs text-zinc-300"
                  >
                    <option value="male">Male (Synthetic Classic)</option>
                    <option value="female">Female (Synthetic Classic)</option>
                    <option value="neural_assistant">AI Neural Assistant (High-fidelity WaveNet)</option>
                  </select>
                </div>
              </div>
            </div>

            {/* Carrier Callback Simulation Controls */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider">Gateway Callback API</span>
                <span className="text-[9px] font-mono font-bold bg-zinc-900 border border-zinc-900 text-emerald-400 px-2 py-0.5 rounded">AUTHENTICATED HANDSHAKE</span>
              </div>
              <input
                type="text"
                readOnly
                value={provider.callbackUrl}
                className="w-full bg-zinc-950/80 border border-zinc-900 rounded-lg p-2 text-[10px] font-mono text-zinc-500 focus:outline-none select-all"
              />
              <p className="text-[9px] text-zinc-500 leading-normal font-mono">
                Carriers send secure JSON webhook handshakes containing dialing metadata to this verification route after DTMF key interactions occur on physical handsets.
              </p>
            </div>

            {/* Failure Sandbox Button */}
            <div className="bg-amber-500/5 border border-amber-500/15 rounded-xl p-4 flex items-center justify-between">
              <div className="space-y-0.5 max-w-sm">
                <span className="text-xs font-semibold text-amber-300 block">Outage Simulation Sandbox</span>
                <span className="text-[10px] text-zinc-400 block leading-normal">Instantly trigger an outage of the active gateway to force routing fallbacks.</span>
              </div>
              <button
                onClick={triggerProviderFailover}
                className="bg-zinc-900 hover:bg-zinc-800 border border-zinc-900 text-zinc-200 text-xs font-semibold py-2 px-3.5 rounded-lg flex items-center space-x-1.5 cursor-pointer transition-all active:scale-95 shrink-0"
              >
                <CloudLightning className="w-3.5 h-3.5 text-amber-400 shrink-0" />
                <span>Trigger Gate Outage</span>
              </button>
            </div>

            <div className="flex justify-end pt-2">
              <button
                onClick={() => handleSave('providers')}
                className="bg-emerald-500 hover:bg-emerald-600 text-slate-950 font-bold text-xs py-2.5 px-5 rounded-lg flex items-center space-x-1.5 transition-colors cursor-pointer"
              >
                {isSaved ? <Check className="w-4 h-4" /> : <Save className="w-4 h-4" />}
                <span>{isSaved ? 'Gateway Configuration Saved' : 'Save Gateway Parameters'}</span>
              </button>
            </div>
          </div>
        )}

        {/* TAB: CARRIER DIAGNOSTICS */}
        {adminTab === 'diagnostics' && (
          <div className="space-y-6">
            <div className="flex justify-between items-start">
              <div>
                <h3 className="text-sm font-bold text-white tracking-wide uppercase font-mono">Carrier Telemetry & Call Health</h3>
                <p className="text-xs text-zinc-400 mt-1">Real-time statistics monitor, fraud pattern logs, and billing calculations.</p>
              </div>
              <button
                onClick={resetStats}
                className="text-[10px] text-zinc-500 hover:text-red-400 flex items-center space-x-1 font-mono cursor-pointer transition-all"
              >
                <RefreshCw className="w-3 h-3" />
                <span>Reset Telemetry Data</span>
              </button>
            </div>

            {/* Quick stats numbers bar */}
            <div className="grid grid-cols-4 gap-3">
              {[
                { title: 'Total Handshakes', value: stats.totalCalls, desc: 'Calls initiated' },
                { title: 'Completed', value: `${stats.completed}`, desc: '98.5% Callback rate' },
                { title: 'Abandoned / Failed', value: `${stats.abandoned + stats.busyNoAnswer}`, desc: 'Line drops' },
                { title: 'Est. Gateway Billing', value: `$${stats.estimatedCost.toFixed(2)}`, desc: 'USDT avg' },
              ].map((stat, i) => (
                <div key={i} className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-3.5 text-left">
                  <span className="text-[10px] text-zinc-500 font-mono uppercase block">{stat.title}</span>
                  <span className="text-lg font-bold text-white block mt-1 tracking-tight font-mono">{stat.value}</span>
                  <span className="text-[9px] text-zinc-400 block mt-0.5">{stat.desc}</span>
                </div>
              ))}
            </div>

            {/* Hand-drawn premium SVG area (represents hourly load chart) */}
            <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4.5 space-y-4">
              <div className="flex justify-between items-center">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Live Delivery Rate Wave (Last 24h)</span>
                <div className="flex space-x-3 text-[9px] font-mono text-zinc-500">
                  <span className="flex items-center space-x-1"><span className="w-2 h-2 rounded bg-emerald-500"></span><span>Callbacks</span></span>
                  <span className="flex items-center space-x-1"><span className="w-2 h-2 rounded bg-red-400"></span><span>Carrier drops</span></span>
                </div>
              </div>

              {/* Handcrafted premium layout chart using standard high-quality SVG */}
              <div className="relative w-full h-32 bg-zinc-950/20 border border-zinc-900 rounded-lg overflow-hidden">
                <svg className="w-full h-full" viewBox="0 0 400 120" preserveAspectRatio="none">
                  {/* Grid Lines */}
                  <line x1="0" y1="30" x2="400" y2="30" stroke="#1f2937" strokeDasharray="4 4" strokeWidth="0.5" />
                  <line x1="0" y1="60" x2="400" y2="60" stroke="#1f2937" strokeDasharray="4 4" strokeWidth="0.5" />
                  <line x1="0" y1="90" x2="400" y2="90" stroke="#1f2937" strokeDasharray="4 4" strokeWidth="0.5" />

                  {/* Gradient Area for Callbacks */}
                  <defs>
                    <linearGradient id="grad-callback" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stopColor="#10b981" stopOpacity="0.15" />
                      <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                    </linearGradient>
                  </defs>
                  
                  {/* Callback Wave Path */}
                  <path 
                    d="M 0,90 Q 50,40 100,70 T 200,30 T 300,50 T 400,20 L 400,120 L 0,120 Z" 
                    fill="url(#grad-callback)" 
                  />
                  <path 
                    d="M 0,90 Q 50,40 100,70 T 200,30 T 300,50 T 400,20" 
                    fill="none" 
                    stroke="#10b981" 
                    strokeWidth="2" 
                    strokeLinecap="round"
                  />

                  {/* Carrier Drops Path */}
                  <path 
                    d="M 0,110 Q 50,112 100,95 T 200,105 T 300,100 T 400,115" 
                    fill="none" 
                    stroke="#f87171" 
                    strokeWidth="1.5" 
                    strokeDasharray="3 3"
                    strokeLinecap="round"
                  />
                </svg>
                <div className="absolute bottom-2 left-3 text-[8px] font-mono text-zinc-500">00:00</div>
                <div className="absolute bottom-2 right-3 text-[8px] font-mono text-zinc-500">23:59</div>
              </div>
            </div>

            {/* Carrier Outage / Fraud indicators */}
            <div className="grid grid-cols-2 gap-4">
              
              <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4 space-y-3">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Carrier Signaling Latency</span>
                
                <div className="space-y-2 text-xs">
                  {[
                    { carrier: 'Twilio Gateway Trunks (US/CA)', ping: '42ms', load: 'Optimized', color: 'text-emerald-400' },
                    { carrier: 'Infobip Global Signaling Routing', ping: '84ms', load: 'Optimized', color: 'text-emerald-400' },
                    { carrier: 'Custom SIP Enterprise Backplane', ping: '110ms', load: 'Mild queue congestion', color: 'text-amber-400' }
                  ].map((trunk, i) => (
                    <div key={i} className="flex justify-between items-center p-1.5 bg-zinc-900 border border-zinc-900/40 rounded-lg">
                      <span className="font-semibold text-zinc-300 font-mono text-[10px]">{trunk.carrier}</span>
                      <div className="flex items-center space-x-2 text-[10px] font-mono">
                        <span className="text-zinc-500">{trunk.ping}</span>
                        <span className={`font-bold ${trunk.color}`}>{trunk.load}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="bg-zinc-950/40 border border-zinc-900 rounded-xl p-4 space-y-3">
                <span className="text-[11px] font-mono font-medium text-zinc-400 uppercase tracking-wider block">Security & Fraud Indicators</span>
                
                <div className="space-y-2 text-xs">
                  <div className="flex justify-between text-[10px] p-1.5 bg-zinc-900/60 rounded-lg">
                    <span className="text-zinc-400 font-mono">Robotic pumping threshold:</span>
                    <span className="font-bold text-white font-mono">ACTIVE (Max 3/min)</span>
                  </div>
                  <div className="flex justify-between text-[10px] p-1.5 bg-zinc-900/60 rounded-lg">
                    <span className="text-zinc-400 font-mono">Replay nonce check:</span>
                    <span className="font-bold text-emerald-400 font-mono">ENFORCED</span>
                  </div>
                  <div className="flex justify-between text-[10px] p-1.5 bg-zinc-900/60 rounded-lg">
                    <span className="text-zinc-400 font-mono">Voicemail signaling check:</span>
                    <span className="font-bold text-emerald-400 font-mono">VOICEMAIL_DROP_ACTIVE</span>
                  </div>
                </div>
              </div>

            </div>

          </div>
        )}

      </div>
    </div>
  );
}
