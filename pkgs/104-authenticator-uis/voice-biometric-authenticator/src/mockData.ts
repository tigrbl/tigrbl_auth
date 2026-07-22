import { VoiceProfile, PolicyConfig, VerifierConfig, AuditLog, DiagnosticsSummary } from './types';

// Default initial state
const DEFAULT_PROFILE: VoiceProfile = {
  id: 'usr_vbm_90241',
  status: 'unenrolled',
  consentSigned: false,
  consentVersion: 'v1.4-VBM-PRIVACY',
  samples: [],
  modelId: 'VBM-Neural-v4.2-Liveness',
  region: 'us-east1',
  deletionStatus: 'none',
};

const DEFAULT_POLICY: PolicyConfig = {
  minConfidence: 82,
  strictnessLevel: 'medium',
  allowedLanguages: ['en-US', 'es-MX', 'fr-FR'],
  fallbackFactor: 'fido_passkey',
  retentionDays: 180,
  strictLiveness: true,
  noiseThresholdDb: -42,
};

const DEFAULT_VERIFIER: VerifierConfig = {
  providerName: 'SentryVoice Biometrics',
  endpointUrl: 'https://api.sentryvoice.biometrics.gcp/v2/verify',
  region: 'us-east1',
  activeModel: 'VBM-Neural-v4.2-Liveness',
  healthStatus: 'healthy',
  failBehavior: 'fail_safe',
};

const INITIAL_AUDIT_LOGS: AuditLog[] = [
  {
    id: 'tx_vbm_8820',
    timestamp: '2026-07-15T09:12:00-07:00',
    action: 'POLICY_UPDATE',
    status: 'success',
    details: 'Security Policy updated: strictLiveness set to TRUE, minConfidence threshold set to 82%.',
    ipAddress: '192.168.1.100',
  },
  {
    id: 'tx_vbm_8819',
    timestamp: '2026-07-15T08:44:12-07:00',
    action: 'VERIFICATION_ATTEMPT',
    status: 'success',
    details: 'Voice verification successful. confidence: 91%, liveness: live.',
    amrToken: 'amr_vbm.v1_match.91_live_sha256_b831fa',
    ipAddress: '24.112.98.4',
  },
  {
    id: 'tx_vbm_8818',
    timestamp: '2026-07-14T23:10:05-07:00',
    action: 'VERIFICATION_FAILED',
    status: 'warning',
    details: 'Verification failed: confidence (64%) below matching threshold (82%).',
    ipAddress: '98.15.201.12',
  },
  {
    id: 'tx_vbm_8817',
    timestamp: '2026-07-14T18:20:19-07:00',
    action: 'SPOOF_ATTEMPT_REJECTED',
    status: 'failure',
    details: 'Replay attack signature detected on verifier. Match aborted.',
    ipAddress: '185.220.101.44',
  },
  {
    id: 'tx_vbm_8816',
    timestamp: '2026-07-13T14:30:22-07:00',
    action: 'ENROLLMENT_COMPLETED',
    status: 'success',
    details: 'User voice biometric profile activated. Consent version v1.4-VBM-PRIVACY signed.',
    ipAddress: '192.168.1.100',
  },
];

const INITIAL_DIAGNOSTICS: DiagnosticsSummary = {
  totalAttempts: 248,
  successCount: 204,
  failureCount: 44,
  spoofAttempts: {
    replay: 14,
    synthetic: 6,
  },
  noiseFailures: 15,
  noSpeechFailures: 9,
  averageResponseTimeMs: 420,
};

// Local storage state keys
const KEYS = {
  PROFILE: 'vbm_profile',
  POLICY: 'vbm_policy',
  VERIFIER: 'vbm_verifier',
  AUDIT_LOGS: 'vbm_audit_logs',
  DIAGNOSTICS: 'vbm_diagnostics',
};

