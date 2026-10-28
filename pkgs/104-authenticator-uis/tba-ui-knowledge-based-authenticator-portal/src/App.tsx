/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import { useState, useCallback, useMemo } from "react";
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
  Plus,
  Check,
  Smartphone,
  Play,
  Layout,
  RefreshCcw,
  Info,
  Sliders,
  Database
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
} from "./types";
import { APPROVED_QUESTIONS, DEFAULT_POLICY, DEFAULT_PROVIDERS, SEED_AUDIT_LOGS } from "./data";
import {
  KbaRiskNotice,
  KbaQuestionPicker,
  KbaAnswerField,
  KbaChallengeStep,
  KbaPolicySummary,
  CeremonyShell,
  AuthenticatorMethodPicker,
  RecentAuthenticationGate,
  AuthenticatorDetailPanel,
  AuthenticatorEventTimeline,
  PolicyImpactPreview,
  DangerZone
} from "./components/KbaComponents";

export default function App() {
  // ----------------------------------------------------
  // Global States
  // ----------------------------------------------------
  const [userEmail] = useState("jick.68.0@gmail.com");
  const [policy, setPolicy] = useState<TenantPolicy>(DEFAULT_POLICY);
  const [providers, setProviders] = useState<ProviderConfig[]>(DEFAULT_PROVIDERS);
  const [auditLogs, setAuditLogs] = useState<AuditEvent[]>(SEED_AUDIT_LOGS);

  // Default user credentials with pre-seeded questions to let users test challenges right away!
  const [credential, setCredential] = useState<KbaUserCredential>({
    status: AuthenticatorStatus.ACTIVE,
    enrollmentDate: "2026-07-15T12:00:00-07:00",
    lastUsedDate: "2026-07-16T15:25:02-07:00",
    enrolledQuestions: [
      { questionId: "q1", questionText: "What was the brand or manufacturer of your first vehicle?", normalizedHash: "toyota" },
      { questionId: "q2", questionText: "What was the first name of your supervisor at your very first professional job?", normalizedHash: "sarah" },
      { questionId: "q4", questionText: "What was the name of the elementary school you attended for first grade?", normalizedHash: "oakwood" }
    ],
    failureCount: 0,
    lockoutUntil: null
  });

  // Simulator Ceremony State
  const [activeCeremony, setActiveCeremony] = useState<CeremonyType>(CeremonyType.SIGN_IN);
  const [ceremonyStatus, setCeremonyStatus] = useState<CeremonyStatus>(CeremonyStatus.READY);
  const [statusMessage, setStatusMessage] = useState("");
  const [currentChallengeStep, setCurrentChallengeStep] = useState(0);
  const [isMobilePreview, setIsMobilePreview] = useState(false);

  // Inputs for active ceremony
  const [activeChallengeAnswers, setActiveChallengeAnswers] = useState<string[]>(["", "", ""]);
  const [challengeStepError, setChallengeStepError] = useState("");
  const [remainingChallengeAttempts, setRemainingChallengeAttempts] = useState(3);

  // Enrollment/Creation wizard state
  const [enrollmentStep, setEnrollmentStep] = useState<"notice" | "questions" | "review">("notice");
  const [wizardQuestions, setWizardQuestions] = useState<{ id: string; answer: string; confirm: string }[]>([
    { id: "q1", answer: "", confirm: "" },
    { id: "q2", answer: "", confirm: "" },
    { id: "q3", answer: "", confirm: "" }
  ]);
  const [wizardErrors, setWizardErrors] = useState<string[]>(["", "", ""]);

  // Authentication gate for lifecycle changes (Replace / Remove)
  const [isGateOpen, setIsGateOpen] = useState(false);
  const [pendingSensitiveAction, setPendingSensitiveAction] = useState<"replace" | "remove" | null>(null);

  // Dynamic simulation variables
  const [isSubmittingCeremony, setIsSubmittingCeremony] = useState(false);

  // ----------------------------------------------------
  // Helpers & Utility Handlers
  // ----------------------------------------------------
  const addAuditLog = useCallback((
    action: string,
    ceremony: CeremonyType,
    status: CeremonyStatus | "completed" | "failed",
    details: string,
    ip: string = "192.168.1.45"
  ) => {
    const newEvent: AuditEvent = {
      id: `evt-${Math.floor(100 + Math.random() * 900)}`,
      timestamp: new Date().toISOString(),
      userEmail,
      action,
      ceremonyType: ceremony,
      status,
      providerId: "prov-1",
      details,
      ipAddress: ip,
      assuranceLevel: policy.minAssuranceRequired
    };
    setAuditLogs((prev) => [newEvent, ...prev]);
  }, [userEmail, policy.minAssuranceRequired]);

  // Normalize string for answer validation
  const normalizeAnswer = (str: string): string => {
    return str.trim().toLowerCase().replace(/[\s\-_]+/g, "");
  };

  const activeProvider = useMemo(() => {
    return providers.find(p => p.id === "prov-1") || providers[0];
  }, [providers]);

  // Reset the ceremony back to initial ready state
  const resetCeremony = useCallback((type: CeremonyType = CeremonyType.SIGN_IN) => {
    setActiveCeremony(type);
    setCeremonyStatus(CeremonyStatus.READY);
    setStatusMessage("");
    setCurrentChallengeStep(0);
    setActiveChallengeAnswers(["", "", ""]);
    setChallengeStepError("");
    setRemainingChallengeAttempts(policy.maxAttempts);
    setIsSubmittingCeremony(false);

    // If enrolling, reset step
    if (type === CeremonyType.ENROLLMENT || type === CeremonyType.REPLACEMENT) {
      setEnrollmentStep("notice");
      setWizardQuestions([
        { id: "q1", answer: "", confirm: "" },
        { id: "q2", answer: "", confirm: "" },
        { id: "q3", answer: "", confirm: "" }
      ]);
      setWizardErrors(["", "", ""]);
    }
  }, [policy.maxAttempts]);

  // ----------------------------------------------------
  // Ceremonies Implementation
  // ----------------------------------------------------

  // 1. Enrollment Ceremony Submit
  const handleEnrollmentSubmit = () => {
    // Validate inputs
    let hasError = false;
    const errors = ["", "", ""];

    // Ensure proper number of questions
    const requiredCount = policy.requiredQuestionCount;
    const selectedIds = wizardQuestions.slice(0, requiredCount).map(q => q.id);
    const uniqueIds = new Set(selectedIds);

    if (uniqueIds.size !== requiredCount) {
      alert("Duplicate questions detected. Please select distinct questions.");
      return;
    }

    for (let i = 0; i < requiredCount; i++) {
      const q = wizardQuestions[i];
      if (!q.id) {
        errors[i] = "Please select an approved security question.";
        hasError = true;
      } else if (!q.answer.trim()) {
        errors[i] = "Answer input cannot be left blank.";
        hasError = true;
      } else if (q.answer !== q.confirm) {
        errors[i] = "Confirmation answer mismatch. Please verify input.";
        hasError = true;
      }
    }

    setWizardErrors(errors);
    if (hasError) return;

    // Proceed to Review stage
    setEnrollmentStep("review");
  };

  const handleEnrollmentComplete = () => {
    setIsSubmittingCeremony(true);
    setCeremonyStatus(CeremonyStatus.SUBMITTING);

    setTimeout(() => {
      // Build credential questions
      const enrolled: KbaAnswerEnrollment[] = wizardQuestions
        .slice(0, policy.requiredQuestionCount)
        .map((q) => {
          const originalText = APPROVED_QUESTIONS.find(aq => aq.id === q.id)?.text || "Enrolled Question";
          return {
            questionId: q.id,
            questionText: originalText,
            normalizedHash: normalizeAnswer(q.answer)
          };
        });

      setCredential((prev) => ({
        ...prev,
        status: AuthenticatorStatus.ACTIVE,
        enrollmentDate: new Date().toISOString(),
        enrolledQuestions: enrolled,
        failureCount: 0
      }));

      setIsSubmittingCeremony(false);
      setCeremonyStatus(CeremonyStatus.SUCCESS);
      setStatusMessage("KBA Enrollment activated successfully with server HMAC-SHA256 references stored.");
      addAuditLog("enrollment_completed", CeremonyType.ENROLLMENT, CeremonyStatus.SUCCESS, `User enrolled ${enrolled.length} questions successfully.`);
    }, 1200);
  };

  // 2. KBA Challenge Ceremony Submit (One question per step verification loop)
  const handleChallengeStepSubmit = () => {
    if (policy.isKbaProhibited) {
      setCeremonyStatus(CeremonyStatus.BLOCKED);
      setStatusMessage("Identity policy changed. KBA access has been prohibited globally.");
      return;
    }

    // Check provider health
    if (activeProvider.healthStatus === "outage") {
      setCeremonyStatus(CeremonyStatus.PROVIDER_UNAVAILABLE);
      setStatusMessage("The first-party identity verifier service is currently experiencing an outage. Try a fallback factor.");
      addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.PROVIDER_UNAVAILABLE, "Verification blocked due to provider service outage.");
      return;
    }

    setIsSubmittingCeremony(true);
    setChallengeStepError("");

    setTimeout(() => {
      const activeEnrolledQuestions = credential.enrolledQuestions;
      const targetQuestion = activeEnrolledQuestions[currentChallengeStep];
      const userInput = activeChallengeAnswers[currentChallengeStep];

      const isCorrect = normalizeAnswer(userInput) === targetQuestion.normalizedHash;

      setIsSubmittingCeremony(false);

      if (isCorrect) {
        // Go to next question or complete ceremony
        const nextStep = currentChallengeStep + 1;
        if (nextStep >= activeEnrolledQuestions.length || nextStep >= policy.requiredQuestionCount) {
          // Success!
          setCeremonyStatus(CeremonyStatus.SUCCESS);
          setCredential(prev => ({ ...prev, lastUsedDate: new Date().toISOString(), failureCount: 0 }));
          setStatusMessage(`Authentication ceremony complete. Evidence level: KBA-${policy.minAssuranceRequired}.`);
          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.SUCCESS, `KBA verification succeeded. Approved via provider ${activeProvider.name}.`);
        } else {
          setCurrentChallengeStep(nextStep);
          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.READY, `Verified question ${currentChallengeStep + 1} of ${policy.requiredQuestionCount}. Continuing step.`);
        }
      } else {
        // Mismatch logic
        const newAttempts = remainingChallengeAttempts - 1;
        setRemainingChallengeAttempts(newAttempts);

        if (newAttempts <= 0) {
          // Lockout trigger
          setCeremonyStatus(CeremonyStatus.ATTEMPTS_EXHAUSTED);
          setCredential(prev => ({ ...prev, status: AuthenticatorStatus.SUSPENDED, failureCount: policy.maxAttempts }));
          setStatusMessage("Too many invalid verification attempts. This credential has been suspended to prevent public indexing.");
          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.ATTEMPTS_EXHAUSTED, `Attempts exhausted lockout triggered. Status changed to SUSPENDED.`);
        } else {
          // Standard error message. Note: We must not identify *which* specific question failed. But since they verify step-by-step in the UI, we keep the error generic and allow them to re-attempt.
          setChallengeStepError("Verification failed. The answer does not match the enrolled record.");
          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.INVALID_RESPONSE, `Mismatch on question step ${currentChallengeStep + 1}. ${newAttempts} remaining.`);
        }
      }
    }, 1000);
  };

  // 3. Sensitive Action Guard Verification (MFA Step Up Gate)
  const triggerSensitiveAction = (action: "replace" | "remove") => {
    setPendingSensitiveAction(action);
    setIsGateOpen(true);
  };

  const handleGateVerifySuccess = () => {
    setIsGateOpen(false);
    const action = pendingSensitiveAction;
    setPendingSensitiveAction(null);

    if (action === "replace") {
      resetCeremony(CeremonyType.REPLACEMENT);
    } else if (action === "remove") {
      // Prevent last factor lockout rule: verify if there is another recovery or authentication method
      // (For simulation, we always permit, but we append a critical audit warning)
      setCredential({
        status: AuthenticatorStatus.NOT_ENROLLED,
        enrollmentDate: null,
        lastUsedDate: null,
        enrolledQuestions: [],
        failureCount: 0,
        lockoutUntil: null
      });
      addAuditLog("removal", CeremonyType.REMOVAL, CeremonyStatus.SUCCESS, "KBA Authenticator factor successfully removed under high-assurance gate protection.");
      alert("Authenticator has been removed successfully.");
    }
  };

  // 4. Quick Scenario Simulator Playbook Actions
  const runPresetScenario = (scenario: "compromise" | "outage" | "lockout" | "policy") => {
    if (scenario === "compromise") {
      setCredential(prev => ({ ...prev, status: AuthenticatorStatus.COMPROMISED }));
      addAuditLog("compromise_response", CeremonyType.SIGN_IN, CeremonyStatus.BLOCKED, "Simulated security response: External breach detected. KBA marked compromised.");
      alert("Scenario: Authenticator marked COMPROMISED. The portal now forces replacement.");
    } else if (scenario === "outage") {
      setProviders(prev => prev.map(p => p.id === "prov-1" ? { ...p, healthStatus: "outage" } : p));
      addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.PROVIDER_UNAVAILABLE, "Simulated provider health change: OUTAGE status detected on Aegis verifier.");
      alert("Scenario: Aegis provider outage triggered. Live challenges will now block.");
    } else if (scenario === "lockout") {
      setCredential(prev => ({ ...prev, status: AuthenticatorStatus.SUSPENDED, failureCount: policy.maxAttempts }));
      addAuditLog("challenge_attempt", CeremonyType.SIGN_IN, CeremonyStatus.ATTEMPTS_EXHAUSTED, "Simulated brute-force attack playbook. Lockout active.");
      alert("Scenario: Maximum failure attempts simulated. User is now suspended.");
    } else if (scenario === "policy") {
      setPolicy(prev => ({ ...prev, isKbaProhibited: true }));
      addAuditLog("policy_updated", CeremonyType.ENROLLMENT, CeremonyStatus.BLOCKED, "Simulated policy compliance rule: KBA strictly prohibited.");
      alert("Scenario: Enterprise compliance policy changed. KBA has been prohibited.");
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 font-sans text-slate-900 selection:bg-slate-900 selection:text-white" id="main-container">
      {/* Upper Navigation/Header */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-40 px-4 md:px-8 py-4 shadow-2xs">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-slate-900 animate-pulse" />
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-widest font-mono">
                AMR: KNOWLEDGE FACTOR (kba)
              </span>
            </div>
            <h1 className="text-xl md:text-2xl font-display font-bold tracking-tight text-slate-900 mt-1">
              Knowledge-Based Authentication Portal
            </h1>
            <p className="text-xs text-slate-500 mt-0.5">
              High-fidelity simulation arena for first-party KBA enrollment, verifier, policy, and diagnostics.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-3 bg-slate-50 border border-slate-200 px-4 py-2.5 rounded-xl text-xs">
            <div className="flex items-center gap-1.5 border-r border-slate-200 pr-3 mr-1">
              <Database className="h-4 w-4 text-slate-500" />
              <div>
                <span className="text-slate-400 block text-[9px] uppercase font-bold">Identified User</span>
                <span className="font-semibold text-slate-800">{userEmail}</span>
              </div>
            </div>
            <div>
              <span className="text-slate-400 block text-[9px] uppercase font-bold">MFA Guard State</span>
              <span className={`font-semibold capitalize flex items-center gap-1 ${
                credential.status === AuthenticatorStatus.ACTIVE
                  ? "text-emerald-600"
                  : credential.status === AuthenticatorStatus.NOT_ENROLLED
                  ? "text-slate-500"
                  : "text-rose-600"
              }`}>
                {credential.status === AuthenticatorStatus.ACTIVE ? <Unlock className="h-3 w-3" /> : <Lock className="h-3 w-3" />}
                {credential.status}
              </span>
            </div>
          </div>
        </div>
      </header>

      {/* Main Grid View */}
      <main className="max-w-7xl mx-auto px-4 md:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
          
          {/* ====================================================
              LEFT PANEL: LIVE SIMULATION ARENA (Lg: col-span-7)
              ==================================================== */}
          <div className="lg:col-span-7 space-y-6">
            
            {/* Header Simulator Controls */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
              <div className="flex justify-between items-center mb-4">
                <div className="flex items-center gap-2">
                  <Sliders className="h-4 w-4 text-slate-600" />
                  <h2 className="font-display font-semibold text-slate-950 text-base">
                    Active Simulation Deck
                  </h2>
                </div>
                <div className="flex gap-1.5 bg-slate-100 p-0.5 rounded-lg text-[10px] font-semibold border border-slate-200">
                  <button
                    onClick={() => setIsMobilePreview(false)}
                    className={`px-2.5 py-1 rounded-md transition-colors ${!isMobilePreview ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-800"}`}
                  >
                    Desktop UI
                  </button>
                  <button
                    onClick={() => setIsMobilePreview(true)}
                    className={`px-2.5 py-1 rounded-md transition-colors flex items-center gap-1 ${isMobilePreview ? "bg-white text-slate-900 shadow-xs" : "text-slate-500 hover:text-slate-800"}`}
                  >
                    <Smartphone className="h-3 w-3" /> Native UI
                  </button>
                </div>
              </div>

              {/* Selector for simulation ceremonies */}
              <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5">
                <button
                  onClick={() => resetCeremony(CeremonyType.SIGN_IN)}
                  className={`px-3 py-2 text-xs font-semibold rounded-lg border text-center transition-all ${
                    activeCeremony === CeremonyType.SIGN_IN
                      ? "bg-slate-950 border-slate-950 text-white shadow"
                      : "bg-white border-slate-200 text-slate-600 hover:border-slate-400"
                  }`}
                >
                  Sign-In Verification
                </button>
                <button
                  onClick={() => resetCeremony(CeremonyType.STEP_UP)}
                  className={`px-3 py-2 text-xs font-semibold rounded-lg border text-center transition-all ${
                    activeCeremony === CeremonyType.STEP_UP
                      ? "bg-slate-950 border-slate-950 text-white shadow"
                      : "bg-white border-slate-200 text-slate-600 hover:border-slate-400"
                  }`}
                >
                  Step-Up Challenge
                </button>
                <button
                  onClick={() => resetCeremony(CeremonyType.RECOVERY)}
                  className={`px-3 py-2 text-xs font-semibold rounded-lg border text-center transition-all ${
                    activeCeremony === CeremonyType.RECOVERY
                      ? "bg-slate-950 border-slate-950 text-white shadow"
                      : "bg-white border-slate-200 text-slate-600 hover:border-slate-400"
                  }`}
                >
                  Governed Recovery
                </button>
                <button
                  onClick={() => resetCeremony(CeremonyType.ENROLLMENT)}
                  className={`px-3 py-2 text-xs font-semibold rounded-lg border text-center transition-all ${
                    activeCeremony === CeremonyType.ENROLLMENT || activeCeremony === CeremonyType.REPLACEMENT
                      ? "bg-slate-950 border-slate-950 text-white shadow"
                      : "bg-white border-slate-200 text-slate-600 hover:border-slate-400"
                  }`}
                >
                  Enrollment Wizard
                </button>
              </div>
            </div>

            {/* Simulated Frame (Either native mockup or desktop box) */}
            <div className={isMobilePreview ? "max-w-sm mx-auto border-[10px] border-slate-900 rounded-[36px] bg-slate-950 p-3 shadow-2xl relative" : ""}>
              {isMobilePreview && (
                <div className="absolute top-0 left-1/2 -translate-x-1/2 w-28 h-4 bg-slate-900 rounded-b-xl z-20 flex items-center justify-center">
                  <span className="w-10 h-1 bg-slate-750 rounded-full" />
                </div>
              )}
              
              <div className={`${isMobilePreview ? "bg-white rounded-[26px] overflow-hidden min-h-[580px] text-slate-900 px-3 py-5 space-y-4" : "space-y-6"}`}>
                
                {/* 1. ENROLLMENT / REPLACEMENT WIZARD CEREMONY VIEW */}
                {(activeCeremony === CeremonyType.ENROLLMENT || activeCeremony === CeremonyType.REPLACEMENT) && (
                  <CeremonyShell
                    title={activeCeremony === CeremonyType.REPLACEMENT ? "Authenticator Questions Replacement" : "Enroll Security Questions Factor"}
                    subtitle="Register highly vetted, server-evaluated knowledge factors"
                    ceremonyType={activeCeremony}
                    status={ceremonyStatus}
                    statusText={statusMessage}
                    onReset={() => resetCeremony(activeCeremony)}
                  >
                    {ceremonyStatus === CeremonyStatus.READY && (
                      <div className="space-y-5">
                        
                        {/* Progressive Step Progress */}
                        <div className="flex justify-between items-center border-b border-slate-100 pb-3">
                          <span className="text-xs font-bold uppercase tracking-wider text-slate-400">Progress</span>
                          <div className="flex gap-1.5">
                            <span className={`h-2 w-10 rounded ${enrollmentStep === "notice" ? "bg-slate-900" : "bg-emerald-500"}`} />
                            <span className={`h-2 w-10 rounded ${enrollmentStep === "questions" ? "bg-slate-900" : enrollmentStep === "review" ? "bg-emerald-500" : "bg-slate-200"}`} />
                            <span className={`h-2 w-10 rounded ${enrollmentStep === "review" ? "bg-slate-900" : "bg-slate-200"}`} />
                          </div>
                        </div>

                        {/* STEP A: RISK NOTICE */}
                        {enrollmentStep === "notice" && (
                          <div className="space-y-4">
                            <KbaRiskNotice onDismiss={() => setEnrollmentStep("questions")} />
                            <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs space-y-2">
                              <h5 className="font-semibold text-slate-900 flex items-center gap-1.5">
                                <Info className="h-3.5 w-3.5 text-slate-500" /> Enrollment Constraints:
                              </h5>
                              <p className="text-slate-600">
                                You are enrolling exactly <strong>{policy.requiredQuestionCount}</strong> security questions. In accordance with enterprise policy guidelines:
                              </p>
                              <ul className="list-disc pl-4 text-slate-500 space-y-0.5">
                                <li>Answers must never be reused passwords or public facts.</li>
                                <li>Your answers will be converted to high-assurance hashes client-side.</li>
                              </ul>
                            </div>
                            <button
                              id="wizard-start-btn"
                              onClick={() => {
                                setEnrollmentStep("questions");
                                addAuditLog("enrollment_started", activeCeremony, CeremonyStatus.READY, "User entered KBA enrollment question wizard.");
                              }}
                              className="w-full py-2 bg-slate-950 hover:bg-slate-850 text-white font-semibold text-xs rounded-xl flex items-center justify-center gap-1"
                            >
                              Acknowledge and Begin <ArrowRight className="h-3.5 w-3.5" />
                            </button>
                          </div>
                        )}

                        {/* STEP B: QUESTIONS SELECTION AND CONFIRMATION */}
                        {enrollmentStep === "questions" && (
                          <div className="space-y-5">
                            {Array.from({ length: policy.requiredQuestionCount }).map((_, idx) => (
                              <div key={idx} className="p-4 border border-slate-200 rounded-xl bg-slate-50/50 space-y-3.5">
                                <span className="text-[10px] font-bold text-slate-400 block uppercase tracking-wider">
                                  Verification Slot {idx + 1}
                                </span>
                                
                                <KbaQuestionPicker
                                  id={`wiz-q-picker-${idx}`}
                                  questions={APPROVED_QUESTIONS}
                                  selectedQuestionId={wizardQuestions[idx]?.id || ""}
                                  onChange={(val) => {
                                    const updated = [...wizardQuestions];
                                    updated[idx] = { ...updated[idx], id: val };
                                    setWizardQuestions(updated);
                                  }}
                                  excludeQuestionIds={wizardQuestions.map((q, i) => i !== idx ? q.id : "").filter(Boolean)}
                                />

                                <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-1">
                                  <KbaAnswerField
                                    id={`wiz-answer-${idx}`}
                                    value={wizardQuestions[idx]?.answer || ""}
                                    onChange={(val) => {
                                      const updated = [...wizardQuestions];
                                      updated[idx] = { ...updated[idx], answer: val };
                                      setWizardQuestions(updated);
                                    }}
                                    placeholder="Enforce answer precision"
                                    label="Create Answer"
                                  />
                                  <KbaAnswerField
                                    id={`wiz-confirm-${idx}`}
                                    value={wizardQuestions[idx]?.confirm || ""}
                                    onChange={(val) => {
                                      const updated = [...wizardQuestions];
                                      updated[idx] = { ...updated[idx], confirm: val };
                                      setWizardQuestions(updated);
                                    }}
                                    placeholder="Confirm exact answer spelling"
                                    label="Confirm Answer"
                                    error={wizardErrors[idx]}
                                  />
                                </div>
                              </div>
                            ))}

                            <div className="flex gap-3 pt-2">
                              <button
                                onClick={() => setEnrollmentStep("notice")}
                                className="px-4 py-2 border border-slate-200 text-xs font-semibold rounded-lg text-slate-600 hover:bg-slate-50"
                              >
                                Back
                              </button>
                              <button
                                id="wiz-questions-next-btn"
                                onClick={handleEnrollmentSubmit}
                                className="flex-1 py-2 bg-slate-900 hover:bg-slate-800 text-white font-semibold text-xs rounded-lg flex items-center justify-center gap-1"
                              >
                                Review & Confirm <ArrowRight className="h-3.5 w-3.5" />
                              </button>
                            </div>
                          </div>
                        )}

                        {/* STEP C: REVIEW & FINALIZE */}
                        {enrollmentStep === "review" && (
                          <div className="space-y-4 text-xs">
                            <div className="bg-slate-900 text-white rounded-xl p-4 space-y-3">
                              <h5 className="font-display font-semibold text-sm">Security Enrollment Manifest</h5>
                              <p className="text-slate-400 text-[11px] leading-relaxed">
                                Please review your selected questions. Raw answers are cleared immediately upon submission. Only secure reference hashes are saved.
                              </p>
                              <div className="space-y-2 border-t border-slate-800 pt-3">
                                {wizardQuestions.slice(0, policy.requiredQuestionCount).map((q, idx) => {
                                  const text = APPROVED_QUESTIONS.find(aq => aq.id === q.id)?.text;
                                  return (
                                    <div key={idx} className="flex justify-between items-start gap-4">
                                      <span className="text-slate-400 font-medium">Slot {idx+1}:</span>
                                      <div className="text-right">
                                        <p className="font-semibold text-white">{text}</p>
                                        <p className="font-mono text-[10px] text-slate-400 mt-0.5">Answer Hash: [HIDDEN]</p>
                                      </div>
                                    </div>
                                  );
                                })}
                              </div>
                            </div>

                            <div className="flex gap-3 pt-2">
                              <button
                                onClick={() => setEnrollmentStep("questions")}
                                className="px-4 py-2 border border-slate-200 font-semibold rounded-lg text-slate-600 hover:bg-slate-50"
                              >
                                Edit Answers
                              </button>
                              <button
                                id="wiz-finalize-btn"
                                onClick={handleEnrollmentComplete}
                                disabled={isSubmittingCeremony}
                                className="flex-1 py-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold rounded-lg flex items-center justify-center gap-1 shadow"
                              >
                                {isSubmittingCeremony ? <RefreshCw className="h-4.5 w-4.5 animate-spin" /> : "Authorize & Activate Verification"}
                              </button>
                            </div>
                          </div>
                        )}

                      </div>
                    )}
                  </CeremonyShell>
                )}

                {/* 2. CHOSEN AUTHENTICATION CHANNELS CEREMONY VIEW (SIGN IN / STEP UP / RECOVERY) */}
                {activeCeremony !== CeremonyType.ENROLLMENT && activeCeremony !== CeremonyType.REPLACEMENT && (
                  <CeremonyShell
                    title={
                      activeCeremony === CeremonyType.SIGN_IN
                        ? "Verify Sign-In Factor"
                        : activeCeremony === CeremonyType.STEP_UP
                        ? "Elevated Step-Up Challenge"
                        : "Account Recovery Challenge"
                    }
                    subtitle={
                      activeCeremony === CeremonyType.SIGN_IN
                        ? "Confirm your identity via registered credentials"
                        : activeCeremony === CeremonyType.STEP_UP
                        ? "High-assurance session confirmation"
                        : "Supervised fallback authentication loop"
                    }
                    ceremonyType={activeCeremony}
                    status={ceremonyStatus}
                    statusText={statusMessage}
                    onReset={() => resetCeremony(activeCeremony)}
                  >
                    {/* Ready selection state (offering KBA vs other factors) */}
                    {ceremonyStatus === CeremonyStatus.READY && currentChallengeStep === 0 && (
                      <div className="space-y-5">
                        
                        {/* Notice for KBA Status */}
                        {credential.status !== AuthenticatorStatus.ACTIVE ? (
                          <div className="bg-slate-50 border border-slate-200 rounded-2xl p-5 text-center space-y-3">
                            <HelpCircle className="h-10 w-10 text-slate-400 mx-auto" />
                            <div>
                              <h4 className="font-display font-semibold text-slate-800 text-sm">Security questions not active</h4>
                              <p className="text-xs text-slate-500 max-w-xs mx-auto mt-1">
                                Your account does not have KBA verification questions enrolled yet. Use the Enrollment tab to configure them.
                              </p>
                            </div>
                            <button
                              id="simulate-enrollment-trigger-btn"
                              onClick={() => resetCeremony(CeremonyType.ENROLLMENT)}
                              className="px-4 py-2 bg-slate-900 hover:bg-slate-850 text-white text-xs font-semibold rounded-lg shadow"
                            >
                              Run Enrollment Ceremony
                            </button>
                          </div>
                        ) : (
                          <>
                            <div className="bg-slate-50 border border-slate-100 p-4 rounded-xl text-xs space-y-1 text-slate-600">
                              <p className="font-semibold text-slate-800">Dynamic Context Notice:</p>
                              <p>
                                Select from the security parameters below. Knowledge factor verification questions will query exactly {policy.requiredQuestionCount} server-evaluated slots consecutively.
                              </p>
                            </div>

                            <AuthenticatorMethodPicker
                              isKbaEnrolled={credential.status === AuthenticatorStatus.ACTIVE}
                              isKbaProhibited={policy.isKbaProhibited}
                              onSelectMethod={(method) => {
                                if (method === "kba") {
                                  setCurrentChallengeStep(0);
                                  setRemainingChallengeAttempts(policy.maxAttempts);
                                  addAuditLog("challenge_started", activeCeremony, CeremonyStatus.READY, `User initiated security questions verification challenge.`);
                                  // Instantly transition to challenge
                                  setCeremonyStatus(CeremonyStatus.REQUIRES_NEXT_STEP);
                                } else {
                                  alert(`Simulation: Chosen factor [${method}] requires different token handlers. This playground focuses on KBA (Security Questions).`);
                                }
                              }}
                            />
                          </>
                        )}
                      </div>
                    )}

                    {/* Active Challenge Ceremony Steps */}
                    {ceremonyStatus === CeremonyStatus.REQUIRES_NEXT_STEP && credential.status === AuthenticatorStatus.ACTIVE && (
                      <KbaChallengeStep
                        currentStep={currentChallengeStep + 1}
                        totalSteps={Math.min(credential.enrolledQuestions.length, policy.requiredQuestionCount)}
                        questionText={credential.enrolledQuestions[currentChallengeStep]?.questionText || "Unknown Question Slot"}
                        answerValue={activeChallengeAnswers[currentChallengeStep] || ""}
                        onAnswerChange={(val) => {
                          const updated = [...activeChallengeAnswers];
                          updated[currentChallengeStep] = val;
                          setActiveChallengeAnswers(updated);
                        }}
                        onSubmit={handleChallengeStepSubmit}
                        onCancel={() => {
                          resetCeremony(activeCeremony);
                          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.CANCELLED, "Challenge verification ceremony canceled by user.");
                        }}
                        error={challengeStepError}
                        isSubmitting={isSubmittingCeremony}
                        expirySeconds={policy.sessionFreshnessSeconds}
                        onExpired={() => {
                          setCeremonyStatus(CeremonyStatus.EXPIRED);
                          setStatusMessage("The authentication challenge session has expired due to compliance freshness duration.");
                          addAuditLog("challenge_attempt", activeCeremony, CeremonyStatus.EXPIRED, "Verification session expired based on freshness timer.");
                        }}
                        remainingAttempts={remainingChallengeAttempts}
                      />
                    )}
                  </CeremonyShell>
                )}

                {/* 3. AUTHENTICATOR DETAIL & OPERATIONS PANEL */}
                {credential.status !== AuthenticatorStatus.NOT_ENROLLED && (
                  <div className="pt-2">
                    <AuthenticatorDetailPanel
                      credential={credential}
                      policy={policy}
                      onReplaceTrigger={() => triggerSensitiveAction("replace")}
                      onRemoveTrigger={() => triggerSensitiveAction("remove")}
                    />
                  </div>
                )}

                {/* 4. SECURITY DANGER ZONE */}
                <div className="pt-2">
                  <DangerZone
                    isKbaEnrolled={credential.status === AuthenticatorStatus.ACTIVE}
                    onRemoveRequest={() => triggerSensitiveAction("remove")}
                    onCompromiseSimulate={() => runPresetScenario("compromise")}
                  />
                </div>

              </div>
            </div>

          </div>

          {/* ====================================================
              RIGHT PANEL: CONTROLS, SCHEMAS & LOGS (Lg: col-span-5)
              ==================================================== */}
          <div className="lg:col-span-5 space-y-6">
            
            {/* Playbook Scenario Quick Simulation */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm">
              <div className="flex items-center gap-2 mb-3">
                <Play className="h-4 w-4 text-indigo-600" />
                <h3 className="font-display font-semibold text-slate-900 text-sm">
                  Quick Simulation Playbook
                </h3>
              </div>
              <p className="text-xs text-slate-500 mb-4 leading-normal">
                Trigger security incidents and edge-case exceptions to observe proportional error and UIX defenses.
              </p>
              <div className="grid grid-cols-2 gap-2 text-xs">
                <button
                  onClick={() => runPresetScenario("compromise")}
                  className="px-3 py-2 bg-red-50 hover:bg-red-100 text-red-800 rounded-xl border border-red-200 text-left font-medium transition-colors"
                >
                  <span className="font-bold block">1. Compromise Leak</span>
                  Status set to compromised.
                </button>
                <button
                  onClick={() => runPresetScenario("outage")}
                  className="px-3 py-2 bg-amber-50 hover:bg-amber-100 text-amber-800 rounded-xl border border-amber-200 text-left font-medium transition-colors"
                >
                  <span className="font-bold block">2. Service Outage</span>
                  Set provider status to offline.
                </button>
                <button
                  onClick={() => runPresetScenario("lockout")}
                  className="px-3 py-2 bg-rose-50 hover:bg-rose-100 text-rose-800 rounded-xl border border-rose-200 text-left font-medium transition-colors"
                >
                  <span className="font-bold block">3. Replay Brute-Force</span>
                  Trigger lockout block.
                </button>
                <button
                  onClick={() => runPresetScenario("policy")}
                  className="px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-800 rounded-xl border border-slate-200 text-left font-medium transition-colors"
                >
                  <span className="font-bold block">4. Enforce Prohibition</span>
                  Disable KBA method.
                </button>
              </div>
            </div>

            {/* Tenant Policy Administration Panel */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2">
                  <Settings className="h-4 w-4 text-slate-700" />
                  <h3 className="font-display font-semibold text-slate-900 text-sm">
                    Tenant Security Administration
                  </h3>
                </div>
                <span className="text-[10px] font-bold bg-slate-100 text-slate-700 px-2 py-0.5 rounded">
                  Operator Mode
                </span>
              </div>

              {/* Policy Inputs */}
              <div className="space-y-4 text-xs">
                {/* Prohibit Check */}
                <div className="flex items-center justify-between p-2.5 bg-slate-50 rounded-xl border border-slate-100">
                  <div>
                    <span className="font-semibold text-slate-900 block">Prohibit KBA Authentication</span>
                    <span className="text-[11px] text-slate-400">Strictly block all KBA enrollment and challenge use.</span>
                  </div>
                  <input
                    id="admin-prohibit-toggle"
                    type="checkbox"
                    checked={policy.isKbaProhibited}
                    onChange={(e) => {
                      const updated = { ...policy, isKbaProhibited: e.target.checked };
                      setPolicy(updated);
                      addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.READY, `Compliance rule KBA Prohibited toggled to ${e.target.checked}.`);
                    }}
                    className="h-4 w-4 text-slate-900 focus:ring-slate-900 border-slate-300 rounded"
                  />
                </div>

                {/* Challenge Count */}
                <div className="space-y-1">
                  <label htmlFor="admin-required-count" className="block font-semibold text-slate-700">
                    Required Questions challenge scale
                  </label>
                  <select
                    id="admin-required-count"
                    value={policy.requiredQuestionCount}
                    onChange={(e) => {
                      const updated = { ...policy, requiredQuestionCount: parseInt(e.target.value) };
                      setPolicy(updated);
                      addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.READY, `Compliance policy: Required KBA Question count set to ${e.target.value}.`);
                    }}
                    className="w-full border border-slate-300 rounded-lg p-2 bg-white"
                  >
                    <option value={2}>2 Questions Consecutive Verification</option>
                    <option value={3}>3 Questions Consecutive Verification</option>
                    <option value={4}>4 Questions Consecutive Verification</option>
                  </select>
                </div>

                {/* Max Attempts Budget */}
                <div className="space-y-1">
                  <label htmlFor="admin-max-attempts" className="block font-semibold text-slate-700">
                    Attempts budget (Failure Lockout Trigger)
                  </label>
                  <select
                    id="admin-max-attempts"
                    value={policy.maxAttempts}
                    onChange={(e) => {
                      const updated = { ...policy, maxAttempts: parseInt(e.target.value) };
                      setPolicy(updated);
                      addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.READY, `Compliance policy: Max attempts budget threshold updated to ${e.target.value}.`);
                    }}
                    className="w-full border border-slate-300 rounded-lg p-2 bg-white"
                  >
                    <option value={2}>2 Incorrect Answers before Lockout</option>
                    <option value={3}>3 Incorrect Answers before Lockout</option>
                    <option value={5}>5 Incorrect Answers before Lockout</option>
                  </select>
                </div>

                {/* Session Freshness Timer */}
                <div className="space-y-1">
                  <label htmlFor="admin-session-expiry" className="block font-semibold text-slate-700">
                    Challenge session Freshness constraint
                  </label>
                  <select
                    id="admin-session-expiry"
                    value={policy.sessionFreshnessSeconds}
                    onChange={(e) => {
                      const updated = { ...policy, sessionFreshnessSeconds: parseInt(e.target.value) };
                      setPolicy(updated);
                      addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.READY, `Compliance policy: Expiry freshness limit set to ${e.target.value} seconds.`);
                    }}
                    className="w-full border border-slate-300 rounded-lg p-2 bg-white"
                  >
                    <option value={60}>60 Seconds (Aggressive timer)</option>
                    <option value={120}>120 Seconds (2 mins compliance standard)</option>
                    <option value={300}>300 Seconds (5 mins relaxed)</option>
                  </select>
                </div>
              </div>

              {/* Policy Impact Preview */}
              <PolicyImpactPreview policy={policy} />
            </div>

            {/* Provider Configuration and Health Desk */}
            <div className="bg-white border border-slate-200 rounded-2xl p-5 shadow-sm space-y-4">
              <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                <div className="flex items-center gap-2">
                  <Server className="h-4 w-4 text-slate-700" />
                  <h3 className="font-display font-semibold text-slate-900 text-sm">
                    First-Party Provider Config
                  </h3>
                </div>
                <span className="text-[10px] font-bold text-amber-800 bg-amber-50 px-2 py-0.5 rounded border border-amber-100">
                  Active Trust Boundary
                </span>
              </div>

              <div className="space-y-3.5">
                {providers.map((p) => (
                  <div key={p.id} className="p-3 border border-slate-100 bg-slate-50/50 rounded-xl text-xs space-y-2">
                    <div className="flex justify-between items-start">
                      <div>
                        <span className="font-bold text-slate-900 block">{p.name}</span>
                        <span className="text-[10px] text-slate-400 font-mono">ID: {p.id} ({p.sourceType})</span>
                      </div>
                      <select
                        id={`provider-${p.id}-status`}
                        value={p.healthStatus}
                        onChange={(e) => {
                          const updated = providers.map(pr => pr.id === p.id ? { ...pr, healthStatus: e.target.checked ? "healthy" as const : "outage" as const } : pr);
                          // We treat toggle simple: if status changes we update
                          const nextStatus = e.target.value as "healthy" | "degraded" | "outage";
                          setProviders(providers.map(pr => pr.id === p.id ? { ...pr, healthStatus: nextStatus } : pr));
                          addAuditLog("policy_updated", CeremonyType.SIGN_IN, CeremonyStatus.READY, `Provider [${p.name}] status updated to: ${nextStatus.toUpperCase()}`);
                        }}
                        className={`text-[10px] font-bold p-1 rounded border focus:outline-none ${
                          p.healthStatus === "healthy"
                            ? "bg-emerald-50 text-emerald-800 border-emerald-200"
                            : p.healthStatus === "degraded"
                            ? "bg-amber-50 text-amber-800 border-amber-200"
                            : "bg-red-50 text-red-800 border-red-200"
                        }`}
                      >
                        <option value="healthy">Healthy</option>
                        <option value="degraded">Degraded</option>
                        <option value="outage">Outage (Offline)</option>
                      </select>
                    </div>

                    <div className="grid grid-cols-2 gap-2 text-[10px] text-slate-500 pt-1 border-t border-slate-100">
                      <div>
                        <span className="text-slate-400 block">Encryption boundary</span>
                        <span className="font-semibold text-slate-700">{p.encryptionAlgorithm}</span>
                      </div>
                      <div>
                        <span className="text-slate-400 block">Regional distribution</span>
                        <span className="font-semibold text-slate-700">{p.regionalAvailability.join(", ")}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Audit Logs / Activity Timeline */}
            <AuthenticatorEventTimeline events={auditLogs} />

          </div>

        </div>
      </main>

      {/* Proportional Verification Step Up Gate Modal */}
      <RecentAuthenticationGate
        isOpen={isGateOpen}
        onVerifySuccess={handleGateVerifySuccess}
        onCancel={() => {
          setIsGateOpen(false);
          setPendingSensitiveAction(null);
        }}
      />
    </div>
  );
}
