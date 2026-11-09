import React, { useState } from 'react';
import {
  KeyRound,
  ShieldAlert,
  CheckCircle2,
  XCircle,
  Lock,
  Terminal,
  Server,
} from 'lucide-react';
import type {
  CommunicationIdentity,
  SignerCustodyRecord,
  EvidenceReceipt,
} from '../types/communications.ts';

interface CustodyAndSignersViewProps {
  identities: CommunicationIdentity[];
  signers: SignerCustodyRecord[];
  onSignReceiptCreated: () => void;
}

const API_CONTRACT_SPECS = [
  {
    endpoint: 'GET /api/v1/profiles',
    mediaType: 'application/vnd.tba.comm-profiles.v1+json',
    ownership: 'Communications Identity API + Trust Registry',
    rules: 'Returns channel profile versions, conformance phases, allowed algorithms, and explicit non-claims.',
  },
  {
    endpoint: 'GET · POST · PATCH /api/v1/communication-identities',
    mediaType: 'application/vnd.tba.comm-identity.v1+json',
    ownership: 'Communications Identity API + Principals/Policy',
    rules: 'Manages point-in-time resolvable bindings. Reassignments append a new binding version and never mutate historical evidence.',
  },
  {
    endpoint: 'GET /api/v1/signers',
    mediaType: 'application/vnd.tba.signer-custody.v1+json',
    ownership: 'Communications Identity API + Certificate Center',
    rules: 'Enforces HSM/KMS non-exportable custody and tenant/environment/channel/purpose isolation. Never exposes private keys.',
  },
  {
    endpoint: 'POST /api/v1/sign',
    mediaType: 'Profile-specific (RFC 9421, PASSporT, S/MIME CMS, PAdES)',
    ownership: 'Communications Identity API + JOSE/HSM Boundary',
    rules: 'Requires content digest and server-side actor authorization resolution. Denies arbitrary key IDs or OAuth/JWT key reuse.',
  },
  {
    endpoint: 'POST /api/v1/verify',
    mediaType: 'application/vnd.tba.verification-appraisal.v1+json',
    ownership: 'Communications Identity API + Attestation Center',
    rules: 'Returns machine-readable 8-layer sub-results and separates cryptographic math validity from policy/authority validity.',
  },
  {
    endpoint: 'GET /api/v1/evidence · POST /api/v1/incidents/action',
    mediaType: 'application/vnd.tba.evidence-receipt.v1+json',
    ownership: 'Communications Identity API + Audit & Security Signals',
    rules: 'Stores SHA-256 digests without raw message bodies. Suspends compromised keys immediately while preserving point-in-time historical verification.',
  },
];

