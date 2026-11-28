import express from 'express';
import crypto from 'node:crypto';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
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
} from './src/data/seedControlPlane.ts';
import type {
  CommunicationIdentity,
  EvidenceReceipt,
  VerificationLayerResult,
  VerificationStatus,
  ChannelFamily,
} from './src/types/communications.ts';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.json({ limit: '256kb' }));

// In-memory stateful stores initialized from seed data
const identitiesStore: CommunicationIdentity[] = structuredClone(INITIAL_IDENTITIES);
const signersStore = structuredClone(SIGNER_CUSTODY_RECORDS);
const stirStore = structuredClone(STIR_SHAKEN_RECORDS);
const bimiStore = structuredClone(BIMI_DOMAIN_ASSESSMENTS);
const smimeStore = structuredClone(SMIME_IDENTITY_RECORDS);
const docStore = structuredClone(DOCUMENT_CEREMONY_RECORDS);
const webhookStore = structuredClone(WEBHOOK_PROFILE_RECORDS);
const evidenceStore: EvidenceReceipt[] = structuredClone(INITIAL_EVIDENCE_RECEIPTS);
const incidentsStore = structuredClone(INITIAL_INCIDENTS);

// Non-exportable server-side HSM key material simulation (never returned in API responses)
const SERVER_CUSTODY_SECRET = crypto.randomBytes(32).toString('hex');
const seenReplayNonces = new Set<string>(['nonce-replayed-demo-001']);

function sha256Hex(input: string): string {
  return crypto.createHash('sha256').update(input, 'utf8').digest('hex');
}

function sha256Base64(input: string): string {
  return crypto.createHash('sha256').update(input, 'utf8').digest('base64');
}

function hsmSignDigest(keyId: string, canonicalInput: string): string {
  return crypto
    .createHmac('sha256', `${SERVER_CUSTODY_SECRET}:${keyId}`)
    .update(canonicalInput, 'utf8')
    .digest('base64');
}

// 1. Profiles & Conformance Status
app.get('/api/v1/profiles', (_req, res) => {
  res.json({
    profiles: CHANNEL_PROFILES,
    repositoryFoundations: {
      certificateCenter: 'CONNECTED_CA_LIFECYCLE_OCSP_CRL',
      trustRegistry: 'POINT_IN_TIME_RESOLUTION_ACTIVE',
      joseCrypto: 'HSM_KMS_BOUNDARY_ENFORCED',
      attestationCenter: 'WORKLOAD_AND_MVA_APPRAISAL_READY',
      securitySignals: 'SHARED_SIGNAL_STREAM_ENABLED',
    },
  });
});

// 2. Communication Identities & Point-in-Time Bindings
app.get('/api/v1/communication-identities', (_req, res) => {
  res.json({ identities: identitiesStore });
});

app.post('/api/v1/communication-identities', (req, res) => {
  const {
    organization,
    ownerTeam,
    environment,
    channelFamily,
    representedIdentifier,
    identifierType,
    authorityEvidence,
    verificationMethod,
    allowedActor,
    custodyClass,
    permittedPurpose,
    assuranceRequirement,
  } = req.body;

  if (!representedIdentifier || !channelFamily || !authorityEvidence) {
    res.status(400).json({ error: 'Missing required identity binding fields.' });
    return;
  }

  const profile = CHANNEL_PROFILES.find((p) => p.family === channelFamily) || CHANNEL_PROFILES[0];
  const nowIso = new Date().toISOString();
  const keyId = `key-${channelFamily}-${crypto.randomBytes(3).toString('hex')}`;
  const certFp = `SHA256:${sha256Hex(`${representedIdentifier}:${keyId}:${nowIso}`)}`;
  const newId = `cid-${channelFamily}-${crypto.randomBytes(2).toString('hex')}`;

  const newIdentity: CommunicationIdentity = {
    id: newId,
    tenantId: 'tnt-meridian-fin',
    organization: organization || 'Meridian Global Treasury Ltd.',
    ownerTeam: ownerTeam || 'Communications Security Admin',
    environment: environment || 'production',
    channelFamily,
    profileId: profile.id,
    profileVersion: profile.version,
    representedIdentifier,
    identifierType: identifierType || 'WEBHOOK_SERVICE',
    authorityEvidence,
    verificationMethod: verificationMethod || 'DNS-01 + Workload Attestation',
    externalGovernanceStatus:
      channelFamily === 'stir-shaken' || channelFamily === 'bimi-mark' || channelFamily === 'document-signing'
        ? 'Technical Binding Ready · External Authority Approval Pending'
        : 'Active in Federation Trust Registry',
    allowedActors: [allowedActor || 'svc-automated-dispatcher@meridian.internal'],
    delegatedSigners: [],
    signingKeyRef: `hsm://custody-vault/${keyId}`,
    certificateSerial: crypto.randomBytes(8).toString('hex').toUpperCase().match(/.{1,2}/g)!.join(':'),
    certificateFingerprint: certFp,
    custodyClass: custodyClass || profile.defaultCustody,
    permittedPurposes: [permittedPurpose || 'CHANNEL_DEFAULT_ASSERTION'],
    assuranceRequirement: assuranceRequirement || 'STEP_UP_OR_WORKLOAD_ATTESTATION',
    riskTier: 'HIGH_TRUST',
    effectiveAt: nowIso,
    renewalAt: '2027-10-01T00:00:00Z',
    expiresAt: '2027-11-09T00:00:00Z',
    status:
      channelFamily === 'stir-shaken' || channelFamily === 'bimi-mark'
        ? 'PENDING_EXTERNAL_GOVERNANCE'
        : 'ACTIVE',
    publicationStatus: 'Initial Binding v1 Recorded · Discovery Metadata Staged',
    p95LatencyMs: 3.5,
    volume24h: 0,
    failureRate24h: 0,
    bindingHistory: [
      {
        bindingVersion: 1,
        effectiveFrom: nowIso,
        effectiveUntil: null,
        representedIdentifier,
        authorityEvidenceRef: `ev-${crypto.randomBytes(3).toString('hex')}`,
        verificationMethod: verificationMethod || 'Channel Onboarding Wizard Verification',
        externalGovernanceAuthority: profile.jurisdictionOrGovernance,
        keyId,
        certificateFingerprint: certFp,
        statusAtVersion:
          channelFamily === 'stir-shaken' || channelFamily === 'bimi-mark'
            ? 'PENDING_EXTERNAL_GOVERNANCE'
            : 'ACTIVE',
        changeReason: 'Initial identity onboarding via Channel Wizard',
      },
    ],
  };

  identitiesStore.unshift(newIdentity);
  res.status(201).json({ identity: newIdentity });
});

