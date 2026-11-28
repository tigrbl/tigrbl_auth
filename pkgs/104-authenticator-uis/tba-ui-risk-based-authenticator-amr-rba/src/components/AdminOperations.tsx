import React, { useState } from 'react';
import { SmartCard, TrustAnchor, MTLSConfig, AuditLog, TrustHealthMetrics } from '../types';
import { mockTrustAnchors, mockMTLSConfigs } from '../data/mockData';
import { 
  ShieldAlert, Settings, Network, Server, FileCheck, CheckCircle2, 
  Activity, Search, HelpCircle, Lock, ShieldCheck, Clipboard, FileText, 
  RefreshCw, Sliders, Play, Plus, Trash2, Eye, ExternalLink, AlertTriangle
} from 'lucide-react';

interface AdminOperationsProps {
  cards: SmartCard[];
  trustAnchors: TrustAnchor[];
  mTLSConfigs: MTLSConfig[];
  auditLogs: AuditLog[];
  onAddTrustAnchor: (anchor: TrustAnchor) => void;
  onRemoveTrustAnchor: (id: string) => void;
  onAddMTLSConfig: (config: MTLSConfig) => void;
  onRemoveMTLSConfig: (id: string) => void;
  trustOutage: boolean;
  onToggleTrustOutage: () => void;
  onLogIncident: (log: Omit<AuditLog, 'id' | 'timestamp'>) => void;
}

