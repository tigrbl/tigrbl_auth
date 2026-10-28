/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from "react";
import { motion, AnimatePresence } from "motion/react";
import {
  ShieldAlert,
  Key,
  RefreshCw,
  Trash2,
  Settings,
  Activity,
  CheckCircle2,
  Lock,
  Unlock,
  HelpCircle,
  XCircle,
  ArrowRight,
  Eye,
  EyeOff,
  UserCheck,
  Server,
  UserX,
  ChevronRight,
  Fingerprint,
  AlertTriangle,
  FileText,
  Terminal,
  Clock,
  Info,
  Smartphone,
  Check,
  RotateCcw
} from "lucide-react";
import {
  AuthenticatorStatus,
  CeremonyType,
  CeremonyStatus,
  AssuranceLevel,
  KbaQuestion,
  KbaAnswerEnrollment,
  KbaUserCredential,
  TenantPolicy,
  ProviderConfig,
  AuditEvent
} from "../types";

// ==========================================
// 1. KbaRiskNotice Component
// ==========================================
interface KbaRiskNoticeProps {
  id?: string;
  onDismiss?: () => void;
}

export const KbaRiskNotice: React.FC<KbaRiskNoticeProps> = ({ id, onDismiss }) => {
  return (
    <div
      id={id || "kba-risk-notice"}
      className="bg-amber-50 border border-amber-200 rounded-xl p-5 text-amber-900 shadow-sm"
    >
      <div className="flex gap-3">
        <ShieldAlert className="h-6 w-6 text-amber-600 shrink-0 mt-0.5" id="risk-icon" />
        <div>
          <h4 className="font-display font-semibold text-amber-950 text-sm md:text-base mb-1">
            Security Warning: Lower-Assurance Knowledge Factor
          </h4>
          <p className="text-xs md:text-sm text-amber-800 leading-relaxed mb-3">
            Knowledge-Based Authentication (KBA) relies on static information that can often be found in public records, social media, or compromised data breaches.
          </p>
          <ul className="text-xs text-amber-700 list-disc pl-5 space-y-1 mb-4">
            <li>Highly susceptible to targeted social engineering and identity theft.</li>
            <li>Does not satisfy phishing-resistant authentication standards.</li>
            <li>Recommended only as a highly constrained recovery fallback, not a primary authenticator.</li>
          </ul>
          <div className="flex flex-wrap gap-3 items-center">
            <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-amber-100 text-amber-800 border border-amber-200">
              Assurance Level: LOW
            </span>
            {onDismiss && (
              <button
                id="dismiss-risk-btn"
                onClick={onDismiss}
                className="text-xs font-semibold text-amber-900 hover:text-amber-950 underline transition-colors"
              >
                Acknowledge and Continue
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 2. KbaQuestionPicker Component
// ==========================================
interface KbaQuestionPickerProps {
  id?: string;
  questions: KbaQuestion[];
  selectedQuestionId: string;
  onChange: (questionId: string) => void;
  disabled?: boolean;
  excludeQuestionIds?: string[];
  placeholder?: string;
}

export const KbaQuestionPicker: React.FC<KbaQuestionPickerProps> = ({
  id,
  questions,
  selectedQuestionId,
  onChange,
  disabled = false,
  excludeQuestionIds = [],
  placeholder = "Select an approved security question..."
}) => {
  const filteredQuestions = questions.filter(
    (q) => !excludeQuestionIds.includes(q.id) || q.id === selectedQuestionId
  );

  return (
    <div id={id || "kba-question-picker-container"} className="space-y-1">
      <label
        htmlFor={id ? `${id}-select` : "kba-question-select"}
        className="block text-xs font-medium text-slate-700"
      >
        Approved Security Question
      </label>
      <div className="relative">
        <select
          id={id ? `${id}-select` : "kba-question-select"}
          value={selectedQuestionId}
          onChange={(e) => onChange(e.target.value)}
          disabled={disabled}
          className="w-full pl-3 pr-10 py-2 text-sm bg-white border border-slate-300 rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-500 focus:border-slate-500 disabled:bg-slate-50 disabled:text-slate-400 font-sans transition-all"
        >
          <option value="" disabled>
            {placeholder}
          </option>
          {filteredQuestions.map((q) => (
            <option key={q.id} value={q.id}>
              [{q.category}] {q.text}
            </option>
          ))}
        </select>
        <div className="absolute inset-y-0 right-0 flex items-center pr-3 pointer-events-none text-slate-500">
          <HelpCircle className="h-4 w-4" />
        </div>
      </div>
      <p className="text-[11px] text-slate-400">
        Questions are server-vetted to resist standard public search exposure.
      </p>
    </div>
  );
};

// ==========================================
// 3. KbaAnswerField Component
// ==========================================
interface KbaAnswerFieldProps {
  id: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  disabled?: boolean;
  label?: string;
  error?: string;
  onKeyDown?: (e: React.KeyboardEvent<HTMLInputElement>) => void;
}

export const KbaAnswerField: React.FC<KbaAnswerFieldProps> = ({
  id,
  value,
  onChange,
  placeholder = "Type your answer...",
  disabled = false,
  label = "Security Answer",
  error,
  onKeyDown
}) => {
  const [showAnswer, setShowAnswer] = useState(false);

  return (
    <div id={`${id}-container`} className="space-y-1.5">
      <div className="flex justify-between items-center">
        <label htmlFor={id} className="block text-xs font-semibold text-slate-700">
          {label}
        </label>
        <span className="text-[10px] text-slate-400">Case/spacing normalized on server</span>
      </div>
      <div className="relative rounded-lg shadow-sm">
        <input
          id={id}
          type={showAnswer ? "text" : "password"}
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder={placeholder}
          disabled={disabled}
          onKeyDown={onKeyDown}
          autoComplete="off"
          data-lpignore="true" // Ignore LastPass
          className={`w-full pl-3 pr-10 py-2 text-sm bg-white border rounded-lg shadow-sm focus:outline-none focus:ring-2 focus:ring-slate-500 focus:border-slate-500 font-mono disabled:bg-slate-50 disabled:text-slate-400 ${
            error ? "border-red-300 focus:ring-red-500 focus:border-red-500" : "border-slate-300"
          }`}
        />
        <button
          id={`${id}-toggle-visibility`}
          type="button"
          onClick={() => setShowAnswer(!showAnswer)}
          disabled={disabled}
          tabIndex={-1}
          className="absolute inset-y-0 right-0 flex items-center pr-3 text-slate-400 hover:text-slate-600 focus:outline-none"
        >
          {showAnswer ? <EyeOff className="h-4 w-4" id="eye-off" /> : <Eye className="h-4 w-4" id="eye" />}
        </button>
      </div>
      {error && (
        <p id={`${id}-error`} className="text-xs text-red-600 font-medium flex items-center gap-1">
          <AlertTriangle className="h-3.5 w-3.5 shrink-0" />
          {error}
        </p>
      )}
    </div>
  );
};

// ==========================================
// 4. AnswerSecretClearBoundary Component
// ==========================================
interface AnswerSecretClearBoundaryProps {
  id?: string;
  onClear: () => void;
  children: React.ReactNode;
}

export const AnswerSecretClearBoundary: React.FC<AnswerSecretClearBoundaryProps> = ({
  id,
  onClear,
  children
}) => {
  // Clear secrets on unmount, page hide, or user visibility change
  useEffect(() => {
    const handleVisibilityChange = () => {
      if (document.hidden) {
        onClear();
      }
    };

    window.addEventListener("pagehide", onClear);
    window.addEventListener("beforeunload", onClear);
    document.addEventListener("visibilitychange", handleVisibilityChange);

    return () => {
      onClear();
      window.removeEventListener("pagehide", onClear);
      window.removeEventListener("beforeunload", onClear);
      document.removeEventListener("visibilitychange", handleVisibilityChange);
    };
  }, [onClear]);

  return (
    <div id={id || "answer-secret-clear-boundary"} className="relative">
      {children}
    </div>
  );
};

// ==========================================
// 5. KbaChallengeStep Component
// ==========================================
interface KbaChallengeStepProps {
  id?: string;
  currentStep: number;
  totalSteps: number;
  questionText: string;
  answerValue: string;
  onAnswerChange: (val: string) => void;
  onSubmit: () => void;
  onCancel: () => void;
  error?: string;
  isSubmitting: boolean;
  expirySeconds: number;
  onExpired: () => void;
  remainingAttempts: number;
}

export const KbaChallengeStep: React.FC<KbaChallengeStepProps> = ({
  id,
  currentStep,
  totalSteps,
  questionText,
  answerValue,
  onAnswerChange,
  onSubmit,
  onCancel,
  error,
  isSubmitting,
  expirySeconds,
  onExpired,
  remainingAttempts
}) => {
  const [timeLeft, setTimeLeft] = useState(expirySeconds);

  useEffect(() => {
    setTimeLeft(expirySeconds);
  }, [currentStep, expirySeconds]);

  useEffect(() => {
    if (timeLeft <= 0) {
      onExpired();
      return;
    }
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft, onExpired]);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && answerValue.trim()) {
      onSubmit();
    }
  };

  return (
    <div id={id || "kba-challenge-step"} className="space-y-4">
      <div className="flex justify-between items-center bg-slate-50 border border-slate-100 p-3 rounded-lg">
        <div className="flex items-center gap-2">
          <span className="inline-flex items-center justify-center h-6 w-6 rounded-full bg-slate-900 text-white text-xs font-semibold">
            {currentStep}
          </span>
          <span className="text-xs text-slate-500">
            of {totalSteps} required verification questions
          </span>
        </div>
        <div className="flex items-center gap-1.5 text-xs font-semibold text-slate-700">
          <Clock className={`h-4 w-4 ${timeLeft < 30 ? "text-red-500 animate-pulse" : "text-slate-500"}`} />
          <span className={timeLeft < 30 ? "text-red-600" : ""}>
            {Math.floor(timeLeft / 60)}:{(timeLeft % 60).toString().padStart(2, "0")}
          </span>
        </div>
      </div>

      <div className="bg-slate-50 border border-slate-100 p-4 rounded-xl">
        <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block mb-1">
          Verification Prompt
        </span>
        <p className="font-display font-medium text-slate-900 text-sm md:text-base leading-snug">
          {questionText}
        </p>
      </div>

      <AnswerSecretClearBoundary onClear={() => onAnswerChange("")}>
        <KbaAnswerField
          id="challenge-answer-input"
          value={answerValue}
          onChange={onAnswerChange}
          placeholder="Provide the answer precisely..."
          disabled={isSubmitting}
          label="Your Answer"
          error={error}
          onKeyDown={handleKeyDown}
        />
      </AnswerSecretClearBoundary>

      <div className="bg-slate-50 rounded-lg p-3 border border-slate-100 flex items-center justify-between text-xs text-slate-500">
        <span className="flex items-center gap-1 text-slate-600">
          <Info className="h-3.5 w-3.5" /> Security note: Incorrect answers are generic.
        </span>
        <span className="font-semibold text-slate-700">
          Attempts left: <span className={remainingAttempts === 1 ? "text-red-600 font-bold" : ""}>{remainingAttempts}</span>
        </span>
      </div>

      <div className="flex justify-end gap-3 pt-2">
        <button
          id="challenge-cancel-btn"
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="px-4 py-2 border border-slate-200 text-xs font-medium rounded-lg text-slate-600 hover:bg-slate-50 transition-colors disabled:opacity-50"
        >
          Cancel
        </button>
        <button
          id="challenge-submit-btn"
          type="button"
          onClick={onSubmit}
          disabled={isSubmitting || !answerValue.trim()}
          className="px-4 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg shadow transition-colors flex items-center gap-1.5 disabled:opacity-50"
        >
          {isSubmitting ? (
            <>
              <RefreshCw className="h-3.5 w-3.5 animate-spin" /> Verifying...
            </>
          ) : (
            <>
              Next Question <ArrowRight className="h-3.5 w-3.5" />
            </>
          )}
        </button>
      </div>
    </div>
  );
};

// ==========================================
// 6. KbaPolicySummary Component
// ==========================================
interface KbaPolicySummaryProps {
  id?: string;
  policy: TenantPolicy;
}

export const KbaPolicySummary: React.FC<KbaPolicySummaryProps> = ({ id, policy }) => {
  return (
    <div id={id || "kba-policy-summary"} className="bg-slate-50 border border-slate-200 rounded-xl p-4">
      <div className="flex items-center gap-2 mb-3">
        <Settings className="h-4 w-4 text-slate-700" />
        <h4 className="font-display font-semibold text-slate-900 text-sm">
          Active Tenant Security Policy
        </h4>
      </div>
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs">
        <div className="bg-white p-2 rounded-lg border border-slate-100 shadow-2xs">
          <span className="text-slate-400 block mb-0.5">Policy Status</span>
          <span className={`font-semibold ${policy.isKbaProhibited ? "text-red-600" : "text-emerald-600"}`}>
            {policy.isKbaProhibited ? "PROHIBITED (Disabled)" : "ENABLED (Restricted)"}
          </span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-100 shadow-2xs">
          <span className="text-slate-400 block mb-0.5">Vetting Mode</span>
          <span className="font-semibold text-slate-800">
            {policy.allowCustomQuestions ? "Custom Allowed" : "Strict Catalog Only"}
          </span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-100 shadow-2xs">
          <span className="text-slate-400 block mb-0.5">Challenge Scale</span>
          <span className="font-semibold text-slate-800">
            {policy.requiredQuestionCount} Questions
          </span>
        </div>
        <div className="bg-white p-2 rounded-lg border border-slate-100 shadow-2xs">
          <span className="text-slate-400 block mb-0.5">Session Expiry</span>
          <span className="font-semibold text-slate-800">
            {policy.sessionFreshnessSeconds}s (MFA Freshness)
          </span>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 7. CeremonyShell Component
// ==========================================
interface CeremonyShellProps {
  id?: string;
  title: string;
  subtitle: string;
  ceremonyType: CeremonyType;
  status: CeremonyStatus;
  statusText?: string;
  onReset?: () => void;
  children: React.ReactNode;
}

export const CeremonyShell: React.FC<CeremonyShellProps> = ({
  id,
  title,
  subtitle,
  ceremonyType,
  status,
  statusText,
  onReset,
  children
}) => {
  const getBannerColor = () => {
    switch (status) {
      case CeremonyStatus.SUCCESS:
        return "bg-emerald-50 text-emerald-800 border-emerald-200";
      case CeremonyStatus.RATE_LIMITED:
      case CeremonyStatus.BLOCKED:
      case CeremonyStatus.ATTEMPTS_EXHAUSTED:
        return "bg-rose-50 text-rose-800 border-rose-200";
      case CeremonyStatus.EXPIRED:
      case CeremonyStatus.PROVIDER_UNAVAILABLE:
        return "bg-amber-50 text-amber-800 border-amber-200";
      default:
        return "bg-slate-50 text-slate-700 border-slate-200";
    }
  };

  const getStatusIcon = () => {
    switch (status) {
      case CeremonyStatus.SUCCESS:
        return <CheckCircle2 className="h-5 w-5 text-emerald-600 shrink-0" />;
      case CeremonyStatus.RATE_LIMITED:
      case CeremonyStatus.BLOCKED:
      case CeremonyStatus.ATTEMPTS_EXHAUSTED:
        return <UserX className="h-5 w-5 text-rose-600 shrink-0" />;
      default:
        return <Activity className="h-5 w-5 text-amber-500 shrink-0" />;
    }
  };

  return (
    <div
      id={id || "ceremony-shell"}
      className="bg-white border border-slate-200 rounded-2xl shadow-xl overflow-hidden max-w-lg w-full mx-auto"
    >
      {/* Header */}
      <div className="bg-slate-900 px-6 py-5 text-white relative">
        <div className="flex justify-between items-start">
          <div>
            <span className="inline-flex items-center px-2 py-0.5 rounded text-[10px] font-semibold bg-slate-800 text-slate-300 border border-slate-700 uppercase tracking-wider mb-2">
              Ceremony: {ceremonyType.replace("_", " ")}
            </span>
            <h3 className="font-display font-semibold text-lg leading-tight">{title}</h3>
            <p className="text-xs text-slate-400 mt-1">{subtitle}</p>
          </div>
          <Fingerprint className="h-8 w-8 text-slate-400 opacity-80 shrink-0 mt-1" />
        </div>
      </div>

      {/* Dynamic Status Alert Banner */}
      {status !== CeremonyStatus.READY && status !== CeremonyStatus.SUBMITTING && (
        <div className={`px-6 py-3 border-b flex items-start gap-2.5 text-xs leading-relaxed ${getBannerColor()}`}>
          {getStatusIcon()}
          <div className="flex-1">
            <span className="font-semibold block capitalize">
              {status.replace("_", " ")} State
            </span>
            <p className="opacity-95">{statusText || "The authentication factor has entered a secured state."}</p>
          </div>
          {onReset && (
            <button
              onClick={onReset}
              className="text-xs font-bold underline shrink-0 hover:opacity-80 ml-2"
            >
              Retry
            </button>
          )}
        </div>
      )}

      {/* Body Content */}
      <div className="p-6">
        {status === CeremonyStatus.SUCCESS ? (
          <div id="ceremony-success-view" className="text-center py-6 space-y-4">
            <div className="inline-flex items-center justify-center h-14 w-14 rounded-full bg-emerald-100 text-emerald-600 border-4 border-emerald-50 mb-2">
              <Check className="h-7 w-7" />
            </div>
            <h4 className="font-display font-bold text-slate-900 text-lg">Ceremony Satisfied Successfully</h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Knowledge-Based Authentication completed with server cryptographic assurance token issued. Proceeding to downstream authorization parameters.
            </p>
            {onReset && (
              <button
                id="success-continue-btn"
                onClick={onReset}
                className="mt-2 px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold rounded-lg shadow transition-colors"
              >
                Simulate Next Session
              </button>
            )}
          </div>
        ) : status === CeremonyStatus.ATTEMPTS_EXHAUSTED || status === CeremonyStatus.BLOCKED ? (
          <div id="ceremony-locked-view" className="text-center py-6 space-y-4">
            <div className="inline-flex items-center justify-center h-14 w-14 rounded-full bg-rose-100 text-rose-600 border-4 border-rose-50 mb-2">
              <Lock className="h-7 w-7" />
            </div>
            <h4 className="font-display font-bold text-slate-900 text-lg">Identity Lockdown Initiated</h4>
            <p className="text-xs text-slate-500 max-w-sm mx-auto">
              Too many incorrect attempts have been made. To protect the account holder from public records lookup profiling, KBA authentication has been locked down.
            </p>
            <div className="bg-slate-50 p-3 rounded-lg border border-slate-100 max-w-xs mx-auto text-left text-xs text-slate-600 space-y-1">
              <p className="font-semibold text-slate-800">Available Fallbacks:</p>
              <ul className="list-disc pl-4 space-y-0.5 text-[11px] text-slate-500">
                <li>Supervised Administrator Reset Verification</li>
                <li>FIDO2 Hardware WebAuthn Key Presentation</li>
              </ul>
            </div>
            {onReset && (
              <button
                id="locked-reset-btn"
                onClick={onReset}
                className="mt-2 px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-600 text-xs font-semibold rounded-lg transition-colors inline-flex items-center gap-1"
              >
                <RotateCcw className="h-3.5 w-3.5" /> Reset Simulation
              </button>
            )}
          </div>
        ) : (
          children
        )}
      </div>
    </div>
  );
};

// ==========================================
// 8. AuthenticatorMethodPicker Component
// ==========================================
interface AuthenticatorMethodPickerProps {
  id?: string;
  isKbaEnrolled: boolean;
  isKbaProhibited: boolean;
  onSelectMethod: (method: "kba" | "passkey" | "totp" | "recovery") => void;
}

export const AuthenticatorMethodPicker: React.FC<AuthenticatorMethodPickerProps> = ({
  id,
  isKbaEnrolled,
  isKbaProhibited,
  onSelectMethod
}) => {
  return (
    <div id={id || "auth-method-picker"} className="space-y-3 max-w-md mx-auto">
      <p className="text-xs font-semibold text-slate-500 uppercase tracking-wider block mb-1">
        Select Authentication Factor
      </p>

      {/* Passkey */}
      <div
        id="picker-passkey"
        onClick={() => onSelectMethod("passkey")}
        className="flex items-center gap-3.5 p-4 border border-slate-200 hover:border-slate-400 bg-white hover:bg-slate-50 rounded-xl cursor-pointer transition-all shadow-xs group"
      >
        <div className="h-10 w-10 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center shrink-0">
          <Fingerprint className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-display font-semibold text-slate-900 text-sm">Passkey / Security Key</span>
            <span className="px-1.5 py-0.5 text-[9px] font-bold bg-indigo-100 text-indigo-800 rounded">HIGH ASSURANCE</span>
          </div>
          <p className="text-xs text-slate-400 truncate">Hardware-bound, phishing-resistant cryptographic session</p>
        </div>
        <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-slate-600 group-hover:translate-x-0.5 transition-all" />
      </div>

      {/* TOTP */}
      <div
        id="picker-totp"
        onClick={() => onSelectMethod("totp")}
        className="flex items-center gap-3.5 p-4 border border-slate-200 hover:border-slate-400 bg-white hover:bg-slate-50 rounded-xl cursor-pointer transition-all shadow-xs group"
      >
        <div className="h-10 w-10 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center shrink-0">
          <Smartphone className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2">
            <span className="font-display font-semibold text-slate-900 text-sm">Authenticator App (TOTP)</span>
            <span className="px-1.5 py-0.5 text-[9px] font-bold bg-blue-100 text-blue-800 rounded">MEDIUM</span>
          </div>
          <p className="text-xs text-slate-400 truncate">Time-based one-time passcode verification loop</p>
        </div>
        <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-slate-600 group-hover:translate-x-0.5 transition-all" />
      </div>

      {/* KBA */}
      <div
        id="picker-kba"
        onClick={() => {
          if (!isKbaProhibited && isKbaEnrolled) {
            onSelectMethod("kba");
          }
        }}
        className={`flex items-center gap-3.5 p-4 border rounded-xl transition-all shadow-xs group ${
          isKbaProhibited
            ? "opacity-55 cursor-not-allowed bg-slate-50 border-slate-200"
            : !isKbaEnrolled
            ? "border-slate-200 hover:border-slate-400 bg-white hover:bg-slate-50 cursor-pointer"
            : "border-slate-200 hover:border-slate-400 bg-white hover:bg-slate-50 cursor-pointer"
        }`}
      >
        <div className="h-10 w-10 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center shrink-0">
          <HelpCircle className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <span className="font-display font-semibold text-slate-900 text-sm">Security Questions (KBA)</span>
            <span className="px-1.5 py-0.5 text-[9px] font-bold bg-amber-100 text-amber-800 rounded">LOW ASSURANCE</span>
          </div>
          <p className="text-xs text-slate-400 truncate">
            {isKbaProhibited
              ? "Prohibited by enterprise compliance policy"
              : !isKbaEnrolled
              ? "Setup required before challenge eligibility"
              : "Verify via custom enrolled server-checked questions"}
          </p>
        </div>
        {!isKbaProhibited && (
          <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-slate-600 group-hover:translate-x-0.5 transition-all" />
        )}
      </div>

      {/* Governed Recovery */}
      <div
        id="picker-recovery"
        onClick={() => onSelectMethod("recovery")}
        className="flex items-center gap-3.5 p-4 border border-dashed border-slate-300 hover:border-slate-400 bg-slate-50/50 hover:bg-slate-50 rounded-xl cursor-pointer transition-all group"
      >
        <div className="h-10 w-10 rounded-lg bg-slate-100 text-slate-600 flex items-center justify-center shrink-0">
          <RefreshCw className="h-5 w-5" />
        </div>
        <div className="flex-1 min-w-0">
          <span className="font-display font-semibold text-slate-700 text-sm block">Governed Account Recovery</span>
          <p className="text-xs text-slate-400 truncate">Recover access with secondary factors and holding period delay</p>
        </div>
        <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-slate-600 group-hover:translate-x-0.5 transition-all" />
      </div>
    </div>
  );
};

// ==========================================
// 9. RecentAuthenticationGate Component
// ==========================================
interface RecentAuthenticationGateProps {
  id?: string;
  isOpen: boolean;
  onVerifySuccess: () => void;
  onCancel: () => void;
  requiredAssurance?: AssuranceLevel;
}

export const RecentAuthenticationGate: React.FC<RecentAuthenticationGateProps> = ({
  id,
  isOpen,
  onVerifySuccess,
  onCancel,
  requiredAssurance = AssuranceLevel.HIGH
}) => {
  const [passkeyVerifying, setPasskeyVerifying] = useState(false);

  if (!isOpen) return null;

  const handleSimulateHighAssurance = () => {
    setPasskeyVerifying(true);
    setTimeout(() => {
      setPasskeyVerifying(false);
      onVerifySuccess();
    }, 1200);
  };

  return (
    <div
      id={id || "recent-auth-gate"}
      className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4"
    >
      <motion.div
        initial={{ opacity: 0, scale: 0.95 }}
        animate={{ opacity: 1, scale: 1 }}
        exit={{ opacity: 0, scale: 0.95 }}
        className="bg-white border border-slate-200 rounded-2xl shadow-2xl max-w-md w-full overflow-hidden"
      >
        <div className="bg-slate-950 p-5 text-white flex items-center gap-3">
          <Lock className="h-6 w-6 text-indigo-400 shrink-0" />
          <div>
            <h3 className="font-display font-semibold text-sm md:text-base">Sensitive Step-Up Required</h3>
            <p className="text-xs text-slate-400">Validate your primary secure credential first</p>
          </div>
        </div>

        <div className="p-6 space-y-4">
          <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 flex gap-3 text-indigo-900">
            <Fingerprint className="h-5 w-5 text-indigo-600 shrink-0" />
            <div className="text-xs md:text-sm">
              <p className="font-semibold text-indigo-950 mb-0.5">High-Assurance MFA Binding Guard</p>
              <p className="text-indigo-800">
                To replace or remove an authenticator, security policy demands that you provide recent verification from a hardware-backed factor (such as a FIDO2 Passkey).
              </p>
            </div>
          </div>

          <div className="border border-slate-200 rounded-lg p-3 flex justify-between items-center bg-slate-50 text-xs">
            <span className="text-slate-500">Required Assurance</span>
            <span className="px-2 py-0.5 bg-indigo-100 text-indigo-800 font-semibold rounded uppercase">
              {requiredAssurance}
            </span>
          </div>

          <div className="flex justify-end gap-3 pt-2">
            <button
              id="gate-cancel-btn"
              onClick={onCancel}
              disabled={passkeyVerifying}
              className="px-4 py-2 border border-slate-200 text-xs font-medium rounded-lg text-slate-600 hover:bg-slate-50 transition-colors"
            >
              Cancel Action
            </button>
            <button
              id="gate-verify-btn"
              onClick={handleSimulateHighAssurance}
              disabled={passkeyVerifying}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold rounded-lg shadow transition-colors flex items-center gap-1.5"
            >
              {passkeyVerifying ? (
                <>
                  <RefreshCw className="h-3.5 w-3.5 animate-spin" /> Simulating Passkey...
                </>
              ) : (
                <>
                  <Fingerprint className="h-3.5 w-3.5" /> Present Passkey
                </>
              )}
            </button>
          </div>
        </div>
      </motion.div>
    </div>
  );
};

// ==========================================
// 10. AuthenticatorDetailPanel Component
// ==========================================
interface AuthenticatorDetailPanelProps {
  id?: string;
  credential: KbaUserCredential;
  policy: TenantPolicy;
  onReplaceTrigger: () => void;
  onRemoveTrigger: () => void;
}

export const AuthenticatorDetailPanel: React.FC<AuthenticatorDetailPanelProps> = ({
  id,
  credential,
  policy,
  onReplaceTrigger,
  onRemoveTrigger
}) => {
  const getStatusColor = () => {
    switch (credential.status) {
      case AuthenticatorStatus.ACTIVE:
        return "bg-emerald-50 text-emerald-700 border-emerald-200";
      case AuthenticatorStatus.SUSPENDED:
        return "bg-amber-50 text-amber-700 border-amber-200";
      case AuthenticatorStatus.COMPROMISED:
      case AuthenticatorStatus.REPLACEMENT_REQUIRED:
        return "bg-red-50 text-red-700 border-red-200";
      default:
        return "bg-slate-50 text-slate-600 border-slate-200";
    }
  };

  return (
    <div id={id || "auth-detail-panel"} className="bg-white border border-slate-200 rounded-xl shadow-xs overflow-hidden">
      <div className="bg-slate-900 p-4 text-white flex justify-between items-center">
        <div className="flex items-center gap-2">
          <HelpCircle className="h-5 w-5 text-amber-400" />
          <h4 className="font-display font-semibold text-sm">Security Questions Detail</h4>
        </div>
        <span className={`px-2 py-0.5 rounded text-[10px] font-bold border capitalize ${getStatusColor()}`}>
          {credential.status}
        </span>
      </div>

      <div className="p-4 space-y-4">
        {/* Core details */}
        <div className="grid grid-cols-2 gap-4 text-xs">
          <div>
            <span className="text-slate-400 block">Enrollment Ceremony</span>
            <span className="font-semibold text-slate-800">
              {credential.enrollmentDate ? new Date(credential.enrollmentDate).toLocaleString() : "Never"}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block">Last Verification Use</span>
            <span className="font-semibold text-slate-800">
              {credential.lastUsedDate ? new Date(credential.lastUsedDate).toLocaleString() : "Never"}
            </span>
          </div>
          <div>
            <span className="text-slate-400 block">Enrolled Questions count</span>
            <span className="font-semibold text-slate-800">
              {credential.enrolledQuestions.length} Vetted Questions
            </span>
          </div>
          <div>
            <span className="text-slate-400 block">Cryptographic Hashing</span>
            <span className="font-mono text-slate-600">HMAC-SHA256 (Salted)</span>
          </div>
        </div>

        {/* Security Warning */}
        <div className="bg-slate-50 border border-slate-100 rounded-lg p-3 text-slate-600 text-xs">
          <div className="flex gap-2">
            <Info className="h-4 w-4 text-slate-500 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-slate-800">Answer Privacy Protected</p>
              <p className="text-slate-500 mt-0.5 leading-relaxed">
                Neither support operators nor portal administrators can retrieve your raw security answers. They are verified purely through client-side normalization rules and server-side hashes.
              </p>
            </div>
          </div>
        </div>

        {/* Enrolled questions lookup */}
        {credential.enrolledQuestions.length > 0 && (
          <div className="space-y-2">
            <span className="text-xs font-semibold text-slate-500">Currently Enrolled Prompts:</span>
            <div className="space-y-1.5">
              {credential.enrolledQuestions.map((eq, idx) => (
                <div key={idx} className="bg-slate-50 border border-slate-100 rounded p-2 flex justify-between items-center text-xs">
                  <span className="text-slate-700 truncate max-w-[280px]">
                    {idx + 1}. {eq.questionText}
                  </span>
                  <span className="font-mono text-[9px] text-slate-400 shrink-0">
                    Hashed: {eq.normalizedHash.slice(0, 10)}...
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Action controls */}
        <div className="flex gap-3 pt-2 border-t border-slate-100">
          <button
            id="detail-replace-btn"
            onClick={onReplaceTrigger}
            className="flex-1 px-3 py-1.5 border border-slate-200 text-xs font-medium rounded-lg text-slate-700 hover:bg-slate-50 transition-colors flex items-center justify-center gap-1"
          >
            <RefreshCw className="h-3.5 w-3.5" /> Replace Questions
          </button>
          <button
            id="detail-remove-btn"
            onClick={onRemoveTrigger}
            className="flex-1 px-3 py-1.5 border border-red-200 text-xs font-medium rounded-lg text-red-700 hover:bg-red-50 transition-colors flex items-center justify-center gap-1"
          >
            <Trash2 className="h-3.5 w-3.5" /> Remove Authenticator
          </button>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 11. AuthenticatorEventTimeline Component
// ==========================================
interface AuthenticatorEventTimelineProps {
  id?: string;
  events: AuditEvent[];
}

export const AuthenticatorEventTimeline: React.FC<AuthenticatorEventTimelineProps> = ({
  id,
  events
}) => {
  return (
    <div id={id || "auth-event-timeline"} className="bg-white border border-slate-200 rounded-xl p-4 shadow-2xs">
      <div className="flex items-center gap-2 mb-4">
        <FileText className="h-4 w-4 text-slate-600" />
        <h4 className="font-display font-semibold text-slate-900 text-sm">Security Audit Logs & Events</h4>
      </div>
      <div className="space-y-4 max-h-[300px] overflow-y-auto pr-1">
        {events.length === 0 ? (
          <p className="text-xs text-slate-400 text-center py-4">No audit events logged yet.</p>
        ) : (
          events.map((evt) => (
            <div key={evt.id} className="relative pl-5 border-l border-slate-100 pb-1 text-xs">
              <div className={`absolute -left-1.5 top-1.5 h-3 w-3 rounded-full border-2 bg-white ${
                evt.status === "completed" || evt.status === CeremonyStatus.SUCCESS
                  ? "border-emerald-500"
                  : evt.status === "failed" || evt.status === CeremonyStatus.ATTEMPTS_EXHAUSTED
                  ? "border-red-500"
                  : "border-slate-300"
              }`} />
              <div className="flex items-center justify-between text-[11px] text-slate-400 mb-0.5">
                <span>{new Date(evt.timestamp).toLocaleTimeString()}</span>
                <span className="font-mono text-[10px]">{evt.id}</span>
              </div>
              <p className="font-semibold text-slate-800">
                {evt.action.replace("_", " ").toUpperCase()} ({evt.ceremonyType})
              </p>
              <p className="text-slate-500 text-[11px] mt-0.5 leading-relaxed">{evt.details}</p>
              <div className="flex gap-2 items-center mt-1 text-[10px] text-slate-400">
                <span className="font-mono">IP: {evt.ipAddress}</span>
                <span>•</span>
                <span>Assurance: <span className="font-semibold uppercase">{evt.assuranceLevel}</span></span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

// ==========================================
// 12. PolicyImpactPreview Component
// ==========================================
interface PolicyImpactPreviewProps {
  id?: string;
  policy: TenantPolicy;
}

export const PolicyImpactPreview: React.FC<PolicyImpactPreviewProps> = ({
  id,
  policy
}) => {
  return (
    <div id={id || "policy-impact-preview"} className="bg-slate-900 text-slate-300 rounded-xl p-4 border border-slate-800">
      <div className="flex items-center gap-2 mb-3">
        <Terminal className="h-4 w-4 text-amber-400 animate-pulse" />
        <h4 className="font-display font-semibold text-white text-sm">Real-time Policy Simulator</h4>
      </div>
      <div className="space-y-3.5 text-xs">
        <p className="text-slate-400 text-[11px]">
          Simulating system behavior under current rule settings:
        </p>

        {/* Prohibited Alert */}
        {policy.isKbaProhibited ? (
          <div className="bg-red-950/50 border border-red-900 text-red-300 p-2.5 rounded-lg flex items-start gap-2">
            <XCircle className="h-4 w-4 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-white">Rule Impact: Hard Prohibited</p>
              <p className="text-[11px] opacity-90">KBA registration is strictly blocked. Users are restricted to passkeys/TOTP hardware.</p>
            </div>
          </div>
        ) : (
          <div className="bg-emerald-950/50 border border-emerald-900 text-emerald-300 p-2.5 rounded-lg flex items-start gap-2">
            <CheckCircle2 className="h-4 w-4 shrink-0 mt-0.5" />
            <div>
              <p className="font-semibold text-white">Rule Impact: Restricted Enrollment Permitted</p>
              <p className="text-[11px] opacity-90">KBA allowed strictly as secondary/recovery option under low-assurance policy constraints.</p>
            </div>
          </div>
        )}

        {/* Scoring Scale */}
        <div className="bg-slate-850 p-2.5 rounded border border-slate-800 space-y-1">
          <div className="flex justify-between font-semibold text-slate-200">
            <span>Challenge Scale constraint</span>
            <span>{policy.requiredQuestionCount} Questions</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-snug">
            The verification ceremony requires the user to answer exactly {policy.requiredQuestionCount} distinct questions consecutively with 100% correct matching.
          </p>
        </div>

        {/* Lockout Rule */}
        <div className="bg-slate-850 p-2.5 rounded border border-slate-800 space-y-1">
          <div className="flex justify-between font-semibold text-slate-200">
            <span>Attempt Budget Threshold</span>
            <span>{policy.maxAttempts} Tries</span>
          </div>
          <p className="text-[11px] text-slate-400 leading-snug">
            Exceeding {policy.maxAttempts} cumulative answer errors triggers a hard lockout duration of {policy.lockoutDurationMinutes} minutes, raising an alarm in the Abuse Diagnostics.
          </p>
        </div>
      </div>
    </div>
  );
};

// ==========================================
// 13. DangerZone Component
// ==========================================
interface DangerZoneProps {
  id?: string;
  isKbaEnrolled: boolean;
  onRemoveRequest: () => void;
  onCompromiseSimulate: () => void;
}

export const DangerZone: React.FC<DangerZoneProps> = ({
  id,
  isKbaEnrolled,
  onRemoveRequest,
  onCompromiseSimulate
}) => {
  return (
    <div id={id || "danger-zone"} className="border border-red-200 bg-red-50/50 rounded-xl overflow-hidden">
      <div className="bg-red-900 p-3 text-white flex items-center gap-2">
        <AlertTriangle className="h-4 w-4" />
        <h4 className="font-display font-bold text-xs uppercase tracking-wider">Security Danger Zone</h4>
      </div>
      <div className="p-4 space-y-4">
        <div>
          <h5 className="text-xs font-semibold text-slate-900">Exposed Answer / Breach Response</h5>
          <p className="text-[11px] text-slate-500 leading-normal mt-0.5">
            If security questions are suspected of being compromised or leaked via a third-party social breach, instantly flag the status as "compromised" to enforce step-up MFA.
          </p>
          <button
            id="danger-compromise-btn"
            onClick={onCompromiseSimulate}
            disabled={!isKbaEnrolled}
            className="mt-2 text-xs font-semibold px-3 py-1 bg-red-100 hover:bg-red-200 border border-red-200 text-red-800 rounded-lg transition-colors disabled:opacity-50"
          >
            Trigger Compromise Alarm
          </button>
        </div>

        <div className="pt-3 border-t border-red-100">
          <h5 className="text-xs font-semibold text-slate-900">Proportional Last-Factor Lockout Guard</h5>
          <p className="text-[11px] text-slate-500 leading-normal mt-0.5">
            Removing KBA leaves your account protected by other enrolled factors. The system prevents removing your last active authenticator factor to secure you against complete lockout.
          </p>
          <button
            id="danger-remove-btn"
            onClick={onRemoveRequest}
            disabled={!isKbaEnrolled}
            className="mt-2 text-xs font-semibold px-3 py-1.5 bg-red-600 hover:bg-red-700 text-white rounded-lg shadow-sm transition-colors disabled:opacity-50 inline-flex items-center gap-1"
          >
            <Trash2 className="h-3.5 w-3.5" /> Force Removal Ceremony
          </button>
        </div>
      </div>
    </div>
  );
};
