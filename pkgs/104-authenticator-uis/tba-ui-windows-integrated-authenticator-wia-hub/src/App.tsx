/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import {
  ShieldAlert,
  ShieldCheck,
  UserCheck,
  LayoutDashboard,
  Settings,
  Terminal as TermIcon,
  Laptop,
  Server,
  Globe,
  Loader2,
  FileText,
  AlertTriangle,
  RefreshCw,
  LogOut,
  HelpCircle,
  Clock,
  HeartPulse
} from 'lucide-react';
import {
  EnterpriseDomain,
  ServicePrincipalName,
  BrowserPolicy,
  UserEnterpriseIdentity,
  SystemHealthMetric,
  SimMode,
  SimConfig,
  AuditLog
} from './types';

// Import our modular components
import EnterpriseMethodCard from './components/EnterpriseMethodCard';
import IntegratedAuthProgress from './components/IntegratedAuthProgress';
import ManagedEnvironmentNotice from './components/ManagedEnvironmentNotice';
import EnterpriseIdentityProjection from './components/EnterpriseIdentityProjection';
import AccountLinkRiskGate from './components/AccountLinkRiskGate';
import DomainProviderConfig from './components/DomainProviderConfig';
import BrowserCompatibilityMatrix from './components/BrowserCompatibilityMatrix';
import EnterpriseHealthSummary from './components/EnterpriseHealthSummary';
import CliDiagnostics from './components/CliDiagnostics';
import SecurityAuditLogs from './components/SecurityAuditLogs';

// Initial Mock Seed Data
const initialDomains: EnterpriseDomain[] = [
  {
    id: 'dom-1',
    name: 'corp.enterprise.local',
    verified: true,
    trustType: 'bidirectional',
    kdcServer: 'dc1.corp.enterprise.local',
    mappedUsersCount: 1420,
    lastSync: new Date().toISOString(),
  },
  {
    id: 'dom-2',
    name: 'uk.corp.enterprise.local',
    verified: true,
    trustType: 'one-way-incoming',
    kdcServer: 'dc-uk-01.uk.corp.enterprise.local',
    mappedUsersCount: 890,
    lastSync: new Date().toISOString(),
  },
];

const initialSpns: ServicePrincipalName[] = [
  {
    id: 'spn-1',
    spn: 'HTTP/sso.corp.com',
    serviceAccount: 'svc_webgateway_sso',
    realm: 'CORP.ENTERPRISE.LOCAL',
    encryptionTypes: ['AES256-CTS-HMAC-SHA1-96'],
    delegationAllowed: true,
    delegationAllowlist: ['HTTP/*', 'LDAP/*'],
  },
  {
    id: 'spn-2',
    spn: 'HTTP/app.internal',
    serviceAccount: 'svc_internal_app',
    realm: 'CORP.ENTERPRISE.LOCAL',
    encryptionTypes: ['AES256-CTS-HMAC-SHA1-96', 'RC4-HMAC'],
    delegationAllowed: true,
    delegationAllowlist: [],
  },
];

const initialPolicy: BrowserPolicy = {
  wiaEnabled: true,
  allowPrivateBrowsingWia: false,
  intranetZoneOnly: true,
  requireChannelBinding: true,
  extendedProtection: 'WhenSupported',
  supportedBrowsers: [
    { browser: 'Microsoft Edge (Managed GPO)', os: 'Windows 11', supported: true, policyStatus: 'Active' },
    { browser: 'Google Chrome (Managed GPO)', os: 'Windows 11', supported: true, policyStatus: 'Active' },
    { browser: 'Firefox Enterprise (Unmanaged)', os: 'Windows 11', supported: false, policyStatus: 'Warning' },
    { browser: 'Safari Private Browser Tab', os: 'macOS Sonoma', supported: false, policyStatus: 'Warning' },
    { browser: 'Enterprise Workplace Desktop Client', os: 'Windows 11 Native', supported: true, policyStatus: 'Active' },
  ],
};

