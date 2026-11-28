import { SmartCard, TrustAnchor, MTLSConfig, AuditLog } from '../types';

export const mockCards: SmartCard[] = [
  {
    id: 'sc-01',
    label: 'U.S. Government CAC (Active)',
    subject: 'CN=SMITH.JOHN.DANIEL.1023948576,OU=USA,O=U.S. Government,C=US',
    issuer: 'CN=DOD SUBCA CA-62,OU=PKI,O=U.S. Government,C=US',
    serialNumber: '0A:4D:12:F3:5E:7B:99:A0',
    fingerprint: 'SHA-256: 4A:9C:B2:D3:8E:7F:10:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:A2:3B',
    notBefore: '2025-01-15T08:00:00Z',
    notAfter: '2028-01-15T08:00:00Z',
    eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)'],
    san: 'PrincipalName: 1023948576@mil | RFC822Name: john.d.smith.mil@mail.mil',
    status: 'active',
    lastUsed: '2026-07-19T14:32:00-07:00',
    hardware: {
      reader: 'SCR-3310 Contactless Smart Card Reader',
      cardType: 'CAC',
      pinAttemptsRemaining: 3,
      pinLocked: false,
      touchRequired: true,
    }
  },
  {
    id: 'sc-02',
    label: 'Federal PIV Token (Expiring Soon)',
    subject: 'CN=ALVAREZ.ELENA.MARIA.2049581102,OU=HHS,O=U.S. Government,C=US',
    issuer: 'CN=HHS PIV SUBCA G3,OU=PKI,O=U.S. Government,C=US',
    serialNumber: '1C:32:9B:EE:71:D8:0C:55',
    fingerprint: 'SHA-256: F1:E2:D3:C4:B5:A6:97:88:79:6A:5B:4C:3D:2E:1D:0C:FB:A9:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:AA',
    notBefore: '2023-08-01T12:00:00Z',
    notAfter: '2026-08-01T12:00:00Z', // Expiring in ~10 days relative to 2026-07-20
    eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)'],
    san: 'PrincipalName: elena.alvarez@hhs.gov',
    status: 'expiring',
    lastUsed: '2026-07-20T07:15:00-07:00',
    hardware: {
      reader: 'Omnikey 5022 CL Smart Card Reader',
      cardType: 'PIV',
      pinAttemptsRemaining: 3,
      pinLocked: false,
      touchRequired: false,
    }
  },
  {
    id: 'sc-03',
    label: 'Legacy CAC (Expired)',
    subject: 'CN=DOE.JANE.MARIE.3094857211,OU=USA,O=U.S. Government,C=US',
    issuer: 'CN=DOD SUBCA CA-51,OU=PKI,O=U.S. Government,C=US',
    serialNumber: '8D:11:A3:4C:E9:99:12:00',
    fingerprint: 'SHA-256: 8D:E3:4C:A1:99:BC:D1:4E:99:FF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CE:D1',
    notBefore: '2021-06-01T00:00:00Z',
    notAfter: '2024-06-01T00:00:00Z', // Expired
    eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)'],
    san: 'PrincipalName: 3094857211@mil',
    status: 'expired',
    lastUsed: '2024-05-30T16:45:00-07:00',
    hardware: {
      reader: 'SCR-3310 Contactless Smart Card Reader',
      cardType: 'CAC',
      pinAttemptsRemaining: 0,
      pinLocked: true,
      touchRequired: false,
    }
  },
  {
    id: 'sc-04',
    label: 'Contractor Smart Card (Revoked)',
    subject: 'CN=MILLER.THOMAS.PATRICK.99120485,OU=OUTSOURCE,O=U.S. Government,C=US',
    issuer: 'CN=EXTERNAL CA G4,OU=PKI,O=U.S. Government,C=US',
    serialNumber: 'FF:BB:AA:33:44:55:66:77',
    fingerprint: 'SHA-256: CC:BB:AA:99:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:AA:99:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:44',
    notBefore: '2024-10-10T10:00:00Z',
    notAfter: '2027-10-10T10:00:00Z',
    eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)'],
    san: 'PrincipalName: tmiller.ctr@navy.mil',
    status: 'revoked', // Revoked in CRL
    lastUsed: '2026-05-12T09:12:00-07:00',
    hardware: {
      reader: 'SCR-3310 Contactless Smart Card Reader',
      cardType: 'Custom',
      pinAttemptsRemaining: 3,
      pinLocked: false,
      touchRequired: false,
    }
  },
  {
    id: 'sc-05',
    label: 'U.S. Army CAC (PIN Blocked)',
    subject: 'CN=DAVIS.ROBERT.JAMES.4820194851,OU=USA,O=U.S. Government,C=US',
    issuer: 'CN=DOD SUBCA CA-62,OU=PKI,O=U.S. Government,C=US',
    serialNumber: 'B3:F9:A1:0C:4E:D5:78:12',
    fingerprint: 'SHA-256: BB:AA:CC:DD:EE:FF:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88:99:00:11:22:33:44:55:66:77:88:99:32',
    notBefore: '2024-03-01T08:00:00Z',
    notAfter: '2027-03-01T08:00:00Z',
    eku: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)'],
    san: 'PrincipalName: 4820194851@mil',
    status: 'suspended',
    lastUsed: '2026-07-15T11:24:00-07:00',
    hardware: {
      reader: 'SCR-3310 Contactless Smart Card Reader',
      cardType: 'CAC',
      pinAttemptsRemaining: 0, // Blocked!
      pinLocked: true,
      touchRequired: true,
    }
  },
  {
    id: 'sc-06',
    label: 'Personal Certificate (Wrong Profile / Non-PIV)',
    subject: 'CN=JICK.68.0,OU=USERS,O=Gmail,C=US',
    issuer: 'CN=Google Trust Services,O=Google Trust Services LLC,C=US',
    serialNumber: '92:4B:88:2E:CD:15:3A:FF',
    fingerprint: 'SHA-256: 01:02:03:04:05:06:07:08:09:0A:0B:0C:0D:0E:0F:10:11:12:13:14:15:16:17:18:19:1A:1B:1C:1D:1E:1F:20:21:22:23:24',
    notBefore: '2026-01-01T00:00:00Z',
    notAfter: '2027-01-01T00:00:00Z',
    eku: ['Secure Email (1.3.6.1.5.5.7.3.4)'], // Missing Client Auth or Smartcard Logon
    san: 'RFC822Name: jick.68.0@gmail.com',
    status: 'active',
    lastUsed: '2026-07-18T10:05:00-07:00',
    hardware: {
      reader: 'Built-in Security Hub',
      cardType: 'Custom',
      pinAttemptsRemaining: 3,
      pinLocked: false,
      touchRequired: false,
    }
  }
];

