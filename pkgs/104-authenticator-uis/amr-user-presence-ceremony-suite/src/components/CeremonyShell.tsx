/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { CeremonyState, Authenticator, PresencePolicy, ManagedKeyProfile, CeremonyEvidence, AuditLog } from '../types';
import { INITIAL_AUTHENTICATORS, INITIAL_POLICIES, INITIAL_MANAGED_PROFILES, INITIAL_AUDIT_LOGS } from '../data';
import DeviceSimulator from './DeviceSimulator';
import PasskeyPrompt from './PasskeyPrompt';
import EnrollmentCeremony from './EnrollmentCeremony';
import PolicyEditor from './PolicyEditor';
import EvidencePanel from './EvidencePanel';
import PreflightChecklist from './PreflightChecklist';
import { Shield, Fingerprint, Lock, ShieldCheck, Activity, Terminal, CheckCircle, Info, Settings, UserCheck } from 'lucide-react';

export default function CeremonyShell() {
  // State lists
  const [authenticators, setAuthenticators] = useState<Authenticator[]>(INITIAL_AUTHENTICATORS);
  const [policies, setPolicies] = useState<PresencePolicy[]>(INITIAL_POLICIES);
  const [managedProfiles, setManagedProfiles] = useState<ManagedKeyProfile[]>(INITIAL_MANAGED_PROFILES);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(INITIAL_AUDIT_LOGS);

  // Active Workspace tab
  const [activeTab, setActiveTab] = useState<'auth' | 'enroll' | 'policy' | 'diagnostics'>('auth');

  // Ceremony state machine
  const [activeState, setActiveState] = useState<CeremonyState>(CeremonyState.IDLE);
  const [activeAuthenticator, setActiveAuthenticator] = useState<Authenticator | null>(null);
  const [activePolicy, setActivePolicy] = useState<PresencePolicy>(INITIAL_POLICIES[0]);
  const [ceremonyPurpose, setCeremonyPurpose] = useState('');
  const [isKeyInserted, setIsKeyInserted] = useState(true); // Default to inserted for seamless start
  const [latestEvidence, setLatestEvidence] = useState<CeremonyEvidence | null>(null);
  const [errorMessage, setErrorMessage] = useState('');

  // Browser support state
  const [isBrowserWebAuthnSupported, setIsBrowserWebAuthnSupported] = useState(true);

  // Derive if PIN is required based on policy and UV capabilities
  const isPinRequired = activePolicy.uvRequired;

  // Add dynamic audit logs helper
  const addAuditLog = (
    event: string,
    category: 'auth' | 'enrollment' | 'policy' | 'lifecycle' | 'error',
    status: 'success' | 'failure' | 'warning' | 'info',
    details: string
  ) => {
    const newLog: AuditLog = {
      id: `log-${Date.now()}`,
      timestamp: new Date().toISOString(),
      event,
      category,
      status,
      details,
      auditReference: `AUDIT-${Math.random().toString(36).substring(2, 6).toUpperCase()}-${Math.floor(1000 + Math.random() * 9000)}`,
    };
    setAuditLogs(prev => [newLog, ...prev]);
  };

  // Handle active authenticator connection changes
  const handleInsertToggle = () => {
    const nextState = !isKeyInserted;
    setIsKeyInserted(nextState);

    addAuditLog(
      nextState ? 'Security key inserted' : 'Security key removed',
      'lifecycle',
      nextState ? 'info' : 'warning',
      `Physical USB connection state changed. Key is now ${nextState ? 'connected' : 'disconnected'}.`
    );

    // If key is removed midway during a ceremony, trigger the error state!
    if (!nextState && [CeremonyState.AWAITING_DEVICE, CeremonyState.TOUCH_GUIDANCE].includes(activeState)) {
      handleDeviceError(CeremonyState.DEVICE_REMOVED);
    } else if (nextState && activeState === CeremonyState.INSERT_GUIDANCE) {
      // If we were waiting for insertion, proceed to touch guidance!
      setActiveState(CeremonyState.TOUCH_GUIDANCE);
    }
  };

  // Initiate Ceremony (P0 Phase)
  const handleInitiateCeremony = (auth: Authenticator, policy: PresencePolicy, purpose: string) => {
    setActiveAuthenticator(auth);
    setActivePolicy(policy);
    setCeremonyPurpose(purpose);
    setLatestEvidence(null);
    setErrorMessage('');

    addAuditLog(
      'Ceremony challenge created',
      'auth',
      'info',
      `Initiating user-presence ceremony for target: "${purpose}". Required policy: ${policy.name}.`
    );

    setActiveState(CeremonyState.AWAITING_DEVICE);

    // Simulate device handoff latency
    setTimeout(() => {
      // If authenticator is USB or Managed but key is not connected, require insertion guidance
      if ((auth.transport === 'usb' || auth.type === 'managed_key') && !isKeyInserted) {
        setActiveState(CeremonyState.INSERT_GUIDANCE);
        addAuditLog(
          'Awaiting USB insertion',
          'lifecycle',
          'warning',
          `Selected authenticator "${auth.name}" requires active USB connection. Prompting user to plug in device.`
        );
      } else {
        setActiveState(CeremonyState.TOUCH_GUIDANCE);
      }
    }, 600);
  };

  // Handle successful touch / presence confirmation
  const handleTouchConfirmed = (presenceSuccess: boolean, uvSuccess: boolean, pinUsed?: string) => {
    if (!activeAuthenticator) return;

    setActiveState(CeremonyState.PROCESSING);
    addAuditLog(
      'Physical interaction detected',
      'auth',
      'info',
      `Sensor touch triggered. UP flag set. UV flag set to ${uvSuccess ? 'true' : 'false'}.`
    );

    // Simulated cryptographic signature generation latency
    setTimeout(() => {
      // Origin and RP variables
      const origin = window.location.origin;
      const rpId = window.location.hostname;
      const clientDataHash = crypto.randomUUID().replace(/-/g, '');
      const signature = '3045022100e4708a0d927a3f01' + Math.random().toString(16).substring(2, 10) + '02202bc92e31';

      // Evaluate policy compliance
      const isPolicySatisfied = 
        (!activePolicy.presenceRequired || presenceSuccess) &&
        (!activePolicy.uvRequired || uvSuccess);

      const evidence: CeremonyEvidence = {
        id: `ev-${Date.now()}`,
        timestamp: new Date().toISOString(),
        authenticatorId: activeAuthenticator.id,
        authenticatorName: activeAuthenticator.name,
        authenticatorType: activeAuthenticator.type,
        transport: activeAuthenticator.transport,
        purpose: ceremonyPurpose,
        userPresent: presenceSuccess,
        userVerified: uvSuccess,
        modality: pinUsed ? 'pin' : activeAuthenticator.type === 'passkey' ? 'biometric' : 'touch',
        origin,
        rpId,
        clientDataHash,
        signature,
        counter: activeAuthenticator.signatureCount + 1,
        policySatisfied: isPolicySatisfied,
        auditReference: `AUDIT-EV-${Math.random().toString(36).substring(2, 6).toUpperCase()}`,
      };

      // Increment signature counter on authenticator
      setAuthenticators(prev => prev.map(a => 
        a.id === activeAuthenticator.id 
          ? { ...a, signatureCount: a.signatureCount + 1, lastUsedAt: new Date().toISOString() }
          : a
      ));

      setLatestEvidence(evidence);

      if (isPolicySatisfied) {
        setActiveState(CeremonyState.SUCCESS);
        addAuditLog(
          'Presence Ceremony Success',
          'auth',
          'success',
          `Assertion complete. UP/UV signature validated against ${activePolicy.name} policy.`
        );
      } else {
        setActiveState(CeremonyState.UV_REQUIRED);
        addAuditLog(
          'Policy Evaluation Blocked',
          'policy',
          'warning',
          `Presence established but policy demanded User Verification. UP=true, UV=false.`
        );
      }
    }, 800);
  };

  // Handle external device errors / injected simulation failures
  const handleDeviceError = (errorState: CeremonyState) => {
    setActiveState(errorState);

    let details = 'Physical ceremony failed.';
    let category: 'auth' | 'enrollment' | 'policy' | 'lifecycle' | 'error' = 'error';

    switch (errorState) {
      case CeremonyState.PRESENCE_ABSENT:
        details = 'Verification failed: User touch sensor was not tapped.';
        break;
      case CeremonyState.CANCELLED:
        details = 'Interaction interrupted: User clicked cancel on browser authenticator window.';
        category = 'lifecycle';
        break;
      case CeremonyState.TIMEOUT:
        details = 'Handshake timed out: Security token waiting period expired.';
        break;
      case CeremonyState.DEVICE_REMOVED:
        details = 'Hardware connection lost: Security key unplugged midway.';
        break;
      case CeremonyState.TRANSPORT_UNAVAILABLE:
        details = 'Transport failure: Bluetooth/NFC reader unresponsive.';
        break;
      case CeremonyState.REPLAY_DETECTED:
        details = 'CRITICAL: Signature counter mismatch detected. Blocking session. Replay guard alert triggered.';
        category = 'error';
        break;
    }

    addAuditLog('Ceremony Interaction Interrupted', category, 'failure', details);
  };

  // Handle simulated NFC Tap
  const handleNfcTap = () => {
    if (activeAuthenticator?.transport === 'nfc') {
      handleTouchConfirmed(true, activePolicy.uvRequired ? false : true);
    }
  };

  // Reset active ceremony to configure phase
  const handleResetCeremony = () => {
    setActiveState(CeremonyState.IDLE);
    setActiveAuthenticator(null);
    setLatestEvidence(null);
  };

  // Enroll key lifecycle helper (P1 Screen)
  const handleEnrollKey = (newKey: Authenticator) => {
    setAuthenticators(prev => [...prev, newKey]);
    addAuditLog(
      'Authenticator enrolled',
      'enrollment',
      'success',
      `Registered new credential: "${newKey.name}". AAGUID attestation reports genuine ${newKey.type}.`
    );
  };

  const handleRemoveKey = (id: string) => {
    setAuthenticators(prev => prev.filter(a => a.id !== id));
    addAuditLog(
      'Authenticator revoked',
      'enrollment',
      'info',
      `Key ID ${id} was deleted from user lifecycle and marked revoked on corporate server.`
    );
  };

  // Start enrollment touch handshake in simulator
  const handleStartEnrollCeremony = (auth: Authenticator) => {
    setActiveAuthenticator(auth);
    setCeremonyPurpose(`Enroll underlying ${auth.type} credential`);
    setActiveState(CeremonyState.AWAITING_DEVICE);

    setTimeout(() => {
      setActiveState(CeremonyState.TOUCH_GUIDANCE);
    }, 500);
  };

  // Fallback method trigger
  const handleFallbackUsed = () => {
    addAuditLog(
      'Fallback authenticator requested',
      'lifecycle',
      'info',
      'User bypassed primary presence target and requested alternative enrollment verification.'
    );
    // Find first other transport / or switch to passkey
    alert('Mock Handoff: Safe fallback loop initiated. Secondary PIN/Recovery page loaded.');
  };

  return (
    <div className="min-h-screen bg-zinc-50/50 flex flex-col font-sans text-zinc-900 selection:bg-indigo-100">
      {/* Universal Workspace Header */}
      <header className="bg-white border-b border-zinc-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 bg-zinc-900 text-white rounded-xl shadow-md">
              <Shield className="w-6 h-6 text-indigo-400" />
            </div>
            <div>
              <h1 className="font-display font-bold text-lg text-zinc-950 tracking-tight">
                AMR User-Presence Ceremony Suite
              </h1>
              <p className="font-sans text-[11px] text-zinc-500 font-medium">
                Standard FIDO2 Touch/Touchless Interaction & Dynamic Policy Handshake Sandbox
              </p>
            </div>
          </div>

          {/* Quick status counters */}
          <div className="flex items-center gap-2 bg-zinc-100/80 border border-zinc-200/50 rounded-xl px-3 py-1.5 font-mono text-[11px] text-zinc-600">
            <Activity className="w-3.5 h-3.5 text-indigo-500 shrink-0" />
            <span>Active Keys: {authenticators.length}</span>
            <span className="w-1.5 h-1.5 rounded-full bg-zinc-300 mx-1" />
            <span>Audit Records: {auditLogs.length}</span>
          </div>
        </div>
      </header>

      {/* Primary Workstation Grid */}
      <main className="flex-1 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 w-full">
        {/* Browser Preflight Box (Dynamic Checkup) */}
        <section className="mb-6">
          <PreflightChecklist onCheckComplete={setIsBrowserWebAuthnSupported} />
        </section>

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Main Workspace Column (Left) */}
          <div className="lg:col-span-8 flex flex-col space-y-6">
            {/* Navigational Tabs / Priority Workspace Gates */}
            <nav className="flex bg-white p-1 rounded-xl border border-zinc-200/80 shadow-sm gap-1">
              <button
                id="tab-auth"
                onClick={() => setActiveTab('auth')}
                className={`flex-1 font-sans text-xs font-semibold py-2.5 px-3 rounded-lg transition-colors flex items-center justify-center gap-1.5 ${
                  activeTab === 'auth'
                    ? 'bg-zinc-900 text-white shadow-sm'
                    : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900'
                }`}
              >
                <Fingerprint className="w-4 h-4" />
                P0 — Interaction Ceremony
              </button>
              <button
                id="tab-enroll"
                onClick={() => setActiveTab('enroll')}
                className={`flex-1 font-sans text-xs font-semibold py-2.5 px-3 rounded-lg transition-colors flex items-center justify-center gap-1.5 ${
                  activeTab === 'enroll'
                    ? 'bg-zinc-900 text-white shadow-sm'
                    : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900'
                }`}
              >
                <UserCheck className="w-4 h-4" />
                P1 — Enrollment Lifecycle
              </button>
              <button
                id="tab-policy"
                onClick={() => setActiveTab('policy')}
                className={`flex-1 font-sans text-xs font-semibold py-2.5 px-3 rounded-lg transition-colors flex items-center justify-center gap-1.5 ${
                  activeTab === 'policy'
                    ? 'bg-zinc-900 text-white shadow-sm'
                    : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900'
                }`}
              >
                <Lock className="w-4 h-4" />
                P2 — Policies & Profiles
              </button>
              <button
                id="tab-diagnostics"
                onClick={() => setActiveTab('diagnostics')}
                className={`flex-1 font-sans text-xs font-semibold py-2.5 px-3 rounded-lg transition-colors flex items-center justify-center gap-1.5 ${
                  activeTab === 'diagnostics'
                    ? 'bg-zinc-900 text-white shadow-sm'
                    : 'text-zinc-600 hover:bg-zinc-50 hover:text-zinc-900'
                }`}
              >
                <Terminal className="w-4 h-4" />
                CLI Diagnostics
              </button>
            </nav>

            {/* Active Workspace Viewport */}
            <div className="transition-all duration-300">
              {activeTab === 'auth' && (
                <PasskeyPrompt
                  authenticators={authenticators}
                  policies={policies}
                  activeState={activeState}
                  onInitiateCeremony={handleInitiateCeremony}
                  onResetCeremony={handleResetCeremony}
                  evidenceResult={latestEvidence}
                  policySatisfied={latestEvidence ? latestEvidence.policySatisfied : false}
                  onFallbackUsed={handleFallbackUsed}
                  activePolicy={activePolicy}
                  selectedAuth={activeAuthenticator}
                  errorMessage={errorMessage}
                />
              )}

              {activeTab === 'enroll' && (
                <EnrollmentCeremony
                  authenticators={authenticators}
                  onEnrollKey={handleEnrollKey}
                  onRemoveKey={handleRemoveKey}
                  activeState={activeState}
                  onStartEnrollCeremony={handleStartEnrollCeremony}
                />
              )}

              {activeTab === 'policy' && (
                <PolicyEditor
                  policies={policies}
                  managedProfiles={managedProfiles}
                  onUpdatePolicy={(p) => setPolicies(prev => prev.map(item => item.id === p.id ? p : item))}
                  onUpdateProfile={(prof) => setManagedProfiles(prev => prev.map(item => item.id === prof.id ? prof : item))}
                />
              )}

              {activeTab === 'diagnostics' && (
                <EvidencePanel
                  auditLogs={auditLogs}
                  latestEvidence={latestEvidence}
                  onClearLogs={() => setAuditLogs([])}
                  onInjectAudit={(ev, cat, stat, det) => addAuditLog(ev, cat, stat, det)}
                />
              )}
            </div>
          </div>

          {/* Device Ceremony Visual Simulator Column (Right) */}
          <div className="lg:col-span-4 lg:sticky lg:top-24">
            <DeviceSimulator
              activeAuthenticator={activeAuthenticator}
              activeState={activeState}
              onTouch={handleTouchConfirmed}
              onTriggerError={handleDeviceError}
              isPinRequired={isPinRequired}
              isKeyInserted={isKeyInserted}
              onInsertToggle={handleInsertToggle}
              onNfcTap={handleNfcTap}
              ceremonyPurpose={ceremonyPurpose}
            />
          </div>
        </div>
      </main>

      {/* Sticky footer for design elegance */}
      <footer className="mt-auto bg-white border-t border-zinc-200/80 py-4 font-sans text-center text-[11px] text-zinc-400">
        <div className="max-w-7xl mx-auto px-4">
          AMR User-Presence Ceremony Sandbox · Enforces strict FIDO2/WebAuthn dynamic token flags · Dec 2026
        </div>
      </footer>
    </div>
  );
}
