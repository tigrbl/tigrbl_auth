export interface HardwareAuthenticator {
  id: string;
  name: string;
  type: 'platform' | 'roaming' | 'workload' | 'software';
  aaguid: string;
  manufacturer: string;
  backing: 'verified_hwk' | 'unverified' | 'software_only' | 'unavailable';
  transports: ('usb' | 'nfc' | 'ble' | 'internal' | 'hybrid')[];
  created: string;
  lastUsed: string;
  status: 'active' | 'suspended' | 'revoked';
  algorithm: 'ES256' | 'RS256' | 'EdDSA';
  attestationFormat: 'packed' | 'tpm' | 'android-key' | 'apple-anonymous' | 'none';
  backupEligible: boolean;
  backupState: 'backed_up' | 'single_device';
  trustRoot: string;
  aaguidTrusted: boolean;
  userVerification: 'required' | 'preferred' | 'discouraged';
}

export interface WorkloadKey {
  id: string;
  name: string;
  profileName: string;
  algorithm: 'RS256' | 'ES256' | 'EdDSA';
  materialType: 'jwks' | 'certificate' | 'csr';
  publicKeyMaterial: string;
  fingerprint: string;
  created: string;
  expiry: string;
  status: 'active' | 'pending_rotation' | 'retired';
  keyProtection: 'HSM' | 'TPM' | 'Software';
  provenanceSource: string;
  lastVerified: string;
}

export interface CeremonyState {
  mode: 'auth' | 'enroll';
  status: 'idle' | 'preflight' | 'user_gesture' | 'submitting' | 'success' | 'failed' | 'cross_device';
  authenticatorType: 'platform' | 'roaming' | 'software';
  chosenMethodId?: string;
  currentStep: string;
  errorMsg?: string;
  countdown: number;
  selectedTransport: 'usb' | 'nfc' | 'ble' | 'internal' | 'hybrid';
  requiresNextStep?: boolean;
  hwkVerified: boolean;
  provenanceSource?: string;
  keyProtection?: string;
  trustRoot?: string;
}

export interface PolicyConfig {
  requireHwkEvidence: boolean;
  acceptedAttestationRoots: string[];
  allowedAlgorithms: ('ES256' | 'RS256' | 'EdDSA')[];
  userVerification: 'required' | 'preferred' | 'discouraged';
  allowSyncedPasskeys: boolean;
  requireDiscoverable: boolean;
  gracePeriodDays: number;
  enforcementMode: 'enforce' | 'audit_only' | 'disabled';
}

export interface AuditLogEntry {
  id: string;
  timestamp: string;
  event: string;
  category: 'authentication' | 'enrollment' | 'workload' | 'policy' | 'system';
  status: 'success' | 'warning' | 'failure';
  actor: string;
  details: string;
}

export interface AttestationRootMetadata {
  aaguid: string;
  name: string;
  manufacturer: string;
  hardwareBacking: 'verified_hwk' | 'software_only' | 'unverified';
  certificationLevel: 'L1' | 'L2' | 'L3' | 'none';
  supportedTransports: ('usb' | 'nfc' | 'ble' | 'internal' | 'hybrid')[];
}