export const CustodyAndSignersView: React.FC<CustodyAndSignersViewProps> = ({
  identities,
  signers,
  onSignReceiptCreated,
}) => {
  const [selectedIdentityId, setSelectedIdentityId] = useState(
    identities[0]?.id || 'cid-http-treasury-01'
  );
  const [actorPrincipal, setActorPrincipal] = useState(
    identities[0]?.allowedActors[0] || 'wkld-ledger-outbox-prod'
  );
  const [purpose, setPurpose] = useState('SETTLEMENT_WEBHOOK_DISPATCH');
  const [payloadSummary, setPayloadSummary] = useState(
    '{"event":"settlement.completed","settlementId":"stl_994810","amount":"2450000.00"}'
  );
  const [attemptKeyMisuse, setAttemptKeyMisuse] = useState(false);
  const [signLoading, setSignLoading] = useState(false);
  const [signResult, setSignResult] = useState<{
    authorized: boolean;
    canonicalInput?: string;
    detachedSignatureBase64?: string;
    receipt: EvidenceReceipt;
  } | null>(null);

  const selectedIdentity =
    identities.find((i) => i.id === selectedIdentityId) || identities[0];

  const handleIdentityChange = (nextId: string) => {
    setSelectedIdentityId(nextId);
    const found = identities.find((i) => i.id === nextId);
    if (found) {
      setActorPrincipal(found.allowedActors[0] || 'svc-default');
      setPurpose(found.permittedPurposes[0] || 'DEFAULT_PURPOSE');
    }
  };

  const executeSigningTest = async (presetMode?: 'AUTHORIZED' | 'UNAUTHORIZED_ACTOR' | 'KEY_MISUSE') => {
    setSignLoading(true);
    let effectiveActor = actorPrincipal;
    let effectiveMisuse = attemptKeyMisuse;

    if (presetMode === 'AUTHORIZED' && selectedIdentity) {
      effectiveActor = selectedIdentity.allowedActors[0];
      effectiveMisuse = false;
      setActorPrincipal(effectiveActor);
      setAttemptKeyMisuse(false);
    } else if (presetMode === 'UNAUTHORIZED_ACTOR') {
      effectiveActor = 'svc-unapproved-marketing-bot@meridian.internal';
      effectiveMisuse = false;
      setActorPrincipal(effectiveActor);
      setAttemptKeyMisuse(false);
    } else if (presetMode === 'KEY_MISUSE') {
      effectiveMisuse = true;
      setAttemptKeyMisuse(true);
    }

    try {
      const res = await fetch('/api/v1/sign', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          identityId: selectedIdentityId,
          actorPrincipal: effectiveActor,
          purpose,
          payloadSummary,
          attemptCrossPurposeKeyMisuse: effectiveMisuse,
        }),
      });
      const data = await res.json();
      setSignResult(data);
      onSignReceiptCreated();
    } finally {
      setSignLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 dark:border-slate-800">
        <div className="text-xs text-slate-500 dark:text-slate-400">
          Key Custody, Signer Authorization &amp; Architectural Ownership
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-1">
          Non-Exportable Custody Matrix &amp; Signing-Oracle Boundary
        </h1>
        <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-3xl">
          Private signing keys default to HSM, Cloud KMS, or Remote QTSP SAM custody and never leave the security boundary. General OAuth/JWT keys are strictly prohibited from signing voice, email, document, or webhook assertions.
        </p>
      </div>

      {/* Interactive Signing Boundary Policy Tester (/api/v1/sign) */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
        <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                Interactive Signing Boundary Tester (POST /api/v1/sign)
              </h2>
              <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
                Test actor authorization, suspended identity rejection, and cross-protocol key misuse prevention.
              </p>
            </div>
          </div>

          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => executeSigningTest('AUTHORIZED')}
              className="px-3 py-1.5 text-xs font-medium bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-900 dark:text-slate-100 rounded-md transition-colors cursor-pointer"
            >
              Preset 1: Authorized Workload
            </button>
            <button
              type="button"
              onClick={() => executeSigningTest('UNAUTHORIZED_ACTOR')}
              className="px-3 py-1.5 text-xs font-medium bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-900 dark:text-slate-100 rounded-md transition-colors cursor-pointer"
            >
              Preset 2: Unauthorized Actor Attempt
            </button>
            <button
              type="button"
              onClick={() => executeSigningTest('KEY_MISUSE')}
              className="px-3 py-1.5 text-xs font-medium bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 text-slate-900 dark:text-slate-100 rounded-md transition-colors cursor-pointer"
            >
              Preset 3: OAuth/JWT Key Reuse Attempt
            </button>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Communication Identity
            </label>
            <select
              value={selectedIdentityId}
              onChange={(e) => handleIdentityChange(e.target.value)}
              className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md text-slate-900 dark:text-slate-100"
            >
              {identities.map((id) => (
                <option key={id.id} value={id.id}>
                  [{id.status}] {id.representedIdentifier} ({id.channelFamily})
                </option>
              ))}
            </select>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Requesting Actor / Workload Principal
              </label>
              <input
                type="text"
                value={actorPrincipal}
                onChange={(e) => setActorPrincipal(e.target.value)}
                className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
              />
            </div>
            <div>
              <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                Asserted Purpose
              </label>
              <input
                type="text"
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
                className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Detached Content Input (Hashed at Boundary; Raw Body Never Stored in Evidence)
            </label>
            <textarea
              rows={2}
              value={payloadSummary}
              onChange={(e) => setPayloadSummary(e.target.value)}
              className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
            />
          </div>

          <label className="flex items-center gap-2 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
            <input
              type="checkbox"
              checked={attemptKeyMisuse}
              onChange={(e) => setAttemptKeyMisuse(e.target.checked)}
              className="rounded border-slate-300"
            />
            <span>
              Simulate cross-protocol key confusion (attempting to sign with general OAuth/JWT key)
            </span>
          </label>

          <button
            type="button"
            onClick={() => executeSigningTest()}
            disabled={signLoading}
            className="w-full py-2 px-4 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors cursor-pointer"
          >
            {signLoading ? 'Evaluating Policy & Custody...' : 'Submit Typed Signing Request'}
          </button>
        </div>

        <div className="lg:col-span-6 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
          <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
            Signing Boundary Decision &amp; Content-Minimized Receipt
          </h2>
          {!signResult ? (
            <div className="py-12 text-center border border-dashed border-slate-200 dark:border-slate-800 rounded-lg">
              <p className="text-xs text-slate-500">
                Execute a signing request or choose a preset on the left to inspect the policy decision, canonical input, and evidence receipt.
              </p>
            </div>
          ) : (
            <div className="space-y-4 text-xs">
              <div className="p-3.5 rounded-lg border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 space-y-2">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 font-semibold text-slate-900 dark:text-slate-100">
                    {signResult.authorized ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                    ) : (
                      <XCircle className="w-4 h-4 text-rose-600 shrink-0" />
                    )}
                    <span>{signResult.receipt.qualifiedResultLabel}</span>
                  </div>
                  <span className="font-mono text-slate-500">
                    {signResult.receipt.authorizationOutcome}
                  </span>
                </div>
                <div className="font-mono text-slate-600 dark:text-slate-400">
                  Assertion ID: {signResult.receipt.assertionId} · Policy ID:{' '}
                  {signResult.receipt.policyDecisionId}
                </div>
                <div className="font-mono text-slate-600 dark:text-slate-400 break-all">
                  Input Digest: {signResult.receipt.inputContentDigestSha256} (Raw Content Retained:{' '}
                  {String(signResult.receipt.rawContentRetained)})
                </div>
              </div>

              {signResult.canonicalInput && (
                <div>
                  <div className="font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Constructed Profile-Native Canonical Signing Input
                  </div>
                  <pre className="p-3 font-mono bg-slate-900 text-slate-100 rounded-lg overflow-x-auto">
                    {signResult.canonicalInput}
                  </pre>
                </div>
              )}

              <div className="p-3 rounded-lg border border-slate-200 dark:border-slate-800 space-y-1">
                <div className="font-semibold text-slate-900 dark:text-slate-100">
                  Authority &amp; Custody Audit Record:
                </div>
                <div className="text-slate-600 dark:text-slate-400">
                  Actor: <span className="font-mono">{signResult.receipt.actorPrincipal}</span>
                </div>
                <div className="text-slate-600 dark:text-slate-400">
                  Represented Identity:{' '}
                  <span className="font-mono">{signResult.receipt.representedIdentifier}</span>
                </div>
                <div className="text-slate-600 dark:text-slate-400">
                  Authority Basis: {signResult.receipt.productPromise.authorityBasis}
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Signer Custody Inventory Table */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
        <div className="p-5 border-b border-slate-200 dark:border-slate-800">
          <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
            Active Key Custody &amp; Domain-Separated Signer Inventory
          </h2>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
            Keys are strictly partitioned by tenant, environment, channel, communication identity, profile, and purpose.
          </p>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse">
            <thead>
              <tr className="border-b border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-950 text-xs font-semibold text-slate-600 dark:text-slate-400">
                <th className="py-3 px-4">Key Identifier</th>
                <th className="py-3 px-4">Channel &amp; Purpose</th>
                <th className="py-3 px-4">Algorithm</th>
                <th className="py-3 px-4">Custody Class</th>
                <th className="py-3 px-4">Quorum / Export</th>
                <th className="py-3 px-4">Rotation State</th>
                <th className="py-3 px-4 text-right">Expires</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-200 dark:divide-slate-800 text-xs">
              {signers.map((sgn) => (
                <tr
                  key={sgn.id}
                  className="hover:bg-slate-50/80 dark:hover:bg-slate-800/40 transition-colors"
                >
                  <td className="py-3 px-4 font-mono font-medium text-slate-900 dark:text-slate-100">
                    <div>{sgn.keyId}</div>
                    <div className="text-slate-500 text-[11px]">{sgn.publicJwkThumbprint}</div>
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-700 dark:text-slate-300">
                    {sgn.channelFamily} · {sgn.purpose}
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-700 dark:text-slate-300">
                    {sgn.algorithm}
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-700 dark:text-slate-300">
                    {sgn.custodyClass}
                  </td>
                  <td className="py-3 px-4 text-slate-600 dark:text-slate-400">
                    Non-Exportable · {sgn.quorumRequired ? 'Dual Quorum' : 'Workload Attested'}
                  </td>
                  <td className="py-3 px-4 font-mono text-slate-800 dark:text-slate-200">
                    {sgn.rotationState}
                  </td>
                  <td className="py-3 px-4 font-mono text-right text-slate-600 dark:text-slate-400 tabular-nums">
                    {sgn.expiresAt.slice(0, 10)}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Architectural Ownership & Versioned API Reference */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg overflow-hidden">
        <div className="p-5 border-b border-slate-200 dark:border-slate-800">
          <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
            Communications Identity API Surface &amp; Architectural Ownership
          </h2>
          <p className="text-xs text-slate-600 dark:text-slate-400 mt-0.5">
            Pairing: <span className="font-mono">tba-router-communications-identity</span> +{' '}
            <span className="font-mono">@tba/communications-identity-uix</span> orchestrating Certificate Center, Trust Registry, JOSE, Attestation Center, and Security Signals.
          </p>
        </div>
        <div className="divide-y divide-slate-200 dark:divide-slate-800">
          {API_CONTRACT_SPECS.map((spec, idx) => (
            <div
              key={idx}
              className="p-4 flex flex-col lg:flex-row lg:items-center lg:justify-between gap-2 text-xs"
            >
              <div className="space-y-1">
                <div className="font-mono font-semibold text-slate-900 dark:text-slate-100">
                  {spec.endpoint}
                </div>
                <div className="text-slate-600 dark:text-slate-400">{spec.rules}</div>
              </div>
              <div className="lg:text-right font-mono text-slate-500 shrink-0">
                <div>{spec.mediaType}</div>
                <div className="text-slate-400">{spec.ownership}</div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