export const AdminOperations: React.FC<AdminOperationsProps> = ({
  cards,
  trustAnchors,
  mTLSConfigs,
  auditLogs,
  onAddTrustAnchor,
  onRemoveTrustAnchor,
  onAddMTLSConfig,
  onRemoveMTLSConfig,
  trustOutage,
  onToggleTrustOutage,
  onLogIncident,
}) => {
  const [activeSubTab, setActiveSubTab] = useState<'policy' | 'mtls' | 'diagnostics' | 'health' | 'audit'>('policy');
  
  // Search query for audit logs
  const [searchQuery, setSearchQuery] = useState('');

  // Diagnostic states
  const [diagSelectedCardId, setDiagSelectedCardId] = useState<string>(cards[0]?.id || '');
  const [diagResults, setDiagResults] = useState<{ step: string; status: 'pass' | 'fail' | 'warning' | 'pending'; msg: string }[]>([]);
  const [diagRunning, setDiagRunning] = useState(false);

  // New Trust Anchor states
  const [showAddAnchor, setShowAddAnchor] = useState(false);
  const [newAnchorName, setNewAnchorName] = useState('');
  const [newAnchorSubject, setNewAnchorSubject] = useState('');
  const [newAnchorCrl, setNewAnchorCrl] = useState('');

  // New mTLS Endpoint states
  const [showAddMtls, setShowAddMtls] = useState(false);
  const [newMtlsName, setNewMtlsName] = useState('');
  const [newMtlsEndpoint, setNewMtlsEndpoint] = useState('');
  const [newMtlsStrategy, setNewMtlsStrategy] = useState<'strict-chain' | 'san-mapping' | 'subject-exact'>('san-mapping');
  const [newMtlsCertFingerprint, setNewMtlsCertFingerprint] = useState('');

  // EKU Policy setting
  const [ekuClientAuth, setEkuClientAuth] = useState(true);
  const [ekuSmartcardLogon, setEkuSmartcardLogon] = useState(true);
  const [revocationCheckMode, setRevocationCheckMode] = useState<'both' | 'ocsp' | 'crl'>('both');

  const runDiagnostics = () => {
    if (!diagSelectedCardId) return;
    setDiagRunning(true);
    setDiagResults([]);

    const card = cards.find(c => c.id === diagSelectedCardId);
    if (!card) return;

    const steps = [
      { step: 'Smart Card PKCS#11 Driver Connection Check', status: 'pending' as const, msg: 'Testing communication layer...' },
      { step: 'Public Certificate Profile Parsing & Encoding', status: 'pending' as const, msg: 'Validating DER x509 structures...' },
      { step: 'Extended Key Usage (EKU) Domain Mapping', status: 'pending' as const, msg: 'Asserting strict EKU capabilities...' },
      { step: 'Trust Chain Construction to Root Anchors', status: 'pending' as const, msg: 'Searching trust paths in local store...' },
      { step: 'Real-Time Revocation Status Assessment', status: 'pending' as const, msg: 'Contacting CRL and OCSP endpoints...' },
      { step: 'Clock Skew & Validation Boundary Checks', status: 'pending' as const, msg: 'Evaluating active period constraints...' },
    ];

    let current = 0;
    const interval = setInterval(() => {
      if (current >= steps.length) {
        clearInterval(interval);
        setDiagRunning(false);
        return;
      }

      const stepIndex = current;
      let finalStatus: 'pass' | 'fail' | 'warning' = 'pass';
      let finalMsg = 'Operational. Check passed successfully.';

      // Logic overrides based on card values and sandbox outage state
      if (stepIndex === 0) {
        finalMsg = `Connected via local client driver ${card.hardware.reader.split(' ')[0]}. Card reader online.`;
      } else if (stepIndex === 1) {
        finalMsg = `Valid certificate schema found. Subject CN parsed correctly.`;
      } else if (stepIndex === 2) {
        const isWrongProfile = card.eku.length === 1 && card.eku[0].includes('Secure Email');
        if (isWrongProfile) {
          finalStatus = 'fail';
          finalMsg = 'Critical Profile Violation: EKU contains secureEmail only. Lacks clientAuth (1.3.6.1.5.5.7.3.2).';
        } else {
          finalMsg = `EKU asserts: ${card.eku.join(', ')}. Conforms to organization access profile.`;
        }
      } else if (stepIndex === 3) {
        if (card.status === 'expired') {
          finalStatus = 'fail';
          finalMsg = 'Chain Construction Failed: Root anchor is valid, but child certificate is out of active date limits.';
        } else {
          finalMsg = `Chain successfully built to trusted root anchor: ${card.issuer.split(',')[0].replace('CN=', '')}.`;
        }
      } else if (stepIndex === 4) {
        if (trustOutage) {
          finalStatus = 'fail';
          finalMsg = 'Outage Out: OCSP lookup and CRL downloads returned HTTP-504 timeout error.';
        } else if (card.status === 'revoked') {
          finalStatus = 'fail';
          finalMsg = 'Revocation Asserted: Serial listed on CRL. Reason Code: KeyCompromise.';
        } else if (card.status === 'expiring') {
          finalStatus = 'warning';
          finalMsg = 'Warning: Certificate is close to expiry. Overlap grace period is currently running.';
        } else {
          finalMsg = 'Active Status Confirmed: OCSP responder returned signed positive status (freshness: 2.5m).';
        }
      } else if (stepIndex === 5) {
        if (card.status === 'expired') {
          finalStatus = 'fail';
          finalMsg = `Validation boundaries violated. Certificate expired on ${new Date(card.notAfter).toLocaleDateString()}.`;
        } else if (card.status === 'expiring') {
          finalStatus = 'warning';
          finalMsg = 'Valid, but nearing boundary constraint. Expiry is under 30 days.';
        } else {
          finalMsg = `Clock verified. Active validity range matches local client time.`;
        }
      }

      setDiagResults(prev => [...prev, { step: steps[stepIndex].step, status: finalStatus, msg: finalMsg }]);
      current++;
    }, 450);
  };

  const handleAddAnchorSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newAnchorName || !newAnchorSubject) return;

    const newAnchor: TrustAnchor = {
      id: `root-${Date.now()}`,
      name: newAnchorName,
      subject: newAnchorSubject,
      status: 'trusted',
      expiry: '2036-12-31T23:59:59Z',
      crlUrl: newAnchorCrl || 'http://http.fpki.gov/custom/crl',
      ocspUrl: 'http://ocsp.fpki.gov',
      allowedEkis: ['Client Authentication (1.3.6.1.5.5.7.3.2)']
    };

    onAddTrustAnchor(newAnchor);
    setNewAnchorName('');
    setNewAnchorSubject('');
    setNewAnchorCrl('');
    setShowAddAnchor(false);
    onLogIncident({
      event: 'sc.trust.anchor_added',
      actor: 'ADMINISTRATOR',
      status: 'success',
      details: `Added new root trust anchor: "${newAnchor.name}" supporting clientAuth.`,
      ipAddress: '10.142.0.2'
    });
  };

  const handleAddMtlsSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newMtlsName || !newMtlsEndpoint) return;

    const newConfig: MTLSConfig = {
      id: `mtls-${Date.now()}`,
      name: newMtlsName,
      endpoint: newMtlsEndpoint,
      boundCertFingerprint: newMtlsCertFingerprint || 'SHA-256: ALL_CERTS_STRICT_CHAIN',
      authStrategy: newMtlsStrategy,
      createdAt: new Date().toISOString(),
      status: 'active'
    };

    onAddMTLSConfig(newConfig);
    setNewMtlsName('');
    setNewMtlsEndpoint('');
    setNewMtlsCertFingerprint('');
    setShowAddMtls(false);
    onLogIncident({
      event: 'sc.mtls.endpoint_configured',
      actor: 'ADMINISTRATOR',
      status: 'success',
      details: `Configured new mTLS client endpoint gateway: "${newConfig.name}" with mapping strategy: ${newConfig.authStrategy}.`,
      ipAddress: '10.142.0.2'
    });
  };

  // Mask sensitive parts of subject for privacy-compliant logging
  const maskSubject = (subjectStr: string) => {
    return subjectStr.replace(/CN=([^,]+)/, (match, p1) => {
      const parts = p1.split('.');
      if (parts.length > 2) {
        return `CN=${parts[0]}.${parts[1]}.******.${parts[parts.length - 1]}`;
      }
      return `CN=${p1.slice(0, 4)}******`;
    });
  };

  const filteredLogs = auditLogs.filter(log => {
    const q = searchQuery.toLowerCase();
    return log.event.toLowerCase().includes(q) || 
           log.details.toLowerCase().includes(q) || 
           log.actor.toLowerCase().includes(q);
  });

  return (
    <div className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm flex flex-col h-full" id="admin-panel">
      {/* Sidebar selection tabs */}
      <div className="bg-slate-50 border-b border-slate-200 flex flex-wrap gap-1 px-4 py-2">
        <button
          onClick={() => setActiveSubTab('policy')}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === 'policy' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-800'
          }`}
          id="btn-admin-tab-policy"
        >
          <Sliders className="w-3.5 h-3.5" />
          Trust Policy
        </button>
        <button
          onClick={() => setActiveSubTab('mtls')}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === 'mtls' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-800'
          }`}
          id="btn-admin-tab-mtls"
        >
          <Server className="w-3.5 h-3.5" />
          mTLS Gateways
        </button>
        <button
          onClick={() => {
            setActiveSubTab('diagnostics');
            if (cards.length > 0 && !diagSelectedCardId) {
              setDiagSelectedCardId(cards[0].id);
            }
          }}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === 'diagnostics' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-800'
          }`}
          id="btn-admin-tab-diag"
        >
          <Activity className="w-3.5 h-3.5" />
          Diagnostics
        </button>
        <button
          onClick={() => setActiveSubTab('health')}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === 'health' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-800'
          }`}
          id="btn-admin-tab-health"
        >
          <Network className="w-3.5 h-3.5" />
          Trust Health
        </button>
        <button
          onClick={() => setActiveSubTab('audit')}
          className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-semibold rounded-lg transition-colors ${
            activeSubTab === 'audit' ? 'bg-indigo-600 text-white shadow-xs' : 'text-slate-600 hover:bg-slate-200 hover:text-slate-800'
          }`}
          id="btn-admin-tab-audit"
        >
          <Clipboard className="w-3.5 h-3.5" />
          Audit Logs
        </button>
      </div>

      {/* Detail Area */}
      <div className="p-5 flex-1 min-h-[420px] flex flex-col justify-between">
        {activeSubTab === 'policy' && (
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="text-sm font-bold text-slate-800">PIV/CAC Root Anchors & Key Policies</h4>
                <p className="text-xs text-slate-500 mt-0.5">Govern root validation chains, allowed EKU mapping filters, and algorithms.</p>
              </div>
              <button
                onClick={() => setShowAddAnchor(!showAddAnchor)}
                className="px-2.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg flex items-center gap-1 transition-colors shadow-xs"
                id="btn-add-trust-anchor"
              >
                <Plus className="w-3.5 h-3.5" />
                Add Trust Root
              </button>
            </div>

            {showAddAnchor && (
              <form onSubmit={handleAddAnchorSubmit} className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3.5">
                <div className="text-xs font-bold text-slate-700">Add Trusted Root Authority</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3.5 text-xs">
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">Anchor Name</label>
                    <input
                      type="text"
                      value={newAnchorName}
                      onChange={(e) => setNewAnchorName(e.target.value)}
                      placeholder="e.g. DoD Root CA 6"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                      required
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">Subject DN</label>
                    <input
                      type="text"
                      value={newAnchorSubject}
                      onChange={(e) => setNewAnchorSubject(e.target.value)}
                      placeholder="e.g. CN=DoD Root CA 6,O=U.S. Government,C=US"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                      required
                    />
                  </div>
                </div>
                <div className="space-y-1 text-xs">
                  <label className="text-[10px] font-bold text-slate-500 uppercase">CRL Distribution Point Endpoint</label>
                  <input
                    type="url"
                    value={newAnchorCrl}
                    onChange={(e) => setNewAnchorCrl(e.target.value)}
                    placeholder="http://crl.disa.mil/dodca6/dodca6.crl"
                    className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                  />
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setShowAddAnchor(false)}
                    className="px-3 py-1.5 text-slate-600 bg-white border border-slate-300 rounded-lg text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-bold shadow-xs"
                  >
                    Authorize Anchor
                  </button>
                </div>
              </form>
            )}

            {/* List of root anchors */}
            <div className="space-y-2.5">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Authorized Trust Anchors</span>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                {trustAnchors.map((anchor) => (
                  <div key={anchor.id} className="p-3 bg-slate-50 rounded-lg border border-slate-200 flex justify-between items-start">
                    <div className="min-w-0 flex-1">
                      <div className="flex items-center gap-1.5">
                        <span className={`w-1.5 h-1.5 rounded-full ${anchor.status === 'trusted' ? 'bg-emerald-400 animate-pulse' : 'bg-rose-400'}`}></span>
                        <span className="text-xs font-bold text-slate-800">{anchor.name}</span>
                      </div>
                      <p className="text-[9.5px] font-mono text-slate-500 mt-0.5 truncate">{anchor.subject}</p>
                      <p className="text-[9.5px] text-slate-400 mt-0.5 font-mono truncate">CRL: {anchor.crlUrl}</p>
                    </div>
                    <button
                      onClick={() => {
                        if (confirm(`Remove trust anchor: ${anchor.name}?`)) {
                          onRemoveTrustAnchor(anchor.id);
                          onLogIncident({
                            event: 'sc.trust.anchor_removed',
                            actor: 'ADMINISTRATOR',
                            status: 'warning',
                            details: `Removed trusted root anchor: "${anchor.name}".`,
                            ipAddress: '10.142.0.2'
                          });
                        }
                      }}
                      className="text-slate-400 hover:text-rose-600 p-1 rounded hover:bg-slate-150 transition-colors ml-1.5"
                      title="Remove Anchor"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                ))}
              </div>
            </div>

            {/* General policies mapping */}
            <div className="bg-slate-50 p-4 border border-slate-200 rounded-lg grid grid-cols-1 sm:grid-cols-3 gap-5 text-xs">
              <div className="space-y-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">EKU Restrictions</span>
                <label className="flex items-center gap-2 text-slate-700 font-semibold">
                  <input
                    type="checkbox"
                    checked={ekuClientAuth}
                    onChange={(e) => setEkuClientAuth(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  Client Authentication (1.3.6.1.5.5.7.3.2)
                </label>
                <label className="flex items-center gap-2 text-slate-700 font-semibold">
                  <input
                    type="checkbox"
                    checked={ekuSmartcardLogon}
                    onChange={(e) => setEkuSmartcardLogon(e.target.checked)}
                    className="rounded border-slate-300 text-indigo-600 focus:ring-indigo-500"
                  />
                  Smartcard Logon (1.3.6.1.4.1.311.20.2.2)
                </label>
              </div>

              <div className="space-y-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Revocation Verification</span>
                <select
                  value={revocationCheckMode}
                  onChange={(e) => setRevocationCheckMode(e.target.value as any)}
                  className="w-full px-2 py-1 bg-white border border-slate-300 rounded text-xs text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                >
                  <option value="both">CRL and OCSP (Strict Double-check)</option>
                  <option value="ocsp">OCSP Check Only (High Latency-safe)</option>
                  <option value="crl">CRL Check Only (Offline-Cached Cache)</option>
                </select>
                <p className="text-[9.5px] text-slate-400 leading-relaxed">
                  Strict double-check contacts real-time OCSP endpoints while falling back to periodically synchronized CRL cache list maps.
                </p>
              </div>

              <div className="space-y-2">
                <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Active Policies Summary</span>
                <div className="bg-white border border-slate-200 rounded p-2 text-[10px] text-slate-500 space-y-1 font-mono">
                  <div>• Min cryptopair: RSA-2048 / ECC P-256</div>
                  <div>• Expiry policy: Strict (No expired allowable)</div>
                  <div>• Mapping rule: SAN PrincipalName primary</div>
                  <div>• CRL cached grace limit: 60 minutes</div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeSubTab === 'mtls' && (
          <div className="space-y-4">
            <div className="flex justify-between items-start">
              <div>
                <h4 className="text-sm font-bold text-slate-800">Developer & Service mTLS Gateway Setup</h4>
                <p className="text-xs text-slate-500 mt-0.5">Govern client mTLS connections routing smart card credentials to application environments.</p>
              </div>
              <button
                onClick={() => setShowAddMtls(!showAddMtls)}
                className="px-2.5 py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-bold rounded-lg flex items-center gap-1 transition-colors shadow-xs"
                id="btn-add-mtls-gateway"
              >
                <Plus className="w-3.5 h-3.5" />
                Configure mTLS Node
              </button>
            </div>

            {showAddMtls && (
              <form onSubmit={handleAddMtlsSubmit} className="bg-slate-50 p-4 rounded-lg border border-slate-200 space-y-3">
                <div className="text-xs font-bold text-slate-700">Configure Client/Server mTLS Node Binding</div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">Gateway Name</label>
                    <input
                      type="text"
                      value={newMtlsName}
                      onChange={(e) => setNewMtlsName(e.target.value)}
                      placeholder="e.g. Secure API Endpoint Alpha"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                      required
                    />
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">External URI endpoint</label>
                    <input
                      type="text"
                      value={newMtlsEndpoint}
                      onChange={(e) => setNewMtlsEndpoint(e.target.value)}
                      placeholder="https://ingress.staging.agency.gov:8443"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                      required
                    />
                  </div>
                </div>
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs">
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">Subject Identifier Mapping Strategy</label>
                    <select
                      value={newMtlsStrategy}
                      onChange={(e) => setNewMtlsStrategy(e.target.value as any)}
                      className="w-full px-3 py-1.5 border border-slate-300 rounded bg-white text-xs text-slate-800"
                    >
                      <option value="san-mapping">SAN RFC822/Principal Name Mapping (Recommended)</option>
                      <option value="strict-chain">Strict Root Issuer Chain Only (Wildcard allowed)</option>
                      <option value="subject-exact">Subject exact match verification (Lock-down)</option>
                    </select>
                  </div>
                  <div className="space-y-1">
                    <label className="text-[10px] font-bold text-slate-500 uppercase">Specific Certificate Fingerprint Pinning (Optional)</label>
                    <input
                      type="text"
                      value={newMtlsCertFingerprint}
                      onChange={(e) => setNewMtlsCertFingerprint(e.target.value)}
                      placeholder="SHA-256 fingerprint for exclusive access pinning"
                      className="w-full px-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white"
                    />
                  </div>
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => setShowAddMtls(false)}
                    className="px-3 py-1.5 text-slate-600 bg-white border border-slate-300 rounded-lg text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button
                    type="submit"
                    className="px-4 py-1.5 bg-indigo-600 text-white rounded-lg text-xs font-bold shadow-xs"
                  >
                    Deploy Gateway Ingress
                  </button>
                </div>
              </form>
            )}

            {/* List of mTLS config nodes */}
            <div className="space-y-2">
              <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Deployed mTLS Ingress Gateways</span>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs">
                {mTLSConfigs.map((config) => (
                  <div key={config.id} className="p-3 bg-slate-50 border border-slate-200 rounded-lg flex flex-col justify-between">
                    <div>
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-slate-800">{config.name}</span>
                        <span className={`text-[8.5px] uppercase tracking-wider px-1.5 font-bold rounded ${
                          config.status === 'active' ? 'bg-emerald-100 text-emerald-800' : 'bg-slate-200 text-slate-600'
                        }`}>
                          {config.status}
                        </span>
                      </div>
                      <div className="text-[10.5px] font-mono text-slate-600 mt-1 font-semibold">{config.endpoint}</div>
                      <div className="grid grid-cols-2 gap-1 text-[10px] text-slate-400 mt-2">
                        <div>Mapping: <span className="text-slate-600 font-mono font-medium">{config.authStrategy}</span></div>
                        <div>Added: <span className="text-slate-600">{new Date(config.createdAt).toLocaleDateString()}</span></div>
                      </div>
                      <div className="text-[9.5px] text-slate-400 mt-1 bg-white p-1 rounded border border-slate-150 truncate font-mono">
                        Bound cert fingerprint: {config.boundCertFingerprint}
                      </div>
                    </div>
                    
                    {/* Shell Config Template Generation */}
                    <div className="mt-3 pt-2 border-t border-dashed border-slate-200 flex justify-between items-center">
                      <button
                        onClick={() => {
                          const curlSample = `curl -v --cert-type PEM --cert client-pub.pem --key client-key.pem \\
  --cacert root-fpki.pem \\
  "${config.endpoint}/api/v1/auth"`;
                          alert(`### EXPORTED mTLS GATEWAY CONFIG PAYLOAD ###\n\nEndpoint: ${config.endpoint}\nStrategy: ${config.authStrategy}\n\nClient Connection Command:\n\n${curlSample}`);
                        }}
                        className="text-[10px] text-indigo-600 hover:text-indigo-800 font-bold flex items-center gap-1"
                      >
                        <ExternalLink className="w-3 h-3" />
                        Export Nginx/cURL Template
                      </button>

                      <button
                        onClick={() => {
                          if (confirm(`Remove mTLS endpoint configuration: ${config.name}?`)) {
                            onRemoveMTLSConfig(config.id);
                            onLogIncident({
                              event: 'sc.mtls.gateway_removed',
                              actor: 'ADMINISTRATOR',
                              status: 'warning',
                              details: `Decommissioned mTLS endpoint gateway: "${config.name}".`,
                              ipAddress: '10.142.0.2'
                            });
                          }
                        }}
                        className="text-slate-400 hover:text-rose-600 p-1"
                        title="Delete Gateway"
                      >
                        <Trash2 className="w-3.5 h-3.5" />
                      </button>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeSubTab === 'diagnostics' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-bold text-slate-800">Hardware Certificate Validation Diagnostics</h4>
              <p className="text-xs text-slate-500 mt-0.5">Test cryptographic signatures, revocation freshness, and path construction without exporting keys.</p>
            </div>

            <div className="bg-slate-50 p-4 border border-slate-200 rounded-lg flex flex-col sm:flex-row gap-4 items-end text-xs">
              <div className="flex-1 space-y-1.5 w-full">
                <label className="text-[10px] font-bold text-slate-500 uppercase block">Select Target Smart-Card Certificate</label>
                <select
                  value={diagSelectedCardId}
                  onChange={(e) => setDiagSelectedCardId(e.target.value)}
                  className="w-full px-3 py-1.8 border border-slate-300 rounded bg-white text-xs text-slate-800"
                  id="diag-select-card"
                >
                  <option value="" disabled>-- Select Enrolled Card --</option>
                  {cards.map(c => (
                    <option key={c.id} value={c.id}>{c.label} ({c.hardware.cardType}) - Serial {c.serialNumber.slice(0, 8)}...</option>
                  ))}
                </select>
              </div>
              <button
                onClick={runDiagnostics}
                disabled={!diagSelectedCardId || diagRunning}
                className="py-1.8 px-4 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded text-xs flex items-center gap-1.5 disabled:bg-slate-300 transition-colors shrink-0 w-full sm:w-auto"
                id="btn-run-diagnostics"
              >
                <Play className="w-3.5 h-3.5" />
                {diagRunning ? 'Running Cryptographic Verification...' : 'Run Full Diagnostics'}
              </button>
            </div>

            {/* Diagnostic results console */}
            {diagResults.length > 0 && (
              <div className="bg-slate-950 p-4 rounded-lg border border-slate-800 font-mono space-y-3 text-xs text-slate-300 max-h-[250px] overflow-y-auto">
                <div className="text-[10px] text-slate-500 font-bold uppercase border-b border-slate-800 pb-1.5">CRYPTOGRAPHIC VERIFICATION RUN OUTPUT</div>
                {diagResults.map((res, idx) => (
                  <div key={idx} className="space-y-1 border-b border-slate-900 pb-2 last:border-none last:pb-0">
                    <div className="flex justify-between">
                      <span className="font-semibold text-slate-200">{res.step}</span>
                      <span className={`text-[10px] font-bold ${
                        res.status === 'pass' ? 'text-emerald-400' :
                        res.status === 'fail' ? 'text-rose-400' : 'text-amber-400'
                      }`}>
                        [{res.status.toUpperCase()}]
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 pl-3 border-l border-slate-800">{res.msg}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}

        {activeSubTab === 'health' && (
          <div className="space-y-4">
            <div>
              <h4 className="text-sm font-bold text-slate-800">Trust Provider & Middleware Health</h4>
              <p className="text-xs text-slate-500 mt-0.5">Real-time status monitoring for FPKI revocation links, latency, and simulated outage bypass hooks.</p>
            </div>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <span className="text-slate-500 text-[10px] block uppercase font-bold tracking-wider">OCSP Ping Latency</span>
                <span className="text-xl font-mono text-slate-800 font-bold mt-1 block">42ms</span>
                <span className="text-[10px] text-emerald-700 font-semibold block mt-1">● Optimal</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <span className="text-slate-500 text-[10px] block uppercase font-bold tracking-wider">CRL Sync Age</span>
                <span className="text-xl font-mono text-slate-800 font-bold mt-1 block">18m ago</span>
                <span className="text-[10px] text-slate-400 block mt-1">Automatic interval: 60m</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <span className="text-slate-500 text-[10px] block uppercase font-bold tracking-wider">Active Trust Anchors</span>
                <span className="text-xl font-mono text-slate-800 font-bold mt-1 block">{trustAnchors.length} Roots</span>
                <span className="text-[10px] text-slate-400 block mt-1">EKU matches required</span>
              </div>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200">
                <span className="text-slate-500 text-[10px] block uppercase font-bold tracking-wider">CRL Status Responder</span>
                <span className={`text-xl font-mono font-bold mt-1 block ${trustOutage ? 'text-rose-600' : 'text-emerald-600'}`}>
                  {trustOutage ? 'OUTAGE' : 'OPERATIONAL'}
                </span>
                <span className={`text-[10px] font-semibold block mt-1 ${trustOutage ? 'text-rose-700' : 'text-emerald-700'}`}>
                  {trustOutage ? '● Responder Timeout' : '● Online'}
                </span>
              </div>
            </div>

            {/* Outage simulator trigger */}
            <div className="bg-slate-50 border border-slate-200 rounded-lg p-4 flex flex-col sm:flex-row justify-between items-center gap-4 text-xs">
              <div className="space-y-1">
                <span className="font-semibold text-slate-800 block">Outage & Degraded Connection Simulator</span>
                <p className="text-[10.5px] text-slate-500 leading-relaxed max-w-md">
                  Simulate a connectivity loss to the external Federal PKI OCSP validation responder. Turn this on to inspect how the P0 authentication ceremony gracefully degrades and suggests recovery paths.
                </p>
              </div>
              <button
                onClick={onToggleTrustOutage}
                className={`px-4 py-2.5 rounded-lg text-xs font-bold transition-all whitespace-nowrap active:scale-98 shadow-xs ${
                  trustOutage 
                    ? 'bg-rose-600 hover:bg-rose-700 text-white' 
                    : 'bg-slate-200 hover:bg-slate-300 text-slate-700 border border-slate-300'
                }`}
                id="btn-toggle-outage-state"
              >
                {trustOutage ? 'Disable Simulated Outage' : 'Simulate OCSP Trust Outage'}
              </button>
            </div>
          </div>
        )}

        {activeSubTab === 'audit' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center gap-4">
              <div>
                <h4 className="text-sm font-bold text-slate-800">High-Assurance Cryptographic Audit Logs</h4>
                <p className="text-xs text-slate-500 mt-0.5">Masked public parameters of authentication attempts, keys enrollment, policy updates, and diagnostic evaluations.</p>
              </div>

              {/* Search bar */}
              <div className="relative max-w-xs w-full shrink-0">
                <Search className="w-3.5 h-3.5 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
                <input
                  type="text"
                  value={searchQuery}
                  onChange={(e) => setSearchQuery(e.target.value)}
                  placeholder="Filter logs by actor, event..."
                  className="w-full pl-8 pr-3 py-1.5 border border-slate-300 rounded-lg text-xs bg-white text-slate-800 focus:outline-none focus:ring-1 focus:ring-indigo-500"
                  id="input-search-audit-logs"
                />
              </div>
            </div>

            {/* Logs List */}
            <div className="border border-slate-200 rounded-lg overflow-hidden bg-slate-50">
              <div className="max-h-[300px] overflow-y-auto">
                <table className="min-w-full divide-y divide-slate-200 text-left text-xs text-slate-600">
                  <thead className="bg-slate-100 text-[10px] font-bold text-slate-500 uppercase tracking-wider select-none sticky top-0">
                    <tr>
                      <th className="px-4 py-2.5">Timestamp</th>
                      <th className="px-4 py-2.5">Security Event</th>
                      <th className="px-4 py-2.5">Sanitized Actor CN</th>
                      <th className="px-4 py-2.5">Status</th>
                      <th className="px-4 py-2.5">Detailed Parameters</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-slate-200 bg-white">
                    {filteredLogs.map((log) => (
                      <tr key={log.id} className="hover:bg-slate-50/50 transition-colors">
                        <td className="px-4 py-3 font-mono text-[10.5px] whitespace-nowrap text-slate-400">
                          {new Date(log.timestamp).toLocaleTimeString()}
                        </td>
                        <td className="px-4 py-3 font-mono font-semibold text-[10.5px] text-slate-700">
                          {log.event}
                        </td>
                        <td className="px-4 py-3 font-mono text-[10px] truncate max-w-[150px]" title={log.actor}>
                          {maskSubject(log.actor)}
                        </td>
                        <td className="px-4 py-3 whitespace-nowrap">
                          <span className={`text-[9.5px] font-bold uppercase tracking-wider px-1.5 rounded-full ${
                            log.status === 'success' ? 'bg-emerald-50 text-emerald-800 border border-emerald-100' :
                            log.status === 'failure' ? 'bg-rose-50 text-rose-800 border border-rose-100' :
                            'bg-amber-50 text-amber-800 border border-amber-100'
                          }`}>
                            {log.status}
                          </span>
                        </td>
                        <td className="px-4 py-3 text-[10.5px] text-slate-500 max-w-sm truncate" title={log.details}>
                          {log.details}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
