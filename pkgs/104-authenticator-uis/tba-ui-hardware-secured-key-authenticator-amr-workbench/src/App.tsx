import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  ShieldCheck, 
  ShieldAlert, 
  KeyRound, 
  Cpu, 
  Terminal, 
  Sliders, 
  FileCode, 
  History, 
  HelpCircle, 
  Plus, 
  Trash2, 
  RefreshCw, 
  Scan, 
  CheckCircle2, 
  XCircle, 
  Info, 
  Fingerprint, 
  Lock, 
  AlertTriangle,
  Usb,
  Smartphone,
  Check,
  ChevronRight,
  Eye,
  Settings,
  HelpCircle as HelpIcon,
  Play,
  RotateCw,
  Clock,
  ExternalLink
} from 'lucide-react';
import { 
  initialAuthenticators, 
  initialWorkloadKeys, 
  attestationRoots, 
  initialAuditLogs, 
  sampleJWKS, 
  sampleCert, 
  sampleCSR 
} from './data';
import { 
  HardwareAuthenticator, 
  WorkloadKey, 
  AuditLogEntry, 
  CeremonyState, 
  PolicyConfig, 
  AttestationRootMetadata 
} from './types';
import { 
  KeyBackingBadge, 
  TransportBadge, 
  TrustRootBadge, 
  CLICommandOutput, 
  StatusIndicator 
} from './HWKComponents';