app.patch('/api/v1/communication-identities/:id/status', (req, res) => {
  const { id } = req.params;
  const { action, reason } = req.body as {
    action: 'SUSPEND' | 'ACTIVATE' | 'ROTATE_KEY';
    reason?: string;
  };

  const identity = identitiesStore.find((item) => item.id === id);
  if (!identity) {
    res.status(404).json({ error: 'Communication identity not found.' });
    return;
  }

  const nowIso = new Date().toISOString();
  const currentVersion = identity.bindingHistory[0];
  if (currentVersion) {
    currentVersion.effectiveUntil = nowIso;
  }

  const nextVersionNumber = (currentVersion?.bindingVersion || 1) + 1;
  let nextKeyId = currentVersion?.keyId || 'key-default';
  let nextCertFp = identity.certificateFingerprint;

  if (action === 'SUSPEND') {
    identity.status = 'SUSPENDED';
    identity.publicationStatus = 'Suspended via Control Plane · New Signing Blocked';
  } else if (action === 'ACTIVATE') {
    identity.status = 'ACTIVE';
    identity.publicationStatus = 'Active & Synchronized in Trust Registry';
  } else if (action === 'ROTATE_KEY') {
    nextKeyId = `key-${identity.channelFamily}-rotv${nextVersionNumber}-${crypto.randomBytes(2).toString('hex')}`;
    nextCertFp = `SHA256:${sha256Hex(`${identity.id}:${nextKeyId}:${nowIso}`)}`;
    identity.signingKeyRef = `hsm://custody-vault/${nextKeyId}`;
    identity.certificateFingerprint = nextCertFp;
    identity.publicationStatus = `Rotated to ${nextKeyId} (24h Verifier Overlap Active)`;
  }

  identity.bindingHistory.unshift({
    bindingVersion: nextVersionNumber,
    effectiveFrom: nowIso,
    effectiveUntil: null,
    representedIdentifier: identity.representedIdentifier,
    authorityEvidenceRef: currentVersion?.authorityEvidenceRef || 'ev-binding-update',
    verificationMethod: identity.verificationMethod,
    externalGovernanceAuthority: currentVersion?.externalGovernanceAuthority || 'Trust Registry',
    keyId: nextKeyId,
    certificateFingerprint: nextCertFp,
    statusAtVersion: identity.status,
    changeReason:
      reason ||
      (action === 'ROTATE_KEY'
        ? 'Point-in-time key rotation; prior binding version preserved for historical verification'
        : `Operator state change to ${identity.status}`),
  });

  res.json({ identity });
});

// 3. Signers & Custody Boundary
app.get('/api/v1/signers', (_req, res) => {
  res.json({
    signers: signersStore,
    custodyPolicySummary: {
      privateKeyExportAllowed: false,
      oauthJwtKeyReuseProhibited: true,
      tenantEnvironmentChannelIsolation: 'STRICT_ENFORCED',
    },
  });
});

