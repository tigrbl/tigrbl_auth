import { HardwareAuthenticator, WorkloadKey, AuditLogEntry, AttestationRootMetadata } from './types';

export const initialAuthenticators: HardwareAuthenticator[] = [
  {
    id: 'auth-yubikey-5c',
    name: 'Primary YubiKey 5C NFC',
    type: 'roaming',
    aaguid: 'cb581753-f341-4fb9-adc4-ae840d0263f1',
    manufacturer: 'Yubico',
    backing: 'verified_hwk',
    transports: ['usb', 'nfc'],
    created: '2026-03-12T08:14:22Z',
    lastUsed: '2026-07-15T10:22:15Z',
    status: 'active',
    algorithm: 'ES256',
    attestationFormat: 'packed',
    backupEligible: true,
    backupState: 'backed_up',
    trustRoot: 'Yubico_L1_Global_Root_CA',
    aaguidTrusted: true,
    userVerification: 'required'
  },
  {
    id: 'auth-mac-touchid',
    name: 'MacBook Pro Touch ID (Hardware Enclave)',
    type: 'platform',
    aaguid: '74c20894-3ee2-40f0-8c26-5b94f47be683',
    manufacturer: 'Apple Inc.',
    backing: 'verified_hwk',
    transports: ['internal'],
    created: '2026-04-01T14:32:00Z',
    lastUsed: '2026-07-15T09:45:11Z',
    status: 'active',
    algorithm: 'ES256',
    attestationFormat: 'apple-anonymous',
    backupEligible: false,
    backupState: 'single_device',
    trustRoot: 'Apple_WebAuthn_Root_CA',
    aaguidTrusted: true,
    userVerification: 'required'
  },
  {
    id: 'auth-titan-key',
    name: 'Google Titan Security Key',
    type: 'roaming',
    aaguid: '8495a623-e291-49b8-a831-cd34c90141f1',
    manufacturer: 'Google',
    backing: 'verified_hwk',
    transports: ['usb', 'nfc', 'ble'],
    created: '2026-05-18T10:11:05Z',
    lastUsed: '2026-07-14T18:05:44Z',
    status: 'active',
    algorithm: 'ES256',
    attestationFormat: 'packed',
    backupEligible: true,
    backupState: 'backed_up',
    trustRoot: 'Google_Titan_FIDO2_CA',
    aaguidTrusted: true,
    userVerification: 'required'
  },
  {
    id: 'auth-icloud-sync',
    name: 'iCloud Keychain (Synced Passkey)',
    type: 'platform',
    aaguid: 'd91890e4-b772-468a-b9c1-7cb20d414f4e',
    manufacturer: 'Apple Inc.',
    backing: 'software_only', // synched keys are not guaranteed HWK under strict policy since copyable across synced nodes
    transports: ['internal', 'hybrid'],
    created: '2026-06-20T16:45:00Z',
    lastUsed: '2026-07-15T08:12:30Z',
    status: 'active',
    algorithm: 'ES256',
    attestationFormat: 'none',
    backupEligible: true,
    backupState: 'backed_up',
    trustRoot: 'No Attestation (Synced Token)',
    aaguidTrusted: false,
    userVerification: 'preferred'
  },
  {
    id: 'auth-windows-hello',
    name: 'Windows Hello TPM Authenticator',
    type: 'platform',
    aaguid: '2fc20894-3ee2-40f0-8c26-5b94f47be683',
    manufacturer: 'Microsoft Corp.',
    backing: 'verified_hwk',
    transports: ['internal'],
    created: '2026-07-02T11:05:12Z',
    lastUsed: '2026-07-10T15:30:11Z',
    status: 'active',
    algorithm: 'RS256',
    attestationFormat: 'tpm',
    backupEligible: false,
    backupState: 'single_device',
    trustRoot: 'Microsoft_TPM_Attestation_Root',
    aaguidTrusted: true,
    userVerification: 'required'
  }
];

