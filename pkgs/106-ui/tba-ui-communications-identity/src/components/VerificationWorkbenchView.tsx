import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  AlertTriangle,
  XCircle,
  Clock,
  ShieldCheck,
  Play,
  FileSearch,
} from 'lucide-react';
import type {
  ChannelFamily,
  CommunicationIdentity,
  VerificationLayerResult,
  VerificationStatus,
  ProductPromiseAnswer,
} from '../types/communications.ts';

interface VerificationWorkbenchViewProps {
  identities: CommunicationIdentity[];
}

type ScenarioMode =
  | 'NOMINAL_VALID'
  | 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS'
  | 'REPLAY_DETECTED'
  | 'POINT_IN_TIME_HISTORICAL_VALID'
  | 'BYTE_OR_HEADER_TAMPERED'
  | 'TRUST_STATUS_INDETERMINATE';

export const VerificationWorkbenchView: React.FC<VerificationWorkbenchViewProps> = ({
  identities,
}) => {
  const [selectedIdentityId, setSelectedIdentityId] = useState(
    identities[0]?.id || 'cid-http-treasury-01'
  );
  const [scenarioMode, setScenarioMode] = useState<ScenarioMode>('NOMINAL_VALID');
  const [historicalTimestamp, setHistoricalTimestamp] = useState('2026-05-15T12:00:00Z');
  const [loading, setLoading] = useState(false);

  const [result, setResult] = useState<{
    overallStatus: VerificationStatus;
    cryptographicValidity: string;
    policyAndAuthorityValidity: string;
    qualifiedHeadline: string;
    profileId: string;
    profileVersion: string;
    representedIdentifier: string;
    coveredComponents: string[];
    layers: VerificationLayerResult[];
    productPromise: ProductPromiseAnswer;
  } | null>(null);

  const selectedIdentity =
    identities.find((i) => i.id === selectedIdentityId) || identities[0];

  const runVerification = async (
    targetIdentityId = selectedIdentityId,
    targetScenario = scenarioMode
  ) => {
    setLoading(true);
    try {
      const targetIdentity =
        identities.find((i) => i.id === targetIdentityId) || identities[0];
      const res = await fetch('/api/v1/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          channelFamily: targetIdentity?.channelFamily || 'webhook-http-sig',
          identityId: targetIdentityId,
          scenarioMode: targetScenario,
          pointInTimeTimestamp: historicalTimestamp,
        }),
      });
      const data = await res.json();
      setResult(data);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    runVerification(selectedIdentityId, scenarioMode);
  }, []);

  const renderStatusIcon = (status: VerificationStatus) => {
    if (status === 'valid') {
      return <CheckCircle2 className="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />;
    }
    if (status === 'stale' || status === 'indeterminate') {
      return <AlertTriangle className="w-4 h-4 text-amber-600 dark:text-amber-400 shrink-0" />;
    }
    return <XCircle className="w-4 h-4 text-rose-600 dark:text-rose-400 shrink-0" />;
  };

  return (
    <div className="space-y-6">
      <div className="pb-4 border-b border-slate-200 dark:border-slate-800">
        <div className="text-xs text-slate-500 dark:text-slate-400">
          Verification Workbench · Layered Appraisal &amp; 7-Question Product Promise
        </div>
        <h1 className="text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100 mt-1">
          Multi-Layer Cryptographic &amp; Policy Verification Workbench
        </h1>
        <p className="text-xs text-slate-600 dark:text-slate-400 mt-1 max-w-3xl">
          Cryptographic signature validity and channel policy/authority validity are evaluated and reported separately. Uploaded or simulated verification artifacts are appraised in memory and redacted by default.
        </p>
      </div>

      {/* Control Bar */}
      <div className="bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 grid grid-cols-1 lg:grid-cols-12 gap-4 items-end">
        <div className="lg:col-span-5">
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            Target Communication Identity &amp; Channel Profile
          </label>
          <select
            value={selectedIdentityId}
            onChange={(e) => {
              setSelectedIdentityId(e.target.value);
              runVerification(e.target.value, scenarioMode);
            }}
            className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md text-slate-900 dark:text-slate-100"
          >
            {identities.map((id) => (
              <option key={id.id} value={id.id}>
                [{id.channelFamily.toUpperCase()}] {id.representedIdentifier} ({id.profileId})
              </option>
            ))}
          </select>
        </div>

        <div className="lg:col-span-5">
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1.5">
            Verification Test Vector / Appraisal Scenario
          </label>
          <select
            value={scenarioMode}
            onChange={(e) => {
              const nextMode = e.target.value as ScenarioMode;
              setScenarioMode(nextMode);
              runVerification(selectedIdentityId, nextMode);
            }}
            className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md text-slate-900 dark:text-slate-100"
          >
            <option value="NOMINAL_VALID">
              1. Nominal Valid (Crypto Valid + Authority Bound + Fresh + Complete Coverage)
            </option>
            <option value="CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS">
              2. Crypto Valid / Policy Invalid (Signed Too Few Components — Omitted Content-Digest)
            </option>
            <option value="REPLAY_DETECTED">
              3. Stale / Replay Rejected (Mathematically Valid Signature Re-Submitted in Window)
            </option>
            <option value="POINT_IN_TIME_HISTORICAL_VALID">
              4. Point-in-Time Historical Resolution (Verifying Prior Binding v1 Before Key Rotation)
            </option>
            <option value="BYTE_OR_HEADER_TAMPERED">
              5. Post-Signature Tampering (Canonical Digest / Byte Range Mismatch)
            </option>
            <option value="TRUST_STATUS_INDETERMINATE">
              6. Degraded / Indeterminate (External OCSP / STI-CRL Status Source Unreachable)
            </option>
          </select>
        </div>

        <div className="lg:col-span-2">
          <button
            type="button"
            onClick={() => runVerification(selectedIdentityId, scenarioMode)}
            disabled={loading}
            className="w-full flex items-center justify-center gap-2 px-4 py-2 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition-colors whitespace-nowrap shrink-0 cursor-pointer"
          >
            <Play className="w-3.5 h-3.5" />
            {loading ? 'Appraising...' : 'Run Appraisal'}
          </button>
        </div>
      </div>

      {result && (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          {/* Left 7 Columns: 8-Layer Verification Breakdown */}
          <div className="lg:col-span-7 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
            <div className="flex flex-wrap items-center justify-between gap-2 pb-4 border-b border-slate-200 dark:border-slate-800">
              <div className="flex items-center gap-2.5">
                {renderStatusIcon(result.overallStatus)}
                <div>
                  <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100">
                    {result.qualifiedHeadline}
                  </h2>
                  <div className="text-xs text-slate-500 font-mono mt-0.5">
                    Profile: {result.profileId} · Status: {result.overallStatus.toUpperCase()}
                  </div>
                </div>
              </div>

              <div className="text-right text-xs font-mono">
                <div>
                  Cryptographic Math:{' '}
                  <span
                    className={
                      result.cryptographicValidity === 'VALID'
                        ? 'text-emerald-700 dark:text-emerald-400 font-semibold'
                        : 'text-rose-700 dark:text-rose-400 font-semibold'
                    }
                  >
                    {result.cryptographicValidity}
                  </span>
                </div>
                <div>
                  Policy &amp; Authority:{' '}
                  <span
                    className={
                      result.policyAndAuthorityValidity === 'VALID_AUTHORIZED'
                        ? 'text-emerald-700 dark:text-emerald-400 font-semibold'
                        : result.policyAndAuthorityValidity === 'INDETERMINATE_EXTERNAL_DEPENDENCY'
                        ? 'text-amber-700 dark:text-amber-400 font-semibold'
                        : 'text-rose-700 dark:text-rose-400 font-semibold'
                    }
                  >
                    {result.policyAndAuthorityValidity}
                  </span>
                </div>
              </div>
            </div>

            <div className="divide-y divide-slate-200 dark:divide-slate-800 border border-slate-200 dark:border-slate-800 rounded-lg">
              {result.layers.map((layer) => (
                <div key={layer.layer} className="p-3.5 space-y-1">
                  <div className="flex items-center justify-between gap-2">
                    <div className="flex items-center gap-2">
                      {renderStatusIcon(layer.status)}
                      <span className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                        {layer.title}
                      </span>
                    </div>
                    <span className="text-xs font-mono text-slate-500">
                      {layer.status.toUpperCase()} · {layer.reasonCode}
                    </span>
                  </div>
                  <p className="text-xs text-slate-600 dark:text-slate-400 pl-6 leading-relaxed">
                    {layer.detail}
                  </p>
                </div>
              ))}
            </div>
          </div>

          {/* Right 5 Columns: The 7-Question Product Promise Resolution */}
          <div className="lg:col-span-5 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-lg p-5 space-y-4">
            <div className="pb-3 border-b border-slate-200 dark:border-slate-800">
              <div className="text-xs text-slate-500">Product Promise Appraisal</div>
              <h2 className="text-base font-semibold text-slate-900 dark:text-slate-100 mt-0.5">
                7-Question Attestation Resolution
              </h2>
            </div>

            <dl className="space-y-3 text-xs">
              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  1. Who or what requested the signature or assertion?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 font-mono mt-1">
                  {result.productPromise.actorWhoRequested}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  2. Which organization, domain, number, mailbox, role, or endpoint was represented?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 font-mono mt-1">
                  {result.productPromise.representedEntity}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  3. What authority allowed that representation?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 mt-1">
                  {result.productPromise.authorityBasis}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  4. Which fields or content were cryptographically covered?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 font-mono mt-1">
                  {result.productPromise.cryptographicallyCoveredFields.join(' · ')}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  5. Which certificate, key, trust framework, and profile were used?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 font-mono mt-1">
                  {result.productPromise.certificateKeyTrustProfile}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  6. Was the proof valid, fresh, authorized, and non-replayed at verification time?
                </dt>
                <dd className="text-slate-700 dark:text-slate-300 mt-1">
                  {result.productPromise.validityFreshnessReplayStatus}
                </dd>
              </div>

              <div className="p-3 rounded-md bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 space-y-2">
                <dt className="font-semibold text-slate-900 dark:text-slate-100">
                  7. What does the proof establish—and what does it NOT establish?
                </dt>
                <dd className="space-y-1.5">
                  <div className="text-emerald-700 dark:text-emerald-400 font-medium">
                    Establishes:
                  </div>
                  <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                    {result.productPromise.establishes.map((item, idx) => (
                      <li key={idx}>• {item}</li>
                    ))}
                  </ul>
                  <div className="text-amber-700 dark:text-amber-400 font-medium pt-1">
                    Does NOT Establish:
                  </div>
                  <ul className="space-y-1 text-slate-700 dark:text-slate-300">
                    {result.productPromise.doesNotEstablish.map((item, idx) => (
                      <li key={idx}>• {item}</li>
                    ))}
                  </ul>
                </dd>
              </div>
            </dl>
          </div>
        </div>
      )}
    </div>
  );
};