// 4. Shared Profile-Driven Signing Pipeline (/api/v1/sign)
app.post('/api/v1/sign', (req, res) => {
  const {
    identityId,
    actorPrincipal,
    purpose,
    payloadSummary,
    coveredComponents,
    attemptCrossPurposeKeyMisuse,
  } = req.body as {
    identityId: string;
    actorPrincipal: string;
    purpose: string;
    payloadSummary: string;
    coveredComponents?: string[];
    attemptCrossPurposeKeyMisuse?: boolean;
  };

  const identity = identitiesStore.find((i) => i.id === identityId);
  if (!identity) {
    res.status(404).json({ error: 'Communication identity not found.' });
    return;
  }

  const profile = CHANNEL_PROFILES.find((p) => p.id === identity.profileId) || CHANNEL_PROFILES[0];
  const nowIso = new Date().toISOString();
  const inputDigest = `SHA256:${sha256Hex(payloadSummary || 'empty-payload')}`;
  const keyId = identity.bindingHistory[0]?.keyId || 'key-unknown';

  // Check 1: Identity active status
  if (identity.status !== 'ACTIVE') {
    const deniedReceipt: EvidenceReceipt = {
      assertionId: `asn-denied-${crypto.randomBytes(3).toString('hex')}`,
      timestamp: nowIso,
      channelFamily: identity.channelFamily,
      profileId: identity.profileId,
      profileVersion: identity.profileVersion,
      tenantId: identity.tenantId,
      actorPrincipal,
      subjectIdentityId: identity.id,
      representedIdentifier: identity.representedIdentifier,
      authorityReference: `binding-v${identity.bindingHistory[0]?.bindingVersion || 1}`,
      policyDecisionId: `pdp-deny-status-${crypto.randomBytes(2).toString('hex')}`,
      inputContentDigestSha256: inputDigest,
      canonicalInputDigestSha256: 'NONE',
      signatureOutputDigestSha256: 'NONE',
      rawContentRetained: false,
      signingKeyId: keyId,
      certificateFingerprint: identity.certificateFingerprint,
      trustRegistrySnapshotId: `tr-snap-${nowIso.slice(0, 10)}`,
      algorithm: profile.allowedAlgorithms[0],
      coveredComponents: [],
      verificationStatus: 'invalid',
      authorizationOutcome: 'DENIED_SUSPENDED_IDENTITY',
      qualifiedResultLabel: `Signing Denied · Identity Status is ${identity.status}`,
      reasonCode: `ERR_IDENTITY_${identity.status}`,
      latencyMs: 0.7,
      productPromise: {
        actorWhoRequested: actorPrincipal,
        representedEntity: identity.representedIdentifier,
        authorityBasis: `DENIED — Identity status is ${identity.status}`,
        cryptographicallyCoveredFields: [],
        certificateKeyTrustProfile: `${keyId} (${identity.custodyClass}) — Not Invoked`,
        validityFreshnessReplayStatus: 'Rejected before cryptographic signing',
        establishes: ['Suspended, pending, or expired identities cannot emit new signatures.'],
        doesNotEstablish: ['No signature was created.'],
      },
    };
    evidenceStore.unshift(deniedReceipt);
    res.status(403).json({
      authorized: false,
      receipt: deniedReceipt,
    });
    return;
  }

  // Check 2: Cross-purpose / OAuth JWT key misuse check
  if (attemptCrossPurposeKeyMisuse) {
    const misuseReceipt: EvidenceReceipt = {
      assertionId: `asn-denied-${crypto.randomBytes(3).toString('hex')}`,
      timestamp: nowIso,
      channelFamily: identity.channelFamily,
      profileId: identity.profileId,
      profileVersion: identity.profileVersion,
      tenantId: identity.tenantId,
      actorPrincipal,
      subjectIdentityId: identity.id,
      representedIdentifier: identity.representedIdentifier,
      authorityReference: 'DENIED_CROSS_PROTOCOL_KEY_CONFUSION',
      policyDecisionId: `pdp-deny-keypurpose-${crypto.randomBytes(2).toString('hex')}`,
      inputContentDigestSha256: inputDigest,
      canonicalInputDigestSha256: 'NONE',
      signatureOutputDigestSha256: 'NONE',
      rawContentRetained: false,
      signingKeyId: 'oauth-jwt-general-key-blocked',
      certificateFingerprint: identity.certificateFingerprint,
      trustRegistrySnapshotId: `tr-snap-${nowIso.slice(0, 10)}`,
      algorithm: profile.allowedAlgorithms[0],
      coveredComponents: [],
      verificationStatus: 'invalid',
      authorizationOutcome: 'DENIED_KEY_PURPOSE_MISMATCH',
      qualifiedResultLabel: 'Signing Denied · Cross-Protocol Key Purpose Violation',
      reasonCode: 'ERR_OAUTH_JWT_KEY_REUSE_PROHIBITED',
      latencyMs: 0.6,
      productPromise: {
        actorWhoRequested: actorPrincipal,
        representedEntity: identity.representedIdentifier,
        authorityBasis: 'DENIED — Attempted to sign communications payload with a general OAuth/JWT key or mismatched channel purpose',
        cryptographicallyCoveredFields: [],
        certificateKeyTrustProfile: 'Signing boundary rejected key purpose mismatch',
        validityFreshnessReplayStatus: 'No signature emitted',
        establishes: ['Domain-separated signing boundary prevented cross-protocol key confusion.'],
        doesNotEstablish: ['No cryptographic assertion was emitted.'],
      },
    };
    evidenceStore.unshift(misuseReceipt);
    res.status(403).json({
      authorized: false,
      receipt: misuseReceipt,
    });
    return;
  }

  // Check 3: Actor authorization
  const isActorAllowed =
    identity.allowedActors.includes(actorPrincipal) ||
    identity.delegatedSigners.includes(actorPrincipal);

  if (!isActorAllowed) {
    const unauthorizedReceipt: EvidenceReceipt = {
      assertionId: `asn-denied-${crypto.randomBytes(3).toString('hex')}`,
      timestamp: nowIso,
      channelFamily: identity.channelFamily,
      profileId: identity.profileId,
      profileVersion: identity.profileVersion,
      tenantId: identity.tenantId,
      actorPrincipal,
      subjectIdentityId: identity.id,
      representedIdentifier: identity.representedIdentifier,
      authorityReference: 'NONE_ACTOR_NOT_BOUND',
      policyDecisionId: `pdp-deny-actor-${crypto.randomBytes(2).toString('hex')}`,
      inputContentDigestSha256: inputDigest,
      canonicalInputDigestSha256: 'NONE',
      signatureOutputDigestSha256: 'NONE',
      rawContentRetained: false,
      signingKeyId: keyId,
      certificateFingerprint: identity.certificateFingerprint,
      trustRegistrySnapshotId: `tr-snap-${nowIso.slice(0, 10)}`,
      algorithm: profile.allowedAlgorithms[0],
      coveredComponents: [],
      verificationStatus: 'invalid',
      authorizationOutcome: 'DENIED_POLICY',
      qualifiedResultLabel: 'Signing Denied · Actor Not Authorized For Identity',
      reasonCode: 'ERR_ACTOR_NOT_IN_ALLOWED_BINDING',
      latencyMs: 0.9,
      productPromise: {
        actorWhoRequested: actorPrincipal,
        representedEntity: identity.representedIdentifier,
        authorityBasis: `DENIED — Actor "${actorPrincipal}" is not authorized under ${identity.id}`,
        cryptographicallyCoveredFields: [],
        certificateKeyTrustProfile: `${keyId} — Protected by Signer Authorization Policy`,
        validityFreshnessReplayStatus: 'Rejected prior to key custody invocation',
        establishes: ['Unauthorized workload or user was blocked from asserting the communication identity.'],
        doesNotEstablish: ['No signature was created.'],
      },
    };
    evidenceStore.unshift(unauthorizedReceipt);
    res.status(403).json({
      authorized: false,
      receipt: unauthorizedReceipt,
    });
    return;
  }

  // Authorized: construct canonical input and sign via server-side custody
  const components =
    coveredComponents && coveredComponents.length > 0
      ? coveredComponents
      : ['@method', '@target-uri', '@authority', 'content-digest', 'x-tba-timestamp'];
  const canonicalInput = [
    `profile=${profile.id}@${profile.version}`,
    `identity=${identity.representedIdentifier}`,
    `actor=${actorPrincipal}`,
    `purpose=${purpose || identity.permittedPurposes[0]}`,
    `digest=${inputDigest}`,
    `components=${components.join(',')}`,
    `ts=${nowIso}`,
  ].join('\n');

  const canonicalDigest = `SHA256:${sha256Hex(canonicalInput)}`;
  const rawSignature = hsmSignDigest(keyId, canonicalInput);
  const sigOutputDigest = `SHA256:${sha256Hex(rawSignature)}`;

  const validReceipt: EvidenceReceipt = {
    assertionId: `asn-${identity.channelFamily}-${crypto.randomBytes(3).toString('hex')}`,
    timestamp: nowIso,
    channelFamily: identity.channelFamily,
    profileId: identity.profileId,
    profileVersion: identity.profileVersion,
    tenantId: identity.tenantId,
    actorPrincipal,
    subjectIdentityId: identity.id,
    representedIdentifier: identity.representedIdentifier,
    authorityReference: `binding-v${identity.bindingHistory[0]?.bindingVersion || 1}:${identity.bindingHistory[0]?.authorityEvidenceRef || 'ev-active'}`,
    policyDecisionId: `pdp-allow-${crypto.randomBytes(3).toString('hex')}`,
    inputContentDigestSha256: inputDigest,
    canonicalInputDigestSha256: canonicalDigest,
    signatureOutputDigestSha256: sigOutputDigest,
    rawContentRetained: false,
    signingKeyId: keyId,
    certificateFingerprint: identity.certificateFingerprint,
    trustRegistrySnapshotId: `tr-snap-${nowIso.slice(0, 10)}`,
    algorithm: profile.allowedAlgorithms[0],
    coveredComponents: components,
    verificationStatus: 'valid',
    authorizationOutcome: 'AUTHORIZED',
    qualifiedResultLabel: profile.qualifiedVocabulary.positiveLabel,
    reasonCode: 'SIGNED_AND_EVIDENCE_RECORDED',
    latencyMs: identity.p95LatencyMs,
    productPromise: {
      actorWhoRequested: `${actorPrincipal} (Tenant ${identity.tenantId})`,
      representedEntity: `${identity.representedIdentifier} (${identity.organization})`,
      authorityBasis: `${identity.authorityEvidence} · Purpose: ${purpose || identity.permittedPurposes[0]}`,
      cryptographicallyCoveredFields: components,
      certificateKeyTrustProfile: `Key ${keyId} (${identity.custodyClass}) · Cert ${identity.certificateSerial} · Profile ${profile.id}`,
      validityFreshnessReplayStatus: `Valid at ${nowIso} · Bound to digest ${inputDigest.slice(0, 24)}...`,
      establishes: profile.whatItProves,
      doesNotEstablish: profile.whatItDoesNotProve,
    },
  };

  identity.volume24h += 1;
  evidenceStore.unshift(validReceipt);

  res.json({
    authorized: true,
    canonicalInput,
    detachedSignatureBase64: rawSignature,
    receipt: validReceipt,
  });
});