const defaultIdentity: UserEnterpriseIdentity = {
  id: 'usr-1',
  upn: 'j.doe@corp.enterprise.local',
  samAccountName: 'CORP\\jdoe',
  sid: 'S-1-5-21-3623811015-3361044348-30300820-1013',
  displayName: 'Jonathan Doe',
  email: 'j.doe@corp.enterprise.local',
  domain: 'corp.enterprise.local',
  memberOf: ['Domain Users', 'Enterprise Admins', 'SSO-Access-Allowed', 'Finance-Approvers'],
  status: 'active',
  assuranceLevel: 'High',
  linkedAt: '2026-07-15T12:00:00Z',
  lastAuthEvidence: {
    amr: ['wia', 'mfa'],
    spnUsed: 'HTTP/sso.corp.com',
    authTime: '2026-07-20T08:00:00Z',
    ticketFreshnessSeconds: 602,
    channelBound: true,
  }
};

const initialAuditLogs: AuditLog[] = [
  {
    id: 'aud-1',
    timestamp: '2026-07-20T08:00:00Z',
    eventType: 'token_validation',
    summary: 'Successful automatic silent Windows Kerberos sign-on',
    details: 'Kerberos ticket for Principal j.doe@corp.enterprise.local successfully validated against KDC (dc1.corp.enterprise.local). Token signatures verified using AES256-CTS-HMAC-SHA1-96. Session bound and authorized with AMR wia.',
    actor: 'CORP\\jdoe',
    amr: ['wia'],
    status: 'success',
    ipAddress: '10.240.12.80',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0',
  },
  {
    id: 'aud-2',
    timestamp: '2026-07-20T07:45:00Z',
    eventType: 'policy_update',
    summary: 'Extended Protection for Authentication GPO level modified',
    details: 'Administrator modified Extended Protection Level from "Required" to "WhenSupported" to allow legacy developer compatibility clients.',
    actor: 'CORP\\admin_sam',
    status: 'warning',
    ipAddress: '10.240.10.15',
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Edge/120.0.0.0',
  },
];