export const initialWorkloadKeys: WorkloadKey[] = [
  {
    id: 'wl-billing',
    name: 'Billing Microservice Client Key',
    profileName: 'Internal Ledger Transactor',
    algorithm: 'ES256',
    materialType: 'jwks',
    publicKeyMaterial: '{\n  "keys": [\n    {\n      "kty": "EC",\n      "crv": "P-256",\n      "x": "MKBXSTp9YL71CDy5T4U3GjS_6fLq7_E...",\n      "y": "f83OJ3D2xF118BF3OkM_SVDy1CDy5T4...",\n      "use": "sig",\n      "kid": "wl-billing-key-01"\n    }\n  ]\n}',
    fingerprint: 'sha256:d89482f1b490ce01ab78c3c1a84f4f30...',
    created: '2026-01-10T09:00:00Z',
    expiry: '2027-01-10T09:00:00Z',
    status: 'active',
    keyProtection: 'HSM',
    provenanceSource: 'YubiHSM 2 Hardware Attestation Certificate',
    lastVerified: '2026-07-15T10:00:00Z'
  },
  {
    id: 'wl-cicd',
    name: 'CI/CD Deployment Operator Cert',
    profileName: 'Prod Release Pipeline Creator',
    algorithm: 'RS256',
    materialType: 'certificate',
    publicKeyMaterial: '-----BEGIN CERTIFICATE-----\nMIIB7TCCAVegAwIBAgIJAK9qD3tFz+9kMA0GCSqGSIb3DQEBCwUAMA0xCzAJBgNV\nBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYwFAYDVQQHDA1Nb3VudGFpbiBW\naWV3MRIwEAYDVQQKDAlBY21lIENvcnAwIBcNMjYwNzAxMDAwMDAwWhgPMjEyNjA3\nMDEwMDAwMDBaMA0xCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYw\nFAYDVQQHDA1Nb3VudGFpbiBWaWV3MRIwEAYDVQQKDAlBY21lIENvcnAwgZ8wDQYJ\nKoZIhvcNAQEBBQADgY0AMIGJAoGBALN7rMv...',
    fingerprint: 'sha256:fa234125fbc7098e1cbda537cb0184e1...',
    created: '2026-07-01T00:00:00Z',
    expiry: '2026-10-01T00:00:00Z',
    status: 'active',
    keyProtection: 'TPM',
    provenanceSource: 'Intel TXT TPM 2.0 Endorsement Key Proof',
    lastVerified: '2026-07-15T10:25:31Z'
  },
  {
    id: 'wl-webhook',
    name: 'Staging Webhook Workload Signature',
    profileName: 'Staging Event Publisher',
    algorithm: 'EdDSA',
    materialType: 'csr',
    publicKeyMaterial: '-----BEGIN CERTIFICATE REQUEST-----\nMIIBvDCCASQCAQAwFjEUMBIGA1UEAwwLd2ViaG9vay1zdGcwgZ8wDQYJKoZIhvcN\nAQEBBQADgY0AMIGJAoGBAMr7lq8tX81C7Yy8u2S5yTz6S6Fv8X7Vd1L_6fLq7_Ek\nbW8F3OkM_SVDyMKBXSTp9YL71CDy5T4U3GjS_6fLq7_E8bW8F3OkM_SVDyMKBXST\np9YL71CDy5T4U3GjS_6fLq7_EkHwIDAQABoAAwDQYJKoZIhvcNAQEFBQADgYEAc\n7fV7bNqY7...',
    fingerprint: 'sha256:88941031cb48f2038e1cbca530ff01ce...',
    created: '2026-07-14T21:10:00Z',
    expiry: '2026-08-14T21:10:00Z',
    status: 'pending_rotation',
    keyProtection: 'Software',
    provenanceSource: 'No Attestation (Client CSR Self-Signed)',
    lastVerified: '2026-07-14T21:10:00Z'
  }
];

export const attestationRoots: AttestationRootMetadata[] = [
  {
    aaguid: 'cb581753-f341-4fb9-adc4-ae840d0263f1',
    name: 'YubiKey 5 Series Series FIDO2',
    manufacturer: 'Yubico',
    hardwareBacking: 'verified_hwk',
    certificationLevel: 'L3',
    supportedTransports: ['usb', 'nfc']
  },
  {
    aaguid: '74c20894-3ee2-40f0-8c26-5b94f47be683',
    name: 'Apple iCloud Secure Enclave Passkey',
    manufacturer: 'Apple Inc.',
    hardwareBacking: 'verified_hwk',
    certificationLevel: 'L2',
    supportedTransports: ['internal']
  },
  {
    aaguid: '8495a623-e291-49b8-a831-cd34c90141f1',
    name: 'Google Titan Security Key FIDO2',
    manufacturer: 'Google',
    hardwareBacking: 'verified_hwk',
    certificationLevel: 'L3',
    supportedTransports: ['usb', 'nfc', 'ble']
  },
  {
    aaguid: '2fc20894-3ee2-40f0-8c26-5b94f47be683',
    name: 'Windows Hello TPM FIDO2 Authenticator',
    manufacturer: 'Microsoft Corp.',
    hardwareBacking: 'verified_hwk',
    certificationLevel: 'L2',
    supportedTransports: ['internal']
  },
  {
    aaguid: 'd91890e4-b772-468a-b9c1-7cb20d414f4e',
    name: 'Generic Apple Synced Passkey Profile',
    manufacturer: 'Apple Inc.',
    hardwareBacking: 'software_only',
    certificationLevel: 'none',
    supportedTransports: ['internal', 'hybrid']
  },
  {
    aaguid: '00000000-0000-0000-0000-000000000000',
    name: 'Unverified Soft-Token Authenticator',
    manufacturer: 'Generic Software',
    hardwareBacking: 'software_only',
    certificationLevel: 'none',
    supportedTransports: ['usb', 'internal']
  }
];