// 5. Layered Verification Workbench (/api/v1/verify)
app.post('/api/v1/verify', (req, res) => {
  const {
    channelFamily,
    identityId,
    scenarioMode,
    pointInTimeTimestamp,
    coveredComponents,
    nonceValue,
  } = req.body as {
    channelFamily: ChannelFamily;
    identityId: string;
    scenarioMode:
      | 'NOMINAL_VALID'
      | 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS'
      | 'REPLAY_DETECTED'
      | 'POINT_IN_TIME_HISTORICAL_VALID'
      | 'BYTE_OR_HEADER_TAMPERED'
      | 'TRUST_STATUS_INDETERMINATE';
    pointInTimeTimestamp?: string;
    coveredComponents?: string[];
    nonceValue?: string;
  };

  const identity =
    identitiesStore.find((i) => i.id === identityId) ||
    identitiesStore.find((i) => i.channelFamily === channelFamily) ||
    identitiesStore[0];
  const profile =
    CHANNEL_PROFILES.find((p) => p.family === (channelFamily || identity.channelFamily)) ||
    CHANNEL_PROFILES[0];

  const layers: VerificationLayerResult[] = [
    {
      layer: 'PARSE_BOUNDS',
      title: '1. Syntax, Media-Type & Strict Size Bounds',
      status: 'valid',
      reasonCode: 'PARSE_BOUND_OK',
      detail: `Artifact parsed cleanly under ${profile.mediaType} within strict 64KB header/envelope bounds.`,
    },
    {
      layer: 'CANONICAL_RECONSTRUCTION',
      title: '2. Profile-Native Canonical Input Reconstruction',
      status: scenarioMode === 'BYTE_OR_HEADER_TAMPERED' ? 'invalid' : 'valid',
      reasonCode:
        scenarioMode === 'BYTE_OR_HEADER_TAMPERED'
          ? 'ERR_CANONICAL_DIGEST_MISMATCH'
          : 'CANONICAL_BASE_MATCHED',
      detail:
        scenarioMode === 'BYTE_OR_HEADER_TAMPERED'
          ? 'Reconstructed content-digest / MIME body hash does NOT match the signed digest attribute (post-signing mutation detected).'
          : `Reconstructed canonical signing base for ${profile.id} matches signed digest bytes.`,
    },
    {
      layer: 'TRUST_CHAIN_RESOLUTION',
      title: '3. Key, Certificate Chain & Point-in-Time Trust Registry',
      status: scenarioMode === 'TRUST_STATUS_INDETERMINATE' ? 'indeterminate' : 'valid',
      reasonCode:
        scenarioMode === 'TRUST_STATUS_INDETERMINATE'
          ? 'WARN_OCSP_RESPONDER_TIMEOUT'
          : 'TRUST_ANCHOR_RESOLVED',
      detail:
        scenarioMode === 'POINT_IN_TIME_HISTORICAL_VALID'
          ? `Resolved historical Binding v1 key (${identity.bindingHistory[identity.bindingHistory.length - 1]?.keyId}) active at ${pointInTimeTimestamp || '2026-05-15T12:00:00Z'} under ${profile.trustRegistryScope}.`
          : scenarioMode === 'TRUST_STATUS_INDETERMINATE'
          ? 'Leaf certificate chains to recognized root, but external OCSP/STI-CRL status source timed out; failing safe as indeterminate.'
          : `Resolved active certificate ${identity.certificateSerial} under ${profile.trustRegistryScope}.`,
    },
    {
      layer: 'CRYPTOGRAPHIC_SIGNATURE',
      title: '4. Cryptographic Signature & Algorithm Policy',
      status: scenarioMode === 'BYTE_OR_HEADER_TAMPERED' ? 'invalid' : 'valid',
      reasonCode:
        scenarioMode === 'BYTE_OR_HEADER_TAMPERED'
          ? 'ERR_SIGNATURE_VERIFICATION_FAILED'
          : 'CRYPTO_SIG_VALID',
      detail:
        scenarioMode === 'BYTE_OR_HEADER_TAMPERED'
          ? `Signature verification failed under ${profile.allowedAlgorithms[0]} over mutated payload bytes.`
          : `Mathematical signature verified with ${profile.allowedAlgorithms[0]} using public key thumbprint.`,
    },
    {
      layer: 'IDENTITY_AUTHORITY_BINDING',
      title: '5. Represented Identity & Authority Binding',
      status: 'valid',
      reasonCode: 'IDENTITY_BINDING_ACTIVE_AT_SIGNING',
      detail: `Signer key is cryptographically bound to ${identity.representedIdentifier} with verified authority (${identity.authorityEvidence}).`,
    },
    {
      layer: 'TIME_STATUS_REVOCATION',
      title: '6. Effective Window, Expiry & Revocation Status',
      status: scenarioMode === 'TRUST_STATUS_INDETERMINATE' ? 'indeterminate' : 'valid',
      reasonCode:
        scenarioMode === 'TRUST_STATUS_INDETERMINATE'
          ? 'STATUS_SOURCE_UNAVAILABLE'
          : 'CERT_AND_BINDING_NOT_REVOKED',
      detail:
        scenarioMode === 'POINT_IN_TIME_HISTORICAL_VALID'
          ? 'Evaluated at historical signature timestamp: certificate and binding were active and non-compromised at creation time.'
          : 'Signing timestamp falls within certificate and authority binding validity window.',
    },
    {
      layer: 'FRESHNESS_REPLAY_POLICY',
      title: '7. Freshness Window, Nonce & Replay State',
      status: scenarioMode === 'REPLAY_DETECTED' ? 'stale' : 'valid',
      reasonCode:
        scenarioMode === 'REPLAY_DETECTED'
          ? 'ERR_NONCE_ALREADY_CONSUMED'
          : 'FRESHNESS_AND_NONCE_OK',
      detail:
        scenarioMode === 'REPLAY_DETECTED'
          ? `Nonce "${nonceValue || 'nonce-replayed-demo-001'}" was already observed within the 300s replay window. Cryptographic signature is valid, but transaction is rejected as a replay.`
          : 'Creation timestamp is fresh and nonce/origid is unique in the replay state store.',
    },
    {
      layer: 'PROFILE_COMPONENT_POLICY',
      title: '8. Covered Component & Channel Policy Conformance',
      status:
        scenarioMode === 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS' ? 'invalid' : 'valid',
      reasonCode:
        scenarioMode === 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS'
          ? 'ERR_REQUIRED_COMPONENT_OMITTED'
          : 'PROFILE_COVERAGE_COMPLETE',
      detail:
        scenarioMode === 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS'
          ? 'Cryptographic signature is mathematically valid over (@method, @target-uri), but omits mandatory "content-digest" and "@authority" required by profile policy.'
          : 'All mandatory profile components and claims are covered by the signature.',
    },
  ];

  let overallStatus: VerificationStatus = 'valid';
  let qualifiedHeadline = profile.qualifiedVocabulary.positiveLabel;

  if (scenarioMode === 'BYTE_OR_HEADER_TAMPERED') {
    overallStatus = 'invalid';
    qualifiedHeadline = profile.qualifiedVocabulary.failedLabel;
  } else if (scenarioMode === 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS') {
    overallStatus = 'invalid';
    qualifiedHeadline = 'Cryptographically Valid · Policy Invalid (Insufficient Covered Components)';
  } else if (scenarioMode === 'REPLAY_DETECTED') {
    overallStatus = 'stale';
    qualifiedHeadline = 'Signature Mathematically Valid · Rejected as Stale/Replayed Artifact';
  } else if (scenarioMode === 'TRUST_STATUS_INDETERMINATE') {
    overallStatus = 'indeterminate';
    qualifiedHeadline = 'Validation Indeterminate · External Revocation/Status Source Unreachable';
  } else if (scenarioMode === 'POINT_IN_TIME_HISTORICAL_VALID') {
    overallStatus = 'valid';
    qualifiedHeadline = 'Historical Artifact Valid Under Point-in-Time Binding Resolution';
  }

  const effectiveCovered =
    scenarioMode === 'CRYPTO_VALID_POLICY_INSUFFICIENT_COMPONENTS'
      ? ['@method', '@target-uri']
      : coveredComponents || ['@method', '@target-uri', '@authority', 'content-digest', 'x-tba-event-id'];

  res.json({
    overallStatus,
    cryptographicValidity: scenarioMode === 'BYTE_OR_HEADER_TAMPERED' ? 'INVALID' : 'VALID',
    policyAndAuthorityValidity:
      scenarioMode === 'NOMINAL_VALID' || scenarioMode === 'POINT_IN_TIME_HISTORICAL_VALID'
        ? 'VALID_AUTHORIZED'
        : scenarioMode === 'TRUST_STATUS_INDETERMINATE'
        ? 'INDETERMINATE_EXTERNAL_DEPENDENCY'
        : 'POLICY_OR_REPLAY_REJECTED',
    qualifiedHeadline,
    profileId: profile.id,
    profileVersion: profile.version,
    representedIdentifier: identity.representedIdentifier,
    coveredComponents: effectiveCovered,
    layers,
    productPromise: {
      actorWhoRequested: identity.allowedActors[0] || 'Authorized Workload',
      representedEntity: `${identity.representedIdentifier} (${identity.organization})`,
      authorityBasis: identity.authorityEvidence,
      cryptographicallyCoveredFields: effectiveCovered,
      certificateKeyTrustProfile: `${identity.signingKeyRef} · ${profile.id} (${profile.version})`,
      validityFreshnessReplayStatus: `${overallStatus.toUpperCase()} — ${
        layers.find((l) => l.status !== 'valid')?.detail ||
        'All cryptographic, authority, freshness, and component policies satisfied.'
      }`,
      establishes: profile.whatItProves,
      doesNotEstablish: profile.whatItDoesNotProve,
    },
  });
});