export function loadProfile(): VoiceProfile {
  const data = localStorage.getItem(KEYS.PROFILE);
  if (!data) {
    saveProfile(DEFAULT_PROFILE);
    return DEFAULT_PROFILE;
  }
  return JSON.parse(data);
}

export function saveProfile(profile: VoiceProfile): void {
  localStorage.setItem(KEYS.PROFILE, JSON.stringify(profile));
}

export function loadPolicy(): PolicyConfig {
  const data = localStorage.getItem(KEYS.POLICY);
  if (!data) {
    savePolicy(DEFAULT_POLICY);
    return DEFAULT_POLICY;
  }
  return JSON.parse(data);
}

export function savePolicy(policy: PolicyConfig): void {
  localStorage.setItem(KEYS.POLICY, JSON.stringify(policy));
}

export function loadVerifier(): VerifierConfig {
  const data = localStorage.getItem(KEYS.VERIFIER);
  if (!data) {
    saveVerifier(DEFAULT_VERIFIER);
    return DEFAULT_VERIFIER;
  }
  return JSON.parse(data);
}

export function saveVerifier(verifier: VerifierConfig): void {
  localStorage.setItem(KEYS.VERIFIER, JSON.stringify(verifier));
}

export function loadAuditLogs(): AuditLog[] {
  const data = localStorage.getItem(KEYS.AUDIT_LOGS);
  if (!data) {
    saveAuditLogs(INITIAL_AUDIT_LOGS);
    return INITIAL_AUDIT_LOGS;
  }
  return JSON.parse(data);
}

export function saveAuditLogs(logs: AuditLog[]): void {
  localStorage.setItem(KEYS.AUDIT_LOGS, JSON.stringify(logs));
}

export function addAuditLog(action: string, status: 'success' | 'failure' | 'warning' | 'info', details: string, amrToken?: string): void {
  const logs = loadAuditLogs();
  const newLog: AuditLog = {
    id: `tx_vbm_${Math.floor(1000 + Math.random() * 9000)}`,
    timestamp: new Date().toISOString(),
    action,
    status,
    details,
    amrToken,
    ipAddress: '192.168.1.100',
  };
  logs.unshift(newLog);
  saveAuditLogs(logs);
}

export function loadDiagnostics(): DiagnosticsSummary {
  const data = localStorage.getItem(KEYS.DIAGNOSTICS);
  if (!data) {
    saveDiagnostics(INITIAL_DIAGNOSTICS);
    return INITIAL_DIAGNOSTICS;
  }
  return JSON.parse(data);
}

export function saveDiagnostics(diag: DiagnosticsSummary): void {
  localStorage.setItem(KEYS.DIAGNOSTICS, JSON.stringify(diag));
}

export function recordDiagResult(
  category: 'success' | 'mismatch' | 'replay' | 'synthetic' | 'noise' | 'no_speech',
  responseTimeMs: number
): void {
  const diag = loadDiagnostics();
  diag.totalAttempts += 1;
  diag.averageResponseTimeMs = Math.round(
    (diag.averageResponseTimeMs * (diag.totalAttempts - 1) + responseTimeMs) / diag.totalAttempts
  );

  if (category === 'success') {
    diag.successCount += 1;
  } else {
    diag.failureCount += 1;
    if (category === 'replay') diag.spoofAttempts.replay += 1;
    else if (category === 'synthetic') diag.spoofAttempts.synthetic += 1;
    else if (category === 'noise') diag.noiseFailures += 1;
    else if (category === 'no_speech') diag.noSpeechFailures += 1;
  }
  saveDiagnostics(diag);
}

export function resetAllData(): void {
  localStorage.removeItem(KEYS.PROFILE);
  localStorage.removeItem(KEYS.POLICY);
  localStorage.removeItem(KEYS.VERIFIER);
  localStorage.removeItem(KEYS.AUDIT_LOGS);
  localStorage.removeItem(KEYS.DIAGNOSTICS);
}
