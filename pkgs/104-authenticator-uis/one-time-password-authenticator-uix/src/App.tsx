/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect, useRef } from "react";
import { 
  Shield, 
  KeyRound, 
  Lock, 
  Unlock, 
  RotateCw, 
  Trash2, 
  Plus, 
  QrCode, 
  Settings, 
  Users, 
  FileCode, 
  Clipboard, 
  Clock, 
  CheckCircle, 
  XCircle, 
  AlertTriangle, 
  Smartphone, 
  RefreshCw, 
  Copy, 
  HelpCircle, 
  Check, 
  ArrowRight, 
  Flame, 
  Sliders, 
  Search, 
  ShieldCheck, 
  Eye, 
  EyeOff,
  UserCheck,
  Power,
  History
} from "lucide-react";
import { 
  OtpAlgorithm, 
  FactorStatus, 
  AuthenticatorProfile, 
  AuditLog, 
  TenantPolicy, 
  SecurityPosture, 
  SimulationState 
} from "./types";
import { 
  generateBase32Secret, 
  generateTOTP, 
  verifyTOTP, 
  generateRecoveryCodes, 
  formatTime, 
  DEFAULT_POLICY, 
  INITIAL_AUTHENTICATORS, 
  INITIAL_AUDIT_LOGS 
} from "./utils";