// 6. Voice Identity Center (STIR/SHAKEN)
app.get('/api/v1/telephone-identities', (_req, res) => {
  res.json({ records: stirStore });
});

app.post('/api/v1/telephone-identities/test-call', (req, res) => {
  const { recordId, origTn, destTn, attestationOverride, simulateTransitStrip } = req.body as {
    recordId: string;
    origTn: string;
    destTn: string;
    attestationOverride?: 'A' | 'B' | 'C';
    simulateTransitStrip?: boolean;
  };

  const record = stirStore.find((r) => r.id === recordId) || stirStore[0];
  const attest = attestationOverride || record.defaultAttestationLevel;
  const iat = Math.floor(Date.now() / 1000);
  const origid = `orig-${crypto.randomBytes(6).toString('hex')}`;

  const passportHeader = {
    alg: 'ES256',
    ppt: 'shaken',
    typ: 'passport',
    x5u: record.certificateUrl,
  };

  const passportPayload = {
    attest,
    dest: { tn: [destTn || '+12125550999'] },
    iat,
    orig: { tn: origTn || '+12125550142' },
    origid,
  };

  const encodedHeader = Buffer.from(JSON.stringify(passportHeader)).toString('base64url');
  const encodedPayload = Buffer.from(JSON.stringify(passportPayload)).toString('base64url');
  const sig = Buffer.from(
    hsmSignDigest(record.activePassportKid, `${encodedHeader}.${encodedPayload}`)
  ).toString('base64url');

  const sipIdentityHeader = simulateTransitStrip
    ? '[STRIPPED BY INTERMEDIATE TDM TRANSIT CARRIER — NO SIP IDENTITY HEADER PRESENT]'
    : `Identity: ${encodedHeader}.${encodedPayload}.${sig};info=<${record.certificateUrl}>;alg=ES256;ppt=shaken`;

  const attestationMeaning =
    attest === 'A'
      ? 'Full Attestation (A): Originating carrier authenticated the customer trunk and verified explicit authority to use this telephone number.'
      : attest === 'B'
      ? 'Partial Attestation (B): Originating carrier authenticated the enterprise customer trunk, but could not verify per-number authorization.'
      : 'Gateway Attestation (C): Originating gateway received the call from an international or non-IP interconnect without number authority proof; origid recorded for traceback.';

  res.json({
    verificationStatus: simulateTransitStrip ? 'indeterminate' : 'valid',
    qualifiedResultLabel: simulateTransitStrip
      ? 'No PASSporT Received · Intermediate Transit Stripped SIP Identity Header'
      : `PASSporT Valid · SHAKEN Attestation Level ${attest}`,
    passportHeader,
    passportPayload,
    sipIdentityHeader,
    attestationMeaning,
    separateRobocallSignal: record.robocallAnalyticsScore,
    whatItDoesNotProve: [
      'Attestation level does NOT prove the spoken conversation is truthful, wanted, or harmless.',
      'Does NOT override independent behavioral robocall/spam analytics.',
    ],
  });
});

