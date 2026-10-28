import React, { useState, useEffect } from 'react';
import { 
  Authenticator, 
  AuthenticatorMethod, 
  CeremonyStep, 
  Policy, 
  ProviderHealth, 
  AuditEvent, 
  CeremonySession 
} from './types';
import { ChannelProviderHealthGrid } from './components/HealthDashboard';
import { DiagnosticsTimeline } from './components/DiagnosticsTimeline';
import { ExternalApprovalWait } from './components/ExternalApprovalWait';
import { ChannelFallbackComparison } from './components/ChannelFallbackComparison';
import { IndependenceEvidenceSummary } from './components/IndependenceEvidenceSummary';
import { 
  Shield, 
  Settings, 
  Key, 
  Activity, 
  Terminal, 
  Clock, 
  Smartphone, 
  Mail, 
  Phone, 
  AlertTriangle, 
  CheckCircle2, 
  HelpCircle, 
  Plus, 
  Check, 
  User, 
  RefreshCw, 
  Wifi, 
  Lock, 
  Sliders, 
  ArrowRight,
  Sparkles
} from 'lucide-react';

export default function App() {
  // --- STATE SEEDING ---
  const initialAuthenticators: Authenticator[] = [
    { id: 'auth-1', type: 'sms', label: 'Personal Mobile Cellular', destination: '+1 (•••) •••-4821', enrolled: true, independentGroup: 'Telecom Network' },
    { id: 'auth-2', type: 'email', label: 'Corporate Mail Gateway', destination: 'ad•••@corporate.internal', enrolled: true, independentGroup: 'Cloud Web Infrastructure' },
    { id: 'auth-3', type: 'totp', label: 'Hardware-Bound Google Authenticator', destination: 'TOTP Client Profile', enrolled: true, independentGroup: 'HMAC Application State' },
    { id: 'auth-4', type: 'push', label: 'Corporate Managed Phone', destination: 'iPhone 15 Pro Max', enrolled: true, independentGroup: 'Second-Device Secure App' },
    { id: 'auth-5', type: 'passkey', label: 'MacBook TouchID WebAuthn', destination: 'Secure Enclave Biometric', enrolled: false, independentGroup: 'Cryptographic Security Key' },
    { id: 'auth-6', type: 'voice', label: 'Office Landline Call', destination: '+1 (•••) •••-9210', enrolled: true, independentGroup: 'Telecom Network' }
  ];

  const initialPolicy: Policy = {
    id: 'pol-default',
    name: 'High Assurance Multi-Channel Policy',
    requiredIndependentChannels: 2,
    allowedCombinations: [
      ['totp', 'push'],
      ['totp', 'sms'],
      ['passkey', 'sms'],
      ['passkey', 'email'],
      ['push', 'email']
    ],
    sequenceOrder: 'strict',
    tokenExpirySeconds: 60,
    allowFallback: true,
    fallbackCombination: ['sms', 'email']
  };

  const initialProviders: ProviderHealth[] = [
    { id: 'prov-sms', name: 'Twilio Cellular Gateway', type: 'sms', status: 'operational', latencyMs: 120, reliability: 99.8 },
    { id: 'prov-email', name: 'SendGrid SMTP Service', type: 'email', status: 'operational', latencyMs: 78, reliability: 99.9 },
    { id: 'prov-totp', name: 'WebAuthn Local Sync Engine', type: 'totp', status: 'operational', latencyMs: 15, reliability: 100 },
    { id: 'prov-push', name: 'Apple APNS & Firebase Push', type: 'push', status: 'operational', latencyMs: 195, reliability: 99.4 },
    { id: 'prov-passkey', name: 'Local TPM/Security Key Provider', type: 'passkey', status: 'operational', latencyMs: 10, reliability: 100 },
    { id: 'prov-voice', name: 'Interactive Voice Relay', type: 'voice', status: 'operational', latencyMs: 310, reliability: 98.2 }
  ];

  const initialSession: CeremonySession = {
    id: 'sess_corr_8b91fa02',
    subject: 'admin@corporate.internal',
    tenantId: 'tenant_9a8f2_prod',
    ipAddress: '198.51.100.45',
    deviceOs: 'macOS Sonoma (Arc Browser)',
    location: 'San Jose, CA',
    amrEmitted: [],
    mcaAchieved: false
  };

  const [activeTab, setActiveTab] = useState<'ceremony' | 'enrollment' | 'policy'>('ceremony');
  const [authenticators, setAuthenticators] = useState<Authenticator[]>(initialAuthenticators);
  const [policy, setPolicy] = useState<Policy>(initialPolicy);
  const [providers, setProviders] = useState<ProviderHealth[]>(initialProviders);
  const [session, setSession] = useState<CeremonySession>(initialSession);
  const [events, setEvents] = useState<AuditEvent[]>([]);

  // --- CEREMONY WORKFLOW STATE ---
  const [ceremonyState, setCeremonyState] = useState<'idle' | 'introduction' | 'method_selection' | 'step_active' | 'oob_waiting' | 'success' | 'failed'>('idle');
  const [ceremonySteps, setCeremonySteps] = useState<CeremonyStep[]>([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(0);
  const [otpValue, setOtpValue] = useState('');
  const [otpError, setOtpError] = useState('');
  const [oobResendCooldown, setOobResendCooldown] = useState(0);
  const [simulatedCarrierCompromise, setSimulatedCarrierCompromise] = useState(false);

  // --- ADD LOG HELPER ---
  const logEvent = (level: AuditEvent['level'], category: AuditEvent['category'], message: string, details?: any) => {
    const newEvent: AuditEvent = {
      id: `evt_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      level,
      category,
      message,
      ceremonyId: session.id,
      details
    };
    setEvents((prev) => [newEvent, ...prev]);
  };

  // Seed initial audit events
  useEffect(() => {
    logEvent('info', 'orchestration', 'Authentication server initialized security tenant workspace.', { tenantId: session.tenantId, clientIp: session.ipAddress });
    logEvent('info', 'policy', `Security policy loaded: "${initialPolicy.name}". Required channels: ${initialPolicy.requiredIndependentChannels}.`, initialPolicy);
    logEvent('info', 'enrollment', 'Scanned enrolled credentials for subject.', { enrolledCount: initialAuthenticators.filter(a => a.enrolled).length });
  }, []);

  // Countdown timer for resend cooldown
  useEffect(() => {
    if (oobResendCooldown > 0) {
      const timer = setTimeout(() => setOobResendCooldown((p) => p - 1), 1000);
      return () => clearTimeout(timer);
    }
  }, [oobResendCooldown]);

  // --- PROVIDER TOGGLE SIMULATION ---
  const handleToggleProvider = (id: string) => {
    setProviders((prev) => prev.map((prov) => {
      if (prov.id === id) {
        let nextStatus: ProviderHealth['status'] = 'operational';
        let latency = 50;
        let rel = 100;

        if (prov.status === 'operational') {
          nextStatus = 'degraded';
          latency = 480;
          rel = 81.5;
        } else if (prov.status === 'degraded') {
          nextStatus = 'outage';
          latency = 0;
          rel = 0;
        }

        logEvent(
          nextStatus === 'operational' ? 'success' : nextStatus === 'degraded' ? 'warn' : 'error',
          'provider',
          `Provider "${prov.name}" status updated to ${nextStatus.toUpperCase()}.`,
          { id, type: prov.type, nextStatus, latencyMs: latency, reliability: rel }
        );

        return { ...prov, status: nextStatus, latencyMs: latency, reliability: rel };
      }
      return prov;
    }));
  };

  // --- INITIATE AUTHENTICATION CEREMONY ---
  const handleStartCeremony = () => {
    // 1. Evaluate if current policy allows starting
    logEvent('info', 'orchestration', 'Subject initiated authentication ceremony. Evaluating policy and enrolled channels...');

    const enrolledMethods = authenticators.filter(a => a.enrolled).map(a => a.type);
    
    // Find eligible paths that use ENROLLED and OPERATIONAL methods
    const activeOperationalMethods = enrolledMethods.filter(m => {
      const prov = providers.find(p => p.type === m);
      return prov && prov.status !== 'outage';
    });

    logEvent('info', 'policy', 'Checking enrollment coverage against combination configurations.', {
      enrolled: enrolledMethods,
      operational: activeOperationalMethods
    });

    // Generate steps dynamically based on policy requirements
    const steps: CeremonyStep[] = [
      {
        id: 'step-1',
        title: 'Primary Verification Step',
        description: 'Verify identity using a strong hardware-bound key or local authenticator application.',
        allowedMethods: ['totp', 'passkey'],
        selectedMethod: null,
        status: 'current',
        progressText: 'Awaiting primary credential selection',
        completedAt: null,
        providerId: 'prov-totp'
      },
      {
        id: 'step-2',
        title: 'Secondary Channel Verification',
        description: 'Verify identity via disjoint physical network (e.g. mobile push or cellular OTP).',
        allowedMethods: ['push', 'sms', 'email'],
        selectedMethod: null,
        status: 'waiting',
        progressText: 'Awaiting primary step verification',
        completedAt: null,
        providerId: 'prov-push'
      }
    ];

    setCeremonySteps(steps);
    setCurrentStepIndex(0);
    setCeremonyState('introduction');
    setOtpValue('');
    setOtpError('');
    
    logEvent('success', 'orchestration', 'Ceremony loaded. Presenting Multi-Channel Authentication required steps to user.');
  };

  // --- USER ACCEPTED INTRODUCTION / SELECTS METHOD ---
  const handleAcceptIntroduction = () => {
    setCeremonyState('method_selection');
    logEvent('info', 'orchestration', 'User reviewed policy requirements. Advancing to channel chooser.');
  };

  // --- METHOD CHOSEN FOR CURRENT STEP ---
  const handleSelectMethod = (method: AuthenticatorMethod) => {
    const updatedSteps = [...ceremonySteps];
    const currentStep = updatedSteps[currentStepIndex];
    currentStep.selectedMethod = method;
    currentStep.status = 'current';

    // Map method to provider ID
    const providerMap: Record<AuthenticatorMethod, string> = {
      sms: 'prov-sms',
      email: 'prov-email',
      totp: 'prov-totp',
      push: 'prov-push',
      passkey: 'prov-passkey',
      voice: 'prov-voice',
      smartcard: 'prov-passkey'
    };
    currentStep.providerId = providerMap[method];

    setCeremonySteps(updatedSteps);

    // Double-check if provider has outage or latency
    const targetProvider = providers.find(p => p.type === method);
    if (targetProvider && targetProvider.status === 'outage') {
      logEvent('error', 'provider', `User selected channel "${method}" but the provider "${targetProvider.name}" is currently reporting an outage.`, targetProvider);
      setOtpError(`The ${targetProvider.name} is currently offline. Please choose a different independent channel.`);
      return;
    }

    setOtpError('');
    logEvent('info', 'orchestration', `User selected verification method: ${method.toUpperCase()} for Step ${currentStepIndex + 1}.`, {
      stepId: currentStep.id,
      selectedMethod: method,
      provider: targetProvider?.name
    });

    if (method === 'push' || method === 'voice') {
      setCeremonyState('oob_waiting');
      logEvent('info', 'orchestration', `Initiating out-of-band correlation polling loop for method: ${method.toUpperCase()}`);
    } else {
      setCeremonyState('step_active');
    }
  };

  // --- SIMULATE SMS/EMAIL/TOTP CODE VERIFICATION ---
  const handleVerifyOtp = () => {
    setOtpError('');
    const currentStep = ceremonySteps[currentStepIndex];
    const selected = currentStep.selectedMethod;

    if (!otpValue || otpValue.length < 4) {
      setOtpError('Please enter a valid verification code.');
      return;
    }

    // Simulate provider latency impact
    const targetProvider = providers.find(p => p.type === selected);
    if (targetProvider && targetProvider.status === 'degraded') {
      logEvent('warn', 'provider', `Provider latency check: "${targetProvider.name}" latency is ${targetProvider.latencyMs}ms. Processing will feel sluggish.`, targetProvider);
    }

    // Server-side check simulation
    logEvent('info', 'orchestration', `Submitting evidence token code [${otpValue}] to server verification endpoint...`);

    // In simulation, code "0000" or simple mock values are accepted, but let's accept anything except invalid entries
    if (otpValue === '9999' || otpValue.toLowerCase() === 'fail') {
      setOtpError('Security verification failed. Invalid challenge token or expired signature.');
      logEvent('error', 'orchestration', `Verification endpoint rejected challenge for channel: ${selected?.toUpperCase()}. Invalid payload signature.`);
      return;
    }

    // Check if independence is compromised by simulating carrier trunk intercepts
    if (simulatedCarrierCompromise && selected === 'sms') {
      setOtpError('Channel intercepted! SIM-Swap / cellular compromise detected on SMS carrier trunks.');
      logEvent('error', 'orchestration', 'CRITICAL SECURITY INCIDENT: Cell tower routing mismatch. Cryptographic verification rejected due to destination spoofing risk.', { method: 'sms' });
      return;
    }

    // Complete Step successfully
    completeStep(currentStepIndex);
  };

  // --- PASSKEY BIOMETRIC SIMULATOR TRIGGER ---
  const handlePasskeyTrigger = () => {
    setOtpError('');
    const currentStep = ceremonySteps[currentStepIndex];
    
    logEvent('info', 'orchestration', 'Invoking browser-level WebAuthn navigator.credentials.get()...');
    
    setTimeout(() => {
      logEvent('success', 'orchestration', 'Cryptographic hardware challenge generated and signed by Secure Enclave.', {
        algorithm: 'RS256',
        rpId: 'corporate.internal',
        credentialId: 'c2VjdXJlX2VuY2xhdmVfY3JlZF9pZA=='
      });
      completeStep(currentStepIndex);
    }, 1000);
  };

  // --- OUT OF BAND (OOB) SIMULATED EVENTS ---
  const handleOobApprove = () => {
    logEvent('success', 'orchestration', `Callback webhook received: Positive approval signed on secondary OOB device for step ${currentStepIndex + 1}.`);
    completeStep(currentStepIndex);
  };

  const handleOobReject = (reason: string) => {
    setOtpError(`OOB channel rejected: ${reason}`);
    setCeremonyState('step_active');
    logEvent('error', 'orchestration', `OOB callback reported rejection or failure: ${reason}`);
  };

  const handleOobCancel = () => {
    setCeremonyState('method_selection');
    logEvent('warn', 'orchestration', 'User cancelled out-of-band polling. Returning to method chooser.');
  };

  const handleOobResend = () => {
    setOobResendCooldown(15);
    logEvent('info', 'provider', `Resending notification payload to target destination device...`, { cooldownActive: true });
  };

  // --- HELPER TO COMPLETE STEP AND ADVANCE ---
  const completeStep = (index: number) => {
    const updatedSteps = [...ceremonySteps];
    const currentStep = updatedSteps[index];

    currentStep.status = 'completed';
    currentStep.completedAt = new Date().toISOString();
    currentStep.progressText = `Verified via ${currentStep.selectedMethod?.toUpperCase()} at ${new Date().toLocaleTimeString([], { hour12: false })}`;

    setCeremonySteps(updatedSteps);
    setOtpValue('');
    setOtpError('');

    logEvent('success', 'orchestration', `Step ${index + 1} ("${currentStep.title}") successfully completed. Independent evidence recorded server-side.`);

    const nextIndex = index + 1;
    if (nextIndex < updatedSteps.length) {
      // Advance to next step
      setCurrentStepIndex(nextIndex);
      const nextStep = updatedSteps[nextIndex];
      nextStep.status = 'current';
      nextStep.progressText = 'Awaiting method selection';
      setCeremonyState('method_selection');
      logEvent('info', 'orchestration', `Advancing ceremony to Step ${nextIndex + 1}: "${nextStep.title}".`);
    } else {
      // All steps completed! Evaluate overall MCA Independence
      evaluateCeremonyIndependence(updatedSteps);
    }
  };

  // --- CEREMONY EVALUATOR (CRITICAL PART OF THE MANDATE) ---
  const evaluateCeremonyIndependence = (completedSteps: CeremonyStep[]) => {
    logEvent('info', 'policy', 'Ceremony steps concluded. Initiating cryptographic Independence and Combination Evaluator...');

    const usedMethods = completedSteps.map(s => s.selectedMethod as AuthenticatorMethod);
    
    // Check if we have duplicate methods on same underlying channels (e.g. SMS and Voice)
    const hasSms = usedMethods.includes('sms');
    const hasVoice = usedMethods.includes('voice');

    // If both are used, they belong to the same 'Telecom Network' independent group
    let validatedGroups = new Set<string>();
    usedMethods.forEach(m => {
      const auth = authenticators.find(a => a.type === m);
      if (auth) {
        validatedGroups.add(auth.independentGroup);
      }
    });

    logEvent('info', 'policy', 'Disjoint groups extracted from completed evidence:', Array.from(validatedGroups));

    if (validatedGroups.size < policy.requiredIndependentChannels) {
      logEvent('error', 'policy', `CRITICAL COMBINATION FAILURE: Completed channels do not satisfy the minimum required independent channels of ${policy.requiredIndependentChannels}. Required: ${policy.requiredIndependentChannels}, Achieved: ${validatedGroups.size}.`, {
        usedMethods,
        validatedGroups: Array.from(validatedGroups)
      });
      setCeremonyState('failed');
      return;
    }

    // Success state
    setSession(prev => ({
      ...prev,
      mcaAchieved: true,
      amrEmitted: ['mca', ...usedMethods]
    }));
    setCeremonyState('success');
    logEvent('success', 'policy', 'MCA VERIFIED. Emitting server-signed JWT auth metadata assertion with "mca" claim successfully.', {
      emittedAmr: ['mca', ...usedMethods],
      provenance: 'first-party-mca-assertion-signed'
    });
  };

  const handleResetCeremony = () => {
    setCeremonyState('idle');
    setCeremonySteps([]);
    setCurrentStepIndex(0);
    setOtpValue('');
    setOtpError('');
    setSession(prev => ({
      ...prev,
      mcaAchieved: false,
      amrEmitted: []
    }));
    logEvent('info', 'orchestration', 'Ceremony state reset. Clean session context established.');
  };

  // --- ENROLLMENT ACTIONS ---
  const [enrollMethod, setEnrollMethod] = useState<AuthenticatorMethod>('passkey');
  const [enrollLabel, setEnrollLabel] = useState('');
  const [enrollDest, setEnrollDest] = useState('');

  const handleEnrollDevice = (e: React.FormEvent) => {
    e.preventDefault();
    if (!enrollLabel || !enrollDest) return;

    const groupMap: Record<AuthenticatorMethod, string> = {
      sms: 'Telecom Network',
      email: 'Cloud Web Infrastructure',
      totp: 'HMAC Application State',
      push: 'Second-Device Secure App',
      passkey: 'Cryptographic Security Key',
      voice: 'Telecom Network',
      smartcard: 'Cryptographic Security Key'
    };

    // Update state or override
    setAuthenticators(prev => prev.map(a => {
      if (a.type === enrollMethod) {
        logEvent('success', 'enrollment', `Successfully re-enrolled/replaced credential for channel: ${enrollMethod.toUpperCase()}.`, {
          previous: a.destination,
          new: enrollDest,
          label: enrollLabel,
          independentGroup: groupMap[enrollMethod]
        });
        return {
          ...a,
          label: enrollLabel,
          destination: enrollDest,
          enrolled: true
        };
      }
      return a;
    }));

    setEnrollLabel('');
    setEnrollDest('');
  };

  const handleToggleEnrollment = (id: string) => {
    setAuthenticators(prev => prev.map(a => {
      if (a.id === id) {
        const nextState = !a.enrolled;
        logEvent('info', 'enrollment', `Enrolled state for device "${a.label}" updated to ${nextState ? 'ENROLLED' : 'DRAFT/UNENROLLED'}.`);
        return { ...a, enrolled: nextState };
      }
      return a;
    }));
  };

  // --- POLICY EDIT ACTIONS ---
  const handleUpdatePolicy = (updates: Partial<Policy>) => {
    setPolicy(prev => {
      const nextPolicy = { ...prev, ...updates };
      logEvent('success', 'policy', 'Security policy constraints adjusted interactively.', nextPolicy);
      return nextPolicy;
    });
  };

  return (
    <div className="min-h-screen bg-zinc-950 text-zinc-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200" id="mca-app-root">
      
      {/* HEADER SECTION */}
      <header className="border-b border-zinc-900 bg-zinc-900/40 backdrop-blur-md sticky top-0 z-50 px-4 py-3 sm:px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="bg-gradient-to-br from-indigo-500 to-purple-500 p-2 rounded-xl shadow-lg shadow-indigo-500/10 border border-indigo-400/20">
              <Shield className="h-6 w-6 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-base sm:text-lg font-bold tracking-tight text-white font-mono uppercase">
                  Multi-Channel Ceremony
                </h1>
                <span className="inline-flex items-center gap-1 rounded-full bg-indigo-500/10 px-2 py-0.5 text-[9px] font-mono font-medium text-indigo-400 border border-indigo-500/20">
                  AMR: mca ●
                </span>
              </div>
              <p className="text-2xs text-zinc-400 mt-0.5">
                First-Party Cryptographic Multi-Channel Orchestration & Diagnostics
              </p>
            </div>
          </div>

          {/* Subject Context Header Card */}
          <div className="flex flex-wrap items-center gap-3 bg-zinc-900/60 rounded-xl border border-zinc-800 p-2.5 max-w-full sm:max-w-md">
            <div className="bg-zinc-950 p-1.5 rounded-lg border border-zinc-800 shrink-0">
              <User className="h-4 w-4 text-zinc-400" />
            </div>
            <div className="flex-1 min-w-0 text-2xs font-mono space-y-0.5">
              <div className="flex items-center justify-between">
                <span className="text-zinc-500">Subject:</span>
                <span className="text-zinc-300 font-medium truncate ml-1">{session.subject}</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-zinc-500">Tenant:</span>
                <span className="text-zinc-300 truncate ml-1">{session.tenantId}</span>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* SUB-HEADER STATUS STRIP */}
      <div className="bg-zinc-950 border-b border-zinc-900/50 px-4 py-2 sm:px-6">
        <div className="max-w-7xl mx-auto flex flex-col sm:flex-row sm:items-center justify-between gap-2 text-2xs text-zinc-500 font-mono">
          <div className="flex items-center gap-4 flex-wrap">
            <span className="flex items-center gap-1.5">
              <span className="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-ping" />
              <span>IP Context: <strong className="text-zinc-400">{session.ipAddress}</strong></span>
            </span>
            <span>Location: <strong className="text-zinc-400">{session.location}</strong></span>
            <span>OS Host: <strong className="text-zinc-400">{session.deviceOs}</strong></span>
          </div>
          <div className="flex items-center gap-2">
            <span>Server Time:</span>
            <span className="text-zinc-400 font-bold">2026-07-15 10:46 UTC</span>
          </div>
        </div>
      </div>

      {/* MAIN CONTAINER */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        
        {/* TAB CHOOSER */}
        <div className="flex border-b border-zinc-800 gap-1 p-1 bg-zinc-900/30 rounded-xl max-w-md" id="tab-chooser">
          <button
            onClick={() => setActiveTab('ceremony')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition ${
              activeTab === 'ceremony'
                ? 'bg-zinc-800 text-zinc-100 shadow-sm border border-zinc-700/50'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/40'
            }`}
          >
            <Key className="h-3.5 w-3.5" />
            P0 Ceremony Chamber
          </button>
          <button
            onClick={() => setActiveTab('enrollment')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition ${
              activeTab === 'enrollment'
                ? 'bg-zinc-800 text-zinc-100 shadow-sm border border-zinc-700/50'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/40'
            }`}
          >
            <Smartphone className="h-3.5 w-3.5" />
            P1 Channel Enrollment
          </button>
          <button
            onClick={() => setActiveTab('policy')}
            className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 rounded-lg text-xs font-semibold transition ${
              activeTab === 'policy'
                ? 'bg-zinc-800 text-zinc-100 shadow-sm border border-zinc-700/50'
                : 'text-zinc-400 hover:text-zinc-200 hover:bg-zinc-900/40'
            }`}
          >
            <Settings className="h-3.5 w-3.5" />
            P2 Policy & Health
          </button>
        </div>

        {/* TAB PANELS */}
        <div className="space-y-6">

          {/* TAB 1: P0 CEREMONY */}
          {activeTab === 'ceremony' && (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6" id="ceremony-tab-panel">
              
              {/* Left Column: Flow Progress & Information (Span 5) */}
              <div className="lg:col-span-5 space-y-6">
                
                {/* Intro Card */}
                <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4">
                  <div className="flex items-start justify-between">
                    <div className="space-y-1">
                      <span className="text-[10px] text-indigo-400 font-mono tracking-widest uppercase font-bold">
                        Universal Authentication
                      </span>
                      <h2 className="text-base font-bold text-zinc-100">
                        Multi-Channel Ceremony Intro
                      </h2>
                    </div>
                    <span className="bg-zinc-950 text-indigo-400 text-2xs font-mono px-2 py-1 rounded-md border border-zinc-800">
                      Policy: STRICT
                    </span>
                  </div>

                  <p className="text-xs text-zinc-400 leading-relaxed">
                    This ceremony implements secure <strong>multi-channel identity proofing</strong>. To sign the multi-channel reference authentication token (`mca`), you must pass independent verification steps.
                  </p>

                  <div className="space-y-2.5 border-t border-zinc-900 pt-3">
                    <div className="flex gap-2 text-xs">
                      <span className="text-zinc-500 font-mono">1. Independence:</span>
                      <span className="text-zinc-300">Channels must use completely disjoint authentication groups.</span>
                    </div>
                    <div className="flex gap-2 text-xs">
                      <span className="text-zinc-500 font-mono">2. Strict Flow:</span>
                      <span className="text-zinc-300">Step 1 must fully complete before Step 2 callbacks are authorized.</span>
                    </div>
                    <div className="flex gap-2 text-xs">
                      <span className="text-zinc-500 font-mono">3. Timeout Guard:</span>
                      <span className="text-zinc-300">Unused session tokens expire within 60 seconds automatically.</span>
                    </div>
                  </div>

                  {ceremonyState === 'idle' && (
                    <button
                      onClick={handleStartCeremony}
                      className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl py-2.5 text-xs transition shadow-lg shadow-indigo-600/10 flex items-center justify-center gap-1.5"
                      id="start-ceremony-btn"
                    >
                      <Sparkles className="h-4 w-4" />
                      Begin Dynamic Ceremony
                    </button>
                  )}
                </div>

                {/* Vertical Timeline Steps (CeremonyProgress) */}
                {ceremonySteps.length > 0 && (
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4">
                    <span className="text-[10px] text-zinc-500 font-mono tracking-widest uppercase font-bold">
                      Ceremony Steps Tracker
                    </span>

                    <div className="relative pl-6 space-y-6 border-l border-zinc-800">
                      {ceremonySteps.map((step, idx) => (
                        <div key={step.id} className="relative" id={`timeline-step-${step.id}`}>
                          {/* Dot Badge Indicator */}
                          <div className={`absolute -left-[31px] top-0.5 h-4 w-4 rounded-full border-2 flex items-center justify-center text-[9px] font-bold ${
                            step.status === 'completed'
                              ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400'
                              : step.status === 'current'
                              ? 'bg-indigo-500/20 border-indigo-500 text-indigo-400'
                              : 'bg-zinc-950 border-zinc-800 text-zinc-600'
                          }`}>
                            {step.status === 'completed' ? <Check className="h-2 w-2" /> : idx + 1}
                          </div>

                          <div className="space-y-1">
                            <div className="flex items-center justify-between">
                              <h4 className={`text-xs font-bold font-mono uppercase tracking-wider ${
                                step.status === 'current' ? 'text-zinc-100' : 'text-zinc-400'
                              }`}>
                                {step.title}
                              </h4>
                              {step.status === 'completed' && (
                                <span className="text-[9px] font-mono text-emerald-400 bg-emerald-500/10 border border-emerald-500/20 px-1.5 py-0.2 rounded-md">
                                  VERIFIED
                                </span>
                              )}
                              {step.status === 'current' && (
                                <span className="text-[9px] font-mono text-indigo-400 bg-indigo-500/10 border border-indigo-500/20 px-1.5 py-0.2 rounded-md animate-pulse">
                                  ACTIVE
                                </span>
                              )}
                            </div>

                            <p className="text-2xs text-zinc-400 leading-relaxed">{step.description}</p>
                            <p className="text-2xs text-zinc-500 font-mono">
                              Status: <span className="text-zinc-300 font-medium">{step.progressText}</span>
                            </p>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Interactive Simulation Panel for Carrier Integrity */}
                {ceremonyState !== 'idle' && (
                  <div className="bg-zinc-900/20 border border-zinc-800 border-dashed rounded-xl p-4 space-y-3">
                    <h4 className="text-xs font-semibold text-amber-500 flex items-center gap-1.5">
                      <AlertTriangle className="h-4 w-4" />
                      Simulate Carrier Attack Vector
                    </h4>
                    <p className="text-2xs text-zinc-400">
                      Compromise cellular trunks to intercept OTP messages. This tests whether the policy correctly blocks single-channel substitution.
                    </p>
                    <label className="flex items-center justify-between bg-zinc-950 p-2.5 rounded-lg border border-zinc-900 cursor-pointer select-none">
                      <span className="text-2xs font-mono text-zinc-300">
                        Carrier SIM-Swap / Trunk Intercept:
                      </span>
                      <input
                        type="checkbox"
                        checked={simulatedCarrierCompromise}
                        onChange={(e) => {
                          setSimulatedCarrierCompromise(e.target.checked);
                          logEvent(
                            e.target.checked ? 'warn' : 'info',
                            'orchestration',
                            `Carrier integrity simulation updated: ${e.target.checked ? 'COMPROMISED (SMS SIM-Swap risk active)' : 'INTEGRAL'}`
                          );
                        }}
                        className="rounded border-zinc-800 bg-zinc-900 text-indigo-600 focus:ring-0"
                      />
                    </label>
                  </div>
                )}
              </div>

              {/* Right Column: Interaction Sandbox Panel (Span 7) */}
              <div className="lg:col-span-7 space-y-6">
                
                {/* Idle Prompt */}
                {ceremonyState === 'idle' && (
                  <div className="bg-zinc-900/30 border border-zinc-800 rounded-2xl p-10 text-center space-y-4 flex flex-col items-center justify-center min-h-[350px]">
                    <div className="bg-zinc-900 p-4 rounded-full border border-zinc-800">
                      <Key className="h-8 w-8 text-indigo-400" />
                    </div>
                    <div className="space-y-1">
                      <h3 className="font-bold text-zinc-200">Ceremony Chamber Dormant</h3>
                      <p className="text-xs text-zinc-500 max-w-sm mx-auto">
                        Please initiate the Multi-Channel Authentication ceremony to interact with step adapters, out-of-band push callbacks, and evidence gathering.
                      </p>
                    </div>
                    <button
                      onClick={handleStartCeremony}
                      className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl px-4 py-2 text-xs transition"
                    >
                      Start Ceremony
                    </button>
                  </div>
                )}

                {/* Introduction Step */}
                {ceremonyState === 'introduction' && (
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4 min-h-[350px] flex flex-col justify-between">
                    <div className="space-y-3">
                      <div className="flex items-center gap-2 border-b border-zinc-900 pb-2.5">
                        <Sliders className="h-4 w-4 text-indigo-400" />
                        <h3 className="font-bold text-zinc-100 text-sm">Ceremony Verification Protocol</h3>
                      </div>

                      <div className="space-y-3 text-xs text-zinc-400">
                        <p>
                          To satisfy the current organizational policy constraints, your browser must establish cryptographic correlation of two separate identity sources.
                        </p>
                        <p>
                          The verification server will bind the requests utilizing the tenant-specific correlation identifier: <code className="bg-black/40 px-1.5 py-0.5 rounded font-mono text-indigo-400">{session.id}</code>.
                        </p>
                        <p className="text-amber-400/90 font-mono text-2xs bg-amber-500/5 p-2 rounded-lg border border-amber-500/10">
                          NOTE: Verification tokens are single-use. If a token is entered correctly but has timed out, the server will block late assertion submissions.
                        </p>
                      </div>
                    </div>

                    <div className="flex justify-end gap-3 pt-4 border-t border-zinc-900">
                      <button
                        onClick={handleResetCeremony}
                        className="text-xs text-zinc-400 hover:text-zinc-200"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleAcceptIntroduction}
                        className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl px-4 py-2 text-xs transition"
                        id="accept-intro-btn"
                      >
                        Acknowledge & Choose Method
                      </button>
                    </div>
                  </div>
                )}

                {/* Method selection chooser */}
                {ceremonyState === 'method_selection' && (
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4 min-h-[350px]">
                    <div className="flex items-center justify-between border-b border-zinc-900 pb-2.5">
                      <h3 className="font-bold text-zinc-100 text-sm">
                        Select Method for {ceremonySteps[currentStepIndex]?.title}
                      </h3>
                      <span className="text-2xs font-mono text-zinc-500">
                        Allowed by Policy: {ceremonySteps[currentStepIndex]?.allowedMethods.join(', ').toUpperCase()}
                      </span>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
                      {ceremonySteps[currentStepIndex]?.allowedMethods.map((m) => {
                        const targetAuth = authenticators.find(a => a.type === m);
                        const isEnrolled = targetAuth?.enrolled;
                        
                        return (
                          <div
                            key={m}
                            onClick={() => isEnrolled && handleSelectMethod(m)}
                            className={`group border rounded-xl p-4 cursor-pointer select-none transition ${
                              isEnrolled
                                ? 'bg-zinc-900 border-zinc-800 hover:border-zinc-700 hover:bg-zinc-900/80'
                                : 'bg-zinc-950/40 border-zinc-900/50 opacity-50 cursor-not-allowed'
                            }`}
                            id={`method-option-${m}`}
                          >
                            <div className="flex items-start justify-between">
                              <div className="space-y-1">
                                <h4 className="text-xs font-bold text-zinc-200 capitalize group-hover:text-white transition">
                                  {m === 'totp' ? 'Auth App (TOTP)' : m === 'passkey' ? 'FIDO Passkey' : m.toUpperCase()}
                                </h4>
                                <p className="text-[11px] text-zinc-500">
                                  {isEnrolled ? targetAuth.destination : 'Not Enrolled'}
                                </p>
                              </div>
                              <span className={`text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full ${
                                isEnrolled 
                                  ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' 
                                  : 'bg-zinc-950 text-zinc-600'
                              }`}>
                                {isEnrolled ? 'Enrolled' : 'Pending'}
                              </span>
                            </div>

                            <div className="flex items-center gap-1.5 mt-3 text-[10px] text-zinc-500 font-mono">
                              <span>Security Group:</span>
                              <span className="text-zinc-400">{targetAuth?.independentGroup}</span>
                            </div>
                          </div>
                        );
                      })}
                    </div>

                    <div className="flex justify-between items-center pt-4 border-t border-zinc-900">
                      <button
                        onClick={handleResetCeremony}
                        className="text-xs text-zinc-400 hover:text-zinc-200"
                      >
                        Reset Ceremony
                      </button>
                      <p className="text-[10px] text-zinc-500 font-mono">
                        Requires Enrolled Multi-Channel authenticators.
                      </p>
                    </div>
                  </div>
                )}

                {/* Adapter Screen: SMS / Email / TOTP OTP input */}
                {ceremonyState === 'step_active' && (
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4 min-h-[350px] flex flex-col justify-between">
                    <div className="space-y-4">
                      
                      {/* Sub-Header */}
                      <div className="flex items-center justify-between border-b border-zinc-900 pb-2.5">
                        <div className="flex items-center gap-2">
                          {ceremonySteps[currentStepIndex]?.selectedMethod === 'sms' && <Smartphone className="h-4 w-4 text-rose-400" />}
                          {ceremonySteps[currentStepIndex]?.selectedMethod === 'email' && <Mail className="h-4 w-4 text-amber-400" />}
                          {ceremonySteps[currentStepIndex]?.selectedMethod === 'totp' && <Clock className="h-4 w-4 text-purple-400" />}
                          {ceremonySteps[currentStepIndex]?.selectedMethod === 'passkey' && <Key className="h-4 w-4 text-sky-400" />}
                          
                          <h3 className="font-bold text-zinc-100 text-sm">
                            Verify via {ceremonySteps[currentStepIndex]?.selectedMethod?.toUpperCase()}
                          </h3>
                        </div>
                        <button
                          onClick={() => setCeremonyState('method_selection')}
                          className="text-2xs font-mono text-indigo-400 hover:text-indigo-300"
                        >
                          Change Method
                        </button>
                      </div>

                      {/* Display warning or hint */}
                      <div className="text-xs text-zinc-400 leading-relaxed bg-zinc-950 p-3 rounded-xl border border-zinc-900">
                        {ceremonySteps[currentStepIndex]?.selectedMethod === 'sms' && (
                          <span>A verification challenge token was sent to cellular node <strong className="text-zinc-300 font-mono">+1 (•••) •••-4821</strong>. SMS routing typically finishes within 2 seconds.</span>
                        )}
                        {ceremonySteps[currentStepIndex]?.selectedMethod === 'email' && (
                          <span>A secure OTP was forwarded to your authenticated mailbox <strong className="text-zinc-300 font-mono">ad•••@corporate.internal</strong>.</span>
                        )}
                        {ceremonySteps[currentStepIndex]?.selectedMethod === 'totp' && (
                          <span>Generate a 6-digit verification code using your registered TOTP application (Google Authenticator, Duo, etc.) configured for security account context.</span>
                        )}
                        {ceremonySteps[currentStepIndex]?.selectedMethod === 'passkey' && (
                          <span>Initiate a local cryptographic hardware signature utilizing your platform passkey, TouchID, or security token.</span>
                        )}
                      </div>

                      {/* Interactive Adapter UI */}
                      {ceremonySteps[currentStepIndex]?.selectedMethod === 'passkey' ? (
                        <div className="py-6 text-center space-y-4">
                          <button
                            onClick={handlePasskeyTrigger}
                            className="bg-sky-600 hover:bg-sky-500 text-white font-semibold px-6 py-2.5 rounded-xl transition shadow-lg shadow-sky-600/10 inline-flex items-center gap-2 text-xs"
                            id="trigger-webauthn-btn"
                          >
                            <Key className="h-4 w-4" />
                            Trigger WebAuthn Credentials
                          </button>
                          <p className="text-[10px] text-zinc-500 font-mono">
                            Verifying browser biometric context securely.
                          </p>
                        </div>
                      ) : (
                        <div className="space-y-3 py-2 max-w-sm">
                          <div className="space-y-1">
                            <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                              Enter Verification Token Challenge:
                            </label>
                            <div className="flex gap-2">
                              <input
                                type="text"
                                maxLength={6}
                                placeholder="000000"
                                value={otpValue}
                                onChange={(e) => setOtpValue(e.target.value.replace(/\D/g, ''))}
                                className="bg-zinc-950 border border-zinc-800 rounded-lg px-3 py-2 text-sm font-mono tracking-widest text-zinc-200 placeholder-zinc-700 focus:outline-none focus:border-zinc-700 flex-1"
                                id="otp-input-field"
                              />
                              <button
                                onClick={handleVerifyOtp}
                                className="bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-lg px-4 text-xs transition"
                                id="submit-otp-btn"
                              >
                                Verify Token
                              </button>
                            </div>
                          </div>

                          {/* Quick seed helpers for testing */}
                          <div className="flex items-center gap-2 pt-1">
                            <span className="text-[10px] text-zinc-500 font-mono">Quick Sim Code:</span>
                            <button
                              onClick={() => setOtpValue('123456')}
                              className="text-[10px] font-mono text-zinc-400 bg-zinc-900 border border-zinc-800 px-1.5 py-0.5 rounded hover:border-zinc-700"
                            >
                              123456
                            </button>
                            <button
                              onClick={() => setOtpValue('9999')}
                              className="text-[10px] font-mono text-rose-400 bg-zinc-900 border border-rose-950 px-1.5 py-0.5 rounded hover:border-rose-900"
                            >
                              Fail Token
                            </button>
                          </div>
                        </div>
                      )}

                      {/* Display validation errors */}
                      {otpError && (
                        <div className="flex items-center gap-2 text-xs text-rose-400 bg-rose-500/5 border border-rose-500/10 p-2.5 rounded-lg">
                          <AlertTriangle className="h-4 w-4 shrink-0" />
                          <span>{otpError}</span>
                        </div>
                      )}
                    </div>

                    <div className="flex justify-between items-center border-t border-zinc-900 pt-3 text-[11px] text-zinc-500 font-mono">
                      <span>Token Lifetime: 60s</span>
                      <button
                        onClick={handleResetCeremony}
                        className="text-zinc-400 hover:text-zinc-200"
                      >
                        Reset
                      </button>
                    </div>
                  </div>
                )}

                {/* Out of Band Poll Screen */}
                {ceremonyState === 'oob_waiting' && (
                  <ExternalApprovalWait
                    method={ceremonySteps[currentStepIndex]?.selectedMethod as 'push' | 'voice'}
                    destination={authenticators.find(a => a.type === ceremonySteps[currentStepIndex]?.selectedMethod)?.destination || 'Second Device'}
                    expirySeconds={60}
                    onApprove={handleOobApprove}
                    onReject={handleOobReject}
                    onCancel={handleOobCancel}
                    onResend={handleOobResend}
                    canResend={oobResendCooldown === 0}
                  />
                )}

                {/* Final Success state */}
                {ceremonyState === 'success' && (
                  <IndependenceEvidenceSummary
                    session={session}
                    methodsUsed={ceremonySteps.map(s => s.selectedMethod as AuthenticatorMethod)}
                    onReset={handleResetCeremony}
                  />
                )}

                {/* Terminal Failure state */}
                {ceremonyState === 'failed' && (
                  <div className="bg-zinc-900/40 border border-rose-900/30 bg-rose-950/5 rounded-2xl p-6 text-center space-y-4 min-h-[350px] flex flex-col justify-center items-center">
                    <div className="bg-rose-500/10 text-rose-400 p-4 rounded-full border border-rose-500/20">
                      <AlertTriangle className="h-8 w-8 animate-bounce" />
                    </div>
                    <div className="space-y-2">
                      <h3 className="font-bold text-rose-300">Authentication Policy Rejection</h3>
                      <p className="text-xs text-zinc-400 max-w-sm mx-auto">
                        The Multi-Channel orchestration engine detected a critical channel independence breach or compromise event.
                      </p>
                      <p className="text-[11px] text-zinc-500 font-mono bg-black/40 p-2.5 rounded-lg border border-zinc-900">
                        Reason: Steps completed, but credentials lacked the disjoint network groups (e.g., Telecom and Local Hardware) required by the security policy.
                      </p>
                    </div>
                    <div className="flex gap-3">
                      <button
                        onClick={handleResetCeremony}
                        className="bg-zinc-800 hover:bg-zinc-700 text-zinc-200 text-xs font-semibold px-4 py-2 rounded-xl transition border border-zinc-700"
                      >
                        Retry Ceremony
                      </button>
                    </div>
                  </div>
                )}

                {/* Policy Fallback Analyzer Widget */}
                {ceremonySteps.length > 0 && (
                  <ChannelFallbackComparison
                    policy={policy}
                    selectedMethods={ceremonySteps.map(s => s.selectedMethod as AuthenticatorMethod).filter(Boolean)}
                  />
                )}
              </div>
            </div>
          )}

          {/* TAB 2: P1 ENROLLMENT */}
          {activeTab === 'enrollment' && (
            <div className="space-y-6" id="enrollment-tab-panel">
              
              {/* Informative top panel */}
              <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-3">
                <div className="flex items-center gap-2">
                  <Smartphone className="h-5 w-5 text-indigo-400" />
                  <h3 className="font-bold text-zinc-100 text-sm">Underlying Channel Enrollment Directory</h3>
                </div>
                <p className="text-xs text-zinc-400 leading-relaxed max-w-3xl">
                  Multi-channel authentication requires active enrollment of at least two disjoint, independent devices. View, replace, or register your secure communication nodes. Ensure you do not configure duplicate carrier destinations to preserve policy-defined isolation.
                </p>
              </div>

              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                
                {/* Authenticators list directory (Span 7) */}
                <div className="lg:col-span-7 space-y-3">
                  <span className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                    Active Registrations
                  </span>

                  <div className="grid grid-cols-1 gap-2.5">
                    {authenticators.map((auth) => (
                      <div
                        key={auth.id}
                        className={`border rounded-xl p-4 transition ${
                          auth.enrolled
                            ? 'bg-zinc-900 border-zinc-800'
                            : 'bg-zinc-950/20 border-zinc-900 border-dashed opacity-60'
                        }`}
                        id={`enrollment-card-${auth.id}`}
                      >
                        <div className="flex items-start justify-between">
                          <div className="space-y-1">
                            <div className="flex items-center gap-2">
                              <h4 className="text-xs font-bold text-zinc-200">
                                {auth.label}
                              </h4>
                              <span className="text-[9px] font-mono text-zinc-400 uppercase bg-zinc-950 px-1.5 py-0.2 rounded-md border border-zinc-800">
                                {auth.type.toUpperCase()}
                              </span>
                            </div>
                            <p className="text-xs font-mono text-zinc-400">
                              Destination: {auth.enrolled ? auth.destination : 'No hardware registered'}
                            </p>
                          </div>

                          <div className="flex items-center gap-2">
                            <button
                              onClick={() => handleToggleEnrollment(auth.id)}
                              className={`text-[10px] font-mono px-2.5 py-1 rounded-md border transition ${
                                auth.enrolled
                                  ? 'bg-rose-500/10 hover:bg-rose-500/20 text-rose-400 border-rose-500/20'
                                  : 'bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 border-emerald-500/20'
                              }`}
                            >
                              {auth.enrolled ? 'Revoke Enrol' : 'Enroll Now'}
                            </button>
                          </div>
                        </div>

                        <div className="flex items-center gap-2.5 mt-3 border-t border-zinc-950 pt-2 text-[10px] text-zinc-500 font-mono">
                          <span>Independence Grouping:</span>
                          <span className="text-zinc-400 font-semibold">{auth.independentGroup}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                {/* Enrollment simulator registry (Span 5) */}
                <div className="lg:col-span-5 space-y-4">
                  
                  {/* Enroll device form */}
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4">
                    <h3 className="font-bold text-zinc-100 text-sm">Register / Replace Credential</h3>
                    <p className="text-xs text-zinc-400 leading-relaxed">
                      Simulate enrollment of high assurance authenticators, including physical smart cards, biometric passkeys, or distinct mobile carrier destinations.
                    </p>

                    <form onSubmit={handleEnrollDevice} className="space-y-3">
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Authenticator Type:
                        </label>
                        <select
                          value={enrollMethod}
                          onChange={(e) => {
                            const val = e.target.value as AuthenticatorMethod;
                            setEnrollMethod(val);
                            // Set defaults to avoid blank text
                            const defaults: Record<AuthenticatorMethod, { label: string, dest: string }> = {
                              passkey: { label: 'YubiKey 5C NFC WebAuthn', dest: 'FIDO2 TPM Secure Core' },
                              smartcard: { label: 'PIV Smart Card Node', dest: 'CAC Card Token ID: 81a0e' },
                              totp: { label: 'Hardware TOTP App', dest: 'Aegis Security Client' },
                              push: { label: 'Secondary Android Device', dest: 'Pixel 8 Pro' },
                              sms: { label: 'Cellular Secondary SIM', dest: '+1 (•••) •••-2009' },
                              email: { label: 'Personal ProtonMail', dest: 'per•••@proton.me' },
                              voice: { label: 'Simulated Voice Ring', dest: '+1 (•••) •••-8119' }
                            };
                            setEnrollLabel(defaults[val].label);
                            setEnrollDest(defaults[val].dest);
                          }}
                          className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-zinc-700 font-mono"
                        >
                          <option value="passkey">Hardware Passkey (WebAuthn)</option>
                          <option value="totp">Auth Application (TOTP)</option>
                          <option value="push">Mobile Device Callback (Push)</option>
                          <option value="sms">Cellular Trunk (SMS OTP)</option>
                          <option value="email">Mail Relay Gateway (Email)</option>
                          <option value="voice">Telephone Trunk (Voice Ring)</option>
                        </select>
                      </div>

                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Label:
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="e.g. YubiKey 5C Core Key"
                          value={enrollLabel}
                          onChange={(e) => setEnrollLabel(e.target.value)}
                          className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1.5 text-xs text-zinc-200 focus:outline-none"
                        />
                      </div>

                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Destination Hint / Hardware Signature:
                        </label>
                        <input
                          type="text"
                          required
                          placeholder="e.g. +1 (•••) •••-9182"
                          value={enrollDest}
                          onChange={(e) => setEnrollDest(e.target.value)}
                          className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1.5 text-xs text-zinc-200 focus:outline-none font-mono"
                        />
                      </div>

                      <button
                        type="submit"
                        className="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded-xl py-2 text-xs transition flex items-center justify-center gap-1.5 mt-2"
                      >
                        <Plus className="h-4 w-4" /> Enroll Device
                      </button>
                    </form>
                  </div>
                </div>

              </div>
            </div>
          )}

          {/* TAB 3: P2 OPERATIONS, POLICY, DIAGNOSTICS */}
          {activeTab === 'policy' && (
            <div className="space-y-6" id="policy-tab-panel">
              
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                
                {/* Left Column: Admin Policy config (Span 5) */}
                <div className="lg:col-span-5 space-y-4">
                  <div className="bg-zinc-900/40 border border-zinc-800 rounded-2xl p-5 space-y-4">
                    <div className="flex items-center gap-2 border-b border-zinc-900 pb-2.5">
                      <Settings className="h-4 w-4 text-purple-400" />
                      <h3 className="font-bold text-zinc-100 text-sm">Administrative Policy Editor</h3>
                    </div>

                    <div className="space-y-4">
                      {/* Independent group limit */}
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Min Independent Channels Required:
                        </label>
                        <div className="flex gap-2">
                          {[2, 3].map((num) => (
                            <button
                              key={num}
                              type="button"
                              onClick={() => handleUpdatePolicy({ requiredIndependentChannels: num })}
                              className={`flex-1 py-1.5 rounded-lg text-xs font-semibold font-mono border transition ${
                                policy.requiredIndependentChannels === num
                                  ? 'bg-purple-600/20 text-purple-300 border-purple-500/50'
                                  : 'bg-zinc-950 text-zinc-400 border-zinc-900 hover:border-zinc-800'
                              }`}
                            >
                              {num} Channels
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Sequence Order constraint */}
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Ceremony Step Sequencing:
                        </label>
                        <div className="flex gap-2">
                          {['strict', 'flexible'].map((seq) => (
                            <button
                              key={seq}
                              type="button"
                              onClick={() => handleUpdatePolicy({ sequenceOrder: seq as any })}
                              className={`flex-1 py-1.5 rounded-lg text-xs font-semibold font-mono border capitalize transition ${
                                policy.sequenceOrder === seq
                                  ? 'bg-purple-600/20 text-purple-300 border-purple-500/50'
                                  : 'bg-zinc-950 text-zinc-400 border-zinc-900 hover:border-zinc-800'
                              }`}
                            >
                              {seq} Sequential
                            </button>
                          ))}
                        </div>
                      </div>

                      {/* Fallback configuration */}
                      <div className="space-y-1.5">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Assurance Fallback Authorization:
                        </label>
                        <label className="flex items-center justify-between bg-zinc-950 p-2.5 rounded-lg border border-zinc-900 cursor-pointer select-none">
                          <span className="text-2xs text-zinc-400 font-mono">Allow fallback channels if primary suffers outage:</span>
                          <input
                            type="checkbox"
                            checked={policy.allowFallback}
                            onChange={(e) => handleUpdatePolicy({ allowFallback: e.target.checked })}
                            className="rounded border-zinc-800 bg-zinc-900 text-purple-600 focus:ring-0"
                          />
                        </label>
                      </div>

                      {/* Token expiry */}
                      <div className="space-y-1">
                        <label className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                          Assurance Expiry Timeout:
                        </label>
                        <select
                          value={policy.tokenExpirySeconds}
                          onChange={(e) => handleUpdatePolicy({ tokenExpirySeconds: parseInt(e.target.value) })}
                          className="w-full bg-zinc-950 border border-zinc-800 rounded-lg px-2.5 py-1.5 text-xs text-zinc-200 focus:outline-none focus:border-zinc-700 font-mono"
                        >
                          <option value="30">30 Seconds (Ultra-Secured)</option>
                          <option value="60">60 Seconds (Default Standard)</option>
                          <option value="120">120 Seconds (Extended Wait)</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Right Column: Provider Health Dashboard (Span 7) */}
                <div className="lg:col-span-7 space-y-6">
                  <ChannelProviderHealthGrid
                    providers={providers}
                    onToggleStatus={handleToggleProvider}
                  />
                </div>

              </div>

              {/* Bottom Row: Full Diagnostic Log terminal */}
              <div className="space-y-3">
                <span className="text-[10px] uppercase font-bold text-zinc-500 font-mono tracking-wider block">
                  Diagnostic Event Streams
                </span>
                <DiagnosticsTimeline
                  events={events}
                  onClear={() => setEvents([])}
                />
              </div>

            </div>
          )}

        </div>

      </main>

      {/* FOOTER */}
      <footer className="border-t border-zinc-900 bg-zinc-900/20 mt-12 py-6 text-center text-2xs text-zinc-500 font-mono">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <span>First-Party Multi-Channel Authentication (mca) Orchestration Client</span>
          <div className="flex gap-4">
            <span className="flex items-center gap-1">
              <span className="h-1 w-1 bg-emerald-400 rounded-full" />
              Crypto Engine: Active
            </span>
            <span>Tenant context correlation secured</span>
          </div>
        </div>
      </footer>

    </div>
  );
}