export const mockTrustAnchors: TrustAnchor[] = [
  {
    id: 'root-01',
    name: 'Federal Common Policy CA G2',
    subject: 'CN=Federal Common Policy CA G2,OU=FPKI,O=U.S. Government,C=US',
    status: 'trusted',
    expiry: '2035-12-31T23:59:59Z',
    crlUrl: 'http://http.fpki.gov/fcpca/fcpca.crl',
    ocspUrl: 'http://ocsp.fpki.gov',
    allowedEkis: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)']
  },
  {
    id: 'root-02',
    name: 'DoD Root CA 4',
    subject: 'CN=DoD Root CA 4,OU=PKI,O=U.S. Government,C=US',
    status: 'trusted',
    expiry: '2032-09-05T18:00:00Z',
    crlUrl: 'http://crl.disa.mil/dodca4/dodca4.crl',
    ocspUrl: 'http://dodocsp.disa.mil',
    allowedEkis: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)']
  },
  {
    id: 'root-03',
    name: 'DoD Root CA 5',
    subject: 'CN=DoD Root CA 5,OU=PKI,O=U.S. Government,C=US',
    status: 'trusted',
    expiry: '2036-05-14T20:00:00Z',
    crlUrl: 'http://crl.disa.mil/dodca5/dodca5.crl',
    ocspUrl: 'http://dodocsp.disa.mil',
    allowedEkis: ['Client Authentication (1.3.6.1.5.5.7.3.2)', 'Smartcard Logon (1.3.6.1.4.1.311.20.2.2)']
  },
  {
    id: 'root-04',
    name: 'Revoked Legacy Intermediate CA',
    subject: 'CN=DoD Root CA 2,OU=PKI,O=U.S. Government,C=US',
    status: 'revoked',
    expiry: '2025-02-12T12:00:00Z',
    crlUrl: 'http://crl.disa.mil/dodca2/dodca2.crl',
    ocspUrl: 'http://dodocsp.disa.mil',
    allowedEkis: ['Client Authentication (1.3.6.1.5.5.7.3.2)']
  }
];