// 7. Brand & Email Identity Center (BIMI + S/MIME)
app.get('/api/v1/email-identities', (_req, res) => {
  res.json({
    bimiAssessments: bimiStore,
    smimeRecords: smimeStore,
  });
});

app.post('/api/v1/email-identities/bimi-lint', (req, res) => {
  const { domain, dmarcRecord, bimiTxtRecord, svgMarkup } = req.body as {
    domain: string;
    dmarcRecord: string;
    bimiTxtRecord: string;
    svgMarkup: string;
  };

  const issues: string[] = [];
  const dmarcLower = (dmarcRecord || '').toLowerCase();
  const dmarcEnforced =
    (dmarcLower.includes('p=reject') || dmarcLower.includes('p=quarantine')) &&
    !dmarcLower.includes('pct=50');

  if (!dmarcEnforced) {
    issues.push(
      'DMARC Readiness Blocker: Organizational domain must enforce p=quarantine (with pct=100) or p=reject.'
    );
  }

  const bimiValidSyntax =
    (bimiTxtRecord || '').startsWith('v=BIMI1;') && (bimiTxtRecord || '').includes('l=https://');
  if (!bimiValidSyntax) {
    issues.push('BIMI DNS Blocker: TXT record must start with "v=BIMI1;" and provide an HTTPS "l=" SVG URI.');
  }

  // Untrusted SVG Tiny P/S security scanner
  const svgStr = svgMarkup || '';
  let svgStatus: 'VALID_TINY_PS' | 'INVALID_SCRIPT_DETECTED' | 'INVALID_EXTERNAL_REF' | 'MISSING_TITLE' =
    'VALID_TINY_PS';

  if (/<script|onload=|onerror=|javascript:/i.test(svgStr)) {
    svgStatus = 'INVALID_SCRIPT_DETECTED';
    issues.push(
      'SVG Security Violation: Active scripting (<script> or event handler) detected in untrusted SVG. Rejected before rendering.'
    );
  } else if (/xlink:href=["']https?:\/\/|href=["']https?:\/\//i.test(svgStr)) {
    svgStatus = 'INVALID_EXTERNAL_REF';
    issues.push(
      'SVG Tiny P/S Violation: External network reference (http/https href) detected. SVG Tiny P/S must be 100% self-contained.'
    );
  } else if (!/<title>.*<\/title>/i.test(svgStr) || !/baseProfile=["']tiny-ps["']/i.test(svgStr)) {
    svgStatus = 'MISSING_TITLE';
    issues.push(
      'SVG Tiny P/S Conformance: SVG root must declare baseProfile="tiny-ps" and include a non-empty <title> element.'
    );
  }

  const svgDigest = `SHA256:${sha256Hex(svgStr)}`;
  const protocolReady = dmarcEnforced && bimiValidSyntax && svgStatus === 'VALID_TINY_PS';

  res.json({
    domain: domain || 'meridiantreasury.com',
    protocolReady,
    qualifiedResultLabel: protocolReady
      ? 'BIMI Protocol Ready · VMC/SVG Digest Verified (External Provider Display Separate)'
      : 'BIMI Readiness Blocked · Fix Protocol or SVG Tiny P/S Violations',
    checks: {
      dmarcEnforced,
      bimiValidSyntax,
      svgStatus,
      svgReviewedDigest: svgDigest,
      mailboxProviderEligible: protocolReady,
      logoDisplayGuaranteed: false,
    },
    issues,
    providerCaveat:
      'Passing BIMI protocol and VMC checks makes the domain eligible for brand display, but each mailbox provider independently controls whether the logo is rendered based on sender reputation.',
  });
});

// 8. Document Signing Studio
app.get('/api/v1/document-signing', (_req, res) => {
  res.json({ ceremonies: docStore });
});

app.post('/api/v1/document-signing/ceremony', (req, res) => {
  const { ceremonyId, actorEmail, stepUpToken, explicitConsentChecked, simulatePostSignMutation } =
    req.body as {
      ceremonyId: string;
      actorEmail: string;
      stepUpToken: string;
      explicitConsentChecked: boolean;
      simulatePostSignMutation?: boolean;
    };

  const ceremony = docStore.find((c) => c.id === ceremonyId) || docStore[0];

  if (!explicitConsentChecked || !stepUpToken) {
    res.status(400).json({
      error: 'Explicit signer intent consent and step-up authentication token are mandatory prior to SAM sealing.',
    });
    return;
  }

  const nowIso = new Date().toISOString();
  const computedDigest = simulatePostSignMutation
    ? sha256Hex(`${ceremony.documentDigestSha256}:MUTATED_BYTE_0x4F`)
    : ceremony.documentDigestSha256;

  const digestMatchesPreview = computedDigest === ceremony.documentDigestSha256;

  if (digestMatchesPreview) {
    const pendingStep = ceremony.multiSignerOrder.find((s) => s.status === 'AWAITING_CEREMONY');
    if (pendingStep) {
      pendingStep.status = 'SIGNED_SEALED';
      pendingStep.signedAt = nowIso;
      pendingStep.signatureDigest = `SHA256:${sha256Hex(`${ceremony.documentDigestSha256}:${actorEmail}:${nowIso}`)}`;
    }
  }

  res.json({
    status: digestMatchesPreview ? 'valid' : 'invalid',
    qualifiedResultLabel: digestMatchesPreview
      ? 'PAdES-B-LTA Seal Applied · Preview Digest Bound & Timestamped'
      : 'Ceremony Aborted · Displayed Document Bytes Do Not Match Signed Digest',
    ceremony,
    verificationReport: {
      immutableDocumentDigest: ceremony.documentDigestSha256,
      verifiedCandidateDigest: computedDigest,
      digestMatchesPreview,
      stepUpVerifiedWith: stepUpToken,
      rfc3161Timestamp: nowIso,
      jurisdictionCaveat: ceremony.jurisdictionCaveat,
    },
  });
});

// 9. Webhook Signing Studio (RFC 9421)
app.get('/api/v1/webhook-signing', (_req, res) => {
  res.json({ profiles: webhookStore });
});

app.post('/api/v1/webhook-signing/simulate', (req, res) => {
  const {
    method,
    targetUri,
    authority,
    bodyJson,
    coveredComponents,
    eventIdHeader,
    nonce,
    proxyMutationMode,
  } = req.body as {
    method: string;
    targetUri: string;
    authority: string;
    bodyJson: string;
    coveredComponents: string[];
    eventIdHeader: string;
    nonce: string;
    proxyMutationMode: 'NONE' | 'MUTATE_UNCOVERED_HEADER' | 'MUTATE_COVERED_AUTHORITY' | 'REPLAY_NONCE';
  };

  const whProfile = webhookStore[0];
  const created = Math.floor(Date.now() / 1000);
  const expires = created + whProfile.maxValidityWindowSec;
  const effectiveNonce =
    proxyMutationMode === 'REPLAY_NONCE'
      ? 'nonce-replayed-demo-001'
      : nonce || `nonce-${crypto.randomBytes(4).toString('hex')}`;

  const contentDigest = `sha-256=:${sha256Base64(bodyJson || '{}')}:`;
  const compList =
    coveredComponents && coveredComponents.length > 0
      ? coveredComponents
      : whProfile.coveredComponents;

  const componentValues: Record<string, string> = {
    '@method': (method || 'POST').toUpperCase(),
    '@target-uri': targetUri || 'https://partner.example.com/webhooks/settlement',
    '@authority': authority || 'partner.example.com',
    'content-digest': contentDigest,
    'content-type': 'application/json; charset=utf-8',
    'x-tba-event-id': eventIdHeader || 'evt_settlement_994810',
    'x-tba-tenant-id': 'tnt-meridian-fin',
  };

  const sigParamsValue = `(${compList.map((c) => `"${c}"`).join(' ')});created=${created};expires=${expires};keyid="${whProfile.keyId}";alg="${whProfile.algorithm}";nonce="${effectiveNonce}"`;

  const canonicalLines = compList.map((comp) => `"${comp}": ${componentValues[comp] ?? ''}`);
  canonicalLines.push(`"@signature-params": ${sigParamsValue}`);
  const canonicalSignatureBase = canonicalLines.join('\n');

  const signatureBase64 = hsmSignDigest(whProfile.keyId, canonicalSignatureBase);

  // Now simulate verification after optional proxy/intermediary transformation
  const hasMandatoryDigest = compList.includes('content-digest') && compList.includes('@target-uri');
  const isReplay =
    proxyMutationMode === 'REPLAY_NONCE' || seenReplayNonces.has(effectiveNonce);
  if (!isReplay) {
    seenReplayNonces.add(effectiveNonce);
  }

  let verificationOutcome: VerificationStatus = 'valid';
  let policyNote =
    'Cryptographic signature valid, covered components meet profile policy, and nonce is fresh.';

  if (proxyMutationMode === 'MUTATE_COVERED_AUTHORITY') {
    verificationOutcome = 'invalid';
    policyNote =
      'Reverse proxy rewrote Host/@authority header from "partner.example.com" to "internal-ingress.cluster.local". Because "@authority" was covered, verification failed due to canonical base mismatch.';
  } else if (isReplay) {
    verificationOutcome = 'stale';
    policyNote = `Signature is mathematically valid, but nonce "${effectiveNonce}" was already consumed in the 300s replay cache. Rejected as replay.`;
  } else if (!hasMandatoryDigest) {
    verificationOutcome = 'invalid';
    policyNote =
      'Signature is mathematically valid over the selected subset, but policy-invalid because "content-digest" or "@target-uri" was omitted (body tampering remains unprotected).';
  } else if (proxyMutationMode === 'MUTATE_UNCOVERED_HEADER') {
    verificationOutcome = 'valid';
    policyNote =
      'Proxy appended "X-Envoy-External-Address" which is NOT in @signature-params. Signature remains valid, illustrating that RFC 9421 only proves integrity of explicitly listed components.';
  }

  res.json({
    contentDigestHeader: `Content-Digest: ${contentDigest}`,
    signatureInputHeader: `Signature-Input: sig1=${sigParamsValue}`,
    signatureHeader: `Signature: sig1=:${signatureBase64}:`,
    canonicalSignatureBase,
    coveredComponents: compList,
    verificationOutcome,
    cryptographicallyValid: proxyMutationMode !== 'MUTATE_COVERED_AUTHORITY',
    policyValid: verificationOutcome === 'valid',
    qualifiedResultLabel:
      verificationOutcome === 'valid'
        ? 'RFC 9421 Signature & Policy Valid'
        : verificationOutcome === 'stale'
        ? 'Cryptographically Valid · Replay Rejected'
        : 'Verification Failed · Canonical Mismatch or Policy Violation',
    policyNote,
  });
});

// 10. Evidence & Incidents
app.get('/api/v1/evidence', (_req, res) => {
  res.json({
    receipts: evidenceStore,
    privacyPosture: {
      rawMessageBodiesRetained: false,
      digestAlgorithm: 'SHA-256',
      pseudonymousAggregation: true,
    },
  });
});

app.get('/api/v1/incidents', (_req, res) => {
  res.json({ incidents: incidentsStore });
});

app.post('/api/v1/incidents/action', (req, res) => {
  const { incidentId, action } = req.body as {
    incidentId: string;
    action: 'SUSPEND_SIGNING' | 'ROTATE_AND_RECOVER';
  };

  const incident = incidentsStore.find((inc) => inc.id === incidentId);
  if (!incident) {
    res.status(404).json({ error: 'Incident not found.' });
    return;
  }

  const affectedIdentity = identitiesStore.find((i) => i.id === incident.affectedIdentityId);
  const nowIso = new Date().toISOString();

  if (action === 'SUSPEND_SIGNING') {
    incident.status = 'ACTIVE_SUSPENDED';
    if (affectedIdentity) {
      affectedIdentity.status = 'SUSPENDED';
      affectedIdentity.publicationStatus = 'Emergency Suspension Broadcast via Security Signals';
    }
  } else if (action === 'ROTATE_AND_RECOVER') {
    incident.status = 'RESOLVED_HISTORICAL_PRESERVED';
    const newKeyId = `key-${incident.channelFamily}-recovered-${crypto.randomBytes(2).toString('hex')}`;
    incident.affectedKeyId = newKeyId;
    if (affectedIdentity) {
      affectedIdentity.status = 'ACTIVE';
      affectedIdentity.signingKeyRef = `hsm://custody-vault/${newKeyId}`;
      affectedIdentity.publicationStatus = `Recovered with new key ${newKeyId} · Prior binding preserved for point-in-time verification`;
      affectedIdentity.bindingHistory.unshift({
        bindingVersion: (affectedIdentity.bindingHistory[0]?.bindingVersion || 1) + 1,
        effectiveFrom: nowIso,
        effectiveUntil: null,
        representedIdentifier: affectedIdentity.representedIdentifier,
        authorityEvidenceRef: `ev-recovery-${incident.id}`,
        verificationMethod: affectedIdentity.verificationMethod,
        externalGovernanceAuthority: 'Incident Recovery Quorum Approval',
        keyId: newKeyId,
        certificateFingerprint: `SHA256:${sha256Hex(`${newKeyId}:${nowIso}`)}`,
        statusAtVersion: 'ACTIVE',
        changeReason: `Key rotation and recovery from ${incident.id}; historical artifacts prior to suspension remain verifiable under earlier binding`,
      });
    }
  }

  res.json({
    incident,
    affectedIdentity,
  });
});

async function startServer() {
  const port = Number(process.env.PORT ?? 3000);
  const host = '127.0.0.1';
  if (process.env.NODE_ENV !== 'production' && !process.argv.includes('--production')) {
    const { createServer: createViteServer } = await import('vite');
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: 'spa',
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(__dirname, 'dist');
    app.use(express.static(distPath));
    app.get('*', (_req, res) => {
      res.sendFile(path.join(distPath, 'index.html'));
    });
  }

  app.listen(port, host, () => {
    console.log(`TBA Communications Identity Control Plane listening on http://${host}:${port}`);
  });
}

startServer();
