export type ChannelFamily =
  | 'stir-shaken'
  | 'bimi-mark'
  | 'smime'
  | 'document-signing'
  | 'webhook-http-sig';

export type VerificationStatus =
  | 'valid'
  | 'invalid'
  | 'indeterminate'
  | 'stale'
  | 'unsupported';

export type IdentityLifecycleStatus =
  | 'ACTIVE'
  | 'SUSPENDED'
  | 'PENDING_EXTERNAL_GOVERNANCE'
  | 'EXPIRED'
  | 'COMPROMISED';

export type CustodyClass =
  | 'HSM_FIPS_140_3_L3'
  | 'CLOUD_KMS_NON_EXPORTABLE'
  | 'REMOTE_QTSP_SAM'
  | 'EXTERNAL_STI_SIGNER';

export interface ChannelProfileSpec {
  id: string;
  family: ChannelFamily;
  version: string;
  title: string;
  standardReference: string;
  mediaType: string;
  conformanceStatus: 'IMPLEMENTED_PHASE_1' | 'IMPLEMENTED_PHASE_2' | 'IMPLEMENTED_PHASE_3' | 'IMPLEMENTED_PHASE_4';
  jurisdictionOrGovernance: string;
  trustRegistryScope: string;
  allowedAlgorithms: string[];
  defaultCustody: CustodyClass;
  whatItProves: string[];
  whatItDoesNotProve: string[];
  externalDependencies: string[];
  qualifiedVocabulary: {
    positiveLabel: string;
    degradedLabel: string;
    failedLabel: string;
    bannedTerms: string[];
  };
}

export interface AuthorityBindingVersion {
  bindingVersion: number;
  effectiveFrom: string;
  effectiveUntil: string | null;
  representedIdentifier: string;
  authorityEvidenceRef: string;
  verificationMethod: string;
  externalGovernanceAuthority: string;
  keyId: string;
  certificateFingerprint: string;
  statusAtVersion: IdentityLifecycleStatus;
  changeReason: string;
}

export interface CommunicationIdentity {
  id: string;
  tenantId: string;
  organization: string;
  ownerTeam: string;
  environment: 'production' | 'staging' | 'regulated-eu' | 'carrier-us-east';
  channelFamily: ChannelFamily;
  profileId: string;
  profileVersion: string;
  representedIdentifier: string;
  identifierType: 'TELEPHONE_RANGE' | 'DOMAIN' | 'MAILBOX' | 'DOCUMENT_ROLE' | 'WEBHOOK_SERVICE';
  authorityEvidence: string;
  verificationMethod: string;
  externalGovernanceStatus: string;
  allowedActors: string[];
  delegatedSigners: string[];
  signingKeyRef: string;
  certificateSerial: string;
  certificateFingerprint: string;
  custodyClass: CustodyClass;
  permittedPurposes: string[];
  assuranceRequirement: string;
  riskTier: 'CRITICAL_REGULATED' | 'HIGH_TRUST' | 'STANDARD_SERVICE';
  effectiveAt: string;
  renewalAt: string;
  expiresAt: string;
  status: IdentityLifecycleStatus;
  publicationStatus: string;
  p95LatencyMs: number;
  volume24h: number;
  failureRate24h: number;
  bindingHistory: AuthorityBindingVersion[];
}

export interface SignerCustodyRecord {
  id: string;
  keyId: string;
  tenantId: string;
  environment: string;
  channelFamily: ChannelFamily;
  boundIdentityId: string;
  profileId: string;
  purpose: 'VOICE_PASSPORT_SIGN' | 'BIMI_VMC_ASSERTION' | 'SMIME_CONTENT_SIGN' | 'SMIME_KEY_ENCIPHER' | 'PADES_DOC_SEAL' | 'HTTP_MSG_RFC9421';
  algorithm: string;
  custodyClass: CustodyClass;
  nonExportable: boolean;
  quorumRequired: boolean;
  rotationState: 'ACTIVE_PRIMARY' | 'STAGED_OVERLAP' | 'RETIRED_HISTORICAL_VERIFY_ONLY' | 'SUSPENDED_COMPROMISED';
  createdAt: string;
  expiresAt: string;
  certificateChainRef: string;
  publicJwkThumbprint: string;
}

export interface ProductPromiseAnswer {
  actorWhoRequested: string;
  representedEntity: string;
  authorityBasis: string;
  cryptographicallyCoveredFields: string[];
  certificateKeyTrustProfile: string;
  validityFreshnessReplayStatus: string;
  establishes: string[];
  doesNotEstablish: string[];
}

export interface VerificationLayerResult {
  layer:
    | 'PARSE_BOUNDS'
    | 'CANONICAL_RECONSTRUCTION'
    | 'TRUST_CHAIN_RESOLUTION'
    | 'CRYPTOGRAPHIC_SIGNATURE'
    | 'IDENTITY_AUTHORITY_BINDING'
    | 'TIME_STATUS_REVOCATION'
    | 'FRESHNESS_REPLAY_POLICY'
    | 'PROFILE_COMPONENT_POLICY';
  title: string;
  status: VerificationStatus;
  reasonCode: string;
  detail: string;
}

