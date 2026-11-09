import React, { useState } from 'react';
import { X, AlertTriangle, CheckCircle2, ArrowRight, ArrowLeft } from 'lucide-react';
import type { ChannelFamily, CustodyClass } from '../types/communications.ts';

interface OnboardingWizardModalProps {
  isOpen: boolean;
  onClose: () => void;
  onCreated: () => void;
}

const CHANNEL_PRESETS: Record<
  ChannelFamily,
  {
    label: string;
    identifierPlaceholder: string;
    identifierType:
      | 'TELEPHONE_RANGE'
      | 'DOMAIN'
      | 'MAILBOX'
      | 'DOCUMENT_ROLE'
      | 'WEBHOOK_SERVICE';
    authorityPlaceholder: string;
    verificationMethod: string;
    defaultCustody: CustodyClass;
    purposePlaceholder: string;
    externalGovernanceCaveat: string;
  }
> = {
  'webhook-http-sig': {
    label: 'RFC 9421 Webhook & API Message Signing (Phase 1)',
    identifierPlaceholder: 'https://events.meridiantreasury.com/v2/payout-callbacks',
    identifierType: 'WEBHOOK_SERVICE',
    authorityPlaceholder: 'SPIFFE Workload ID spiffe://meridian.prod/ns/payout/sa/dispatcher + DNS TXT',
    verificationMethod: 'SPIFFE mTLS Attestation + DNS-01 Key Publication',
    defaultCustody: 'CLOUD_KMS_NON_EXPORTABLE',
    purposePlaceholder: 'PAYOUT_CALLBACK_RFC9421_SIGN',
    externalGovernanceCaveat:
      'Technical activation publishes the public JWK thumbprint to the partner JWKS endpoint. Receiving partner API verifiers must refresh their cache TTL before enforcing the new key ID.',
  },
  'bimi-mark': {
    label: 'BIMI Brand Indicator & VMC/CMC Mark Evidence (Phase 2)',
    identifierPlaceholder: 'institutional.meridiantreasury.com (selector: default)',
    identifierType: 'DOMAIN',
    authorityPlaceholder: 'USPTO Trademark Reg. #7,104,992 + DigiCert MVA VMC Application #VMC-9921',
    verificationMethod: 'MVA Trademark Notarization + DMARC p=reject DNS Verification',
    defaultCustody: 'HSM_FIPS_140_3_L3',
    purposePlaceholder: 'BIMI_VMC_DOMAIN_ASSERTION',
    externalGovernanceCaveat:
      'Technical DNS and SVG Tiny P/S validation does NOT complete external Mark Verifying Authority (MVA) issuance or guarantee mailbox-provider logo display.',
  },
  smime: {
    label: 'S/MIME 4.0 Organizational Mailbox Identity (Phase 2)',
    identifierPlaceholder: 'treasury-ops-sign@meridiantreasury.com',
    identifierType: 'MAILBOX',
    authorityPlaceholder: 'CABF Strict Organization Proof + Enterprise IdP Role Assignment #TR-88',
    verificationMethod: 'ACME S/MIME Challenge + FIDO2 Hardware Passkey Step-Up',
    defaultCustody: 'HSM_FIPS_140_3_L3',
    purposePlaceholder: 'SMIME_RFC8551_SIGN_ONLY',
    externalGovernanceCaveat:
      'Enforces separate signing and encryption keys. Signing key is non-escrowed; CABF public CA validation is required before external mail clients trust the chain.',
  },
  'document-signing': {
    label: 'PAdES-B-LTA Regulated Document Signing (Phase 3)',
    identifierPlaceholder: 'Authorized Treasury Signatory · EMEA Clearing Mandates',
    identifierType: 'DOCUMENT_ROLE',
    authorityPlaceholder: 'Commercial Register Extract HRB-99201 + eIDAS QTSP Video Ident Ref #ID-441',
    verificationMethod: 'Remote QTSP SAM Sole-Control Ceremony + Biometric Step-Up',
    defaultCustody: 'REMOTE_QTSP_SAM',
    purposePlaceholder: 'PADES_LTA_INSTITUTIONAL_MANDATE',
    externalGovernanceCaveat:
      'Technical profile configuration does NOT confer eIDAS Qualified status until the external Trust Service Provider (QTSP) completes identity proofing and issues the qualified certificate.',
  },
  'stir-shaken': {
    label: 'STIR/SHAKEN SIP Caller Identity (Phase 4)',
    identifierPlaceholder: '+1 (312) 555-0400 through +1 (312) 555-0499 (SPC 8492A)',
    identifierType: 'TELEPHONE_RANGE',
    authorityPlaceholder: 'FCC RMD Filing #RMD-0049182 + NANPA LOA + STI-PA SPC Token',
    verificationMethod: 'STI-PA ICONectiv Token + Carrier SBC mTLS Trunk Binding',
    defaultCustody: 'HSM_FIPS_140_3_L3',
    purposePlaceholder: 'SIP_INVITE_PASSPORT_SHAKEN_A',
    externalGovernanceCaveat:
      'Technical onboarding stages the PASSporT signing policy, but live call attestation requires STI Policy Administrator (STI-PA) approval and STI-CA certificate issuance in the target jurisdiction.',
  },
};

