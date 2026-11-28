/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from "react";
import {
  Shield,
  KeyRound,
  Lock,
  Unlock,
  AlertTriangle,
  CheckCircle2,
  XCircle,
  Clock,
  Eye,
  EyeOff,
  RefreshCw,
  User,
  Settings,
  History,
  AlertOctagon,
  ChevronRight,
  Info,
  Server,
  Smartphone,
  Sparkles,
  ArrowRight,
  X
} from "lucide-react";
import { motion, AnimatePresence } from "motion/react";

// --- TYPES & INTERFACES ---
export type AuthScreenId =
  | "identifier-first"
  | "password-entry"
  | "step-up"
  | "create-password"
  | "requirements-explanation"
  | "change-password"
  | "forced-change"
  | "forgot-password"
  | "reset-link-received"
  | "reset-completion"
  | "invalid-reset"
  | "compromised-response"
  | "password-detail"
  | "disable-remove"
  | "evidence-detail"
  | "policy-editor"
  | "user-posture"
  | "security-events"
  | "native-password";

export interface PasswordPolicy {
  minLength: number;
  requireUppercase: boolean;
  requireLowercase: boolean;
  requireNumbers: boolean;
  requireSpecial: boolean;
  blocklist: string[];
  blockBreachedSecrets: boolean;
  maxAttempts: number;
  rateLimitWindowsMs: number;
  forceResetIntervalDays: number;
}

export interface UserAccount {
  email: string;
  fullName: string;
  passwordHash: string;
  passwordCreatedDate: string;
  passwordChangedDate: string;
  passwordLastUsedDate: string;
  isPasswordRequired: boolean;
  hasMfaEnabled: boolean;
  hasWebAuthnEnabled: boolean;
  failedAttempts: number;
  isLocked: boolean;
  lockoutTime?: string;
  isCompromised: boolean;
  isExpired: boolean;
  needsForcedChange: boolean;
  accountStatus: "active" | "suspended" | "disabled";
}

export interface SecurityEvent {
  id: string;
  timestamp: string;
  eventType: string;
  severity: "info" | "warning" | "critical";
  description: string;
  ipAddress: string;
  userAgent: string;
  redactedDetails?: string;
}

export interface SessionEvidence {
  token: string;
  amr: string[];
  subject: string;
  authenticatedAt: string;
  freshnessSeconds: number;
  purpose: string;
  assuranceLevel: "AAL1" | "AAL2" | "AAL3";
  isStepUpVerified: boolean;
}

// --- INITIAL SIMULATED STATE DATA ---
const INITIAL_POLICY: PasswordPolicy = {
  minLength: 12,
  requireUppercase: true,
  requireLowercase: true,
  requireNumbers: true,
  requireSpecial: true,
  blocklist: ["password123", "qwerty123456", "admin12345", "welcome123"],
  blockBreachedSecrets: true,
  maxAttempts: 5,
  rateLimitWindowsMs: 60000,
  forceResetIntervalDays: 90,
};

const INITIAL_USER: UserAccount = {
  email: "alex.rivera@enterprise.com",
  fullName: "Alex Rivera",
  passwordHash: "SecureP@ss1234",
  passwordCreatedDate: "2026-04-15T09:00:00-07:00",
  passwordChangedDate: "2026-04-15T09:00:00-07:00",
  passwordLastUsedDate: "2026-07-14T18:22:11-07:00",
  isPasswordRequired: true,
  hasMfaEnabled: true,
  hasWebAuthnEnabled: false,
  failedAttempts: 0,
  isLocked: false,
  isCompromised: false,
  isExpired: false,
  needsForcedChange: false,
  accountStatus: "active",
};

const INITIAL_EVENTS: SecurityEvent[] = [
  {
    id: "evt-001",
    timestamp: "2026-07-15T10:15:30-07:00",
    eventType: "sign_in_success",
    severity: "info",
    description: "Successful login using AMR 'pwd'",
    ipAddress: "192.168.1.45",
    userAgent: "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Chrome/120.0.0",
    redactedDetails: "Assurance Level: AAL1, factor: password",
  },
  {
    id: "evt-002",
    timestamp: "2026-07-15T08:12:11-07:00",
    eventType: "password_compromise_detected",
    severity: "critical",
    description: "Password matching active breached-secret telemetry detected on external audit",
    ipAddress: "System Check",
    userAgent: "Breach-Watch Monitor v4.1",
    redactedDetails: "Database matching SHA-1 suffix blocklist check triggered",
  },
  {
    id: "evt-003",
    timestamp: "2026-07-14T22:45:00-07:00",
    eventType: "sign_in_failure",
    severity: "warning",
    description: "Failed password credential attempt",
    ipAddress: "203.0.113.12",
    userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    redactedDetails: "Redacted credentials mismatch, failure threshold: 1/5",
  },
  {
    id: "evt-004",
    timestamp: "2026-07-14T14:30:12-07:00",
    eventType: "policy_updated",
    severity: "info",
    description: "Password policy modified by tenant administrator",
    ipAddress: "10.0.2.11",
    userAgent: "AdminPortal/v2.4.0",
    redactedDetails: "Minimum length changed from 10 to 12. Breached check enabled.",
  },
];