export const mockMTLSConfigs: MTLSConfig[] = [
  {
    id: 'mtls-01',
    name: 'Production Admin Console Ingress',
    endpoint: 'https://admin-mtls.prod.federal.gov:443',
    boundCertFingerprint: 'SHA-256: 4A:9C:B2:D3:8E:7F:10:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:01:23:45:67:89:AB:CD:EF:A2:3B',
    authStrategy: 'san-mapping',
    createdAt: '2026-01-10T11:45:00Z',
    status: 'active'
  },
  {
    id: 'mtls-02',
    name: 'Secure API Gateway Gateway-04',
    endpoint: 'https://api-piv.secure.federal.gov:8443',
    boundCertFingerprint: 'SHA-256: F1:E2:D3:C4:B5:A6:97:88:79:6A:5B:4C:3D:2E:1D:0C:FB:A9:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:AA',
    authStrategy: 'strict-chain',
    createdAt: '2026-03-24T09:30:00Z',
    status: 'active'
  },
  {
    id: 'mtls-03',
    name: 'Staging Audit Collector Service',
    endpoint: 'https://audit-mtls.staging.federal.gov:443',
    boundCertFingerprint: 'SHA-256: CC:BB:AA:99:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:AA:99:88:77:66:55:44:33:22:11:00:FF:EE:DD:CC:BB:44',
    authStrategy: 'subject-exact',
    createdAt: '2026-06-01T15:00:00Z',
    status: 'inactive'
  }
];

export const mockAuditLogs: AuditLog[] = [
  {
    id: 'audit-01',
    timestamp: '2026-07-20T08:05:12-07:00',
    event: 'sc.auth.success',
    actor: 'CN=SMITH.JOHN.DANIEL.1023948576,OU=USA',
    status: 'success',
    cardFingerprint: 'SHA-256: 4A:9C:B2...A2:3B',
    details: 'Completed cryptographic possession proof (RSASSA-PKCS1-v1_5 / SHA-256). Token type: CAC. Chain verified via Federal Common Policy CA G2.',
    ipAddress: '10.142.0.4'
  },
  {
    id: 'audit-02',
    timestamp: '2026-07-20T07:45:30-07:00',
    event: 'sc.auth.failure',
    actor: 'UNKNOWN (PIN Blocked)',
    status: 'failure',
    cardFingerprint: 'SHA-256: BB:AA:CC...32',
    details: 'Cryptographic challenge failed. Middleware reported smart-card PIN is blocked (0 attempts remaining). PIN unblock code (PUK) required.',
    ipAddress: '10.142.12.115'
  },
  {
    id: 'audit-03',
    timestamp: '2026-07-20T06:12:05-07:00',
    event: 'sc.cert.validation.failed',
    actor: 'CN=MILLER.THOMAS.PATRICK.99120485,OU=OUTSOURCE',
    status: 'failure',
    cardFingerprint: 'SHA-256: CC:BB:AA...44',
    details: 'Certificate status check returned REVOKED. OCSP responder (http://ocsp.fpki.gov) signed status: Revocation Reason: KeyCompromise. Access denied.',
    ipAddress: '192.168.4.55'
  },
  {
    id: 'audit-04',
    timestamp: '2026-07-19T23:58:14-07:00',
    event: 'sc.trust.policy.updated',
    actor: 'CN=ADMIN.DOE.JONATHAN.992834',
    status: 'warning',
    cardFingerprint: undefined,
    details: 'Administrator added new trust anchor: DoD Root CA 5. Updated intermediate CRL caching rule to 60-minute background poll.',
    ipAddress: '10.142.0.2'
  },
  {
    id: 'audit-05',
    timestamp: '2026-07-19T18:44:22-07:00',
    event: 'sc.enrollment.started',
    actor: 'CN=ALVAREZ.ELENA.MARIA.2049581102,OU=HHS',
    status: 'success',
    cardFingerprint: 'SHA-256: F1:E2:D3...AA',
    details: 'Successful PIV certificate projection. Chain parsed correctly. Cryptographic signature verification passed. Device registered.',
    ipAddress: '10.22.45.9'
  }
];
