import { BiometricPolicy, ProviderConfig, AuditLogRecord } from './types';

export const DEFAULT_POLICY: BiometricPolicy = {
  allowedProviders: ['first-party-iris', 'fed-eye-id'],
  maxEvidenceAgeSeconds: 300,
  requireLiveness: true,
  applicationScope: 'all',
  fallbackMethod: 'passkey',
  regionalRollout: {
    usEast: true,
    euWest: true,
    apSouth: false
  },
  minTrustLevel: 'high'
};

export const INITIAL_PROVIDERS: ProviderConfig[] = [
  {
    id: 'first-party-iris',
    name: 'IrisLink Specialized USB-C Sensor',
    type: 'first-party',
    status: 'active',
    conformanceCertified: true,
    retentionDays: 0, // In-memory/ephemeral only
    apiEndpoint: 'https://api.irislink.internal/v1/ceremony',
    lastHealthCheck: '2026-07-15T10:30:00-07:00'
  },
  {
    id: 'fed-eye-id',
    name: 'EyeID Federated Passkey Adapter',
    type: 'federated',
    status: 'active',
    conformanceCertified: true,
    retentionDays: 30, // Federated retention policy
    apiEndpoint: 'https://federation.eyeid.net/oauth/v2',
    lastHealthCheck: '2026-07-15T10:28:15-07:00'
  },
  {
    id: 'legacy-retina-corp',
    name: 'RetinaCorp Legacy Gaze Reader',
    type: 'external-native',
    status: 'suspended',
    conformanceCertified: false,
    retentionDays: 90,
    apiEndpoint: 'https://api.retinacorp.com/v3',
    lastHealthCheck: '2026-07-15T09:15:00-07:00'
  }
];

export const INITIAL_AUDIT_LOGS: AuditLogRecord[] = [
  {
    id: 'TX-94021',
    timestamp: '2026-07-15T10:25:31-07:00',
    actor: 'user_subject_9281',
    action: 'BIOMETRIC_ENROLLMENT_COMPLETE',
    outcome: 'success',
    evidenceType: 'iris',
    provenance: 'first-party:IrisLink',
    detailsRedacted: 'Consent: Version 2.1 (A1). Device Calibration: Confirmed. Template ID Hash: e3b0c442... [Image files deleted, ephemeral matching keys registered]'
  },
  {
    id: 'TX-94020',
    timestamp: '2026-07-15T10:24:12-07:00',
    actor: 'user_subject_9281',
    action: 'BIOMETRIC_ENROLLMENT_START',
    outcome: 'success',
    evidenceType: 'none',
    provenance: 'first-party:IrisLink',
    detailsRedacted: 'Consent accepted by subject in UI region: us-east-1. Preflight calibrator status: Green.'
  },
  {
    id: 'TX-93988',
    timestamp: '2026-07-15T10:11:45-07:00',
    actor: 'user_subject_5502',
    action: 'BIOMETRIC_VERIFICATION_ATTEMPT',
    outcome: 'failure',
    evidenceType: 'iris',
    provenance: 'first-party:IrisLink',
    detailsRedacted: 'Liveness fail class: PRESENTATION_ATTACK_SUSPECTED. Challenge bound mismatch. Match score: [REDACTED]. Access denied.'
  },
  {
    id: 'TX-93822',
    timestamp: '2026-07-15T09:44:02-07:00',
    actor: 'user_subject_1104',
    action: 'BIOMETRIC_VERIFICATION_ATTEMPT',
    outcome: 'success',
    evidenceType: 'iris',
    provenance: 'federated:EyeID',
    detailsRedacted: 'Evidence transformation accepted. AMR vector updated: ["iris"]. Trust score verified server-side. No image data transferred.'
  },
  {
    id: 'TX-93711',
    timestamp: '2026-07-15T08:52:19-07:00',
    actor: 'admin_agent_03',
    action: 'BIOMETRIC_POLICY_UPDATE',
    outcome: 'success',
    evidenceType: 'none',
    provenance: 'system',
    detailsRedacted: 'Biometric security policy revised to require mandatory liveness (requireLiveness = true). Policy published to version 4.'
  },
  {
    id: 'TX-93650',
    timestamp: '2026-07-15T08:12:00-07:00',
    actor: 'user_subject_3944',
    action: 'BIOMETRIC_TEMPLATE_DELETION',
    outcome: 'success',
    evidenceType: 'iris',
    provenance: 'first-party:IrisLink',
    detailsRedacted: 'Job ID: DEL-88129. Subject template reference nullified. Ephemeral matcher nodes notified of erasure. Status: Completed.'
  }
];
