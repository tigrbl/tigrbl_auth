export type KeyProfileType = 'passkey' | 'dpop' | 'private_key_jwt' | 'signing' | 'workload';

export interface KeyProfile {
  id: KeyProfileType;
  name: string;
  description: string;
  algorithms: string[];
  recommendedStore: string;
  intendedUse: string;
}

export type StorageClassification = 'software_secured' | 'hardware_backed' | 'unknown';

export interface SoftwareKeyCredential {
  id: string;
  name: string;
  profile: KeyProfileType;
  algorithm: string;
  keyStoreProvider: string; // e.g. "macOS Keychain (CryptoKit)", "Windows CNG", "Linux Secret Service", "CLI Secure Keyring"
  storageClass: StorageClassification;
  hasVerifiedEvidence: boolean; // 'swk' AMR is only verified if evidence proves software-protected
  evidenceProvenance: string; // e.g. "OS Keystore Metadata Statement (v2)"
  publicKeyJwk: string; // Redacted or public representation
  fingerprint: string;
  status: 'active' | 'rotated' | 'compromised' | 'revoked';
  backupPosture: 'permitted' | 'blocked' | 'unverified';
  exportPosture: 'permitted' | 'blocked';
  createdAt: string;
  lastUsedAt: string;
  appScope: string;
  dependencies: string[]; // dependent apps/services
}

export interface KeyOriginPolicy {
  allowedStores: string[];
  allowedAlgorithms: string[];
  backupPolicy: 'allow' | 'block' | 'strict_evidence';
  exportPolicy: 'allow' | 'block';
  requireEnclaveClassification: boolean;
  minKeyLength: number;
  appScopeDefault: string;
}

export interface ProviderHealth {
  id: string;
  name: string;
  type: 'native' | 'sdk' | 'validator';
  status: 'healthy' | 'degraded' | 'unavailable';
  latencyMs: number;
  lastChecked: string;
  version: string;
}

export interface AuditEvent {
  id: string;
  timestamp: string;
  eventType: string; // 'registration' | 'proof_generation' | 'verification' | 'rotation' | 'compromise' | 'policy_change' | 'error'
  actor: string;
  profile: string;
  storageClass: StorageClassification;
  evidenceVerified: boolean;
  details: string;
  hash: string; // cryptographic representation
}

export interface ProofChallenge {
  purpose: string;
  endpoint: string;
  nonce: string;
  audience: string;
  timestamp: string;
  algorithm: string;
}

export interface ProofAssertion {
  signature: string;
  nonce: string;
  audience: string;
  algorithm: string;
  timestamp: string;
  evidenceToken: string; // proof of software execution
  status: 'valid' | 'stale' | 'replay_rejected' | 'invalid_signature' | 'locked_keystore' | 'algorithm_mismatch';
}