export default function App() {
  // Navigation State: 'gateway' | 'profile' | 'admin'
  const [activeTab, setActiveTab] = useState<'gateway' | 'profile' | 'admin'>('gateway');
  // Admin sub-navigation: 'domains' | 'policies' | 'health' | 'terminal' | 'audit'
  const [adminSubTab, setAdminSubTab] = useState<'domains' | 'policies' | 'health' | 'terminal' | 'audit'>('domains');

  // WIA Simulator State Control
  const [simConfig, setSimConfig] = useState<SimConfig>({
    activeMode: 'success_auto',
    networkLatencyMs: 150,
    browserType: 'Chrome_Managed',
    isCorpNetwork: true,
    systemClockOffsetSeconds: 0,
    simulatePromptCancellation: false,
  });

  // Client authentication state
  // 'idle' | 'negotiating' | 'link_risk_gate' | 'notice_error' | 'signed_in'
  const [authState, setAuthState] = useState<'idle' | 'negotiating' | 'link_risk_gate' | 'notice_error' | 'signed_in'>('idle');
  const [authError, setAuthError] = useState<{ code: SimMode; message: string } | null>(null);
  const [authProgressSpn, setAuthProgressSpn] = useState('HTTP/sso.corp.com');

  // Directory Entity States
  const [domains, setDomains] = useState<EnterpriseDomain[]>(initialDomains);
  const [spns, setSpns] = useState<ServicePrincipalName[]>(initialSpns);
  const [policy, setPolicy] = useState<BrowserPolicy>(initialPolicy);
  const [identity, setIdentity] = useState<UserEnterpriseIdentity>(defaultIdentity);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(initialAuditLogs);

  // Sync health metrics dynamically from simConfig
  const getHealthMetrics = (): SystemHealthMetric => {
    const isClockSkew = Math.abs(simConfig.systemClockOffsetSeconds) >= 300;
    const isKdcOffline = simConfig.activeMode === 'provider_timeout';

    return {
      kdcStatus: isKdcOffline ? 'unreachable' : 'healthy',
      dnsSrvStatus: 'healthy',
      clockDriftSeconds: simConfig.systemClockOffsetSeconds,
      keyAgeDays: 45,
      replicationLagSeconds: 0.8,
      conformanceStatus: isClockSkew || isKdcOffline ? 'failed' : 'passed',
    };
  };

  // Log events into audit log trail
  const appendAuditLog = (
    eventType: AuditLog['eventType'],
    summary: string,
    details: string,
    status: AuditLog['status'],
    actor: string,
    amr?: string[]
  ) => {
    const newLog: AuditLog = {
      id: `aud-${Date.now()}`,
      timestamp: new Date().toISOString(),
      eventType,
      summary,
      details,
      actor,
      status,
      amr,
      ipAddress: simConfig.isCorpNetwork ? '10.240.12.80' : '198.51.100.42',
      userAgent: `${simConfig.browserType} (Windows NT 10.0; Win64; x64) SecureChannel/1.0`,
    };
    setAuditLogs((prev) => [newLog, ...prev]);
  };

  // Respond to Simulation Mode changes and auto-configure relevant config items
  const handleSimModeChange = (mode: SimMode) => {
    let update: Partial<SimConfig> = { activeMode: mode };

    if (mode === 'unmanaged_device') {
      update.isCorpNetwork = false;
    } else {
      update.isCorpNetwork = true;
    }

    if (mode === 'clock_skew') {
      update.systemClockOffsetSeconds = 340; // Exceeds 5 mins (300s)
    } else {
      update.systemClockOffsetSeconds = 0;
    }

    if (mode === 'unsupported_browser') {
      update.browserType = 'Firefox_Unmanaged';
    } else if (mode === 'private_mode') {
      update.browserType = 'Safari_Private';
    } else {
      update.browserType = 'Chrome_Managed';
    }

    setSimConfig((prev) => {
      const next = { ...prev, ...update };
      appendAuditLog(
        'policy_update',
        `Simulation state changed: ${mode}`,
        `Administrator modified active simulation profile to evaluate "${mode}" behavior across client zones.`,
        'success',
        'SYSTEM'
      );
      return next;
    });

    // Reset current Auth State to let user test immediately
    setAuthState('idle');
    setAuthError(null);
  };

  // Run the negotiation progress triggered by user clicking login
  const startAuthentication = (bypassIntro: boolean) => {
    setAuthState('negotiating');
    appendAuditLog(
      'discovery',
      'WIA Discovery Triggered',
      `Subject selected manual "Use your work account" path. Starting Negotiate handshake for SPN ${authProgressSpn}.`,
      'success',
      'Anonymous'
    );
  };

  // Handles WIA Negotiation Success
  const handleAuthSuccess = (mappedAccount: string) => {
    // If we want to simulate the P1 Link Confirmation Risk Gate
    const requireLinkCheck = !identity.linkedAt || simConfig.activeMode === 'ambiguous_mapping';

    if (requireLinkCheck) {
      setAuthState('link_risk_gate');
      appendAuditLog(
        'negotiation',
        'Kerberos Token Mapped - Takeover Risk Gate Pending',
        `Kerberos token validated successfully, but account association requires manual link confirmation to prevent takerover exploits.`,
        'warning',
        mappedAccount,
        ['wia']
      );
    } else {
      setAuthState('signed_in');
      setIdentity((prev) => ({
        ...prev,
        lastAuthEvidence: {
          amr: ['wia', 'mfa'],
          spnUsed: authProgressSpn,
          authTime: new Date().toISOString(),
          ticketFreshnessSeconds: 1,
          channelBound: true,
        },
      }));
      appendAuditLog(
        'token_validation',
        'Successful automatic single-sign on session initialized',
        `Windows credential mapped to existing verified user. AMR evidence emitted: wia, mfa. Channel binding active.`,
        'success',
        identity.samAccountName,
        ['wia', 'mfa']
      );
    }
  };

  // Handles WIA Negotiation Failure
  const handleAuthFailure = (errorCode: SimMode, diagnosticMsg: string) => {
    setAuthError({ code: errorCode, message: diagnosticMsg });
    setAuthState('notice_error');
    appendAuditLog(
      'error',
      `Negotiation Handshake Failed: ${errorCode}`,
      `Kerberos Negotiate failed during validation step. Error Code: ${errorCode}. Diagnostic Details: ${diagnosticMsg}`,
      'failure',
      'Anonymous'
    );
  };

  // Approve Account association linking
  const handleApproveLinkAssociation = () => {
    setAuthState('signed_in');
    setIdentity((prev) => ({
      ...prev,
      linkedAt: new Date().toLocaleDateString(),
      lastAuthEvidence: {
        amr: ['wia', 'mfa'],
        spnUsed: authProgressSpn,
        authTime: new Date().toISOString(),
        ticketFreshnessSeconds: 2,
        channelBound: true,
      },
    }));
    appendAuditLog(
      'account_link',
      'Account Mapping Link Authorized',
      `User confirmed takeover mitigation checks and authorized linking of Workstation UPN ${identity.upn} with Local login.`,
      'success',
      identity.samAccountName,
      ['wia', 'mfa']
    );
  };

  // Decline Account association linking
  const handleDeclineLinkAssociation = () => {
    setAuthState('idle');
    appendAuditLog(
      'account_link',
      'Account Mapping Link Declined',
      `User declined the workstation identity link during takeover mitigation check. Ceremony terminated safely.`,
      'warning',
      'Anonymous'
    );
  };

  // Unlink identity (P1 User Lifecycle)
  const handleUnlinkIdentity = () => {
    setIdentity((prev) => ({
      ...prev,
      linkedAt: undefined,
      lastAuthEvidence: undefined,
    }));
    appendAuditLog(
      'account_link',
      'Account Identity Unlinked',
      `User manually unlinked the Active Directory Workstation ticket association. Automatic silent sign-on disabled.`,
      'warning',
      identity.samAccountName
    );
  };

  // Mock domain registration
  const handleAddDomain = (dom: Omit<EnterpriseDomain, 'id'>) => {
    const newDom = { ...dom, id: `dom-${Date.now()}` };
    setDomains([...domains, newDom]);
    appendAuditLog(
      'policy_update',
      `Registered new AD Domain Realm: ${dom.name}`,
      `Administrator registered and verified forest path mapping for active realm ${dom.name} pointing to controller ${dom.kdcServer}.`,
      'success',
      'CORP\\administrator'
    );
  };

  const handleDeleteDomain = (id: string) => {
    const target = domains.find((d) => d.id === id);
    setDomains(domains.filter((d) => d.id !== id));
    if (target) {
      appendAuditLog(
        'policy_update',
        `Deleted Domain Realm: ${target.name}`,
        `Administrator removed verified forest mapping for realm ${target.name}. Workstations inside this realm can no longer authenticate.`,
        'warning',
        'CORP\\administrator'
      );
    }
  };

  // Mock SPN registration
  const handleAddSpn = (spnVal: Omit<ServicePrincipalName, 'id'>) => {
    const newSpnObj = { ...spnVal, id: `spn-${Date.now()}` };
    setSpns([...spns, newSpnObj]);
    appendAuditLog(
      'policy_update',
      `Registered Service Principal Name: ${spnVal.spn}`,
      `Registered active web endpoint ticket mapper mapping ${spnVal.spn} to corporate AD account: ${spnVal.serviceAccount}.`,
      'success',
      'CORP\\administrator'
    );
  };

  const handleDeleteSpn = (id: string) => {
    const target = spns.find((s) => s.id === id);
    setSpns(spns.filter((s) => s.id !== id));
    if (target) {
      appendAuditLog(
        'policy_update',
        `Removed SPN: ${target.spn}`,
        `Deleted Service Principal mapping for ${target.spn}. Clients requesting this host will fail validation with KDC.`,
        'warning',
        'CORP\\administrator'
      );
    }
  };

  const handleRotateSpnKey = (id: string) => {
    appendAuditLog(
      'policy_update',
      'Rotated Service Account cryptographic key credentials',
      'Cryptographic AES256 keytab hashes rotated. Key Version Number (KVNO) incremented inside the KDC schema.',
      'success',
      'CORP\\administrator'
    );
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* Universal Enterprise Header */}
      <header className="bg-slate-900 text-white border-b border-slate-800 shrink-0">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-blue-600 flex items-center justify-center shadow-lg shadow-blue-500/20 border border-blue-400/20">
              <Laptop className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-2">
                <h1 className="text-lg font-bold font-display tracking-tight text-white leading-none">WIA Hub</h1>
                <span className="bg-blue-500/10 border border-blue-500/35 text-[10px] font-semibold text-blue-400 font-mono px-1.5 py-0.5 rounded">v1.2</span>
              </div>
              <p className="text-xs text-slate-400 mt-1">Windows Integrated Authentication & Kerberos Operations Portal</p>
            </div>
          </div>

          {/* Tab Navigation */}
          <nav className="flex bg-slate-950/80 p-1 rounded-lg border border-slate-800" aria-label="Main Navigation">
            <button
              onClick={() => setActiveTab('gateway')}
              className={`px-4 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                activeTab === 'gateway' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <LayoutDashboard className="w-3.5 h-3.5" />
              SSO Portal Gateway
            </button>
            <button
              onClick={() => setActiveTab('profile')}
              className={`px-4 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                activeTab === 'profile' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <UserCheck className="w-3.5 h-3.5" />
              User Profile Enrollment
            </button>
            <button
              onClick={() => setActiveTab('admin')}
              className={`px-4 py-1.5 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-all cursor-pointer ${
                activeTab === 'admin' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
              }`}
            >
              <Settings className="w-3.5 h-3.5" />
              Admin Operations Panel
            </button>
          </nav>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {activeTab === 'gateway' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Interactive Portal Area */}
            <div className="lg:col-span-7 flex flex-col items-center justify-center py-6">
              <div className="w-full flex justify-center">
                {authState === 'idle' && (
                  <EnterpriseMethodCard
                    onStartAuth={startAuthentication}
                    simConfig={simConfig}
                    orgName="Acme Enterprise"
                  />
                )}

                {authState === 'negotiating' && (
                  <IntegratedAuthProgress
                    simConfig={simConfig}
                    onSuccess={handleAuthSuccess}
                    onFailure={handleAuthFailure}
                    onCancel={() => setAuthState('idle')}
                    spn={authProgressSpn}
                  />
                )}

                {authState === 'notice_error' && authError && (
                  <ManagedEnvironmentNotice
                    errorCode={authError.code}
                    errorMessage={authError.message}
                    onRetry={() => {
                      setAuthState('idle');
                      setAuthError(null);
                    }}
                    onFallbackLocal={() => {
                      appendAuditLog(
                        'discovery',
                        'Fallback Local Factor initiated',
                        'User requested manual password fallback due to unmanaged environment constraints.',
                        'success',
                        'Anonymous'
                      );
                      alert('Redirecting to Workplace Local Password & OTP verification screen.');
                    }}
                    onFallbackFederation={() => {
                      appendAuditLog(
                        'discovery',
                        'Fallback Federated IdP redirected',
                        'User redirected to federated OIDC/SAML corporate identity provider.',
                        'success',
                        'Anonymous'
                      );
                      alert('Broker redirecting: SAML 2.0 AuthRequest dispatching to AzureAD/Microsoft Entra SSO gateway.');
                    }}
                  />
                )}

                {authState === 'link_risk_gate' && (
                  <AccountLinkRiskGate
                    localEmail="j.doe@corp.enterprise.local"
                    mappedIdentity={identity}
                    onApprove={handleApproveLinkAssociation}
                    onReject={handleDeclineLinkAssociation}
                  />
                )}

                {authState === 'signed_in' && (
                  <div className="w-full max-w-md bg-white rounded-2xl border border-slate-200 shadow-xl overflow-hidden animate-fadeIn">
                    <div className="p-6 pb-4 bg-gradient-to-br from-slate-900 to-slate-950 text-white relative text-center">
                      <div className="w-14 h-14 rounded-full bg-emerald-500/20 border border-emerald-400/30 flex items-center justify-center mx-auto mb-3 text-emerald-400">
                        <ShieldCheck className="w-8 h-8" />
                      </div>
                      <span className="text-[10px] font-mono font-bold text-emerald-400 uppercase bg-emerald-500/10 border border-emerald-500/20 px-2 py-0.5 rounded">
                        Verified Auth Session
                      </span>
                      <h2 className="font-display text-xl font-bold tracking-tight text-white mt-3">
                        Signed In Successfully
                      </h2>
                      <p className="text-xs text-slate-400 mt-1">Acme Workplace SSO Gateway</p>
                    </div>

                    <div className="p-6 space-y-4">
                      <div className="p-4 bg-slate-50 border border-slate-100 rounded-xl space-y-3.5">
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">Identity Principle:</span>
                          <span className="font-mono font-semibold text-slate-800">{identity.samAccountName}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">UPN:</span>
                          <span className="font-mono text-slate-800">{identity.upn}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">AMR Emitted Code:</span>
                          <span className="font-mono text-blue-700 font-semibold">{identity.lastAuthEvidence?.amr.join(', ')}</span>
                        </div>
                        <div className="flex justify-between text-xs">
                          <span className="text-slate-400">Audience SPN:</span>
                          <span className="font-mono text-slate-700 truncate max-w-[180px]">{identity.lastAuthEvidence?.spnUsed}</span>
                        </div>
                      </div>

                      <div className="flex gap-2">
                        <button
                          onClick={() => {
                            setAuthState('idle');
                            appendAuditLog('token_validation', 'User session signed out manually', 'Active cookie terminated.', 'warning', identity.samAccountName);
                          }}
                          className="w-full py-2.5 px-4 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg flex items-center justify-center gap-1.5 transition-colors cursor-pointer shadow-md"
                        >
                          <LogOut className="w-3.5 h-3.5" /> Terminate Session
                        </button>
                        <button
                          onClick={() => setActiveTab('profile')}
                          className="w-full py-2.5 px-4 bg-white hover:bg-slate-50 text-slate-700 border border-slate-200 text-xs font-semibold rounded-lg text-center cursor-pointer transition-colors"
                        >
                          Review Mapping Details
                        </button>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            </div>

            {/* Simulation Controller Panel */}
            <div className="lg:col-span-5 bg-white rounded-2xl border border-slate-200 p-6 space-y-6 shadow-sm">
              <div>
                <h3 className="font-display font-semibold text-slate-800 text-base flex items-center gap-1.5">
                  <Server className="w-4.5 h-4.5 text-blue-600" />
                  WIA Simulation Control Panel
                </h3>
                <p className="text-xs text-slate-500 mt-0.5">Toggle active directory errors, browsers, and network locations to evaluate the login experience instantly.</p>
              </div>

              <div className="space-y-4">
                {/* Simulation Mode selector */}
                <div>
                  <label htmlFor="sim-mode" className="block text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider mb-2">Active Simulation Mode</label>
                  <select
                    id="sim-mode"
                    value={simConfig.activeMode}
                    onChange={(e) => handleSimModeChange(e.target.value as SimMode)}
                    className="w-full px-3 py-2 text-xs rounded-lg border border-slate-300 bg-white text-slate-800 outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <optgroup label="Success Paths">
                      <option value="success_auto">Perfect Silent Automatic Sign-In (success_auto)</option>
                      <option value="success_prompt">OS Credential Prompt Handoff (success_prompt)</option>
                    </optgroup>
                    <optgroup label="Workstation/Browser Constraints">
                      <option value="unsupported_browser">Unsupported Browser Zone Policy</option>
                      <option value="unmanaged_device">Unmanaged Device (KDC offline)</option>
                      <option value="private_mode">Private/Incognito Window Restriction</option>
                    </optgroup>
                    <optgroup label="Realm Trust & Account Errors">
                      <option value="domain_mismatch">Realm Domain Mismatch / Untrusted</option>
                      <option value="ambiguous_mapping">Ambiguous User Identity Mapping</option>
                      <option value="account_denied">AD Account Locked / Suspended</option>
                    </optgroup>
                    <optgroup label="Handshake Protocol Failures">
                      <option value="clock_skew">Clock DriftSkew &gt; 5 Minutes</option>
                      <option value="spn_failure">Principal Unknown (SPN Unknown)</option>
                      <option value="trust_failure">Cross-Forest Trust Expired</option>
                      <option value="provider_timeout">Domain Controller Connection Timeout</option>
                      <option value="credential_replay">Token Anti-Replay Counter Trigger</option>
                      <option value="proxy_stripped">HTTP Intermediary Proxy Stripped Headers</option>
                    </optgroup>
                  </select>
                </div>

                {/* Environment configurations */}
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label htmlFor="browser-sel" className="block text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Client Browser Profile</label>
                    <select
                      id="browser-sel"
                      value={simConfig.browserType}
                      onChange={(e) => setSimConfig({ ...simConfig, browserType: e.target.value as any })}
                      className="w-full px-2 py-1.5 text-xs rounded border border-slate-300 bg-white"
                    >
                      <option value="Chrome_Managed">Google Chrome (Managed)</option>
                      <option value="Edge_Enterprise">Microsoft Edge (Corp)</option>
                      <option value="Firefox_Unmanaged">Firefox (Unmanaged)</option>
                      <option value="Safari_Private">Safari (Private Tab)</option>
                      <option value="Native_App">Native Workplace Client</option>
                    </select>
                  </div>

                  <div>
                    <label htmlFor="spn-sel" className="block text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider mb-1.5">Requested Portal SPN</label>
                    <select
                      id="spn-sel"
                      value={authProgressSpn}
                      onChange={(e) => setAuthProgressSpn(e.target.value)}
                      className="w-full px-2.5 py-1.5 text-xs rounded border border-slate-300 bg-white font-mono"
                    >
                      {spns.map((s) => (
                        <option key={s.id} value={s.spn}>{s.spn}</option>
                      ))}
                    </select>
                  </div>
                </div>

                {/* Location and Clock skew controls */}
                <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold text-slate-700">Network Domain Scope</span>
                    <button
                      onClick={() => setSimConfig({ ...simConfig, isCorpNetwork: !simConfig.isCorpNetwork })}
                      className={`text-[10px] px-2 py-0.5 rounded font-mono font-bold uppercase transition-all cursor-pointer ${
                        simConfig.isCorpNetwork ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-amber-50 text-amber-700 border border-amber-200'
                      }`}
                    >
                      {simConfig.isCorpNetwork ? 'Intranet Realm' : 'External Web'}
                    </button>
                  </div>

                  <div className="space-y-1">
                    <div className="flex justify-between items-center text-[11px]">
                      <span className="text-slate-600">Simulated Clock Offset:</span>
                      <span className={`font-mono font-bold ${Math.abs(simConfig.systemClockOffsetSeconds) >= 300 ? 'text-rose-600' : 'text-slate-600'}`}>
                        {simConfig.systemClockOffsetSeconds}s
                      </span>
                    </div>
                    <input
                      type="range"
                      min="-350"
                      max="350"
                      step="10"
                      value={simConfig.systemClockOffsetSeconds}
                      onChange={(e) => setSimConfig({ ...simConfig, systemClockOffsetSeconds: parseInt(e.target.value) })}
                      className="w-full cursor-pointer accent-blue-600"
                    />
                  </div>

                  <div className="flex items-center justify-between pt-1">
                    <span className="text-xs font-semibold text-slate-700">Simulate OS Dialog Cancel</span>
                    <input
                      type="checkbox"
                      checked={simConfig.simulatePromptCancellation}
                      onChange={(e) => setSimConfig({ ...simConfig, simulatePromptCancellation: e.target.checked })}
                      className="w-4 h-4 rounded text-blue-600 border-slate-300 focus:ring-blue-500 cursor-pointer"
                    />
                  </div>
                </div>
              </div>

              <div className="pt-2">
                <button
                  onClick={() => {
                    setAuthState('idle');
                    setAuthError(null);
                  }}
                  className="w-full py-2 bg-blue-50 hover:bg-blue-100/70 text-blue-700 rounded-lg text-xs font-semibold transition-colors flex items-center justify-center gap-1 cursor-pointer"
                >
                  <RefreshCw className="w-3.5 h-3.5" /> Reset Authentication Playground
                </button>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'profile' && (
          <div className="space-y-6">
            <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
              <h2 className="font-display font-semibold text-slate-950 text-xl">User Enrollment Center</h2>
              <p className="text-xs text-slate-500 mt-1">Review active mapping link status, secure credential telemetry, and request step-up validations.</p>
            </div>

            <EnterpriseIdentityProjection
              identity={identity}
              onLink={() => {
                setIdentity({
                  ...identity,
                  linkedAt: new Date().toLocaleDateString(),
                });
                appendAuditLog('account_link', 'Account Mapping Manually Linked', 'Linked Workstation credential via profile dashboard.', 'success', identity.samAccountName);
              }}
              onUnlink={handleUnlinkIdentity}
              onTriggerMfaStepUp={() => {
                const stepUp = prompt('Enter your corporate step-up authentication code to elevate assurance to High:');
                if (stepUp) {
                  setIdentity({ ...identity, assuranceLevel: 'High' });
                  appendAuditLog('token_validation', 'Step-up Assurance verified', 'User elevated authentication level to High via MFA.', 'success', identity.samAccountName, ['wia', 'mfa']);
                  alert('Assurance level elevated successfully.');
                }
              }}
            />
          </div>
        )}

        {activeTab === 'admin' && (
          <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
            {/* Sidebar sub-navigation */}
            <div className="lg:col-span-3 bg-white rounded-2xl border border-slate-200 p-4 space-y-1.5 shadow-sm">
              <span className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-widest block px-3 mb-2">Management Realms</span>

              <button
                onClick={() => setAdminSubTab('domains')}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 cursor-pointer transition-colors ${
                  adminSubTab === 'domains' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >
                <Server className="w-4 h-4" /> Domains & SPN Map
              </button>

              <button
                onClick={() => setAdminSubTab('policies')}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 cursor-pointer transition-colors ${
                  adminSubTab === 'policies' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >
                <Laptop className="w-4 h-4" /> Browser GPO Policies
              </button>

              <button
                onClick={() => setAdminSubTab('health')}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 cursor-pointer transition-colors ${
                  adminSubTab === 'health' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >
                <HeartPulse className="w-4 h-4" /> DC Health Telemetry
              </button>

              <button
                onClick={() => setAdminSubTab('terminal')}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 cursor-pointer transition-colors ${
                  adminSubTab === 'terminal' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >
                <TermIcon className="w-4 h-4" /> Diagnostic CLI
              </button>

              <button
                onClick={() => setAdminSubTab('audit')}
                className={`w-full text-left px-3 py-2 rounded-lg text-xs font-semibold flex items-center gap-2 cursor-pointer transition-colors ${
                  adminSubTab === 'audit' ? 'bg-slate-100 text-slate-900' : 'text-slate-500 hover:bg-slate-50 hover:text-slate-800'
                }`}
              >
                <FileText className="w-4 h-4" /> Audit Log Trail
              </button>
            </div>

            {/* Sub-tab detail display */}
            <div className="lg:col-span-9">
              {adminSubTab === 'domains' && (
                <DomainProviderConfig
                  domains={domains}
                  spns={spns}
                  onAddDomain={handleAddDomain}
                  onDeleteDomain={handleDeleteDomain}
                  onAddSpn={handleAddSpn}
                  onDeleteSpn={handleDeleteSpn}
                  onRotateSpnKey={handleRotateSpnKey}
                />
              )}

              {adminSubTab === 'policies' && (
                <BrowserCompatibilityMatrix
                  policy={policy}
                  onUpdatePolicy={(p) => {
                    setPolicy(p);
                    appendAuditLog('policy_update', 'Group Policy GPO modified', 'Administrator altered browser extension parameters and target zone requirements.', 'success', 'CORP\\administrator');
                  }}
                />
              )}

              {adminSubTab === 'health' && (
                <EnterpriseHealthSummary
                  metrics={getHealthMetrics()}
                />
              )}

              {adminSubTab === 'terminal' && (
                <CliDiagnostics
                  currentSpn={authProgressSpn}
                  currentDomain={domains[0]?.name || 'corp.enterprise.local'}
                />
              )}

              {adminSubTab === 'audit' && (
                <SecurityAuditLogs
                  logs={auditLogs}
                />
              )}
            </div>
          </div>
        )}
      </main>

      {/* Corporate Compliance Footer */}
      <footer className="bg-slate-900 border-t border-slate-800 text-slate-400 py-6 shrink-0 mt-12 text-xs">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <Globe className="w-4 h-4 text-blue-500" />
            <span>FIPS 140-2 Cryptographic Handshake Engine Activated</span>
          </div>
          <div>
            <p>&copy; 2026 Acme Enterprise Operations. All Rights Reserved. Redacted Telemetry Logs.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
