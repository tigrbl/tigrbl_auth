import React, { useState, useEffect } from 'react';
import {
  Key,
  ShieldCheck,
  Smartphone,
  CheckCircle,
  AlertTriangle,
  RotateCcw,
  Lock,
  Unlock,
  Settings,
  Clipboard,
  UserCheck,
  RefreshCw,
  FileText,
  XCircle,
  Plus,
  Trash2,
  HelpCircle,
  Activity,
  Info,
  ShieldAlert,
  Eye,
  EyeOff,
  Layers,
  Settings2,
  BookOpen,
  ArrowRight,
  HardDrive,
  Cpu,
  Fingerprint,
  FileCode,
  LockKeyhole
} from 'lucide-react';

import { AMRMode, PinState, AuditEvent, SimulatedServerState, ExternalDeviceProfile } from './types';
import { SecurePinField } from './components/SecurePinField';
import { PinRequirements } from './components/PinRequirements';
import { PinResetArtifactState } from './components/PinResetArtifactState';
import { PinLifecyclePanel } from './components/PinLifecyclePanel';
import {
  CompatibilityNotice,
  AuthenticationContextSummary,
  EvidenceFreshnessBadge,
  MethodSwitchMenu,
  ExternalPinGuidance,
  DeviceBlockedHelp
} from './components/Aesthetics';
import {
  INITIAL_SERVER_STATE,
  hashPin,
  checkDisallowedPatterns,
  createAuditLog
} from './mockServer';

