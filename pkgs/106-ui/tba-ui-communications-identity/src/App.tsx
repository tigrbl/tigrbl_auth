import React, { useState, useEffect, useCallback } from 'react';
import {
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Clock,
  Plus,
  Webhook,
  Mail,
  FileSignature,
  PhoneCall,
  Layers,
  KeyRound,
  FileCheck2,
  History,
  RefreshCw,
  ArrowUpRight,
} from 'lucide-react';
import {
  CHANNEL_PROFILES,
  INITIAL_IDENTITIES,
  SIGNER_CUSTODY_RECORDS,
  STIR_SHAKEN_RECORDS,
  BIMI_DOMAIN_ASSESSMENTS,
  SMIME_IDENTITY_RECORDS,
  DOCUMENT_CEREMONY_RECORDS,
  WEBHOOK_PROFILE_RECORDS,
  INITIAL_EVIDENCE_RECEIPTS,
  INITIAL_INCIDENTS,
} from './data/seedControlPlane.ts';
import type {
  ChannelFamily,
  ChannelProfileSpec,
  CommunicationIdentity,
  SignerCustodyRecord,
  StirShakenRecord,
  BimiDomainAssessment,
  SmimeIdentityRecord,
  DocumentCeremonyRecord,
  WebhookProfileRecord,
  EvidenceReceipt,
  ChannelIncident,
} from './types/communications.ts';
import { ChannelStudiosView } from './components/ChannelStudiosView.tsx';
import { VerificationWorkbenchView } from './components/VerificationWorkbenchView.tsx';
import { CustodyAndSignersView } from './components/CustodyAndSignersView.tsx';
import { IncidentsAndEvidenceView } from './components/IncidentsAndEvidenceView.tsx';
import { OnboardingWizardModal } from './components/OnboardingWizardModal.tsx';

type ActiveWorkspace =
  | 'overview'
  | 'studios'
  | 'verification'
  | 'custody'
  | 'incidents';