export const OnboardingWizardModal: React.FC<OnboardingWizardModalProps> = ({
  isOpen,
  onClose,
  onCreated,
}) => {
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [channelFamily, setChannelFamily] = useState<ChannelFamily>('webhook-http-sig');
  const [organization, setOrganization] = useState('Meridian Global Treasury Ltd.');
  const [ownerTeam, setOwnerTeam] = useState('Communications Security Engineering');
  const [environment, setEnvironment] = useState<
    'production' | 'staging' | 'regulated-eu' | 'carrier-us-east'
  >('production');
  const [representedIdentifier, setRepresentedIdentifier] = useState(
    CHANNEL_PRESETS['webhook-http-sig'].identifierPlaceholder
  );
  const [authorityEvidence, setAuthorityEvidence] = useState(
    CHANNEL_PRESETS['webhook-http-sig'].authorityPlaceholder
  );
  const [allowedActor, setAllowedActor] = useState(
    'wkld-payout-dispatcher@meridian.internal'
  );
  const [custodyClass, setCustodyClass] = useState<CustodyClass>('CLOUD_KMS_NON_EXPORTABLE');
  const [permittedPurpose, setPermittedPurpose] = useState('PAYOUT_CALLBACK_RFC9421_SIGN');
  const [governanceAck, setGovernanceAck] = useState(false);
  const [submitting, setSubmitting] = useState(false);

  if (!isOpen) return null;

  const preset = CHANNEL_PRESETS[channelFamily];

  const handleChannelChange = (nextChannel: ChannelFamily) => {
    setChannelFamily(nextChannel);
    const nextPreset = CHANNEL_PRESETS[nextChannel];
    setRepresentedIdentifier(nextPreset.identifierPlaceholder);
    setAuthorityEvidence(nextPreset.authorityPlaceholder);
    setCustodyClass(nextPreset.defaultCustody);
    setPermittedPurpose(nextPreset.purposePlaceholder);
  };

  const handleSubmit = async () => {
    if (!governanceAck) return;
    setSubmitting(true);
    try {
      const res = await fetch('/api/v1/communication-identities', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          organization,
          ownerTeam,
          environment,
          channelFamily,
          representedIdentifier,
          identifierType: preset.identifierType,
          authorityEvidence,
          verificationMethod: preset.verificationMethod,
          allowedActor,
          custodyClass,
          permittedPurpose,
          assuranceRequirement: 'WORKLOAD_OR_FIDO2_STEP_UP',
        }),
      });
      if (res.ok) {
        onCreated();
        onClose();
      }
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur-xs p-4">
      <div className="w-full max-w-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 rounded-xl shadow-xl overflow-hidden">
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-200 dark:border-slate-800">
          <div>
            <div className="text-xs text-slate-500">
              Channel-Specific Identity Onboarding Wizard · Step {step} of 3
            </div>
            <h2 className="text-lg font-bold text-slate-900 dark:text-slate-100">
              Register Communication Identity &amp; Authority Binding v1
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-slate-700 dark:hover:text-slate-200 rounded-lg cursor-pointer"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="p-6 space-y-5 max-h-[75vh] overflow-y-auto">
          {step === 1 && (
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  1. Select Channel Profile Family
                </label>
                <select
                  value={channelFamily}
                  onChange={(e) => handleChannelChange(e.target.value as ChannelFamily)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md text-slate-900 dark:text-slate-100"
                >
                  <option value="webhook-http-sig">
                    RFC 9421 Webhook &amp; HTTP Message Signing (Phase 1)
                  </option>
                  <option value="bimi-mark">
                    BIMI Brand Indicator with VMC/CMC Evidence (Phase 2)
                  </option>
                  <option value="smime">
                    S/MIME 4.0 Signing &amp; Encryption Identity (Phase 2)
                  </option>
                  <option value="document-signing">
                    PAdES-B-LTA Regulated Document Signing (Phase 3)
                  </option>
                  <option value="stir-shaken">
                    STIR/SHAKEN SIP Caller Identity (Phase 4)
                  </option>
                </select>
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Organization
                  </label>
                  <input
                    type="text"
                    value={organization}
                    onChange={(e) => setOrganization(e.target.value)}
                    className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Owner Team
                  </label>
                  <input
                    type="text"
                    value={ownerTeam}
                    onChange={(e) => setOwnerTeam(e.target.value)}
                    className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    Environment Scope
                  </label>
                  <select
                    value={environment}
                    onChange={(e) =>
                      setEnvironment(
                        e.target.value as
                          | 'production'
                          | 'staging'
                          | 'regulated-eu'
                          | 'carrier-us-east'
                      )
                    }
                    className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  >
                    <option value="production">production</option>
                    <option value="staging">staging</option>
                    <option value="regulated-eu">regulated-eu</option>
                    <option value="carrier-us-east">carrier-us-east</option>
                  </select>
                </div>
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  2. Represented Identifier ({preset.identifierType})
                </label>
                <input
                  type="text"
                  value={representedIdentifier}
                  onChange={(e) => setRepresentedIdentifier(e.target.value)}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  3. Authority &amp; Ownership Proof Reference
                </label>
                <input
                  type="text"
                  value={authorityEvidence}
                  onChange={(e) => setAuthorityEvidence(e.target.value)}
                  className="w-full px-3 py-2 text-xs bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                />
              </div>
            </div>
          )}

          {step === 2 && (
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                  4. Authorized Requesting Actor / Workload Principal
                </label>
                <input
                  type="text"
                  value={allowedActor}
                  onChange={(e) => setAllowedActor(e.target.value)}
                  className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                />
              </div>

              <div className="grid grid-cols-1 sm:grid-cols-2 gap-3">
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    5. Non-Exportable Key Custody Class
                  </label>
                  <select
                    value={custodyClass}
                    onChange={(e) => setCustodyClass(e.target.value as CustodyClass)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  >
                    <option value="HSM_FIPS_140_3_L3">HSM_FIPS_140_3_L3</option>
                    <option value="CLOUD_KMS_NON_EXPORTABLE">CLOUD_KMS_NON_EXPORTABLE</option>
                    <option value="REMOTE_QTSP_SAM">REMOTE_QTSP_SAM</option>
                    <option value="EXTERNAL_STI_SIGNER">EXTERNAL_STI_SIGNER</option>
                  </select>
                </div>
                <div>
                  <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
                    6. Permitted Signing Purpose
                  </label>
                  <input
                    type="text"
                    value={permittedPurpose}
                    onChange={(e) => setPermittedPurpose(e.target.value)}
                    className="w-full px-3 py-2 text-xs font-mono bg-slate-50 dark:bg-slate-950 border border-slate-300 dark:border-slate-700 rounded-md"
                  />
                </div>
              </div>

              <div className="p-3.5 rounded-lg bg-slate-50 dark:bg-slate-950 border border-slate-200 dark:border-slate-800 text-xs space-y-1">
                <div className="font-semibold text-slate-900 dark:text-slate-100">
                  Key Isolation Guarantee:
                </div>
                <p className="text-slate-600 dark:text-slate-400">
                  A dedicated signing key will be provisioned in {custodyClass} scoped exclusively to{' '}
                  <span className="font-mono">{representedIdentifier}</span>. General OAuth/JWT keys cannot be bound.
                </p>
              </div>
            </div>
          )}

          {step === 3 && (
            <div className="space-y-4">
              <div className="text-xs font-semibold text-slate-900 dark:text-slate-100">
                7. Pre-Activation Binding Diff &amp; External Governance Review
              </div>
              <pre className="p-3.5 text-xs font-mono bg-slate-900 text-emerald-300 rounded-lg overflow-x-auto leading-relaxed">
                {JSON.stringify(
                  {
                    action: 'CREATE_COMMUNICATION_IDENTITY_BINDING_V1',
                    channelFamily,
                    environment,
                    representedIdentifier,
                    authorityEvidence,
                    allowedActors: [allowedActor],
                    custodyClass,
                    permittedPurposes: [permittedPurpose],
                    initialLifecycleState:
                      channelFamily === 'stir-shaken' || channelFamily === 'bimi-mark'
                        ? 'PENDING_EXTERNAL_GOVERNANCE'
                        : 'ACTIVE',
                  },
                  null,
                  2
                )}
              </pre>

              <div className="p-3.5 rounded-lg bg-amber-50/80 dark:bg-amber-950/30 border border-amber-200 dark:border-amber-900 text-xs space-y-1.5">
                <div className="flex items-center gap-2 font-semibold text-amber-900 dark:text-amber-300">
                  <AlertTriangle className="w-4 h-4 shrink-0" />
                  <span>External Governance &amp; Ecosystem Authority Notice</span>
                </div>
                <p className="text-amber-800 dark:text-amber-300 leading-relaxed">
                  {preset.externalGovernanceCaveat}
                </p>
              </div>

              <label className="flex items-start gap-2.5 text-xs text-slate-700 dark:text-slate-300 cursor-pointer">
                <input
                  type="checkbox"
                  checked={governanceAck}
                  onChange={(e) => setGovernanceAck(e.target.checked)}
                  className="mt-0.5 rounded border-slate-300"
                />
                <span>
                  I approve this point-in-time communication identity binding and acknowledge that technical validation does not replace external authority or provider governance.
                </span>
              </label>
            </div>
          )}
        </div>

        <div className="flex items-center justify-between px-6 py-4 bg-slate-50 dark:bg-slate-950 border-t border-slate-200 dark:border-slate-800">
          {step > 1 ? (
            <button
              type="button"
              onClick={() => setStep((s) => (s - 1) as 1 | 2 | 3)}
              className="flex items-center gap-1.5 px-3 py-2 text-xs font-medium text-slate-700 dark:text-slate-300 bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-700 rounded-lg cursor-pointer"
            >
              <ArrowLeft className="w-3.5 h-3.5" />
              Previous Step
            </button>
          ) : (
            <div />
          )}

          {step < 3 ? (
            <button
              type="button"
              onClick={() => setStep((s) => (s + 1) as 1 | 2 | 3)}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 rounded-lg cursor-pointer"
            >
              Continue
              <ArrowRight className="w-3.5 h-3.5" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleSubmit}
              disabled={!governanceAck || submitting}
              className="flex items-center gap-1.5 px-4 py-2 text-xs font-medium text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50 rounded-lg cursor-pointer"
            >
              <CheckCircle2 className="w-3.5 h-3.5" />
              {submitting ? 'Registering Binding v1...' : 'Approve & Register Identity'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
};
