/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from 'react';
import { 
  Shield, Phone, Settings, Activity, AlertTriangle, Play, CheckCircle2, 
  RotateCcw, ShieldCheck, Globe, Wifi, Key, Lock, Layers, RefreshCw, 
  Sliders, Info, FileCode, CheckSquare, XSquare, PlusCircle, Server
} from 'lucide-react';
import { 
  PhoneAuthenticator, CallContext, AuditLog, TelephonePolicy, 
  ProviderConfig, CallStats, CallState 
} from './types';
import { 
  COUNTRIES, INITIAL_POLICIES, INITIAL_PROVIDERS, 
  INITIAL_AUTHENTICATORS, INITIAL_STATS, INITIAL_AUDIT_LOGS, 
  maskPhoneNumber 
} from './data';
import AuthCeremony from './components/AuthCeremony';
import PhoneSimulator from './components/PhoneSimulator';

export default function App() {
  // Application states
  const [enrolledPhones, setEnrolledPhones] = useState<PhoneAuthenticator[]>(INITIAL_AUTHENTICATORS);
  const [activeCall, setActiveCall] = useState<CallContext | null>(null);
  const [policy, setPolicy] = useState<TelephonePolicy>(INITIAL_POLICIES);
  const [provider, setProvider] = useState<ProviderConfig>(INITIAL_PROVIDERS);
  const [logs, setLogs] = useState<AuditLog[]>(INITIAL_AUDIT_LOGS);
  const [stats, setStats] = useState<CallStats>(INITIAL_STATS);
  const [simulateStateOverride, setSimulateStateOverride] = useState<'none' | 'busy' | 'no_answer' | 'voicemail' | 'outage'>('none');
  const [successAmr, setSuccessAmr] = useState<any | null>(null);

  // Filter/Search audit logs state
  const [logSearchQuery, setLogSearchQuery] = useState('');
  const [logFilterStatus, setLogFilterStatus] = useState<'all' | 'success' | 'failure' | 'warning' | 'info'>('all');

  // Interactive configurations tab toggler
  const [showConfig, setShowConfig] = useState(true);

  // Real-time server uptime timer (P2 decorative metrics)
  const [uptime, setUptime] = useState('00:00:00');
  useEffect(() => {
    const start = Date.now();
    const interval = setInterval(() => {
      const diff = Date.now() - start;
      const hrs = Math.floor(diff / 3600000).toString().padStart(2, '0');
      const mins = Math.floor((diff % 3600000) / 60000).toString().padStart(2, '0');
      const secs = Math.floor((diff % 60000) / 1000).toString().padStart(2, '0');
      setUptime(`${hrs}:${mins}:${secs}`);
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  // Out-of-band call heartbeat & expiration simulation timer (Crucial for dialing lifecycles)
  useEffect(() => {
    if (!activeCall) return;

    const timer = setInterval(() => {
      setActiveCall(prev => {
        if (!prev) return null;
        
        // Expiration check
        if (prev.timer <= 1) {
          clearInterval(timer);
          logEvent(
            'TEL_CALL_EXPIRED', 
            `OOB verification call session ${prev.id} expired due to network timeout.`, 
            'failure'
          );
          setStats(s => ({ ...s, abandoned: s.abandoned + 1 }));
          return null;
        }

        // Auto transition logic for ring -> answer
        let nextStatus = prev.status;
        if (prev.status === 'queued') {
          nextStatus = 'ringing';
          logEvent('TEL_CARRIER_RINGING', `Outbound trunks initialized. Ringing phone ${prev.maskedDestination} ...`, 'info');
        } else if (prev.status === 'connected') {
          // Progress connected -> ivr_active
          nextStatus = 'ivr_active';
          logEvent('TEL_IVR_ACTIVE', `Speech synthesizer streaming verification voice track to device.`, 'success');
        }

        return {
          ...prev,
          status: nextStatus,
          timer: prev.timer - 1
        };
      });
    }, 1000);

    return () => clearInterval(timer);
  }, [activeCall]);

  // Helper helper to append telemetry logs dynamically
  const logEvent = (type: string, details: string, status: 'success' | 'failure' | 'warning' | 'info') => {
    const newLog: AuditLog = {
      id: `log-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString(),
      eventType: type,
      details,
      status,
      ipAddress: '198.51.100.104',
      maskedNumber: activeCall ? activeCall.maskedDestination : undefined
    };
    setLogs(prev => [newLog, ...prev]);
  };

  // Launch outbound telephone call (Triggered from AuthCeremony panel)
  const startCall = (
    type: 'enrollment' | 'login' | 'step_up', 
    rawNumber: string, 
    label?: string,
    ivrMode?: 'code_read' | 'approval_press',
    purpose?: string
  ) => {
    // Generate a 3-digit verification code
    const generatedCode = Math.floor(100 + Math.random() * 900).toString();
    const masked = maskPhoneNumber(rawNumber, COUNTRIES[0].code);

    const newCall: CallContext = {
      id: `call-${Date.now().toString().slice(-6)}`,
      type,
      destination: rawNumber,
      maskedDestination: masked,
      verificationCode: generatedCode,
      ivrMode: ivrMode || 'approval_press',
      timer: policy.callDurationSeconds,
      maxTimer: policy.callDurationSeconds,
      transactionPurpose: purpose || 'Standard Identity Access',
      status: 'queued',
      provider: provider.activeProvider
    };

    setSuccessAmr(null); // Clear old authentication success certificates
    setActiveCall(newCall);
    setStats(s => ({ ...s, totalCalls: s.totalCalls + 1 }));
    logEvent(
      'TEL_CALL_INITIATED', 
      `Dispatched verification request. Mode: ${newCall.ivrMode.toUpperCase()}. Destination: ${newCall.maskedDestination}`, 
      'info'
    );
  };

  // Abort call sequence manually
  const cancelCall = () => {
    if (!activeCall) return;
    logEvent('TEL_CALL_CANCELLED', `Out-of-band call verification session ${activeCall.id} cancelled by administrative operator.`, 'warning');
    setActiveCall(null);
  };

  // Clicked "Answer" on Phone Simulator screen
  const onAnswerCall = () => {
    if (!activeCall) return;
    setActiveCall(prev => prev ? { ...prev, status: 'connected' } : null);
    logEvent('TEL_LINE_ANSWERED', `Call handset successfully picked up by remote receiver. Handshake established.`, 'info');
  };

  // Clicked "Decline" / Hangup / Carrier rejected
  const onDeclineCall = (reason: 'busy' | 'no_answer' | 'voicemail' | 'rejected' | 'failed') => {
    if (!activeCall) return;
    
    let eventType = 'TEL_LINE_DISCONNECT';
    let status: 'failure' | 'warning' = 'warning';
    let message = `Out-of-band call was declined. Reason: ${reason}`;

    if (reason === 'busy') {
      eventType = 'TEL_CARRIER_BUSY';
      message = `Outbound route returned: CARRIER_LINE_BUSY (486 Busy Here).`;
      setStats(s => ({ ...s, busyNoAnswer: s.busyNoAnswer + 1 }));
    } else if (reason === 'no_answer') {
      eventType = 'TEL_CARRIER_NO_ANSWER';
      message = `Outbound route returned: CARRIER_NO_RESPONSE (408 Timeout).`;
      setStats(s => ({ ...s, busyNoAnswer: s.busyNoAnswer + 1 }));
    } else if (reason === 'voicemail') {
      eventType = 'TEL_VOICEMAIL_DETECTED';
      message = `Signal processing system matched answering machine voice frequencies. Dropping call to secure route.`;
      setStats(s => ({ ...s, voicemailBlocked: s.voicemailBlocked + 1 }));
    } else if (reason === 'rejected') {
      eventType = 'TEL_USER_REJECTED';
      message = `Physical telephone verification rejected manually on dialpad by operator.`;
    } else if (reason === 'failed') {
      eventType = 'TEL_GATEWAY_OUTAGE';
      message = `Trunk provider reported signaling transmission loss (503 Service Unavailable).`;
      status = 'failure';
    }

    logEvent(eventType, message, status);
    setActiveCall(prev => prev ? { ...prev, status: reason } : null);

    // Auto clear call state after 3 seconds so the phone returns to idle cleanly
    setTimeout(() => {
      setActiveCall(prev => {
        if (prev && ['busy', 'no_answer', 'voicemail', 'rejected', 'failed'].includes(prev.status)) {
          return null;
        }
        return prev;
      });
    }, 3000);
  };

  // Triggered when keypad keys are clicked on simulator (helpful for audit trace)
  const onKeypadPress = (key: string) => {
    if (!activeCall) return;
    logEvent('TEL_DTMF_KEYPRESS', `Received OOB callback DTMF signal code: [ ${key} ]`, 'info');
  };

  // IVR approved via pressing [ 1 ] on keypad
  const onIvrSuccess = () => {
    if (!activeCall) return;
    
    logEvent(
      'TEL_IVR_APPROVED', 
      `User confirmed credentials by transmitting secure IVR key press sequence [ 1 ]`, 
      'success'
    );
    
    setActiveCall(prev => prev ? { ...prev, status: 'completed' } : null);
    setStats(s => ({ ...s, completed: s.completed + 1 }));

    // Dispatched success results internally
    const mockAmrPayload = {
      amr: 'tel',
      maskedDestination: activeCall.maskedDestination,
      authenticatedAt: new Date().toISOString(),
      providerUsed: provider.activeProvider,
      transactionBounded: activeCall.type === 'step_up',
      purpose: activeCall.transactionPurpose,
      assuranceLevel: 'higher_assurance (Dual oob channel confirmation; approved via IVR voice gateway keypad)',
    };
    
    setSuccessAmr(mockAmrPayload);

    // Auto hang up phone line after 2.5s
    setTimeout(() => {
      setActiveCall(null);
    }, 2500);
  };

  // Display authentication certificate evidence once success flows complete
  const onSuccessfulAuthentication = (amrResult: any) => {
    setSuccessAmr(amrResult);
    setStats(s => ({ ...s, completed: s.completed + 1 }));
    
    // Auto hang up phone on web success OTP matching
    if (activeCall) {
      setActiveCall(prev => prev ? { ...prev, status: 'completed' } : null);
      setTimeout(() => {
        setActiveCall(null);
      }, 2500);
    }
  };

  // Filter audit logs list
  const filteredLogs = logs.filter(log => {
    const matchesSearch = log.eventType.toLowerCase().includes(logSearchQuery.toLowerCase()) || 
                          log.details.toLowerCase().includes(logSearchQuery.toLowerCase());
    const matchesStatus = logFilterStatus === 'all' || log.status === logFilterStatus;
    return matchesSearch && matchesStatus;
  });

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-emerald-500/20 selection:text-emerald-300">
      
      {/* Top Professional Header Bar */}
      <header className="border-b border-zinc-900 bg-zinc-950/80 backdrop-blur-md sticky top-0 z-50 px-6 py-3.5 flex justify-between items-center">
        <div className="flex items-center space-x-3">
          <div className="w-9 h-9 bg-emerald-500/10 border border-emerald-500/20 rounded-xl flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-5 h-5 animate-[pulse_3s_infinite]" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-sm font-bold text-white tracking-wider font-mono">TELEPHONE CONFIRMATION ENGINE</h1>
              <span className="text-[9px] font-mono font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 rounded px-1.5 py-0.5">MFA/AMR</span>
            </div>
            <p className="text-[11px] text-zinc-500">Security-hardened out-of-band telecommunications authentication gateway simulator</p>
          </div>
        </div>

        <div className="flex items-center space-x-4">
          {/* Diagnostic Stats */}
          <div className="hidden md:flex items-center space-x-6 border-r border-zinc-900 pr-6">
            <div className="text-right">
              <span className="text-[9px] font-mono text-zinc-500 block uppercase">Gateway Status</span>
              <div className="flex items-center space-x-1 justify-end">
                <span className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-ping"></span>
                <span className="text-xs font-mono font-bold text-white">SYSTEM ONLINE</span>
              </div>
            </div>
            <div className="text-right">
              <span className="text-[9px] font-mono text-zinc-500 block uppercase">Server Uptime</span>
              <span className="text-xs font-mono font-bold text-zinc-300">{uptime}</span>
            </div>
          </div>

          <button
            onClick={() => setShowConfig(!showConfig)}
            className={`px-3.5 py-1.5 rounded-lg border border-zinc-900 text-xs font-semibold flex items-center space-x-1.5 transition-all cursor-pointer ${
              showConfig 
                ? 'bg-zinc-900 border-zinc-900 text-white' 
                : 'border-zinc-900 text-zinc-400 hover:text-zinc-200'
            }`}
          >
            <Settings className="w-3.5 h-3.5" />
            <span>Policy Config</span>
          </button>
        </div>
      </header>

      {/* Main Grid Layout */}
      <main className="flex-1 grid grid-cols-1 xl:grid-cols-12 gap-6 p-6 overflow-hidden">
        
        {/* Left Column: Dynamic Policy Configuration Dashboard (Optional & Resizable) */}
        {showConfig && (
          <div className="xl:col-span-3 space-y-6 flex flex-col max-h-[85vh] overflow-y-auto pr-1">
            
            {/* Telecom Provider Selectors */}
            <div className="bg-zinc-900/60 border border-zinc-900 rounded-2xl p-5 space-y-4">
              <div className="flex items-center space-x-2 pb-2 border-b border-zinc-900">
                <Server className="w-4 h-4 text-emerald-400" />
                <h2 className="text-xs font-bold font-mono tracking-widest text-white uppercase">Carrier Route Provider</h2>
              </div>

              <div className="space-y-3 text-xs">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Active Gateway Operator</label>
                  <select
                    value={provider.activeProvider}
                    onChange={(e) => {
                      const next = e.target.value;
                      setProvider(p => ({ ...p, activeProvider: next }));
                      logEvent('TEL_PROVIDER_SWITCH', `Signaling routing switched to gateway: ${next.toUpperCase()}`, 'warning');
                    }}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-zinc-300 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="twilio_telecom">Twilio Global PBX (Tier 1)</option>
                    <option value="infobip_voice">Infobip Enterprise Voice (Tier 2)</option>
                    <option value="custom_sip">Custom Private SIP VoIP Trunk</option>
                  </select>
                </div>

                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Caller ID Outbound Name</label>
                  <input
                    type="text"
                    value={provider.callerIdName}
                    onChange={(e) => setProvider(p => ({ ...p, callerIdName: e.target.value }))}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-zinc-300 focus:outline-none"
                  />
                </div>

                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1">Caller ID Outbound Line</label>
                  <input
                    type="text"
                    value={provider.callerIdNumber}
                    onChange={(e) => setProvider(p => ({ ...p, callerIdNumber: e.target.value }))}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-zinc-300 focus:outline-none font-mono"
                  />
                </div>

                <div className="pt-2">
                  <span className="text-[10px] text-zinc-500 font-mono block mb-1.5">Voice Engine Profile</span>
                  <div className="grid grid-cols-2 gap-1.5">
                    {[
                      { key: 'neural_assistant', label: 'Neural AI' },
                      { key: 'standard_voip', label: 'VoIP Standard' }
                    ].map(v => (
                      <button
                        key={v.key}
                        onClick={() => setProvider(p => ({ ...p, voiceType: v.key as any }))}
                        className={`text-[10px] font-semibold py-1.5 rounded-lg border text-center transition-all cursor-pointer ${
                          provider.voiceType === v.key || (v.key === 'standard_voip' && provider.voiceType !== 'neural_assistant')
                            ? 'bg-emerald-500/10 border-emerald-500/40 text-emerald-300'
                            : 'bg-zinc-950/40 border-zinc-900 text-zinc-500 hover:border-zinc-900'
                        }`}
                      >
                        {v.label}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Telephone Security Policy Dashboard (Satisfies P2 security rules layout) */}
            <div className="bg-zinc-900/60 border border-zinc-900 rounded-2xl p-5 space-y-4">
              <div className="flex items-center space-x-2 pb-2 border-b border-zinc-900">
                <Sliders className="w-4 h-4 text-emerald-400" />
                <h2 className="text-xs font-bold font-mono tracking-widest text-white uppercase">Authenticating Policies</h2>
              </div>

              <div className="space-y-4 text-xs">
                <div>
                  <label className="text-[10px] text-zinc-500 font-mono block mb-1.5">OOB Verification Posture</label>
                  <select
                    value={policy.requireApprovalMode}
                    onChange={(e) => {
                      const mode = e.target.value as any;
                      setPolicy(p => ({ ...p, requireApprovalMode: mode }));
                      logEvent('TEL_POLICY_UPDATE', `Security verification requirement updated to: ${mode.toUpperCase()}`, 'info');
                    }}
                    className="w-full bg-zinc-950 border border-zinc-900 rounded-lg p-2 text-zinc-300 focus:outline-none focus:border-emerald-500"
                  >
                    <option value="both">Both (IVR Keypad Press [1] + Web Code)</option>
                    <option value="ivr_keypad">IVR Keypad [1] Approved Only</option>
                    <option value="web_otp_only">Spoken Code Entered on Web Only</option>
                  </select>
                </div>

                <div className="space-y-2.5">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] text-zinc-400">Voicemail Auto-Dropper</span>
                    <button
                      onClick={() => setPolicy(p => ({ ...p, enableVoicemailDetection: !p.enableVoicemailDetection }))}
                      className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer ${
                        policy.enableVoicemailDetection ? 'bg-emerald-500' : 'bg-zinc-850'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full bg-white transition-transform ${
                        policy.enableVoicemailDetection ? 'translate-x-4' : 'translate-x-0'
                      }`} />
                    </button>
                  </div>
                  <p className="text-[10px] text-zinc-500 leading-normal">
                    Automatically disconnects lines with incoming greeting tones or voicemail answers to avoid unauthorized automated bypass.
                  </p>
                </div>

                <div className="pt-2 border-t border-zinc-900">
                  <div className="flex items-center justify-between">
                    <span className="text-[11px] text-zinc-400">Escrow Code Recovery</span>
                    <button
                      onClick={() => setPolicy(p => ({ ...p, allowReducedAssuranceRecovery: !p.allowReducedAssuranceRecovery }))}
                      className={`w-9 h-5 rounded-full p-0.5 transition-colors cursor-pointer ${
                        policy.allowReducedAssuranceRecovery ? 'bg-emerald-500' : 'bg-zinc-850'
                      }`}
                    >
                      <div className={`w-4 h-4 rounded-full bg-white transition-transform ${
                        policy.allowReducedAssuranceRecovery ? 'translate-x-4' : 'translate-x-0'
                      }`} />
                    </button>
                  </div>
                  <p className="text-[10px] text-zinc-500 leading-normal mt-1">
                    Allows users with physical hardware issues to execute emergency bypass using a paper recovery token profile.
                  </p>
                </div>

                <div className="space-y-2 border-t border-zinc-900 pt-3">
                  <span className="text-[10px] text-zinc-500 font-mono block">Geographic Dialing Whitelist</span>
                  <div className="flex flex-wrap gap-1.5">
                    {COUNTRIES.slice(0, 6).map(c => (
                      <span key={c.code} className="text-[9px] font-mono font-bold px-2 py-0.5 bg-zinc-950 border border-zinc-900 text-zinc-300 rounded">
                        {c.code} ({c.prefix})
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </div>

            {/* Core Traffic Metrics */}
            <div className="bg-zinc-900/60 border border-zinc-900 rounded-2xl p-5 space-y-3">
              <div className="flex items-center space-x-2 pb-2 border-b border-zinc-900">
                <Activity className="w-4 h-4 text-emerald-400" />
                <h2 className="text-xs font-bold font-mono tracking-widest text-white uppercase">Signaling Performance</h2>
              </div>
              <div className="grid grid-cols-2 gap-3 text-center">
                <div className="bg-zinc-950/60 p-2 border border-zinc-900/50 rounded-xl">
                  <span className="text-[9px] font-mono text-zinc-500 block">COMPLETED</span>
                  <span className="text-xs font-mono font-bold text-white">{stats.completed}</span>
                </div>
                <div className="bg-zinc-950/60 p-2 border border-zinc-900/50 rounded-xl">
                  <span className="text-[9px] font-mono text-zinc-500 block">BUSY/ABAND</span>
                  <span className="text-xs font-mono font-bold text-zinc-400">{stats.busyNoAnswer + stats.abandoned}</span>
                </div>
                <div className="bg-zinc-950/60 p-2 border border-zinc-900/50 rounded-xl">
                  <span className="text-[9px] font-mono text-zinc-500 block">BLOCKED VM</span>
                  <span className="text-xs font-mono font-bold text-amber-400">{stats.voicemailBlocked}</span>
                </div>
                <div className="bg-zinc-950/60 p-2 border border-zinc-900/50 rounded-xl">
                  <span className="text-[9px] font-mono text-zinc-500 block">ROUTE COST</span>
                  <span className="text-xs font-mono font-bold text-emerald-400">${stats.estimatedCost.toFixed(2)}</span>
                </div>
              </div>
            </div>

          </div>
        )}

        {/* Middle Column: Authentication Ceremony Workspace & Enrollment */}
        <div className={`col-span-1 ${showConfig ? 'xl:col-span-5' : 'xl:col-span-8'} flex flex-col space-y-6 max-h-[85vh] overflow-y-auto`}>
          
          {/* AMR Token Banner (Dynamic cryptographic verification badge) */}
          {successAmr && (
            <div className="bg-emerald-500/5 border border-emerald-500/20 rounded-2xl p-5 flex items-start space-x-4 relative overflow-hidden">
              <div className="absolute top-0 right-0 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none"></div>
              
              <div className="w-10 h-10 bg-emerald-500/10 border border-emerald-500/20 rounded-xl flex items-center justify-center shrink-0 text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
              </div>
              <div className="space-y-1.5 flex-1 min-w-0">
                <div className="flex items-center space-x-2">
                  <h4 className="text-sm font-bold text-white tracking-wide">AMR Posture Confirmed: [TEL]</h4>
                  <span className="text-[8px] font-mono font-bold bg-emerald-500 text-slate-950 px-1.5 py-0.5 rounded">AUTHENTICATED</span>
                </div>
                <p className="text-xs text-zinc-400 leading-relaxed">
                  The out-of-band telephone verification handshake has produced active evidence. Identity verified using secure callback networks.
                </p>
                <div className="bg-zinc-950/60 border border-zinc-900 rounded-xl p-3 text-[10px] font-mono text-zinc-400 space-y-1 overflow-x-auto">
                  <div><span className="text-zinc-500">Assertion ID:</span> <span className="text-white">tel_asrt_9f82k398a1</span></div>
                  <div><span className="text-zinc-500">Method Claim:</span> <span className="text-emerald-400 font-bold">"tel" (Telephone AMR)</span></div>
                  <div><span className="text-zinc-500">Timestamp:</span> <span className="text-zinc-300">{successAmr.authenticatedAt}</span></div>
                  <div><span className="text-zinc-500">Audit Status:</span> <span className="text-zinc-300">Verified by Gateway</span></div>
                </div>
              </div>
              <button 
                onClick={() => setSuccessAmr(null)} 
                className="text-zinc-500 hover:text-zinc-300 p-1 rounded hover:bg-zinc-900 cursor-pointer"
              >
                <XSquare className="w-4 h-4" />
              </button>
            </div>
          )}

          {/* Core Multi-tab Workspace Ceremony panel */}
          <div className="bg-zinc-900/40 border border-zinc-900 rounded-2xl flex-1 flex flex-col overflow-hidden min-h-[500px]">
            <AuthCeremony
              enrolledPhones={enrolledPhones}
              setEnrolledPhones={setEnrolledPhones}
              activeCall={activeCall}
              startCall={startCall}
              cancelCall={cancelCall}
              logEvent={logEvent}
              policy={policy}
              provider={provider}
              onSuccessfulAuthentication={onSuccessfulAuthentication}
            />
          </div>
        </div>

        {/* Right Column: Physical Out-of-band Mobile Phone Simulator */}
        <div className="xl:col-span-4 flex flex-col max-h-[85vh] overflow-y-auto">
          <PhoneSimulator
            activeCall={activeCall}
            onAnswerCall={onAnswerCall}
            onDeclineCall={onDeclineCall}
            onKeypadPress={onKeypadPress}
            onIvrSuccess={onIvrSuccess}
            simulateStateOverride={simulateStateOverride}
            setSimulateStateOverride={setSimulateStateOverride}
          />
        </div>

      </main>

      {/* Bottom Section: Scrollable Live Security Operations Audit Log Feed */}
      <section className="border-t border-zinc-900 bg-zinc-950 px-6 py-4 flex-1 flex flex-col min-h-[220px] max-h-[280px]">
        
        {/* Logs Filter Header Toolbar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-3.5 border-b border-zinc-900 gap-3">
          <div className="flex items-center space-x-2">
            <Activity className="w-4 h-4 text-emerald-400" />
            <h3 className="text-xs font-bold font-mono tracking-widest text-white uppercase">Out-of-Band Telemetry Logs</h3>
            <span className="text-[10px] font-mono bg-zinc-900 px-2 py-0.5 text-zinc-400 rounded-md">Live feed</span>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 w-full sm:w-auto">
            {/* Search Input */}
            <input
              type="text"
              placeholder="Filter by keyword..."
              value={logSearchQuery}
              onChange={(e) => setLogSearchQuery(e.target.value)}
              className="bg-zinc-900 border border-zinc-900 rounded-lg px-3 py-1.5 text-xs text-zinc-300 focus:outline-none focus:border-emerald-500 w-full sm:w-48 placeholder-zinc-600"
            />

            {/* Filter Buttons */}
            <div className="flex bg-zinc-900/60 p-0.5 border border-zinc-900 rounded-lg text-[10px] font-mono">
              {[
                { key: 'all', label: 'All' },
                { key: 'success', label: 'Success' },
                { key: 'failure', label: 'Failure' },
                { key: 'warning', label: 'Warning' },
                { key: 'info', label: 'Info' }
              ].map(f => (
                <button
                  key={f.key}
                  onClick={() => setLogFilterStatus(f.key as any)}
                  className={`px-2.5 py-1 rounded transition-colors cursor-pointer ${
                    logFilterStatus === f.key 
                      ? 'bg-zinc-850 text-emerald-400 font-bold' 
                      : 'text-zinc-500 hover:text-zinc-300'
                  }`}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {/* Clear logs */}
            <button
              onClick={() => {
                setLogs([]);
                logEvent('TEL_LOGS_CLEARED', 'Audit console logs cleared by administrator.', 'info');
              }}
              className="p-1.5 text-zinc-500 hover:text-zinc-300 border border-zinc-900 hover:border-zinc-900 rounded-lg cursor-pointer"
              title="Clear telemetry logs"
            >
              <RotateCcw className="w-3.5 h-3.5" />
            </button>
          </div>
        </div>

        {/* Scrollable Audit Trace Feed */}
        <div id="logs-feed" className="flex-1 overflow-y-auto mt-3 space-y-1.5 font-mono text-[11px] pr-2">
          {filteredLogs.length === 0 ? (
            <div className="h-full flex items-center justify-center text-zinc-600 py-6">
              No matching security events logged.
            </div>
          ) : (
            filteredLogs.map(log => (
              <div 
                key={log.id} 
                className="flex items-start space-x-3 py-1 px-2.5 rounded hover:bg-zinc-900/40 border border-transparent hover:border-zinc-900 transition-colors"
              >
                {/* Timestamp */}
                <span className="text-zinc-600 shrink-0 select-none">
                  {new Date(log.timestamp).toLocaleTimeString([], { hour12: false })}
                </span>

                {/* Event Category Badge */}
                <span className={`w-36 font-bold shrink-0 truncate ${
                  log.status === 'success' ? 'text-emerald-400' :
                  log.status === 'failure' ? 'text-red-400' :
                  log.status === 'warning' ? 'text-amber-400' : 'text-blue-400'
                }`}>
                  [{log.eventType}]
                </span>

                {/* Details Text */}
                <span className="text-zinc-300 flex-1 break-all">
                  {log.details}
                </span>

                {/* Destination if present */}
                {log.maskedNumber && (
                  <span className="text-zinc-500 shrink-0 hidden md:inline-block">
                    Line: {log.maskedNumber}
                  </span>
                )}

                {/* IP address of gateway request */}
                <span className="text-zinc-600 shrink-0 text-right font-light hidden lg:inline-block select-all">
                  IP: {log.ipAddress}
                </span>
              </div>
            ))
          )}
        </div>
      </section>

    </div>
  );
}
