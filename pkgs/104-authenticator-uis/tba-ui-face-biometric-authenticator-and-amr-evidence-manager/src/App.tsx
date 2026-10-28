/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  INITIAL_AUTHENTICATORS, 
  INITIAL_PROVIDERS, 
  INITIAL_POLICY, 
  INITIAL_AUDIT_LOGS 
} from './mockData';
import { 
  FaceAuthenticator, 
  TenantEvidencePolicy, 
  TrustedProvider, 
  AuditLogEntry, 
  BiometricEvidence 
} from './types';
import { ActiveSessionContext } from './components/ActiveSessionContext';
import { ActiveCeremonyWizard } from './components/ActiveCeremonyWizard';
import { AccountDashboard } from './components/AccountDashboard';
import { AdminPolicyDashboard } from './components/AdminPolicyDashboard';
import { Shield, KeyRound, Sliders, LayoutDashboard, Compass, Activity, BookOpen, AlertCircle } from 'lucide-react';

export default function App() {
  const [tab, setTab] = useState<'playground' | 'account' | 'admin'>('playground');
  
  // App state
  const [authenticators, setAuthenticators] = useState<FaceAuthenticator[]>(INITIAL_AUTHENTICATORS);
  const [providers, setProviders] = useState<TrustedProvider[]>(INITIAL_PROVIDERS);
  const [policy, setPolicy] = useState<TenantEvidencePolicy>(INITIAL_POLICY);
  const [auditLogs, setAuditLogs] = useState<AuditLogEntry[]>(INITIAL_AUDIT_LOGS);
  
  // Active session biometric verified evidence
  const [verifiedEvidence, setVerifiedEvidence] = useState<BiometricEvidence | null>({
    amr: 'face',
    provenance: 'face_verified',
    issuer: 'approved-native-enclave-v4',
    verificationTime: new Date().toISOString(),
    freshnessSeconds: 12,
    confidenceRating: 'high_attested',
    isHardwareBacked: true,
    isLivenessProtected: true,
    auditReference: 'aud-ev-direct-prepopulated-881',
    redactedRawClaims: {}
  });

  // Secure Audit Log helper
  const handleLogAudit = (
    event: string, 
    category: any, 
    status: 'success' | 'failure' | 'warning' | 'info', 
    details: string,
    amr?: string,
    provenance?: string
  ) => {
    const newLog: AuditLogEntry = {
      id: `log-${Math.floor(Math.random() * 90000) + 10000}`,
      timestamp: new Date().toISOString(),
      event,
      category,
      actor: 'jick.68.0@gmail.com',
      status,
      details,
      amrEvidence: amr,
      provenance: provenance as any,
      device: 'Enterprise Laptop Enclave Terminal',
      ip: '198.51.100.42'
    };
    setAuditLogs(prev => [newLog, ...prev]);
  };

  // Add Authenticator (e.g. on successful enrollment wizard)
  const handleAddAuthenticator = (newAuth: FaceAuthenticator) => {
    setAuthenticators(prev => [newAuth, ...prev]);
  };

  // Retrain Trigger from Account dashboard
  const handleInitiateRetrain = (id: string) => {
    // Select the playground tab and set the ceremony mode
    setTab('playground');
    handleLogAudit(
      'Authenticator Retraining Initialized',
      'lifecycle',
      'info',
      `Subject initiated a replacement ceremony for template: ${id}. Overlap transition active.`
    );
  };

  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans antialiased flex flex-col pb-12">
      {/* Top Brand Banner */}
      <header className="bg-white border-b border-gray-200 sticky top-0 z-40">
        <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap items-center justify-between gap-4">
          
          {/* Logo */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-indigo-600 text-white rounded-xl">
              <Shield className="w-5 h-5" />
            </div>
            <div>
              <h1 className="text-sm font-bold text-gray-900 tracking-tight">Face AMR</h1>
              <p className="text-[10px] text-gray-400 font-mono">Biometric Authenticator Sandbox</p>
            </div>
          </div>

          {/* Tab Navigation Menu */}
          <nav className="flex space-x-1 bg-gray-100 p-1 rounded-xl text-xs font-semibold">
            <button
              type="button"
              onClick={() => setTab('playground')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                tab === 'playground'
                  ? 'bg-white text-gray-900 shadow-xs'
                  : 'text-gray-500 hover:text-gray-900'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              Ceremony Playground
            </button>
            <button
              type="button"
              onClick={() => setTab('account')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                tab === 'account'
                  ? 'bg-white text-gray-900 shadow-xs'
                  : 'text-gray-500 hover:text-gray-900'
              }`}
            >
              <KeyRound className="w-3.5 h-3.5" />
              My Biometric Profile
            </button>
            <button
              type="button"
              onClick={() => setTab('admin')}
              className={`flex items-center gap-1.5 px-4 py-2 rounded-lg transition-all ${
                tab === 'admin'
                  ? 'bg-white text-gray-900 shadow-xs'
                  : 'text-gray-500 hover:text-gray-900'
              }`}
            >
              <Sliders className="w-3.5 h-3.5" />
              Tenant Admin View
            </button>
          </nav>

          {/* Dev info / metadata indicator */}
          <div className="hidden md:flex items-center gap-2 text-right">
            <span className="text-[10px] font-mono text-gray-400">AMR Method evidence:</span>
            <span className="text-[10px] font-mono font-bold bg-indigo-50 text-indigo-700 px-2 py-0.5 rounded border border-indigo-200">
              face_verified
            </span>
          </div>

        </div>
      </header>

      {/* Main Container */}
      <main className="max-w-6xl w-full mx-auto px-4 sm:px-6 lg:px-8 mt-6 flex-grow space-y-6">
        
        {/* Compliance Reminder Callout Banner */}
        <div className="bg-indigo-50/55 border border-indigo-100 rounded-2xl p-4 text-left flex items-start gap-3.5">
          <BookOpen className="w-5.5 h-5.5 text-indigo-600 shrink-0 mt-0.5" />
          <div className="text-xs text-indigo-950">
            <span className="font-bold block text-indigo-900 text-sm mb-1">Core Compliance Requirement Checklist</span>
            <ul className="list-disc pl-4 space-y-1 text-[11px] text-indigo-800 leading-relaxed">
              <li>
                <strong className="text-indigo-900">Never infer `face` from general WebAuthn UV:</strong> When the browser returns a standard credentials gesture, we preserve the metadata as generic user verification (`uv`). We never relabel or promote it as `face` unless explicit, certified modality evidence accompanies the assertion.
              </li>
              <li>
                <strong className="text-indigo-900">Secure Biometric Data Boundary:</strong> Raw facial coordinates, matrices, and camera feeds are processed exclusively inside transient native secure enclaves. General application code and DOM state never receive raw biometric samples.
              </li>
            </ul>
          </div>
        </div>

        {/* Active Session Verification Context Widget */}
        <ActiveSessionContext
          evidence={verifiedEvidence}
          onClearSession={() => {
            setVerifiedEvidence(null);
            handleLogAudit('Active Session Cleared', 'authentication', 'info', 'Subject manually cleared active biometric session context.');
          }}
        />

        {/* Dynamic Tab Renderers */}
        <div className="transition-all duration-300">
          {tab === 'playground' && (
            <div className="space-y-6">
              <div className="text-left max-w-xl mx-auto">
                <h3 className="text-lg font-bold text-gray-900">Biometric Handoff & Ceremony Sandbox</h3>
                <p className="text-xs text-gray-500 mt-1">
                  Enact biometric workflows. Use the sandbox controls inside to simulate face matching, presentation attacks (spoof warning alerts), and WebAuthn general uv credentials.
                </p>
              </div>

              <ActiveCeremonyWizard
                onAddAuthenticator={handleAddAuthenticator}
                onLogAudit={handleLogAudit}
                onSetVerifiedEvidence={setVerifiedEvidence}
                policyAllowFirstParty={policy.allowFirstPartyFace}
                policyAllowFederated={policy.allowFederatedFace}
              />
            </div>
          )}

          {tab === 'account' && (
            <div className="space-y-4">
              <div className="text-left">
                <h3 className="text-lg font-bold text-gray-900">My Biometric Profile Management</h3>
                <p className="text-xs text-gray-500 mt-0.5">View enrolled templates, request secure asynchronous deletion jobs, or replace outdated profiles.</p>
              </div>

              <AccountDashboard
                authenticators={authenticators}
                onUpdateAuthenticators={setAuthenticators}
                onInitiateRetrain={handleInitiateRetrain}
                onLogAudit={handleLogAudit}
              />
            </div>
          )}

          {tab === 'admin' && (
            <div className="space-y-4">
              <div className="text-left">
                <h3 className="text-lg font-bold text-gray-900">Tenant Administrator Dashboard</h3>
                <p className="text-xs text-gray-500 mt-0.5">Establish biometric requirements, configure enterprise identity provider enclaves, and check lockout coverage metrics.</p>
              </div>

              <AdminPolicyDashboard
                policy={policy}
                onUpdatePolicy={setPolicy}
                providers={providers}
                onUpdateProviders={setProviders}
                auditLogs={auditLogs}
                onLogAudit={handleLogAudit}
              />
            </div>
          )}
        </div>

      </main>

      {/* Elegant Humble Footer */}
      <footer className="text-center text-[10px] text-gray-400 mt-12 pt-4 border-t border-gray-200">
        <p>© 2026 Face AMR Biometric Evidence Framework. Conformant to SEC Biometric Identity & WebAuthn Multi-Factor Attestation Guidelines.</p>
        <p className="mt-0.5 text-gray-400 font-mono">Isolated Verifier Enclave v4.0.12-Sec • Active Challenge Cryptoservice</p>
      </footer>
    </div>
  );
}