export default function App() {
  // --- CORE STATE ---
  const [user, setUser] = useState<UserAccount>(INITIAL_USER);
  const [policy, setPolicy] = useState<PasswordPolicy>(INITIAL_POLICY);
  const [events, setEvents] = useState<SecurityEvent[]>(INITIAL_EVENTS);
  const [evidence, setEvidence] = useState<SessionEvidence | null>(null);

  // Flow & View States
  const [activeTab, setActiveTab] = useState<"p0" | "p1" | "p2">("p0");
  const [currentScreen, setCurrentScreen] = useState<AuthScreenId>("identifier-first");
  const [systemMessage, setSystemMessage] = useState<{ type: "success" | "error" | "info" | null; text: string | null }>({
    type: null,
    text: null,
  });

  // Authentication temporary fields
  const [identifier, setIdentifier] = useState(user.email);
  const [password, setPassword] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [mfaCode, setMfaCode] = useState("");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [simulatedLoadProgress, setSimulatedLoadProgress] = useState("");

  // Step up gate configuration
  const [pendingActionLabel, setPendingActionLabel] = useState<string>("");
  const [postStepUpScreen, setPostStepUpScreen] = useState<AuthScreenId | null>(null);

  // Recovery link token state
  const [resetToken, setResetToken] = useState<string | null>(null);
  const [resetTokenStatus, setResetTokenStatus] = useState<"pending" | "valid" | "expired" | "used">("pending");

  // Options to simulate adverse states
  const [simulateLocked, setSimulateLocked] = useState(false);
  const [simulateRateLimit, setSimulateRateLimit] = useState(false);
  const [simulateExpired, setSimulateExpired] = useState(false);
  const [simulateCompromised, setSimulateCompromised] = useState(false);

  // Session Invalidation Preferences
  const [invalidateAllSessions, setInvalAllSessions] = useState(true);

  // Dynamic feedback for password validation
  const [reqFeedback, setReqFeedback] = useState({
    lengthOk: false,
    upperOk: false,
    lowerOk: false,
    numberOk: false,
    specialOk: false,
    similarityOk: true,
    notInBlocklist: true,
    notBreached: true,
    passed: false,
  });

  // --- PASSWORD EVALUATION EFFECT ---
  useEffect(() => {
    const passwordText = newPassword;
    const lengthOk = passwordText.length >= policy.minLength;
    const upperOk = !policy.requireUppercase || /[A-Z]/.test(passwordText);
    const lowerOk = !policy.requireLowercase || /[a-z]/.test(passwordText);
    const numberOk = !policy.requireNumbers || /[0-9]/.test(passwordText);
    const specialOk = !policy.requireSpecial || /[^A-Za-z0-9]/.test(passwordText);
    const similarityOk = !user.email || !passwordText.toLowerCase().includes(user.email.split("@")[0].toLowerCase());
    const notInBlocklist = !policy.blocklist.some((b) => passwordText.toLowerCase().includes(b.toLowerCase()));
    
    const commonBreachedText = ["12345678", "password", "qwerty", "letmein", "sunshine", "iloveyou", "admin", "welcome"];
    const notBreached = !policy.blockBreachedSecrets || !commonBreachedText.some((b) => passwordText.toLowerCase().includes(b));

    const passed =
      lengthOk && upperOk && lowerOk && numberOk && specialOk && similarityOk && notInBlocklist && notBreached;

    setReqFeedback({
      lengthOk,
      upperOk,
      lowerOk,
      numberOk,
      specialOk,
      similarityOk,
      notInBlocklist,
      notBreached,
      passed,
    });
  }, [newPassword, policy, user.email]);

  // --- HELPER FUNCTION: ADD AUDIT LOG ---
  const addAuditLog = (
    eventType: string,
    severity: SecurityEvent["severity"],
    description: string,
    redactedDetails?: string
  ) => {
    const newEvent: SecurityEvent = {
      id: `evt-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString(),
      eventType,
      severity,
      description,
      ipAddress: "192.168.1.45",
      userAgent: "Verified Secure Browser Runtime",
      redactedDetails,
    };
    setEvents((prev) => [newEvent, ...prev]);
  };

  // --- ACTIONS ---

  // Handle Identifier First Submit
  const handleIdentifierSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier.trim()) {
      setSystemMessage({ type: "error", text: "Please enter a valid identifier." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Performing enumeration-safe tenant lookup...");
    setSystemMessage({ type: null, text: null });

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");
      setCurrentScreen("password-entry");
      addAuditLog("identifier_submitted", "info", `Identifier submitted: ${identifier} (safe status query)`, "Tenant verified, redirecting to pwd factor");
    }, 800);
  };

  // Handle Password authentication submit
  const handlePasswordSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setIsSubmitting(true);
    setSystemMessage({ type: null, text: null });
    setSimulatedLoadProgress("Verifying credentials against security policy v4.2...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");

      // 1. Check Locked state
      if (simulateLocked || user.isLocked) {
        setUser((prev) => ({ ...prev, isLocked: true }));
        setCurrentScreen("security-events");
        setSystemMessage({
          type: "error",
          text: "This account has been locked due to excessive failed attempts. Please contact security operations.",
        });
        addAuditLog("lockout", "critical", `Account lockout triggered for ${identifier}`, "Lockout threshold exceeded (5/5 failed attempts)");
        return;
      }

      // 2. Check Rate Limit simulation
      if (simulateRateLimit) {
        setSystemMessage({
          type: "error",
          text: "Too many requests. Please slow down and try again in 45 seconds.",
        });
        addAuditLog("sign_in_failure", "warning", `Rate limit triggered for ${identifier}`, "IP address 192.168.1.45 flagged temporary cooldown");
        return;
      }

      // 3. Verify Password Correctness
      if (password !== user.passwordHash) {
        setUser((prev) => {
          const nextAttempts = prev.failedAttempts + 1;
          const lock = nextAttempts >= policy.maxAttempts;
          return {
            ...prev,
            failedAttempts: nextAttempts,
            isLocked: lock,
          };
        });

        const failedNum = user.failedAttempts + 1;
        addAuditLog(
          "sign_in_failure",
          failedNum >= policy.maxAttempts ? "critical" : "warning",
          `Failed password credential attempt for ${identifier}`,
          `Attempt ${failedNum}/${policy.maxAttempts}. Redacted credential mismatch.`
        );

        if (failedNum >= policy.maxAttempts) {
          setSystemMessage({
            type: "error",
            text: "Maximum attempts reached. Your account is now locked for security purposes.",
          });
        } else {
          setSystemMessage({
            type: "error",
            text: `Invalid credentials. Please try again. (Attempt ${failedNum}/${policy.maxAttempts})`,
          });
        }
        return;
      }

      // 4. Force Change validation
      if (simulateExpired || user.isExpired || user.needsForcedChange) {
        setCurrentScreen("forced-change");
        addAuditLog("forced_change_triggered", "warning", `Forced password change required for ${identifier}`, "Password age exceeds policy max limits");
        return;
      }

      // 5. Compromised Password simulation check
      if (simulateCompromised || user.isCompromised) {
        setCurrentScreen("compromised-response");
        addAuditLog("password_compromise_detected", "critical", `Compromised password detected for ${identifier}`, "SHA-1 match in global breach corpus");
        return;
      }

      // Success Reset Attempts
      setUser((prev) => ({ ...prev, failedAttempts: 0 }));

      // MFA transitions
      if (user.hasMfaEnabled) {
        setCurrentScreen("step-up");
        setSystemMessage({ type: "info", text: "Identity verified. Multi-Factor authentication required." });
      } else {
        const freshEvidence: SessionEvidence = {
          token: "eyJhbGciOiJSUzI1NiIsImtpZCI6InB3ZF9hdXRoX2dhdGV3YXkifQ..." + Math.random().toString(36).substring(7),
          amr: ["pwd"],
          subject: user.email,
          authenticatedAt: new Date().toISOString(),
          freshnessSeconds: 0,
          purpose: "Primary Authentication Flow",
          assuranceLevel: "AAL1",
          isStepUpVerified: false,
        };
        setEvidence(freshEvidence);
        setCurrentScreen("evidence-detail");
        addAuditLog("sign_in_success", "info", `Successful user authentication via 'pwd'`, "AMR: pwd. Token produced and cryptographic evidence generated.");
      }
    }, 1200);
  };

  // Handle MFA step up
  const handleMfaSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!mfaCode || mfaCode.length < 6) {
      setSystemMessage({ type: "error", text: "Please enter a valid 6-digit authenticator token." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Verifying TOTP hardware key token...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");
      setMfaCode("");

      const freshEvidence: SessionEvidence = {
        token: "eyJhbGciOiJSUzI1NiIsImtpZCI6InB3ZF9hdXRoX2dhdGV3YXkifQ..." + Math.random().toString(36).substring(7),
        amr: ["pwd", "mfa"],
        subject: user.email,
        authenticatedAt: new Date().toISOString(),
        freshnessSeconds: 0,
        purpose: "Multi-Factor Authentication Flow",
        assuranceLevel: "AAL2",
        isStepUpVerified: true,
      };
      setEvidence(freshEvidence);

      if (postStepUpScreen) {
        setCurrentScreen(postStepUpScreen);
        setPostStepUpScreen(null);
      } else {
        setCurrentScreen("evidence-detail");
      }

      addAuditLog("mfa_success", "info", `MFA token validated successfully`, "AMR update: [pwd, mfa]. Session escalated to AAL2.");
      setSystemMessage({ type: "success", text: "Multi-factor authentication validated." });
    }, 900);
  };

  // Launch step-up gate for sensitive activities
  const triggerStepUpGate = (actionLabel: string, targetScreen: AuthScreenId) => {
    setPendingActionLabel(actionLabel);
    setPostStepUpScreen(targetScreen);
    setCurrentScreen("step-up");
    setSystemMessage({ type: "info", text: `Verification required for action: ${actionLabel}` });
  };

  // Handle Forgot Password Request
  const handleForgotPasswordRequest = (e: React.FormEvent) => {
    e.preventDefault();
    if (!identifier) {
      setSystemMessage({ type: "error", text: "Please enter your email identifier." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Generating safe token and outbound transaction...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");
      
      const tokenString = "rst_" + Math.random().toString(36).substring(2, 10);
      setResetToken(tokenString);
      setResetTokenStatus("valid");

      setSystemMessage({
        type: "success",
        text: "If that account exists in our records, we have sent instructions to reset your password. Please check your inbox.",
      });

      addAuditLog(
        "forgot_password_request",
        "info",
        `Password reset requested for identifier ${identifier}`,
        "Safe generic response dispatched. Outbound message queued."
      );
    }, 1000);
  };

  // Simulate receiving reset link
  const simulateResetLinkClick = () => {
    if (!resetToken) {
      setResetToken("rst_dummy123");
    }
    setResetTokenStatus("valid");
    setCurrentScreen("reset-link-received");
    setSystemMessage({ type: "info", text: "Secure reset link validated. Single-use token bound." });
    addAuditLog("reset_link_validated", "info", "Security reset link clicked and validated", "Token bound to browser user-agent and matching fingerprint.");
  };

  // Handle reset token verification and password change
  const handleResetCompletion = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPassword || !confirmPassword) {
      setSystemMessage({ type: "error", text: "Please enter and confirm your new password." });
      return;
    }
    if (newPassword !== confirmPassword) {
      setSystemMessage({ type: "error", text: "Passwords do not match. Please try again." });
      return;
    }
    if (!reqFeedback.passed) {
      setSystemMessage({ type: "error", text: "Password does not satisfy current cryptographic policies." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Consuming single-use token and invalidating active session tokens...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");

      if (resetTokenStatus === "expired" || resetTokenStatus === "used") {
        setCurrentScreen("invalid-reset");
        setSystemMessage({ type: "error", text: "This reset link has already been used or has expired." });
        addAuditLog("sign_in_failure", "warning", "Replay attack detected on reset token", `Attempted reuse of token ${resetToken}`);
        return;
      }

      setUser((prev) => ({
        ...prev,
        passwordHash: newPassword,
        passwordChangedDate: new Date().toISOString(),
        needsForcedChange: false,
        isExpired: false,
        isCompromised: false,
        failedAttempts: 0,
        isLocked: false,
      }));

      setResetTokenStatus("used");
      setNewPassword("");
      setConfirmPassword("");

      setSystemMessage({ type: "success", text: "Your password has been successfully reset. You may now sign in." });
      setCurrentScreen("password-entry");
      addAuditLog("reset_completed", "info", "Password reset successfully completed", "Active browser session tokens invalidated.");
    }, 1200);
  };

  // Handle standard change password
  const handleChangePassword = (e: React.FormEvent) => {
    e.preventDefault();
    if (!password || !newPassword || !confirmPassword) {
      setSystemMessage({ type: "error", text: "All fields are required." });
      return;
    }
    if (password !== user.passwordHash) {
      setSystemMessage({ type: "error", text: "The current password entered is incorrect." });
      return;
    }
    if (newPassword !== confirmPassword) {
      setSystemMessage({ type: "error", text: "New passwords do not match." });
      return;
    }
    if (!reqFeedback.passed) {
      setSystemMessage({ type: "error", text: "The new password does not meet strength guidelines." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Verifying entropy and checking similarity thresholds...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");

      setUser((prev) => ({
        ...prev,
        passwordHash: newPassword,
        passwordChangedDate: new Date().toISOString(),
      }));

      setPassword("");
      setNewPassword("");
      setConfirmPassword("");

      setSystemMessage({ type: "success", text: "Password changed successfully." });
      setCurrentScreen("password-detail");
      addAuditLog("password_change", "info", "Password successfully changed by owner", `Session invalidation setting: ${invalidateAllSessions ? "all" : "current"}`);
    }, 1000);
  };

  // Handle forced password change
  const handleForcedChangeSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPassword || !confirmPassword) {
      setSystemMessage({ type: "error", text: "All fields are required." });
      return;
    }
    if (newPassword !== confirmPassword) {
      setSystemMessage({ type: "error", text: "New passwords do not match." });
      return;
    }
    if (!reqFeedback.passed) {
      setSystemMessage({ type: "error", text: "Password does not satisfy server-enforced policy." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Applying forced-change and renewing lifecycle dates...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");

      setUser((prev) => ({
        ...prev,
        passwordHash: newPassword,
        passwordChangedDate: new Date().toISOString(),
        needsForcedChange: false,
        isExpired: false,
      }));

      setNewPassword("");
      setConfirmPassword("");

      setSystemMessage({ type: "success", text: "Required password change complete. Account access restored." });
      setCurrentScreen("password-entry");
      addAuditLog("forced_change_completed", "info", "Required forced password change completed", "Lifecycle constraints cleared successfully.");
    }, 1100);
  };

  // Handle initial creation
  const handleCreatePassword = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newPassword || !confirmPassword) {
      setSystemMessage({ type: "error", text: "Please enter your password." });
      return;
    }
    if (newPassword !== confirmPassword) {
      setSystemMessage({ type: "error", text: "Passwords do not match." });
      return;
    }
    if (!reqFeedback.passed) {
      setSystemMessage({ type: "error", text: "Password does not satisfy server policy criteria." });
      return;
    }

    setIsSubmitting(true);
    setSimulatedLoadProgress("Enrolling brand new password credential into tenant realm...");

    setTimeout(() => {
      setIsSubmitting(false);
      setSimulatedLoadProgress("");

      setUser((prev) => ({
        ...prev,
        passwordHash: newPassword,
        passwordCreatedDate: new Date().toISOString(),
        passwordChangedDate: new Date().toISOString(),
        isPasswordRequired: true,
      }));

      setNewPassword("");
      setConfirmPassword("");

      setSystemMessage({ type: "success", text: "Initial password enrollment complete." });
      setCurrentScreen("password-detail");
      addAuditLog("password_change", "info", "Initial password credential enrolled", "Ceremony complete, MFA tokens remained active");
    }, 1100);
  };

  // Handle password deactivation
  const handleDisablePassword = () => {
    if (user.hasWebAuthnEnabled || user.hasMfaEnabled) {
      setIsSubmitting(true);
      setSimulatedLoadProgress("De-provisioning password factor from authentication list...");

      setTimeout(() => {
        setIsSubmitting(false);
        setSimulatedLoadProgress("");

        setUser((prev) => ({
          ...prev,
          isPasswordRequired: false,
        }));

        setSystemMessage({
          type: "success",
          text: "Password successfully deactivated. You may now log in strictly using WebAuthn / Passkeys.",
        });
        setCurrentScreen("password-detail");
        addAuditLog("password_disabled", "critical", "Password credential deactivated by user", "Transitioned to pure passwordless (AAL2 key required)");
      }, 1000);
    } else {
      setSystemMessage({
        type: "error",
        text: "You must have another strong credential (like Passkeys or Authenticator) active before disabling passwords.",
      });
    }
  };

  // Admin forced password reset trigger
  const triggerAdminForcedReset = () => {
    setUser((prev) => ({ ...prev, needsForcedChange: true }));
    addAuditLog("admin_action", "warning", "Forced password change administratively flagged", "Triggered by security administrator Alex.");
    setSystemMessage({ type: "success", text: "Forced change flag enabled for this user. They will be prompted on next sign-in." });
  };

  // Admin simulated password unlock
  const triggerAdminUnlock = () => {
    setUser((prev) => ({ ...prev, isLocked: false, failedAttempts: 0 }));
    addAuditLog("admin_action", "info", "Account unlock processed by administrator", "Redacted brute-force audit parameters cleared.");
    setSystemMessage({ type: "success", text: "User account unlocked successfully." });
  };

  // Admin update policy settings
  const updatePolicy = (newPolicy: Partial<PasswordPolicy>) => {
    setPolicy((prev) => {
      const updated = { ...prev, ...newPolicy };
      addAuditLog(
        "policy_updated",
        "info",
        "Credential policy update committed",
        `New configuration - Length: ${updated.minLength}, Breached-Secret check: ${updated.blockBreachedSecrets}`
      );
      return updated;
    });
    setSystemMessage({ type: "success", text: "Password policy saved and propagated globally." });
  };

  const handleFillMockValid = () => {
    setNewPassword("SecureP@ss1234");
    setConfirmPassword("SecureP@ss1234");
  };

  const handleFillMockCommon = () => {
    setNewPassword("password123");
    setConfirmPassword("password123");
  };

  // --- RENDERING SHARED COMPONENTS ---

  const PasswordFieldComponent = ({
    label,
    value,
    onChange,
    id,
    placeholder = "••••••••••••",
    autoComplete,
    rightElement,
  }: {
    label: string;
    value: string;
    onChange: (val: string) => void;
    id: string;
    placeholder?: string;
    autoComplete?: string;
    rightElement?: React.ReactNode;
  }) => {
    const [show, setShow] = useState(false);
    return (
      <div className="space-y-1.5" id={`field-container-${id}`}>
        <div className="flex justify-between items-center">
          <label className="text-xs font-semibold text-slate-700 font-sans tracking-wide" htmlFor={id}>
            {label}
          </label>
          {rightElement}
        </div>
        <div className="relative">
          <input
            id={id}
            type={show ? "text" : "password"}
            value={value}
            onChange={(e) => onChange(e.target.value)}
            className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 font-mono text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
            placeholder={placeholder}
            autoComplete={autoComplete}
            data-testid={id}
          />
          <button
            type="button"
            onClick={() => setShow(!show)}
            className="absolute right-2.5 top-2 text-slate-400 hover:text-slate-600 transition-colors focus:outline-none"
            aria-label={show ? "Hide password" : "Show password"}
          >
            {show ? <EyeOff className="w-4.5 h-4.5" /> : <Eye className="w-4.5 h-4.5" />}
          </button>
        </div>
      </div>
    );
  };

  const PasswordRequirementsComponent = () => {
    const items = [
      { key: "lengthOk", label: `At least ${policy.minLength} characters` },
      { key: "upperOk", label: "One uppercase letter (A-Z)" },
      { key: "lowerOk", label: "One lowercase letter (a-z)" },
      { key: "numberOk", label: "One number (0-9)" },
      { key: "specialOk", label: "One special character (e.g., @, #, $, %)" },
      { key: "similarityOk", label: "Not match/contain user identity details" },
      { key: "notInBlocklist", label: "Not containing blocklist terms" },
      { key: "notBreached", label: "Passes global breached secret search" },
    ];

    return (
      <div className="bg-slate-50 border border-slate-200/60 rounded-xl p-4 space-y-2.5" id="password-req-panel">
        <div className="flex items-center gap-2 mb-1.5">
          <Shield className="w-4 h-4 text-indigo-600" />
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-widest">Enforced Security Criteria</h4>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-xs">
          {items.map((item) => {
            const passed = reqFeedback[item.key as keyof typeof reqFeedback];
            return (
              <div key={item.key} className="flex items-center gap-2 text-slate-600">
                {passed ? (
                  <CheckCircle2 className="w-4 h-4 text-green-500 shrink-0" />
                ) : (
                  <div className="w-4 h-4 rounded-full border border-slate-300 shrink-0 flex items-center justify-center text-[8px] text-slate-400 font-bold font-mono">
                    !
                  </div>
                )}
                <span className={passed ? "text-slate-700 font-medium" : "text-slate-500"}>{item.label}</span>
              </div>
            );
          })}
        </div>
      </div>
    );
  };

  const CeremonyShell = ({ children, title, subtitle, statusText = "Ready" }: { children: React.ReactNode; title: string; subtitle: string; statusText?: string }) => {
    return (
      <div className="flex-1 bg-white border border-slate-200 rounded-2xl shadow-sm flex flex-col overflow-hidden h-full min-h-[500px]" id="ceremony-shell-container">
        <div className="h-1 w-full bg-gradient-to-r from-indigo-500 via-indigo-600 to-indigo-700"></div>

        <div className="p-8 flex-1 flex flex-col justify-between overflow-y-auto">
          <div className="mb-6">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-[10px] bg-slate-100 text-slate-600 border border-slate-200 px-2 py-0.5 rounded-full font-mono uppercase font-bold">
                pwd CEREMONY
              </span>
              <span className="text-[10px] bg-indigo-50 text-indigo-600 px-2 py-0.5 rounded-full font-mono uppercase font-bold">
                AMR CORE
              </span>
            </div>
            <h2 className="text-xl font-bold tracking-tight text-slate-900 font-display">{title}</h2>
            <p className="text-slate-500 text-xs mt-1 leading-relaxed">{subtitle}</p>
          </div>

          <div className="flex-1 flex flex-col justify-center">
            {children}
          </div>

          {isSubmitting && (
            <div className="mt-4 p-3 bg-indigo-50 text-indigo-700 border border-indigo-100 rounded-lg flex items-center gap-3 animate-pulse">
              <RefreshCw className="w-4 h-4 animate-spin text-indigo-600 shrink-0" />
              <p className="text-xs font-semibold leading-none">{simulatedLoadProgress || "Contacting security subsystem..."}</p>
            </div>
          )}

          <div className="mt-6 pt-4 border-t border-slate-100 flex items-center justify-between gap-4 text-[10px] text-slate-400 font-mono">
            <span>Status: <span className="text-slate-600 font-bold">{statusText}</span></span>
            <span>Cryptographic Mode: SHA-256 / PBKDF2</span>
          </div>
        </div>
      </div>
    );
  };

  return (
    <div className="flex flex-col h-screen w-screen bg-slate-50 font-sans text-slate-900 overflow-hidden select-none" id="app-root-container">
      
      {/* HEADER SECTION */}
      <header className="h-16 flex items-center justify-between px-6 bg-white border-b border-slate-200 shrink-0 shadow-sm" id="main-header">
        <div className="flex items-center gap-4">
          <div className="w-9 h-9 bg-indigo-600 rounded-xl flex items-center justify-center text-white font-bold text-lg shadow-md shadow-indigo-100">
            P
          </div>
          <div>
            <h1 className="text-sm font-bold tracking-wider text-slate-800 uppercase font-display flex items-center gap-2">
              Password AMR <span className="text-indigo-600 font-light">\ pwd</span>
            </h1>
            <p className="text-[10px] text-slate-400 font-mono">Knowledge Factor Enrollment & lifecycle gate</p>
          </div>
        </div>

        <div className="flex gap-4 items-center">
          <div className="flex items-center gap-2 px-3 py-1 bg-green-50 text-green-700 border border-green-200 rounded-full text-[10px] font-bold tracking-wide">
            <div className="w-1.5 h-1.5 rounded-full bg-green-500 animate-pulse"></div>
            CORE VERIFICATION ACTIVE
          </div>
          <div className="text-slate-400 font-mono text-xs hidden sm:block">v2.5.0-release</div>
        </div>
      </header>

      {/* SYSTEM BROADCAST MESSAGE BAR */}
      {systemMessage.text && (
        <div
          className={`px-6 py-2.5 flex items-center justify-between text-xs transition-colors shrink-0 ${
            systemMessage.type === "error"
              ? "bg-red-50 text-red-700 border-b border-red-100"
              : systemMessage.type === "success"
              ? "bg-green-50 text-green-700 border-b border-green-100"
              : "bg-indigo-50 text-indigo-700 border-b border-indigo-100"
          }`}
          id="system-broadcast"
        >
          <div className="flex items-center gap-2">
            {systemMessage.type === "error" ? (
              <XCircle className="w-4 h-4 text-red-500" />
            ) : systemMessage.type === "success" ? (
              <CheckCircle2 className="w-4 h-4 text-green-500" />
            ) : (
              <Info className="w-4 h-4 text-indigo-500" />
            )}
            <p className="font-medium">{systemMessage.text}</p>
          </div>
          <button
            onClick={() => setSystemMessage({ type: null, text: null })}
            className="text-slate-400 hover:text-slate-600"
          >
            <X className="w-3.5 h-3.5" />
          </button>
        </div>
      )}

      {/* CORE GRID MAIN CONTAINER */}
      <main className="flex-1 grid grid-cols-12 overflow-hidden" id="main-grid">
        
        {/* LEFT SIDEBAR: FLOW CONTROLS & ADVERSE STATES (col-span-3) */}
        <aside className="col-span-3 bg-white border-r border-slate-200 flex flex-col p-5 overflow-y-auto" id="flow-controls-sidebar">
          <div className="flex bg-slate-100 p-1 rounded-lg gap-1 mb-5 text-xs font-semibold">
            <button
              onClick={() => setActiveTab("p0")}
              className={`flex-1 text-center py-1.5 rounded-md transition-all ${
                activeTab === "p0" ? "bg-white text-slate-800 shadow-xs" : "text-slate-500 hover:text-slate-800"
              }`}
            >
              P0 — Sign-in
            </button>
            <button
              onClick={() => setActiveTab("p1")}
              className={`flex-1 text-center py-1.5 rounded-md transition-all ${
                activeTab === "p1" ? "bg-white text-slate-800 shadow-xs" : "text-slate-500 hover:text-slate-800"
              }`}
            >
              P1 — Lifecycle
            </button>
            <button
              onClick={() => setActiveTab("p2")}
              className={`flex-1 text-center py-1.5 rounded-md transition-all ${
                activeTab === "p2" ? "bg-white text-slate-800 shadow-xs" : "text-slate-500 hover:text-slate-800"
              }`}
            >
              P2 — Ops / Admin
            </button>
          </div>

          <div className="flex-1 space-y-5">
            {activeTab === "p0" && (
              <div className="space-y-4">
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Core Auth Sequence</p>
                  <div className="space-y-1">
                    {[
                      { id: "identifier-first", label: "Identifier entry" },
                      { id: "password-entry", label: "Password submission" },
                      { id: "step-up", label: "MFA / Step-up Verification" },
                      { id: "evidence-detail", label: "Auth Evidence (AMR Token)" },
                    ].map((s) => (
                      <button
                        key={s.id}
                        onClick={() => setCurrentScreen(s.id as AuthScreenId)}
                        className={`w-full text-left px-3 py-2 text-xs rounded-lg flex items-center justify-between font-medium transition-all ${
                          currentScreen === s.id
                            ? "bg-indigo-50 text-indigo-700 border border-indigo-100"
                            : "text-slate-600 hover:bg-slate-50 border border-transparent"
                        }`}
                      >
                        <span>{s.label}</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Adverse State Simulation</p>
                  <div className="bg-slate-50 border border-slate-200 rounded-xl p-3 space-y-3">
                    <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={simulateLocked}
                        onChange={(e) => setSimulateLocked(e.target.checked)}
                        className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                      />
                      <div>
                        <span className="font-semibold block">Lock Account</span>
                        <span className="text-[10px] text-slate-400">Trigger excessive attempts lockout</span>
                      </div>
                    </label>

                    <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={simulateRateLimit}
                        onChange={(e) => setSimulateRateLimit(e.target.checked)}
                        className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                      />
                      <div>
                        <span className="font-semibold block">Rate-Limit IP</span>
                        <span className="text-[10px] text-slate-400">Force generic client cooldown</span>
                      </div>
                    </label>

                    <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={simulateExpired}
                        onChange={(e) => setSimulateExpired(e.target.checked)}
                        className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                      />
                      <div>
                        <span className="font-semibold block">Expired Password</span>
                        <span className="text-[10px] text-slate-400">Force immediate rotation on login</span>
                      </div>
                    </label>

                    <label className="flex items-center gap-2 text-xs text-slate-700 cursor-pointer">
                      <input
                        type="checkbox"
                        checked={simulateCompromised}
                        onChange={(e) => setSimulateCompromised(e.target.checked)}
                        className="rounded text-indigo-600 focus:ring-indigo-500 w-3.5 h-3.5"
                      />
                      <div>
                        <span className="font-semibold block">Compromised Credential</span>
                        <span className="text-[10px] text-slate-400">Trigger breached-secret lock</span>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
            )}

            {activeTab === "p1" && (
              <div className="space-y-4">
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Enrollment & Transitions</p>
                  <div className="space-y-1">
                    {[
                      { id: "create-password", label: "Initial password setup" },
                      { id: "requirements-explanation", label: "Policy expectations" },
                      { id: "change-password", label: "Regular change request" },
                      { id: "forced-change", label: "Required forced change" },
                      { id: "disable-remove", label: "Disable password factor" },
                    ].map((s) => (
                      <button
                        key={s.id}
                        onClick={() => setCurrentScreen(s.id as AuthScreenId)}
                        className={`w-full text-left px-3 py-2 text-xs rounded-lg flex items-center justify-between font-medium transition-all ${
                          currentScreen === s.id
                            ? "bg-indigo-50 text-indigo-700 border border-indigo-100"
                            : "text-slate-600 hover:bg-slate-50 border border-transparent"
                        }`}
                      >
                        <span>{s.label}</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                      </button>
                    ))}
                  </div>
                </div>

                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Recovery & Out-of-band</p>
                  <div className="space-y-1">
                    {[
                      { id: "forgot-password", label: "Forgot credential form" },
                      { id: "reset-link-received", label: "Verify reset callback" },
                      { id: "reset-completion", label: "Reset password entry" },
                      { id: "invalid-reset", label: "Expired/Replayed token state" },
                      { id: "compromised-response", label: "Security threat warning" },
                      { id: "password-detail", label: "Credential dashboard detail" },
                    ].map((s) => (
                      <button
                        key={s.id}
                        onClick={() => setCurrentScreen(s.id as AuthScreenId)}
                        className={`w-full text-left px-3 py-2 text-xs rounded-lg flex items-center justify-between font-medium transition-all ${
                          currentScreen === s.id
                            ? "bg-indigo-50 text-indigo-700 border border-indigo-100"
                            : "text-slate-600 hover:bg-slate-50 border border-transparent"
                        }`}
                      >
                        <span>{s.label}</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                      </button>
                    ))}
                  </div>

                  {resetToken && (
                    <div className="mt-3 p-2.5 bg-indigo-50 rounded-lg border border-indigo-100">
                      <p className="text-[9px] font-bold text-indigo-500 uppercase tracking-wide font-mono">Outbound Email Mock</p>
                      <p className="text-[10px] text-slate-600 mt-1">A recovery token was dispatched.</p>
                      <button
                        onClick={simulateResetLinkClick}
                        className="mt-2 w-full py-1.5 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold rounded text-[10px] tracking-wide transition-colors"
                      >
                        Simulate Link Click
                      </button>
                    </div>
                  )}
                </div>
              </div>
            )}

            {activeTab === "p2" && (
              <div className="space-y-4">
                <div>
                  <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest mb-2">Administration Panels</p>
                  <div className="space-y-1">
                    {[
                      { id: "policy-editor", label: "Global Policy settings" },
                      { id: "user-posture", label: "User security posture" },
                      { id: "security-events", label: "Diagnostics & audit logs" },
                      { id: "native-password", label: "Native application layout" },
                    ].map((s) => (
                      <button
                        key={s.id}
                        onClick={() => setCurrentScreen(s.id as AuthScreenId)}
                        className={`w-full text-left px-3 py-2 text-xs rounded-lg flex items-center justify-between font-medium transition-all ${
                          currentScreen === s.id
                            ? "bg-indigo-50 text-indigo-700 border border-indigo-100"
                            : "text-slate-600 hover:bg-slate-50 border border-transparent"
                        }`}
                      >
                        <span>{s.label}</span>
                        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
                      </button>
                    ))}
                  </div>
                </div>

                <div className="p-3 bg-indigo-50 border border-indigo-100 rounded-xl space-y-1 text-xs">
                  <span className="text-[10px] font-bold text-indigo-600 uppercase tracking-wider block font-mono">Security Insights</span>
                  <div className="flex justify-between font-medium mt-1">
                    <span className="text-slate-500 font-sans">MFA Coverage:</span>
                    <span className="text-slate-800 font-semibold font-mono">98.2%</span>
                  </div>
                  <div className="flex justify-between font-medium">
                    <span className="text-slate-500 font-sans">Postures verified:</span>
                    <span className="text-green-600 font-bold font-sans">100% Secure</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          <div className="mt-auto pt-4 border-t border-slate-200">
            <button
              onClick={() => {
                setUser(INITIAL_USER);
                setPolicy(INITIAL_POLICY);
                setEvents(INITIAL_EVENTS);
                setEvidence(null);
                setSystemMessage({ type: "success", text: "Simulated directory database reset to defaults." });
                addAuditLog("admin_action", "info", "Local simulation state reset requested", "Tenant state initialized to standard secure profile.");
              }}
              className="w-full py-1.5 border border-slate-200 hover:bg-slate-50 text-slate-600 hover:text-slate-800 text-[10px] font-bold uppercase tracking-wider rounded-lg flex items-center justify-center gap-1.5 transition-colors"
            >
              <RefreshCw className="w-3 h-3" /> Reset Mock Data
            </button>
          </div>
        </aside>

        {/* MIDDLE CONTENT: HIGH-FIDELITY INTERACTIVE CARDS (col-span-5) */}
        <section className="col-span-5 bg-slate-50 p-6 flex flex-col justify-center overflow-y-auto" id="main-content-display">
          <AnimatePresence mode="wait">
            <motion.div
              key={currentScreen}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              transition={{ duration: 0.2 }}
              className="h-full max-w-lg mx-auto w-full flex flex-col justify-center"
            >
              {/* SCREEN 1: IDENTIFIER FIRST LOGIN */}
              {currentScreen === "identifier-first" && (
                <CeremonyShell
                  title="Verify Account Identification"
                  subtitle="Please enter your enterprise identifier to continue"
                >
                  <form onSubmit={handleIdentifierSubmit} className="space-y-5" id="form-identifier-first">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-slate-700" htmlFor="email-identifier">
                        Enterprise Email / Account ID
                      </label>
                      <input
                        id="email-identifier"
                        type="email"
                        value={identifier}
                        onChange={(e) => setIdentifier(e.target.value)}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                        placeholder="e.g. user@enterprise.com"
                        required
                        autoComplete="username"
                      />
                    </div>
                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full py-2.5 bg-slate-900 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-md hover:bg-slate-800 active:scale-98 transition-all flex items-center justify-center gap-1.5 cursor-pointer"
                    >
                      Continue <ArrowRight className="w-3.5 h-3.5" />
                    </button>
                    
                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-200/50 flex gap-2">
                      <Info className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                      <p className="text-[10px] text-slate-500 leading-relaxed font-sans">
                        <strong>Enumeration-Safe Protection:</strong> The timing and client response of this verification step will remain strictly identical whether the account exists or not to prevent hostile profiling.
                      </p>
                    </div>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 2: PASSWORD SIGN-IN */}
              {currentScreen === "password-entry" && (
                <CeremonyShell
                  title="Enter Password"
                  subtitle={`Security context validated for: ${identifier}`}
                >
                  <form onSubmit={handlePasswordSubmit} className="space-y-5" id="form-password-entry">
                    <div className="flex items-center gap-2 p-2 bg-slate-50 rounded-lg border border-slate-200/50 mb-1">
                      <div className="w-6 h-6 rounded-full bg-slate-200 flex items-center justify-center text-slate-600 font-bold text-xs uppercase font-sans">
                        {identifier.charAt(0)}
                      </div>
                      <div className="truncate">
                        <p className="text-[11px] font-semibold text-slate-800 truncate font-sans">{identifier}</p>
                        <p className="text-[9px] text-slate-400 font-mono">ID: usr_8842</p>
                      </div>
                      <button
                        type="button"
                        onClick={() => setCurrentScreen("identifier-first")}
                        className="ml-auto text-[10px] text-indigo-600 font-semibold hover:underline font-sans"
                      >
                        Change
                      </button>
                    </div>

                    <PasswordFieldComponent
                      label="Your Account Password"
                      id="current-password-input"
                      value={password}
                      onChange={setPassword}
                      autoComplete="current-password"
                      rightElement={
                        <button
                          type="button"
                          onClick={() => setCurrentScreen("forgot-password")}
                          className="text-xs text-indigo-600 font-medium hover:underline font-sans"
                        >
                          Forgot Password?
                        </button>
                      }
                    />

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full py-2.5 bg-slate-900 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-md hover:bg-slate-800 active:scale-98 transition-all flex items-center justify-center cursor-pointer font-sans"
                    >
                      Authenticate Securely
                    </button>

                    <div className="flex justify-between items-center text-[10px] text-slate-400 font-mono">
                      <span>Rate limit threshold: 5 attempts</span>
                      <span className="flex items-center gap-1">
                        <Lock className="w-3 h-3 text-green-500" /> AES-256 Transport
                      </span>
                    </div>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 3: PASSWORD STEP-UP / REAUTHENTICATION */}
              {currentScreen === "step-up" && (
                <CeremonyShell
                  title="Multi-Factor Verification Required"
                  subtitle={pendingActionLabel ? `Authorize sensitive action: "${pendingActionLabel}"` : "Escalate authorization session to Level 2"}
                >
                  <form onSubmit={handleMfaSubmit} className="space-y-5" id="form-step-up-mfa">
                    <div className="p-4 bg-indigo-50 border border-indigo-100 rounded-xl flex gap-3 text-indigo-950">
                      <Shield className="w-5 h-5 text-indigo-600 shrink-0 mt-0.5 animate-pulse" />
                      <div>
                        <h4 className="text-xs font-bold uppercase tracking-wider font-mono">Session Security Gate</h4>
                        <p className="text-[11px] text-indigo-700 mt-1 leading-relaxed font-sans">
                          Your active session has AMR <strong>[pwd]</strong>. Performing this action requires verifying your second factor (AMR: <strong>[mfa]</strong>) to achieve Assurance Level AAL2.
                        </p>
                      </div>
                    </div>

                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-slate-700" htmlFor="totp-code-input">
                        Authenticator Code (TOTP)
                      </label>
                      <input
                        id="totp-code-input"
                        type="text"
                        maxLength={6}
                        value={mfaCode}
                        onChange={(e) => setMfaCode(e.target.value.replace(/\D/g, ""))}
                        className="w-full text-center tracking-widest font-mono text-lg px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                        placeholder="000000"
                        required
                      />
                    </div>

                    <div className="flex gap-2">
                      <button
                        type="button"
                        onClick={() => {
                          setMfaCode("123456");
                        }}
                        className="flex-1 py-1 px-2 border border-slate-200 rounded text-[10px] text-slate-500 hover:bg-slate-50"
                      >
                        Auto-fill Mock Code (123456)
                      </button>
                      <button
                        type="button"
                        onClick={() => {
                          setCurrentScreen("password-entry");
                        }}
                        className="px-3 py-1 border border-slate-200 rounded text-[10px] text-slate-500 hover:bg-slate-50"
                      >
                        Back
                      </button>
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full py-2.5 bg-indigo-600 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-md hover:bg-indigo-700 active:scale-98 transition-all flex items-center justify-center cursor-pointer font-sans"
                    >
                      Verify Factor
                    </button>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 4: CREATE PASSWORD */}
              {currentScreen === "create-password" && (
                <CeremonyShell
                  title="Configure Your Security Password"
                  subtitle="Enroll your initial credentials into the tenant realm"
                >
                  <form onSubmit={handleCreatePassword} className="space-y-4" id="form-create-password">
                    <PasswordFieldComponent
                      label="Choose Password"
                      id="new-password-enroll"
                      value={newPassword}
                      onChange={setNewPassword}
                      autoComplete="new-password"
                    />

                    <PasswordFieldComponent
                      label="Confirm Your Password"
                      id="confirm-password-enroll"
                      value={confirmPassword}
                      onChange={setConfirmPassword}
                      autoComplete="new-password"
                    />

                    <PasswordRequirementsComponent />

                    <div className="flex gap-2 justify-end">
                      <button
                        type="button"
                        onClick={handleFillMockValid}
                        className="py-1 px-2 bg-slate-100 hover:bg-slate-200 rounded text-[10px] text-slate-600 font-semibold font-sans"
                      >
                        Fill Strong mock
                      </button>
                      <button
                        type="button"
                        onClick={handleFillMockCommon}
                        className="py-1 px-2 bg-red-50 hover:bg-red-100 text-red-600 rounded text-[10px] font-semibold font-sans"
                      >
                        Fill Common mock
                      </button>
                    </div>

                    <button
                      type="submit"
                      disabled={isSubmitting || !reqFeedback.passed}
                      className={`w-full py-2.5 text-xs font-bold uppercase tracking-wider rounded-lg shadow-md transition-all flex items-center justify-center cursor-pointer font-sans ${
                        reqFeedback.passed
                          ? "bg-indigo-600 text-white hover:bg-indigo-700"
                          : "bg-slate-200 text-slate-400 cursor-not-allowed"
                      }`}
                    >
                      Enroll Password Credential
                    </button>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 5: PASSWORD REQUIREMENTS EXPLANATION */}
              {currentScreen === "requirements-explanation" && (
                <CeremonyShell
                  title="Password Complexity Regulations"
                  subtitle="Standard requirements enforced on administrative and personal user accounts"
                >
                  <div className="space-y-4" id="view-requirements-explanation">
                    <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3">
                      <div className="flex gap-2 items-center text-slate-800 font-bold text-xs uppercase tracking-wide font-sans">
                        <Settings className="w-4 h-4 text-indigo-600" /> Current Policy Rules
                      </div>
                      <div className="space-y-2 text-xs text-slate-600 font-sans">
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Minimum Character Length:</span>
                          <span className="font-mono font-bold text-slate-800">{policy.minLength} characters</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Require Uppercase Letter:</span>
                          <span className="font-semibold text-slate-800">{policy.requireUppercase ? "YES" : "NO"}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Require Lowercase Letter:</span>
                          <span className="font-semibold text-slate-800">{policy.requireLowercase ? "YES" : "NO"}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Require Numerical Digits:</span>
                          <span className="font-semibold text-slate-800">{policy.requireNumbers ? "YES" : "NO"}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Require Special Symbols:</span>
                          <span className="font-semibold text-slate-800">{policy.requireSpecial ? "YES" : "NO"}</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1.5">
                          <span>Global Breach Blocklist:</span>
                          <span className="text-red-600 font-bold">Enabled (Breach-Watch)</span>
                        </div>
                      </div>
                    </div>

                    <div className="p-3 bg-indigo-50 text-indigo-950 border border-indigo-100 rounded-xl flex gap-2">
                      <Shield className="w-5 h-5 text-indigo-600 shrink-0" />
                      <p className="text-[11px] leading-relaxed font-sans">
                        Our system utilizes <strong>Breach-Watch Monitor telemetry</strong> to instantly deny any password that has previously appeared in public leak databases, preventing dictionary attacks.
                      </p>
                    </div>

                    <button
                      onClick={() => setCurrentScreen("create-password")}
                      className="w-full py-2 bg-slate-900 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow hover:bg-slate-800 transition-all flex items-center justify-center gap-1 cursor-pointer font-sans"
                    >
                      Proceed to Setup <ArrowRight className="w-4 h-4" />
                    </button>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 6: CHANGE PASSWORD */}
              {currentScreen === "change-password" && (
                <CeremonyShell
                  title="Modify Account Password"
                  subtitle="Verify current knowledge credential to assign a secure replacement"
                >
                  <form onSubmit={handleChangePassword} className="space-y-4" id="form-change-password">
                    <PasswordFieldComponent
                      label="Current Active Password"
                      id="current-password-verify"
                      value={password}
                      onChange={setPassword}
                      autoComplete="current-password"
                    />

                    <PasswordFieldComponent
                      label="New Secure Password"
                      id="new-password-change"
                      value={newPassword}
                      onChange={setNewPassword}
                      autoComplete="new-password"
                    />

                    <PasswordFieldComponent
                      label="Confirm New Password"
                      id="confirm-password-change"
                      value={confirmPassword}
                      onChange={setConfirmPassword}
                      autoComplete="new-password"
                    />

                    <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block font-mono">Session Control Preference</span>
                      <label className="flex items-start gap-2 text-xs text-slate-700 cursor-pointer font-sans">
                        <input
                          type="checkbox"
                          checked={invalidateAllSessions}
                          onChange={(e) => setInvalAllSessions(e.target.checked)}
                          className="rounded text-indigo-600 focus:ring-indigo-500 mt-0.5"
                        />
                        <div>
                          <span className="font-bold text-slate-800 block">Revoke all other active session tokens</span>
                          <p className="text-[10px] text-slate-400">Instantly sign out of other devices and APIs for maximum containment.</p>
                        </div>
                      </label>
                    </div>

                    {newPassword && <PasswordRequirementsComponent />}

                    <button
                      type="submit"
                      disabled={isSubmitting}
                      className="w-full py-2.5 bg-slate-900 text-white text-xs font-bold uppercase tracking-wider rounded-lg shadow-md hover:bg-slate-800 transition-all flex items-center justify-center cursor-pointer font-sans"
                    >
                      Apply Password Modification
                    </button>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 7: FORCED CHANGE */}
              {currentScreen === "forced-change" && (
                <CeremonyShell
                  title="Forced Password Rotation Required"
                  subtitle="Your password has expired or was administratively reset. Update is mandatory before app entry."
                  statusText="Enforcing change"
                >
                  <form onSubmit={handleForcedChangeSubmit} className="space-y-4" id="form-forced-change">
                    <div className="p-4 bg-amber-50 border border-amber-200 text-amber-900 rounded-xl flex gap-3 text-xs leading-relaxed font-sans">
                      <AlertOctagon className="w-5 h-5 text-amber-500 shrink-0" />
                      <div>
                        <strong>Action Mandatory:</strong> Your access token is restricted. Navigation into the service console is locked until this credential renewal is verified.
                      </div>
                    </div>

                    <PasswordFieldComponent
                      label="Configure New Password"
                      id="forced-password-new"
                      value={newPassword}
                      onChange={setNewPassword}
                      autoComplete="new-password"
                    />

                    <PasswordFieldComponent
                      label="Confirm Password Configuration"
                      id="forced-password-confirm"
                      value={confirmPassword}
                      onChange={setConfirmPassword}
                      autoComplete="new-password"
                    />

                    <PasswordRequirementsComponent />

                    <button
                      type="submit"
                      disabled={isSubmitting || !reqFeedback.passed}
                      className={`w-full py-2.5 text-xs font-bold uppercase tracking-wider rounded-lg shadow-md transition-all flex items-center justify-center cursor-pointer font-sans ${
                        reqFeedback.passed
                          ? "bg-amber-600 text-white hover:bg-amber-700"
                          : "bg-slate-200 text-slate-400 cursor-not-allowed"
                      }`}
                    >
                      Update Credential & Sign In
                    </button>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 8: FORGOT-PASSWORD REQUEST */}
              {currentScreen === "forgot-password" && (
                <CeremonyShell
                  title="Initiate Account Recovery"
                  subtitle="Start recovery request without leaking credential existences"
                >
                  <form onSubmit={handleForgotPasswordRequest} className="space-y-5" id="form-forgot-password-request">
                    <div className="space-y-1.5">
                      <label className="text-xs font-semibold text-slate-700" htmlFor="forgot-email">
                        Enter Registered Account Email
                      </label>
                      <input
                        id="forgot-email"
                        type="email"
                        value={identifier}
                        onChange={(e) => setIdentifier(e.target.value)}
                        className="w-full px-3 py-2 bg-slate-50 border border-slate-200 rounded-lg text-slate-800 placeholder-slate-400 text-sm focus:ring-2 focus:ring-indigo-500/20 focus:border-indigo-500 outline-none transition-all"
                        placeholder="e.g. user@enterprise.com"
                        required
                      />
                    </div>

                    <div className="p-3.5 bg-slate-50 border border-slate-200 rounded-xl space-y-2 text-xs">
                      <div className="flex gap-2 font-bold text-slate-700 uppercase tracking-widest text-[9px] font-mono">
                        <Clock className="w-4.5 h-4.5 text-indigo-600 shrink-0" /> Policy Recovery Constraints
                      </div>
                      <p className="text-[11px] text-slate-500 leading-relaxed font-sans">
                        Recovery links are valid for exactly <strong>15 minutes</strong>. Dispatched transactions invalidate any previously issued active tokens.
                      </p>
                    </div>

                    <div className="flex gap-2 font-sans">
                      <button
                        type="button"
                        onClick={() => setCurrentScreen("password-entry")}
                        className="flex-1 py-2 border border-slate-200 rounded text-xs text-slate-600 font-semibold hover:bg-slate-50 transition-colors"
                      >
                        Cancel
                      </button>
                      <button
                        type="submit"
                        disabled={isSubmitting}
                        className="flex-1 py-2 bg-indigo-600 text-white text-xs font-bold uppercase tracking-wider rounded shadow hover:bg-indigo-700 transition-all"
                      >
                        Dispatched Reset Code
                      </button>
                    </div>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 9: RESET LINK RECEIVED */}
              {currentScreen === "reset-link-received" && (
                <CeremonyShell
                  title="Verify Secure Reset Link"
                  subtitle="Verify outbound artifact metadata and signatures"
                >
                  <div className="space-y-5" id="view-reset-received">
                    <div className="p-4 bg-green-50 border border-green-200 text-green-950 rounded-xl space-y-3 font-sans">
                      <div className="flex items-center gap-2 font-bold text-xs uppercase tracking-wide">
                        <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" /> Artifact Validated
                      </div>
                      <p className="text-xs leading-relaxed">
                        A bound recovery code has been verified. The transaction is ready to commit.
                      </p>
                      
                      <div className="bg-white/80 p-3 rounded-lg space-y-1.5 text-[10px] font-mono text-slate-700 border border-green-100">
                        <div className="flex justify-between">
                          <span>Bound Token ID:</span>
                          <span className="font-bold text-slate-800">{resetToken || "rst_3f3a2b"}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Token Freshness:</span>
                          <span className="text-slate-800">Fresh (0m 12s ago)</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Source Fingerprint:</span>
                          <span className="text-slate-800">192.168.1.45 (matches requester)</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Token Expire Time:</span>
                          <span className="text-red-600 font-bold">In 14 minutes</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex gap-2 font-sans">
                      <button
                        onClick={() => {
                          setResetTokenStatus("expired");
                          setCurrentScreen("invalid-reset");
                          addAuditLog("sign_in_failure", "warning", "Artifact manually expired by simulator check", "Simulated expiration response validation");
                        }}
                        className="flex-1 py-2 border border-red-200 text-red-600 font-semibold text-xs rounded hover:bg-red-50"
                      >
                        Simulate Expiration
                      </button>

                      <button
                        onClick={() => {
                          setCurrentScreen("reset-completion");
                        }}
                        className="flex-1 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold text-xs rounded uppercase tracking-wider"
                      >
                        Proceed to Reset
                      </button>
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 10: RESET COMPLETION */}
              {currentScreen === "reset-completion" && (
                <CeremonyShell
                  title="Configure New Credentials"
                  subtitle="Provide a brand new compliant password to secure your portal account"
                >
                  <form onSubmit={handleResetCompletion} className="space-y-4" id="form-reset-completion">
                    <div className="bg-slate-50 border border-slate-200 p-3 rounded-xl flex gap-2 items-center text-xs text-slate-700 font-semibold font-sans">
                      <Lock className="w-4 h-4 text-indigo-600" /> Token consumption active: {resetToken || "rst_3f3a2b"}
                    </div>

                    <PasswordFieldComponent
                      label="Assign New Password"
                      id="reset-password-new"
                      value={newPassword}
                      onChange={setNewPassword}
                      autoComplete="new-password"
                    />

                    <PasswordFieldComponent
                      label="Verify New Password"
                      id="reset-password-confirm"
                      value={confirmPassword}
                      onChange={setConfirmPassword}
                      autoComplete="new-password"
                    />

                    <PasswordRequirementsComponent />

                    <button
                      type="submit"
                      disabled={isSubmitting || !reqFeedback.passed}
                      className={`w-full py-2.5 text-xs font-bold uppercase tracking-wider rounded-lg shadow-md transition-all flex items-center justify-center cursor-pointer font-sans ${
                        reqFeedback.passed
                          ? "bg-indigo-600 text-white hover:bg-indigo-700"
                          : "bg-slate-200 text-slate-400 cursor-not-allowed"
                      }`}
                    >
                      Commit Password & Access
                    </button>
                  </form>
                </CeremonyShell>
              )}

              {/* SCREEN 11: INVALID/EXPIRED/USED RESET */}
              {currentScreen === "invalid-reset" && (
                <CeremonyShell
                  title="Recovery Token Failure"
                  subtitle="The system failed to consume this authentication recovery link"
                  statusText="Token Rejected"
                >
                  <div className="space-y-4 text-center py-6 font-sans" id="view-invalid-reset">
                    <div className="w-12 h-12 bg-red-100 rounded-full flex items-center justify-center mx-auto text-red-600 mb-2">
                      <AlertTriangle className="w-6 h-6" />
                    </div>
                    <h4 className="text-sm font-bold text-slate-800">Invalid Recovery Token</h4>
                    <p className="text-xs text-slate-500 leading-relaxed max-w-sm mx-auto">
                      This reset artifact has either expired, was already consumed, or was administratively revoked due to a security update or concurrency limit.
                    </p>

                    <div className="p-3 bg-slate-50 rounded-xl border border-slate-100 text-[11px] text-slate-600 flex gap-2 text-left">
                      <Shield className="w-4 h-4 text-indigo-600 shrink-0 mt-0.5" />
                      <div>
                        <strong>Pro-tip:</strong> Requesting another recovery link invalidates any outstanding links. Only the latest link in your mailbox remains active.
                      </div>
                    </div>

                    <div className="flex gap-2 pt-2 max-w-sm mx-auto">
                      <button
                        onClick={() => setCurrentScreen("forgot-password")}
                        className="flex-1 py-2 bg-slate-900 text-white text-xs font-bold uppercase tracking-wider rounded hover:bg-slate-800 transition-colors"
                      >
                        Request New Link
                      </button>
                      <button
                        onClick={() => setCurrentScreen("identifier-first")}
                        className="flex-1 py-2 border border-slate-200 text-slate-600 text-xs font-bold uppercase tracking-wider rounded hover:bg-slate-50 transition-colors"
                      >
                        Return to login
                      </button>
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 12: COMPROMISED-PASSWORD RESPONSE */}
              {currentScreen === "compromised-response" && (
                <CeremonyShell
                  title="Breach Threat Containment"
                  subtitle="This credential was discovered in a public data leak"
                  statusText="Credential Blocked"
                >
                  <div className="space-y-4" id="view-compromised-response">
                    <div className="p-4 bg-red-50 border border-red-200 text-red-950 rounded-xl flex gap-3 text-xs leading-relaxed font-sans">
                      <AlertOctagon className="w-5 h-5 text-red-600 shrink-0 mt-0.5 animate-pulse" />
                      <div>
                        <strong>Security Protection Active:</strong> Our database telemetry verified that this password matches a known compromised hash from an external breach list. Usage of this credential has been instantly disabled.
                      </div>
                    </div>

                    <p className="text-xs text-slate-600 leading-relaxed font-sans">
                      We require you to create a completely unique password immediately to restore server access. We also highly recommend rotating this password on any third-party services where it may have been reused.
                    </p>

                    <div className="p-3.5 bg-slate-100 border border-slate-200 rounded-xl font-sans">
                      <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Global Breach Statistics</span>
                      <div className="flex justify-between text-xs mt-1 text-slate-700">
                        <span>Database matches:</span>
                        <span className="font-mono text-red-600 font-bold">Over 4,200,000 matches</span>
                      </div>
                    </div>

                    <button
                      onClick={() => {
                        setCurrentScreen("forced-change");
                      }}
                      className="w-full py-2.5 bg-red-600 text-white font-bold text-xs uppercase tracking-wider rounded-lg shadow hover:bg-red-700 transition-all flex items-center justify-center gap-1.5 cursor-pointer font-sans"
                    >
                      Resolve Breach Now <ChevronRight className="w-4.5 h-4.5" />
                    </button>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 13: PASSWORD DETAIL / STATUS */}
              {currentScreen === "password-detail" && (
                <CeremonyShell
                  title="Credential Posture Detail"
                  subtitle="Manage account credentials, dates, strength, and security protocols"
                >
                  <div className="space-y-4" id="view-password-detail">
                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-3 font-sans">
                      <div className="flex justify-between items-center pb-2 border-b border-slate-200/50">
                        <div className="flex items-center gap-1.5 font-bold text-xs uppercase tracking-wider text-slate-700">
                          <User className="w-4 h-4 text-indigo-600" /> {user.fullName}
                        </div>
                        <span className="text-[10px] bg-green-50 text-green-700 border border-green-200 rounded-full px-2 py-0.5 font-bold">
                          {user.accountStatus.toUpperCase()}
                        </span>
                      </div>

                      <div className="grid grid-cols-2 gap-3 text-xs">
                        <div className="bg-white p-2.5 rounded-lg border border-slate-100">
                          <span className="text-[9px] text-slate-400 uppercase tracking-widest block font-bold">Credential Status</span>
                          <span className="text-slate-800 font-semibold block mt-0.5">
                            {user.isPasswordRequired ? "Active Password" : "Passwordless Setup"}
                          </span>
                        </div>
                        <div className="bg-white p-2.5 rounded-lg border border-slate-100">
                          <span className="text-[9px] text-slate-400 uppercase tracking-widest block font-bold">MFA Protection</span>
                          <span className="text-green-600 font-semibold block mt-0.5">
                            {user.hasMfaEnabled ? "Enabled (TOTP)" : "Disabled"}
                          </span>
                        </div>
                        <div className="bg-white p-2.5 rounded-lg border border-slate-100">
                          <span className="text-[9px] text-slate-400 uppercase tracking-widest block font-bold">Last Changed</span>
                          <span className="text-slate-600 font-medium block mt-0.5 font-mono text-[10px]">
                            {new Date(user.passwordChangedDate).toLocaleDateString()}
                          </span>
                        </div>
                        <div className="bg-white p-2.5 rounded-lg border border-slate-100">
                          <span className="text-[9px] text-slate-400 uppercase tracking-widest block font-bold">Last Signed In</span>
                          <span className="text-slate-600 font-medium block mt-0.5 font-mono text-[10px]">
                            {new Date(user.passwordLastUsedDate).toLocaleDateString()}
                          </span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2 font-sans">
                      <button
                        onClick={() => setCurrentScreen("change-password")}
                        className="w-full py-2.5 bg-slate-900 text-white font-semibold text-xs rounded-lg hover:bg-slate-800 transition-colors flex items-center justify-center gap-2"
                      >
                        <RefreshCw className="w-4 h-4" /> Change Password Factor
                      </button>

                      <button
                        onClick={() => {
                          triggerStepUpGate("Deactivate Password Factor", "disable-remove");
                        }}
                        className="w-full py-2.5 border border-red-200 text-red-600 font-semibold text-xs rounded-lg hover:bg-red-50 transition-colors flex items-center justify-center gap-2"
                      >
                        Disable / Transition to Passwordless
                      </button>
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 14: DISABLE / REMOVE PASSWORD */}
              {currentScreen === "disable-remove" && (
                <CeremonyShell
                  title="Disable Password Credentials"
                  subtitle="Transition this account permanently to passwordless operations"
                >
                  <div className="space-y-4 font-sans" id="view-disable-remove">
                    <div className="p-4 bg-red-50 border border-red-200 rounded-xl text-red-950 space-y-2 text-xs">
                      <div className="flex gap-2 font-bold uppercase tracking-wider text-red-700 text-[10px]">
                        <AlertTriangle className="w-5 h-5 shrink-0" /> Critical Security Modification
                      </div>
                      <p className="leading-relaxed">
                        Deactivating password credentials prevents typical dictionary lookup attempts. However, you MUST ensure you have verified alternative factors like WebAuthn or FIDO hardware keys registered to avoid locked outcomes.
                      </p>
                    </div>

                    <div className="p-3 bg-slate-50 border border-slate-200 rounded-xl space-y-1.5">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block font-mono">Requirement Gate Check</span>
                      <div className="flex justify-between text-xs items-center">
                        <span className="text-slate-700">MFA Token Verification:</span>
                        <span className="text-green-600 font-bold flex items-center gap-1">
                          <CheckCircle2 className="w-3.5 h-3.5" /> ESCALATED (AAL2)
                        </span>
                      </div>
                      <div className="flex justify-between text-xs items-center">
                        <span className="text-slate-700">Alternative WebAuthn Config:</span>
                        {user.hasWebAuthnEnabled ? (
                          <span className="text-green-600 font-bold flex items-center gap-1">
                            <CheckCircle2 className="w-3.5 h-3.5" /> Registered
                          </span>
                        ) : (
                          <button
                            type="button"
                            onClick={() => {
                              setUser((prev) => ({ ...prev, hasWebAuthnEnabled: true }));
                              addAuditLog("admin_action", "info", "WebAuthn alternative enrolled", "Client FIDO credentials registered.");
                            }}
                            className="text-[10px] text-indigo-600 font-semibold hover:underline"
                          >
                            + Register Passkey
                          </button>
                        )}
                      </div>
                    </div>

                    <div className="flex gap-2">
                      <button
                        onClick={() => setCurrentScreen("password-detail")}
                        className="flex-1 py-2 border border-slate-200 rounded text-xs font-semibold text-slate-600 hover:bg-slate-50"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={handleDisablePassword}
                        disabled={!user.hasWebAuthnEnabled && !user.hasMfaEnabled}
                        className={`flex-1 py-2 text-xs font-bold uppercase tracking-wider rounded shadow transition-all ${
                          user.hasWebAuthnEnabled || user.hasMfaEnabled
                            ? "bg-red-600 hover:bg-red-700 text-white"
                            : "bg-slate-200 text-slate-400 cursor-not-allowed"
                        }`}
                      >
                        Confirm Disable
                      </button>
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 15: EVIDENCE / SESSION DETAIL */}
              {currentScreen === "evidence-detail" && (
                <CeremonyShell
                  title="Cryptographic Session Evidence"
                  subtitle="Live AMR metrics generated on verified authentication gates"
                >
                  <div className="space-y-4 text-xs font-sans" id="view-evidence-detail">
                    {evidence ? (
                      <div className="space-y-3">
                        <div className="p-3.5 bg-green-50 border border-green-200 text-green-950 rounded-xl flex gap-3 leading-relaxed">
                          <CheckCircle2 className="w-5 h-5 text-green-500 shrink-0" />
                          <div>
                            <strong>Session Authenticated:</strong> Valid AMR metadata generated. You are fully authorized to access enterprise resources.
                          </div>
                        </div>

                        <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2.5 font-mono">
                          <div className="flex justify-between border-b border-slate-200/50 pb-1.5">
                            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold">Assurance Rating</span>
                            <span className="text-green-700 font-bold">{evidence.assuranceLevel}</span>
                          </div>
                          <div className="flex justify-between border-b border-slate-200/50 pb-1.5">
                            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold">Authentication Factors (AMR)</span>
                            <span className="text-slate-800 font-bold">{JSON.stringify(evidence.amr)}</span>
                          </div>
                          <div className="flex justify-between border-b border-slate-200/50 pb-1.5">
                            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold">Subject identifier</span>
                            <span className="text-slate-800 truncate max-w-[180px]">{evidence.subject}</span>
                          </div>
                          <div className="flex justify-between border-b border-slate-200/50 pb-1.5">
                            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold">Timestamp</span>
                            <span className="text-slate-600">{new Date(evidence.authenticatedAt).toLocaleTimeString()}</span>
                          </div>
                          <div className="flex justify-between">
                            <span className="text-[10px] text-slate-400 uppercase tracking-widest font-sans font-bold">Token Freshness</span>
                            <span className="text-slate-800 font-semibold">Fresh (Under 10s)</span>
                          </div>
                        </div>

                        <div className="bg-slate-900 text-slate-300 p-3 rounded-lg text-[9px] leading-relaxed break-all font-mono">
                          <span className="text-indigo-400 font-bold block mb-1">Signed JWT Header Payload:</span>
                          {evidence.token}
                        </div>

                        <button
                          onClick={() => {
                            setEvidence(null);
                            setCurrentScreen("identifier-first");
                            addAuditLog("admin_action", "info", "User manually logged out", "Active session evidence invalidated on client request.");
                          }}
                          className="w-full py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold text-xs uppercase tracking-wider rounded-lg shadow"
                        >
                          Revoke Active Session (Sign out)
                        </button>
                      </div>
                    ) : (
                      <div className="text-center py-8">
                        <Lock className="w-10 h-10 text-slate-300 mx-auto mb-2" />
                        <h4 className="font-bold text-slate-700">No active session evidence</h4>
                        <p className="text-slate-400 text-[11px] mt-1 max-w-xs mx-auto">
                          Perform a successful authentication flow to generate active secure AMR credentials.
                        </p>
                        <button
                          onClick={() => setCurrentScreen("identifier-first")}
                          className="mt-4 px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-bold rounded text-xs uppercase tracking-wider"
                        >
                          Initiate flow
                        </button>
                      </div>
                    )}
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 16: PASSWORD POLICY EDITOR */}
              {currentScreen === "policy-editor" && (
                <CeremonyShell
                  title="Configure Password Policy"
                  subtitle="Enterprise security constraints editor"
                >
                  <div className="space-y-4" id="view-policy-editor">
                    <div className="space-y-3 bg-slate-50 border border-slate-200 p-4 rounded-xl text-xs font-sans">
                      <div>
                        <label className="block text-slate-700 font-semibold mb-1">Minimum Character Length ({policy.minLength} chars)</label>
                        <input
                          type="range"
                          min={8}
                          max={20}
                          value={policy.minLength}
                          onChange={(e) => updatePolicy({ minLength: Number(e.target.value) })}
                          className="w-full accent-indigo-600"
                        />
                      </div>

                      <div className="space-y-2 pt-1 border-t border-slate-200/50">
                        <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                          <input
                            type="checkbox"
                            checked={policy.requireUppercase}
                            onChange={(e) => updatePolicy({ requireUppercase: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500"
                          />
                          <span>Require Uppercase letter (A-Z)</span>
                        </label>

                        <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                          <input
                            type="checkbox"
                            checked={policy.requireLowercase}
                            onChange={(e) => updatePolicy({ requireLowercase: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500"
                          />
                          <span>Require Lowercase letter (a-z)</span>
                        </label>

                        <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                          <input
                            type="checkbox"
                            checked={policy.requireSpecial}
                            onChange={(e) => updatePolicy({ requireSpecial: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500"
                          />
                          <span>Require Special symbols</span>
                        </label>

                        <label className="flex items-center gap-2 cursor-pointer text-slate-700">
                          <input
                            type="checkbox"
                            checked={policy.blockBreachedSecrets}
                            onChange={(e) => updatePolicy({ blockBreachedSecrets: e.target.checked })}
                            className="rounded text-indigo-600 focus:ring-indigo-500"
                          />
                          <span className="font-semibold text-red-600">Enforce global compromised secret checks</span>
                        </label>
                      </div>

                      <div className="pt-2 border-t border-slate-200/50 font-sans">
                        <label className="block text-slate-700 font-semibold mb-1">Maximum Failure Lockout Attempts</label>
                        <select
                          value={policy.maxAttempts}
                          onChange={(e) => updatePolicy({ maxAttempts: Number(e.target.value) })}
                          className="w-full bg-white border border-slate-200 rounded px-2 py-1 text-xs outline-none focus:ring-2 focus:ring-indigo-550/20"
                        >
                          <option value={3}>3 Attempts</option>
                          <option value={5}>5 Attempts</option>
                          <option value={10}>10 Attempts</option>
                        </select>
                      </div>
                    </div>

                    <div className="p-3 bg-indigo-50 text-indigo-950 border border-indigo-100 rounded-xl text-[11px] leading-relaxed font-sans">
                      <strong>Policy impact:</strong> Saving these options triggers dynamic client updates on all future password setup, forced changes, or password resets.
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 17: USER POSTURE / ADMIN RESET */}
              {currentScreen === "user-posture" && (
                <CeremonyShell
                  title="User Security Posture & Operations"
                  subtitle="Govern credentials, support recovery operations, and active lockdowns"
                >
                  <div className="space-y-4 font-sans" id="view-user-posture">
                    <div className="p-4 bg-slate-50 border border-slate-200 rounded-xl space-y-3 text-xs text-slate-700">
                      <div className="flex justify-between border-b border-slate-200/50 pb-2 items-center">
                        <div>
                          <span className="font-bold text-slate-800 text-sm block">{user.fullName}</span>
                          <span className="text-slate-500 block">{user.email}</span>
                        </div>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          user.isLocked ? "bg-red-50 text-red-700 border border-red-200" : "bg-green-50 text-green-700 border border-green-200"
                        }`}>
                          {user.isLocked ? "LOCKED" : "ACTIVE"}
                        </span>
                      </div>

                      <div className="space-y-1.5 text-xs text-slate-600 font-sans">
                        <div className="flex justify-between">
                          <span>Active Fail Attempts:</span>
                          <span className="font-mono text-slate-800 font-bold">{user.failedAttempts} / {policy.maxAttempts}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Forced Rotation:</span>
                          <span className="text-slate-800 font-semibold">{user.needsForcedChange ? "Triggered" : "Active / Standard"}</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Alternative Factors:</span>
                          <span className="text-slate-800 font-semibold">{user.hasWebAuthnEnabled ? "WebAuthn / Passkeys active" : "None"}</span>
                        </div>
                      </div>
                    </div>

                    <div className="space-y-2">
                      <p className="text-[10px] font-bold text-slate-400 uppercase tracking-widest font-mono">Support Diagnostics Actions</p>
                      
                      <div className="grid grid-cols-2 gap-2">
                        <button
                          onClick={triggerAdminUnlock}
                          disabled={!user.isLocked && user.failedAttempts === 0}
                          className="py-2 bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <Unlock className="w-4 h-4" /> Reset lockout
                        </button>

                        <button
                          onClick={triggerAdminForcedReset}
                          disabled={user.needsForcedChange}
                          className="py-2 bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs rounded-lg transition-colors flex items-center justify-center gap-1 cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
                        >
                          <RefreshCw className="w-4 h-4" /> Force password update
                        </button>
                      </div>

                      <button
                        onClick={() => {
                          const tokenString = "rst_" + Math.random().toString(36).substring(2, 10);
                          setResetToken(tokenString);
                          setResetTokenStatus("valid");
                          setSystemMessage({ type: "success", text: `A secure reset link was generated: ${tokenString}` });
                          addAuditLog("admin_action", "info", "Manual recovery token issued by admin", "Link valid for 15 minutes");
                        }}
                        className="w-full py-2 border border-slate-200 text-slate-700 font-semibold text-xs rounded-lg hover:bg-slate-50 transition-colors flex items-center justify-center gap-2 cursor-pointer"
                      >
                        <Shield className="w-4 h-4" /> Out-of-band Recovery link
                      </button>
                    </div>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 18: LOCKOUT / SECURITY EVENT DETAIL */}
              {currentScreen === "security-events" && (
                <CeremonyShell
                  title="Diagnostics & Lockouts timeline"
                  subtitle="Investigate redacted authentication failures and security events"
                >
                  <div className="space-y-4" id="view-security-events">
                    <div className="p-3 bg-red-50 border border-red-200 text-red-950 rounded-xl space-y-2 text-xs font-sans">
                      <div className="flex gap-2 font-bold uppercase tracking-wider text-[10px] text-red-700">
                        <AlertTriangle className="w-4.5 h-4.5 shrink-0" /> Security Lockout Detected
                      </div>
                      <p className="leading-relaxed">
                        User Alex Rivera reached the maximum lockout rate limit of 5 failed attempts at {new Date().toLocaleTimeString()}. Outbound alert notifications have been dispatched.
                      </p>
                    </div>

                    <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 space-y-2 font-sans">
                      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block font-mono">Diagnostics Event Parameters</span>
                      <div className="space-y-2 text-xs text-slate-600 font-mono">
                        <div className="flex justify-between border-b border-slate-100 pb-1">
                          <span>Enforcer:</span>
                          <span className="text-slate-800">pwd-auth-gateway</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1">
                          <span>Target ID:</span>
                          <span className="text-slate-800">alex.rivera@enterprise.com</span>
                        </div>
                        <div className="flex justify-between border-b border-slate-100 pb-1">
                          <span>IP Origin:</span>
                          <span className="text-slate-800">192.168.1.45</span>
                        </div>
                        <div className="flex justify-between">
                          <span>Payload Hashing:</span>
                          <span className="text-slate-800">Argon2id (Salted/Redacted)</span>
                        </div>
                      </div>
                    </div>

                    <button
                      onClick={triggerAdminUnlock}
                      className="w-full py-2.5 bg-green-600 hover:bg-green-700 text-white font-bold text-xs uppercase tracking-wider rounded-lg shadow-md transition-colors font-sans"
                    >
                      Clear lockout & Restore Account
                    </button>
                  </div>
                </CeremonyShell>
              )}

              {/* SCREEN 19: NATIVE PASSWORD SCREEN */}
              {currentScreen === "native-password" && (
                <CeremonyShell
                  title="iOS / Android Secure Entry Layout"
                  subtitle="Secure native rendering compatibility and Password manager overlay checks"
                >
                  <div className="space-y-4" id="view-native-password">
                    <div className="bg-slate-900 border-4 border-slate-800 rounded-3xl p-5 text-white space-y-4 shadow-xl max-w-sm mx-auto font-sans">
                      <div className="flex justify-between items-center text-slate-400 text-[10px] pb-2 border-b border-slate-800 font-mono">
                        <span>Carrier LTE</span>
                        <span>10:33 AM</span>
                        <span>100%</span>
                      </div>

                      <div className="space-y-2">
                        <h4 className="text-sm font-bold tracking-tight text-white flex items-center gap-1.5 font-display">
                          <Smartphone className="w-4 h-4 text-indigo-400" /> Enterprise Sign-In
                        </h4>
                        <p className="text-[11px] text-slate-400">Secure entry view utilizing native autofill hints</p>
                      </div>

                      <div className="space-y-3 pt-2 text-xs">
                        <div className="space-y-1">
                          <label className="text-[10px] text-slate-400 font-semibold block">Password</label>
                          <input
                            type="password"
                            value="superpassword123"
                            disabled
                            className="w-full px-3 py-2 bg-slate-800 border border-slate-700 text-white rounded-lg text-xs font-mono"
                          />
                        </div>

                        <div className="p-2.5 bg-slate-800 border border-indigo-500 rounded-xl flex items-center gap-2 animate-bounce cursor-pointer">
                          <KeyRound className="w-5 h-5 text-indigo-400 shrink-0" />
                          <div className="text-left text-[11px]">
                            <p className="font-bold text-indigo-300">Use Saved Password</p>
                            <p className="text-slate-400 text-[9px] font-mono">alex.rivera@enterprise.com</p>
                          </div>
                          <Sparkles className="w-3.5 h-3.5 text-yellow-400 ml-auto" />
                        </div>
                      </div>

                      <div className="flex gap-2 pt-2">
                        <button className="flex-1 py-1.5 bg-indigo-600 text-white font-bold text-[11px] rounded-lg">
                          Login
                        </button>
                        <button className="px-2 bg-slate-800 border border-slate-700 rounded-lg flex items-center justify-center">
                          <Smartphone className="w-4 h-4 text-indigo-400" />
                        </button>
                      </div>
                    </div>

                    <div className="p-3 bg-indigo-50 text-indigo-950 border border-indigo-100 rounded-xl text-[11px] leading-relaxed font-sans">
                      <strong>Native compliance:</strong> Uses <code>autocomplete=&quot;current-password&quot;</code> and <code>textContentType=&quot;password&quot;</code> parameters to prompt standard password manager autofills without blockages.
                    </div>
                  </div>
                </CeremonyShell>
              )}
            </motion.div>
          </AnimatePresence>
        </section>

        {/* RIGHT SIDEBAR: POLICY CONFIGURATION & AUDIT TIMELINE (col-span-4) */}
        <aside className="col-span-4 bg-white border-l border-slate-200 flex flex-col p-5 overflow-y-auto" id="policy-audit-sidebar">
          
          <div className="space-y-4 mb-6">
            <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5 font-mono">
              <Settings className="w-3.5 h-3.5 text-indigo-600" /> Active Policy Configuration
            </h3>

            <div className="bg-slate-50 border border-slate-200 rounded-xl p-3.5 space-y-3 text-xs">
              <div className="flex justify-between items-center font-sans">
                <span className="text-slate-600 font-sans">Min Length:</span>
                <span className="px-1.5 py-0.5 bg-slate-200 rounded text-[11px] font-mono font-bold text-slate-800">
                  {policy.minLength} characters
                </span>
              </div>
              
              <div className="flex justify-between items-center font-sans">
                <span className="text-slate-600 font-sans">Lockout threshold:</span>
                <span className="px-1.5 py-0.5 bg-red-50 text-red-700 border border-red-200 rounded text-[11px] font-mono font-bold">
                  {policy.maxAttempts} attempts
                </span>
              </div>

              <div className="flex justify-between items-center font-sans">
                <span className="text-slate-600">Breach-Watch check:</span>
                <span className={`text-[11px] font-bold ${policy.blockBreachedSecrets ? "text-green-600" : "text-slate-500"}`}>
                  {policy.blockBreachedSecrets ? "ENABLED" : "DISABLED"}
                </span>
              </div>

              <div className="flex justify-between items-center font-sans">
                <span className="text-slate-600">Forced reset days:</span>
                <span className="text-slate-800 font-semibold">{policy.forceResetIntervalDays} days</span>
              </div>

              <button
                onClick={() => setCurrentScreen("policy-editor")}
                className="w-full text-center py-1.5 border border-indigo-100 hover:bg-indigo-50 text-indigo-600 hover:text-indigo-700 text-[10px] font-bold tracking-wide rounded uppercase transition-colors font-mono"
              >
                Modify Rules
              </button>
            </div>
          </div>

          <div className="flex-1 flex flex-col overflow-hidden">
            <h3 className="text-[10px] font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5 mb-3 font-mono">
              <History className="w-3.5 h-3.5 text-indigo-600" /> Audit Ceremony Timeline
            </h3>

            <div className="flex-1 overflow-y-auto pr-1 space-y-3.5" id="audit-timeline-items">
              {events.map((evt, idx) => {
                let badgeColor = "bg-green-500";
                if (evt.severity === "warning") badgeColor = "bg-amber-500";
                if (evt.severity === "critical") badgeColor = "bg-red-500";

                return (
                  <div key={evt.id || idx} className="flex gap-3 text-xs">
                    <div className="w-px bg-slate-200 relative shrink-0">
                      <div className={`absolute -left-[4.5px] top-1 w-2.5 h-2.5 rounded-full border-2 border-white ${badgeColor}`}></div>
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-bold text-slate-800 truncate uppercase text-[11px] tracking-wide flex items-center gap-1 font-mono">
                        {evt.eventType}
                      </p>
                      <p className="text-slate-500 text-[10px] mt-0.5 leading-relaxed font-sans">{evt.description}</p>
                      {evt.redactedDetails && (
                        <span className="block text-[9px] text-slate-400 font-mono italic mt-0.5">{evt.redactedDetails}</span>
                      )}
                      <p className="text-[9px] text-slate-400 font-mono mt-0.5">
                        {new Date(evt.timestamp).toLocaleTimeString()} · {evt.ipAddress}
                      </p>
                    </div>
                  </div>
                );
              })}
            </div>

            <button
              onClick={() => setCurrentScreen("security-events")}
              className="mt-4 text-xs font-semibold text-indigo-600 text-center py-2 border border-indigo-100 rounded-lg hover:bg-indigo-50 transition-colors font-sans"
            >
              View Detailed Diagnostics
            </button>
          </div>
        </aside>
      </main>

      {/* FOOTER SECTION */}
      <footer className="h-10 bg-slate-900 flex items-center justify-between px-6 text-[10px] text-slate-400 shrink-0 border-t border-slate-800 font-mono" id="main-footer">
        <div className="flex gap-4">
          <span className="flex items-center gap-1"><Server className="w-3 h-3 text-green-500" /> System Status: Healthy</span>
          <span>AMR Protocol Version: pwd_v2_fido_hybrid</span>
          <span>Security Level: AAL2 (Enforced)</span>
        </div>
        <div>&copy; {new Date().getFullYear()} SECURE_PWD_IDENTITY_GATEWAY • All Ceremonies Logged</div>
      </footer>
    </div>
  );
}
