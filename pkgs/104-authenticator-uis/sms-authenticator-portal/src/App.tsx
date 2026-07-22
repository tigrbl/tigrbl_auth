import { useState, useEffect } from 'react';
import { SmsPolicy, SmsProvider, SmsLog, AuditLog, Country, EnrolledPhone, SmsCeremonySession } from './types';
import { DEFAULT_COUNTRIES } from './countriesData';
import { CeremonyWizard } from './components/CeremonyWizard';
import { AdminConsole } from './components/AdminConsole';
import { PhoneSimulator } from './components/PhoneSimulator';
import { Shield, Smartphone, ShieldCheck, Activity, Award, CheckCircle2, AlertTriangle, Cpu, Play, RefreshCw, Layers } from 'lucide-react';

export default function App() {
  // Global States
  const [policy, setPolicy] = useState<SmsPolicy>({
    allowedCountries: DEFAULT_COUNTRIES.filter(c => c.isAllowed).map(c => c.code),
    maxAttempts: 3,
    codeExpiryMinutes: 5,
    resendDelaySeconds: 45,
    smsCostLimitMonthly: 500,
    minAssuranceLevel: 'none',
    simChangeBlock: true,
    pumpingProtection: true,
    defaultTemplate: "Your security verification code is {{code}}. It expires in 5 minutes. Do not share this code with anyone.",
  });

  const [providers, setProviders] = useState<SmsProvider[]>([
    { id: 'twilio-t1', name: 'Twilio (Tier-1 Direct)', status: 'active', routingWeight: 50, costPerSms: 0.0075, totalSent: 1240, totalFailed: 2, avgLatencyMs: 110 },
    { id: 'aws-sns', name: 'AWS SNS (Direct Route)', status: 'active', routingWeight: 30, costPerSms: 0.0090, totalSent: 820, totalFailed: 4, avgLatencyMs: 140 },
    { id: 'sinch', name: 'Sinch Global Broker', status: 'active', routingWeight: 20, costPerSms: 0.0480, totalSent: 480, totalFailed: 18, avgLatencyMs: 230 },
    { id: 'infobip', name: 'Infobip Failover', status: 'degraded', routingWeight: 0, costPerSms: 0.0120, totalSent: 150, totalFailed: 3, avgLatencyMs: 180 },
  ]);

  const [countries, setCountries] = useState<Country[]>(DEFAULT_COUNTRIES);

  const [enrolledPhones, setEnrolledPhones] = useState<EnrolledPhone[]>([
    {
      id: 'phone-primary',
      label: 'Corporate SIM (Backup)',
      countryCode: 'US',
      number: '5550194821',
      maskedNumber: '+1 ••• ••• 4821',
      verifiedAt: '2026-07-14T09:12:00Z',
      lastUsedAt: '2026-07-15T10:45:00Z',
      status: 'active',
    }
  ]);

  // Logs & Audits
  const [logs, setLogs] = useState<SmsLog[]>([
    {
      id: 'log-hist-1',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      recipient: '+15550194821',
      maskedRecipient: '+1 ••• ••• 4821',
      code: '821495',
      providerId: 'twilio-t1',
      state: 'delivered',
      latencyMs: 104,
      carrier: 'Twilio-TIGR-US',
      simSwapRisk: 'low',
      isPumpingRisk: false,
      purpose: 'enrollment'
    },
    {
      id: 'log-hist-2',
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      recipient: '+15550194821',
      maskedRecipient: '+1 ••• ••• 4821',
      code: '319402',
      providerId: 'aws-sns',
      state: 'delivered',
      latencyMs: 142,
      carrier: 'AWS-Global-Direct',
      simSwapRisk: 'low',
      isPumpingRisk: false,
      purpose: 'authentication'
    }
  ]);

  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([
    { id: 'audit-1', timestamp: new Date(Date.now() - 3600000).toISOString(), actor: 'System', action: 'AuthGateway Initialized', category: 'provider', details: 'All SMS route providers registered successfully.', severity: 'info' },
    { id: 'audit-2', timestamp: new Date(Date.now() - 1800000).toISOString(), actor: 'Admin (jick.68.0@gmail.com)', action: 'SIM Lock Policy Enabled', category: 'policy', details: 'SIM change detection block rule activated globally.', severity: 'info' },
    { id: 'audit-3', timestamp: new Date(Date.now() - 900000).toISOString(), actor: 'System', action: 'Authenticator Registered', category: 'enrollment', details: 'Phone authenticator bound to target account.', severity: 'info' },
  ]);

  // Session & Emulator States
  const [currentSession, setCurrentSession] = useState<SmsCeremonySession | null>(null);
  const [simSwapRisk, setSimSwapRisk] = useState<'low' | 'medium' | 'high'>('low');
  const [networkCondition, setNetworkCondition] = useState<'good' | 'congested' | 'outage'>('good');

  // Trigger countdown timers
  useEffect(() => {
    const timer = setInterval(() => {
      if (currentSession) {
        setCurrentSession(prev => {
          if (!prev) return null;
          if (prev.state !== 'otp_waiting') return prev;
          
          const nextResend = prev.resendCountdown > 0 ? prev.resendCountdown - 1 : 0;
          const nextExpiry = prev.expiryCountdown > 0 ? prev.expiryCountdown - 1 : 0;

          // If expired completely
          if (nextExpiry === 0 && prev.expiryCountdown > 0) {
            addAuditLog('System', 'OTP Expired', 'authentication', `Challenge code session ${prev.id} expired.`, 'warning');
            return {
              ...prev,
              resendCountdown: nextResend,
              expiryCountdown: 0,
              subState: 'expired'
            };
          }

          return {
            ...prev,
            resendCountdown: nextResend,
            expiryCountdown: nextExpiry
          };
        });
      }
    }, 1000);

    return () => clearInterval(timer);
  }, [currentSession]);

  // Helper to append audits
  const addAuditLog = (
    actor: string,
    action: string,
    category: AuditLog['category'],
    details: string,
    severity: AuditLog['severity'] = 'info'
  ) => {
    const newAudit: AuditLog = {
      id: `audit-${Date.now()}-${Math.random().toString(36).substr(2, 4)}`,
      timestamp: new Date().toISOString(),
      actor,
      action,
      category,
      details,
      severity,
    };
    setAuditLogs(prev => [...prev, newAudit]);
  };

  // Helper to mask numbers
  const maskNumber = (dial: string, raw: string) => {
    const digits = raw.replace(/\D/g, '');
    const last4 = digits.slice(-4) || 'xxxx';
    return `${dial} ••• ••• ${last4}`;
  };

  // Start ceremonies
  const startEnrollment = () => {
    setCurrentSession({
      id: `session-enr-${Date.now()}`,
      type: 'enroll',
      phoneNumber: '',
      countryCode: '',
      dialCode: '',
      maskedNumber: '',
      state: 'introduction',
      subState: 'ready',
      generatedCode: '',
      attemptsCount: 0,
      resendCountdown: 0,
      expiryCountdown: 0,
      providerId: '',
      purpose: 'enrollment',
    });
    addAuditLog('User', 'Enrollment Ceremony Initialized', 'enrollment', 'Subject requested new first-party phone enrollment.');
  };

  const startLogin = () => {
    setCurrentSession({
      id: `session-log-${Date.now()}`,
      type: 'login',
      phoneNumber: '',
      countryCode: '',
      dialCode: '',
      maskedNumber: '',
      state: 'introduction',
      subState: 'ready',
      generatedCode: '',
      attemptsCount: 0,
      resendCountdown: 0,
      expiryCountdown: 0,
      providerId: '',
      purpose: 'authentication',
    });
    addAuditLog('User', 'Login Ceremony Initialized', 'authentication', 'Subject requested SMS MFA challenge login.');
  };

  const startStepUp = () => {
    setCurrentSession({
      id: `session-step-${Date.now()}`,
      type: 'step-up',
      phoneNumber: '',
      countryCode: '',
      dialCode: '',
      maskedNumber: '',
      state: 'introduction',
      subState: 'ready',
      generatedCode: '',
      attemptsCount: 0,
      resendCountdown: 0,
      expiryCountdown: 0,
      providerId: '',
      purpose: 'step-up',
    });
    addAuditLog('User', 'Step-Up Ceremony Initialized', 'authentication', 'Administrative action triggered fresh step-up challenge.');
  };

  const startReplacement = (phoneId: string) => {
    const p = enrolledPhones.find(x => x.id === phoneId);
    if (!p) return;
    setCurrentSession({
      id: `session-rep-${Date.now()}`,
      type: 'replace',
      phoneNumber: p.number,
      countryCode: p.countryCode,
      dialCode: '',
      maskedNumber: p.maskedNumber,
      state: 'introduction',
      subState: 'ready',
      generatedCode: '',
      attemptsCount: 0,
      resendCountdown: 0,
      expiryCountdown: 0,
      providerId: '',
      purpose: 'enrollment',
      label: p.label, // keep track of label to overwrite
    });
    addAuditLog('User', 'Replacement Ceremony Initialized', 'enrollment', `Request to replace authenticator ${p.label}.`);
  };

  const startRecovery = () => {
    setCurrentSession({
      id: `session-rec-${Date.now()}`,
      type: 'recovery',
      phoneNumber: '',
      countryCode: '',
      dialCode: '',
      maskedNumber: '',
      state: 'introduction',
      subState: 'ready',
      generatedCode: '',
      attemptsCount: 0,
      resendCountdown: 0,
      expiryCountdown: 0,
      providerId: '',
      purpose: 'recovery',
    });
    addAuditLog('User', 'Recovery Ceremony Initialized', 'authentication', 'Account recovery initiated via SMS channel.', 'warning');
  };

  const cancelSession = () => {
    setCurrentSession(null);
    addAuditLog('User', 'Ceremony Aborted', 'authentication', 'Active authentication ceremony cancelled by client.');
  };

  const deletePhone = (id: string) => {
    const p = enrolledPhones.find(x => x.id === id);
    if (!p) return;
    setEnrolledPhones(prev => prev.filter(x => x.id !== id));
    addAuditLog('User', 'Phone Authenticator Removed', 'enrollment', `Removed authenticator ${p.label} (${p.maskedNumber}).`, 'warning');
  };

  // Submission of phone digits
  const submitPhoneNumber = (countryCode: string, dialCode: string, rawNumber: string) => {
    if (!currentSession) return;

    // If enrolling/replacing, use newly entered digits
    if (currentSession.type === 'enroll' || currentSession.type === 'replace' || currentSession.type === 'recovery') {
      const masked = maskNumber(dialCode, rawNumber);
      setCurrentSession(prev => prev ? {
        ...prev,
        phoneNumber: rawNumber,
        countryCode,
        dialCode,
        maskedNumber: masked,
        state: 'send_pending',
        subState: 'ready',
      } : null);
      addAuditLog('User', 'Destination Entered', 'enrollment', `Phone destination normalized: ${masked}.`);
    } else {
      // Login or step-up using existing phone
      const p = enrolledPhones.find(x => x.number === rawNumber);
      if (p) {
        setCurrentSession(prev => prev ? {
          ...prev,
          phoneNumber: p.number,
          countryCode: p.countryCode,
          maskedNumber: p.maskedNumber,
          state: 'send_pending',
          subState: 'ready',
        } : null);
        addAuditLog('User', 'Authenticator Selected', 'authentication', `Selected destination for MFA challenge dispatch: ${p.maskedNumber}.`);
      }
    }
  };

  // Dispatch SMS verification code
  const sendCode = () => {
    if (!currentSession) return;

    const targetCountry = countries.find(c => c.code === currentSession.countryCode);
    
    // 1. Check Policy Block for Restricted Country
    if (targetCountry && !targetCountry.isAllowed) {
      addAuditLog('System', 'Policy Block Triggered', 'policy', `SMS dispatch to restricted region ${currentSession.countryCode} halted.`, 'critical');
      setCurrentSession(prev => prev ? { ...prev, state: 'failed', subState: 'blocked' } : null);
      return;
    }

    // 2. Check Carrier SIM Swap block
    if (simSwapRisk === 'high' && policy.simChangeBlock) {
      addAuditLog('System', 'Carrier Abuse Block', 'abuse', `IMSI SIM-swap activity detected. Halted challenge credentials for ${currentSession.maskedNumber}.`, 'critical');
      
      const failedLog: SmsLog = {
        id: `log-${Date.now()}`,
        timestamp: new Date().toISOString(),
        recipient: currentSession.phoneNumber,
        maskedRecipient: currentSession.maskedNumber,
        code: '••••••',
        providerId: 'REJECTED-IMSI',
        state: 'failed',
        latencyMs: 0,
        carrier: 'Twilio-TIGR',
        simSwapRisk: 'high',
        isPumpingRisk: false,
        purpose: currentSession.purpose,
      };
      setLogs(prev => [failedLog, ...prev]);
      setCurrentSession(prev => prev ? { ...prev, state: 'failed', subState: 'blocked' } : null);
      return;
    }

    // 3. Provider routing selector with Failover logic
    // We look for active provider with highest weight
    let activeProvList = providers.filter(p => p.status === 'active');
    
    // Simulate Outage: If networkCondition is set to 'outage', Twilio status is treated as offline internally, triggering failover
    if (networkCondition === 'outage') {
      activeProvList = activeProvList.filter(p => p.id !== 'twilio-t1');
      addAuditLog('System', 'Provider Failover Triggered', 'provider', `Outage reported on Twilio (Tier-1 Gateway). Re-routing fallback traffic to AWS SNS.`, 'warning');
    }

    if (activeProvList.length === 0) {
      // All fallback networks exhausted
      addAuditLog('System', 'Provider Exhaustion', 'provider', 'All carrier gateways offline. Delivery failed.', 'critical');
      setCurrentSession(prev => prev ? { ...prev, state: 'failed', subState: 'failed' } : null);
      return;
    }

    // Sort by weight descending
    activeProvList.sort((a, b) => b.routingWeight - a.routingWeight);
    const selectedProvider = activeProvList[0];

    // Generate random 6-digit challenge code
    const generatedOTP = Math.floor(100000 + Math.random() * 900000).toString();

    // Premium pumping protections check
    const isPumpingDetected = policy.pumpingProtection && targetCountry && targetCountry.costPerSms > 0.15;
    if (isPumpingDetected) {
      addAuditLog('System', 'Pumping Protection Active', 'abuse', `Toll pumping signature detected for region ${currentSession.countryCode}. Enforcing strict IP velocity controls.`, 'warning');
    }

    // Create Initial Log (starting as queued)
    const logId = `log-${Date.now()}`;
    const newLog: SmsLog = {
      id: logId,
      timestamp: new Date().toISOString(),
      recipient: currentSession.phoneNumber || '1234567',
      maskedRecipient: currentSession.maskedNumber,
      code: generatedOTP,
      providerId: selectedProvider.id,
      state: 'queued',
      latencyMs: selectedProvider.avgLatencyMs + Math.floor(Math.random() * 30),
      carrier: selectedProvider.id === 'twilio-t1' ? 'Twilio-TIGR-US' : 'AWS-Global-Direct',
      simSwapRisk,
      isPumpingRisk: !!isPumpingDetected,
      purpose: currentSession.purpose,
    };

    setLogs(prev => [newLog, ...prev]);

    // Update session state
    setCurrentSession(prev => prev ? {
      ...prev,
      state: 'otp_waiting',
      subState: 'queued',
      generatedCode: generatedOTP,
      providerId: selectedProvider.id,
      resendCountdown: policy.resendDelaySeconds,
      expiryCountdown: policy.codeExpiryMinutes * 60,
    } : null);

    addAuditLog('System', 'OTP Dispatched', 'authentication', `Challenge code dispatched via ${selectedProvider.name} to ${currentSession.maskedNumber}.`);

    // Simulate carrier tower delivery hook after 1.5 seconds
    setTimeout(() => {
      setLogs(prevLogs =>
        prevLogs.map(l => {
          if (l.id === logId) {
            const nextState = networkCondition === 'congested' ? 'delayed' : 'delivered';
            
            // Sync session subState
            setCurrentSession(session => {
              if (session && session.state === 'otp_waiting') {
                return { ...session, subState: nextState === 'delayed' ? 'delayed' : 'delivered' };
              }
              return session;
            });

            if (nextState === 'delayed') {
              addAuditLog('System', 'Carrier Delivery Delayed', 'provider', `Delivery receipt slow. Congestion warning flagged for log ${logId}.`, 'warning');
            } else {
              addAuditLog('System', 'Carrier Delivery Receipt', 'provider', `Tower receipt acknowledged for log ${logId}.`);
            }

            return { ...l, state: nextState };
          }
          return l;
        })
      );
    }, 1500);
  };

  // OTP Verification Submission
  const verifyCode = (code: string) => {
    if (!currentSession) return;

    if (code === currentSession.generatedCode) {
      // MATCH SUCCESS
      setCurrentSession(prev => prev ? {
        ...prev,
        state: 'completed',
        subState: 'delivered',
      } : null);

      addAuditLog('System', 'OTP Verification Success', 'authentication', `Subject successfully matched challenge for ${currentSession.maskedNumber}. Cryptographic verification evidence issued.`);
      
      // Update lastUsed date of existing phone if match is from active authenticator
      if (currentSession.type === 'login' || currentSession.type === 'step-up') {
        setEnrolledPhones(prev =>
          prev.map(p => p.number === currentSession.phoneNumber ? { ...p, lastUsedAt: new Date().toISOString() } : p)
        );
      }
    } else {
      // MISMATCH
      const nextAttempts = currentSession.attemptsCount + 1;
      
      addAuditLog('System', 'OTP Verification Failed', 'authentication', `Incorrect code submitted (${code}) for ${currentSession.maskedNumber}. Attempt ${nextAttempts} of ${policy.maxAttempts}.`, 'warning');

      if (nextAttempts >= policy.maxAttempts) {
        // Locks down session
        setCurrentSession(prev => prev ? {
          ...prev,
          attemptsCount: nextAttempts,
          state: 'failed',
          subState: 'rate-limited'
        } : null);
        addAuditLog('System', 'Security Lockdown Triggered', 'abuse', `Verification bounds exceeded for ${currentSession.maskedNumber}. Ceremony terminated to protect credentials.`, 'critical');
      } else {
        setCurrentSession(prev => prev ? {
          ...prev,
          attemptsCount: nextAttempts,
        } : null);
      }
    }
  };

  // Complete Enrollment & name authenticator
  const saveEnrollment = (label: string) => {
    if (!currentSession) return;

    const newAuth: EnrolledPhone = {
      id: `phone-${Date.now()}`,
      label: label || 'My Personal SIM',
      countryCode: currentSession.countryCode,
      number: currentSession.phoneNumber,
      maskedNumber: currentSession.maskedNumber,
      verifiedAt: new Date().toISOString(),
      lastUsedAt: new Date().toISOString(),
      status: 'active',
    };

    // If it was a replacement, remove the old one first
    if (currentSession.type === 'replace') {
      setEnrolledPhones(prev => prev.filter(p => p.number !== currentSession.phoneNumber));
    }

    setEnrolledPhones(prev => [...prev, newAuth]);
    setCurrentSession(null);
    addAuditLog('User', 'Phone Authenticator Registered', 'enrollment', `Authenticator '${newAuth.label}' successfully activated and added to profile.`);
  };

  const copyCodeToClipboard = (code: string) => {
    navigator.clipboard.writeText(code);
    addAuditLog('Client', 'OTP Copied', 'authentication', 'One-time passcode copied from virtual phone container.');
  };

  const clearLogHistory = () => {
    setLogs([]);
    addAuditLog('Admin', 'Logs Purged', 'provider', 'Delivery logs and carrier telemetry cleared by administrator.', 'warning');
  };

  // SCENARIO SHORTCUTS FOR IMMEDIATE TESTING
  const loadScenario = (type: 'fresh' | 'sim' | 'delay' | 'outage') => {
    // Stop existing session
    setCurrentSession(null);

    if (type === 'fresh') {
      setEnrolledPhones([]);
      setSimSwapRisk('low');
      setNetworkCondition('good');
      addAuditLog('Admin', 'Scenario Loaded', 'policy', 'Scenario Loaded: Fresh Slate Enrollment.');
      // Auto trigger first step
      setTimeout(() => startEnrollment(), 200);
    } else if (type === 'sim') {
      setSimSwapRisk('high');
      setNetworkCondition('good');
      addAuditLog('Admin', 'Scenario Loaded', 'policy', 'Scenario Loaded: High Risk SIM-Swap Defense.');
      // Ensure corporate SIM is enrolled
      if (enrolledPhones.length === 0) {
        setEnrolledPhones([{ id: 'phone-primary', label: 'Corporate SIM (Backup)', countryCode: 'US', number: '5550194821', maskedNumber: '+1 ••• ••• 4821', verifiedAt: new Date().toISOString(), lastUsedAt: new Date().toISOString(), status: 'active' }]);
      }
      setTimeout(() => startLogin(), 200);
    } else if (type === 'delay') {
      setSimSwapRisk('low');
      setNetworkCondition('congested');
      addAuditLog('Admin', 'Scenario Loaded', 'policy', 'Scenario Loaded: Congested Network Delivery Delay.');
      if (enrolledPhones.length === 0) {
        setEnrolledPhones([{ id: 'phone-primary', label: 'Corporate SIM (Backup)', countryCode: 'US', number: '5550194821', maskedNumber: '+1 ••• ••• 4821', verifiedAt: new Date().toISOString(), lastUsedAt: new Date().toISOString(), status: 'active' }]);
      }
      setTimeout(() => startLogin(), 200);
    } else if (type === 'outage') {
      setSimSwapRisk('low');
      setNetworkCondition('outage');
      // Set Twilio Offline
      setProviders(prev => prev.map(p => p.id === 'twilio-t1' ? { ...p, status: 'offline' } : p));
      addAuditLog('Admin', 'Scenario Loaded', 'policy', 'Scenario Loaded: Carrier Gateway Outage & Failover.');
      if (enrolledPhones.length === 0) {
        setEnrolledPhones([{ id: 'phone-primary', label: 'Corporate SIM (Backup)', countryCode: 'US', number: '5550194821', maskedNumber: '+1 ••• ••• 4821', verifiedAt: new Date().toISOString(), lastUsedAt: new Date().toISOString(), status: 'active' }]);
      }
      setTimeout(() => startLogin(), 200);
    }
  };

  return (
    <div className="min-h-screen bg-[#080c14] text-slate-100 flex flex-col justify-between font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      
      {/* Dynamic Header */}
      <header className="border-b border-slate-800 bg-[#0c111e]/80 backdrop-blur-md sticky top-0 z-50 px-4 py-3.5">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="w-2.5 h-2.5 rounded-full bg-indigo-500 animate-pulse" />
              <h1 className="text-lg font-bold font-display tracking-tight text-white">AuthGateway SMS Platform</h1>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">
              Comprehensive identity phone enrollment, E.164 normalization, carrier failover routing, and IMSI risk defenses.
            </p>
          </div>

          <div className="flex items-center gap-1.5 bg-slate-900 border border-slate-800 p-1.5 rounded-xl text-xs max-w-full overflow-x-auto">
            <span className="text-[10px] uppercase font-bold text-slate-500 px-2 font-mono">Presets:</span>
            <button
              onClick={() => loadScenario('fresh')}
              className="px-2.5 py-1 rounded-lg bg-slate-800 hover:bg-slate-750 text-slate-200 transition text-[11px] font-semibold whitespace-nowrap"
            >
              Fresh Slate
            </button>
            <button
              onClick={() => loadScenario('sim')}
              className="px-2.5 py-1 rounded-lg bg-rose-950/40 border border-rose-900/30 hover:bg-rose-950/60 text-rose-300 transition text-[11px] font-semibold whitespace-nowrap"
            >
              SIM Swap Attack
            </button>
            <button
              onClick={() => loadScenario('delay')}
              className="px-2.5 py-1 rounded-lg bg-amber-950/40 border border-amber-900/30 hover:bg-amber-950/60 text-amber-300 transition text-[11px] font-semibold whitespace-nowrap"
            >
              Network Delay
            </button>
            <button
              onClick={() => loadScenario('outage')}
              className="px-2.5 py-1 rounded-lg bg-indigo-950/40 border border-indigo-900/30 hover:bg-indigo-950/60 text-indigo-300 transition text-[11px] font-semibold whitespace-nowrap"
            >
              Outage Failover
            </button>
          </div>
        </div>
      </header>

      {/* Main Workspace */}
      <main className="max-w-7xl mx-auto w-full px-4 py-6 flex-1 grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        
        {/* Column 1: P0 User Verification Client Container (35% width equivalent) */}
        <div className="lg:col-span-4 space-y-6">
          <div className="flex justify-between items-center px-1">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Layers className="w-3.5 h-3.5 text-indigo-400" /> Verification Client
            </span>
            <span className="text-[10px] text-slate-500 font-mono">P0/P1 Authenticator</span>
          </div>
          
          <CeremonyWizard
            session={currentSession}
            policy={policy}
            countries={countries}
            enrolledPhones={enrolledPhones}
            logs={logs}
            onStartEnrollment={startEnrollment}
            onStartLogin={startLogin}
            onStartStepUp={startStepUp}
            onStartReplacement={startReplacement}
            onStartRecovery={startRecovery}
            onCancelSession={cancelSession}
            onSubmitPhoneNumber={submitPhoneNumber}
            onSendCode={sendCode}
            onVerifyCode={verifyCode}
            onSaveEnrollment={saveEnrollment}
            onReplacePhone={saveEnrollment}
            onDeletePhone={deletePhone}
            simSwapRisk={simSwapRisk}
            networkCondition={networkCondition}
          />

          {/* Minimal Assurance Warning Banner */}
          <div className="bg-slate-900 border border-slate-850 rounded-2xl p-4 flex gap-3 text-xs text-slate-400">
            <Shield className="w-5 h-5 text-indigo-400 shrink-0 mt-0.5" />
            <div>
              <span className="font-semibold text-slate-200 block">Assure Policy: Low Assurance</span>
              <p className="mt-1 leading-relaxed text-[11px]">
                The SMS channel is treated as low assurance because it lacks FIDO2 phishing resistance. This platform implements IMSI block checking to protect recovery fallback tunnels.
              </p>
            </div>
          </div>
        </div>

        {/* Column 2: Administration, Diagnostics, Policies & Audits (40% width equivalent) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="flex justify-between items-center px-1">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Cpu className="w-3.5 h-3.5 text-indigo-400" /> Platform Admin Terminal
            </span>
            <span className="text-[10px] text-slate-500 font-mono">P2 Operations Console</span>
          </div>

          <AdminConsole
            policy={policy}
            setPolicy={setPolicy}
            providers={providers}
            setProviders={setProviders}
            logs={logs}
            auditLogs={auditLogs}
            countries={countries}
            setCountries={setCountries}
            onClearLogs={clearLogHistory}
          />
        </div>

        {/* Column 3: Physical Device Handset Simulator (25% width equivalent) */}
        <div className="lg:col-span-3 space-y-6">
          <div className="flex justify-between items-center px-1">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider flex items-center gap-1">
              <Smartphone className="w-3.5 h-3.5 text-indigo-400" /> Virtual Handset
            </span>
            <span className="text-[10px] text-slate-500 font-mono">External Receipt</span>
          </div>

          <PhoneSimulator
            logs={logs}
            onCopyCode={copyCodeToClipboard}
            simSwapRisk={simSwapRisk}
            setSimSwapRisk={setSimSwapRisk}
            networkCondition={networkCondition}
            setNetworkCondition={setNetworkCondition}
          />
        </div>

      </main>

      {/* Footer */}
      <footer className="border-t border-slate-900 bg-[#060810] py-4 px-4 text-center text-slate-500 text-[10px] font-mono">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row justify-between items-center gap-2">
          <span>AuthGateway Identity Services © 2026</span>
          <span className="text-indigo-400">Lower Assurance Authentication Channel (SMS AMR)</span>
        </div>
      </footer>

    </div>
  );
}
