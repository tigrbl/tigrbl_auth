/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { KbaQuestion, TenantPolicy, ProviderConfig, AuditEvent, CeremonyType, AssuranceLevel } from "./types";

// Server-approved KBA question catalog (Categorized and vetted for social-engineering exposure)
export const APPROVED_QUESTIONS: KbaQuestion[] = [
  { id: "q1", category: "Financial History", text: "What was the brand or manufacturer of your first vehicle?" },
  { id: "q2", category: "Employment History", text: "What was the first name of your supervisor at your very first professional job?" },
  { id: "q3", category: "Personal History", text: "In which city or town did your parents meet?" },
  { id: "q4", category: "Education History", text: "What was the name of the elementary school you attended for first grade?" },
  { id: "q5", category: "Financial History", text: "What was the name of the first bank where you opened a checking account?" },
  { id: "q6", category: "Employment History", text: "In which city or town was your first job interview or offer located?" },
  { id: "q7", category: "Personal History", text: "What was the name of the street on which your family lived when you were ten?" }
];

// Default configuration for the Tenant KBA Policy
export const DEFAULT_POLICY: TenantPolicy = {
  isKbaProhibited: false,
  minAssuranceRequired: AssuranceLevel.LOW, // KBA is lower-assurance, disabled for high assurance
  maxAttempts: 3,
  lockoutDurationMinutes: 15,
  sessionFreshnessSeconds: 120, // 2 minutes expiry for challenge sessions
  allowCustomQuestions: false, // Strict server-selected questions only
  requiredQuestionCount: 3,
  questionSource: "First-Party Standard Catalog",
  fallbackFactors: ["Passkey (FIDO2)", "TOTP Hardware Key", "Email Out-of-Band Link"]
};

// Approved Providers configuration
export const DEFAULT_PROVIDERS: ProviderConfig[] = [
  {
    id: "prov-1",
    name: "Aegis Secure Identity Bureau (Internal)",
    sourceType: "internal",
    encryptionAlgorithm: "AES-GCM-256 (Server Key Vault)",
    keyRotationDate: "2026-06-01",
    healthStatus: "healthy",
    regionalAvailability: ["US-East", "EU-West", "AP-South"]
  },
  {
    id: "prov-2",
    name: "Equifax Identity Verification Suite",
    sourceType: "identity_bureau",
    encryptionAlgorithm: "RSA-4096 / SHA-256",
    keyRotationDate: "2026-04-15",
    healthStatus: "healthy",
    regionalAvailability: ["US-East", "US-West"]
  },
  {
    id: "prov-3",
    name: "Metropolitan Utilities Verifier API",
    sourceType: "utility_records",
    encryptionAlgorithm: "ChaCha20-Poly1305",
    keyRotationDate: "2026-05-10",
    healthStatus: "degraded",
    regionalAvailability: ["EU-Central"]
  }
];

// Seeded Audit Events demonstrating redacted attempts and security outcomes
export const SEED_AUDIT_LOGS: AuditEvent[] = [
  {
    id: "evt-101",
    timestamp: "2026-07-16T15:24:10-07:00",
    userEmail: "jick.68.0@gmail.com",
    action: "challenge_attempt",
    ceremonyType: CeremonyType.SIGN_IN,
    status: "failed",
    providerId: "prov-1",
    details: "KBA verifier check completed. Result: MISMATCH [REDACTED_ANSWER_HASH]. Attempt 1 of 3.",
    ipAddress: "192.168.1.45",
    assuranceLevel: AssuranceLevel.LOW
  },
  {
    id: "evt-102",
    timestamp: "2026-07-16T15:25:02-07:00",
    userEmail: "jick.68.0@gmail.com",
    action: "challenge_attempt",
    ceremonyType: CeremonyType.SIGN_IN,
    status: "completed",
    providerId: "prov-1",
    details: "KBA verifier check completed. Result: MATCH [REDACTED_ANSWER_HASH]. Challenge criteria satisfied.",
    ipAddress: "192.168.1.45",
    assuranceLevel: AssuranceLevel.LOW
  },
  {
    id: "evt-103",
    timestamp: "2026-07-16T16:10:00-07:00",
    userEmail: "admin@enterprise.com",
    action: "policy_updated",
    ceremonyType: CeremonyType.ENROLLMENT,
    status: "completed",
    providerId: "prov-1",
    details: "Updated TenantPolicy: KBA requiredQuestionCount changed from 2 to 3. Prohibit KBA for High-Assurance: Enabled.",
    ipAddress: "10.0.4.12",
    assuranceLevel: AssuranceLevel.HIGH
  },
  {
    id: "evt-104",
    timestamp: "2026-07-16T17:45:11-07:00",
    userEmail: "attacker.recon@darkweb.org",
    action: "challenge_attempt",
    ceremonyType: CeremonyType.RECOVERY,
    status: "failed",
    providerId: "prov-2",
    details: "Account recovery challenge failed. Result: EXHAUSTED. Lockout triggered for 15 mins. [REDACTED_ANSWER_HASH].",
    ipAddress: "185.220.101.4",
    assuranceLevel: AssuranceLevel.LOW
  }
];