export const initialAuditLogs: AuditLogEntry[] = [
  {
    id: 'log-001',
    timestamp: '2026-07-15T10:25:31Z',
    event: 'Workload Key Verification Successful',
    category: 'workload',
    status: 'success',
    actor: 'system-agent',
    details: 'Verified CI/CD deployment cert against Intel TXT TPM root. Key Protection: TPM. HWK classification enabled.'
  },
  {
    id: 'log-002',
    timestamp: '2026-07-15T10:22:15Z',
    event: 'Human User Authentication (hwk_assert)',
    category: 'authentication',
    status: 'success',
    actor: 'jick.68.0@gmail.com',
    details: 'Completed roaming key assertion using YubiKey 5C NFC. Verified HWK Evidence. AMR: hwk. RP ID: secure.hwk.internal'
  },
  {
    id: 'log-003',
    timestamp: '2026-07-15T09:45:11Z',
    event: 'Step-Up Verification Successful',
    category: 'authentication',
    status: 'success',
    actor: 'jick.68.0@gmail.com',
    details: 'Verified platform key on MacBook Pro Touch ID. Apple Secure Enclave attestation validated.'
  },
  {
    id: 'log-004',
    timestamp: '2026-07-15T09:30:00Z',
    event: 'AMR Policy Config Altered',
    category: 'policy',
    status: 'warning',
    actor: 'admin@hwk.internal',
    details: 'Required hardware evidence policy updated to FORCE_ENFORCE. Transports without attestation will trigger fallbacks.'
  },
  {
    id: 'log-005',
    timestamp: '2026-07-14T21:10:00Z',
    event: 'Workload Key Registration Requested',
    category: 'workload',
    status: 'warning',
    actor: 'dev-webhook-operator',
    details: 'Staging Webhook key uploaded. Self-signed CSR has NO hardware attestation. Classified as UNVERIFIED.'
  },
  {
    id: 'log-006',
    timestamp: '2026-07-14T18:05:44Z',
    event: 'Hardware Authentication Warning',
    category: 'authentication',
    status: 'failure',
    actor: 'jick.68.0@gmail.com',
    details: 'iCloud Keychain passkey assertion returned software-only backing. Blocked step-up action (Requires hwk evidence).'
  }
];

export const sampleJWKS = `{
  "keys": [
    {
      "kty": "EC",
      "crv": "P-256",
      "x": "MKBXSTp9YL71CDy5T4U3GjS_6fLq7_Ek",
      "y": "f83OJ3D2xF118BF3OkM_SVDyMKBXSTp9",
      "use": "sig",
      "kid": "wl-billing-key-01"
    }
  ]
}`;

export const sampleCert = `-----BEGIN CERTIFICATE-----
MIIB7TCCAVegAwIBAgIJAK9qD3tFz+9kMA0GCSqGSIb3DQEBCwUAMA0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYwFAYDVQQHDA1Nb3VudGFpbiBW
aWV3MRIwEAYDVQQKDAlBY21lIENvcnAwIBcNMjYwNzAxMDAwMDAwWhgPMjEyNjA3
MDEwMDAwMDBaMA0xCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRYw
FAYDVQQHDA1Nb3VudGFpbiBWaWV3MRIwEAYDVQQKDAlBY21lIENvcnAwgZ8wDQYJ
KoZIhvcNAQEBBQADgY0AMIGJAoGBALN7rMv96qBpx5DsyB7x+vQ0q6S2v1KzM9Lg
m8H3OkM/SVDyMKBXSTp9YL71CDy5T4U3GjS/6fLq7/EkHwIDAQABoAAwDQYJKoZI
hvcNAQEFBQADgYEAc7fV7bNqY7l4oY6F9F2g6GzS9v3Y1bL+6m5GZ9f2bCq5f2gG
-----END CERTIFICATE-----`;

export const sampleCSR = `-----BEGIN CERTIFICATE REQUEST-----
MIIBvDCCASQCAQAwFjEUMBIGA1UEAwwLd2ViaG9vay1zdGcwgZ8wDQYJKoZIhvcN
AQEBBQADgY0AMIGJAoGBAMr7lq8tX81C7Yy8u2S5yTz6S6Fv8X7Vd1L_6fLq7_Ek
bW8F3OkM_SVDyMKBXSTp9YL71CDy5T4U3GjS_6fLq7_E8bW8F3OkM_SVDyMKBXST
p9YL71CDy5T4U3GjS_6fLq7_EkHwIDAQABoAAwDQYJKoZIhvcNAQEFBQADgYEAc
7fV7bNqY7l4oY6F9F2g6GzS9v3Y1bL+6m5GZ9f2bCq5f2gG
-----END CERTIFICATE REQUEST-----`;
