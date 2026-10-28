/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { EyeOff, Clock, Layers, ShieldCheck, Activity, KeyRound, AlertTriangle } from 'lucide-react';
import { BiometricEvidence } from '../types';

interface EvidenceProvenancePanelProps {
  evidence: BiometricEvidence;
}

export const EvidenceProvenancePanel: React.FC<EvidenceProvenancePanelProps> = ({ evidence }) => {
  const getRatingBadge = () => {
    switch (evidence.confidenceRating) {
      case 'high_attested':
        return <span className="bg-green-100 text-green-800 border border-green-200 px-2 py-0.5 rounded text-[10px] font-bold font-mono">HIGHLY ATTESTED (SECURE ENCLAVE)</span>;
      case 'medium_reported':
        return <span className="bg-indigo-100 text-indigo-800 border border-indigo-200 px-2 py-0.5 rounded text-[10px] font-bold font-mono">MEDIUM REPORTED (TRUSTED IDP)</span>;
      default:
        return <span className="bg-amber-100 text-amber-800 border border-amber-200 px-2 py-0.5 rounded text-[10px] font-bold font-mono">LOW UNKNOWN</span>;
    }
  };

  return (
    <div id="evidence-provenance-panel" className="bg-white border border-gray-200 rounded-xl p-5 text-left shadow-sm">
      <div className="flex items-center justify-between border-b border-gray-100 pb-3 mb-4">
        <div>
          <h4 className="text-sm font-bold text-gray-900 flex items-center gap-1.5">
            <Layers className="w-4 h-4 text-indigo-500" /> Evidence Provenance Audit Log
          </h4>
          <p className="text-[10px] text-gray-500">Validated cryptographic authentication context for this active session.</p>
        </div>
        <div>
          {getRatingBadge()}
        </div>
      </div>

      {/* Structured details in definition list format as requested by narrow/wide guidelines */}
      <dl className="grid grid-cols-1 md:grid-cols-2 gap-y-3.5 gap-x-6 text-xs text-gray-700">
        <div>
          <dt className="text-gray-400 font-medium mb-0.5 flex items-center gap-1">
            <Clock className="w-3.5 h-3.5" /> Authentication Time
          </dt>
          <dd className="font-semibold text-gray-900 font-mono">{new Date(evidence.verificationTime).toLocaleString()}</dd>
        </div>

        <div>
          <dt className="text-gray-400 font-medium mb-0.5 flex items-center gap-1">
            <Activity className="w-3.5 h-3.5" /> Evidence Freshness Lifetime
          </dt>
          <dd className="font-semibold text-gray-900 font-mono">
            {evidence.freshnessSeconds} seconds old 
            {evidence.freshnessSeconds > 3600 ? (
              <span className="text-red-600 font-bold ml-1.5">(STALE)</span>
            ) : (
              <span className="text-green-600 font-bold ml-1.5">(ACTIVE)</span>
            )}
          </dd>
        </div>

        <div>
          <dt className="text-gray-400 font-medium mb-0.5 flex items-center gap-1">
            <ShieldCheck className="w-3.5 h-3.5" /> Issuer Authority
          </dt>
          <dd className="font-semibold text-gray-900 font-mono text-indigo-600">{evidence.issuer}</dd>
        </div>

        <div>
          <dt className="text-gray-400 font-medium mb-0.5 flex items-center gap-1">
            <KeyRound className="w-3.5 h-3.5" /> Modality Attestation Proof
          </dt>
          <dd className="font-semibold text-gray-900">
            {evidence.amr === 'face' ? (
              <span className="text-green-700 bg-green-50 px-2 py-0.5 rounded font-mono border border-green-200">
                Direct Face AMR Attested
              </span>
            ) : (
              <span className="text-amber-700 bg-amber-50 px-2 py-0.5 rounded font-mono border border-amber-200">
                User-Verification Generic (UV)
              </span>
            )}
          </dd>
        </div>
      </dl>

      {/* Redacted claims inspection view */}
      <div className="mt-5">
        <div className="flex items-center justify-between mb-2">
          <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider flex items-center gap-1">
            <EyeOff className="w-3.5 h-3.5" /> Redacted Cryptographic Claims Block
          </span>
          <span className="text-[9px] font-mono text-gray-400 bg-gray-50 px-1.5 py-0.5 rounded border border-gray-200">Origin Proof Bound</span>
        </div>
        <p className="text-[10px] text-amber-800 bg-amber-50/50 border border-amber-200/50 p-2.5 rounded-lg mb-2 leading-relaxed">
          <span className="font-bold">Privacy Redaction Rule Applied:</span> Raw biometric matrices, neural templates, and camera coordinate descriptors are stripped inside our secure boundary. Displaying such data on client-side terminals or debug systems is strictly prohibited.
        </p>
        <pre className="bg-gray-900 text-indigo-200 p-3 rounded-xl font-mono text-[10px] overflow-x-auto max-h-[140px] border border-gray-800">
{JSON.stringify({
  "alg": "RS256",
  "typ": "JWT",
  "claims_provenance": {
    "iss": evidence.issuer,
    "sub": "jick.68.0@gmail.com",
    "amr": [evidence.amr === 'face' ? "face" : "uv"],
    "auth_time": Math.floor(new Date(evidence.verificationTime).getTime() / 1000),
    "aud": "face-evidence-gateway",
    "nonce": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
    "biometric_metadata": {
      "hardware_backing": evidence.isHardwareBacked,
      "liveness_verified": evidence.isLivenessProtected,
      "sensor_class": "ir_depth_integrated",
      "neural_template_id": "[REDACTED_BY_VERIFIER_AUTHORITY]",
      "presentation_attack_score": "[REDACTED_METRIC]"
    },
    "audit_reference": evidence.auditReference
  }
}, null, 2)}
        </pre>
      </div>
    </div>
  );
};