export default function App() {
  const [activeWorkspace, setActiveWorkspace] = useState<ActiveWorkspace>('overview');
  const [activeStudioFamily, setActiveStudioFamily] =
    useState<ChannelFamily>('webhook-http-sig');
  const [wizardOpen, setWizardOpen] = useState(false);

  // State hydrated from backend API (seeded immediately for zero-latency rendering)
  const [profiles, setProfiles] = useState<ChannelProfileSpec[]>(CHANNEL_PROFILES);
  const [identities, setIdentities] =
    useState<CommunicationIdentity[]>(INITIAL_IDENTITIES);
  const [signers, setSigners] =
    useState<SignerCustodyRecord[]>(SIGNER_CUSTODY_RECORDS);
  const [stirRecords, setStirRecords] =
    useState<StirShakenRecord[]>(STIR_SHAKEN_RECORDS);
  const [bimiAssessments, setBimiAssessments] =
    useState<BimiDomainAssessment[]>(BIMI_DOMAIN_ASSESSMENTS);
  const [smimeRecords, setSmimeRecords] =
    useState<SmimeIdentityRecord[]>(SMIME_IDENTITY_RECORDS);
  const [docCeremonies, setDocCeremonies] =
    useState<DocumentCeremonyRecord[]>(DOCUMENT_CEREMONY_RECORDS);
  const [webhookProfiles, setWebhookProfiles] =
    useState<WebhookProfileRecord[]>(WEBHOOK_PROFILE_RECORDS);
  const [receipts, setReceipts] =
    useState<EvidenceReceipt[]>(INITIAL_EVIDENCE_RECEIPTS);
  const [incidents, setIncidents] =
    useState<ChannelIncident[]>(INITIAL_INCIDENTS);

  const [selectedIdentityForHistory, setSelectedIdentityForHistory] = useState<string>(
    INITIAL_IDENTITIES[0].id
  );
  const [channelFilter, setChannelFilter] = useState<'ALL' | ChannelFamily>('ALL');
  const [mutatingIdentityId, setMutatingIdentityId] = useState<string | null>(null);

  const fetchAllControlPlaneState = useCallback(async () => {
    try {
      const [
        profRes,
        idRes,
        sgnRes,
        telRes,
        emailRes,
        docRes,
        whRes,
        evRes,
        incRes,
      ] = await Promise.all([
        fetch('/api/v1/profiles'),
        fetch('/api/v1/communication-identities'),
        fetch('/api/v1/signers'),
        fetch('/api/v1/telephone-identities'),
        fetch('/api/v1/email-identities'),
        fetch('/api/v1/document-signing'),
        fetch('/api/v1/webhook-signing'),
        fetch('/api/v1/evidence'),
        fetch('/api/v1/incidents'),
      ]);

      if (profRes.ok) {
        const d = await profRes.json();
        setProfiles(d.profiles);
      }
      if (idRes.ok) {
        const d = await idRes.json();
        setIdentities(d.identities);
      }
      if (sgnRes.ok) {
        const d = await sgnRes.json();
        setSigners(d.signers);
      }
      if (telRes.ok) {
        const d = await telRes.json();
        setStirRecords(d.records);
      }
      if (emailRes.ok) {
        const d = await emailRes.json();
        setBimiAssessments(d.bimiAssessments);
        setSmimeRecords(d.smimeRecords);
      }
      if (docRes.ok) {
        const d = await docRes.json();
        setDocCeremonies(d.ceremonies);
      }
      if (whRes.ok) {
        const d = await whRes.json();
        setWebhookProfiles(d.profiles);
      }
      if (evRes.ok) {
        const d = await evRes.json();
        setReceipts(d.receipts);
      }
      if (incRes.ok) {
        const d = await incRes.json();
        setIncidents(d.incidents);
      }
    } catch {
      // Fallback to initial seeded state if offline
    }
  }, []);

  useEffect(() => {
    fetchAllControlPlaneState();
  }, [fetchAllControlPlaneState]);

  const handleIdentityLifecycleAction = async (
    identityId: string,
    action: 'SUSPEND' | 'ACTIVATE' | 'ROTATE_KEY'
  ) => {
    setMutatingIdentityId(identityId);
    try {
      const res = await fetch(`/api/v1/communication-identities/${identityId}/status`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ action }),
      });
      if (res.ok) {
        await fetchAllControlPlaneState();
      }
    } finally {
      setMutatingIdentityId(null);
    }
  };

  const openChannelStudio = (family: ChannelFamily) => {
    setActiveStudioFamily(family);
    setActiveWorkspace('studios');
  };

  const filteredIdentities = identities.filter(
    (item) => channelFilter === 'ALL' || item.channelFamily === channelFilter
  );

  const inspectedIdentity =
    identities.find((i) => i.id === selectedIdentityForHistory) || identities[0];

  const activeCount = identities.filter((i) => i.status === 'ACTIVE').length;
  const totalVolume24h = identities.reduce((acc, item) => acc + item.volume24h, 0);
  const deniedCount = receipts.filter(
    (r) => r.authorizationOutcome !== 'AUTHORIZED'
  ).length;

  return (
    <div className="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-900 dark:text-slate-100">
      {/* Top Bar Contract: Zone 1 (Single Brand Wordmark) — Zone 2 (5 Concise Nav Links) — Zone 3 (1 Primary CTA) */}
      <header className="sticky top-0 z-30 flex items-center justify-between gap-8 px-6 py-3.5 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800">
        <a
          href="#overview"
          onClick={(e) => {
            e.preventDefault();
            setActiveWorkspace('overview');
          }}
          className="text-base font-bold tracking-tight text-slate-900 dark:text-slate-100 whitespace-nowrap shrink-0"
        >
          TBA Communications Identity
        </a>

        <nav className="hidden md:flex items-center gap-6 text-xs font-medium text-slate-600 dark:text-slate-400">
          <button
            type="button"
            onClick={() => setActiveWorkspace('overview')}
            className={`py-1 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeWorkspace === 'overview'
                ? 'text-blue-600 dark:text-blue-400 underline underline-offset-8 decoration-2'
                : 'hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            Overview
          </button>
          <button
            type="button"
            onClick={() => setActiveWorkspace('studios')}
            className={`py-1 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeWorkspace === 'studios'
                ? 'text-blue-600 dark:text-blue-400 underline underline-offset-8 decoration-2'
                : 'hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            Channel Studios
          </button>
          <button
            type="button"
            onClick={() => setActiveWorkspace('verification')}
            className={`py-1 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeWorkspace === 'verification'
                ? 'text-blue-600 dark:text-blue-400 underline underline-offset-8 decoration-2'
                : 'hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            Verification Workbench
          </button>
          <button
            type="button"
            onClick={() => setActiveWorkspace('custody')}
            className={`py-1 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeWorkspace === 'custody'
                ? 'text-blue-600 dark:text-blue-400 underline underline-offset-8 decoration-2'
                : 'hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            Custody &amp; Signers
          </button>
          <button
            type="button"
            onClick={() => setActiveWorkspace('incidents')}
            className={`py-1 transition-colors whitespace-nowrap shrink-0 cursor-pointer ${
              activeWorkspace === 'incidents'
                ? 'text-blue-600 dark:text-blue-400 underline underline-offset-8 decoration-2'
                : 'hover:text-slate-900 dark:hover:text-slate-100'
            }`}
          >
            Incidents &amp; Evidence
          </button>
        </nav>

        <div className="flex items-center shrink-0">
          <button
            type="button"
            onClick={() => setWizardOpen(true)}
            className="flex items-center gap-1.5 px-3.5 py-2 text-xs font-medium text-white bg-slate-900 dark:bg-blue-600 hover:bg-slate-800 dark:hover:bg-blue-700 rounded-lg transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            <Plus className="w-3.5 h-3.5" />
            Onboard Identity
          </button>
        </div>
      </header>

      {/* Main Workspace Canvas: 260px Sidebar + Primary Content Viewport */}
      <div className="flex-1 flex flex-col lg:flex-row">
        <aside className="w-full lg:w-64 shrink-0 bg-white dark:bg-slate-900 border-b lg:border-b-0 lg:border-r border-slate-200 dark:border-slate-800 p-4 flex flex-col justify-between gap-6">
          <div className="space-y-6">
            <div>
              <div className="px-2.5 text-[11px] font-semibold text-slate-400 dark:text-slate-500 mb-2">
                Control Plane Workspaces
              </div>
              <div className="space-y-1">
                <button
                  type="button"
                  onClick={() => setActiveWorkspace('overview')}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'overview'
                      ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <ShieldCheck className="w-4 h-4 shrink-0" />
                  <span className="truncate">Identity Overview &amp; Bindings</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveWorkspace('verification')}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'verification'
                      ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <Layers className="w-4 h-4 shrink-0" />
                  <span className="truncate">Verification Workbench</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveWorkspace('custody')}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'custody'
                      ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <KeyRound className="w-4 h-4 shrink-0" />
                  <span className="truncate">Key Custody &amp; Signer API</span>
                </button>
                <button
                  type="button"
                  onClick={() => setActiveWorkspace('incidents')}
                  className={`w-full flex items-center gap-2.5 px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'incidents'
                      ? 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-slate-100'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <FileCheck2 className="w-4 h-4 shrink-0" />
                  <span className="truncate">Incidents &amp; Evidence Center</span>
                </button>
              </div>
            </div>

            <div>
              <div className="px-2.5 text-[11px] font-semibold text-slate-400 dark:text-slate-500 mb-2">
                Channel Profile Studios
              </div>
              <div className="space-y-1">
                <button
                  type="button"
                  onClick={() => openChannelStudio('webhook-http-sig')}
                  className={`w-full flex items-center justify-between px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'studios' &&
                    activeStudioFamily === 'webhook-http-sig'
                      ? 'bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <span className="flex items-center gap-2 truncate">
                    <Webhook className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">RFC 9421 Webhooks</span>
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">Phase 1</span>
                </button>

                <button
                  type="button"
                  onClick={() => openChannelStudio('bimi-mark')}
                  className={`w-full flex items-center justify-between px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'studios' &&
                    (activeStudioFamily === 'bimi-mark' ||
                      activeStudioFamily === 'smime')
                      ? 'bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <span className="flex items-center gap-2 truncate">
                    <Mail className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">BIMI / VMC &amp; S/MIME</span>
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">Phase 2</span>
                </button>

                <button
                  type="button"
                  onClick={() => openChannelStudio('document-signing')}
                  className={`w-full flex items-center justify-between px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'studios' &&
                    activeStudioFamily === 'document-signing'
                      ? 'bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <span className="flex items-center gap-2 truncate">
                    <FileSignature className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">Document Signing</span>
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">Phase 3</span>
                </button>

                <button
                  type="button"
                  onClick={() => openChannelStudio('stir-shaken')}
                  className={`w-full flex items-center justify-between px-2.5 py-2 text-xs font-medium rounded-lg transition-colors cursor-pointer ${
                    activeWorkspace === 'studios' &&
                    activeStudioFamily === 'stir-shaken'
                      ? 'bg-blue-50 dark:bg-blue-950/50 text-blue-700 dark:text-blue-300'
                      : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/50'
                  }`}
                >
                  <span className="flex items-center gap-2 truncate">
                    <PhoneCall className="w-3.5 h-3.5 shrink-0" />
                    <span className="truncate">Voice STIR/SHAKEN</span>
                  </span>
                  <span className="text-[11px] font-mono text-slate-400">Phase 4</span>
                </button>
              </div>
            </div>
          </div>

          <div className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs space-y-1.5">
            <div className="font-semibold text-slate-900 dark:text-slate-100">
              Vocabulary Qualification Rule
            </div>
            <p className="text-slate-600 dark:text-slate-400 leading-relaxed">
              This control plane never emits a generic &quot;Verified&quot; badge. Every result states exact profile coverage, authority basis, and external dependencies.
            </p>
          </div>
        </aside>

        {/* Main Viewport */}
        <main className="flex-1 p-6 lg:p-8 max-w-[1360px] w-full mx-auto">
          {activeWorkspace === 'overview' && (
            <div className="space-y-6">
              {/* Header */}
              <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
                <div>
                  <div className="text-xs text-slate-500 dark:text-slate-400 font-mono">
                    @tba/ui-communications-identity · Local demo API
                  </div>
                  <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-1">
                    Communications Identity &amp; Attestation Control Plane
                  </h1>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-3xl">
                    Profile-driven orchestration proving who or what requested a signature, which identity and authority were asserted, what components were covered, and what remains governed by external ecosystems.
                  </p>
                </div>

                <div className="flex items-center gap-2 shrink-0">
                  <button
                    type="button"
                    onClick={() => setActiveWorkspace('verification')}
                    className="px-3.5 py-2 text-xs font-medium text-slate-700 dark:text-slate-200 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 hover:bg-slate-50 rounded-lg transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                  >
                    Open Verification Workbench
                  </button>
                </div>
              </div>

              {/* 4-Column Metric Strip */}
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4">
                  <div className="text-xs text-slate-500">
                    Active Communication Identities
                  </div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mt-1 font-mono tabular-nums">
                    {activeCount} / {identities.length}
                  </div>
                  <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    Point-in-time versioned bindings across 5 channel profiles
                  </div>
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4">
                  <div className="text-xs text-slate-500">
                    24h Profile-Signed Assertions
                  </div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mt-1 font-mono tabular-nums">
                    {totalVolume24h.toLocaleString()}
                  </div>
                  <div className="text-xs text-slate-600 dark:text-slate-400 mt-1 font-mono tabular-nums">
                    p95 Voice: 2.1ms · HTTP: 3.8ms · S/MIME: 18.2ms
                  </div>
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4">
                  <div className="text-xs text-slate-500">
                    Unauthorized / Oracle Attempts Denied
                  </div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mt-1 font-mono tabular-nums">
                    {deniedCount} Denied
                  </div>
                  <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    0 fail-open signatures · OAuth/JWT key reuse blocked
                  </div>
                </div>

                <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4">
                  <div className="text-xs text-slate-500">
                    Content-Minimized Evidence Chain
                  </div>
                  <div className="text-2xl font-bold text-slate-900 dark:text-slate-100 mt-1 font-mono tabular-nums">
                    100.0% SHA-256
                  </div>
                  <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    Zero raw message bodies or private keys in evidence
                  </div>
                </div>
              </div>

              {/* Channel Profile Families & Conformance Matrix */}
              <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                <div className="p-5 border-b border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2">
                  <div>
                    <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                      Supported Channel Profile Families &amp; Native Trust Semantics
                    </h2>
                    <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                      Each profile preserves the native cryptographic and governance rules of its channel rather than inventing one universal badge.
                    </p>
                  </div>
                </div>

                <div className="divide-y divide-slate-200 dark:divide-slate-800">
                  {profiles.map((prof) => (
                    <div
                      key={prof.id}
                      className="p-5 flex flex-col lg:flex-row lg:items-start justify-between gap-4 hover:bg-slate-50/60 dark:hover:bg-slate-800/30 transition-colors"
                    >
                      <div className="space-y-2 max-w-3xl">
                        <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-slate-500">
                          <span className="font-semibold text-slate-900 dark:text-slate-100">
                            {prof.id}
                          </span>
                          <span>·</span>
                          <span>v{prof.version}</span>
                          <span>·</span>
                          <span>{prof.standardReference}</span>
                          <span>·</span>
                          <span>{prof.conformanceStatus}</span>
                        </div>
                        <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                          {prof.title}
                        </h3>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 text-xs pt-1">
                          <div>
                            <span className="font-semibold text-emerald-700 dark:text-emerald-400">
                              Qualified Positive Label:
                            </span>{' '}
                            <span className="font-mono text-slate-800 dark:text-slate-200">
                              {prof.qualifiedVocabulary.positiveLabel}
                            </span>
                            <p className="text-slate-600 dark:text-slate-400 mt-1">
                              {prof.whatItProves[0]}
                            </p>
                          </div>
                          <div>
                            <span className="font-semibold text-amber-700 dark:text-amber-400">
                              Explicit Non-Claim:
                            </span>{' '}
                            <span className="text-slate-600 dark:text-slate-400">
                              {prof.whatItDoesNotProve[0]}
                            </span>
                          </div>
                        </div>
                      </div>

                      <div className="flex items-center gap-2 shrink-0">
                        <button
                          type="button"
                          onClick={() => openChannelStudio(prof.family)}
                          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-blue-600 dark:text-blue-400 bg-blue-50 dark:bg-blue-950/50 hover:bg-blue-100 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                        >
                          Open Studio
                          <ArrowUpRight className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              {/* Communication Identity Inventory + Point-in-Time Binding Version Explorer */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
                <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
                  <div className="p-5 border-b border-slate-200 dark:border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
                    <div>
                      <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                        Communication Identities &amp; Verified Bindings
                      </h2>
                      <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                        Select any identity to inspect its point-in-time binding version history or rotate keys without mutating prior evidence.
                      </p>
                    </div>
                    <select
                      value={channelFilter}
                      onChange={(e) =>
                        setChannelFilter(e.target.value as 'ALL' | ChannelFamily)
                      }
                      className="px-3 py-1.5 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                    >
                      <option value="ALL">All Channels ({identities.length})</option>
                      <option value="webhook-http-sig">RFC 9421 Webhooks</option>
                      <option value="bimi-mark">BIMI / VMC Email</option>
                      <option value="smime">S/MIME 4.0 Email</option>
                      <option value="document-signing">Document Signing</option>
                      <option value="stir-shaken">STIR/SHAKEN Voice</option>
                    </select>
                  </div>

                  <div className="divide-y divide-slate-200 dark:divide-slate-800">
                    {filteredIdentities.map((id) => {
                      const isSelected = id.id === inspectedIdentity?.id;
                      return (
                        <div
                          key={id.id}
                          onClick={() => setSelectedIdentityForHistory(id.id)}
                          className={`p-4 transition-colors cursor-pointer ${
                            isSelected
                              ? 'bg-blue-50/50 dark:bg-blue-950/30'
                              : 'hover:bg-slate-50 dark:hover:bg-slate-800/40'
                          }`}
                        >
                          <div className="flex flex-wrap items-center justify-between gap-2 text-xs">
                            <div className="flex items-center gap-2 font-mono">
                              {id.status === 'ACTIVE' ? (
                                <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0" />
                              ) : id.status === 'PENDING_EXTERNAL_GOVERNANCE' ? (
                                <Clock className="w-3.5 h-3.5 text-amber-600 shrink-0" />
                              ) : (
                                <AlertTriangle className="w-3.5 h-3.5 text-rose-600 shrink-0" />
                              )}
                              <span className="font-semibold text-slate-900 dark:text-slate-100">
                                {id.id}
                              </span>
                              <span className="text-slate-400">·</span>
                              <span className="text-slate-600 dark:text-slate-400">
                                {id.channelFamily}
                              </span>
                              <span className="text-slate-400">·</span>
                              <span className="text-slate-500">
                                Binding v{id.bindingHistory[0]?.bindingVersion || 1}
                              </span>
                            </div>

                            <span className="font-mono text-slate-600 dark:text-slate-400">
                              {id.status}
                            </span>
                          </div>

                          <div className="text-sm font-semibold text-slate-900 dark:text-slate-100 font-mono mt-1 break-all">
                            {id.representedIdentifier}
                          </div>

                          <div className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                            Authority: {id.authorityEvidence}
                          </div>

                          <div className="flex flex-wrap items-center justify-between gap-2 mt-2.5 pt-2 border-t border-slate-200/70 dark:border-slate-800/70 text-xs font-mono text-slate-500">
                            <span>
                              Custody: {id.custodyClass} · 24h Vol:{' '}
                              {id.volume24h.toLocaleString()}
                            </span>
                            <span>p95: {id.p95LatencyMs}ms</span>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>

                {/* Right 5 Columns: Point-in-Time Binding Version Explorer & Lifecycle Actions */}
                <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
                  {inspectedIdentity && (
                    <>
                      <div className="pb-3 border-b border-slate-200 dark:border-slate-800">
                        <div className="flex items-center gap-1.5 text-xs text-slate-500">
                          <History className="w-3.5 h-3.5" />
                          <span>Point-in-Time Binding Resolution &amp; Lifecycle</span>
                        </div>
                        <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 font-mono mt-1 break-all">
                          {inspectedIdentity.representedIdentifier}
                        </h3>
                        <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                          External Governance: {inspectedIdentity.externalGovernanceStatus}
                        </p>
                      </div>

                      <div className="flex flex-wrap items-center gap-2">
                        <button
                          type="button"
                          onClick={() =>
                            handleIdentityLifecycleAction(
                              inspectedIdentity.id,
                              'ROTATE_KEY'
                            )
                          }
                          disabled={mutatingIdentityId === inspectedIdentity.id}
                          className="flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                        >
                          <RefreshCw className="w-3.5 h-3.5" />
                          Stage Key Rotation (+Binding Version)
                        </button>

                        {inspectedIdentity.status === 'ACTIVE' ? (
                          <button
                            type="button"
                            onClick={() =>
                              handleIdentityLifecycleAction(
                                inspectedIdentity.id,
                                'SUSPEND'
                              )
                            }
                            disabled={mutatingIdentityId === inspectedIdentity.id}
                            className="px-3 py-1.5 text-xs font-medium text-rose-700 dark:text-rose-300 bg-rose-50 dark:bg-rose-950/50 border border-rose-200 dark:border-rose-900 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                          >
                            Suspend Signing
                          </button>
                        ) : (
                          <button
                            type="button"
                            onClick={() =>
                              handleIdentityLifecycleAction(
                                inspectedIdentity.id,
                                'ACTIVATE'
                              )
                            }
                            disabled={mutatingIdentityId === inspectedIdentity.id}
                            className="px-3 py-1.5 text-xs font-medium text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/50 border border-emerald-200 dark:border-emerald-900 rounded-md transition-colors whitespace-nowrap shrink-0 cursor-pointer"
                          >
                            Reactivate Identity
                          </button>
                        )}
                      </div>

                      <div className="space-y-2 text-xs">
                        <div className="font-semibold text-slate-900 dark:text-slate-100">
                          Allowed Requesting Actors / Workloads:
                        </div>
                        <div className="font-mono text-slate-700 dark:text-slate-300 bg-slate-50 dark:bg-slate-950 p-2.5 rounded border border-slate-200 dark:border-slate-800">
                          {inspectedIdentity.allowedActors.join(' · ')}
                        </div>
                      </div>

                      <div className="space-y-2.5">
                        <div className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                          Immutable Binding Version History (Point-in-Time Resolvable)
                        </div>
                        <div className="space-y-2.5">
                          {inspectedIdentity.bindingHistory.map((ver) => (
                            <div
                              key={ver.bindingVersion}
                              className="p-3 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs space-y-1"
                            >
                              <div className="flex items-center justify-between font-mono">
                                <span className="font-semibold text-slate-900 dark:text-slate-100">
                                  Binding v{ver.bindingVersion} · Key: {ver.keyId}
                                </span>
                                <span className="text-slate-500">
                                  {ver.statusAtVersion}
                                </span>
                              </div>
                              <div className="font-mono text-[11px] text-slate-500">
                                Effective: {ver.effectiveFrom} →{' '}
                                {ver.effectiveUntil || 'PRESENT (Active Head)'}
                              </div>
                              <div className="text-slate-700 dark:text-slate-300 pt-1">
                                {ver.changeReason}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                    </>
                  )}
                </div>
              </div>
            </div>
          )}

          {activeWorkspace === 'studios' && (
            <ChannelStudiosView
              activeStudio={activeStudioFamily}
              onSelectStudio={setActiveStudioFamily}
              profiles={profiles}
              stirRecords={stirRecords}
              bimiAssessments={bimiAssessments}
              smimeRecords={smimeRecords}
              docCeremonies={docCeremonies}
              webhookProfiles={webhookProfiles}
              onRefreshData={fetchAllControlPlaneState}
            />
          )}

          {activeWorkspace === 'verification' && (
            <VerificationWorkbenchView identities={identities} />
          )}

          {activeWorkspace === 'custody' && (
            <CustodyAndSignersView
              identities={identities}
              signers={signers}
              onSignReceiptCreated={fetchAllControlPlaneState}
            />
          )}

          {activeWorkspace === 'incidents' && (
            <IncidentsAndEvidenceView
              incidents={incidents}
              receipts={receipts}
              onRefreshAll={fetchAllControlPlaneState}
            />
          )}
        </main>
      </div>

      <OnboardingWizardModal
        isOpen={wizardOpen}
        onClose={() => setWizardOpen(false)}
        onCreated={fetchAllControlPlaneState}
      />
    </div>
  );
}
