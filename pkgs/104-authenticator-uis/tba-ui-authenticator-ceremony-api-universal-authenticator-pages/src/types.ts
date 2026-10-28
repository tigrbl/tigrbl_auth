export enum AuthenticatorEnum {
  PASSWORD_LOCAL = "password_local",
  API_KEY_LOCAL = "api_key_local",
  SERVICE_KEY_LOCAL = "service_key_local",
  CLIENT_SECRET_LOCAL = "client_secret_local",
  SESSION_LOCAL = "session_local",
  OTP_LOCAL = "otp_local",
  RECOVERY_CODE_LOCAL = "recovery_code_local",
  WEBAUTHN_LOCAL = "webauthn_local",
  MTLS_CLIENT_CERT = "mtls_client_cert",
  DPOP_PROOF = "dpop_proof",
  REMOTE_INTROSPECTION = "remote_introspection",
  FEDERATED_OIDC = "federated_oidc"
}

export enum DisplayCategory {
  HUMAN = "human",
  RECOVERY = "recovery",
  MACHINE = "machine",
  SUPPORTING = "supporting"
}

export enum CeremonyState {
  INITIALIZING = "initializing",
  READY = "ready",
  AWAITING_USER = "awaiting_user",
  AWAITING_EXTERNAL_PROVIDER = "awaiting_external_provider",
  SUBMITTING = "submitting",
  RETRYABLE_FAILURE = "retryable_failure",
  TERMINAL_FAILURE = "terminal_failure",
  EXPIRED = "expired",
  CANCELLED = "cancelled",
  BLOCKED = "blocked",
  SUCCEEDED = "succeeded",
  REQUIRES_NEXT_STEP = "requires_next_step"
}

export enum CeremonyPurpose {
  SIGN_IN = "sign-in",
  ENROLLMENT = "enrollment",
  VERIFICATION = "verification",
  STEP_UP = "step-up",
  RECOVERY = "recovery",
  LINKING = "linking",
  REPLACEMENT = "replacement",
  REMOVAL = "removal",
  REAUTHENTICATION = "reauthentication"
}

export interface Authenticator {
  id: string;
  name: string;
  type: AuthenticatorEnum;
  category: DisplayCategory;
  status: "active" | "suspended" | "revoked" | "expired" | "enrollment_pending" | "replacement_required";
  created: string;
  lastUsed?: string;
  metadata?: Record<string, any>;
  properties?: {
    phishingResistant: boolean;
    hardwareProtected: boolean;
    userPresent: boolean;
    userVerified: boolean;
    senderConstrained: boolean;
    replayResistant: boolean;
  };
}

export interface AuthenticatorPolicy {
  id: string;
  version: number;
  isActive: boolean;
  allowedMethods: AuthenticatorEnum[];
  requiredMethods: AuthenticatorEnum[];
  prohibitedMethods: AuthenticatorEnum[];
  attestationPolicy: "none" | "indirect" | "direct";
  algorithmPolicy: string[];
  mfaGracePeriodDays: number;
  requireHardwareProtection: boolean;
  updatedAt: string;
  updatedBy: string;
}

export interface Ceremony {
  id: string;
  type: AuthenticatorEnum;
  purpose: CeremonyPurpose;
  state: CeremonyState;
  subjectDisplayName: string;
  tenantId: string;
  realm: string;
  challengeDescriptor?: string;
  expiryTime: string;
  serverTime: string;
  attemptBudget: number;
  attemptsRemaining: number;
  retryAfterSeconds?: number;
  methodSwitchEligibility: AuthenticatorEnum[];
  requiredAcr?: string;
  achievedAcr?: string;
  riskSafeExplanation?: string;
  nextAction?: string;
  callbackTarget?: string;
  cancellationPolicy: "allowed" | "prohibited";
  errorCode?: string;
  safeRecoveryAction?: string;
  correlationId: string;
  evidence?: {
    amr: string[];
    properties: string[];
    time: string;
  };
}

export interface AuthEvent {
  id: string;
  timestamp: string;
  eventType: string;
  subjectId: string;
  tenantId: string;
  authenticatorType?: AuthenticatorEnum;
  authenticatorId?: string;
  success: boolean;
  ipAddress: string;
  location: string;
  acr?: string;
  amr?: string[];
  userAgent: string;
  details: string;
}

export interface ServerState {
  authenticators: Authenticator[];
  ceremonies: Record<string, Ceremony>;
  policies: AuthenticatorPolicy[];
  activePolicyId: string;
  events: AuthEvent[];
}