export interface EvidenceReceipt {
  assertionId: string;
  timestamp: string;
  channelFamily: ChannelFamily;
  profileId: string;
  profileVersion: string;
  tenantId: string;
  actorPrincipal: string;
  subjectIdentityId: string;
  representedIdentifier: string;
  authorityReference: string;
  policyDecisionId: string;
  inputContentDigestSha256: string;
  canonicalInputDigestSha256: string;
  signatureOutputDigestSha256: string;
  rawContentRetained: false;
  signingKeyId: string;
  certificateFingerprint: string;
  trustRegistrySnapshotId: string;
  algorithm: string;
  coveredComponents: string[];
  verificationStatus: VerificationStatus;
  authorizationOutcome: 'AUTHORIZED' | 'DENIED_POLICY' | 'DENIED_SUSPENDED_IDENTITY' | 'DENIED_KEY_PURPOSE_MISMATCH';
  qualifiedResultLabel: string;
  reasonCode: string;
  latencyMs: number;
  productPromise: ProductPromiseAnswer;
}

export interface StirShakenRecord {
  id: string;
  identityId: string;
  tnRange: string;
  ocnSpid: string;
  jurisdiction: 'US-FCC-STI-GA' | 'CA-CRTC-CSTGA';
  stiCaIssuer: string;
  certificateUrl: string;
  tnAuthListspc: string;
  defaultAttestationLevel: 'A' | 'B' | 'C';
  originationTrunkGroup: string;
  activePassportKid: string;
  rolloverStandbyKid: string;
  p95SignLatencyMs: number;
  callsSigned24h: number;
  robocallAnalyticsScore: string;
  status: IdentityLifecycleStatus;
}

export interface BimiDomainAssessment {
  id: string;
  identityId: string;
  domain: string;
  selector: string;
  dmarcPolicy: 'p=reject; pct=100' | 'p=quarantine; pct=100' | 'p=none (Blocker)';
  dmarcSatisfiesProfile: boolean;
  bimiDnsTxtRecord: string;
  dnsRecordValid: boolean;
  svgTinyPsStatus: 'VALID_TINY_PS' | 'INVALID_SCRIPT_DETECTED' | 'INVALID_EXTERNAL_REF' | 'MISSING_TITLE';
  svgReviewedSha256: string;
  markCertificateType: 'VMC (Registered Trademark)' | 'CMC (Common Mark)' | 'NONE';
  markCertificateIssuer: string;
  markCertificateValidAndBound: boolean;
  assetHostingHttpsHealth: 'HEALTHY_TLS13_200' | 'DEGRADED_LATENCY' | 'HASH_MISMATCH';
  mailboxProviderEligible: boolean;
  providerDisplayObservations: {
    provider: string;
    protocolEligible: boolean;
    observedLogoDisplayed: boolean;
    lastObservedAt: string;
    note: string;
  }[];
  blockers: string[];
}

export interface SmimeIdentityRecord {
  id: string;
  identityId: string;
  mailbox: string;
  signerClassification: 'ORGANIZATIONAL_ROLE' | 'PERSONAL_EMPLOYEE' | 'GATEWAY_MTA_SIGNER';
  signingCertSerial: string;
  encryptionCertSerial: string;
  separateKeysEnforced: boolean;
  escrowPolicy: 'NO_ESCROW_SIGNING_KEY' | 'DUAL_CUSTODY_ENC_ESCROW_APPROVED';
  supportedModes: ('SIGNED_ONLY_MULTIPART' | 'ENVELOPED_ONLY' | 'SIGNED_AND_ENVELOPED')[];
  coveredHeaders: string[];
  uncoveredVisibleFieldsWarning: string[];
  clientInteroperability: {
    client: string;
    cmsParsePass: boolean;
    headerProtectionRfc8551: boolean;
    notes: string;
  }[];
}

export interface DocumentCeremonyRecord {
  id: string;
  identityId: string;
  documentTitle: string;
  profileSpec: 'PAdES-B-LTA (ETSI EN 319 142-1)' | 'CAdES-B-LT' | 'XAdES-B-T';
  immutableDocumentBytesLen: number;
  documentDigestSha256: string;
  signerName: string;
  signerRole: string;
  organizationAuthority: string;
  declaredIntent: string;
  stepUpAuthMethod: string;
  tsaAuthority: string;
  ltvArchiveStatus: 'COMPLETE_OCSP_CRL_EMBEDDED' | 'TIMESTAMPED_ONLY' | 'PENDING_SECOND_SIGNER';
  multiSignerOrder: {
    step: number;
    role: string;
    actor: string;
    status: 'SIGNED_SEALED' | 'AWAITING_CEREMONY' | 'COUNTERSIGNED';
    signedAt: string | null;
    signatureDigest: string | null;
  }[];
  jurisdictionCaveat: string;
}

export interface WebhookProfileRecord {
  id: string;
  identityId: string;
  endpointPattern: string;
  keyId: string;
  stagedRotationKeyId: string | null;
  algorithm: 'ed25519' | 'ecdsa-p256-sha256' | 'hmac-sha256';
  coveredComponents: string[];
  maxValidityWindowSec: number;
  replayPolicy: 'NONCE_REDIS_STRICT_300S' | 'EVENT_ID_IDEMPOTENCY_24H';
  proxyCanonicalizationNote: string;
  verifierCacheTtlSec: number;
}

export interface ChannelIncident {
  id: string;
  severity: 'CRITICAL' | 'HIGH' | 'MODERATE';
  title: string;
  channelFamily: ChannelFamily;
  affectedIdentityId: string;
  affectedRepresentedIdentifier: string;
  affectedKeyId: string;
  status: 'ACTIVE_SUSPENDED' | 'CONTAINED_ROTATING' | 'RESOLVED_HISTORICAL_PRESERVED';
  detectedAt: string;
  summary: string;
  historicalVerificationRule: string;
  recommendedRecoverySteps: string[];
}