export default function App() {
  // --- Persistent State & LocalStorage Helpers ---
  const [authenticators, setAuthenticators] = useState<AuthenticatorProfile[]>(() => {
    const stored = localStorage.getItem("otp_authenticators");
    return stored ? JSON.parse(stored) : INITIAL_AUTHENTICATORS;
  });

  const [policy, setPolicy] = useState<TenantPolicy>(() => {
    const stored = localStorage.getItem("otp_policy");
    return stored ? JSON.parse(stored) : DEFAULT_POLICY;
  });

  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(() => {
    const stored = localStorage.getItem("otp_audit_logs");
    return stored ? JSON.parse(stored) : INITIAL_AUDIT_LOGS;
  });

  const [posture, setPosture] = useState<SecurityPosture>({
    failedAttemptsCount: 0,
    isLockedOut: false,
    lockoutExpiresAt: undefined,
    lastSuccessfulAuth: undefined,
    recentVerificationType: null,
    activeStepUpChallenge: null,
  });

  const [simulation, setSimulation] = useState<SimulationState>({
    currentTimeSkewSeconds: 0,
    simulateReplayAttack: false,
    simulateStorageFailure: false,
    simulateNoRecoveryCode: false,
  });

  // --- Synchronization & Side Effects ---
  useEffect(() => {
    localStorage.setItem("otp_authenticators", JSON.stringify(authenticators));
  }, [authenticators]);

  useEffect(() => {
    localStorage.setItem("otp_policy", JSON.stringify(policy));
  }, [policy]);

  useEffect(() => {
    localStorage.setItem("otp_audit_logs", JSON.stringify(auditLogs));
  }, [auditLogs]);

  // --- Active Views state ---
  // "LOGIN" | "MFA_CHOOSER" | "MFA_CHALLENGE" | "STEP_UP" | "SUCCESS" | "PROFILE" | "ENROLL_INTRO" | "ENROLL_REVEAL" | "ENROLL_VERIFY" | "ENROLL_NAME" | "ENROLL_RECOVERY" | "ENROLL_COMPLETED" | "RECOVERY_RESET"
  const [currentView, setCurrentView] = useState<string>("LOGIN");
  
  // Active states for challenge entry
  const [activeFactor, setActiveFactor] = useState<AuthenticatorProfile | null>(null);
  const [challengeCode, setChallengeCode] = useState<string[]>([]);
  const [challengeError, setChallengeError] = useState<string | null>(null);
  const [challengeState, setChallengeState] = useState<"ready" | "submitting" | "invalid" | "expired" | "replayed" | "rate_limited" | "success">("ready");
  
  // Replay protection set (mock database)
  const [verifiedCodesStore, setVerifiedCodesStore] = useState<string[]>([]);

  // Enrollment process state
  const [enrollmentFactor, setEnrollmentFactor] = useState<AuthenticatorProfile | null>(null);
  const [enrollmentSecretRevealed, setEnrollmentSecretRevealed] = useState<boolean>(false);
  const [enrollmentVerifyCode, setEnrollmentVerifyCode] = useState<string[]>([]);
  const [enrollmentError, setEnrollmentError] = useState<string | null>(null);
  const [enrollmentLabel, setEnrollmentLabel] = useState<string>("");
  const [recoveryCodes, setRecoveryCodes] = useState<string[]>([]);
  const [recoveryConfirmed, setRecoveryConfirmed] = useState<boolean>(false);
  
  // Custom toast notification
  const [toast, setToast] = useState<{ message: string; type: "success" | "error" | "info" } | null>(null);

  // Time remaining for current TOTP step
  const [timeRemaining, setTimeRemaining] = useState<number>(30);

  // Countdown timer for challenge
  const [challengeCountdown, setChallengeCountdown] = useState<number>(30);

  // Active step-up action text
  const [activeStepUpText, setActiveStepUpText] = useState<string>("Wire Transfer Authorization ($12,500.00 to vendor LLC)");

  // Reference for input fields to support focus jumping and pasting
  const inputRefs = useRef<(HTMLInputElement | null)[]>([]);

  // --- Real-time Tick Loop ---
  useEffect(() => {
    const interval = setInterval(() => {
      const nowSeconds = Math.floor(Date.now() / 1000);
      const activePeriod = policy.allowedPeriods[0] || 30;
      const remaining = activePeriod - (nowSeconds % activePeriod);
      setTimeRemaining(remaining);
    }, 1000);
    return () => clearInterval(interval);
  }, [policy.allowedPeriods]);

  // Challenge countdown timer
  useEffect(() => {
    let timer: NodeJS.Timeout;
    if (currentView === "MFA_CHALLENGE" && challengeCountdown > 0 && challengeState === "ready") {
      timer = setTimeout(() => {
        setChallengeCountdown(prev => prev - 1);
      }, 1000);
    } else if (challengeCountdown === 0 && currentView === "MFA_CHALLENGE" && challengeState === "ready") {
      setChallengeState("expired");
      setChallengeError("Verification code has expired. Please use the current code.");
      addAuditLog("AUTH_FAIL", "j.austin@enterprise.com", `Challenge expired for factor ${activeFactor?.label}`, "warning");
    }
    return () => clearTimeout(timer);
  }, [challengeCountdown, currentView, challengeState, activeFactor]);

  // --- Helper: Add Audit Log ---
  const addAuditLog = (
    eventType: AuditLog["eventType"],
    actor: string,
    details: string,
    status: AuditLog["status"]
  ) => {
    const newLog: AuditLog = {
      id: `log-${Date.now()}-${Math.floor(Math.random() * 1000)}`,
      timestamp: new Date().toISOString(),
      eventType,
      actor,
      details,
      status,
      ipAddress: "192.168.1.108",
      requestId: `req-${Math.random().toString(36).substr(2, 8)}`,
    };
    setAuditLogs(prev => [newLog, ...prev].slice(0, 40));
  };

  // --- Trigger Global Feedback Toast ---
  const triggerToast = (message: string, type: "success" | "error" | "info" = "info") => {
    setToast({ message, type });
    setTimeout(() => setToast(null), 3500);
  };

  // --- TOTP Generation for Simulator ---
  const getSimulatedTotpCode = (profile: AuthenticatorProfile) => {
    return generateTOTP(
      profile.secret,
      simulation.currentTimeSkewSeconds,
      profile.period,
      profile.digits
    );
  };

  // --- Handler: Autofill code from Simulator ---
  const handleAutofill = (code: string) => {
    const targetDigits = activeFactor ? activeFactor.digits : enrollmentFactor ? enrollmentFactor.digits : 6;
    const splitCode = code.slice(0, targetDigits).split("");
    
    if (currentView === "MFA_CHALLENGE" || currentView === "STEP_UP") {
      const newCode = [...challengeCode];
      for (let i = 0; i < targetDigits; i++) {
        newCode[i] = splitCode[i] || "";
      }
      setChallengeCode(newCode);
      triggerToast("Auto-filled code from Authenticator Simulator", "success");
      
      setTimeout(() => {
        inputRefs.current[targetDigits - 1]?.focus();
      }, 50);
    } else if (currentView === "ENROLL_VERIFY") {
      const newCode = [...enrollmentVerifyCode];
      for (let i = 0; i < targetDigits; i++) {
        newCode[i] = splitCode[i] || "";
      }
      setEnrollmentVerifyCode(newCode);
      triggerToast("Auto-filled initial setup verification code", "success");
      
      setTimeout(() => {
        inputRefs.current[targetDigits - 1]?.focus();
      }, 50);
    }
  };

  // --- Handler: Paste Support ---
  const handlePaste = (e: React.ClipboardEvent<HTMLInputElement>, target: "challenge" | "enroll") => {
    e.preventDefault();
    const pastedData = e.clipboardData.getData("text").trim();
    if (!/^\d+$/.test(pastedData)) {
      triggerToast("Paste failed: Clipboard contents must contain only numbers", "error");
      return;
    }

    const targetDigits = activeFactor ? activeFactor.digits : enrollmentFactor ? enrollmentFactor.digits : 6;
    const splitCode = pastedData.slice(0, targetDigits).split("");

    if (target === "challenge") {
      const newCode = [...challengeCode];
      for (let i = 0; i < targetDigits; i++) {
        newCode[i] = splitCode[i] || "";
      }
      setChallengeCode(newCode);
      inputRefs.current[Math.min(pastedData.length, targetDigits) - 1]?.focus();
    } else {
      const newCode = [...enrollmentVerifyCode];
      for (let i = 0; i < targetDigits; i++) {
        newCode[i] = splitCode[i] || "";
      }
      setEnrollmentVerifyCode(newCode);
      inputRefs.current[Math.min(pastedData.length, targetDigits) - 1]?.focus();
    }
    triggerToast("Verification code pasted successfully", "success");
  };

  // --- Action: Initialize Login ---
  const startLoginFlow = () => {
    const totpFactors = authenticators.filter(a => a.status === FactorStatus.ACTIVE);
    if (totpFactors.length === 0) {
      triggerToast("No active OTP authenticators found. Directing to secure enrollment.", "info");
      initiateEnrollment();
      return;
    }

    const defaultFactor = totpFactors.find(f => f.type === "totp") || totpFactors[0];
    setActiveFactor(defaultFactor);
    setChallengeCode(new Array(defaultFactor.digits).fill(""));
    setChallengeError(null);
    setChallengeState("ready");
    setChallengeCountdown(defaultFactor.period);
    setCurrentView("MFA_CHOOSER");
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", "Password credentials approved. Proceeding to possession factor check.", "info");
  };

  // --- Action: Select MFA Factor ---
  const selectMfaFactor = (factor: AuthenticatorProfile) => {
    if (factor.status !== FactorStatus.ACTIVE) {
      triggerToast("Factor is currently inactive, suspended or revoked", "error");
      return;
    }
    setActiveFactor(factor);
    setChallengeCode(new Array(factor.digits).fill(""));
    setChallengeError(null);
    setChallengeState("ready");
    setChallengeCountdown(factor.period);
    setCurrentView("MFA_CHALLENGE");
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", `Possession challenge issued for factor: ${factor.label}`, "info");
  };

  // --- Action: Resend Delivered OTP (SMS/Email) ---
  const triggerResendCode = () => {
    if (!activeFactor || activeFactor.type === "totp") return;
    
    setChallengeState("ready");
    setChallengeError(null);
    setChallengeCountdown(activeFactor.period);
    
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", `Delivered new OTP code to customer pathway: ${activeFactor.deliveryTarget}`, "info");
    triggerToast(`New OTP code delivered to ${activeFactor.deliveryTarget}!`, "success");
  };

  // --- Action: Submit Challenge Code ---
  const submitChallengeCode = () => {
    if (!activeFactor) return;

    if (simulation.simulateStorageFailure) {
      setChallengeState("invalid");
      setChallengeError("Identity Storage Service outage (503). Cannot communicate with provider.");
      addAuditLog("AUTH_FAIL", "j.austin@enterprise.com", "Authentication halted: Identity storage service unresponsive", "error");
      return;
    }

    const fullCode = challengeCode.join("");
    if (fullCode.length !== activeFactor.digits) {
      setChallengeState("invalid");
      setChallengeError(`Please enter a complete ${activeFactor.digits}-digit code.`);
      return;
    }

    setChallengeState("submitting");

    setTimeout(() => {
      // Replay attack simulation
      if (simulation.simulateReplayAttack && verifiedCodesStore.includes(fullCode)) {
        setChallengeState("replayed");
        setChallengeError("Replay Protection triggered: This OTP code was already used within the valid window.");
        addAuditLog("REPLAY_REJECT", "j.austin@enterprise.com", `Replayed code rejected: ${fullCode}`, "error");
        return;
      }

      // Lockout check
      if (posture.failedAttemptsCount >= policy.attemptsLimit) {
        setChallengeState("rate_limited");
        setChallengeError("Account locked. Too many failed verification attempts. Administrative help-desk reset required.");
        addAuditLog("LOCKOUT_TRIGGERED", "j.austin@enterprise.com", "Maximum verification attempts exhausted", "error");
        return;
      }

      // Cryptographic TOTP algorithm validation
      const validation = verifyTOTP(
        fullCode,
        activeFactor.secret,
        simulation.currentTimeSkewSeconds,
        activeFactor.period,
        activeFactor.digits,
        policy.driftWindowGrace,
        new Set(verifiedCodesStore)
      );

      if (validation.success) {
        setVerifiedCodesStore(prev => [...prev, fullCode]);
        setChallengeState("success");
        setPosture(prev => ({
          ...prev,
          failedAttemptsCount: 0,
          lastSuccessfulAuth: new Date().toISOString(),
          recentVerificationType: activeFactor.type,
        }));

        let auditDetail = `MFA challenge verified successfully via ${activeFactor.label}`;
        if (validation.driftSteps !== 0) {
          auditDetail += ` (Clock drift of ${validation.driftSteps} step(s) automatically corrected and aligned)`;
          addAuditLog("DRIFT_CORRECTED", "j.austin@enterprise.com", `Drift alignment registered (${validation.driftSteps > 0 ? "+" : ""}${validation.driftSteps} period)`, "info");
        }

        addAuditLog("AUTH_SUCCESS", "j.austin@enterprise.com", auditDetail, "success");
        triggerToast("Authentication verified successfully!", "success");

        setTimeout(() => {
          setCurrentView("SUCCESS");
        }, 1000);
      } else {
        const attemptsLeft = policy.attemptsLimit - (posture.failedAttemptsCount + 1);
        setPosture(prev => ({
          ...prev,
          failedAttemptsCount: prev.failedAttemptsCount + 1,
        }));

        setChallengeState("invalid");
        if (attemptsLeft <= 0) {
          setChallengeState("rate_limited");
          setChallengeError("Maximum verification attempts reached. Account locked.");
          addAuditLog("LOCKOUT_TRIGGERED", "j.austin@enterprise.com", "Authentication attempts exceeded policy safety limit.", "error");
        } else {
          setChallengeError(`Invalid verification code. ${attemptsLeft} attempts remaining before account lock.`);
          addAuditLog("AUTH_FAIL", "j.austin@enterprise.com", `Failed verification attempt via ${activeFactor.label}`, "warning");
        }
      }
    }, 500);
  };

  // --- Action: Initiate Step-Up ---
  const triggerStepUp = () => {
    const totpFactors = authenticators.filter(a => a.status === FactorStatus.ACTIVE);
    if (totpFactors.length === 0) {
      triggerToast("No active authenticator enrolled for step-up. Please enroll one first.", "error");
      return;
    }
    const defaultFactor = totpFactors.find(f => f.type === "totp") || totpFactors[0];
    setActiveFactor(defaultFactor);
    setChallengeCode(new Array(defaultFactor.digits).fill(""));
    setChallengeError(null);
    setChallengeState("ready");
    setChallengeCountdown(defaultFactor.period);
    setCurrentView("STEP_UP");
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", `Step-up authentication ceremony started for: "${activeStepUpText}"`, "warning");
  };

  // --- Action: Complete Step-Up ---
  const submitStepUpCode = () => {
    if (!activeFactor) return;

    const fullCode = challengeCode.join("");
    if (fullCode.length !== activeFactor.digits) {
      setChallengeError(`Enter complete ${activeFactor.digits}-digit code.`);
      return;
    }

    setChallengeState("submitting");

    setTimeout(() => {
      const validation = verifyTOTP(
        fullCode,
        activeFactor.secret,
        simulation.currentTimeSkewSeconds,
        activeFactor.period,
        activeFactor.digits,
        policy.driftWindowGrace,
        new Set(verifiedCodesStore)
      );

      if (validation.success) {
        setVerifiedCodesStore(prev => [...prev, fullCode]);
        setChallengeState("success");
        addAuditLog("STEP_UP_SUCCESS", "j.austin@enterprise.com", `High-privilege step-up approved: ${activeStepUpText}`, "success");
        triggerToast("Ceremony Authorized Successfully!", "success");
        setTimeout(() => {
          setCurrentView("PROFILE");
        }, 1200);
      } else {
        setChallengeState("invalid");
        setChallengeError("Invalid step-up authorization code.");
        addAuditLog("AUTH_FAIL", "j.austin@enterprise.com", `Step-up rejected: incorrect verification code`, "error");
      }
    }, 500);
  };

  // --- Action: Account Recovery Reset ---
  const startRecoveryReset = () => {
    setCurrentView("RECOVERY_RESET");
    setChallengeCode(["", "", "", "", "", ""]);
    setChallengeError(null);
    setChallengeState("ready");
  };

  const submitRecoveryReset = () => {
    const codeStr = challengeCode.join("");
    if (codeStr.length < 6) {
      setChallengeError("Please enter a valid backup recovery key.");
      return;
    }

    setChallengeState("submitting");
    setTimeout(() => {
      setPosture(prev => ({
        ...prev,
        failedAttemptsCount: 0,
        isLockedOut: false,
      }));
      addAuditLog("ADMIN_RESET", "j.austin@enterprise.com", "Self-service user account recovered via multi-use recovery key", "success");
      triggerToast("Account successfully unlocked!", "success");
      setCurrentView("PROFILE");
    }, 800);
  };

  // --- Action: Initiate Enrollment ---
  const initiateEnrollment = () => {
    const generatedSecret = generateBase32Secret();
    const newFactor: AuthenticatorProfile = {
      id: `auth-totp-${Date.now()}`,
      label: "My Authenticator App",
      type: "totp",
      status: FactorStatus.ENROLLMENT_PENDING,
      secret: generatedSecret,
      digits: policy.allowedDigits[0] || 6,
      period: policy.allowedPeriods[0] || 30,
      algorithm: policy.allowedAlgorithms[0] || OtpAlgorithm.SHA1,
      created: new Date().toISOString(),
    };

    setEnrollmentFactor(newFactor);
    setEnrollmentSecretRevealed(false);
    setEnrollmentVerifyCode(new Array(newFactor.digits).fill(""));
    setEnrollmentError(null);
    setEnrollmentLabel("");
    setRecoveryCodes(generateRecoveryCodes());
    setRecoveryConfirmed(false);
    setCurrentView("ENROLL_INTRO");
    
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", "Started new TOTP authenticator enrollment ceremony", "info");
  };

  // --- Action: Reveal Secret Seed ---
  const handleRevealSecret = () => {
    setEnrollmentSecretRevealed(true);
    if (enrollmentFactor) {
      const updated = { ...enrollmentFactor, status: FactorStatus.SECRET_REVEALED };
      setEnrollmentFactor(updated);
    }
    addAuditLog("ENROLL_INIT", "j.austin@enterprise.com", "TOTP registration seed exposed to user browser once", "warning");
  };

  // --- Action: Verify Initial Setup Code ---
  const verifyInitialEnrollmentCode = () => {
    if (!enrollmentFactor) return;
    const fullCode = enrollmentVerifyCode.join("");
    if (fullCode.length !== enrollmentFactor.digits) {
      setEnrollmentError(`Please enter the full ${enrollmentFactor.digits}-digit code.`);
      return;
    }

    const validation = verifyTOTP(
      fullCode,
      enrollmentFactor.secret,
      simulation.currentTimeSkewSeconds,
      enrollmentFactor.period,
      enrollmentFactor.digits,
      0 // Strict alignment required for initial setup proof
    );

    if (validation.success) {
      setEnrollmentError(null);
      setCurrentView("ENROLL_NAME");
      addAuditLog("ENROLL_VERIFY_SUCCESS", "j.austin@enterprise.com", "Initial setup challenge approved. Seed possession verified.", "success");
      triggerToast("Setup code approved!", "success");
    } else {
      setEnrollmentError("Verification failed. Please ensure your clock is synced and enter the active code shown in the simulator.");
      addAuditLog("ENROLL_VERIFY_FAIL", "j.austin@enterprise.com", "Initial setup verification code failed", "error");
    }
  };

  // --- Action: Save Name & Advance ---
  const saveAuthenticatorName = () => {
    if (!enrollmentFactor) return;
    const finalLabel = enrollmentLabel.trim() || "Authenticator Factor";
    setEnrollmentFactor({
      ...enrollmentFactor,
      label: finalLabel,
    });
    setCurrentView("ENROLL_RECOVERY");
  };

  // --- Action: Complete Enrollment Activation ---
  const activateAuthenticatorFactor = () => {
    if (!enrollmentFactor || !recoveryConfirmed) return;

    const activatedFactor: AuthenticatorProfile = {
      ...enrollmentFactor,
      status: FactorStatus.ACTIVE,
      created: new Date().toISOString(),
      lastUsed: new Date().toISOString(),
    };

    // Replace or add to authenticators. If replacement requested, we retain previous state overlap until this verify.
    setAuthenticators(prev => [
      activatedFactor,
      ...prev.filter(f => f.status === FactorStatus.ACTIVE)
    ]);

    // Clear client-side cache of raw seeds
    setEnrollmentSecretRevealed(false);
    setCurrentView("ENROLL_COMPLETED");
    addAuditLog("ENROLL_VERIFY_SUCCESS", "j.austin@enterprise.com", `New authenticator activated: "${activatedFactor.label}"`, "success");
    triggerToast("Factor activated successfully!", "success");
  };

  // --- Action: Suspend / Revoke ---
  const toggleFactorStatus = (id: string, status: FactorStatus) => {
    setAuthenticators(prev => prev.map(f => {
      if (f.id === id) {
        const updated = { ...f, status };
        addAuditLog(
          status === FactorStatus.SUSPENDED ? "FACTOR_SUSPENDED" : "FACTOR_REVOKED", 
          "admin@enterprise.com", 
          `MFA factor "${f.label}" status updated to ${status}`, 
          "warning"
        );
        return updated;
      }
      return f;
    }));
    triggerToast(`Factor updated to ${status}`, "info");
  };

  const removeFactor = (id: string) => {
    const activeLeft = authenticators.filter(f => f.id !== id && f.status === FactorStatus.ACTIVE);
    if (activeLeft.length === 0 && policy.forceMfa) {
      triggerToast("Cannot remove last active factor. Tenant security policy requires MFA enforcement.", "error");
      addAuditLog("FACTOR_REVOKED", "admin@enterprise.com", "Factor deletion blocked: Policy mandates at least one active factor", "error");
      return;
    }

    setAuthenticators(prev => prev.filter(f => f.id !== id));
    addAuditLog("FACTOR_REVOKED", "admin@enterprise.com", `MFA Factor ID ${id} revoked and deleted.`, "error");
    triggerToast("Factor removed.", "success");
  };

  // --- Action: Help-Desk Admin Reset ---
  const handleAdminResetAll = () => {
    setAuthenticators(INITIAL_AUTHENTICATORS);
    setPolicy(DEFAULT_POLICY);
    setPosture({
      failedAttemptsCount: 0,
      isLockedOut: false,
      lockoutExpiresAt: undefined,
      lastSuccessfulAuth: undefined,
      recentVerificationType: null,
      activeStepUpChallenge: null,
    });
    setSimulation({
      currentTimeSkewSeconds: 0,
      simulateReplayAttack: false,
      simulateStorageFailure: false,
      simulateNoRecoveryCode: false,
    });
    setVerifiedCodesStore([]);
    setAuditLogs(INITIAL_AUDIT_LOGS);
    triggerToast("System configuration reset to defaults", "success");
    addAuditLog("ADMIN_RESET", "admin@enterprise.com", "Administrative global hard reset triggered", "warning");
    setCurrentView("LOGIN");
  };

  // --- Input Jump Handler helper ---
  const handleInputChange = (val: string, index: number, total: number, target: "challenge" | "enroll") => {
    const cleanVal = val.replace(/\D/g, "");
    const codeArr = target === "challenge" ? [...challengeCode] : [...enrollmentVerifyCode];
    codeArr[index] = cleanVal.slice(-1);

    if (target === "challenge") {
      setChallengeCode(codeArr);
    } else {
      setEnrollmentVerifyCode(codeArr);
    }

    if (cleanVal && index < total - 1) {
      inputRefs.current[index + 1]?.focus();
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>, index: number, target: "challenge" | "enroll") => {
    if (e.key === "Backspace") {
      const codeArr = target === "challenge" ? [...challengeCode] : [...enrollmentVerifyCode];
      if (!codeArr[index] && index > 0) {
        inputRefs.current[index - 1]?.focus();
      }
    }
  };

  return (
    <div id="app-root" className="w-full min-h-screen bg-slate-50 flex flex-col font-sans text-slate-800">
      
      {/* Toast Banner */}
      {toast && (
        <div className="fixed top-5 left-1/2 -translate-x-1/2 z-50 flex items-center gap-2.5 px-4.5 py-3 bg-slate-900 text-white text-xs font-semibold rounded-xl shadow-xl border border-slate-700 animate-fade-in">
          <Shield className="w-4 h-4 text-indigo-400" />
          <span>{toast.message}</span>
        </div>
      )}

      {/* Main Header / Title Bar */}
      <nav className="h-16 border-b border-slate-200 bg-white flex items-center justify-between px-8 flex-shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 bg-slate-900 rounded flex items-center justify-center">
            <Shield className="w-5 h-5 text-white" />
          </div>
          <div>
            <span className="font-bold tracking-tight text-base font-display text-slate-900">TIGRBL Identity</span>
            <span className="text-[10px] block text-slate-400 font-mono -mt-1 uppercase tracking-wider">Possession Factor Ceremony</span>
          </div>
        </div>
        
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-3 bg-slate-50 px-4 py-1.5 rounded-lg border border-slate-100">
            <div className="flex flex-col items-end">
              <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider">Subject Principal</span>
              <span className="text-xs font-medium text-slate-700 font-mono">j.austin@enterprise.com</span>
            </div>
            <div className="w-8 h-8 rounded-full bg-slate-200 border border-slate-300 flex items-center justify-center font-bold text-xs text-slate-600">
              JA
            </div>
          </div>
        </div>
      </nav>

      {/* Primary Panels Layout */}
      <div className="flex-1 flex flex-col lg:flex-row overflow-hidden">
        
        {/* ================= LEFT SIDE PANEL: SIMULATORS & SIMULATION CONTROLS ================= */}
        <aside className="w-full lg:w-80 border-r border-slate-200 bg-white p-6 flex flex-col overflow-y-auto space-y-6">
          
          {/* Simulated External Authenticator App */}
          <div>
            <div className="flex items-center justify-between mb-3">
              <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5">
                <Smartphone className="w-4 h-4 text-slate-400" />
                <span>Authenticator Simulator</span>
              </h2>
              <div className="flex items-center gap-1 text-[10px] text-indigo-600 bg-indigo-50 px-1.5 py-0.5 rounded font-mono">
                <Clock className="w-3 h-3" />
                <span>{timeRemaining}s</span>
              </div>
            </div>

            <div className="p-4 bg-slate-950 text-white rounded-xl space-y-4 border border-slate-800 shadow-inner">
              <p className="text-[10px] text-slate-400 leading-tight">
                This simulator mirrors an external app (like Google Authenticator). Select any factor below to generate or auto-fill valid codes.
              </p>

              {/* Loop factors for quick code check */}
              <div className="space-y-3 pt-1">
                {authenticators.map(factor => {
                  const currentCode = getSimulatedTotpCode(factor);
                  const isSuspended = factor.status === FactorStatus.SUSPENDED;
                  
                  return (
                    <div key={factor.id} className="p-3 bg-slate-900/60 rounded-lg border border-slate-800/80 flex items-center justify-between">
                      <div className="min-w-0">
                        <span className="text-xs font-semibold text-slate-200 block truncate">{factor.label}</span>
                        <span className="text-[9px] text-slate-400 font-mono uppercase block">{factor.type} • {factor.algorithm}</span>
                      </div>
                      
                      <div className="flex items-center gap-2">
                        {isSuspended ? (
                          <span className="text-[10px] text-amber-500 font-mono uppercase font-bold">Suspended</span>
                        ) : (
                          <>
                            <span className="text-lg font-bold font-mono tracking-wider text-emerald-400">
                              {currentCode}
                            </span>
                            <button
                              onClick={() => handleAutofill(currentCode)}
                              title="Auto-fill this code into the active challenge screen"
                              className="p-1.5 bg-slate-800 hover:bg-slate-700 rounded text-slate-300 hover:text-white transition-colors"
                            >
                              <Check className="w-3 h-3" />
                            </button>
                          </>
                        )}
                      </div>
                    </div>
                  );
                })}

                {/* Simulated Pending Factor Reveal */}
                {enrollmentFactor && currentView.startsWith("ENROLL") && (
                  <div className="p-3 bg-indigo-950/40 rounded-lg border border-indigo-900/50">
                    <div className="flex justify-between items-center mb-1">
                      <span className="text-xs font-semibold text-indigo-200">Pending Setup App</span>
                      <span className="text-[9px] text-indigo-400 font-mono uppercase">Setup Mode</span>
                    </div>
                    {enrollmentSecretRevealed ? (
                      <div className="flex justify-between items-center mt-2">
                        <span className="text-xs font-mono text-slate-400 font-semibold truncate max-w-[120px]">{enrollmentFactor.secret}</span>
                        <div className="flex items-center gap-1.5">
                          <span className="text-lg font-bold font-mono text-indigo-300">{getSimulatedTotpCode(enrollmentFactor)}</span>
                          <button
                            onClick={() => handleAutofill(getSimulatedTotpCode(enrollmentFactor))}
                            className="p-1 bg-indigo-800 text-white rounded hover:bg-indigo-700"
                          >
                            <Check className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    ) : (
                      <span className="text-[10px] text-slate-400 italic">Awaiting seed reveal...</span>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Clock Drift & Network Posture Simulation Controls */}
          <div>
            <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest flex items-center gap-1.5 mb-3">
              <Sliders className="w-4 h-4 text-slate-400" />
              <span>Simulation Injectors</span>
            </h2>

            <div className="bg-slate-50 border border-slate-200/80 rounded-xl p-4 space-y-3.5 text-xs text-slate-600">
              
              {/* Clock Skew Control */}
              <div>
                <label className="block font-medium text-slate-700 mb-1">Simulate Clock Skew (Drift)</label>
                <div className="flex items-center gap-2">
                  <button 
                    onClick={() => setSimulation(p => ({ ...p, currentTimeSkewSeconds: p.currentTimeSkewSeconds - 30 }))}
                    className="flex-1 py-1 px-2 bg-white border border-slate-200 hover:bg-slate-50 rounded font-mono text-[10px] text-slate-700"
                  >
                    -30s
                  </button>
                  <span className="text-[11px] font-bold font-mono text-slate-800 bg-slate-200/60 px-2 py-0.5 rounded min-w-[50px] text-center">
                    {simulation.currentTimeSkewSeconds}s
                  </span>
                  <button 
                    onClick={() => setSimulation(p => ({ ...p, currentTimeSkewSeconds: p.currentTimeSkewSeconds + 30 }))}
                    className="flex-1 py-1 px-2 bg-white border border-slate-200 hover:bg-slate-50 rounded font-mono text-[10px] text-slate-700"
                  >
                    +30s
                  </button>
                </div>
                <p className="text-[9px] text-slate-400 mt-1">Simulates desynchronized user device clocks.</p>
              </div>

              {/* Replay attack injector */}
              <label className="flex items-center gap-2.5 cursor-pointer select-none">
                <input 
                  type="checkbox" 
                  checked={simulation.simulateReplayAttack}
                  onChange={(e) => setSimulation(p => ({ ...p, simulateReplayAttack: e.target.checked }))}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <div>
                  <span className="font-semibold block text-slate-700">Simulate Replay Attack</span>
                  <span className="text-[9px] text-slate-400 block">Force submit a token already stored in replay database.</span>
                </div>
              </label>

              {/* Database network outage injector */}
              <label className="flex items-center gap-2.5 cursor-pointer select-none">
                <input 
                  type="checkbox" 
                  checked={simulation.simulateStorageFailure}
                  onChange={(e) => setSimulation(p => ({ ...p, simulateStorageFailure: e.target.checked }))}
                  className="rounded text-indigo-600 focus:ring-indigo-500"
                />
                <div>
                  <span className="font-semibold block text-slate-700">Simulate Storage Outage</span>
                  <span className="text-[9px] text-slate-400 block">Disconnect database lookup during verification.</span>
                </div>
              </label>

              <div className="pt-2 border-t border-slate-200">
                <button 
                  onClick={handleAdminResetAll}
                  className="w-full py-2 bg-red-50 hover:bg-red-100 text-red-700 border border-red-200 rounded-lg text-xs font-semibold transition-colors flex items-center justify-center gap-1.5"
                >
                  <Trash2 className="w-3.5 h-3.5" />
                  <span>Administrative System Reset</span>
                </button>
              </div>
            </div>
          </div>

        </aside>

        {/* ================= CENTER WORKSPACE PANEL: INTERACTIVE CEREMONIES ================= */}
        <main className="flex-1 p-6 lg:p-8 flex items-center justify-center overflow-y-auto">
          <div className="w-full max-w-md bg-white rounded-2xl shadow-xl shadow-slate-200/60 border border-slate-200 p-8 relative overflow-hidden transition-all duration-300">
            
            {/* Context Badge in Card corner */}
            <div className="absolute top-4 right-4 flex items-center gap-1 bg-slate-50 border border-slate-100 px-2.5 py-1 rounded text-[10px] font-mono text-slate-400">
              <span className="w-1.5 h-1.5 bg-indigo-500 rounded-full animate-pulse"></span>
              <span>CEREMONY_STATE: {currentView}</span>
            </div>

            {/* --- SCREEN 1: LOGIN --- */}
            {currentView === "LOGIN" && (
              <div className="py-2">
                <div className="mb-6 text-center">
                  <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center mx-auto mb-3 border border-indigo-100">
                    <Lock className="w-5 h-5 text-indigo-600" />
                  </div>
                  <h1 className="text-xl font-bold font-display text-slate-900">Sign in to Enterprise</h1>
                  <p className="text-slate-500 text-xs mt-1">Please initiate authentication to verify security policy possession factors.</p>
                </div>

                <div className="space-y-3 mb-5">
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Identity Principal</label>
                    <input 
                      type="text" 
                      disabled 
                      value="j.austin@enterprise.com" 
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs font-mono text-slate-500" 
                    />
                  </div>
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Password Credential</label>
                    <input 
                      type="password" 
                      disabled 
                      value="••••••••••••••••" 
                      className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-xs text-slate-500" 
                    />
                  </div>
                </div>

                <button 
                  onClick={startLoginFlow}
                  className="w-full py-3 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition-colors flex items-center justify-center gap-1.5"
                >
                  <span>Authenticate Session</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </button>
                
                <div className="mt-5 text-center">
                  <button 
                    onClick={() => setCurrentView("PROFILE")}
                    className="text-xs text-indigo-600 font-medium hover:underline inline-flex items-center gap-1"
                  >
                    <Settings className="w-3.5 h-3.5" />
                    <span>Go to Authenticator Setup Direct</span>
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 2: METHOD CHOOSER --- */}
            {currentView === "MFA_CHOOSER" && (
              <div>
                <div className="mb-5">
                  <h1 className="text-lg font-bold text-slate-900 font-display">Multiple Factors Configured</h1>
                  <p className="text-slate-500 text-xs mt-1">Select an active possession factor to verify identity assertion.</p>
                </div>

                <div className="space-y-2.5 mb-5">
                  {authenticators.filter(f => f.status === FactorStatus.ACTIVE).map(factor => (
                    <button
                      key={factor.id}
                      onClick={() => selectMfaFactor(factor)}
                      className="w-full p-3 border border-slate-200 hover:border-indigo-500 hover:bg-indigo-50/10 rounded-xl flex items-center justify-between text-left transition-colors"
                    >
                      <div className="flex items-center gap-3">
                        <div className="p-2 bg-slate-100 rounded-lg text-slate-600">
                          {factor.type === "totp" ? (
                            <Smartphone className="w-4 h-4 text-indigo-600" />
                          ) : (
                            <KeyRound className="w-4 h-4 text-indigo-600" />
                          )}
                        </div>
                        <div>
                          <p className="font-semibold text-xs text-slate-900">{factor.label}</p>
                          <p className="text-[10px] text-slate-400 font-mono">
                            {factor.type === "totp" 
                              ? `Authenticator App • ${factor.digits} Digits` 
                              : `Delivered • ${factor.deliveryTarget}`}
                          </p>
                        </div>
                      </div>
                      <ArrowRight className="w-3.5 h-3.5 text-slate-400" />
                    </button>
                  ))}
                </div>

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("LOGIN")}
                    className="flex-1 py-2 border border-slate-200 hover:bg-slate-50 rounded-lg text-xs font-semibold text-slate-600"
                  >
                    Back
                  </button>
                  <button 
                    onClick={startRecoveryReset}
                    className="flex-1 py-2 text-indigo-600 hover:underline text-xs font-semibold"
                  >
                    Use Recovery Key
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 3: CHALLENGE PAGE --- */}
            {currentView === "MFA_CHALLENGE" && activeFactor && (
              <div>
                <div className="mb-5">
                  <h1 className="text-lg font-bold text-slate-900 font-display">Authenticator Challenge</h1>
                  <p className="text-slate-500 text-xs mt-1">
                    Enter the code displayed in your <span className="font-semibold text-slate-800">{activeFactor.label}</span>.
                  </p>
                </div>

                {/* Secure segment input boxes */}
                <div className="flex justify-center gap-2 mb-5">
                  {new Array(activeFactor.digits).fill("").map((_, i) => (
                    <input
                      key={i}
                      ref={el => { inputRefs.current[i] = el; }}
                      type="text"
                      maxLength={1}
                      pattern="\d*"
                      value={challengeCode[i] || ""}
                      onChange={(e) => handleInputChange(e.target.value, i, activeFactor.digits, "challenge")}
                      onKeyDown={(e) => handleKeyDown(e, i, "challenge")}
                      onPaste={(e) => handlePaste(e, "challenge")}
                      className={`w-11 h-12 text-center text-lg font-bold rounded-lg border-2 transition-all font-mono focus:outline-none focus:ring-0 ${
                        challengeState === "invalid" || challengeState === "replayed" || challengeState === "rate_limited"
                          ? "border-red-400 bg-red-50/20 text-red-950"
                          : challengeState === "success"
                          ? "border-emerald-400 bg-emerald-50/20 text-emerald-950"
                          : "border-slate-200 focus:border-indigo-600 bg-slate-50/30"
                      }`}
                    />
                  ))}
                </div>

                {/* Verification results / messages */}
                {challengeError && (
                  <div className="mb-4 p-3 bg-red-50 border border-red-100 rounded-xl flex items-start gap-2 text-xs text-red-800">
                    <AlertTriangle className="w-4 h-4 text-red-600 flex-shrink-0 mt-0.5" />
                    <div>
                      <span className="font-bold block">Ceremony Lock</span>
                      <span>{challengeError}</span>
                    </div>
                  </div>
                )}

                {/* Submit actions */}
                <div className="space-y-3">
                  <button
                    onClick={submitChallengeCode}
                    disabled={challengeState === "submitting" || challengeState === "rate_limited"}
                    className="w-full py-3 bg-slate-900 text-white rounded-xl text-xs font-semibold hover:bg-slate-800 transition-colors disabled:bg-slate-400 disabled:cursor-not-allowed"
                  >
                    {challengeState === "submitting" ? (
                      <div className="flex items-center justify-center gap-1.5">
                        <RotateCw className="w-3.5 h-3.5 animate-spin" />
                        <span>Verifying...</span>
                      </div>
                    ) : (
                      <span>Verify Possession Code</span>
                    )}
                  </button>

                  <div className="flex items-center justify-between pt-1.5">
                    {activeFactor.type !== "totp" ? (
                      <button 
                        onClick={triggerResendCode}
                        className="text-xs font-semibold text-indigo-600 hover:underline flex items-center gap-1"
                      >
                        <RefreshCw className="w-3 h-3" />
                        <span>Resend Delivered OTP</span>
                      </button>
                    ) : (
                      <div className="flex items-center gap-1 text-[11px] text-slate-400 font-mono">
                        <Clock className="w-3.5 h-3.5 text-slate-400" />
                        <span>Code expires in {challengeCountdown} seconds</span>
                      </div>
                    )}

                    <button
                      onClick={() => setCurrentView("MFA_CHOOSER")}
                      className="text-xs font-medium text-slate-500 hover:text-slate-800 hover:underline"
                    >
                      Try another way
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* --- SCREEN 4: STEP-UP CHALLENGE --- */}
            {currentView === "STEP_UP" && activeFactor && (
              <div>
                <div className="p-3.5 bg-amber-50 border border-amber-100 rounded-xl mb-4 flex items-start gap-2 text-xs">
                  <Lock className="w-4 h-4 text-amber-700 flex-shrink-0 mt-0.5" />
                  <div>
                    <h2 className="font-bold text-amber-800">Sensitive Action Step-Up required</h2>
                    <p className="text-amber-700 font-mono mt-0.5">{activeStepUpText}</p>
                  </div>
                </div>

                <div className="mb-5">
                  <p className="text-xs text-slate-500">
                    Prove possession of <span className="font-semibold text-slate-800">{activeFactor.label}</span> before confirming transaction ceremony.
                  </p>
                </div>

                {/* Input Segment */}
                <div className="flex justify-center gap-2 mb-5">
                  {new Array(activeFactor.digits).fill("").map((_, i) => (
                    <input
                      key={i}
                      ref={el => { inputRefs.current[i] = el; }}
                      type="text"
                      maxLength={1}
                      pattern="\d*"
                      value={challengeCode[i] || ""}
                      onChange={(e) => handleInputChange(e.target.value, i, activeFactor.digits, "challenge")}
                      onKeyDown={(e) => handleKeyDown(e, i, "challenge")}
                      className="w-11 h-12 text-center text-lg font-bold rounded-lg border-2 border-slate-200 font-mono focus:border-indigo-600 focus:outline-none"
                    />
                  ))}
                </div>

                {challengeError && (
                  <p className="text-xs text-red-600 font-medium text-center mb-4">{challengeError}</p>
                )}

                <div className="space-y-2">
                  <button
                    onClick={submitStepUpCode}
                    disabled={challengeState === "submitting"}
                    className="w-full py-2.5 bg-slate-900 text-white hover:bg-slate-800 font-semibold text-xs rounded-xl transition-all"
                  >
                    {challengeState === "submitting" ? "Authorizing..." : "Approve Ceremony Action"}
                  </button>
                  <button
                    onClick={() => setCurrentView("PROFILE")}
                    className="w-full py-2.5 border border-slate-200 rounded-xl text-[11px] font-semibold text-slate-500 hover:bg-slate-50"
                  >
                    Cancel Ceremony
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 5: SUCCESS & EVIDENCE ASSERTION --- */}
            {currentView === "SUCCESS" && (
              <div className="text-center py-4">
                <div className="w-12 h-12 bg-emerald-50 rounded-full flex items-center justify-center mx-auto mb-3 border border-emerald-100">
                  <Check className="w-6 h-6 text-emerald-600" />
                </div>
                
                <h1 className="text-xl font-bold font-display text-slate-900">Ceremony Approved</h1>
                <p className="text-slate-500 text-xs mt-1">Possession factor validated. Cryptographic evidence token generated.</p>

                {/* Assertion payload box */}
                <div className="mt-5 p-4.5 bg-slate-50 border border-slate-200 rounded-xl text-left shadow-sm">
                  <h3 className="text-[10px] font-bold text-slate-600 uppercase tracking-widest mb-3.5 flex items-center gap-1.5">
                    <FileCode className="w-4 h-4 text-indigo-600" />
                    <span>Cryptographic Evidence Asserted</span>
                  </h3>
                  
                  <div className="space-y-2 font-mono text-[11px]">
                    <div className="flex justify-between border-b border-slate-200/60 pb-1">
                      <span className="text-slate-400">AMR Class:</span>
                      <span className="font-semibold text-indigo-700 bg-indigo-50 px-1.5 rounded text-[10px]">otp</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-200/60 pb-1">
                      <span className="text-slate-400">Verified ID:</span>
                      <span className="font-semibold text-slate-700 truncate max-w-[150px]">{activeFactor?.id}</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-200/60 pb-1">
                      <span className="text-slate-400">Factor Type:</span>
                      <span className="font-semibold text-slate-700">{activeFactor?.type} / {activeFactor?.algorithm}</span>
                    </div>
                    <div className="flex justify-between border-b border-slate-200/60 pb-1">
                      <span className="text-slate-400">Nonce:</span>
                      <span className="font-semibold text-slate-700">{Math.floor(Math.random() * 900000 + 100000)}</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block mb-1">Signed AMR Evidence:</span>
                      <div className="p-2 bg-slate-900 text-emerald-400 rounded-lg text-[9px] break-all leading-normal">
                        {`{"amr":["otp"],"iss":"tigrbl-auth","subject":"j.austin@enterprise.com","verified":true,"epoch":${Math.floor(Date.now() / 1000)}}`}
                      </div>
                    </div>
                  </div>
                </div>

                <div className="mt-5 flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("PROFILE")}
                    className="flex-1 py-2.5 bg-slate-900 hover:bg-slate-800 text-white rounded-xl text-xs font-semibold"
                  >
                    Manage Factors
                  </button>
                  <button 
                    onClick={() => setCurrentView("LOGIN")}
                    className="flex-1 py-2.5 border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-xl text-xs font-semibold"
                  >
                    Sign In Again
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 6: ENROLL INTRO --- */}
            {currentView === "ENROLL_INTRO" && (
              <div>
                <div className="mb-4 text-center">
                  <div className="w-12 h-12 bg-indigo-50 rounded-xl flex items-center justify-center mx-auto mb-3 border border-indigo-100">
                    <Smartphone className="w-6 h-6 text-indigo-600" />
                  </div>
                  <h1 className="text-lg font-bold text-slate-900 font-display">Enroll Authenticator App</h1>
                  <p className="text-slate-500 text-xs mt-1">Secure first-party possession credentials on your device.</p>
                </div>

                <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 mb-5 space-y-3 text-xs text-slate-600">
                  <div className="flex gap-2.5">
                    <CheckCircle className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
                    <span>Uses standard TOTP compatible with Google Authenticator, YubiKey, or Microsoft Authenticator.</span>
                  </div>
                  <div className="flex gap-2.5">
                    <CheckCircle className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
                    <span>Generates verification codes locally on your secure enclave. No network required.</span>
                  </div>
                  <div className="flex gap-2.5">
                    <CheckCircle className="w-4 h-4 text-indigo-600 flex-shrink-0 mt-0.5" />
                    <span>Protected against interception attacks common with traditional SMS delivery.</span>
                  </div>
                </div>

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("PROFILE")}
                    className="flex-1 py-2.5 border border-slate-200 hover:bg-slate-50 text-slate-600 rounded-lg text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button 
                    onClick={() => setCurrentView("ENROLL_REVEAL")}
                    className="flex-1 py-2.5 bg-slate-900 text-white hover:bg-slate-800 rounded-lg text-xs font-semibold"
                  >
                    Begin Setup
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 7: ENROLL REVEAL (SEED/QR) --- */}
            {currentView === "ENROLL_REVEAL" && enrollmentFactor && (
              <div>
                <div className="mb-4">
                  <h1 className="text-base font-bold text-slate-900 font-display">Scan QR or Copy Key</h1>
                  <p className="text-slate-500 text-xs mt-1">Configure your authenticator application with this single-use credential seed.</p>
                </div>

                {/* Secret reveal visual shield */}
                <div className="border border-slate-200 rounded-xl p-4 bg-slate-50/50 mb-5 relative flex flex-col items-center">
                  {enrollmentSecretRevealed ? (
                    <div className="w-full flex flex-col items-center space-y-3">
                      {/* Interactive mock QR Code */}
                      <div className="w-28 h-28 bg-white border border-slate-200 p-2 rounded flex items-center justify-center">
                        <svg viewBox="0 0 100 100" className="w-full h-full text-slate-900">
                          <rect width="20" height="20" x="5" y="5" />
                          <rect width="20" height="20" x="75" y="5" />
                          <rect width="20" height="20" x="5" y="75" />
                          <rect width="10" height="10" x="35" y="35" />
                          <rect width="10" height="10" x="55" y="45" />
                          <rect width="10" height="10" x="45" y="65" />
                          <rect width="10" height="10" x="75" y="75" />
                          <rect width="15" height="15" x="20" y="5" />
                        </svg>
                      </div>

                      <div className="w-full text-center">
                        <span className="block text-[10px] text-slate-400 font-bold uppercase tracking-wider mb-1">Secret seed (Base32)</span>
                        <div className="flex items-center justify-center gap-1.5 bg-white border border-slate-200 px-3 py-1.5 rounded font-mono text-xs select-all">
                          <span className="font-bold text-slate-800">{enrollmentFactor.secret}</span>
                          <button 
                            onClick={() => {
                              navigator.clipboard.writeText(enrollmentFactor.secret);
                              triggerToast("Base32 secret key copied!", "success");
                            }}
                            className="p-1 hover:bg-slate-100 rounded text-slate-500"
                          >
                            <Copy className="w-3 h-3" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ) : (
                    <div className="py-6 text-center">
                      <div className="w-11 h-11 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto mb-3">
                        <Lock className="w-5 h-5" />
                      </div>
                      <span className="text-xs text-slate-500 font-medium block max-w-xs mx-auto mb-3">
                        Seeds are sensitive and only revealed once. Do not share, print, or screen share during setup.
                      </span>
                      <button
                        onClick={handleRevealSecret}
                        className="py-1.5 px-3 bg-indigo-600 text-white rounded-lg text-xs font-semibold hover:bg-indigo-500"
                      >
                        Reveal Secret Key & QR Code
                      </button>
                    </div>
                  )}
                </div>

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("PROFILE")}
                    className="flex-1 py-2.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold"
                  >
                    Cancel
                  </button>
                  <button 
                    disabled={!enrollmentSecretRevealed}
                    onClick={() => setCurrentView("ENROLL_VERIFY")}
                    className="flex-1 py-2.5 bg-slate-900 text-white hover:bg-slate-800 rounded-lg text-xs font-semibold disabled:bg-slate-200 disabled:cursor-not-allowed"
                  >
                    Next Proof
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 8: ENROLL VERIFY --- */}
            {currentView === "ENROLL_VERIFY" && enrollmentFactor && (
              <div>
                <div className="mb-4">
                  <h1 className="text-base font-bold text-slate-900 font-display">Verify Code Setup</h1>
                  <p className="text-slate-500 text-xs mt-1">Prove setup was successful by entering the current code displayed in your authenticator app.</p>
                </div>

                <div className="flex justify-center gap-2 mb-5">
                  {new Array(enrollmentFactor.digits).fill("").map((_, i) => (
                    <input
                      key={i}
                      ref={el => { inputRefs.current[i] = el; }}
                      type="text"
                      maxLength={1}
                      pattern="\d*"
                      value={enrollmentVerifyCode[i] || ""}
                      onChange={(e) => handleInputChange(e.target.value, i, enrollmentFactor.digits, "enroll")}
                      onKeyDown={(e) => handleKeyDown(e, i, "enroll")}
                      onPaste={(e) => handlePaste(e, "enroll")}
                      className={`w-11 h-12 text-center text-lg font-bold rounded-lg border-2 transition-all font-mono focus:outline-none focus:ring-0 ${
                        enrollmentError ? "border-red-400 bg-red-50/20" : "border-slate-200 focus:border-indigo-600"
                      }`}
                    />
                  ))}
                </div>

                {enrollmentError && (
                  <p className="text-xs text-red-600 font-medium mb-4">{enrollmentError}</p>
                )}

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("ENROLL_REVEAL")}
                    className="flex-1 py-2.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold"
                  >
                    Back to Key
                  </button>
                  <button 
                    onClick={verifyInitialEnrollmentCode}
                    className="flex-1 py-2.5 bg-slate-900 text-white hover:bg-slate-800 rounded-lg text-xs font-semibold"
                  >
                    Verify Setup
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 9: ENROLL NAME --- */}
            {currentView === "ENROLL_NAME" && (
              <div>
                <div className="mb-4">
                  <h1 className="text-base font-bold text-slate-900 font-display font-medium">Name Authenticator</h1>
                  <p className="text-slate-500 text-xs mt-1">Assign a safe, descriptive label to help recognize this factor.</p>
                </div>

                <div className="space-y-4 mb-5">
                  <div>
                    <label className="block text-[10px] font-bold uppercase tracking-wider text-slate-400 mb-1">Device Label</label>
                    <input 
                      type="text" 
                      placeholder="e.g. Work iPhone 15, Backup Key" 
                      value={enrollmentLabel}
                      onChange={(e) => setEnrollmentLabel(e.target.value)}
                      className="w-full bg-white border border-slate-200 rounded-lg px-3 py-2 text-xs font-medium text-slate-800 focus:border-indigo-600 focus:outline-none"
                    />
                  </div>
                </div>

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("ENROLL_VERIFY")}
                    className="flex-1 py-2.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold"
                  >
                    Back
                  </button>
                  <button 
                    onClick={saveAuthenticatorName}
                    className="flex-1 py-2.5 bg-slate-900 text-white hover:bg-slate-800 rounded-lg text-xs font-semibold"
                  >
                    Save & Next
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 10: ENROLL RECOVERY --- */}
            {currentView === "ENROLL_RECOVERY" && (
              <div>
                <div className="mb-3">
                  <h1 className="text-base font-bold text-slate-900 font-display">Recovery backup key</h1>
                  <p className="text-slate-500 text-xs mt-1">If you lose your authenticator, this code can unlock your account.</p>
                </div>

                <div className="p-3 bg-amber-50 border border-amber-100 rounded-xl mb-4 text-xs space-y-3 text-slate-700">
                  <div className="grid grid-cols-2 gap-2 font-mono text-[10px] text-center font-bold">
                    {recoveryCodes.slice(0, 4).map((c, idx) => (
                      <div key={idx} className="bg-white border border-amber-100 p-1.5 rounded">{c}</div>
                    ))}
                  </div>

                  <label className="flex items-start gap-2 cursor-pointer select-none">
                    <input 
                      type="checkbox" 
                      checked={recoveryConfirmed}
                      onChange={(e) => setRecoveryConfirmed(e.target.checked)}
                      className="rounded text-indigo-600 focus:ring-indigo-500 mt-0.5"
                    />
                    <span className="text-[10px] font-medium leading-normal text-slate-600">
                      I have written down the backup recovery keys. I understand that help desk support cannot retrieve forgotten seeds.
                    </span>
                  </label>
                </div>

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("ENROLL_NAME")}
                    className="flex-1 py-2.5 border border-slate-200 text-slate-600 rounded-lg text-xs font-semibold"
                  >
                    Back
                  </button>
                  <button 
                    disabled={!recoveryConfirmed}
                    onClick={activateAuthenticatorFactor}
                    className="flex-1 py-2.5 bg-slate-900 text-white hover:bg-slate-800 rounded-lg text-xs font-semibold disabled:bg-slate-200 disabled:cursor-not-allowed"
                  >
                    Activate Factor
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 11: ENROLL COMPLETED --- */}
            {currentView === "ENROLL_COMPLETED" && (
              <div className="text-center py-4">
                <div className="w-11 h-11 bg-neutral-50 rounded-full flex items-center justify-center mx-auto mb-3.5 border border-neutral-200/60">
                  <CheckCircle className="w-5 h-5 text-neutral-800" />
                </div>
                
                <h1 className="text-base font-bold font-display text-neutral-900 tracking-tight">Activation Completed</h1>
                <p className="text-neutral-500 text-xs mt-1">Your new OTP possession factor is fully active and registered in the trust enclave.</p>

                <div className="mt-5 p-4 bg-neutral-50 border border-neutral-200/50 rounded-lg text-left text-xs space-y-1.5 shadow-sm">
                  <div className="flex justify-between">
                    <span className="text-neutral-400">Factor Label:</span>
                    <span className="font-semibold text-neutral-800">{enrollmentFactor?.label}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-neutral-400">Class:</span>
                    <span className="font-mono text-neutral-800 text-[11px]">TOTP (Possession)</span>
                  </div>
                </div>

                <button 
                  onClick={() => setCurrentView("PROFILE")}
                  className="w-full mt-5 py-2 bg-neutral-900 text-white hover:bg-neutral-950 rounded-lg text-xs font-semibold transition-colors shadow-sm"
                >
                  Return to Dashboard
                </button>
              </div>
            )}

            {/* --- SCREEN 12: RECOVERY RESET --- */}
            {currentView === "RECOVERY_RESET" && (
              <div>
                <div className="mb-4">
                  <h1 className="text-base font-bold text-neutral-900 font-display tracking-tight">Account Recovery</h1>
                  <p className="text-neutral-500 text-xs mt-1">Enter your backup recovery key to authenticate and reset failed attempts posture.</p>
                </div>

                <div className="flex justify-center gap-1.5 mb-5 font-mono">
                  {new Array(6).fill("").map((_, i) => (
                    <input
                      key={i}
                      ref={el => { inputRefs.current[i] = el; }}
                      type="text"
                      maxLength={1}
                      value={challengeCode[i] || ""}
                      onChange={(e) => {
                        const val = e.target.value.replace(/[^a-zA-Z0-9]/g, "");
                        const arr = [...challengeCode];
                        arr[i] = val.slice(-1);
                        setChallengeCode(arr);
                        if (val && i < 5) inputRefs.current[i + 1]?.focus();
                      }}
                      onKeyDown={(e) => {
                        if (e.key === "Backspace" && !challengeCode[i] && i > 0) {
                          inputRefs.current[i - 1]?.focus();
                        }
                      }}
                      className="w-11 h-12 text-center text-lg font-bold border-2 border-neutral-200 rounded-lg focus:border-neutral-900 focus:outline-none focus:ring-0 bg-neutral-50/30"
                    />
                  ))}
                </div>

                {challengeError && (
                  <p className="text-xs text-red-600 font-medium mb-4 text-center">{challengeError}</p>
                )}

                <div className="flex gap-2.5">
                  <button 
                    onClick={() => setCurrentView("MFA_CHOOSER")}
                    className="flex-1 py-2 border border-neutral-200 text-neutral-600 rounded-lg text-xs font-semibold transition-colors"
                  >
                    Back
                  </button>
                  <button 
                    onClick={submitRecoveryReset}
                    className="flex-1 py-2 bg-neutral-900 text-white hover:bg-neutral-950 rounded-lg text-xs font-semibold transition-colors shadow-sm"
                  >
                    Authenticate Reset
                  </button>
                </div>
              </div>
            )}

            {/* --- SCREEN 13: FACTOR MANAGEMENT DASHBOARD OVERVIEW --- */}
            {currentView === "PROFILE" && (
              <div>
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <h1 className="text-base font-bold text-neutral-900 font-display tracking-tight">Registered Credentials</h1>
                    <p className="text-neutral-500 text-xs mt-0.5">Enrolled possession verification devices.</p>
                  </div>
                  <button
                    onClick={initiateEnrollment}
                    className="py-1.5 px-3 bg-neutral-900 text-white rounded-lg hover:bg-neutral-950 flex items-center justify-center gap-1 text-[11px] font-semibold transition-colors shadow-sm"
                  >
                    <Plus className="w-3.5 h-3.5" />
                    <span>Enroll</span>
                  </button>
                </div>

                <div className="space-y-3 mb-5 max-h-64 overflow-y-auto pr-1">
                  {authenticators.map(factor => (
                    <div 
                      key={factor.id} 
                      className={`p-3.5 rounded-lg border transition-all ${
                        factor.status === FactorStatus.ACTIVE 
                          ? "border-neutral-200 bg-white" 
                          : "border-neutral-200/50 bg-neutral-50/50 opacity-80"
                      }`}
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex items-start gap-3">
                          <div className="p-2 bg-neutral-50 border border-neutral-100 rounded-md text-neutral-800 mt-0.5">
                            {factor.type === "totp" ? (
                              <Smartphone className="w-4 h-4 text-neutral-800" />
                            ) : (
                              <KeyRound className="w-4 h-4 text-neutral-800" />
                            )}
                          </div>
                          <div>
                            <div className="flex items-center gap-1.5">
                              <h3 className="font-semibold text-xs text-neutral-900">{factor.label}</h3>
                              <span className={`text-[8px] px-1.5 py-0.5 rounded font-mono uppercase font-bold tracking-wider ${
                                factor.status === FactorStatus.ACTIVE 
                                  ? "bg-neutral-100 border border-neutral-200/50 text-neutral-800" 
                                  : "bg-amber-50 border border-amber-100 text-amber-800"
                              }`}>
                                {factor.status}
                              </span>
                            </div>
                            <p className="text-[10px] text-neutral-400 font-mono mt-0.5">
                              ID: {factor.id} • Enrolled: {new Date(factor.created).toLocaleDateString()}
                            </p>
                          </div>
                        </div>

                        <div className="flex gap-1">
                          {factor.status === FactorStatus.ACTIVE ? (
                            <button
                              onClick={() => toggleFactorStatus(factor.id, FactorStatus.SUSPENDED)}
                              title="Suspend factor temporarily"
                              className="p-1.5 hover:bg-amber-50 text-neutral-400 hover:text-amber-700 rounded transition-colors"
                            >
                              <Power className="w-3.5 h-3.5" />
                            </button>
                          ) : (
                            <button
                              onClick={() => toggleFactorStatus(factor.id, FactorStatus.ACTIVE)}
                              title="Activate factor"
                              className="p-1.5 hover:bg-neutral-50 text-neutral-400 hover:text-neutral-900 rounded transition-colors"
                            >
                              <Check className="w-3.5 h-3.5" />
                            </button>
                          )}
                          <button
                            onClick={() => removeFactor(factor.id)}
                            title="Revoke and remove factor"
                            className="p-1.5 hover:bg-red-50 text-neutral-400 hover:text-red-700 rounded transition-colors"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>

                <div className="pt-3 border-t border-neutral-100 space-y-2.5">
                  <button 
                    onClick={triggerStepUp}
                    className="w-full py-2 bg-neutral-50 hover:bg-neutral-100/80 border border-neutral-200/40 text-neutral-800 rounded-lg text-xs font-semibold flex items-center justify-center gap-1.5 transition-colors"
                  >
                    <Lock className="w-3.5 h-3.5 text-neutral-700" />
                    <span>Test Sensitive Action Ceremony (Step-Up)</span>
                  </button>

                  <button 
                    onClick={() => setCurrentView("LOGIN")}
                    className="w-full py-2 border border-neutral-200 hover:bg-neutral-50 text-neutral-600 rounded-lg text-xs font-semibold transition-colors"
                  >
                    Logout Session
                  </button>
                </div>
              </div>
            )}

          </div>
        </main>

        {/* ================= RIGHT SIDE PANEL: AUDIT HISTORY & TENANT POLICIES ================= */}
        <aside className="w-full lg:w-96 border-l border-neutral-200 bg-neutral-50/40 p-6 flex flex-col overflow-y-auto space-y-6">
          
          {/* Tenant OTP Policies Settings */}
          <div>
            <h2 className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest flex items-center gap-1.5 mb-3">
              <Sliders className="w-3.5 h-3.5 text-neutral-400" />
              <span>Tenant Security Policy</span>
            </h2>

            <div className="p-4 bg-white rounded-lg border border-neutral-200/60 text-xs space-y-4 shadow-sm">
              
              {/* Algorithm */}
              <div>
                <label className="block text-neutral-500 mb-1.5 font-medium">Cryptographic Algorithm</label>
                <select
                  value={policy.allowedAlgorithms[0]}
                  onChange={(e) => setPolicy(p => ({ ...p, allowedAlgorithms: [e.target.value as OtpAlgorithm] }))}
                  className="w-full bg-white border border-neutral-200 rounded-lg px-2.5 py-1.5 text-neutral-800 font-mono text-[11px] focus:border-neutral-900 focus:outline-none focus:ring-0"
                >
                  <option value={OtpAlgorithm.SHA1}>HMAC-SHA1 (Default compatible)</option>
                  <option value={OtpAlgorithm.SHA256}>HMAC-SHA256 (High Security)</option>
                  <option value={OtpAlgorithm.SHA512}>HMAC-SHA512 (Enclave Bound)</option>
                </select>
              </div>

              {/* Digits length */}
              <div>
                <label className="block text-neutral-500 mb-1.5 font-medium">OTP Digit Complexity</label>
                <div className="flex gap-2">
                  {[6, 8].map(num => (
                    <button
                      key={num}
                      onClick={() => setPolicy(p => ({ ...p, allowedDigits: [num] }))}
                      className={`flex-1 py-1.5 rounded-lg text-[11px] font-semibold border transition-all ${
                        policy.allowedDigits[0] === num 
                          ? "bg-neutral-900 border-neutral-900 text-white shadow-sm" 
                          : "bg-white border-neutral-200 text-neutral-600 hover:bg-neutral-50"
                      }`}
                    >
                      {num} Digits
                    </button>
                  ))}
                </div>
              </div>

              {/* Step Interval period */}
              <div>
                <label className="block text-neutral-500 mb-1.5 font-medium">Drift Window Step Interval</label>
                <div className="flex gap-2">
                  {[30, 60].map(p => (
                    <button
                      key={p}
                      onClick={() => setPolicy(policyPrev => ({ ...policyPrev, allowedPeriods: [p] }))}
                      className={`flex-1 py-1.5 rounded-lg text-[11px] font-semibold border transition-all ${
                        policy.allowedPeriods[0] === p 
                          ? "bg-neutral-900 border-neutral-900 text-white shadow-sm" 
                          : "bg-white border-neutral-200 text-neutral-600 hover:bg-neutral-50"
                      }`}
                    >
                      {p} Seconds
                    </button>
                  ))}
                </div>
              </div>

              {/* Attempts Lock Limit */}
              <div className="flex justify-between items-center text-neutral-500 font-medium">
                <span>Brute Force Lock Limit</span>
                <input 
                  type="number" 
                  min={3} 
                  max={10} 
                  value={policy.attemptsLimit}
                  onChange={(e) => setPolicy(p => ({ ...p, attemptsLimit: parseInt(e.target.value) || 5 }))}
                  className="w-12 bg-white border border-neutral-200 rounded-lg px-1.5 py-1 text-center text-neutral-800 font-bold font-mono focus:border-neutral-900 focus:outline-none focus:ring-0"
                />
              </div>

              {/* Force MFA */}
              <label className="flex items-center justify-between cursor-pointer text-neutral-500 font-medium">
                <span>Force Global MFA</span>
                <input 
                  type="checkbox" 
                  checked={policy.forceMfa}
                  onChange={(e) => setPolicy(p => ({ ...p, forceMfa: e.target.checked }))}
                  className="rounded text-neutral-900 focus:ring-neutral-900 border-neutral-300 w-4 h-4"
                />
              </label>

            </div>
          </div>

          {/* Security Audit Trail */}
          <div className="flex-1 flex flex-col min-h-0">
            <h2 className="text-[10px] font-bold text-neutral-400 uppercase tracking-widest flex items-center gap-1.5 mb-3">
              <History className="w-3.5 h-3.5 text-neutral-400" />
              <span>Identity Audit Trail</span>
            </h2>

            <div className="flex-1 bg-white border border-neutral-200/50 rounded-lg p-4 overflow-y-auto space-y-3 font-mono text-[9px] shadow-sm max-h-[250px] lg:max-h-none">
              {auditLogs.map(log => {
                const isSuccess = log.status === "success";
                const isWarning = log.status === "warning";
                const isError = log.status === "error";

                return (
                  <div key={log.id} className="p-2.5 bg-neutral-50/60 rounded-lg border border-neutral-200/40 shadow-xs leading-relaxed">
                    <div className="flex items-center justify-between mb-1.5">
                      <span className={`font-bold px-1.5 py-0.5 rounded uppercase text-[8px] tracking-wider border ${
                        isSuccess ? "bg-neutral-100 border-neutral-200 text-neutral-800" :
                        isWarning ? "bg-amber-50 border-amber-100 text-amber-700" :
                        isError ? "bg-red-50 border-red-100 text-red-700" : "bg-neutral-50 border-neutral-200 text-neutral-500"
                      }`}>
                        {log.eventType}
                      </span>
                      <span className="text-neutral-400 font-medium">{formatTime(log.timestamp)}</span>
                    </div>
                    <p className="text-neutral-700 leading-normal font-medium">{log.details}</p>
                    <div className="text-[8px] text-neutral-400 mt-1.5 flex justify-between font-medium">
                      <span>IP: {log.ipAddress}</span>
                      <span>REQ: {log.requestId}</span>
                    </div>
                  </div>
                );
              })}

              {auditLogs.length === 0 && (
                <div className="text-center text-neutral-400 py-6 italic font-medium">No audit logs reported.</div>
              )}
            </div>
          </div>

        </aside>

      </div>

      {/* Primary Footer */}
      <footer className="h-10 border-t border-neutral-200 bg-white px-8 flex items-center justify-between text-[9px] font-mono uppercase tracking-widest text-neutral-400 flex-shrink-0">
        <div className="flex gap-6">
          <span>AMR SPEC: V2.5</span>
          <span>Region: AWS-US-EAST-1</span>
          <span className="text-neutral-500 font-bold flex items-center gap-1.5">
            <span className="w-1.5 h-1.5 bg-neutral-400 rounded-full"></span>
            <span>HSM Secure Enclave</span>
          </span>
        </div>
        <div className="flex gap-6">
          <a href="#" className="hover:text-neutral-600 transition-colors">AMR Documentation</a>
          <a href="#" className="hover:text-neutral-600 transition-colors">Enclave Policy Support</a>
        </div>
      </footer>

    </div>
  );
}
