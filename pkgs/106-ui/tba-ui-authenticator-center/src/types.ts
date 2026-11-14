export type AuthenticatorKind = "password" | "totp" | "hotp" | "recovery_code" | "webauthn" | "federated_oidc" | "mtls" | "dpop";
export type AuthenticatorState = "active" | "suspended" | "revoked" | "pending" | "expired" | "reenrollment_required" | "pending_enrollment";
export type AuthenticatorProperties = Record<"userPresent" | "userVerified" | "phishingResistant" |
  "verifierNameBound" | "replayResistant" | "senderConstrained" | "hardwareBacked" |
  "synced" | "discoverable" | "attested", boolean>;
export type IdentityProfile = { id: string; email: string; name: string; avatarUrl: string; role: "user" | "admin" };
export type Authenticator = {
  id: string; principalId: string; tenantId: string; kind: AuthenticatorKind; displayName: string;
  state: AuthenticatorState; enrolledAt: string; lastVerifiedAt: string | null;
  lastUsedAt: string | null; expiresAt: string | null; suspendedAt: string | null;
  revokedAt: string | null; amr: string[]; properties: AuthenticatorProperties;
  attestationSummary: string; recoveryEligibility: boolean; version: number;
  details?: Record<string, unknown> & { remainingCount?: number };
};
export type TenantPolicy = {
  tenantId: string; allowedKinds: AuthenticatorKind[]; requiredKinds: AuthenticatorKind[];
  prohibitedKinds: AuthenticatorKind[]; stepUpEligibleKinds: AuthenticatorKind[];
  gracePeriodDays: number; attestationPolicy: string; allowedAlgorithms: string[];
  updatedBy: string; updatedAt: string; version: number;
};
export type AuditLog = {
  id: string; timestamp: string; subjectId: string; tenantId: string; action: string;
  authenticatorId?: string; operatorId: string; status: "success" | "failure";
  reasonCode?: string; correlationId: string; details: string;
};
export type Ceremony = {
  id: string; kind: AuthenticatorKind; operation: string; subjectId: string; tenantId: string;
  challenge: string; expiresAt: string; origin?: string; rpId?: string; userVerification?: string;
  requiredPresence?: boolean; otpSecret?: string; recoveryCodes?: string[]; replaceAuthId?: string;
};
type Aal = "NONE" | "AAL1" | "AAL2" | "AAL3";
export type AuthenticationContext = {
  requiredAal: Aal; achievedAal: Aal; requiredAcr: string[]; achievedAmr: string[];
  achievedProperties: Partial<AuthenticatorProperties>; sessionExpiresAt: string; evaluatedAt: string;
  contributingAuthenticators: Pick<Authenticator, "id" | "kind" | "displayName" | "properties">[];
};
