/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { ShieldCheck, ShieldAlert, AlertTriangle, CheckCircle, Info, Key, ExternalLink } from 'lucide-react';
import { EvidenceProvenance, BiometricEvidence } from '../types';

interface BiometricEvidenceQualifierProps {
  provenance: EvidenceProvenance;
  evidence?: BiometricEvidence;
  compact?: boolean;
}

export const BiometricEvidenceQualifier: React.FC<BiometricEvidenceQualifierProps> = ({
  provenance,
  evidence,
  compact = false
}) => {
  // Config state mappings based on the rigorous requirements
  const getConfig = () => {
    switch (provenance) {
      case 'face_verified':
        return {
          title: 'Direct Facial Recognition Attested',
          badgeClass: 'bg-green-50 border-green-200 text-green-800',
          iconClass: 'text-green-600 bg-green-100',
          icon: ShieldCheck,
          confidence: 'CRITICAL / PHISHING RESISTANT',
          description: 'Verified directly in our approved native biometric capture boundary. Challenge-bound liveness was fully attested and hardware enclave bound.',
          hardware: 'YES (Secure Enclave Sealed)',
          liveness: 'YES (Active Challenge-Response Verification)'
        };
      case 'upstream_face_trusted':
        return {
          title: 'Federated Face Evidence Accepted',
          badgeClass: 'bg-indigo-50 border-indigo-200 text-indigo-800',
          iconClass: 'text-indigo-600 bg-indigo-100',
          icon: CheckCircle,
          confidence: 'HIGH / FEDERATED SOURCE',
          description: 'Exposed by a trusted configured identity provider (IDP) with verified AMR mappings. Trusted assertion and origin signatures verified.',
          hardware: 'YES (Upstream Attested)',
          liveness: 'YES (Upstream Evaluated)'
        };
      case 'user_verified_modality_unknown':
        return {
          title: 'User Verified (Modality Unknown)',
          badgeClass: 'bg-amber-50 border-amber-200 text-amber-800',
          iconClass: 'text-amber-600 bg-amber-100',
          icon: Key,
          confidence: 'MEDIUM / NOT MODALITY CERTIFIED',
          description: 'A WebAuthn user verification flag was received from the browser. Modality cannot be proven. It might be a PIN, fingerprint, or password.',
          hardware: 'Indeterminate',
          liveness: 'No separate liveness proof'
        };
      case 'upstream_face_untrusted':
        return {
          title: 'Unmapped / Untrusted Upstream Claim',
          badgeClass: 'bg-red-50 border-red-200 text-red-800',
          iconClass: 'text-red-600 bg-red-100',
          icon: ShieldAlert,
          confidence: 'INSUFFICIENT TRUST',
          description: 'The identity provider reported face recognition, but the provider or signature fails our required regional/tenant trust profiles.',
          hardware: 'UNVERIFIED',
          liveness: 'UNVERIFIED'
        };
      case 'face_evidence_stale':
        return {
          title: 'Face Evidence Expired (Stale)',
          badgeClass: 'bg-red-50 border-red-200 text-red-800',
          iconClass: 'text-red-600 bg-red-100',
          icon: AlertTriangle,
          confidence: 'STALE ASSERTION',
          description: 'The facial authenticator assertion is valid, but exceeds the tenant maximum lifetime policy. Step-up liveness check required.',
          hardware: 'YES (But expired session time)',
          liveness: 'Expired'
        };
      default:
        return {
          title: 'Unknown Evidence Provenance',
          badgeClass: 'bg-gray-100 border-gray-200 text-gray-800',
          iconClass: 'text-gray-600 bg-gray-200',
          icon: Info,
          confidence: 'NO TRUST RATINGS',
          description: 'No validated biometric claims are present in current session headers.',
          hardware: 'NO',
          liveness: 'NO'
        };
    }
  };

  const config = getConfig();
  const Icon = config.icon;

  if (compact) {
    return (
      <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-semibold border ${config.badgeClass}`}>
        <Icon className="w-3.5 h-3.5" />
        <span>{config.title}</span>
      </div>
    );
  }

  return (
    <div id={`evidence-qualifier-${provenance}`} className="bg-white border border-gray-200 rounded-xl p-5 text-left shadow-sm">
      <div className="flex items-start gap-3.5">
        <div className={`p-2.5 rounded-xl shrink-0 ${config.iconClass}`}>
          <Icon className="w-5.5 h-5.5" />
        </div>
        <div className="space-y-1">
          <div className="flex flex-wrap items-center gap-2">
            <h4 className="text-sm font-bold text-gray-900">{config.title}</h4>
            <span className="text-[9px] font-mono font-bold tracking-wider px-2 py-0.5 rounded bg-gray-100 text-gray-700 border border-gray-200">
              AMR: {provenance === 'user_verified_modality_unknown' ? 'uv' : 'face'}
            </span>
          </div>
          <p className="text-xs text-gray-600 leading-relaxed">{config.description}</p>
        </div>
      </div>

      {/* Trust Rating Meta Panel */}
      <div className="grid grid-cols-3 gap-2 mt-4 pt-3.5 border-t border-gray-100 text-[11px]">
        <div>
          <span className="block text-gray-400 font-medium">Confidence Level</span>
          <span className="font-semibold text-gray-900 font-mono">{config.confidence}</span>
        </div>
        <div>
          <span className="block text-gray-400 font-medium">Hardware Bound</span>
          <span className="font-semibold text-gray-900 font-mono">{config.hardware}</span>
        </div>
        <div>
          <span className="block text-gray-400 font-medium">Liveness Certified</span>
          <span className="font-semibold text-gray-900 font-mono">{config.liveness}</span>
        </div>
      </div>

      {/* Warning callout for WebAuthn UV Fallback */}
      {provenance === 'user_verified_modality_unknown' && (
        <div className="bg-amber-50/75 border border-amber-200 rounded-lg p-3 mt-3 flex items-start gap-2 text-[11px] text-amber-900">
          <AlertTriangle className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
          <div>
            <span className="font-bold">Strict Modality Warning:</span> This assertion was processed via a standard WebAuthn browser call. The operating system authenticated the user locally, but does not transmit evidence proving that facial recognition (rather than a PIN, pattern, or touch) was executed. <span className="font-semibold underline">Never represent this assertion as face-authenticated in security dashboards.</span>
          </div>
        </div>
      )}

      {/* Verified Claims Payload Details */}
      {evidence && (
        <div className="mt-4 pt-3 border-t border-dashed border-gray-100">
          <span className="text-[10px] uppercase font-bold text-gray-400 tracking-wider">Verified Token Reference</span>
          <div className="mt-1 bg-gray-50 rounded-lg p-2.5 font-mono text-[10px] text-gray-600 grid grid-cols-2 gap-y-1 gap-x-4">
            <div>Issuer Auth: <span className="text-indigo-600">{evidence.issuer}</span></div>
            <div>Audit Hash: <span className="text-gray-900">{evidence.auditReference.substring(0, 16)}...</span></div>
            <div>Age Checked: <span className="text-gray-900">{evidence.freshnessSeconds}s ago</span></div>
            <div>Hardware: <span className="text-gray-900">{evidence.isHardwareBacked ? 'True' : 'False'}</span></div>
          </div>
        </div>
      )}
    </div>
  );
};
