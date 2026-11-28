/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { Authenticator, PresencePolicy, ManagedKeyProfile, AuditLog } from './types';

export const INITIAL_AUTHENTICATORS: Authenticator[] = [
  {
    id: 'auth-macbook-touchid',
    name: 'MacBook Built-in Touch ID',
    type: 'passkey',
    transport: 'internal',
    upSupported: true,
    uvSupported: true,
    hardwareBacked: true,
    aaguid: 'adce0002-35bc-c60a-2b7b-40b2fed21711',
    createdAt: '2026-01-10T14:22:00Z',
    lastUsedAt: '2026-07-14T18:30:12Z',
    signatureCount: 42,
  },
  {
    id: 'auth-yubikey-5c',
    name: 'YubiKey 5C Nano (Hardware Key)',
    type: 'security_key',
    transport: 'usb',
    upSupported: true,
    uvSupported: true, // PIN or FIDO2 UV
    hardwareBacked: true,
    aaguid: 'cb69481e-8e17-4dd3-97f9-2e0085a6cfbc',
    createdAt: '2026-02-15T09:05:33Z',
    lastUsedAt: '2026-07-15T02:11:44Z',
    signatureCount: 119,
  },
  {
    id: 'auth-feitian-ieee',
    name: 'Managed Feitian Key (Corp Issued)',
    type: 'managed_key',
    transport: 'usb',
    upSupported: true,
    uvSupported: false, // Strict UP only
    hardwareBacked: true,
    aaguid: '7f348e02-45a8-4441-bc19-10aa1982a17f',
    createdAt: '2026-05-01T08:00:00Z',
    lastUsedAt: '2026-07-13T10:45:19Z',
    signatureCount: 8,
  },
  {
    id: 'auth-yubikey-nfc',
    name: 'YubiKey 5C NFC (Roaming)',
    type: 'security_key',
    transport: 'nfc',
    upSupported: true,
    uvSupported: true,
    hardwareBacked: true,
    aaguid: 'c53e164f-bc90-48e2-b0ef-1ef11d51a66a',
    createdAt: '2026-06-20T11:15:00Z',
    lastUsedAt: null,
    signatureCount: 0,
  }
];

export const INITIAL_POLICIES: PresencePolicy[] = [
  {
    id: 'policy-default',
    name: 'Standard Customer Login',
    presenceRequired: true,
    uvRequired: false,
    phishingResistant: true,
    hardwareBacked: false,
    maxAuthAgeSeconds: 86400, // 24 hours
    appScope: 'portal.main',
  },
  {
    id: 'policy-high-value',
    name: 'High-Value Transfer (Step-up)',
    presenceRequired: true,
    uvRequired: true, // Require User Verification (biometrics/PIN)
    phishingResistant: true,
    hardwareBacked: true,
    maxAuthAgeSeconds: 300, // 5 minutes
    appScope: 'portal.billing.transfer',
  },
  {
    id: 'policy-admin-console',
    name: 'Managed Dev / Admin Console',
    presenceRequired: true,
    uvRequired: false,
    phishingResistant: true,
    hardwareBacked: true, // Must be hardware key
    maxAuthAgeSeconds: 3600, // 1 hour
    appScope: 'admin.console',
  }
];

export const INITIAL_MANAGED_PROFILES: ManagedKeyProfile[] = [
  {
    id: 'profile-corporate-default',
    name: 'Corporate Device Trust Core',
    allowedTransports: ['usb', 'internal'],
    enforceHardwareBacking: true,
    allowedAaguids: [
      'cb69481e-8e17-4dd3-97f9-2e0085a6cfbc', // YubiKey 5C Nano
      '7f348e02-45a8-4441-bc19-10aa1982a17f', // Managed Feitian Key
    ],
    requireFreshnessSeconds: 60,
  }
];

export const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: 'log-1',
    timestamp: '2026-07-15T10:00:15Z',
    event: 'System preflight verification completed',
    category: 'lifecycle',
    status: 'success',
    details: 'Browser user-presence capabilities detected. PublicKeyCredential is supported.',
    auditReference: 'AUDIT-PRE-77A1',
  },
  {
    id: 'log-2',
    timestamp: '2026-07-15T10:05:44Z',
    event: 'Managed Key Enrollment Successful',
    category: 'enrollment',
    status: 'success',
    details: 'Enrollment complete for "Managed Feitian Key (Corp Issued)". Attestation flag UP verified.',
    auditReference: 'AUDIT-ENR-21C9',
  },
  {
    id: 'log-3',
    timestamp: '2026-07-15T10:12:10Z',
    event: 'Policy enforcement mismatch',
    category: 'policy',
    status: 'warning',
    details: 'Policy "High-Value Transfer (Step-up)" evaluated. Required: UV. Provided: UP only. User Verification additionally required.',
    auditReference: 'AUDIT-POL-8832',
  }
];
