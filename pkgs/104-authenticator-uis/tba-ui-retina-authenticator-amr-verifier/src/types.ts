export type BiometricStatus = 'active' | 'suspended' | 'revoked' | 'none';

export interface BiometricConsentRecord {
  id: string;
  version: string;
  timestamp: string;
  purpose: string;
  status: 'accepted' | 'declined' | 'withdrawn';
  retentionDays: number;
  alternativeSelected: string | null;
}

export interface VerifierDevice {
  id: string;
  name: string;
  model: string;
  location: string;
  firmwareVersion: string;
  status: 'online' | 'offline' | 'calibrating' | 'maintenance';
  conformanceClass: 'Class-A' | 'Class-B' | 'Class-C';
  lastCalibrationDate: string;
  ambientLightLux: number;
  cameraResolution: string;
}

export interface DeletionJob {
  id: string;
  templateId: string;
  status: 'pending' | 'completed' | 'failed';
  requestedAt: string;
  completedAt: string | null;
  auditReference: string;
  evidenceRedacted: boolean;
}

export interface AuditLog {
  id: string;
  timestamp: string;
  eventType: 'consent_accept' | 'consent_withdraw' | 'preflight_pass' | 'preflight_fail' | 'enrollment_start' | 'enrollment_success' | 'enrollment_fail' | 'verification_success' | 'verification_fail' | 'template_delete' | 'policy_change' | 'device_outage' | 'device_calibration';
  subjectId: string;
  deviceId: string;
  outcome: 'success' | 'failed' | 'warning';
  livenessClass: 'Level-1' | 'Level-2' | 'Level-3' | 'None';
  matchScoreClass: 'high_confidence' | 'low_confidence' | 'no_match' | 'spoof_detected' | 'N/A';
  details: string;
}

export interface BiometricPolicy {
  eligibilityScope: 'all_users' | 'high_assurance_only' | 'custom';
  requiredLivenessLevel: 'Level-1' | 'Level-2' | 'Level-3';
  retentionPeriodMonths: number;
  allowWebFallback: boolean;
  geofenceEnabled: boolean;
  geofencedRegions: string[];
}

export interface RetinaEnrollment {
  id: string;
  subjectId: string;
  deviceId: string;
  enrolledAt: string;
  status: BiometricStatus;
  calibrationScore: number;
  consentVersion: string;
  lastUsedAt: string;
  expiresAt: string;
}

export type CeremonyType = 'enrollment' | 'verification' | 'step-up';

export interface LivenessStep {
  id: number;
  instruction: string;
  targetX: number; // percentage of target frame
  targetY: number; // percentage of target frame
  durationMs: number;
}
