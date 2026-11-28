import React, { useState } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  ShieldCheck,
  Terminal,
  FileSignature,
  Mail,
  PhoneCall,
  Webhook,
  RefreshCw,
  Lock,
  ExternalLink,
  Copy,
  Check,
} from 'lucide-react';
import type {
  ChannelFamily,
  ChannelProfileSpec,
  StirShakenRecord,
  BimiDomainAssessment,
  SmimeIdentityRecord,
  DocumentCeremonyRecord,
  WebhookProfileRecord,
  VerificationStatus,
} from '../types/communications.ts';

interface ChannelStudiosViewProps {
  activeStudio: ChannelFamily;
  onSelectStudio: (family: ChannelFamily) => void;
  profiles: ChannelProfileSpec[];
  stirRecords: StirShakenRecord[];
  bimiAssessments: BimiDomainAssessment[];
  smimeRecords: SmimeIdentityRecord[];
  docCeremonies: DocumentCeremonyRecord[];
  webhookProfiles: WebhookProfileRecord[];
  onRefreshData: () => void;
}

const ALL_RFC9421_COMPONENTS = [
  '@method',
  '@target-uri',
  '@authority',
  'content-digest',
  'content-type',
  'x-tba-event-id',
  'x-tba-tenant-id',
];

export const ChannelStudiosView: React.FC<ChannelStudiosViewProps> = ({
  activeStudio,
  onSelectStudio,
  profiles,
  stirRecords,
  bimiAssessments,
  smimeRecords,
  docCeremonies,
  webhookProfiles,
  onRefreshData,
}) => {
  const currentProfile =
    profiles.find((p) => p.family === activeStudio) || profiles[0];

  // 1. Webhook Studio State (RFC 9421)
  const [whMethod, setWhMethod] = useState('POST');
  const [whTargetUri, setWhTargetUri] = useState(
    'https://partner.example.com/webhooks/settlement'
  );
  const [whAuthority, setWhAuthority] = useState('partner.example.com');
  const [whEventId, setWhEventId] = useState('evt_settlement_994810');
  const [whBodyJson, setWhBodyJson] = useState(
    JSON.stringify(
      {
        settlementId: 'stl_2026_11_09_8841',
        amount: '2450000.00',
        currency: 'USD',
        beneficiaryBic: 'MRMDUS33XXX',
      },
      null,
      2
    )
  );
  const [whComponents, setWhComponents] = useState<string[]>(
    webhookProfiles[0]?.coveredComponents || ALL_RFC9421_COMPONENTS
  );
  const [whProxyMode, setWhProxyMode] = useState<
    'NONE' | 'MUTATE_UNCOVERED_HEADER' | 'MUTATE_COVERED_AUTHORITY' | 'REPLAY_NONCE'
  >('NONE');
  const [whResult, setWhResult] = useState<{
    contentDigestHeader: string;
    signatureInputHeader: string;
    signatureHeader: string;
    canonicalSignatureBase: string;
    coveredComponents: string[];
    verificationOutcome: VerificationStatus;
    cryptographicallyValid: boolean;
    policyValid: boolean;
    qualifiedResultLabel: string;
    policyNote: string;
  } | null>(null);
  const [whLoading, setWhLoading] = useState(false);
  const [copiedHeader, setCopiedHeader] = useState(false);

  // 2. Email Sub-Mode (BIMI vs S/MIME)
  const [emailSubTab, setEmailSubTab] = useState<'bimi' | 'smime'>('bimi');
  const [bimiDomainInput, setBimiDomainInput] = useState('meridiantreasury.com');
  const [bimiDmarcInput, setBimiDmarcInput] = useState(
    'v=DMARC1; p=reject; pct=100; rua=mailto:dmarc@meridiantreasury.com;'
  );
  const [bimiTxtInput, setBimiTxtInput] = useState(
    'v=BIMI1; l=https://bimi.meridiantreasury.com/logo-tiny-ps.svg; a=https://bimi.meridiantreasury.com/meridian-vmc.pem;'
  );
  const [bimiSvgInput, setBimiSvgInput] = useState(
    `<svg xmlns="http://www.w3.org/2000/svg" version="1.2" baseProfile="tiny-ps" viewBox="0 0 100 100">\n  <title>Meridian Global Treasury Ltd.</title>\n  <rect width="100" height="100" fill="#0f172a"/>\n  <path d="M22 74V26h14l14 28 14-28h14v48H66V45L50 75 34 45v29H22z" fill="#38bdf8"/>\n</svg>`
  );
  const [bimiLintResult, setBimiLintResult] = useState<{
    protocolReady: boolean;
    qualifiedResultLabel: string;
    checks: {
      dmarcEnforced: boolean;
      bimiValidSyntax: boolean;
      svgStatus: string;
      svgReviewedDigest: string;
      mailboxProviderEligible: boolean;
      logoDisplayGuaranteed: boolean;
    };
    issues: string[];
    providerCaveat: string;
  } | null>(null);
  const [bimiLoading, setBimiLoading] = useState(false);

  // 3. Document Signing Ceremony State
  const [docStepUpToken, setDocStepUpToken] = useState(
    'WEBAUTHN_ASSERTION_FIDO2_SAM_99412A'
  );
  const [docConsentChecked, setDocConsentChecked] = useState(true);
  const [docMutateTest, setDocMutateTest] = useState(false);
  const [docCeremonyResult, setDocCeremonyResult] = useState<{
    status: VerificationStatus;
    qualifiedResultLabel: string;
    verificationReport: {
      immutableDocumentDigest: string;
      verifiedCandidateDigest: string;
      digestMatchesPreview: boolean;
      stepUpVerifiedWith: string;
      rfc3161Timestamp: string;
      jurisdictionCaveat: string;
    };
  } | null>(null);
  const [docLoading, setDocLoading] = useState(false);

  // 4. Voice STIR/SHAKEN Test Call State
  const [voiceOrigTn, setVoiceOrigTn] = useState('+12125550142');
  const [voiceDestTn, setVoiceDestTn] = useState('+12025550188');
  const [voiceAttestLevel, setVoiceAttestLevel] = useState<'A' | 'B' | 'C'>('A');
  const [voiceTransitStrip, setVoiceTransitStrip] = useState(false);
  const [voiceResult, setVoiceResult] = useState<{
    verificationStatus: VerificationStatus;
    qualifiedResultLabel: string;
    passportHeader: Record<string, unknown>;
    passportPayload: Record<string, unknown>;
    sipIdentityHeader: string;
    attestationMeaning: string;
    separateRobocallSignal: string;
    whatItDoesNotProve: string[];
  } | null>(null);
  const [voiceLoading, setVoiceLoading] = useState(false);

  const toggleWhComponent = (comp: string) => {
    setWhComponents((prev) =>
      prev.includes(comp) ? prev.filter((c) => c !== comp) : [...prev, comp]
    );
  };

  const runWebhookSimulation = async () => {
    setWhLoading(true);
    try {
      const res = await fetch('/api/v1/webhook-signing/simulate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          method: whMethod,
          targetUri: whTargetUri,
          authority: whAuthority,
          bodyJson: whBodyJson,
          coveredComponents: whComponents,
          eventIdHeader: whEventId,
          nonce: `nonce-${Date.now()}`,
          proxyMutationMode: whProxyMode,
        }),
      });
      const data = await res.json();
      setWhResult(data);
    } finally {
      setWhLoading(false);
    }
  };

  const runBimiLint = async () => {
    setBimiLoading(true);
    try {
      const res = await fetch('/api/v1/email-identities/bimi-lint', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          domain: bimiDomainInput,
          dmarcRecord: bimiDmarcInput,
          bimiTxtRecord: bimiTxtInput,
          svgMarkup: bimiSvgInput,
        }),
      });
      const data = await res.json();
      setBimiLintResult(data);
    } finally {
      setBimiLoading(false);
    }
  };

  const runDocumentCeremony = async () => {
    setDocLoading(true);
    try {
      const res = await fetch('/api/v1/document-signing/ceremony', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ceremonyId: docCeremonies[0]?.id || 'doc-cer-01',
          actorEmail: 'a.solberg@nordicpension.no',
          stepUpToken: docStepUpToken,
          explicitConsentChecked: docConsentChecked,
          simulatePostSignMutation: docMutateTest,
        }),
      });
      const data = await res.json();
      if (res.ok) {
        setDocCeremonyResult(data);
        onRefreshData();
      }
    } finally {
      setDocLoading(false);
    }
  };

  const runStirShakenTestCall = async () => {
    setVoiceLoading(true);
    try {
      const res = await fetch('/api/v1/telephone-identities/test-call', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          recordId: stirRecords[0]?.id || 'stir-nyc-01',
          origTn: voiceOrigTn,
          destTn: voiceDestTn,
          attestationOverride: voiceAttestLevel,
          simulateTransitStrip: voiceTransitStrip,
        }),
      });
      const data = await res.json();
      setVoiceResult(data);
    } finally {
      setVoiceLoading(false);
    }
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    setCopiedHeader(true);
    setTimeout(() => setCopiedHeader(false), 1800);
  };

  return (
    <div className="space-y-6">
      {/* Channel Family Selector Bar (Interactive Functional Buttons) */}
      <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4 pb-5 border-b border-slate-200 dark:border-slate-800">
        <div>
          <div className="text-xs text-slate-500 dark:text-slate-400">
            Channel Profile Studios · Profile-Native Canonical Construction & Verification
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-1">
            {currentProfile?.title}
          </h1>
          <div className="flex flex-wrap items-center gap-2 text-xs text-slate-600 dark:text-slate-400 mt-1.5 font-mono">
            <span>{currentProfile?.id}</span>
            <span aria-hidden="true">·</span>
            <span>v{currentProfile?.version}</span>
            <span aria-hidden="true">·</span>
            <span>{currentProfile?.standardReference}</span>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-1 p-1 bg-slate-200/80 dark:bg-slate-800 rounded-lg">
          <button
            type="button"
            onClick={() => onSelectStudio('webhook-http-sig')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
              activeStudio === 'webhook-http-sig'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Webhook className="w-3.5 h-3.5" />
            RFC 9421 Webhooks
          </button>
          <button
            type="button"
            onClick={() => {
              onSelectStudio('bimi-mark');
              setEmailSubTab('bimi');
            }}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
              activeStudio === 'bimi-mark' || activeStudio === 'smime'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <Mail className="w-3.5 h-3.5" />
            Brand & Email (BIMI / S/MIME)
          </button>
          <button
            type="button"
            onClick={() => onSelectStudio('document-signing')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
              activeStudio === 'document-signing'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <FileSignature className="w-3.5 h-3.5" />
            Document Signing
          </button>
          <button
            type="button"
            onClick={() => onSelectStudio('stir-shaken')}
            className={`flex items-center gap-1.5 px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
              activeStudio === 'stir-shaken'
                ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                : 'text-slate-600 dark:text-slate-400 hover:text-slate-900 dark:hover:text-slate-200'
            }`}
          >
            <PhoneCall className="w-3.5 h-3.5" />
            Voice (STIR/SHAKEN)
          </button>
        </div>
      </div>

      {/* Profile Trust Boundary & Explicit Non-Claims Banner */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs font-semibold text-emerald-700 dark:text-emerald-400">
            <CheckCircle2 className="w-4 h-4 shrink-0" />
            <span>What This Channel Profile Establishes</span>
          </div>
          <ul className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
            {currentProfile?.whatItProves.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-slate-400 select-none">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
        <div className="space-y-2 lg:border-l lg:border-slate-200 dark:lg:border-slate-800 lg:pl-5">
          <div className="flex items-center gap-2 text-xs font-semibold text-amber-700 dark:text-amber-400">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>What This Profile Does NOT Establish (Explicit Non-Claims)</span>
          </div>
          <ul className="space-y-1.5 text-xs text-slate-700 dark:text-slate-300 leading-relaxed">
            {currentProfile?.whatItDoesNotProve.map((item, idx) => (
              <li key={idx} className="flex items-start gap-2">
                <span className="text-slate-400 select-none">•</span>
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* STUDIO 1: WEBHOOK & HTTP MESSAGE SIGNATURE STUDIO (RFC 9421) */}
      {activeStudio === 'webhook-http-sig' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-5">
            <div>
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                RFC 9421 Covered-Component & Proxy Transformation Builder
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                Configure covered HTTP components, test canonical signature base construction, and simulate reverse-proxy transformations or replay attacks.
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  HTTP Method
                </label>
                <select
                  value={whMethod}
                  onChange={(e) => setWhMethod(e.target.value)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md font-mono text-slate-900 dark:text-slate-100"
                >
                  <option value="POST">POST</option>
                  <option value="PUT">PUT</option>
                  <option value="DELETE">DELETE</option>
                </select>
              </div>
              <div className="sm:col-span-2">
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  @authority (Host)
                </label>
                <input
                  type="text"
                  value={whAuthority}
                  onChange={(e) => setWhAuthority(e.target.value)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md font-mono text-slate-900 dark:text-slate-100"
                />
              </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  @target-uri
                </label>
                <input
                  type="text"
                  value={whTargetUri}
                  onChange={(e) => setWhTargetUri(e.target.value)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md font-mono text-slate-900 dark:text-slate-100"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  x-tba-event-id (Idempotency Key)
                </label>
                <input
                  type="text"
                  value={whEventId}
                  onChange={(e) => setWhEventId(e.target.value)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md font-mono text-slate-900 dark:text-slate-100"
                />
              </div>
            </div>

            <div>
              <div className="flex items-center justify-between mb-2">
                <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                  Covered Components in @signature-params
                </label>
                <span className="text-xs text-slate-500 font-mono">
                  {whComponents.length} of {ALL_RFC9421_COMPONENTS.length} selected
                </span>
              </div>
              <div className="flex flex-wrap gap-2">
                {ALL_RFC9421_COMPONENTS.map((comp) => {
                  const selected = whComponents.includes(comp);
                  return (
                    <button
                      key={comp}
                      type="button"
                      onClick={() => toggleWhComponent(comp)}
                      className={`px-2.5 py-1.5 text-xs font-mono rounded-md border transition-colors whitespace-nowrap shrink-0 ${
                        selected
                          ? 'bg-slate-900 dark:bg-blue-600 text-white border-slate-900 dark:border-blue-500'
                          : 'bg-slate-50 dark:bg-slate-950 text-slate-600 dark:text-slate-400 border-slate-300 dark:border-slate-700 hover:text-slate-900'
                      }`}
                    >
                      {selected ? '✓ ' : '+ '}
                      {comp}
                    </button>
                  );
                })}
              </div>
              {(!whComponents.includes('content-digest') ||
                !whComponents.includes('@target-uri')) && (
                <p className="text-xs text-amber-700 dark:text-amber-400 mt-2">
                  Policy Warning: Omitting &quot;content-digest&quot; or &quot;@target-uri&quot; produces a signature that is mathematically valid over the remaining headers but rejected by TBA profile policy.
                </p>
              )}
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                HTTP JSON Payload (Hashed via RFC 9530 Content-Digest)
              </label>
              <textarea
                rows={4}
                value={whBodyJson}
                onChange={(e) => setWhBodyJson(e.target.value)}
                className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md font-mono text-slate-900 dark:text-slate-100"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Intermediary / Replay Simulation Mode
              </label>
              <select
                value={whProxyMode}
                onChange={(e) =>
                  setWhProxyMode(
                    e.target.value as
                      | 'NONE'
                      | 'MUTATE_UNCOVERED_HEADER'
                      | 'MUTATE_COVERED_AUTHORITY'
                      | 'REPLAY_NONCE'
                  )
                }
                className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md text-slate-900 dark:text-slate-100"
              >
                <option value="NONE">
                  Nominal Direct Delivery (Preserves Covered Components & Fresh Nonce)
                </option>
                <option value="MUTATE_UNCOVERED_HEADER">
                  Proxy Appends Uncovered X-Envoy Header (Cryptographically & Policy Valid)
                </option>
                <option value="MUTATE_COVERED_AUTHORITY">
                  Ingress Proxy Rewrites Host/@authority Header (Canonical Mismatch Failure)
                </option>
                <option value="REPLAY_NONCE">
                  Attacker Replays Previously Consumed Nonce Within 300s Window (Replay Rejected)
                </option>
              </select>
            </div>

            <div className="flex items-center justify-between pt-2">
              <div className="text-xs text-slate-500 font-mono">
                Active Key: key-rfc9421-ed25519-09a · Overlap: key-rfc9421-ed25519-10next
              </div>
              <button
                type="button"
                onClick={runWebhookSimulation}
                disabled={whLoading}
                className="flex items-center gap-2 px-4 py-2 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors whitespace-nowrap shrink-0 cursor-pointer"
              >
                <Terminal className="w-3.5 h-3.5" />
                {whLoading ? 'Computing RFC 9421 Base...' : 'Build & Verify HTTP Signature'}
              </button>
            </div>
          </div>

          <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                Canonical Signature Base & Verification Output
              </h2>
              {whResult && (
                <button
                  type="button"
                  onClick={() =>
                    copyToClipboard(
                      `${whResult.contentDigestHeader}\n${whResult.signatureInputHeader}\n${whResult.signatureHeader}`
                    )
                  }
                  className="flex items-center gap-1.5 px-2.5 py-1 text-xs font-medium text-slate-700 dark:text-slate-300 bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 rounded-md whitespace-nowrap shrink-0"
                >
                  {copiedHeader ? (
                    <>
                      <Check className="w-3.5 h-3.5 text-emerald-600" />
                      Copied Headers
                    </>
                  ) : (
                    <>
                      <Copy className="w-3.5 h-3.5" />
                      Copy HTTP Headers
                    </>
                  )}
                </button>
              )}
            </div>

            {!whResult ? (
              <div className="py-12 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-lg">
                <p className="text-xs text-slate-500 dark:text-slate-400">
                  Click &quot;Build &amp; Verify HTTP Signature&quot; to construct the RFC 9421 canonical signature base and test verifier policy enforcement.
                </p>
              </div>
            ) : (
              <div className="space-y-4">
                <div className="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950">
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-2">
                      {whResult.verificationOutcome === 'valid' ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                      ) : whResult.verificationOutcome === 'stale' ? (
                        <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0" />
                      )}
                      <span className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                        {whResult.qualifiedResultLabel}
                      </span>
                    </div>
                    <div className="text-xs font-mono text-slate-500">
                      Crypto: {whResult.cryptographicallyValid ? 'VALID' : 'INVALID'} · Policy:{' '}
                      {whResult.policyValid ? 'VALID' : 'REJECTED'}
                    </div>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-2 leading-relaxed">
                    {whResult.policyNote}
                  </p>
                </div>

                <div>
                  <div className="text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                    Constructed RFC 9421 Canonical Signature Base (Exact Bytes Signed)
                  </div>
                  <pre className="p-3 text-xs font-mono bg-slate-900 text-slate-100 rounded-lg overflow-x-auto leading-relaxed">
                    {whResult.canonicalSignatureBase}
                  </pre>
                </div>

                <div>
                  <div className="text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
                    Attached Wire Headers (RFC 9530 + RFC 9421)
                  </div>
                  <pre className="p-3 text-xs font-mono bg-slate-900 text-emerald-300 rounded-lg overflow-x-auto leading-relaxed">
                    {whResult.contentDigestHeader}
                    {'\n'}
                    {whResult.signatureInputHeader}
                    {'\n'}
                    {whResult.signatureHeader}
                  </pre>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* STUDIO 2: BRAND & EMAIL IDENTITY CENTER (BIMI VMC/CMC + S/MIME 4.0) */}
      {(activeStudio === 'bimi-mark' || activeStudio === 'smime') && (
        <div className="space-y-6">
          {/* Sub-workspace switch separating BIMI Readiness from S/MIME 4.0 Lifecycle */}
          <div className="flex items-center justify-between bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-4">
            <div>
              <h2 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Email Channel Separation: BIMI Brand Indicators vs. S/MIME 4.0 Cryptographic Messaging
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                BIMI/VMC assertions prove domain DMARC enforcement and trademarked logo binding; S/MIME proves covered MIME entity integrity and mailbox identity.
              </p>
            </div>
            <div className="flex items-center gap-1 p-1 bg-slate-100 dark:bg-slate-800 rounded-lg shrink-0">
              <button
                type="button"
                onClick={() => {
                  setEmailSubTab('bimi');
                  onSelectStudio('bimi-mark');
                }}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
                  emailSubTab === 'bimi'
                    ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                    : 'text-slate-600 dark:text-slate-400'
                }`}
              >
                BIMI &amp; VMC/CMC Readiness
              </button>
              <button
                type="button"
                onClick={() => {
                  setEmailSubTab('smime');
                  onSelectStudio('smime');
                }}
                className={`px-3 py-1.5 text-xs font-medium rounded-md transition-colors whitespace-nowrap shrink-0 ${
                  emailSubTab === 'smime'
                    ? 'bg-white dark:bg-slate-900 text-slate-900 dark:text-slate-100 shadow-xs'
                    : 'text-slate-600 dark:text-slate-400'
                }`}
              >
                S/MIME 4.0 Lifecycle &amp; Coverage
              </button>
            </div>
          </div>

          {emailSubTab === 'bimi' ? (
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {/* Left: Domain Assessment Matrix (Separating Protocol Readiness from Provider Display) */}
              <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-5">
                <div>
                  <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                    BIMI 6-State Protocol Readiness vs. External Mailbox-Provider Observations
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    Protocol readiness does NOT guarantee inbox placement or logo display. Provider display observations are tracked separately.
                  </p>
                </div>

                {bimiAssessments.map((item) => (
                  <div
                    key={item.id}
                    className="border border-slate-200 dark:border-slate-800 rounded-lg p-4 space-y-4"
                  >
                    <div className="flex flex-wrap items-center justify-between gap-2 pb-3 border-b border-slate-200 dark:border-slate-800">
                      <div>
                        <span className="text-sm font-semibold text-slate-900 dark:text-slate-100 font-mono">
                          {item.domain}
                        </span>
                        <span className="text-xs text-slate-500 ml-2 font-mono">
                          selector: {item.selector} · {item.markCertificateType}
                        </span>
                      </div>
                      <div className="flex items-center gap-1.5 text-xs font-medium">
                        {item.mailboxProviderEligible ? (
                          <>
                            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                            <span className="text-emerald-700 dark:text-emerald-400">
                              BIMI Protocol Ready
                            </span>
                          </>
                        ) : (
                          <>
                            <XCircle className="w-4 h-4 text-rose-600" />
                            <span className="text-rose-700 dark:text-rose-400">
                              Protocol Blocker Active
                            </span>
                          </>
                        )}
                      </div>
                    </div>

                    {/* The 6 Distinct States Required by Section 9 */}
                    <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 text-xs">
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">1. DNS TXT Record</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                          {item.dnsRecordValid ? 'Valid v=BIMI1' : 'Invalid'}
                        </div>
                      </div>
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">2. DMARC Posture</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5 font-mono">
                          {item.dmarcPolicy}
                        </div>
                      </div>
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">3. SVG Tiny P/S</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5 font-mono">
                          {item.svgTinyPsStatus}
                        </div>
                      </div>
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">4. Mark Certificate</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                          {item.markCertificateValidAndBound ? 'Valid & Bound' : 'Unbound'}
                        </div>
                      </div>
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">5. Provider Eligible</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                          {item.mailboxProviderEligible ? 'Eligible' : 'Not Eligible'}
                        </div>
                      </div>
                      <div className="p-2.5 bg-slate-50 dark:bg-slate-950 rounded border border-slate-200 dark:border-slate-800">
                        <div className="text-slate-500">6. Logo Displayed</div>
                        <div className="font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                          Provider-Specific (See Below)
                        </div>
                      </div>
                    </div>

                    {item.blockers.length > 0 && (
                      <div className="p-3 bg-rose-50/70 dark:bg-rose-950/30 border border-rose-200 dark:border-rose-900 rounded-md space-y-1">
                        <div className="text-xs font-semibold text-rose-800 dark:text-rose-300">
                          Exact Readiness Blockers:
                        </div>
                        {item.blockers.map((b, i) => (
                          <div key={i} className="text-xs text-rose-700 dark:text-rose-300">
                            • {b}
                          </div>
                        ))}
                      </div>
                    )}

                    <div>
                      <div className="text-xs font-medium text-slate-700 dark:text-slate-300 mb-2">
                        External Mailbox Provider Observations (Separated from Protocol Readiness)
                      </div>
                      <div className="divide-y divide-slate-200 dark:divide-slate-800 border border-slate-200 dark:border-slate-800 rounded-md">
                        {item.providerDisplayObservations.map((obs, idx) => (
                          <div
                            key={idx}
                            className="p-2.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2 text-xs"
                          >
                            <div>
                              <span className="font-medium text-slate-900 dark:text-slate-100">
                                {obs.provider}
                              </span>
                              <p className="text-slate-500 dark:text-slate-400 mt-0.5">{obs.note}</p>
                            </div>
                            <div className="font-mono text-right shrink-0">
                              <span className="text-slate-600 dark:text-slate-400">
                                Eligible: {obs.protocolEligible ? 'Yes' : 'No'} · Displayed:{' '}
                                {obs.observedLogoDisplayed ? 'Observed' : 'Not Displayed'}
                              </span>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                ))}
              </div>

              {/* Right: Untrusted SVG Tiny P/S Linter & Isolated Sandbox */}
              <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
                <div>
                  <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                    BIMI DNS &amp; Untrusted SVG Tiny P/S Sanitizer
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    Uploaded SVGs are treated as untrusted active content. Validate against SVG Tiny P/S, reject scripts or external references, and compute a reviewed SHA-256 digest.
                  </p>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    DMARC TXT Policy Input
                  </label>
                  <input
                    type="text"
                    value={bimiDmarcInput}
                    onChange={(e) => setBimiDmarcInput(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>

                <div>
                  <div className="flex items-center justify-between mb-1">
                    <label className="text-xs font-medium text-slate-700 dark:text-slate-300">
                      Candidate SVG Tiny P/S Source
                    </label>
                    <button
                      type="button"
                      onClick={() =>
                        setBimiSvgInput(
                          `<svg xmlns="http://www.w3.org/2000/svg" baseProfile="tiny-ps" viewBox="0 0 100 100">\n  <script>alert("xss")</script>\n  <image xlink:href="https://evil.example.com/pixel.png"/>\n</svg>`
                        )
                      }
                      className="text-xs text-blue-600 dark:text-blue-400 hover:underline"
                    >
                      Load Malicious SVG Test Vector
                    </button>
                  </div>
                  <textarea
                    rows={5}
                    value={bimiSvgInput}
                    onChange={(e) => setBimiSvgInput(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>

                <button
                  type="button"
                  onClick={runBimiLint}
                  disabled={bimiLoading}
                  className="w-full py-2 px-4 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors cursor-pointer"
                >
                  {bimiLoading ? 'Linting BIMI & Sanitizing SVG...' : 'Validate BIMI Readiness & SVG Tiny P/S'}
                </button>

                {bimiLintResult && (
                  <div className="p-4 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 space-y-3">
                    <div className="flex items-center gap-2">
                      {bimiLintResult.protocolReady ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                      )}
                      <span className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                        {bimiLintResult.qualifiedResultLabel}
                      </span>
                    </div>
                    <div className="text-xs font-mono text-slate-600 dark:text-slate-400 break-all">
                      Reviewed SVG Digest: {bimiLintResult.checks.svgReviewedDigest}
                    </div>
                    {bimiLintResult.issues.length > 0 && (
                      <ul className="space-y-1 text-xs text-rose-700 dark:text-rose-400">
                        {bimiLintResult.issues.map((iss, i) => (
                          <li key={i}>• {iss}</li>
                        ))}
                      </ul>
                    )}
                    <p className="text-xs text-slate-500">{bimiLintResult.providerCaveat}</p>
                  </div>
                )}
              </div>
            </div>
          ) : (
            /* S/MIME 4.0 Lifecycle & Covered Header View */
            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
              {smimeRecords.map((rec) => (
                <div
                  key={rec.id}
                  className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4"
                >
                  <div className="flex items-start justify-between gap-2 pb-3 border-b border-slate-200 dark:border-slate-800">
                    <div>
                      <div className="text-xs text-slate-500">
                        Signer Classification: {rec.signerClassification}
                      </div>
                      <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100 font-mono mt-0.5">
                        {rec.mailbox}
                      </h3>
                    </div>
                    <span className="text-xs font-mono text-emerald-700 dark:text-emerald-400">
                      Separate Keys Enforced
                    </span>
                  </div>

                  <div className="space-y-2 text-xs">
                    <div className="flex justify-between py-1 border-b border-slate-100 dark:border-slate-800/60">
                      <span className="text-slate-500">Signing Certificate (Never Escrowed):</span>
                      <span className="font-mono text-slate-900 dark:text-slate-100">
                        {rec.signingCertSerial}
                      </span>
                    </div>
                    <div className="flex justify-between py-1 border-b border-slate-100 dark:border-slate-800/60">
                      <span className="text-slate-500">Encryption Certificate:</span>
                      <span className="font-mono text-slate-900 dark:text-slate-100">
                        {rec.encryptionCertSerial}
                      </span>
                    </div>
                    <div className="flex justify-between py-1">
                      <span className="text-slate-500">Supported S/MIME 4.0 Modes:</span>
                      <span className="font-mono text-slate-900 dark:text-slate-100">
                        {rec.supportedModes.join(' · ')}
                      </span>
                    </div>
                  </div>

                  <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-2">
                    <div className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                      Covered MIME Headers (RFC 8551 Wrapped Header Protection):
                    </div>
                    <div className="text-xs font-mono text-slate-700 dark:text-slate-300">
                      {rec.coveredHeaders.join(' · ')}
                    </div>
                    <div className="text-xs font-semibold text-amber-700 dark:text-amber-400 pt-1">
                      Uncovered Visible Mail-Client Field Limitations:
                    </div>
                    <ul className="space-y-1 text-xs text-slate-600 dark:text-slate-400">
                      {rec.uncoveredVisibleFieldsWarning.map((w, idx) => (
                        <li key={idx}>• {w}</li>
                      ))}
                    </ul>
                  </div>

                  <div>
                    <div className="text-xs font-medium text-slate-700 dark:text-slate-300 mb-2">
                      Client Interoperability Matrix
                    </div>
                    <div className="divide-y divide-slate-200 dark:divide-slate-800 border border-slate-200 dark:border-slate-800 rounded-md">
                      {rec.clientInteroperability.map((cli, idx) => (
                        <div key={idx} className="p-2.5 text-xs flex items-center justify-between gap-3">
                          <div>
                            <div className="font-medium text-slate-900 dark:text-slate-100">
                              {cli.client}
                            </div>
                            <div className="text-slate-500">{cli.notes}</div>
                          </div>
                          <div className="font-mono text-right shrink-0">
                            CMS: {cli.cmsParsePass ? 'Pass' : 'Fail'} · RFC8551:{' '}
                            {cli.headerProtectionRfc8551 ? 'Full' : 'Partial'}
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {/* STUDIO 3: DOCUMENT SIGNING STUDIO (PAdES-B-LTA) */}
      {activeStudio === 'document-signing' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {docCeremonies.map((cer) => (
            <React.Fragment key={cer.id}>
              <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-5">
                <div className="pb-3 border-b border-slate-200 dark:border-slate-800">
                  <div className="text-xs text-slate-500 font-mono">
                    {cer.profileSpec} · Immutable Bytes: {cer.immutableDocumentBytesLen.toLocaleString()} bytes
                  </div>
                  <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100 mt-1">
                    {cer.documentTitle}
                  </h2>
                </div>

                {/* Human-Readable Document Preview Explicitly Bound to Signed SHA-256 Digest */}
                <div className="p-4 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-3">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-semibold text-slate-900 dark:text-slate-100">
                      Human-Readable Preview Bound to Exact Signed Digest
                    </span>
                    <span className="font-mono text-slate-500">
                      SHA-256: {cer.documentDigestSha256.slice(0, 20)}...
                    </span>
                  </div>
                  <div className="p-3 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded text-xs text-slate-700 dark:text-slate-300 leading-relaxed font-sans space-y-2">
                    <p className="font-semibold">
                      SCHEDULE B — INSTITUTIONAL DIGITAL ASSET CUSTODY &amp; SEGREGATION MANDATE
                    </p>
                    <p>
                      1. Custody Segregation: Custodian shall maintain all Client settlement assets in dedicated, bankruptcy-remote omnibus or segregated accounts verified under EU eIDAS Regulation (EU) No 910/2014 and applicable UK Financial Conduct Authority rules.
                    </p>
                    <p>
                      2. Immutable Correction Rule: Any modification or amendment to this Schedule requires a new versioned PDF byte stream and a fresh multi-party cryptographic signing ceremony. In-place byte mutation invalidates the PAdES-B-LTA seal.
                    </p>
                  </div>
                  <div className="text-xs font-mono text-slate-600 dark:text-slate-400 break-all">
                    Full Immutable Byte Digest: SHA256:{cer.documentDigestSha256}
                  </div>
                </div>

                {/* Multi-Signer Ceremony Order */}
                <div>
                  <h3 className="text-xs font-semibold text-slate-900 dark:text-slate-100 mb-2">
                    Multi-Signer Order, Role Authority &amp; Long-Term Validation (LTV) State
                  </h3>
                  <div className="divide-y divide-slate-200 dark:divide-slate-800 border border-slate-200 dark:border-slate-800 rounded-lg">
                    {cer.multiSignerOrder.map((step) => (
                      <div key={step.step} className="p-3 flex items-center justify-between gap-4 text-xs">
                        <div>
                          <div className="font-medium text-slate-900 dark:text-slate-100">
                            Step {step.step}: {step.role}
                          </div>
                          <div className="text-slate-500">{step.actor}</div>
                          {step.signatureDigest && (
                            <div className="font-mono text-slate-400 mt-0.5">
                              Seal: {step.signatureDigest.slice(0, 36)}...
                            </div>
                          )}
                        </div>
                        <div className="text-right font-mono shrink-0">
                          <div
                            className={
                              step.status === 'SIGNED_SEALED'
                                ? 'text-emerald-700 dark:text-emerald-400 font-semibold'
                                : 'text-amber-700 dark:text-amber-400 font-semibold'
                            }
                          >
                            {step.status}
                          </div>
                          {step.signedAt && <div className="text-slate-400">{step.signedAt}</div>}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              </div>

              {/* Right: Signer Ceremony Execution & Tamper Detection Test */}
              <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
                <div>
                  <h3 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                    Signer Ceremony Confirmation &amp; Byte-Digest Binding
                  </h3>
                  <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                    Signing confirmation names the exact signer identity, organizational role, document digest, and jurisdictional caveat.
                  </p>
                </div>

                <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs space-y-1.5">
                  <div>
                    <span className="text-slate-500">Signer Identity:</span>{' '}
                    <span className="font-medium text-slate-900 dark:text-slate-100">
                      {cer.signerName}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Organizational Role:</span>{' '}
                    <span className="font-medium text-slate-900 dark:text-slate-100">
                      {cer.signerRole}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Authority Basis:</span>{' '}
                    <span className="font-medium text-slate-900 dark:text-slate-100">
                      {cer.organizationAuthority}
                    </span>
                  </div>
                  <div>
                    <span className="text-slate-500">Qualified TSA:</span>{' '}
                    <span className="font-mono text-slate-800 dark:text-slate-200">
                      {cer.tsaAuthority}
                    </span>
                  </div>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Step-Up Authentication &amp; Remote QTSP SAM Token
                  </label>
                  <input
                    type="text"
                    value={docStepUpToken}
                    onChange={(e) => setDocStepUpToken(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>

                <label className="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                  <input
                    type="checkbox"
                    checked={docConsentChecked}
                    onChange={(e) => setDocConsentChecked(e.target.checked)}
                    className="mt-0.5 rounded border-slate-300"
                  />
                  <span>{cer.declaredIntent}</span>
                </label>

                <label className="flex items-start gap-2.5 text-xs text-amber-800 dark:text-amber-400 cursor-pointer pt-1">
                  <input
                    type="checkbox"
                    checked={docMutateTest}
                    onChange={(e) => setDocMutateTest(e.target.checked)}
                    className="mt-0.5 rounded border-slate-300"
                  />
                  <span>
                    Simulate 1-byte post-preview PDF mutation (verifies ceremony aborts if displayed bytes differ from signed digest)
                  </span>
                </label>

                <button
                  type="button"
                  onClick={runDocumentCeremony}
                  disabled={docLoading || !docConsentChecked}
                  className="w-full py-2.5 px-4 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg transition-colors cursor-pointer"
                >
                  {docLoading
                    ? 'Invoking Remote QTSP SAM...'
                    : 'Execute Step-Up Ceremony & Seal Document Digest'}
                </button>

                <div className="p-3 rounded-md border border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
                  <strong className="text-slate-900 dark:text-slate-200">
                    Jurisdictional &amp; Legal Scope Notice:
                  </strong>{' '}
                  {cer.jurisdictionCaveat}
                </div>

                {docCeremonyResult && (
                  <div className="p-4 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 space-y-2 text-xs">
                    <div className="flex items-center gap-2 font-semibold text-slate-900 dark:text-slate-100">
                      {docCeremonyResult.status === 'valid' ? (
                        <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                      ) : (
                        <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                      )}
                      <span>{docCeremonyResult.qualifiedResultLabel}</span>
                    </div>
                    <div className="font-mono text-slate-600 dark:text-slate-400 break-all">
                      Candidate Digest: {docCeremonyResult.verificationReport.verifiedCandidateDigest}
                    </div>
                    <div className="font-mono text-slate-500">
                      RFC 3161 Timestamp: {docCeremonyResult.verificationReport.rfc3161Timestamp}
                    </div>
                  </div>
                )}
              </div>
            </React.Fragment>
          ))}
        </div>
      )}

      {/* STUDIO 4: VOICE IDENTITY CENTER (STIR/SHAKEN) */}
      {activeStudio === 'stir-shaken' && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-5">
            <div>
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                Telephone Number Inventory, STI-CA Certificates &amp; Governance
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-1">
                SHAKEN program roles and STI-CA certificates are scoped by national governance authority (US-FCC-STI-GA vs. CA-CRTC-CSTGA).
              </p>
            </div>

            <div className="space-y-3">
              {stirRecords.map((rec) => (
                <div
                  key={rec.id}
                  className="p-4 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-950 space-y-2 text-xs"
                >
                  <div className="flex items-center justify-between">
                    <span className="font-semibold text-slate-900 dark:text-slate-100 font-mono">
                      {rec.tnRange}
                    </span>
                    <span className="font-mono text-slate-600 dark:text-slate-400">
                      {rec.jurisdiction} · Default Attest {rec.defaultAttestationLevel}
                    </span>
                  </div>
                  <div className="text-slate-600 dark:text-slate-400 font-mono">
                    {rec.ocnSpid} · Active Kid: {rec.activePassportKid} (Standby: {rec.rolloverStandbyKid})
                  </div>
                  <div className="text-slate-600 dark:text-slate-400">
                    STI-CA Repository: <span className="font-mono">{rec.certificateUrl}</span>
                  </div>
                  <div className="pt-1 border-t border-slate-200 dark:border-slate-800 text-slate-500">
                    {rec.robocallAnalyticsScore}
                  </div>
                </div>
              ))}
            </div>

            <div className="pt-2 border-t border-slate-200 dark:border-slate-800 space-y-3">
              <h3 className="text-sm font-semibold text-slate-900 dark:text-slate-100">
                Test SIP INVITE &amp; SHAKEN PASSporT Assertion
              </h3>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Origination TN (orig.tn)
                  </label>
                  <input
                    type="text"
                    value={voiceOrigTn}
                    onChange={(e) => setVoiceOrigTn(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Destination TN (dest.tn)
                  </label>
                  <input
                    type="text"
                    value={voiceDestTn}
                    onChange={(e) => setVoiceDestTn(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Attestation Level
                  </label>
                  <select
                    value={voiceAttestLevel}
                    onChange={(e) => setVoiceAttestLevel(e.target.value as 'A' | 'B' | 'C')}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  >
                    <option value="A">A — Full Attestation</option>
                    <option value="B">B — Partial Attestation</option>
                    <option value="C">C — Gateway Attestation</option>
                  </select>
                </div>
              </div>

              <label className="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={voiceTransitStrip}
                  onChange={(e) => setVoiceTransitStrip(e.target.checked)}
                  className="rounded border-slate-300"
                />
                <span>
                  Simulate legacy TDM intermediate transit carrier stripping SIP Identity header
                </span>
              </label>

              <button
                type="button"
                onClick={runStirShakenTestCall}
                disabled={voiceLoading}
                className="w-full py-2 px-4 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors cursor-pointer"
              >
                {voiceLoading ? 'Signing PASSporT (ES256)...' : 'Construct SHAKEN PASSporT & Verify SIP Identity'}
              </button>
            </div>
          </div>

          <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
            <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
              PASSporT Token, SIP Identity Header &amp; Separate Abuse Signal
            </h2>
            {!voiceResult ? (
              <div className="py-12 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-lg">
                <p className="text-xs text-slate-500">
                  Run a test call assertion to inspect the RFC 8225 / RFC 8588 PASSporT claims, SIP Identity header, and attestation scope.
                </p>
              </div>
            ) : (
              <div className="space-y-4 text-xs">
                <div className="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 space-y-2">
                  <div className="flex items-center gap-2 font-semibold text-slate-900 dark:text-slate-100">
                    {voiceResult.verificationStatus === 'valid' ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    ) : (
                      <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0" />
                    )}
                    <span>{voiceResult.qualifiedResultLabel}</span>
                  </div>
                  <p className="text-slate-600 dark:text-slate-400">{voiceResult.attestationMeaning}</p>
                </div>

                <div>
                  <div className="font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Decoded PASSporT Header &amp; Payload (RFC 8588)
                  </div>
                  <pre className="p-3 font-mono bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
                    {JSON.stringify(
                      {
                        header: voiceResult.passportHeader,
                        payload: voiceResult.passportPayload,
                      },
                      null,
                      2
                    )}
                  </pre>
                </div>

                <div>
                  <div className="font-medium text-slate-700 dark:text-slate-300 mb-1">
                    SIP INVITE Identity Header (RFC 8224)
                  </div>
                  <pre className="p-3 font-mono bg-slate-900 text-emerald-300 rounded-lg overflow-x-auto whitespace-pre-wrap break-all">
                    {voiceResult.sipIdentityHeader}
                  </pre>
                </div>

                <div className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 space-y-1">
                  <div className="font-semibold text-slate-900 dark:text-slate-100">
                    Independent Behavioral Robocall / Abuse Analytics Signal:
                  </div>
                  <div className="text-slate-600 dark:text-slate-400">
                    {voiceResult.separateRobocallSignal}
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