export default function App() {
  // Navigation
  const [activeTab, setActiveTab] = useState<'auth' | 'enroll' | 'workloads' | 'policy' | 'audit'>('auth');

  // Core State
  const [authenticators, setAuthenticators] = useState<HardwareAuthenticator[]>(initialAuthenticators);
  const [workloadKeys, setWorkloadKeys] = useState<WorkloadKey[]>(initialWorkloadKeys);
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>(initialAuditLogs);
  const [selectedAuth, setSelectedAuth] = useState<HardwareAuthenticator | null>(initialAuthenticators[0]);
  
  // Policy State
  const [policy, setPolicy] = useState<PolicyConfig>({
    requireHwkEvidence: true,
    acceptedAttestationRoots: [
      'Yubico_L1_Global_Root_CA',
      'Apple_WebAuthn_Root_CA',
      'Google_Titan_FIDO2_CA',
      'Microsoft_TPM_Attestation_Root'
    ],
    allowedAlgorithms: ['ES256', 'RS256'],
    userVerification: 'required',
    allowSyncedPasskeys: false,
    requireDiscoverable: true,
    gracePeriodDays: 7,
    enforcementMode: 'enforce'
  });

  // P0 - Auth Ceremony State
  const [ceremony, setCeremony] = useState<CeremonyState>({
    mode: 'auth',
    status: 'idle',
    authenticatorType: 'roaming',
    currentStep: 'Preflight check completed.',
    countdown: 45,
    selectedTransport: 'usb',
    hwkVerified: false
  });

  // Selected credential for signing in
  const [selectedCredForAuth, setSelectedCredForAuth] = useState<string>(initialAuthenticators[0].id);
  const [txPurpose, setTxPurpose] = useState<string>('Step-up access to Production Database Cluster (prod-db-01)');
  const [pinInput, setPinInput] = useState<string>('');
  const [osPromptActive, setOsPromptActive] = useState<boolean>(false);
  const [osPromptStep, setOsPromptStep] = useState<'insert' | 'pin' | 'touch' | 'hybrid-qr' | 'success' | 'error'>('insert');
  const [osPromptErrorType, setOsPromptErrorType] = useState<string>('');

  // P1 - Enrollment Form State
  const [enrollName, setEnrollName] = useState<string>('My Backup Security Key');
  const [enrollType, setEnrollType] = useState<'platform' | 'roaming'>('roaming');
  const [enrollAaguid, setEnrollAaguid] = useState<string>('cb581753-f341-4fb9-adc4-ae840d0263f1'); // Yubikey 5 by default
  const [enrollTransport, setEnrollTransport] = useState<('usb' | 'nfc' | 'ble' | 'internal' | 'hybrid')[]>(['usb', 'nfc']);
  const [enrollAlgorithm, setEnrollAlgorithm] = useState<'ES256' | 'RS256' | 'EdDSA'>('ES256');
  const [enrollAttestation, setEnrollAttestation] = useState<'packed' | 'tpm' | 'apple-anonymous' | 'none'>('packed');
  const [isEnrollingActive, setIsEnrollingActive] = useState<boolean>(false);

  // P2 - Workload State
  const [wlName, setWlName] = useState<string>('Inventory Event Publisher');
  const [wlProfile, setWlProfile] = useState<string>('E-Commerce Fulfillment Agent');
  const [wlAlg, setWlAlg] = useState<'RS256' | 'ES256' | 'EdDSA'>('ES256');
  const [wlMaterialType, setWlMaterialType] = useState<'jwks' | 'certificate' | 'csr'>('jwks');
  const [wlMaterialText, setWlMaterialText] = useState<string>(sampleJWKS);
  const [wlProtection, setWlProtection] = useState<'HSM' | 'TPM' | 'Software'>('HSM');
  const [wlProvenance, setWlProvenance] = useState<string>('Hardware-backed YubiHSM 2 Attestation Chain');
  const [testPayload, setTestPayload] = useState<string>('{"action": "rotate-database-creds", "timestamp": 1784112000}');
  const [testResult, setTestResult] = useState<string>('');
  const [isRotating, setIsRotating] = useState<string | null>(null);

  // Diagnostics / CLI CLI Workspace
  const [cliCommand, setCliCommand] = useState<string>('hwk-verify --credential auth-yubikey-5c');
  const [cliOutput, setCliOutput] = useState<string>('FIDO2 Hardware Cryptographic Evidence Diagnostics v2.4.0\nType commands or select a diagnostic preset below.');

  // Countdown timer effect
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (ceremony.status === 'user_gesture' && ceremony.countdown > 0) {
      timer = setInterval(() => {
        setCeremony(prev => {
          if (prev.countdown <= 1) {
            handleCeremonyError('timeout', 'WebAuthn request timed out awaiting user interaction.');
            return { ...prev, countdown: 0, status: 'failed' };
          }
          return { ...prev, countdown: prev.countdown - 1 };
        });
      }, 1000);
    }
    return () => clearInterval(timer);
  }, [ceremony.status, ceremony.countdown]);

  const addLog = (event: string, category: 'authentication' | 'enrollment' | 'workload' | 'policy' | 'system', status: 'success' | 'warning' | 'failure', details: string) => {
    const newLog: AuditLogEntry = {
      id: `log-${Date.now()}`,
      timestamp: new Date().toISOString(),
      event,
      category,
      status,
      actor: 'jick.68.0@gmail.com',
      details
    };
    setAuditLogs(prev => [newLog, ...prev]);
  };

  // P0 CEREMONY CONTROLS
  const startAuthCeremony = () => {
    const cred = authenticators.find(a => a.id === selectedCredForAuth);
    if (!cred) return;

    addLog('Authentication Ceremony Initiated', 'authentication', 'success', `Starting P0 sign-in flow for credential: ${cred.name}`);
    
    // 1. Preflight
    setCeremony({
      mode: 'auth',
      status: 'preflight',
      authenticatorType: cred.type === 'platform' ? 'platform' : 'roaming',
      chosenMethodId: cred.id,
      currentStep: 'Performing client environment preflight... checking browser WebAuthn API availability.',
      countdown: 45,
      selectedTransport: cred.transports[0] || 'usb',
      hwkVerified: false
    });

    setTimeout(() => {
      // Transition to Awaiting Device Prompt
      setCeremony(prev => ({
        ...prev,
        status: 'user_gesture',
        currentStep: 'Awaiting hardware authenticator touch / verification gesture.'
      }));
      setOsPromptActive(true);
      if (cred.transports.includes('internal')) {
        setOsPromptStep('touch'); // Touch ID or PIN
      } else if (cred.transports.includes('hybrid')) {
        setOsPromptStep('hybrid-qr');
      } else {
        setOsPromptStep('insert');
      }
    }, 1000);
  };

  const handleCeremonyTouch = () => {
    const cred = authenticators.find(a => a.id === ceremony.chosenMethodId);
    if (!cred) return;

    setOsPromptStep('touch');
    setCeremony(prev => ({
      ...prev,
      currentStep: 'Hardware token detected. Processing user gesture authorization.'
    }));

    setTimeout(() => {
      // Evaluate server-side policy and hardware evidence
      const meetsHwkPolicy = cred.backing === 'verified_hwk';
      const algorithmAllowed = policy.allowedAlgorithms.includes(cred.algorithm);
      const uvSatisfied = policy.userVerification === 'required' ? cred.userVerification === 'required' : true;

      // Rule check
      if (policy.requireHwkEvidence && !meetsHwkPolicy) {
        handleCeremonyError('policy-insufficient', 'The selected key does not supply certified hardware-protected attestation evidence (AMR hwk flag rejected).');
        return;
      }

      if (!algorithmAllowed) {
        handleCeremonyError('untrusted-hardware', `Security key algorithm ${cred.algorithm} is rejected by active administrator trust policies.`);
        return;
      }

      // Success
      setCeremony(prev => ({
        ...prev,
        status: 'success',
        currentStep: 'Attestation & assertion signature verified successfully. Classifying session AMR as [hwk].',
        hwkVerified: meetsHwkPolicy,
        provenanceSource: cred.attestationFormat === 'apple-anonymous' ? 'Apple Secure Enclave' : 'FIDO2 Hardware Attestation Statement',
        keyProtection: cred.backing === 'verified_hwk' ? 'Hardware-Backed HSM / Enclave' : 'Software-Backed / Synced Keychain',
        trustRoot: cred.trustRoot
      }));
      setOsPromptStep('success');

      addLog(
        'AMR hwk Authentication Ceremony Complete', 
        'authentication', 
        'success', 
        `Successfully logged in with ${cred.name}. Hardware verification: ${meetsHwkPolicy ? 'VERIFIED (hwk AMR)' : 'UNVERIFIED (lower assurance)'}`
      );
    }, 1200);
  };

  const handleCeremonyError = (type: 'cancelled' | 'timeout' | 'transport' | 'untrusted-hardware' | 'policy-insufficient', customMsg?: string) => {
    let errorMsg = customMsg || 'An error occurred during verification.';
    if (type === 'cancelled') {
      errorMsg = 'Operation cancelled by the user.';
    } else if (type === 'timeout') {
      errorMsg = 'Interaction timed out. Hardware key touch was not received within limit.';
    } else if (type === 'transport') {
      errorMsg = 'Transport failure. Device was removed or lost connection.';
    }

    setCeremony(prev => ({
      ...prev,
      status: 'failed',
      currentStep: `Ceremony Failed: ${errorMsg}`,
      errorMsg: errorMsg
    }));
    setOsPromptErrorType(type);
    setOsPromptStep('error');

    addLog(
      'Authentication Ceremony Failed', 
      'authentication', 
      type === 'policy-insufficient' ? 'failure' : 'warning', 
      `Failure state triggered: ${type}. details: ${errorMsg}`
    );
  };

  const resetCeremony = () => {
    setCeremony({
      mode: 'auth',
      status: 'idle',
      authenticatorType: 'roaming',
      currentStep: 'Preflight check completed.',
      countdown: 45,
      selectedTransport: 'usb',
      hwkVerified: false
    });
    setOsPromptActive(false);
    setPinInput('');
  };

  // P1 ENROLLMENT CONTROLS
  const startEnrollment = (e: React.FormEvent) => {
    e.preventDefault();
    setIsEnrollingActive(true);
    addLog('Human Key Enrollment Started', 'enrollment', 'success', `Enrolling new authenticator: ${enrollName}`);

    // Preflight check
    setTimeout(() => {
      // Find metadata root
      const rootMeta = attestationRoots.find(r => r.aaguid === enrollAaguid);
      const isHwkBacking = rootMeta ? rootMeta.hardwareBacking === 'verified_hwk' : false;

      // Create new authenticator object
      const newAuth: HardwareAuthenticator = {
        id: `auth-${Date.now()}`,
        name: enrollName,
        type: enrollType,
        aaguid: enrollAaguid,
        manufacturer: rootMeta ? rootMeta.manufacturer : 'Generic OEM',
        backing: isHwkBacking ? 'verified_hwk' : 'software_only',
        transports: enrollTransport,
        created: new Date().toISOString(),
        lastUsed: 'Never Used',
        status: 'active',
        algorithm: enrollAlgorithm,
        attestationFormat: enrollAttestation,
        backupEligible: enrollType === 'roaming',
        backupState: enrollType === 'roaming' ? 'backed_up' : 'single_device',
        trustRoot: rootMeta ? rootMeta.name : 'Unknown Attestation Authority',
        aaguidTrusted: rootMeta ? rootMeta.hardwareBacking === 'verified_hwk' : false,
        userVerification: 'required'
      };

      setAuthenticators(prev => [...prev, newAuth]);
      setSelectedCredForAuth(newAuth.id);
      setIsEnrollingActive(false);
      
      addLog(
        'Human Key Enrolled Successfully', 
        'enrollment', 
        isHwkBacking ? 'success' : 'warning', 
        `Authenticator [${enrollName}] registered with level ${isHwkBacking ? 'HWK VERIFIED' : 'SOFTWARE ONLY'}. Trust Root: ${newAuth.trustRoot}`
      );

      // Reset enroll fields
      setEnrollName('My Backup Security Key');
    }, 1500);
  };

  const removeAuthenticator = (id: string) => {
    const activeCreds = authenticators.filter(a => a.status === 'active');
    const target = authenticators.find(a => a.id === id);
    
    if (activeCreds.length <= 1 && target?.status === 'active') {
      alert('Security Policy Lockout Protection: You cannot delete your last active hardware authenticator. Please enroll an alternative backup key first.');
      addLog('Deletion Blocked', 'system', 'failure', `Attempted to delete the last active authenticator: ${target.name}. Action rejected.`);
      return;
    }

    setAuthenticators(prev => prev.filter(a => a.id !== id));
    if (selectedAuth?.id === id) {
      setSelectedAuth(null);
    }
    addLog('Authenticator Revoked/Removed', 'enrollment', 'warning', `User deleted authenticator: ${target?.name}`);
  };

  const toggleAuthenticatorStatus = (id: string, newStatus: 'active' | 'suspended') => {
    setAuthenticators(prev => prev.map(a => {
      if (a.id === id) {
        return { ...a, status: newStatus };
      }
      return a;
    }));
    addLog('Authenticator Status Modified', 'enrollment', 'warning', `Set authenticator status of ID [${id}] to ${newStatus}`);
  };

  // P2 WORKLOAD CONTROLS
  const registerWorkloadKey = (e: React.FormEvent) => {
    e.preventDefault();
    const newKey: WorkloadKey = {
      id: `wl-${Date.now()}`,
      name: wlName,
      profileName: wlProfile,
      algorithm: wlAlg,
      materialType: wlMaterialType,
      publicKeyMaterial: wlMaterialText,
      fingerprint: `sha256:${Math.random().toString(16).substr(2, 32)}...`,
      created: new Date().toISOString(),
      expiry: new Date(Date.now() + 30 * 24 * 60 * 60 * 1000).toISOString(), // 30 days
      status: 'active',
      keyProtection: wlProtection,
      provenanceSource: wlProvenance,
      lastVerified: new Date().toISOString()
    };

    setWorkloadKeys(prev => [newKey, ...prev]);
    addLog(
      'Workload Client Key Registered', 
      'workload', 
      wlProtection === 'HSM' ? 'success' : 'warning', 
      `Registered workload [${wlName}] with protection level: ${wlProtection}. Fingerprint: ${newKey.fingerprint}`
    );

    // Reset fields
    setWlName('Inventory Event Publisher');
  };

  const triggerRotation = (id: string) => {
    setIsRotating(id);
    addLog('Workload Key Rotation Triggered', 'workload', 'warning', `Key rotation sequence started for workload ID: ${id}`);
    
    setTimeout(() => {
      setWorkloadKeys(prev => prev.map(k => {
        if (k.id === id) {
          return {
            ...k,
            status: 'active',
            lastVerified: new Date().toISOString(),
            created: new Date().toISOString(),
            fingerprint: `sha256:${Math.random().toString(16).substr(2, 32)}...`
          };
        }
        return k;
      }));
      setIsRotating(null);
      addLog('Workload Key Rotated Successfully', 'workload', 'success', `Overlap rotation complete. Activated new credential for workload: ${id}. Retired prior key material.`);
    }, 2000);
  };

  const testWorkloadSignature = (key: WorkloadKey) => {
    setTestResult('Verifying signature payload...');
    setTimeout(() => {
      const valid = key.keyProtection !== 'Software';
      if (valid) {
        setTestResult(`SUCCESS: Signature verification passed.\nWorkload key: ${key.name}\nKey Protection: ${key.keyProtection} Verified (hwk:verified evidence found)\nFingerprint: ${key.fingerprint}\nChallenge context validated against origin successfully.`);
        addLog('Diagnostic Signature Verified', 'workload', 'success', `Workload signature verification verified successfully for ${key.name}`);
      } else {
        setTestResult(`WARNING: Verification passed but evidence is flagged as UNVERIFIED software backing.\nWorkload key: ${key.name}\nProtection: Software-Only\nOrigin evidence: missing hardware validation. Subject to downgrade.`);
        addLog('Diagnostic Signature Unverified Warning', 'workload', 'warning', `Workload verification warning for ${key.name}: Software backing detected.`);
      }
    }, 1000);
  };

  // DIAGNOSTIC CLI RUNNER
  const runPresetCliCommand = (cmd: string) => {
    setCliCommand(cmd);
    if (cmd.includes('--credential')) {
      const credId = cmd.split('--credential ')[1];
      const cred = authenticators.find(a => a.id === credId) || authenticators[0];
      setCliOutput(
        `$ hwk-verify --credential ${cred.id}\n` +
        `-----------------------------------------------------\n` +
        `FIDO2 HARDWARE CRYPTOGRAPHIC EVIDENCE DIAGNOSTIC\n` +
        `-----------------------------------------------------\n` +
        `Target Name       : ${cred.name}\n` +
        `Manufacturer      : ${cred.manufacturer}\n` +
        `AAGUID            : ${cred.aaguid}\n` +
        `Security Profile  : ${cred.backing === 'verified_hwk' ? 'HARDWARE_SECURED_KEY (hwk)' : 'SOFTWARE_ONLY / SYNCHRONIZED'}\n` +
        `Alg Standard      : ${cred.algorithm} (Approved standard)\n` +
        `Attestation Format: ${cred.attestationFormat}\n` +
        `Trust CA Chain    : ${cred.trustRoot}\n\n` +
        `[DECISION RESULT] : ${cred.backing === 'verified_hwk' ? '✓ VERIFIED HARDWARE AMR ACTIVE. Eligible for high-assurance network routing.' : '⚠ ATTENTION: Attestation missing or synced. Classified as level [software_only].'}`
      );
    } else if (cmd === 'hwk-policy-check') {
      setCliOutput(
        `$ hwk-policy-check\n` +
        `-----------------------------------------------------\n` +
        `AMR SECURITY ENFORCEMENT CONFIGURATION\n` +
        `-----------------------------------------------------\n` +
        `Require Hardware Evidence       : ${policy.requireHwkEvidence ? 'YES (FORCE_ENFORCE)' : 'NO'}\n` +
        `Allowed Alg List                : ${policy.allowedAlgorithms.join(', ')}\n` +
        `User Verification Mode         : ${policy.userVerification.toUpperCase()}\n` +
        `Allow Synced Cloud Tokens       : ${policy.allowSyncedPasskeys ? 'YES' : 'NO (BLOCKED)'}\n` +
        `Platform Enforce State         : ${policy.enforcementMode.toUpperCase()}\n\n` +
        `Diagnostics verdict: Security policy conforms to FedRAMP High Authenticator assurance.`
      );
    } else if (cmd === 'hwk-fido2-list') {
      const listString = authenticators.map(a => ` - [${a.backing === 'verified_hwk' ? 'HWK' : 'SOFT'}] ID: ${a.id.padEnd(20)} OEM: ${a.manufacturer.padEnd(12)} AAGUID: ${a.aaguid}`).join('\n');
      setCliOutput(
        `$ hwk-fido2-list\n` +
        `-----------------------------------------------------\n` +
        `DETECTED LOCAL WEBAUTHN PUBLIC KEY REGISTRATIONS\n` +
        `-----------------------------------------------------\n` +
        listString + `\n\nTotal security key tokens: ${authenticators.length}`
      );
    }
  };

  return (
    <div className="flex flex-col min-h-screen w-full bg-[#020617] text-slate-200 font-sans overflow-x-hidden selection:bg-emerald-500/30 selection:text-white">
      
      {/* Background Orbs */}
      <div className="absolute top-0 left-1/4 w-[500px] h-[500px] bg-emerald-500/5 rounded-full blur-[120px] pointer-events-none"></div>
      <div className="absolute bottom-10 right-1/4 w-[400px] h-[400px] bg-blue-500/5 rounded-full blur-[100px] pointer-events-none"></div>

      {/* Header */}
      <header className="sticky top-0 z-40 flex flex-col md:flex-row items-center justify-between px-6 md:px-8 py-4 border-b border-white/5 glass-dark backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-emerald-500 rounded-lg flex items-center justify-center font-bold text-slate-900 shadow-[0_0_15px_rgba(16,185,129,0.3)]">
            <Shield className="w-5 h-5 text-slate-950" />
          </div>
          <div>
            <h1 className="font-semibold tracking-tight text-lg text-white flex items-center gap-2">
              HWK <span className="text-slate-400 font-light text-base">SecureAccess AMR Workbench</span>
            </h1>
            <p className="text-[10px] text-slate-500 font-mono">Evidence-Driven Authentication Security Panel</p>
          </div>
        </div>

        {/* Global metadata status block */}
        <div className="flex flex-wrap gap-4 mt-4 md:mt-0 text-xs items-center">
          <div className="flex items-center gap-2 bg-white/5 px-3 py-1.5 rounded-lg border border-white/5">
            <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse shadow-[0_0_8px_#10b981]"></span>
            <span className="text-slate-400 font-mono">session_amr:</span>
            <span className="text-emerald-400 font-bold font-mono">hwk:verified</span>
          </div>

          <div className="hidden lg:flex items-center gap-4 text-[11px] text-slate-400 font-mono italic">
            <span>RP_ID: secure.hwk.internal</span>
            <span className="text-white/10">|</span>
            <span>session: 8824-X9</span>
          </div>
        </div>
      </header>

      {/* Main Content Workspace Layout */}
      <div className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-8 grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side Sidebar / Navigation Selector */}
        <div className="lg:col-span-3 flex flex-col gap-6">
          <div className="glass p-5 rounded-2xl flex flex-col gap-1.5">
            <h2 className="text-xs font-bold uppercase tracking-widest text-slate-500 px-2 mb-2">Ceremonies & Configuration</h2>
            
            <button 
              id="tab-auth"
              onClick={() => setActiveTab('auth')}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition text-left text-sm ${activeTab === 'auth' ? 'bg-emerald-500/10 text-white font-medium border-l-4 border-emerald-500' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'}`}
            >
              <Fingerprint className="w-4 h-4 text-emerald-400" />
              <div className="flex-1">
                <div>P0 Assertion Ceremony</div>
                <div className="text-[10px] text-slate-500 font-mono">Sign-In & Proof Simulation</div>
              </div>
            </button>

            <button 
              id="tab-enroll"
              onClick={() => setActiveTab('enroll')}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition text-left text-sm ${activeTab === 'enroll' ? 'bg-emerald-500/10 text-white font-medium border-l-4 border-emerald-500' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'}`}
            >
              <KeyRound className="w-4 h-4 text-emerald-400" />
              <div className="flex-1">
                <div>P1 Human Enrollment</div>
                <div className="text-[10px] text-slate-500 font-mono">WebAuthn Keys & Lifecycle</div>
              </div>
            </button>

            <button 
              id="tab-workloads"
              onClick={() => setActiveTab('workloads')}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition text-left text-sm ${activeTab === 'workloads' ? 'bg-emerald-500/10 text-white font-medium border-l-4 border-emerald-500' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'}`}
            >
              <Cpu className="w-4 h-4 text-emerald-400" />
              <div className="flex-1">
                <div>P2 Workload Keys</div>
                <div className="text-[10px] text-slate-500 font-mono">HSM & TPM Client Certs</div>
              </div>
            </button>

            <button 
              id="tab-policy"
              onClick={() => setActiveTab('policy')}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition text-left text-sm ${activeTab === 'policy' ? 'bg-emerald-500/10 text-white font-medium border-l-4 border-emerald-500' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'}`}
            >
              <Sliders className="w-4 h-4 text-emerald-400" />
              <div className="flex-1">
                <div>AMR Governance Policy</div>
                <div className="text-[10px] text-slate-500 font-mono">Attestation Policy Rules</div>
              </div>
            </button>

            <button 
              id="tab-audit"
              onClick={() => setActiveTab('audit')}
              className={`flex items-center gap-3 px-4 py-3 rounded-xl transition text-left text-sm ${activeTab === 'audit' ? 'bg-emerald-500/10 text-white font-medium border-l-4 border-emerald-500' : 'text-slate-400 hover:text-slate-200 hover:bg-white/5'}`}
            >
              <History className="w-4 h-4 text-emerald-400" />
              <div className="flex-1">
                <div>Diagnostics & Logs</div>
                <div className="text-[10px] text-slate-500 font-mono">Audit Traces & Terminal</div>
              </div>
            </button>
          </div>

          {/* Quick Active Policy Card */}
          <div className="glass-dark p-5 rounded-2xl border-white/10">
            <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400 mb-3 flex items-center justify-between">
              <span>Active Policy Status</span>
              <Settings className="w-3.5 h-3.5 text-slate-500" />
            </h3>
            <div className="space-y-3">
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">HWK Enforcement</span>
                <span className={`font-mono text-[11px] font-semibold px-1.5 py-0.5 rounded ${policy.requireHwkEvidence ? 'bg-emerald-500/15 text-emerald-400' : 'bg-slate-500/20 text-slate-400'}`}>
                  {policy.requireHwkEvidence ? 'STRICT' : 'AUDIT_ONLY'}
                </span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">User Verification</span>
                <span className="text-emerald-400 font-medium">✓ Required</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">FIDO L3 Trust Roots</span>
                <span className="text-emerald-400 font-medium">✓ Active</span>
              </div>
              <div className="flex justify-between items-center text-xs">
                <span className="text-slate-400">Synced Passkeys</span>
                <span className="text-red-400 font-medium">✗ Blocked</span>
              </div>
            </div>
            <div className="mt-4 pt-3 border-t border-white/5 flex flex-col gap-1.5 text-[11px]">
              <span className="text-slate-500">Authorized Admin Context:</span>
              <span className="text-slate-300 font-mono select-all truncate">jick.68.0@gmail.com</span>
            </div>
          </div>
        </div>

        {/* Right Side Work Area */}
        <div className="lg:col-span-9 flex flex-col gap-6">

          {/* P0 - AUTHENTICATION CEREMONY SCREEN */}
          {activeTab === 'auth' && (
            <div className="space-y-6">
              
              {/* Top description banner */}
              <div className="glass p-6 rounded-2xl flex flex-col md:flex-row gap-6 justify-between items-start md:items-center">
                <div>
                  <h2 className="text-xl font-semibold text-white">P0 - Hardware-Secured Public Key Assertion Ceremony</h2>
                  <p className="text-sm text-slate-400 mt-1">
                    Simulate real-world WebAuthn multi-factor assertion. Choose an enrolled credential to verify cryptographic evidence in real-time.
                  </p>
                </div>
                <div className="bg-emerald-500/10 border border-emerald-500/20 px-3 py-1 rounded-lg text-emerald-400 text-xs font-mono font-bold flex items-center gap-1.5 shrink-0">
                  <ShieldCheck className="w-4 h-4" /> AMR Mode: hwk
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                
                {/* Left controls: choose credential & configure transaction */}
                <div className="md:col-span-5 space-y-4">
                  <div className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">1. Select Target Authenticator</h3>
                    
                    <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
                      {authenticators.map((auth) => (
                        <div 
                          key={auth.id}
                          onClick={() => {
                            if (ceremony.status !== 'user_gesture') {
                              setSelectedCredForAuth(auth.id);
                            }
                          }}
                          className={`p-3 rounded-xl border text-left cursor-pointer transition flex items-center gap-3 ${selectedCredForAuth === auth.id ? 'bg-emerald-500/10 border-emerald-500/50 shadow-[0_0_12px_rgba(16,185,129,0.1)]' : 'bg-white/5 border-white/5 hover:border-white/10 hover:bg-white/10'} ${ceremony.status === 'user_gesture' ? 'pointer-events-none opacity-60' : ''}`}
                        >
                          <div className={`p-1.5 rounded-lg ${auth.backing === 'verified_hwk' ? 'bg-emerald-500/10 text-emerald-400' : 'bg-slate-500/15 text-slate-400'}`}>
                            {auth.type === 'platform' ? <Smartphone className="w-4 h-4" /> : <Usb className="w-4 h-4" />}
                          </div>
                          
                          <div className="flex-grow min-w-0">
                            <div className="text-xs font-semibold text-white truncate">{auth.name}</div>
                            <div className="flex items-center gap-1.5 mt-0.5">
                              <span className="text-[9px] font-mono text-slate-400 uppercase">{auth.type}</span>
                              <span className="text-[9px] text-slate-500 font-mono">•</span>
                              <span className="text-[9px] font-mono text-slate-400 uppercase">{auth.algorithm}</span>
                            </div>
                          </div>

                          <div className="shrink-0 flex flex-col items-end gap-1">
                            <KeyBackingBadge backing={auth.backing} />
                            {auth.status !== 'active' && (
                              <span className="text-[9px] text-amber-400 font-bold uppercase">{auth.status}</span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="space-y-2 pt-2">
                      <label className="text-xs text-slate-400 block font-medium">2. Ceremony Transaction Context</label>
                      <textarea 
                        value={txPurpose}
                        onChange={(e) => setTxPurpose(e.target.value)}
                        disabled={ceremony.status === 'user_gesture'}
                        rows={2}
                        className="w-full bg-black/30 border border-white/10 rounded-xl p-2.5 text-xs focus:border-emerald-500 focus:outline-none text-slate-300 disabled:opacity-60"
                        placeholder="Cryptographic challenge transaction context..."
                      />
                    </div>

                    <button
                      onClick={startAuthCeremony}
                      disabled={ceremony.status === 'user_gesture'}
                      className="w-full py-3 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-semibold text-xs tracking-wider uppercase transition shadow-lg shadow-emerald-950/20 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                      <Play className="w-4 h-4 text-slate-950 fill-current" />
                      Trigger Ceremony Proof
                    </button>
                  </div>
                </div>

                {/* Right side: Active device/OS ceremony viewport simulation */}
                <div className="md:col-span-7 flex flex-col">
                  
                  {/* Outer container */}
                  <div className="glass p-6 rounded-3xl flex-grow flex flex-col justify-between min-h-[350px] relative overflow-hidden">
                    
                    {/* Glowing status light depending on ceremony */}
                    <div className={`absolute top-0 left-1/2 -translate-x-1/2 w-48 h-1 transition-all duration-500 rounded-b-full ${
                      ceremony.status === 'success' ? 'bg-emerald-500 shadow-[0_0_15px_#10b981]' :
                      ceremony.status === 'failed' ? 'bg-red-500 shadow-[0_0_15px_#ef4444]' :
                      ceremony.status === 'user_gesture' ? 'bg-amber-500 animate-pulse shadow-[0_0_15px_#f59e0b]' :
                      'bg-slate-700'
                    }`}></div>

                    {/* Top status state indicator */}
                    <div className="flex justify-between items-center text-xs text-slate-400 mb-4 font-mono">
                      <span>CEREMONY_STATE: <strong className="text-white">{ceremony.status.toUpperCase()}</strong></span>
                      {ceremony.status === 'user_gesture' && (
                        <span className="text-amber-400 font-bold animate-pulse">TIMEOUT IN: {ceremony.countdown}s</span>
                      )}
                    </div>

                    {/* Central Area: Dynamic Interface based on Ceremony State */}
                    <div className="flex-grow flex flex-col items-center justify-center py-6 text-center">
                      
                      {ceremony.status === 'idle' && (
                        <div className="max-w-sm space-y-4">
                          <div className="w-16 h-16 rounded-full bg-slate-800/50 border border-white/10 flex items-center justify-center mx-auto text-slate-400">
                            <Fingerprint className="w-8 h-8" />
                          </div>
                          <div>
                            <h4 className="text-base font-semibold text-white">Ceremony Ready for Initialization</h4>
                            <p className="text-xs text-slate-400 mt-1">
                              Select a registered security key on the left, review the transaction context, then trigger the hardware assertion.
                            </p>
                          </div>
                        </div>
                      )}

                      {ceremony.status === 'preflight' && (
                        <div className="space-y-4 animate-pulse">
                          <div className="w-12 h-12 rounded-full border border-emerald-500/30 bg-emerald-500/5 flex items-center justify-center mx-auto">
                            <RefreshCw className="w-6 h-6 text-emerald-400 animate-spin" />
                          </div>
                          <div className="text-sm font-semibold text-slate-200">Evaluating client and platform prerequisites...</div>
                        </div>
                      )}

                      {ceremony.status === 'user_gesture' && (
                        <div className="max-w-md w-full space-y-6">
                          
                          {/* Animated Target Graphic */}
                          <div className="relative mx-auto w-24 h-24 flex items-center justify-center">
                            <div className="absolute inset-0 rounded-full bg-emerald-500/5 border border-emerald-500/20 animate-ping"></div>
                            <div className="absolute inset-2 rounded-full bg-emerald-500/10 border border-emerald-500/30 animate-pulse"></div>
                            <div className="relative w-16 h-16 rounded-full bg-emerald-950/40 border border-emerald-500/40 flex items-center justify-center text-emerald-400 shadow-[0_0_15px_rgba(16,185,129,0.2)]">
                              {ceremony.authenticatorType === 'platform' ? <Fingerprint className="w-8 h-8" /> : <Usb className="w-8 h-8" />}
                            </div>
                          </div>

                          <div className="space-y-2">
                            <h4 className="text-lg font-bold text-white flex items-center justify-center gap-2">
                              {ceremony.authenticatorType === 'platform' ? 'Biometric Touch Verification Required' : 'Insert / Touch Your Security Key'}
                            </h4>
                            <p className="text-xs text-slate-300 leading-relaxed max-w-sm mx-auto">
                              Authorized origin <span className="font-mono text-emerald-400">secure.hwk.internal</span> requests public key signature for step-up access.
                            </p>
                          </div>

                          {/* Quick details of simulated key */}
                          <div className="bg-black/30 rounded-xl p-3 max-w-xs mx-auto border border-white/5 space-y-1.5 text-left text-[11px]">
                            <div className="flex justify-between">
                              <span className="text-slate-500">Target Token</span>
                              <span className="text-slate-300 truncate font-semibold">
                                {authenticators.find(a => a.id === ceremony.chosenMethodId)?.name}
                              </span>
                            </div>
                            <div className="flex justify-between">
                              <span className="text-slate-500">Expected AMR</span>
                              <span className="text-emerald-400 font-mono font-bold">hwk:verified</span>
                            </div>
                          </div>

                          {/* Action emulation drawer (acting as physical finger touch) */}
                          <div className="bg-emerald-500/5 border border-emerald-500/10 p-4 rounded-xl text-center space-y-3">
                            <p className="text-[11px] text-slate-400 italic">Simulate user interaction by touching the virtual key below:</p>
                            <div className="flex justify-center gap-2">
                              <button 
                                onClick={handleCeremonyTouch}
                                className="px-5 py-2 bg-emerald-500 text-slate-950 font-bold text-xs rounded-lg hover:bg-emerald-400 active:scale-95 transition flex items-center gap-2 shadow-lg shadow-emerald-500/20"
                              >
                                <Fingerprint className="w-4 h-4 text-slate-950" />
                                Touch Security Key Sensor
                              </button>
                              <button 
                                onClick={() => handleCeremonyError('cancelled')}
                                className="px-4 py-2 bg-white/5 border border-white/10 text-xs font-semibold rounded-lg hover:bg-white/10 text-slate-300 transition"
                              >
                                Cancel Gesture
                              </button>
                            </div>
                          </div>
                        </div>
                      )}

                      {ceremony.status === 'success' && (
                        <div className="max-w-md space-y-5 animate-fadeIn">
                          <div className="w-16 h-16 rounded-full bg-emerald-500/10 border border-emerald-500/30 flex items-center justify-center mx-auto text-emerald-400 shadow-[0_0_20px_rgba(16,185,129,0.3)]">
                            <CheckCircle2 className="w-10 h-10" />
                          </div>
                          
                          <div>
                            <h4 className="text-lg font-bold text-white">Cryptographic Proof Accepted</h4>
                            <p className="text-xs text-emerald-400 font-mono mt-0.5">amr_evidence_class = hwk:verified (High Assurance L3)</p>
                            <p className="text-xs text-slate-400 mt-2 max-w-xs mx-auto">
                              Challenge response verified. Authorized access granted to your current session.
                            </p>
                          </div>

                          {/* Provenance Metadata review */}
                          <div className="bg-black/30 rounded-2xl p-4 border border-white/5 text-left text-xs space-y-2 max-w-xs mx-auto">
                            <div className="flex justify-between items-center pb-1.5 border-b border-white/5">
                              <span className="text-slate-500">Key Protection</span>
                              <span className="text-white font-mono text-[11px] font-semibold">{ceremony.keyProtection}</span>
                            </div>
                            <div className="flex justify-between items-center pb-1.5 border-b border-white/5">
                              <span className="text-slate-500">Attestation Origin</span>
                              <span className="text-white font-mono text-[11px]">{ceremony.provenanceSource}</span>
                            </div>
                            <div className="flex justify-between items-center">
                              <span className="text-slate-500">CA Trust Root</span>
                              <span className="text-emerald-400 font-mono text-[11px] truncate max-w-[140px]" title={ceremony.trustRoot}>
                                {ceremony.trustRoot}
                              </span>
                            </div>
                          </div>

                          <button 
                            onClick={resetCeremony}
                            className="px-5 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-semibold text-slate-300 transition"
                          >
                            Return to Dashboard
                          </button>
                        </div>
                      )}

                      {ceremony.status === 'failed' && (
                        <div className="max-w-md space-y-5">
                          <div className="w-16 h-16 rounded-full bg-red-500/10 border border-red-500/30 flex items-center justify-center mx-auto text-red-400 shadow-[0_0_20px_rgba(239,68,68,0.2)]">
                            <XCircle className="w-10 h-10" />
                          </div>
                          
                          <div>
                            <h4 className="text-lg font-bold text-white">Assertion Signature Rejected</h4>
                            <p className="text-xs text-red-400 font-mono mt-0.5">amr_evidence_class = unavailable</p>
                            <p className="text-xs text-slate-400 mt-2 max-w-xs mx-auto">
                              {ceremony.errorMsg}
                            </p>
                          </div>

                          {/* Fallback & Recovery paths as requested by Brief */}
                          <div className="bg-red-500/5 border border-red-500/15 p-4 rounded-xl text-left max-w-sm mx-auto space-y-2.5">
                            <h5 className="text-xs font-semibold text-red-400 flex items-center gap-1.5">
                              <AlertTriangle className="w-3.5 h-3.5" /> Approved Fallback Channels
                            </h5>
                            <p className="text-[11px] text-slate-300">
                              Direct hardware verification failed. Active policy permits administrative fallback to registered security keys over USB/NFC.
                            </p>
                            <div className="flex gap-2 pt-1">
                              <button 
                                onClick={startAuthCeremony}
                                className="px-3 py-1.5 bg-white/10 hover:bg-white/15 rounded text-[11px] font-semibold text-white transition flex items-center gap-1"
                              >
                                <RefreshCw className="w-3 h-3" /> Retry WebAuthn
                              </button>
                              <button 
                                onClick={() => {
                                  // Emulate fall back to platform OTP
                                  alert('Administrative Bypass: Initiated MFA recovery context. Secure push notification delivered to registered hardware device.');
                                  addLog('Bypass Initiated', 'authentication', 'warning', 'Initiated fallback push token notification due to hardware assertion fail.');
                                }}
                                className="px-3 py-1.5 bg-red-950/40 text-red-300 hover:bg-red-900/30 rounded text-[11px] font-semibold transition"
                              >
                                Trigger Backup Push Notification
                              </button>
                            </div>
                          </div>

                          <button 
                            onClick={resetCeremony}
                            className="px-5 py-2 bg-white/5 hover:bg-white/10 border border-white/10 rounded-lg text-xs font-semibold text-slate-300 transition"
                          >
                            Reset Workspace
                          </button>
                        </div>
                      )}

                    </div>

                    {/* Outer Footer/Metadata Area */}
                    <div className="mt-4 pt-3 border-t border-white/5 flex flex-wrap gap-x-4 gap-y-2 text-[11px] text-slate-500 font-mono">
                      <span>Ceremony Log: <span className="text-slate-300">{ceremony.currentStep}</span></span>
                    </div>

                  </div>

                </div>

              </div>

            </div>
          )}

          {/* P1 - HUMAN ENROLLMENT & LIFECYCLE */}
          {activeTab === 'enroll' && (
            <div className="space-y-6">
              
              {/* Introduction header */}
              <div className="glass p-6 rounded-2xl">
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <KeyRound className="w-5 h-5 text-emerald-400" />
                  P1 - Human Public Key Enrollment Panel
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Configure and register high-assurance hardware tokens. Verified hardware attestation grants the session <code className="text-emerald-400 font-bold bg-white/5 px-1 rounded">hwk</code> classification.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                
                {/* Left Form: Key Creator */}
                <div className="md:col-span-5">
                  <form onSubmit={startEnrollment} className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Enroll New Authenticator</h3>
                    
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400 font-medium block">Key Custom Label</label>
                      <input 
                        type="text" 
                        value={enrollName}
                        onChange={(e) => setEnrollName(e.target.value)}
                        required
                        className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        placeholder="e.g. Back-up Blue Key 5 NFC"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Key Class</label>
                        <select 
                          value={enrollType}
                          onChange={(e) => setEnrollType(e.target.value as 'platform' | 'roaming')}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="roaming">Roaming Security Key</option>
                          <option value="platform">Platform Passkey</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Algorithm</label>
                        <select 
                          value={enrollAlgorithm}
                          onChange={(e) => setEnrollAlgorithm(e.target.value as 'ES256' | 'RS256' | 'EdDSA')}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="ES256">ES256 (ECDSA P-256)</option>
                          <option value="RS256">RS256 (RSA 2048)</option>
                          <option value="EdDSA">EdDSA (Ed25519)</option>
                        </select>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs text-slate-400 font-medium block">Attestation Format</label>
                      <select 
                        value={enrollAttestation}
                        onChange={(e) => setEnrollAttestation(e.target.value as any)}
                        className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                      >
                        <option value="packed">Packed Attestation Certificate</option>
                        <option value="tpm">TPM v2.0 Endorsement Proof</option>
                        <option value="apple-anonymous">Apple Anonymous Hardware Cert</option>
                        <option value="none">None (Self-Signed / Synced Token)</option>
                      </select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs text-slate-400 font-medium block">FIDO AAGUID Registry Profile</label>
                      <select 
                        value={enrollAaguid}
                        onChange={(e) => setEnrollAaguid(e.target.value)}
                        className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                      >
                        {attestationRoots.map(root => (
                          <option key={root.aaguid} value={root.aaguid}>
                            {root.name} ({root.manufacturer})
                          </option>
                        ))}
                      </select>
                    </div>

                    <div className="space-y-2">
                      <label className="text-xs text-slate-400 font-medium block">Supported Transports</label>
                      <div className="grid grid-cols-2 gap-2">
                        {['usb', 'nfc', 'ble', 'internal'].map(transport => (
                          <label key={transport} className="flex items-center gap-2 bg-black/20 p-2 rounded-lg text-xs cursor-pointer border border-white/5 hover:border-white/10">
                            <input 
                              type="checkbox" 
                              checked={enrollTransport.includes(transport as any)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setEnrollTransport([...enrollTransport, transport as any]);
                                } else {
                                  setEnrollTransport(enrollTransport.filter(t => t !== transport));
                                }
                              }}
                              className="accent-emerald-500"
                            />
                            <span className="font-mono text-slate-300 uppercase text-[10px]">{transport}</span>
                          </label>
                        ))}
                      </div>
                    </div>

                    <button 
                      type="submit"
                      disabled={isEnrollingActive}
                      className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs tracking-wider uppercase rounded-xl transition flex items-center justify-center gap-2"
                    >
                      {isEnrollingActive ? (
                        <>
                          <RefreshCw className="w-4 h-4 animate-spin text-slate-950" />
                          Verifying Attestation...
                        </>
                      ) : (
                        <>
                          <Plus className="w-4 h-4 text-slate-950" />
                          Enroll Authenticator
                        </>
                      )}
                    </button>
                  </form>
                </div>

                {/* Right Panel: Authenticator Directory List */}
                <div className="md:col-span-7 space-y-4">
                  <div className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Active Human Authenticator Directory</h3>

                    <div className="space-y-3">
                      {authenticators.map((auth) => (
                        <div key={auth.id} className="bg-black/30 border border-white/5 rounded-xl p-4 flex flex-col md:flex-row justify-between items-start md:items-center gap-4 hover:border-white/10 transition">
                          <div className="space-y-1 flex-grow">
                            <div className="flex items-center gap-2 flex-wrap">
                              <h4 className="text-sm font-semibold text-white">{auth.name}</h4>
                              <span className="bg-white/5 border border-white/10 text-[9px] text-slate-300 px-1.5 py-0.5 rounded font-mono uppercase">{auth.type}</span>
                              <KeyBackingBadge backing={auth.backing} />
                            </div>
                            
                            <div className="space-y-1 text-xs text-slate-400 mt-1">
                              <div><span className="text-slate-500 font-mono text-[10px]">AAGUID:</span> <code className="text-slate-300 font-mono text-[10px] select-all">{auth.aaguid}</code></div>
                              <div><span className="text-slate-500 font-mono text-[10px]">Trust CA:</span> <span className="text-slate-300 italic">{auth.trustRoot}</span></div>
                              <div className="flex items-center gap-4 text-[10px] text-slate-500 font-mono pt-1">
                                <span>Created: {new Date(auth.created).toLocaleDateString()}</span>
                                <span>Used: {auth.lastUsed === 'Never Used' ? 'Never' : new Date(auth.lastUsed).toLocaleDateString()}</span>
                              </div>
                            </div>

                            <div className="flex items-center gap-1.5 pt-2 flex-wrap">
                              {auth.transports.map(t => (
                                <TransportBadge key={t} transport={t} />
                              ))}
                              <span className="bg-emerald-500/10 text-emerald-400 font-mono text-[9px] px-1.5 py-0.5 rounded border border-emerald-500/20">{auth.algorithm}</span>
                            </div>
                          </div>

                          <div className="shrink-0 flex md:flex-col items-end gap-2 justify-between w-full md:w-auto border-t md:border-t-0 pt-3 md:pt-0 border-white/5">
                            <div className="flex items-center gap-2">
                              <StatusIndicator status={auth.status} />
                              {auth.status === 'active' ? (
                                <button 
                                  type="button"
                                  onClick={() => toggleAuthenticatorStatus(auth.id, 'suspended')}
                                  className="text-[10px] hover:text-white bg-amber-500/10 text-amber-400 px-2 py-1 rounded border border-amber-500/20 transition"
                                >
                                  Suspend
                                </button>
                              ) : (
                                <button 
                                  type="button"
                                  onClick={() => toggleAuthenticatorStatus(auth.id, 'active')}
                                  className="text-[10px] hover:text-white bg-emerald-500/10 text-emerald-400 px-2 py-1 rounded border border-emerald-500/20 transition"
                                >
                                  Activate
                                </button>
                              )}
                            </div>

                            <button 
                              type="button"
                              onClick={() => removeAuthenticator(auth.id)}
                              className="text-[10px] hover:text-white bg-red-500/10 text-red-400 px-2 py-1 rounded border border-red-500/20 transition flex items-center gap-1"
                            >
                              <Trash2 className="w-3 h-3" />
                              Revoke
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>

              </div>

            </div>
          )}

          {/* P2 - CLIENT & WORKLOAD REGISTRATION */}
          {activeTab === 'workloads' && (
            <div className="space-y-6">
              
              {/* Introduction */}
              <div className="glass p-6 rounded-2xl">
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <Cpu className="w-5 h-5 text-emerald-400" />
                  P2 - Client & Workload Key Infrastructure
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Bind server-side machine client keys, JWT JWKS, or X509 certificates. The workbench verifies cryptographic origin and hardware assurance roots prior to traffic activation.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                
                {/* Registration Form */}
                <div className="md:col-span-5 space-y-4">
                  <form onSubmit={registerWorkloadKey} className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Register Client Key / Cert</h3>
                    
                    <div className="space-y-1">
                      <label className="text-xs text-slate-400 font-medium block">Workload Name</label>
                      <input 
                        type="text" 
                        value={wlName}
                        onChange={(e) => setWlName(e.target.value)}
                        required
                        className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        placeholder="e.g. Analytics Webhook Signer"
                      />
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs text-slate-400 font-medium block">Identity Profile Profile</label>
                      <input 
                        type="text" 
                        value={wlProfile}
                        onChange={(e) => setWlProfile(e.target.value)}
                        required
                        className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        placeholder="e.g. Production Publisher Agent"
                      />
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Algorithm</label>
                        <select 
                          value={wlAlg}
                          onChange={(e) => setWlAlg(e.target.value as any)}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="ES256">ES256</option>
                          <option value="RS256">RS256</option>
                          <option value="EdDSA">EdDSA</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Material Type</label>
                        <select 
                          value={wlMaterialType}
                          onChange={(e) => {
                            const val = e.target.value as 'jwks' | 'certificate' | 'csr';
                            setWlMaterialType(val);
                            if (val === 'jwks') setWlMaterialText(sampleJWKS);
                            else if (val === 'certificate') setWlMaterialText(sampleCert);
                            else if (val === 'csr') setWlMaterialText(sampleCSR);
                          }}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="jwks">JWK Set / JWKS</option>
                          <option value="certificate">X.509 Certificate</option>
                          <option value="csr">CSR Request</option>
                        </select>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 gap-3">
                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Key Protection</label>
                        <select 
                          value={wlProtection}
                          onChange={(e) => {
                            const val = e.target.value as 'HSM' | 'TPM' | 'Software';
                            setWlProtection(val);
                            if (val === 'HSM') {
                              setWlProvenance('Hardware-backed YubiHSM 2 Attestation Chain');
                            } else if (val === 'TPM') {
                              setWlProvenance('Intel TXT TPM 2.0 Endorsement Proof');
                            } else {
                              setWlProvenance('No Attestation (Client CSR Self-Signed)');
                            }
                          }}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="HSM">Hardware HSM</option>
                          <option value="TPM">Enclave TPM</option>
                          <option value="Software">Software Only</option>
                        </select>
                      </div>

                      <div>
                        <label className="text-xs text-slate-400 font-medium block mb-1">Provenance</label>
                        <input 
                          type="text" 
                          value={wlProvenance}
                          readOnly
                          className="w-full bg-black/20 border border-white/10 rounded-xl px-3 py-2 text-xs text-slate-400 select-none cursor-not-allowed"
                        />
                      </div>
                    </div>

                    <div className="space-y-1">
                      <label className="text-xs text-slate-400 font-medium block">Public Material Content</label>
                      <textarea 
                        value={wlMaterialText}
                        onChange={(e) => setWlMaterialText(e.target.value)}
                        required
                        rows={5}
                        className="w-full bg-black/40 border border-white/10 rounded-xl p-2 text-[10px] font-mono focus:border-emerald-500 focus:outline-none text-slate-300"
                        placeholder="Insert public PEM certificates, public JWK sets, etc."
                      />
                    </div>

                    <button 
                      type="submit"
                      className="w-full py-3 bg-emerald-600 hover:bg-emerald-500 text-slate-950 font-bold text-xs tracking-wider uppercase rounded-xl transition flex items-center justify-center gap-2"
                    >
                      <Plus className="w-4 h-4 text-slate-950" />
                      Register Public Key material
                    </button>
                  </form>
                </div>

                {/* Directory list of client keys */}
                <div className="md:col-span-7 space-y-4">
                  <div className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Registered Machine Credentials</h3>

                    <div className="space-y-4">
                      {workloadKeys.map((key) => (
                        <div key={key.id} className="bg-black/30 border border-white/5 rounded-xl p-4 space-y-3 hover:border-white/10 transition">
                          <div className="flex flex-wrap items-start justify-between gap-2">
                            <div>
                              <h4 className="text-sm font-semibold text-white">{key.name}</h4>
                              <p className="text-xs text-slate-400 italic">Profile: {key.profileName}</p>
                            </div>
                            <div className="flex items-center gap-2">
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded uppercase ${key.keyProtection !== 'Software' ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-red-500/10 text-red-400 border border-red-500/20'}`}>
                                {key.keyProtection} PROTECTED
                              </span>
                              <span className="bg-white/5 text-slate-300 border border-white/10 text-[9px] px-1.5 py-0.5 rounded font-mono uppercase">{key.materialType}</span>
                            </div>
                          </div>

                          <div className="text-xs text-slate-400 space-y-1 bg-black/20 p-3 rounded-lg border border-white/5 font-mono">
                            <div><span className="text-slate-500">FINGERPRINT:</span> <span className="text-slate-300">{key.fingerprint}</span></div>
                            <div><span className="text-slate-500">PROVENANCE :</span> <span className="text-slate-300">{key.provenanceSource}</span></div>
                            <div className="flex justify-between items-center text-[10px] text-slate-500 pt-2">
                              <span>VERIFIED: {new Date(key.lastVerified).toLocaleDateString()}</span>
                              <span>EXPIRES: {new Date(key.expiry).toLocaleDateString()}</span>
                            </div>
                          </div>

                          {/* Key overlap rotation timeline & synthetic validation tester */}
                          <div className="flex flex-wrap items-center justify-between gap-3 pt-2 border-t border-white/5">
                            <div className="flex gap-2">
                              <button 
                                type="button"
                                onClick={() => testWorkloadSignature(key)}
                                className="text-[10px] hover:text-white bg-emerald-500/10 text-emerald-400 px-3 py-1.5 rounded border border-emerald-500/20 transition flex items-center gap-1.5"
                              >
                                <Scan className="w-3 h-3 text-emerald-400" />
                                Test Synthetic Proof
                              </button>
                              
                              <button 
                                type="button"
                                onClick={() => triggerRotation(key.id)}
                                disabled={isRotating === key.id}
                                className="text-[10px] hover:text-white bg-white/5 text-slate-300 hover:bg-white/10 px-3 py-1.5 rounded border border-white/10 transition flex items-center gap-1.5 disabled:opacity-40"
                              >
                                <RotateCw className={`w-3 h-3 ${isRotating === key.id ? 'animate-spin text-emerald-400' : 'text-slate-400'}`} />
                                {isRotating === key.id ? 'Rotating...' : 'Rotate Overlap'}
                              </button>
                            </div>

                            {/* Timeline display */}
                            <div className="flex items-center gap-1.5 text-[10px] text-slate-500">
                              <span className="w-2 h-2 rounded-full bg-emerald-500"></span>
                              <span>Active</span>
                              <ChevronRight className="w-3 h-3 text-slate-600" />
                              <span className="w-2 h-2 rounded-full bg-slate-700"></span>
                              <span>Prior Retired</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>

                    {/* Signature output sandbox container */}
                    {testResult && (
                      <div className="p-4 bg-black/40 rounded-xl border border-white/10 space-y-2">
                        <h4 className="text-xs font-bold uppercase tracking-wider text-slate-400 flex items-center justify-between">
                          <span>Verification Diagnostics Result</span>
                          <button onClick={() => setTestResult('')} className="text-slate-500 hover:text-slate-300 text-[10px]">Dismiss</button>
                        </h4>
                        <pre className="text-[10px] font-mono text-slate-300 leading-relaxed whitespace-pre-wrap">{testResult}</pre>
                      </div>
                    )}

                  </div>
                </div>

              </div>

            </div>
          )}

          {/* P2 - AMR GOVERNANCE POLICY ADMINISTRATION */}
          {activeTab === 'policy' && (
            <div className="space-y-6">
              
              {/* Introduction Banner */}
              <div className="glass p-6 rounded-2xl">
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <Sliders className="w-5 h-5 text-emerald-400" />
                  P2 - Administrative Authentication & Attestation Governance
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Enforce strict cryptographic limits for local FIDO2 metadata and platform passkeys. Simulate missing attestation fallback flows instantly.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-12 gap-6">
                
                {/* Policy Settings Column */}
                <div className="md:col-span-6 space-y-4">
                  <div className="glass p-5 rounded-2xl space-y-4">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Governance Configurations</h3>
                    
                    <div className="space-y-4 pt-2">
                      <div className="flex items-start justify-between gap-4 bg-black/20 p-3 rounded-xl border border-white/5">
                        <div>
                          <label className="text-xs font-semibold text-white block">Strict AMR hwk Evidence</label>
                          <span className="text-[10px] text-slate-400 block mt-0.5">Show & verify hwk only with signed hardware certificates.</span>
                        </div>
                        <input 
                          type="checkbox" 
                          checked={policy.requireHwkEvidence}
                          onChange={(e) => {
                            setPolicy({ ...policy, requireHwkEvidence: e.target.checked });
                            addLog('Policy Adjusted', 'policy', 'warning', `Require hardware evidence set to: ${e.target.checked}`);
                          }}
                          className="w-4 h-4 accent-emerald-500 shrink-0 mt-1"
                        />
                      </div>

                      <div className="flex items-start justify-between gap-4 bg-black/20 p-3 rounded-xl border border-white/5">
                        <div>
                          <label className="text-xs font-semibold text-white block">Reject Synced Passkeys</label>
                          <span className="text-[10px] text-slate-400 block mt-0.5">Synced cloud keys (iCloud/Google) trigger software-only downgrade.</span>
                        </div>
                        <input 
                          type="checkbox" 
                          checked={!policy.allowSyncedPasskeys}
                          onChange={(e) => {
                            setPolicy({ ...policy, allowSyncedPasskeys: !e.target.checked });
                            addLog('Policy Adjusted', 'policy', 'warning', `Blocked cloud synced keys: ${e.target.checked}`);
                          }}
                          className="w-4 h-4 accent-emerald-500 shrink-0 mt-1"
                        />
                      </div>

                      <div className="space-y-2">
                        <label className="text-xs text-slate-400 block font-medium">User Verification Requirement</label>
                        <select 
                          value={policy.userVerification}
                          onChange={(e) => {
                            setPolicy({ ...policy, userVerification: e.target.value as any });
                            addLog('Policy Adjusted', 'policy', 'warning', `Required User Verification state set to: ${e.target.value.toUpperCase()}`);
                          }}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200"
                        >
                          <option value="required">Required (Biometrics / Token PIN mandated)</option>
                          <option value="preferred">Preferred (Allowed fallback to silent touch)</option>
                          <option value="discouraged">Discouraged</option>
                        </select>
                      </div>

                      <div className="space-y-2">
                        <label className="text-xs text-slate-400 block font-medium">Approved Cryptographic Signature Algs</label>
                        <div className="grid grid-cols-3 gap-2">
                          {['ES256', 'RS256', 'EdDSA'].map(alg => (
                            <label key={alg} className="flex items-center gap-2 bg-black/20 p-2 rounded-lg text-[11px] cursor-pointer border border-white/5 hover:border-white/10">
                              <input 
                                type="checkbox" 
                                checked={policy.allowedAlgorithms.includes(alg as any)}
                                onChange={(e) => {
                                  if (e.target.checked) {
                                    setPolicy({ ...policy, allowedAlgorithms: [...policy.allowedAlgorithms, alg as any] });
                                  } else {
                                    setPolicy({ ...policy, allowedAlgorithms: policy.allowedAlgorithms.filter(a => a !== alg) });
                                  }
                                  addLog('Policy Adjusted', 'policy', 'warning', `Adjusted algorithm parameters for standard: ${alg}`);
                                }}
                                className="accent-emerald-500"
                              />
                              <span className="font-mono text-slate-300">{alg}</span>
                            </label>
                          ))}
                        </div>
                      </div>

                      <div className="space-y-2">
                        <label className="text-xs text-slate-400 block font-medium">Grace Period for Compromised Key Overlap (Days)</label>
                        <input 
                          type="number" 
                          min={0}
                          max={30}
                          value={policy.gracePeriodDays}
                          onChange={(e) => setPolicy({ ...policy, gracePeriodDays: parseInt(e.target.value) || 0 })}
                          className="w-full bg-black/30 border border-white/10 rounded-xl px-3 py-2 text-xs focus:border-emerald-500 focus:outline-none text-slate-200 font-mono"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Simulation Sandbox Column */}
                <div className="md:col-span-6 space-y-4">
                  
                  {/* Attestation Authority Directory List */}
                  <div className="glass p-5 rounded-2xl space-y-3">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Trusted AAGUID Authorities</h3>
                    
                    <div className="space-y-2 max-h-[190px] overflow-y-auto pr-1">
                      {attestationRoots.map(root => (
                        <div key={root.aaguid} className="bg-black/30 p-2.5 rounded-lg border border-white/5 text-xs flex justify-between items-center gap-4">
                          <div>
                            <div className="font-semibold text-slate-200 truncate max-w-[190px]">{root.name}</div>
                            <div className="text-[10px] text-slate-500 font-mono">{root.manufacturer}</div>
                          </div>
                          <div className="flex gap-2 shrink-0">
                            <TrustRootBadge level={root.certificationLevel} />
                            <span className={`text-[9px] font-mono font-bold px-1.5 py-0.5 rounded ${root.hardwareBacking === 'verified_hwk' ? 'text-emerald-400 bg-emerald-500/10' : 'text-slate-400 bg-slate-500/10'}`}>
                              {root.hardwareBacking === 'verified_hwk' ? 'HWK' : 'SOFT'}
                            </span>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* Outage and lockout simulation playground */}
                  <div className="glass p-5 rounded-2xl space-y-3">
                    <h3 className="text-xs font-bold uppercase tracking-widest text-slate-400 flex items-center gap-1.5">
                      <AlertTriangle className="w-4 h-4 text-amber-400" />
                      Policy Simulation Laboratory
                    </h3>
                    <p className="text-[11px] text-slate-400">
                      Instantly simulate credential edge-cases or hardware authentication failures to test high-assurance enforcement.
                    </p>

                    <div className="grid grid-cols-2 gap-2 pt-1">
                      <button 
                        type="button"
                        onClick={() => {
                          // Simulate synced token lockout
                          const syncedKey = authenticators.find(a => a.backing === 'software_only');
                          if (syncedKey) {
                            setSelectedCredForAuth(syncedKey.id);
                            startAuthCeremony();
                            addLog('Simulated Locker', 'policy', 'warning', 'Triggered test sequence for iCloud Synced token. Evaluated high policy enforcement.');
                          } else {
                            alert('No software-only or synced keys currently registered in human folder.');
                          }
                        }}
                        className="p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl text-left transition"
                      >
                        <div className="text-xs font-semibold text-white">Simulate Synced Lockout</div>
                        <span className="text-[9px] text-slate-500 font-mono">Blocks low-assurance key</span>
                      </button>

                      <button 
                        type="button"
                        onClick={() => {
                          // Simulate attestation provider outage
                          alert('Outage Simulated: Metadata Provider Outage Triggered. FIDO AAGUID Trust verification falls back to grace period enforcement logs.');
                          addLog('Provider Outage Sim', 'system', 'warning', 'Simulated attestation provider network outage. Grace period logic activated.');
                        }}
                        className="p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl text-left transition"
                      >
                        <div className="text-xs font-semibold text-white">Metadata Outage</div>
                        <span className="text-[9px] text-slate-500 font-mono">Test attestation backup grace</span>
                      </button>

                      <button 
                        type="button"
                        onClick={() => {
                          // Simulate compromised-key warning
                          alert('Compromise Simulated: Titans series token [auth-titan-key] flagged as compromised on public threat metadata.');
                          setAuthenticators(prev => prev.map(a => {
                            if (a.id === 'auth-titan-key') {
                              return { ...a, status: 'suspended' };
                            }
                            return a;
                          }));
                          addLog('Compromised Key Warning', 'policy', 'failure', 'Titans security token flagged as compromised on public registers. Key suspended.');
                        }}
                        className="p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl text-left transition"
                      >
                        <div className="text-xs font-semibold text-white">Compromised Key Response</div>
                        <span className="text-[9px] text-slate-500 font-mono">Test key revocation loop</span>
                      </button>

                      <button 
                        type="button"
                        onClick={() => {
                          // Simulate lockout warning
                          alert('Safety Check: Verified that you have backup authenticators configured. Administrative lockout validation passed.');
                        }}
                        className="p-2 bg-white/5 hover:bg-white/10 border border-white/5 rounded-xl text-left transition"
                      >
                        <div className="text-xs font-semibold text-white">Verify Backup Overlap</div>
                        <span className="text-[9px] text-slate-500 font-mono">Lockout protection test</span>
                      </button>
                    </div>

                  </div>

                </div>

              </div>

            </div>
          )}

          {/* DIAGNOSTICS & AUDITING TERMINAL VIEW */}
          {activeTab === 'audit' && (
            <div className="space-y-6">
              
              <div className="glass p-6 rounded-2xl">
                <h2 className="text-xl font-semibold text-white flex items-center gap-2">
                  <Terminal className="w-5 h-5 text-emerald-400" />
                  P2 - Cryptographic Audit & Validation Workspace
                </h2>
                <p className="text-sm text-slate-400 mt-1">
                  Query low-level attestation metadata, print synthetic verification diagnostics, and audit hardware lifecycle changes.
                </p>
              </div>

              {/* CLI Validator Workbench */}
              <div className="glass p-5 rounded-2xl space-y-4">
                <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Validation Diagnostics Console (Mock CLI)</h3>
                
                <CLICommandOutput 
                  command={cliCommand}
                  output={cliOutput}
                />

                <div className="flex flex-col md:flex-row gap-3 items-start md:items-center justify-between">
                  <div className="flex flex-wrap gap-2">
                    <button 
                      onClick={() => runPresetCliCommand('hwk-verify --credential auth-yubikey-5c')}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/15 text-slate-300 rounded text-xs transition"
                    >
                      Audit YubiKey FIDO2
                    </button>
                    <button 
                      onClick={() => runPresetCliCommand('hwk-verify --credential auth-mac-touchid')}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/15 text-slate-300 rounded text-xs transition"
                    >
                      Audit TouchID Enclave
                    </button>
                    <button 
                      onClick={() => runPresetCliCommand('hwk-verify --credential auth-icloud-sync')}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/15 text-slate-300 rounded text-xs transition"
                    >
                      Audit Synced Token
                    </button>
                    <button 
                      onClick={() => runPresetCliCommand('hwk-policy-check')}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/15 text-slate-300 rounded text-xs transition"
                    >
                      Dump Policy Config
                    </button>
                    <button 
                      onClick={() => runPresetCliCommand('hwk-fido2-list')}
                      className="px-3 py-1.5 bg-white/5 hover:bg-white/10 border border-white/15 text-slate-300 rounded text-xs transition"
                    >
                      List Registered Tokens
                    </button>
                  </div>

                  <span className="text-[10px] text-slate-500 font-mono italic">
                    CLI Tools accept public parameters only, no private material is stored.
                  </span>
                </div>
              </div>

              {/* Real-time Audit logs */}
              <div className="glass p-5 rounded-2xl space-y-4">
                <div className="flex justify-between items-center">
                  <h3 className="text-xs font-bold uppercase tracking-widest text-slate-500">Security Audit Logs</h3>
                  <button 
                    onClick={() => {
                      setAuditLogs(initialAuditLogs);
                      addLog('Audit logs cleared', 'system', 'warning', 'Operator cleared diagnostic audit console display.');
                    }}
                    className="text-[10px] text-slate-400 hover:text-white transition"
                  >
                    Clear Display
                  </button>
                </div>

                <div className="space-y-2 max-h-[350px] overflow-y-auto pr-1">
                  {auditLogs.map((log) => (
                    <div key={log.id} className="bg-black/20 border border-white/5 rounded-xl p-3 flex items-start gap-3 hover:border-white/10 transition">
                      
                      {/* Log Category Badge */}
                      <span className={`w-2 h-2 rounded-full shrink-0 mt-1.5 ${
                        log.status === 'success' ? 'bg-emerald-500 shadow-[0_0_8px_#10b981]' :
                        log.status === 'warning' ? 'bg-amber-500 shadow-[0_0_8px_#f59e0b]' :
                        'bg-red-500 shadow-[0_0_8px_#ef4444]'
                      }`}></span>

                      <div className="flex-grow space-y-0.5">
                        <div className="flex flex-wrap items-center justify-between gap-x-2 gap-y-1">
                          <span className="text-xs font-semibold text-white">{log.event}</span>
                          <span className="text-[9px] text-slate-500 font-mono">{new Date(log.timestamp).toLocaleTimeString()}</span>
                        </div>
                        <p className="text-[11px] text-slate-400 leading-relaxed">{log.details}</p>
                        <div className="flex items-center gap-3 text-[9px] text-slate-500 font-mono pt-1">
                          <span>CATEGORY: {log.category.toUpperCase()}</span>
                          <span>•</span>
                          <span>ACTOR: {log.actor}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

            </div>
          )}

        </div>

      </div>

      {/* Footer */}
      <footer className="mt-auto py-4 px-8 border-t border-white/5 glass-dark text-[10px] font-mono text-slate-500 flex flex-col md:flex-row justify-between items-center gap-4">
        <div className="flex gap-4">
          <span>RP_ID: secure.hwk.internal</span>
          <span>ORIGIN: https://auth.corp.net</span>
        </div>
        <div className="flex gap-4 items-center">
          <span className="text-emerald-500/70 uppercase tracking-widest font-semibold">Hardware Assurance: High (L3)</span>
          <span className="opacity-30">|</span>
          <span>Build 2.4.0-release</span>
        </div>
      </footer>
    </div>
  );
}