export default function App() {
  // --- Active Screen/Context Selector ---
  // To satisfy the 19 screens, we list them as direct view tabs.
  // The user can interactively select any screen, or click buttons inside a flow that transitions them automatically.
  type ScreenID =
    // P0 - Actual authentication UIX
    | 'passkey-login'
    | 'step-up-chooser'
    | 'webauthn-handoff'
    | 'security-key-instructions'
    | 'native-device-auth'
    | 'result-next-step'
    | 'evidence-detail'
    | 'auth-key-card-detail'
    | 'recovery-fallback'
    // P1 - Enrollment and user lifecycle
    | 'first-party-intro'
    | 'first-party-creation'
    | 'first-party-login-stepup'
    | 'first-party-detail-change'
    | 'first-party-suspend-revoke'
    | 'first-party-forgot-reset'
    // P2 - Administration and operations
    | 'user-verification-policy'
    | 'device-provider-config'
    | 'audit-diagnostics'
    | 'first-party-admin-policy';

  const [activeScreen, setActiveScreen] = useState<ScreenID>('first-party-intro');

  // --- Simulated Server State ---
  const [serverState, setServerState] = useState<SimulatedServerState>(INITIAL_SERVER_STATE);

  // --- Simulated Client State ---
  const [clientPinInput, setClientPinInput] = useState('');
  const [clientConfirmInput, setClientConfirmInput] = useState('');
  const [clientCurrentPinInput, setClientCurrentPinInput] = useState('');
  const [clientError, setClientError] = useState<string | null>(null);
  const [clientSuccess, setClientSuccess] = useState<string | null>(null);
  const [recentStrongAuth, setRecentStrongAuth] = useState(false);
  const [evidenceFreshnessTimestamp, setEvidenceFreshnessTimestamp] = useState<string | null>(null);
  const [activeRecoveryArtifact, setActiveRecoveryArtifact] = useState<string | null>(null);
  const [recoveryUsed, setRecoveryUsed] = useState(false);

  // --- External Device Verification Handshake Simulation States ---
  const [externalAuthState, setExternalAuthState] = useState<'idle' | 'pending' | 'success' | 'failed' | 'canceled'>('idle');
  const [selectedExternalDevice, setSelectedExternalDevice] = useState<'passkey' | 'roaming-key' | 'smart-card' | 'native-biometric'>('roaming-key');
  const [trustedEvidenceResult, setTrustedEvidenceResult] = useState<{
    provenance: string;
    isPinVerified: boolean;
    verificationMethod: string;
    time: string;
  } | null>(null);

  // --- Audit Ledger State ---
  const [auditLogs, setAuditLogs] = useState<AuditEvent[]>([
    createAuditLog('System Bootstrapped', 'system' as any, 'info', 'PIN AMR framework initialized successfully.'),
    createAuditLog('Policy Loaded', 'policy', 'info', 'Default TIGRBL first-party PIN requirements enforced.'),
  ]);

  // Help push state to audit ledger
  const pushAuditLog = (log: AuditEvent) => {
    setAuditLogs((prev) => [log, ...prev]);
  };

  // Safe wrapper to trigger recent strong auth
  const handleTriggerRecentStrongAuth = () => {
    setRecentStrongAuth(true);
    pushAuditLog(
      createAuditLog('Strong Authentication Performed', 'authentication', 'success', 'User performed multi-factor check to unlock secure lifecycle operations.')
    );
    setClientSuccess('Recent strong authentication verified (MFA token active).');
    setTimeout(() => setClientSuccess(null), 3000);
  };

  // --- Simulated Server Operations (Verifier Contract) ---

  // 1. PIN Enrollment
  const handleEnrollPin = (pin: string, confirm: string) => {
    setClientError(null);
    setClientSuccess(null);

    if (pin !== confirm) {
      setClientError('PIN confirmation does not match the initial entry.');
      pushAuditLog(
        createAuditLog('Enrollment Failed', 'lifecycle', 'failure', 'Confirmation mismatch detected during first-party PIN creation.')
      );
      return;
    }

    const policyError = checkDisallowedPatterns(pin, serverState.policy);
    if (policyError) {
      setClientError(policyError);
      pushAuditLog(
        createAuditLog('Enrollment Failed', 'policy', 'failure', `PIN rejected due to policy breach: ${policyError}`)
      );
      return;
    }

    // Hash verifier securely (client never stores or outputs this value)
    const verifierHash = hashPin(pin);

    setServerState((prev) => ({
      ...prev,
      isFirstPartyEnrolled: true,
      firstPartyVerifierHash: verifierHash,
      remainingAttempts: prev.policy.maxAttempts,
      status: 'active',
    }));

    pushAuditLog(
      createAuditLog('First-Party PIN Enrolled', 'lifecycle', 'success', 'New secure verifier hash recorded. PIN activated atomically.', 'tigrbl-server-verifier')
    );

    setClientPinInput('');
    setClientConfirmInput('');
    setClientSuccess('PIN enrolled and activated successfully! Secure verifier recorded.');
    // Transition automatically to detail page
    setTimeout(() => {
      setActiveScreen('first-party-detail-change');
      setClientSuccess(null);
    }, 1500);
  };

  // 2. PIN Validation (Verification Challenge)
  const handleVerifyPinChallenge = (pin: string) => {
    setClientError(null);
    setClientSuccess(null);

    if (!serverState.isFirstPartyEnrolled || !serverState.firstPartyVerifierHash) {
      setClientError('No active first-party PIN verifier exists on the server.');
      return;
    }

    if (serverState.status === 'locked' || serverState.status === 'compromised' || serverState.remainingAttempts <= 0) {
      setClientError('Account PIN is currently locked or blocked due to security violations. Please use recovery options.');
      pushAuditLog(
        createAuditLog('Verification Blocked', 'authentication', 'failure', 'Challenge blocked due to locked/compromised credential status.')
      );
      return;
    }

    const inputHash = hashPin(pin);
    const isValid = inputHash === serverState.firstPartyVerifierHash;

    if (isValid) {
      // Success
      setServerState((prev) => ({
        ...prev,
        remainingAttempts: prev.policy.maxAttempts, // Reset retry counter on success
      }));
      setEvidenceFreshnessTimestamp(new Date().toISOString());
      setClientPinInput('');
      setClientSuccess('PIN verification successful! Cryptographic evidence token generated.');
      
      pushAuditLog(
        createAuditLog('PIN Challenge Verified', 'authentication', 'success', 'Verifier matched. Authentication Method Reference verified as "pin".', 'first-party-verifier')
      );

      // Auto route to result evidence detail screen
      setTimeout(() => {
        setActiveScreen('result-next-step');
        setClientSuccess(null);
      }, 1500);
    } else {
      // Failed attempt
      const newAttempts = Math.max(0, serverState.remainingAttempts - 1);
      const isLocked = newAttempts === 0;

      setServerState((prev) => ({
        ...prev,
        remainingAttempts: newAttempts,
        status: isLocked ? 'locked' : prev.status,
      }));

      setClientPinInput('');
      setClientError(
        isLocked
          ? 'Incorrect PIN. Maximum attempt limit reached. Credential locked.'
          : `Incorrect PIN. Remaining attempts: ${newAttempts}`
      );

      pushAuditLog(
        createAuditLog(
          isLocked ? 'Verifier Locked Out' : 'Verifier Match Failed',
          'authentication',
          isLocked ? 'failure' : 'warning',
          isLocked
            ? 'Account PIN locked due to consecutive authentication failures.'
            : `Failed PIN challenge. Remaining attempts: ${newAttempts}`
        )
      );
    }
  };

  // 3. Change / Replace PIN
  const handleChangePin = (current: string, next: string, nextConfirm: string) => {
    setClientError(null);
    setClientSuccess(null);

    if (!recentStrongAuth) {
      setClientError('Strong authentication safeguard required before editing credential.');
      return;
    }

    if (!serverState.isFirstPartyEnrolled || !serverState.firstPartyVerifierHash) {
      setClientError('No active first-party PIN enrolled.');
      return;
    }

    // Verify current PIN first
    const currentHash = hashPin(current);
    if (currentHash !== serverState.firstPartyVerifierHash) {
      setClientError('Current PIN is incorrect. Operation denied.');
      pushAuditLog(
        createAuditLog('PIN Change Rejected', 'lifecycle', 'failure', 'Incorrect current PIN supplied during replacement request.')
      );
      return;
    }

    if (next !== nextConfirm) {
      setClientError('New PIN confirmation does not match.');
      return;
    }

    const policyError = checkDisallowedPatterns(next, serverState.policy);
    if (policyError) {
      setClientError(policyError);
      return;
    }

    // Update verifier atomically
    const newHash = hashPin(next);
    setServerState((prev) => ({
      ...prev,
      firstPartyVerifierHash: newHash,
      remainingAttempts: prev.policy.maxAttempts,
      status: 'active',
    }));

    pushAuditLog(
      createAuditLog('PIN Replaced Atomically', 'lifecycle', 'success', 'Active verifier replaced with new secure credential hash. Old verifier retired.')
    );

    setClientCurrentPinInput('');
    setClientPinInput('');
    setClientConfirmInput('');
    setClientSuccess('PIN changed successfully! Old verifier retired atomically.');
    setTimeout(() => setClientSuccess(null), 3000);
  };

  // 4. Recovery Artifact Handlers
  const handleInitiateReset = () => {
    const code = `TIGRBL-REC-${Math.floor(1000 + Math.random() * 9000)}-${Math.floor(1000 + Math.random() * 9000)}`;
    setActiveRecoveryArtifact(code);
    setRecoveryUsed(false);
    pushAuditLog(
      createAuditLog('Recovery Ceremony Initiated', 'lifecycle', 'info', 'Bound recovery secret artifact token generated.')
    );
  };

  const handleVerifyArtifact = (code: string): boolean => {
    if (!activeRecoveryArtifact || code !== activeRecoveryArtifact) {
      pushAuditLog(
        createAuditLog('Recovery Code Rejected', 'lifecycle', 'failure', 'Replay or invalid recovery artifact submitted.')
      );
      return false;
    }
    if (recoveryUsed) {
      pushAuditLog(
        createAuditLog('Recovery Code Reuse Stopped', 'lifecycle', 'failure', 'Attempted replay of expired recovery token.')
      );
      return false;
    }
    return true;
  };

  const handleCompleteNewPin = (newPin: string) => {
    const policyError = checkDisallowedPatterns(newPin, serverState.policy);
    if (policyError) {
      pushAuditLog(
        createAuditLog('Recovery PIN Failure', 'policy', 'failure', `New PIN rejected: ${policyError}`)
      );
      return;
    }

    const newHash = hashPin(newPin);
    setServerState((prev) => ({
      ...prev,
      isFirstPartyEnrolled: true,
      firstPartyVerifierHash: newHash,
      remainingAttempts: prev.policy.maxAttempts,
      status: 'active',
    }));

    setRecoveryUsed(true);
    setActiveRecoveryArtifact(null);

    pushAuditLog(
      createAuditLog('Recovery Complete', 'lifecycle', 'success', 'Credential unlocked via recovery token. New verifier active.')
    );

    setClientSuccess('Recovery completed successfully! New secure PIN is active.');
    setTimeout(() => {
      setActiveScreen('first-party-login-stepup');
      setClientSuccess(null);
    }, 1500);
  };

  // 5. Lifecycle Status Modification
  const handleLifecycleAction = (action: string) => {
    if (action === 'suspend') {
      setServerState((prev) => ({ ...prev, status: 'suspended' }));
      pushAuditLog(createAuditLog('PIN Suspended', 'lifecycle', 'warning', 'Credential temporarily suspended by user or system rules.'));
    } else if (action === 'resume') {
      setServerState((prev) => ({ ...prev, status: 'active' }));
      pushAuditLog(createAuditLog('PIN Resumed', 'lifecycle', 'success', 'Credential suspension lifted. Status restored to active.'));
    } else if (action === 'compromise') {
      setServerState((prev) => ({ ...prev, status: 'compromised' }));
      pushAuditLog(createAuditLog('PIN Declared Compromised', 'lifecycle', 'failure', 'Critical security alert: PIN marked as compromised. Enrollment required.', 'user-report'));
    } else if (action === 'force-reset') {
      setServerState((prev) => ({ ...prev, status: 'forced-reset' }));
      pushAuditLog(createAuditLog('Admin Forced Reset', 'admin', 'warning', 'Administrator triggered forced-reset state. Permanent PIN retired until next setup.'));
      setActiveScreen('first-party-forgot-reset');
    } else if (action === 'remove') {
      // safeguard check
      setServerState((prev) => ({
        ...prev,
        isFirstPartyEnrolled: false,
        firstPartyVerifierHash: null,
        status: 'active',
      }));
      pushAuditLog(createAuditLog('PIN Removed', 'lifecycle', 'warning', 'First-party credential purged from server. SAFELIGHT verification active.'));
    }
  };

  // --- External Verification Handshake Simulation Logic ---
  const handleSimulateExternalHandshake = (type: typeof selectedExternalDevice) => {
    setExternalAuthState('pending');
    pushAuditLog(
      createAuditLog(
        `WebAuthn Handoff Initialized`,
        'hardware',
        'info',
        `Contacting platform authenticator engine for device: ${type}...`
      )
    );

    setTimeout(() => {
      if (serverState.providerOutage) {
        setExternalAuthState('failed');
        pushAuditLog(createAuditLog('WebAuthn Handoff Failed', 'hardware', 'failure', 'Service provider outage simulation intercepted connection.'));
        return;
      }
      if (serverState.deviceLocked) {
        setExternalAuthState('failed');
        pushAuditLog(createAuditLog('WebAuthn Handoff Failed', 'hardware', 'failure', 'Connected hardware token reports locked-out state.'));
        return;
      }

      setExternalAuthState('success');
      
      // Map provenance evidence
      let provenance = 'Unknown Device';
      let isPinVerified = false;
      let verificationMethod = 'User verification only';

      if (type === 'passkey') {
        provenance = 'Trusted Platform Passkey Authenticator';
        isPinVerified = false; // "Do not claim pin when WebAuthn reports only user verification"
        verificationMethod = 'User verified (Biometric/FaceID on-device)';
      } else if (type === 'roaming-key') {
        provenance = 'FIDO2 Hardware Token (USB/NFC)';
        isPinVerified = true;
        verificationMethod = 'Hardware-based Authenticator PIN';
      } else if (type === 'smart-card') {
        provenance = 'EMV / PIV Cryptographic Smart Card';
        isPinVerified = true;
        verificationMethod = 'Smart Card Cryptographic PIN';
      } else if (type === 'native-biometric') {
        provenance = 'Device Secure Enclave';
        isPinVerified = false;
        verificationMethod = 'Native Platform Biometric Verification';
      }

      setTrustedEvidenceResult({
        provenance,
        isPinVerified,
        verificationMethod,
        time: new Date().toISOString()
      });

      pushAuditLog(
        createAuditLog(
          'WebAuthn Proof Received',
          'hardware',
          'success',
          `External verification successful. Provenance: ${provenance}. Pin Verified Claim: ${isPinVerified}`
        )
      );

      // Auto route to result detail page
      setTimeout(() => {
        setActiveScreen('result-next-step');
      }, 1000);

    }, 2000);
  };

  // Helper to test various error cases in external flow
  const handleTriggerExternalError = (errType: 'cancel' | 'disconnect' | 'timeout') => {
    setExternalAuthState('idle');
    if (errType === 'cancel') {
      setActiveScreen('recovery-fallback');
      pushAuditLog(createAuditLog('External Prompt Canceled', 'hardware', 'warning', 'User canceled native OS WebAuthn verification prompt. Routing to fallback.'));
    } else if (errType === 'disconnect') {
      setActiveScreen('security-key-instructions');
      pushAuditLog(createAuditLog('Hardware Removed', 'hardware', 'failure', 'Secure token was unplugged or disconnected during transmission.'));
    } else if (errType === 'timeout') {
      pushAuditLog(createAuditLog('Handoff Timeout', 'hardware', 'failure', 'System timed out waiting for touch sensor validation.'));
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans" id="app-root">
      
      {/* --- Elegant Dashboard Header --- */}
      <header className="border-b border-slate-900 bg-slate-950/80 backdrop-blur px-6 py-4 flex flex-col md:flex-row justify-between items-center gap-4 shrink-0">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-xl bg-gradient-to-tr from-blue-600 to-cyan-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
            <LockKeyhole size={20} className="text-white animate-pulse" />
          </div>
          <div>
            <h1 className="text-sm font-bold uppercase tracking-wider text-white">AMR Lifecycle Platform</h1>
            <p className="text-[11px] font-mono text-slate-500">FIRST-PARTY PIN & SECURE MULTI-FACTOR EVIDENCE GATEWAY</p>
          </div>
        </div>

        {/* Current status overview pill */}
        <div className="flex items-center gap-3">
          <div className="text-right">
            <span className="text-[10px] text-slate-500 uppercase tracking-wider block font-mono">Simulated Server Status</span>
            <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1.5 justify-end">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              VERIFIER ENGINE LIVE
            </span>
          </div>
        </div>
      </header>

      {/* --- Main Dual-Column Interface --- */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        
        {/* --- LEFT SIDEBAR: Interactive Screen Catalog --- */}
        <nav className="w-full lg:w-80 border-r border-slate-900 bg-slate-950 p-4 space-y-6 overflow-y-auto shrink-0 flex flex-col">
          
          <div className="space-y-1">
            <h2 className="text-[10px] font-bold text-slate-500 uppercase tracking-widest px-2">
              Authentication Stage Catalog
            </h2>
            <p className="text-[10px] text-slate-400 px-2 leading-relaxed font-mono">
              Directly select any of the 19 mandated screens below to inspect individual behaviors.
            </p>
          </div>

          {/* Group 1: P0 Actual Authentication UIX */}
          <div className="space-y-1">
            <div className="px-2 py-1 text-[10px] font-bold text-blue-400 bg-blue-950/20 rounded border border-blue-900/30 w-fit uppercase">
              P0 — Challenge & Authentication UIX
            </div>
            <div className="space-y-0.5 mt-2">
              {[
                { id: 'first-party-intro', label: '13. First-party PIN Introduction', icon: <BookOpen size={13} /> },
                { id: 'first-party-login-stepup', label: '15. First-party PIN Login/Step-up', icon: <Lock size={13} /> },
                { id: 'passkey-login', label: '1. Passkey/Security-Key Login', icon: <Key size={13} /> },
                { id: 'step-up-chooser', label: '2. Step-up Chooser', icon: <Layers size={13} /> },
                { id: 'webauthn-handoff', label: '3. WebAuthn/Device Handoff', icon: <Cpu size={13} /> },
                { id: 'security-key-instructions', label: '4. Security-Key/Card Instructions', icon: <Info size={13} /> },
                { id: 'native-device-auth', label: '5. Native Device-Auth Screen', icon: <Fingerprint size={13} /> },
                { id: 'result-next-step', label: '6. Result/Next-Step (Verification)', icon: <UserCheck size={13} /> },
                { id: 'evidence-detail', label: '7. Evidence Detail (AMR Status)', icon: <Clipboard size={13} /> },
                { id: 'recovery-fallback', label: '9. Recovery/Fallback Options', icon: <RotateCcw size={13} /> },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveScreen(item.id as ScreenID);
                    setClientError(null);
                    setClientSuccess(null);
                  }}
                  className={`w-full text-left py-2 px-3 rounded-lg text-xs font-mono flex items-center gap-2.5 transition-all cursor-pointer ${
                    activeScreen === item.id
                      ? 'bg-blue-600 text-white font-semibold'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Group 2: P1 Enrollment and user lifecycle */}
          <div className="space-y-1">
            <div className="px-2 py-1 text-[10px] font-bold text-amber-400 bg-amber-950/20 rounded border border-amber-900/30 w-fit uppercase">
              P1 — Enrollment & User Lifecycle
            </div>
            <div className="space-y-0.5 mt-2">
              {[
                { id: 'first-party-creation', label: '14. First-party PIN Enrollment', icon: <Plus size={13} /> },
                { id: 'first-party-detail-change', label: '16. PIN Detail/Change/Replace', icon: <RefreshCw size={13} /> },
                { id: 'first-party-suspend-revoke', label: '17. PIN Suspend/Revoke/Remove', icon: <XCircle size={13} /> },
                { id: 'first-party-forgot-reset', label: '18. Forgot/Reset Recovery', icon: <HelpCircle size={13} /> },
                { id: 'auth-key-card-detail', label: '8. Hardware Detail Management', icon: <Settings2 size={13} /> },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveScreen(item.id as ScreenID);
                    setClientError(null);
                    setClientSuccess(null);
                  }}
                  className={`w-full text-left py-2 px-3 rounded-lg text-xs font-mono flex items-center gap-2.5 transition-all cursor-pointer ${
                    activeScreen === item.id
                      ? 'bg-amber-600 text-white font-semibold'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Group 3: P2 Administration and operations */}
          <div className="space-y-1">
            <div className="px-2 py-1 text-[10px] font-bold text-purple-400 bg-purple-950/20 rounded border border-purple-900/30 w-fit uppercase">
              P2 — Policy & Administration
            </div>
            <div className="space-y-0.5 mt-2">
              {[
                { id: 'first-party-admin-policy', label: '19. PIN Policy & Admin Reset', icon: <Settings size={13} /> },
                { id: 'user-verification-policy', label: '10. User-Verification Policy', icon: <ShieldAlert size={13} /> },
                { id: 'device-provider-config', label: '11. Device/Provider Config', icon: <HardDrive size={13} /> },
                { id: 'audit-diagnostics', label: '12. Audit & Diagnostics Ledger', icon: <FileText size={13} /> },
              ].map((item) => (
                <button
                  key={item.id}
                  onClick={() => {
                    setActiveScreen(item.id as ScreenID);
                    setClientError(null);
                    setClientSuccess(null);
                  }}
                  className={`w-full text-left py-2 px-3 rounded-lg text-xs font-mono flex items-center gap-2.5 transition-all cursor-pointer ${
                    activeScreen === item.id
                      ? 'bg-purple-600 text-white font-semibold'
                      : 'text-slate-400 hover:bg-slate-900 hover:text-slate-200'
                  }`}
                >
                  {item.icon}
                  <span>{item.label}</span>
                </button>
              ))}
            </div>
          </div>

          {/* Quick status box */}
          <div className="mt-auto pt-4 border-t border-slate-900 text-[10px] font-mono text-slate-500 space-y-1.5">
            <div>
              <span>FP enrolled: </span>
              <span className={serverState.isFirstPartyEnrolled ? 'text-emerald-400 font-bold' : 'text-rose-400'}>
                {serverState.isFirstPartyEnrolled ? 'YES' : 'NO'}
              </span>
            </div>
            <div>
              <span>FP Attempts Left: </span>
              <span className="text-slate-300 font-bold">{serverState.remainingAttempts}</span>
            </div>
            <div>
              <span>FP Verifier status: </span>
              <span className="text-yellow-400 uppercase font-bold">{serverState.status}</span>
            </div>
          </div>
        </nav>

        {/* --- CENTER COLUMN: The Live Stage Frame --- */}
        <main className="flex-1 bg-slate-900/40 p-4 md:p-6 overflow-y-auto flex flex-col items-center">
          
          <div className="w-full max-w-2xl bg-slate-950 rounded-2xl border border-slate-900 shadow-2xl flex flex-col overflow-hidden min-h-[600px]">
            
            {/* Live device frame top bezel bar */}
            <div className="bg-slate-950 border-b border-slate-900 px-4 py-3 flex justify-between items-center text-xs font-mono text-slate-500">
              <div className="flex items-center gap-1.5">
                <span className="h-2 w-2 rounded-full bg-blue-500" />
                <span className="text-[10px] tracking-wider">SECURE CLIENT CONTAINER VIEW</span>
              </div>
              <div className="text-[10px] uppercase tracking-wider text-slate-400 bg-slate-900/60 px-2 py-0.5 rounded border border-slate-800">
                Active Screen: <span className="text-blue-400 font-bold font-mono">{activeScreen}</span>
              </div>
            </div>

            {/* Content Stage */}
            <div className="p-6 md:p-8 flex-1 flex flex-col justify-between space-y-6">
              
              {/* Client messages */}
              {clientError && (
                <div className="bg-red-950/20 text-red-400 text-xs p-3.5 rounded-xl border border-red-900/40 font-mono text-left">
                  ⚠️ <span className="font-bold">CLIENT WARNING:</span> {clientError}
                </div>
              )}
              {clientSuccess && (
                <div className="bg-emerald-950/20 text-emerald-400 text-xs p-3.5 rounded-xl border border-emerald-900/40 font-mono text-left">
                  ✓ <span className="font-bold">CLIENT SUCCESS:</span> {clientSuccess}
                </div>
              )}

              {/* SCREEN RENDERING ENGINE */}
              <div className="flex-1 flex flex-col justify-center">
                
                {/* 13. First-party PIN Introduction */}
                {activeScreen === 'first-party-intro' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-fp-intro">
                    <div className="h-12 w-12 rounded-full bg-blue-950 border border-blue-800 flex items-center justify-center mx-auto text-blue-400">
                      <BookOpen size={24} />
                    </div>
                    <div className="space-y-2">
                      <h2 className="text-lg font-bold tracking-tight text-white">Introduce Account-Level PIN</h2>
                      <p className="text-xs text-slate-400 leading-relaxed">
                        Secure your TIGRBL workspace credentials by registering an account-level PIN. This PIN acts as a personal local authenticator verifier managed solely by our isolated host server boundary.
                      </p>
                    </div>

                    <div className="bg-slate-900/60 border border-slate-800 p-4 rounded-xl text-left space-y-3 font-mono text-[11px] text-slate-400">
                      <div className="font-bold text-slate-300">ACCOUNT SCOPE & POLICIES</div>
                      <ul className="space-y-1.5 list-disc list-inside">
                        <li>Length: 6 to 12 cryptographic digits.</li>
                        <li>Uniqueness: Sequences or identical patterns are blocked.</li>
                        <li>Assurance level: Single-factor knowledge method with rate-limiting.</li>
                        <li>No hardware required. Supports recovery fallback options.</li>
                      </ul>
                    </div>

                    <div className="flex flex-col sm:flex-row gap-3">
                      <button
                        type="button"
                        onClick={() => setActiveScreen('first-party-creation')}
                        className="flex-1 py-2.5 px-4 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs tracking-wider uppercase transition-all cursor-pointer"
                      >
                        Enroll New PIN Now
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveScreen('step-up-chooser')}
                        className="flex-1 py-2.5 px-4 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 font-semibold text-xs tracking-wider uppercase transition-all cursor-pointer"
                      >
                        See Other Modalities
                      </button>
                    </div>
                  </div>
                )}

                {/* 14. First-party PIN Creation/Confirmation */}
                {activeScreen === 'first-party-creation' && (
                  <div className="space-y-6 text-center max-w-sm mx-auto" id="screen-fp-creation">
                    <div>
                      <h2 className="text-base font-bold text-white">Enroll TIGRBL-Owned PIN</h2>
                      <p className="text-xs text-slate-400">
                        Input and confirm your new account-level secure knowledge PIN.
                      </p>
                    </div>

                    <div className="space-y-4">
                      <div className="space-y-1 text-left">
                        <label className="text-[10px] font-bold text-slate-400 uppercase">1. Create PIN</label>
                        <input
                          type="password"
                          maxLength={12}
                          value={clientPinInput}
                          onChange={(e) => setClientPinInput(e.target.value.replace(/[^0-9]/g, ''))}
                          placeholder="••••••"
                          className="w-full text-center tracking-[0.3em] font-mono text-lg py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-100"
                        />
                      </div>

                      <div className="space-y-1 text-left">
                        <label className="text-[10px] font-bold text-slate-400 uppercase">2. Confirm PIN</label>
                        <input
                          type="password"
                          maxLength={12}
                          value={clientConfirmInput}
                          onChange={(e) => setClientConfirmInput(e.target.value.replace(/[^0-9]/g, ''))}
                          placeholder="••••••"
                          className="w-full text-center tracking-[0.3em] font-mono text-lg py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-slate-100"
                        />
                      </div>
                    </div>

                    <PinRequirements pin={clientPinInput} policy={serverState.policy} />

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => handleEnrollPin(clientPinInput, clientConfirmInput)}
                        disabled={clientPinInput.length === 0 || clientConfirmInput.length === 0}
                        className="flex-1 py-2.5 bg-blue-600 hover:bg-blue-500 disabled:opacity-40 text-white rounded-xl text-xs font-semibold uppercase tracking-wider transition-all cursor-pointer"
                      >
                        Activate Verifier
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setClientPinInput('');
                          setClientConfirmInput('');
                          setActiveScreen('first-party-intro');
                        }}
                        className="py-2.5 px-4 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-400 rounded-xl text-xs font-semibold cursor-pointer"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {/* 15. First-party PIN Login/Step-up */}
                {activeScreen === 'first-party-login-stepup' && (
                  <div className="space-y-6 text-center max-w-sm mx-auto" id="screen-fp-login">
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Challenge Account PIN</h2>
                      <p className="text-xs text-slate-400">Provide your secure verifier credential to confirm access.</p>
                    </div>

                    <AuthenticationContextSummary purpose="Sensitive Workspace Action" payloadAmount="$1,450.00 USD" amrMode="first-party" />

                    <SecurePinField
                      id="fp-pin-challenge"
                      value={clientPinInput}
                      onChange={setClientPinInput}
                      onSubmit={() => handleVerifyPinChallenge(clientPinInput)}
                      maxLength={serverState.policy.maxLength}
                      disabled={serverState.status === 'locked' || serverState.status === 'compromised'}
                      error={serverState.status === 'locked' ? 'This credential is locked. Please use recovery options.' : undefined}
                    />

                    {serverState.status === 'locked' && (
                      <div className="space-y-2">
                        <p className="text-xs text-red-400 font-mono">Verifier lockout triggered.</p>
                        <button
                          type="button"
                          onClick={() => setActiveScreen('first-party-forgot-reset')}
                          className="text-xs text-blue-400 hover:underline font-semibold cursor-pointer"
                        >
                          Recover Account PIN Now →
                        </button>
                      </div>
                    )}
                  </div>
                )}

                {/* 1. Passkey/Security-Key Login */}
                {activeScreen === 'passkey-login' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-passkey-login">
                    <div className="h-12 w-12 rounded-full bg-blue-950 border border-blue-900 text-blue-400 flex items-center justify-center mx-auto">
                      <Key size={24} />
                    </div>
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white font-sans">Passkey & Hardware Login</h2>
                      <p className="text-xs text-slate-400">Initiate secure passwordless verification using WebAuthn standard.</p>
                    </div>

                    <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800 text-left text-xs text-slate-300 font-mono space-y-2">
                      <span className="font-bold text-blue-400 block uppercase text-[10px]">PRE-HANDOFF NOTICE</span>
                      <p className="leading-relaxed">
                        To guarantee high-assurance credentials, your browser will trigger a system-controlled prompt. You may be requested to present your biometrics, enter an operating system PIN, or touch your roaming security key.
                      </p>
                      <span className="text-emerald-400 text-[10px] block font-bold">✓ APP UI WILL NOT CAPTURE OR SEE YOUR DEVICE PIN.</span>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-left">
                      <button
                        type="button"
                        onClick={() => {
                          setSelectedExternalDevice('passkey');
                          setActiveScreen('webauthn-handoff');
                        }}
                        className="p-3 bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-slate-700 rounded-xl text-xs font-mono font-bold text-slate-200 flex flex-col space-y-1 cursor-pointer transition-all"
                      >
                        <span>Platform Passkey</span>
                        <span className="text-[9px] text-slate-500 font-normal uppercase">On-Device Hello / Apple TouchID</span>
                      </button>

                      <button
                        type="button"
                        onClick={() => {
                          setSelectedExternalDevice('roaming-key');
                          setActiveScreen('webauthn-handoff');
                        }}
                        className="p-3 bg-slate-900 hover:bg-slate-850 border border-slate-800 hover:border-slate-700 rounded-xl text-xs font-mono font-bold text-slate-200 flex flex-col space-y-1 cursor-pointer transition-all"
                      >
                        <span>Roaming Security Key</span>
                        <span className="text-[9px] text-slate-500 font-normal uppercase">USB / NFC FIDO2 Key</span>
                      </button>
                    </div>

                    <button
                      type="button"
                      onClick={() => setActiveScreen('step-up-chooser')}
                      className="text-xs text-slate-500 hover:text-slate-300 font-mono transition-colors"
                    >
                      ← Back to alternative chooser
                    </button>
                  </div>
                )}

                {/* 2. Step-up Chooser */}
                {activeScreen === 'step-up-chooser' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-step-up-chooser">
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Select Verification Method</h2>
                      <p className="text-xs text-slate-400">Select an eligible high-assurance credential to perform step-up challenge.</p>
                    </div>

                    <MethodSwitchMenu
                      currentMode={
                        serverState.isFirstPartyEnrolled ? 'first-party' : 'device-local'
                      }
                      onModeChange={(mode) => {
                        if (mode === 'first-party') {
                          setActiveScreen('first-party-login-stepup');
                        } else if (mode === 'device-local') {
                          setSelectedExternalDevice('native-biometric');
                          setActiveScreen('native-device-auth');
                        } else if (mode === 'authenticator-pin') {
                          setSelectedExternalDevice('roaming-key');
                          setActiveScreen('security-key-instructions');
                        } else if (mode === 'trusted-upstream') {
                          // Simulate upstream evidence
                          setTrustedEvidenceResult({
                            provenance: 'Trusted Upstream Identity Federation',
                            isPinVerified: true,
                            verificationMethod: 'Upstream PIN Authenticated assertion',
                            time: new Date().toISOString()
                          });
                          setActiveScreen('evidence-detail');
                        }
                      }}
                    />

                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-900 text-left space-y-2">
                      <span className="text-[10px] font-mono text-slate-500 block uppercase tracking-wider">ELIGIBLE METRIC</span>
                      <p className="text-xs text-slate-400 leading-relaxed font-sans">
                        First-party account PIN: {serverState.isFirstPartyEnrolled ? '🟢 Available' : '🔴 Not Enrolled'}
                      </p>
                    </div>
                  </div>
                )}

                {/* 3. WebAuthn/Device Handoff */}
                {activeScreen === 'webauthn-handoff' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-webauthn-handoff">
                    <div className="space-y-2">
                      <h2 className="text-base font-bold text-white">Invoking WebAuthn API</h2>
                      <p className="text-xs text-slate-400">Please respond to the system-controlled security prompt.</p>
                    </div>

                    {/* High-fidelity prompt mockup */}
                    <div className="bg-slate-950 p-6 rounded-2xl border border-slate-800 shadow-inner space-y-4">
                      {externalAuthState === 'pending' ? (
                        <div className="space-y-4 py-6">
                          <div className="relative h-12 w-12 mx-auto">
                            <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75" />
                            <div className="relative rounded-full h-12 w-12 bg-cyan-950 border border-cyan-800 flex items-center justify-center text-cyan-400">
                              <Cpu size={20} className="animate-pulse" />
                            </div>
                          </div>
                          <div>
                            <span className="text-xs font-mono font-bold text-cyan-400 animate-pulse block uppercase tracking-widest">AWAITING HARDWARE INTERACTION</span>
                            <span className="text-[10px] text-slate-500 font-mono uppercase block mt-1">THE SYSTEM DIALOG IS NOW ACTIVE</span>
                          </div>
                        </div>
                      ) : (
                        <div className="space-y-4 py-4">
                          <p className="text-xs text-slate-300 font-mono">
                            Ready to initiate credential handoff.
                          </p>
                          <button
                            type="button"
                            onClick={() => handleSimulateExternalHandshake(selectedExternalDevice)}
                            className="w-full py-2.5 px-4 bg-gradient-to-r from-cyan-600 to-cyan-500 hover:from-cyan-500 hover:to-cyan-400 text-white rounded-xl text-xs font-bold uppercase tracking-wider transition-all cursor-pointer"
                          >
                            Launch OS Authenticator API
                          </button>
                        </div>
                      )}
                    </div>

                    <div className="flex flex-wrap justify-center gap-2">
                      <button
                        type="button"
                        onClick={() => handleTriggerExternalError('cancel')}
                        className="py-1 px-2.5 rounded bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] font-mono text-slate-400 cursor-pointer"
                      >
                        Simulate Cancel
                      </button>
                      <button
                        type="button"
                        onClick={() => handleTriggerExternalError('disconnect')}
                        className="py-1 px-2.5 rounded bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] font-mono text-slate-400 cursor-pointer"
                      >
                        Simulate Device Removed
                      </button>
                      <button
                        type="button"
                        onClick={() => handleTriggerExternalError('timeout')}
                        className="py-1 px-2.5 rounded bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] font-mono text-slate-400 cursor-pointer"
                      >
                        Simulate Timeout
                      </button>
                    </div>

                    <ExternalPinGuidance type={selectedExternalDevice} />
                  </div>
                )}

                {/* 4. Security-key/card instructions */}
                {activeScreen === 'security-key-instructions' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-key-instructions">
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Security Key & Card Directives</h2>
                      <p className="text-xs text-slate-400">Complete guide for hardware insertion, touch, and unlock.</p>
                    </div>

                    <ExternalPinGuidance type="roaming-key" />

                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-900 space-y-3">
                      <div className="flex items-center gap-1.5 text-[11px] font-mono font-bold text-yellow-500">
                        <AlertTriangle size={13} />
                        DEVICE TROUBLESHOOTING
                      </div>
                      <p className="text-xs text-slate-400 leading-relaxed text-left">
                        If your hardware token does not respond, verify that it is properly aligned in your USB slot, or ensure NFC is turned on for mobile devices. For smart cards, verify that card middleware is active.
                      </p>
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setActiveScreen('webauthn-handoff')}
                        className="flex-1 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs uppercase tracking-wider cursor-pointer"
                      >
                        Retry Handshake
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveScreen('step-up-chooser')}
                        className="flex-1 py-2 rounded-xl bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 font-semibold text-xs uppercase tracking-wider cursor-pointer"
                      >
                        Select Fallback
                      </button>
                    </div>
                  </div>
                )}

                {/* 5. Native device-auth screen */}
                {activeScreen === 'native-device-auth' && (
                  <div className="space-y-6 text-center max-w-sm mx-auto" id="screen-native-auth">
                    <div className="h-14 w-14 rounded-full bg-cyan-950/40 border border-cyan-800/60 flex items-center justify-center mx-auto text-cyan-400 animate-pulse">
                      <Fingerprint size={28} />
                    </div>
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Native Platform Unlock</h2>
                      <p className="text-xs text-slate-400 font-sans">Triggering native device unlock challenge (FaceID / Fingerprint / OS Code).</p>
                    </div>

                    <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-850 text-left space-y-2">
                      <span className="text-[9px] font-mono text-cyan-400 font-bold block uppercase">PLATFORM DIALOG EXPECTATIONS</span>
                      <p className="text-xs text-slate-400 leading-relaxed font-mono">
                        The application is requesting a high-assurance biometric match. We receive only a signed proof of success; your biometric signatures never leave your secure platform architecture.
                      </p>
                    </div>

                    <button
                      type="button"
                      onClick={() => handleSimulateExternalHandshake('native-biometric')}
                      className="w-full py-2.5 bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-semibold text-xs tracking-wider uppercase rounded-xl cursor-pointer"
                    >
                      Authenticate On Device
                    </button>
                  </div>
                )}

                {/* 6. Result/next-step */}
                {activeScreen === 'result-next-step' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-result">
                    <div className="h-12 w-12 rounded-full bg-emerald-950/50 border border-emerald-800 flex items-center justify-center mx-auto text-emerald-400">
                      <CheckCircle size={24} />
                    </div>
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">User Verification Status</h2>
                      <p className="text-xs text-slate-400">Current authentication assertion results.</p>
                    </div>

                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-900 text-left space-y-3">
                      <div className="flex justify-between items-center text-[10px] font-mono text-slate-500 uppercase tracking-wider pb-2 border-b border-slate-900">
                        <span>VERIFICATION CLAIMS RESULT</span>
                        <span className="text-emerald-400 font-bold">SUCCESS</span>
                      </div>

                      <div className="space-y-2 text-xs font-mono">
                        <div>
                          <span className="text-slate-600 block text-[9px] uppercase tracking-wider">Assertion Level</span>
                          {trustedEvidenceResult?.isPinVerified ? (
                            <span className="text-emerald-400 font-bold">🟢 USER VERIFIED + TRUSTED PIN EVIDENCE PROVENANCE</span>
                          ) : (
                            <span className="text-amber-400 font-bold">🟡 User Verified (Biometric / PIN Provenance Not Disclosed)</span>
                          )}
                        </div>

                        <div>
                          <span className="text-slate-600 block text-[9px] uppercase tracking-wider">Device Provenance Source</span>
                          <span className="text-slate-300 font-medium">{trustedEvidenceResult?.provenance || 'First-Party Server Verifier Contract'}</span>
                        </div>

                        <div>
                          <span className="text-slate-600 block text-[9px] uppercase tracking-wider">Verification Timestamp</span>
                          <span className="text-slate-400">{trustedEvidenceResult?.time || new Date().toISOString()}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => setActiveScreen('evidence-detail')}
                        className="flex-1 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-semibold uppercase tracking-wider cursor-pointer"
                      >
                        Inspect Evidence Detail
                      </button>
                      <button
                        type="button"
                        onClick={() => setActiveScreen('step-up-chooser')}
                        className="py-2 px-4 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 rounded-xl text-xs font-semibold cursor-pointer"
                      >
                        Reset Flow
                      </button>
                    </div>
                  </div>
                )}

                {/* 7. Evidence detail */}
                {activeScreen === 'evidence-detail' && (
                  <div className="space-y-6 text-center max-w-md mx-auto" id="screen-evidence-detail">
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Cryptographic Evidence Details</h2>
                      <p className="text-xs text-slate-400">Inspecting exact AMR metadata and claim constraints.</p>
                    </div>

                    <div className="bg-slate-950 p-5 rounded-2xl border border-slate-850 text-left space-y-4">
                      <div className="border-b border-slate-900 pb-3 flex justify-between items-center">
                        <span className="text-[10px] font-mono text-slate-500 uppercase tracking-widest">AMR CLAIMS VECTOR</span>
                        <span className="text-cyan-400 font-bold font-mono text-[10px]">VERIFIED</span>
                      </div>

                      <div className="space-y-3 text-xs font-mono">
                        <div className="grid grid-cols-2 gap-2 border-b border-slate-900/40 pb-2">
                          <span className="text-slate-500">Method Reference (amr):</span>
                          <span className="text-slate-300 text-right">["pin", "hw", "user_presence"]</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 border-b border-slate-900/40 pb-2">
                          <span className="text-slate-500">Device Provenance:</span>
                          <span className="text-emerald-400 text-right font-semibold">{trustedEvidenceResult?.provenance || 'TIGRBL Secure Verifier Boundary'}</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2 border-b border-slate-900/40 pb-2">
                          <span className="text-slate-500">Security Counter:</span>
                          <span className="text-slate-300 text-right">N/A (Masked by secure middleware)</span>
                        </div>
                        <div className="grid grid-cols-2 gap-2">
                          <span className="text-slate-500">Provenance Trust Class:</span>
                          <span className="text-slate-300 text-right">Class-A Hardware / Server Verifier</span>
                        </div>
                      </div>

                      <div className="bg-slate-900 p-3 rounded-lg border border-slate-800 text-[10px] text-slate-400 font-sans leading-relaxed">
                        🔒 <span className="font-bold text-slate-300 font-mono">SECURITY ASSURANCE:</span> Raw PIN value, verifier hashes, retry limits, and recovery configurations are strictly redacted and never exposed to public DOM contexts.
                      </div>
                    </div>

                    <button
                      type="button"
                      onClick={() => setActiveScreen('step-up-chooser')}
                      className="w-full py-2 bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 font-semibold text-xs tracking-wider uppercase rounded-xl cursor-pointer"
                    >
                      Return To Method Chooser
                    </button>
                  </div>
                )}

                {/* 8. Authenticator/key/card detail */}
                {activeScreen === 'auth-key-card-detail' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-hardware-detail">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">Underlying Authenticator Management</h2>
                      <p className="text-xs text-slate-400">Manage connected physical tokens and passkeys (not PIN values).</p>
                    </div>

                    <div className="space-y-3">
                      {[
                        { name: 'YubiKey 5C NFC', type: 'USB Roaming Security Key', serial: 'SN-9824871', registered: '2026-03-12' },
                        { name: 'Apple TouchID Platform Key', type: 'Built-in Secure Enclave', serial: 'Built-In Platform', registered: '2026-01-05' },
                      ].map((dev, idx) => (
                        <div key={idx} className="bg-slate-950 p-4 rounded-xl border border-slate-850 flex justify-between items-center">
                          <div className="space-y-1">
                            <h4 className="text-xs font-bold text-slate-200">{dev.name}</h4>
                            <span className="text-[10px] font-mono text-slate-500 uppercase block">{dev.type}</span>
                            <span className="text-[9px] font-mono text-slate-600">Registered: {dev.registered}</span>
                          </div>
                          <div className="text-right space-y-1.5">
                            <span className="text-[9px] font-mono font-bold bg-emerald-950/40 text-emerald-400 border border-emerald-900 px-2 py-0.5 rounded">ACTIVE</span>
                            <button
                              type="button"
                              onClick={() => {
                                pushAuditLog(createAuditLog('Token Deregistered', 'hardware', 'warning', `Deregistered device: ${dev.name}. Serial: ${dev.serial}`));
                                setClientSuccess(`Purged token ${dev.name} successfully.`);
                                setTimeout(() => setClientSuccess(null), 3000);
                              }}
                              className="text-[10px] font-semibold text-red-400 hover:underline block text-right cursor-pointer"
                            >
                              Deregister Key
                            </button>
                          </div>
                        </div>
                      ))}
                    </div>

                    <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-850/60 text-xs text-slate-400 space-y-2">
                      <span className="font-bold text-slate-300 block text-[10px] uppercase">LIFECYCLE SAFEGUARD LIMITATION</span>
                      <p className="leading-relaxed font-mono text-[10px]">
                        The client does NOT have access to reset or change the PIN of external hardware keys. To change hardware-level PINs, please utilize your operating system settings panel or device companion app.
                      </p>
                    </div>
                  </div>
                )}

                {/* 9. Recovery/fallback */}
                {activeScreen === 'recovery-fallback' && (
                  <div className="space-y-6 text-center max-w-sm mx-auto" id="screen-fallback">
                    <div className="h-12 w-12 rounded-full bg-yellow-950/50 border border-yellow-850 flex items-center justify-center mx-auto text-yellow-400 animate-pulse">
                      <RotateCcw size={22} />
                    </div>
                    <div className="space-y-1">
                      <h2 className="text-base font-bold text-white">Alternative Verification</h2>
                      <p className="text-xs text-slate-400">Your primary verification method was canceled or is currently blocked.</p>
                    </div>

                    <div className="space-y-3 text-left">
                      <button
                        type="button"
                        onClick={() => setActiveScreen('first-party-login-stepup')}
                        className="w-full p-4 bg-slate-900 hover:bg-slate-850 border border-slate-800 rounded-xl flex items-center justify-between cursor-pointer transition-all"
                      >
                        <div className="space-y-0.5">
                          <span className="text-xs font-bold text-slate-200 block">Use First-Party Account PIN</span>
                          <span className="text-[10px] text-slate-500 font-mono">Verify via TIGRBL server verifier.</span>
                        </div>
                        <ArrowRight size={14} className="text-slate-400" />
                      </button>

                      <button
                        type="button"
                        onClick={() => setActiveScreen('first-party-forgot-reset')}
                        className="w-full p-4 bg-slate-900 hover:bg-slate-850 border border-slate-800 rounded-xl flex items-center justify-between cursor-pointer transition-all"
                      >
                        <div className="space-y-0.5">
                          <span className="text-xs font-bold text-slate-200 block">Initiate Secure PIN Recovery</span>
                          <span className="text-[10px] text-slate-500 font-mono">Bypass with bound recovery token.</span>
                        </div>
                        <ArrowRight size={14} className="text-slate-400" />
                      </button>
                    </div>
                  </div>
                )}

                {/* 16. PIN Detail/Change/Replace */}
                {activeScreen === 'first-party-detail-change' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-fp-detail">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white font-sans">First-Party Account PIN Details</h2>
                      <p className="text-xs text-slate-400">View status and perform atomic replacements securely.</p>
                    </div>

                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-3 font-mono text-xs">
                      <div className="flex justify-between items-center border-b border-slate-900 pb-2">
                        <span className="text-slate-500 text-[10px] uppercase">VERIFIER STATUS</span>
                        <span className="text-emerald-400 font-bold uppercase">{serverState.status}</span>
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <span className="text-slate-500">Remaining Retries:</span>
                        <span className="text-slate-200 text-right font-bold">{serverState.remainingAttempts}</span>
                      </div>

                      <div className="grid grid-cols-2 gap-2">
                        <span className="text-slate-500">Active Hash Digest:</span>
                        <span className="text-slate-400 text-right truncate text-[11px]">
                          {serverState.firstPartyVerifierHash ? 'sha256-v1-tigrbl:••••••••' : 'None enrolled'}
                        </span>
                      </div>
                    </div>

                    {/* Change Form */}
                    <div className="bg-slate-900/60 p-5 rounded-2xl border border-slate-800 space-y-4">
                      <span className="text-[10px] font-mono font-bold text-slate-400 block uppercase">ATOMIC CREDENTIAL REPLACEMENT</span>
                      
                      <div className="space-y-3">
                        <div className="space-y-1">
                          <label className="text-[10px] font-bold text-slate-400 uppercase block">Current Account PIN</label>
                          <input
                            type="password"
                            maxLength={12}
                            value={clientCurrentPinInput}
                            onChange={(e) => setClientCurrentPinInput(e.target.value.replace(/[^0-9]/g, ''))}
                            placeholder="••••••"
                            className="w-full text-center tracking-[0.3em] font-mono text-sm py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-100"
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-[10px] font-bold text-slate-400 uppercase block">New Secure PIN</label>
                          <input
                            type="password"
                            maxLength={12}
                            value={clientPinInput}
                            onChange={(e) => setClientPinInput(e.target.value.replace(/[^0-9]/g, ''))}
                            placeholder="••••••"
                            className="w-full text-center tracking-[0.3em] font-mono text-sm py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-100"
                          />
                        </div>

                        <div className="space-y-1">
                          <label className="text-[10px] font-bold text-slate-400 uppercase block">Confirm New PIN</label>
                          <input
                            type="password"
                            maxLength={12}
                            value={clientConfirmInput}
                            onChange={(e) => setClientConfirmInput(e.target.value.replace(/[^0-9]/g, ''))}
                            placeholder="••••••"
                            className="w-full text-center tracking-[0.3em] font-mono text-sm py-2 rounded-xl bg-slate-950 border border-slate-800 text-slate-100"
                          />
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() => handleChangePin(clientCurrentPinInput, clientPinInput, clientConfirmInput)}
                        className="w-full py-2 bg-gradient-to-r from-blue-600 to-cyan-500 text-white font-semibold text-xs tracking-wider uppercase rounded-xl transition-all cursor-pointer shadow-md"
                      >
                        Atomically Retire Old Verifier
                      </button>
                    </div>
                  </div>
                )}

                {/* 17. PIN Suspend/Revoke/Remove */}
                {activeScreen === 'first-party-suspend-revoke' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-fp-suspend">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">Suspend & Revoke Guards</h2>
                      <p className="text-xs text-slate-400 font-sans">Stop first-party PIN usage with dual safeguards.</p>
                    </div>

                    <PinLifecyclePanel
                      serverState={serverState}
                      onAction={handleLifecycleAction}
                      recentStrongAuth={recentStrongAuth}
                      onTriggerRecentStrongAuth={handleTriggerRecentStrongAuth}
                    />

                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-900 text-xs text-slate-400 space-y-2 leading-relaxed">
                      <span className="font-bold text-red-400 block text-[10px] uppercase">MANDATED SAFELIGHT RULE</span>
                      <p className="font-mono text-[10px]">
                        Removing the final usable authenticator is blocked without replacement/recovery. If the user removes the account PIN, fallback MFA or hardware recovery tokens must be verified before purge complete.
                      </p>
                    </div>
                  </div>
                )}

                {/* 18. Forgot/Reset/Recovery */}
                {activeScreen === 'first-party-forgot-reset' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-fp-recovery">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">First-Party Forgotten PIN Reset</h2>
                      <p className="text-xs text-slate-400">Perform recovery without disclosing or restoring previous verifiers.</p>
                    </div>

                    <PinResetArtifactState
                      onInitiateReset={handleInitiateReset}
                      onVerifyArtifact={handleVerifyArtifact}
                      onCompleteNewPin={handleCompleteNewPin}
                      activeArtifact={activeRecoveryArtifact}
                      errorMsg={null}
                      successMsg={null}
                    />
                  </div>
                )}

                {/* 19. PIN Policy & Admin Reset */}
                {activeScreen === 'first-party-admin-policy' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-fp-admin">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">Administrative Administration Console</h2>
                      <p className="text-xs text-slate-400">Govern PIN parameters without administrators viewing values.</p>
                    </div>

                    <div className="bg-slate-950 p-5 rounded-2xl border border-slate-850 space-y-4">
                      <span className="text-[10px] font-mono font-bold text-slate-400 block uppercase">FORCE RESET WORKFLOW</span>
                      
                      <p className="text-xs text-slate-400 leading-relaxed font-sans">
                        Administrators can mark a PIN verifier as forced-reset. They can NEVER choose, see, or dictate the permanent PIN.
                      </p>

                      <button
                        type="button"
                        onClick={() => handleLifecycleAction('force-reset')}
                        className="w-full py-2 bg-yellow-600 text-white font-semibold text-xs uppercase tracking-wider rounded-xl hover:bg-yellow-500 transition-colors cursor-pointer"
                      >
                        Force Administrative Reset State
                      </button>
                    </div>

                    <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800 text-xs text-slate-400 space-y-2">
                      <span className="font-bold text-slate-300 block text-[10px] uppercase">RECONCILIATION POLICIES</span>
                      <p className="font-mono text-[10px] leading-relaxed">
                        ✓ Locked accounts cannot be unlocked manually by admins; they must route through the client recovery token workflow.
                      </p>
                    </div>
                  </div>
                )}

                {/* 10. User-Verification Policy */}
                {activeScreen === 'user-verification-policy' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-uv-policy">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">Configure User Verification Policy</h2>
                      <p className="text-xs text-slate-400">Configure requirements without forcing modality claims.</p>
                    </div>

                    <div className="space-y-3">
                      {[
                        { label: 'Enforce user verification (uv=required)', desc: 'Blocks verification if user presence is not confirmed.' },
                        { label: 'Allow trusted fallback methods', desc: 'Allows first-party PIN challenge if biometrics fail.' },
                        { label: 'Verify PIN provenance headers', desc: 'Rejects device assertions if provenance cannot be validated.' },
                      ].map((pol, i) => (
                        <div key={i} className="p-4 bg-slate-950 rounded-xl border border-slate-850 flex justify-between items-start gap-3">
                          <div className="space-y-1">
                            <span className="text-xs font-bold text-slate-200 block">{pol.label}</span>
                            <span className="text-[10px] text-slate-500 block leading-normal">{pol.desc}</span>
                          </div>
                          <span className="h-4 w-4 bg-blue-600 rounded flex items-center justify-center text-white text-[9px] font-bold">✓</span>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* 11. Device/Provider Config */}
                {activeScreen === 'device-provider-config' && (
                  <div className="space-y-6 text-left max-w-md mx-auto" id="screen-device-config">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white">Device & Provider Configuration</h2>
                      <p className="text-xs text-slate-400 font-sans">Configure supported key/card/native profiles separately.</p>
                    </div>

                    <div className="space-y-4">
                      {/* Outage controls */}
                      <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-3">
                        <span className="text-[10px] font-mono text-slate-500 uppercase block font-bold">SIMULATION OUTAGE & HARDWARE ERROR INJECTORS</span>
                        
                        <div className="flex justify-between items-center text-xs">
                          <span className="text-slate-300">Simulate Provider Outage:</span>
                          <button
                            type="button"
                            onClick={() => {
                              setServerState((prev) => ({ ...prev, providerOutage: !prev.providerOutage }));
                              pushAuditLog(createAuditLog('Outage State Modified', 'admin', 'info', `Provider outage set to: ${!serverState.providerOutage}`));
                            }}
                            className={`py-1 px-3 rounded font-mono text-[10px] font-bold cursor-pointer uppercase ${
                              serverState.providerOutage ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-slate-900 text-slate-400 border border-slate-800'
                            }`}
                          >
                            {serverState.providerOutage ? 'OUTAGE ACTIVE' : 'SYSTEM HEALTHY'}
                          </button>
                        </div>

                        <div className="flex justify-between items-center text-xs">
                          <span className="text-slate-300">Simulate Hardware Token Locked:</span>
                          <button
                            type="button"
                            onClick={() => {
                              setServerState((prev) => ({ ...prev, deviceLocked: !prev.deviceLocked }));
                              pushAuditLog(createAuditLog('Hardware Lockout Simulated', 'admin', 'info', `Device lock set to: ${!serverState.deviceLocked}`));
                            }}
                            className={`py-1 px-3 rounded font-mono text-[10px] font-bold cursor-pointer uppercase ${
                              serverState.deviceLocked ? 'bg-red-950 text-red-400 border border-red-800' : 'bg-slate-900 text-slate-400 border border-slate-800'
                            }`}
                          >
                            {serverState.deviceLocked ? 'DEVICE LOCKED' : 'DEVICE UNLOCKED'}
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* 12. Audit & Diagnostics Ledger */}
                {activeScreen === 'audit-diagnostics' && (
                  <div className="space-y-6 text-left max-w-2xl mx-auto animate-fadeIn" id="screen-audit-diagnostics">
                    <div className="text-center space-y-1">
                      <h2 className="text-base font-bold text-white font-sans">Cryptographic Audit & Diagnostics</h2>
                      <p className="text-xs text-slate-400">Inspecting redacted verifier operations ledger.</p>
                    </div>

                    <div className="bg-slate-950 rounded-xl border border-slate-850 overflow-hidden">
                      <div className="p-3 bg-slate-900 border-b border-slate-850 text-[10px] font-mono text-slate-400 flex justify-between items-center">
                        <span>LEDGER ID: LDR-928472</span>
                        <span className="text-cyan-400">REDATED: TRUE</span>
                      </div>
                      
                      <div className="max-h-60 overflow-y-auto divide-y divide-slate-900">
                        {auditLogs.map((log) => (
                          <div key={log.id} className="p-3 hover:bg-slate-900/40 transition-colors text-xs font-mono space-y-1">
                            <div className="flex justify-between items-center">
                              <span className="text-slate-500 text-[10px]">{log.timestamp}</span>
                              <span className={`text-[10px] font-bold uppercase px-1.5 py-0.5 rounded ${
                                log.outcome === 'success' ? 'bg-emerald-950 text-emerald-400' :
                                log.outcome === 'failure' ? 'bg-red-950 text-red-400' :
                                log.outcome === 'warning' ? 'bg-amber-950 text-amber-400' : 'bg-slate-900 text-slate-400'
                              }`}>
                                {log.outcome}
                              </span>
                            </div>
                            <div className="font-bold text-slate-300">{log.action}</div>
                            <p className="text-[11px] text-slate-400 leading-normal">{log.details}</p>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                )}

              </div>

              {/* Bottom Bezel Info */}
              <div className="border-t border-slate-900 pt-4 text-center">
                <CompatibilityNotice />
              </div>

            </div>

          </div>

        </main>

        {/* --- RIGHT COLUMN: Secure Verifier Contract & Hardware Token Console --- */}
        <aside className="w-full lg:w-96 border-t lg:border-t-0 lg:border-l border-slate-900 bg-slate-950 p-6 space-y-6 overflow-y-auto shrink-0 flex flex-col">
          
          <div className="space-y-1">
            <h3 className="text-xs font-bold uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
              <Cpu size={14} className="text-cyan-400" />
              Secure Server Controller
            </h3>
            <p className="text-[11px] text-slate-500 font-mono">
              Inspect simulated backend database variables and verify zero-knowledge compliance.
            </p>
          </div>

          {/* Secure Database Metrics Card */}
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-800/80 space-y-4">
            <span className="text-[10px] font-mono font-bold text-slate-400 block uppercase border-b border-slate-850 pb-1.5">
              Simulated Database Registry
            </span>

            <div className="space-y-2.5 text-xs font-mono">
              <div className="flex justify-between">
                <span className="text-slate-500">First-Party Enrolled:</span>
                <span className={serverState.isFirstPartyEnrolled ? 'text-emerald-400 font-bold' : 'text-slate-500'}>
                  {serverState.isFirstPartyEnrolled ? 'TRUE' : 'FALSE'}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-slate-500">Hash (Argon2 / SHA):</span>
                <span className="text-slate-400 select-all font-mono text-[10px] block truncate max-w-[150px]" title={serverState.firstPartyVerifierHash || 'None'}>
                  {serverState.firstPartyVerifierHash || 'None (Null)'}
                </span>
              </div>

              <div className="flex justify-between">
                <span className="text-slate-500">Lockout Remaining Attempts:</span>
                <span className="text-slate-300 font-bold">{serverState.remainingAttempts}</span>
              </div>

              <div className="flex justify-between">
                <span className="text-slate-500">Verifier Status:</span>
                <span className="text-yellow-400 font-bold uppercase">{serverState.status}</span>
              </div>
            </div>
          </div>

          {/* Global verification policy configs */}
          <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-800 space-y-4 text-left">
            <div className="flex justify-between items-center">
              <span className="text-[10px] font-mono font-bold text-slate-400 block uppercase">
                Active Verification Policy
              </span>
              <span className="text-[9px] font-mono text-cyan-400 font-bold">MUTABLE</span>
            </div>

            <div className="space-y-3 font-mono text-xs">
              <div className="space-y-1">
                <label className="text-slate-500 text-[10px]">Min Length requirement:</label>
                <div className="flex items-center gap-2">
                  <input
                    type="range"
                    min={4}
                    max={10}
                    value={serverState.policy.minLength}
                    onChange={(e) => {
                      const len = parseInt(e.target.value);
                      setServerState((prev) => ({
                        ...prev,
                        policy: { ...prev.policy, minLength: len }
                      }));
                      pushAuditLog(createAuditLog('Min Length Modified', 'policy', 'info', `Enforced min length to: ${len}`));
                    }}
                    className="w-full"
                  />
                  <span className="text-slate-200 font-bold">{serverState.policy.minLength}</span>
                </div>
              </div>

              <div className="space-y-1">
                <label className="text-slate-500 text-[10px]">Disallowed blocklists count:</label>
                <div className="text-slate-300 font-bold">
                  {serverState.policy.disallowedPatterns.length} patterns loaded
                </div>
              </div>
            </div>
          </div>

          {/* Simulated Audit Logger quick-view */}
          <div className="flex-1 flex flex-col min-h-[150px]">
            <span className="text-[10px] font-mono font-bold text-slate-400 uppercase mb-2 block">
              Recent Audits
            </span>
            <div className="flex-1 bg-slate-950 border border-slate-900 rounded-xl p-3 font-mono text-[10px] overflow-y-auto space-y-2 max-h-52">
              {auditLogs.slice(0, 3).map((log) => (
                <div key={log.id} className="border-b border-slate-900 pb-1.5 last:border-0 last:pb-0">
                  <div className="flex justify-between text-slate-600">
                    <span>{log.id}</span>
                    <span>{log.timestamp.split('T')[1].substring(0, 8)}</span>
                  </div>
                  <div className="text-slate-300 font-bold truncate">{log.action}</div>
                  <div className="text-slate-500 truncate">{log.details}</div>
                </div>
              ))}
              <button
                type="button"
                onClick={() => setActiveScreen('audit-diagnostics')}
                className="w-full text-center py-1 text-xs text-blue-400 hover:underline font-bold mt-2 cursor-pointer"
              >
                Inspect Full Audit Ledger →
              </button>
            </div>
          </div>

        </aside>

      </div>

    </div>
  );
}
