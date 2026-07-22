import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  ShieldAlert,
  Fingerprint,
  Trash2,
  Lock,
  Unlock,
  Settings,
  Activity,
  CheckCircle2,
  AlertTriangle,
  RefreshCw,
  User,
  Globe,
  Award,
  ChevronRight,
  Info,
  Layers,
  Database,
  ArrowRight,
  Eye,
  Mic,
  Square
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

// Types
import {
  VoiceProfile,
  PolicyConfig,
  VerifierConfig,
  AuditLog,
  DiagnosticsSummary,
  VoiceBiometricStatus,
  LivenessClass,
  DeletionStatus,
  VoiceSample
} from './types';

// Mock DB Utility Functions
import {
  loadProfile,
  saveProfile,
  loadPolicy,
  savePolicy,
  loadVerifier,
  saveVerifier,
  loadAuditLogs,
  saveAuditLogs,
  addAuditLog,
  loadDiagnostics,
  saveDiagnostics,
  recordDiagResult,
  resetAllData
} from './mockData';

// Hook
import { useAudio } from './hooks/useAudio';

// Components
import VoiceConsentRecord from './components/VoiceConsentRecord';
import MicrophonePreflight from './components/MicrophonePreflight';
import RecordingControl from './components/RecordingControl';
import LivenessEvidenceSummary from './components/LivenessEvidenceSummary';
import BiometricDeletionStatus from './components/BiometricDeletionStatus';
import AdminPolicyPanel from './components/AdminPolicyPanel';
import DiagnosticsDashboard from './components/DiagnosticsDashboard';

const ENROLLMENT_CHALLENGES = [
  "My voice is my secure passport, verify my identity now.",
  "SentryVoice authorized access code seven two zero three.",
  "Acoustic analysis confirmed, biometric signature complete."
];

const VERIFICATION_CHALLENGES = [
  "Access granted to secure portal alpha five.",
  "Authenticate biometric signature with SentryVoice node.",
  "Acoustics verified, session confirmation requested."
];

export default function App() {
  // State from local storage/mock DB
  const [profile, setProfile] = useState<VoiceProfile>({
    id: 'usr_vbm_90241',
    status: 'unenrolled',
    consentSigned: false,
    consentVersion: 'v1.4-VBM-PRIVACY',
    samples: [],
    modelId: 'VBM-Neural-v4.2-Liveness',
    region: 'us-east1',
    deletionStatus: 'none',
  });
  const [policy, setPolicy] = useState<PolicyConfig>({
    minConfidence: 82,
    strictnessLevel: 'medium',
    allowedLanguages: ['en-US', 'es-MX', 'fr-FR'],
    fallbackFactor: 'fido_passkey',
    retentionDays: 180,
    strictLiveness: true,
    noiseThresholdDb: -42,
  });
  const [verifier, setVerifier] = useState<VerifierConfig>({
    providerName: 'SentryVoice Biometrics',
    endpointUrl: 'https://api.sentryvoice.biometrics.gcp/v2/verify',
    region: 'us-east1',
    activeModel: 'VBM-Neural-v4.2-Liveness',
    healthStatus: 'healthy',
    failBehavior: 'fail_safe',
  });
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([]);
  const [diagnostics, setDiagnostics] = useState<DiagnosticsSummary>({
    totalAttempts: 0,
    successCount: 0,
    failureCount: 0,
    spoofAttempts: { replay: 0, synthetic: 0 },
    noiseFailures: 0,
    noSpeechFailures: 0,
    averageResponseTimeMs: 0,
  });

  // Navigation and UI state
  const [activeTab, setActiveTab] = useState<'control' | 'admin' | 'diagnostics'>('control');
  const [wizardStep, setWizardStep] = useState<'idle' | 'consent' | 'preflight' | 'recording' | 'complete'>('idle');
  const [enrollmentIndex, setEnrollmentIndex] = useState(0); // 0, 1, 2 for the three challenges
  const [selectedVerificationChallenge, setSelectedVerificationChallenge] = useState('');

  // Active token modal / verification evidence state
  const [activeEvidence, setActiveEvidence] = useState<{
    amrToken: string;
    livenessClass: LivenessClass;
    confidenceScore: number;
    timeFreshnessMs: number;
    nonce: string;
  } | null>(null);

  // Verification capture state
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationStage, setVerificationStage] = useState<'idle' | 'recording' | 'processing'>('idle');

  // Simulation flags for testing failure criteria
  const [simulatedSpoof, setSimulatedSpoof] = useState<'replay' | 'synthetic' | 'none'>('none');
  const [simulatedNoise, setSimulatedNoise] = useState(false);

  // Audio Hook integration
  const audio = useAudio();

  // Load state on mount
  useEffect(() => {
    setProfile(loadProfile());
    setPolicy(loadPolicy());
    setVerifier(loadVerifier());
    setAuditLogs(loadAuditLogs());
    setDiagnostics(loadDiagnostics());
  }, []);

  // Synchronized state saving helpers
  const handleUpdateProfile = (newProfile: VoiceProfile) => {
    setProfile(newProfile);
    saveProfile(newProfile);
  };

  const handleUpdatePolicy = (newPolicy: PolicyConfig) => {
    setPolicy(newPolicy);
    savePolicy(newPolicy);
    // Log audit event
    addAuditLog(
      'POLICY_UPDATE',
      'success',
      `Security Policy updated: Min matching confidence set to ${newPolicy.minConfidence}%, strict liveness set to ${newPolicy.strictLiveness ? 'TRUE' : 'FALSE'}.`
    );
    setAuditLogs(loadAuditLogs());
  };

  const handleUpdateVerifier = (newVerifier: VerifierConfig) => {
    setVerifier(newVerifier);
    saveVerifier(newVerifier);
    addAuditLog(
      'VERIFIER_UPDATE',
      'success',
      `SentryVoice verifier endpoint URL configured to: ${newVerifier.endpointUrl}. Health node state: ${newVerifier.healthStatus.toUpperCase()}.`
    );
    setAuditLogs(loadAuditLogs());
  };

  const handleClearAuditLogs = () => {
    localStorage.removeItem('vbm_audit_logs');
    // Save fresh initial logs
    const defaultLogs: AuditLog[] = [
      {
        id: `tx_vbm_${Math.floor(1000 + Math.random() * 9000)}`,
        timestamp: new Date().toISOString(),
        action: 'LOGS_PURGED',
        status: 'info',
        details: 'Audit trail cleared by console administrator.',
        ipAddress: '192.168.1.100',
      }
    ];
    saveAuditLogs(defaultLogs);
    setAuditLogs(defaultLogs);
  };

  // Run a quick verification test
  const handleStartVerification = () => {
    const randomPhrase = VERIFICATION_CHALLENGES[Math.floor(Math.random() * VERIFICATION_CHALLENGES.length)];
    setSelectedVerificationChallenge(randomPhrase);
    setVerificationStage('recording');
    setIsVerifying(true);
    setSimulatedSpoof('none');
    setSimulatedNoise(false);
  };

  const handleStopAndProcessVerification = async () => {
    setVerificationStage('processing');
    audio.stopRecording();

    // SentryVoice Verifier parsing simulation delay
    setTimeout(() => {
      const responseTimeMs = Math.round(380 + Math.random() * 150);
      let score = Math.round(86 + Math.random() * 11);
      let liveness: LivenessClass = 'live';
      let outcomeStatus: 'success' | 'failure' | 'warning' = 'success';
      let logMsg = '';

      // Check simulated conditions injected by sandbox controllers
      if (simulatedSpoof === 'replay') {
        score = Math.round(42 + Math.random() * 15);
        liveness = 'replay';
        outcomeStatus = 'warning';
        logMsg = 'Voice verification aborted: Replay audio signature detected. Match probability low.';
      } else if (simulatedSpoof === 'synthetic') {
        score = Math.round(28 + Math.random() * 12);
        liveness = 'synthetic';
        outcomeStatus = 'failure';
        logMsg = 'High spoof threshold alert: Spectral formants indicate AI-generated speech (deepfake). Account blocked.';
      } else if (simulatedNoise) {
        score = 0;
        liveness = 'excessive_noise';
        outcomeStatus = 'warning';
        logMsg = 'Verification unsuccessful: Acoustic noise level exceeded boundary criteria (-42dB limit).';
      } else {
        logMsg = `Voice verification successful. confidence: ${score}%, liveness: verified live.`;
      }

      // Record telemetry
      if (liveness === 'live') {
        recordDiagResult('success', responseTimeMs);
      } else if (liveness === 'replay') {
        recordDiagResult('replay', responseTimeMs);
      } else if (liveness === 'synthetic') {
        recordDiagResult('synthetic', responseTimeMs);
      } else if (liveness === 'excessive_noise') {
        recordDiagResult('noise', responseTimeMs);
      }

      // Generate the token
      const nonce = Math.random().toString(36).substring(2, 14);
      const generatedToken = `amr_vbm.v1_match.${score}_${liveness}_sha256_${Math.random().toString(16).substring(2, 8)}`;

      addAuditLog('VERIFICATION_ATTEMPT', outcomeStatus, logMsg, generatedToken);
      
      // Update local state hooks
      setAuditLogs(loadAuditLogs());
      setDiagnostics(loadDiagnostics());

      setActiveEvidence({
        amrToken: generatedToken,
        livenessClass: liveness,
        confidenceScore: score,
        timeFreshnessMs: responseTimeMs,
        nonce,
      });

      setVerificationStage('idle');
      setIsVerifying(false);
    }, 1500);
  };

  // Enrollment process state handlers
  const handleStartEnrollmentWizard = () => {
    setWizardStep('consent');
    setEnrollmentIndex(0);
    setSimulatedSpoof('none');
    setSimulatedNoise(false);
  };

  const handleConsentGranted = (signerName: string, consentVersion: string) => {
    handleUpdateProfile({
      ...profile,
      consentSigned: true,
      consentVersion,
      consentSignedAt: new Date().toISOString(),
      status: 'unenrolled', // consent granted, awaiting calibration & recording
    });
    setWizardStep('preflight');
    addAuditLog(
      'CONSENT_GRANTED',
      'success',
      `Biometric consent disclosure version ${consentVersion} signed electronically by user ${signerName}.`
    );
    setAuditLogs(loadAuditLogs());
  };

  const handlePreflightCompleted = () => {
    setWizardStep('recording');
  };

  const handleSampleSaved = (duration: number, noiseDb: number, qualityScore: number) => {
    const isSpoofActive = simulatedSpoof !== 'none';
    // During enrollment sample capture, the user is speaking naturally, so the live decibel level will
    // always exceed the background noise threshold. We only want to trigger the noise rejection block
    // if the simulatedNoise test flag is explicitly set in the developer/sandbox deck.
    const isNoiseActive = simulatedNoise;

    // Trigger failure simulation if requested in Sandbox Panel
    if (isSpoofActive || isNoiseActive) {
      const responseTimeMs = Math.round(200 + Math.random() * 100);
      let cat: 'replay' | 'synthetic' | 'noise' = 'noise';
      let details = '';
      
      if (simulatedSpoof === 'replay') {
        cat = 'replay';
        details = 'Enrollment sample rejected: Replay attack signature identified on verifier node.';
      } else if (simulatedSpoof === 'synthetic') {
        cat = 'synthetic';
        details = 'Enrollment sample rejected: Neural vocoder pattern indicates AI synthetic deepfake voice.';
      } else {
        cat = 'noise';
        details = `Enrollment sample rejected: Ambient noise level (${noiseDb} dB) exceeds security policy threshold (${policy.noiseThresholdDb} dB).`;
      }

      recordDiagResult(cat, responseTimeMs);
      addAuditLog('ENROLLMENT_SAMPLE_REJECTED', 'warning', details);
      
      setAuditLogs(loadAuditLogs());
      setDiagnostics(loadDiagnostics());

      alert(details); // simple notification for simulation
      return;
    }

    // Save sample
    const newSample: VoiceSample = {
      id: `spl_${Math.floor(1000 + Math.random() * 9000)}`,
      phrase: ENROLLMENT_CHALLENGES[enrollmentIndex],
      durationSeconds: duration,
      noiseDb,
      qualityScore,
      timestamp: new Date().toISOString(),
    };

    const updatedSamples = [...profile.samples, newSample];
    const isComplete = enrollmentIndex === ENROLLMENT_CHALLENGES.length - 1;

    if (isComplete) {
      // Completed all 3 steps successfully!
      const finalProfile: VoiceProfile = {
        ...profile,
        status: 'enrolled',
        createdTime: new Date().toISOString(),
        lastUsedTime: new Date().toISOString(),
        samples: updatedSamples,
      };

      handleUpdateProfile(finalProfile);
      addAuditLog(
        'ENROLLMENT_COMPLETED',
        'success',
        `Enrollment completed successfully. 3 independent voice vectors generated and verified in regional vault.`
      );
      setAuditLogs(loadAuditLogs());
      setWizardStep('complete');
    } else {
      // Advance step
      handleUpdateProfile({
        ...profile,
        samples: updatedSamples,
      });
      setEnrollmentIndex(enrollmentIndex + 1);
    }
  };

  // Deletion / Lifecycle Erasure handlers
  const handleInitiateDeletion = (forceFail?: boolean) => {
    handleUpdateProfile({
      ...profile,
      deletionStatus: 'pending',
    });

    setTimeout(() => {
      if (forceFail) {
        handleUpdateProfile({
          ...profile,
          deletionStatus: 'failed',
        });
        addAuditLog(
          'DELETION_FAILED',
          'failure',
          'Compliance erasure request failed: Active SentryVoice directory offline (connection timeout).'
        );
        setAuditLogs(loadAuditLogs());
        return;
      }

      // Clear state and mark as deleted
      const clearedProfile: VoiceProfile = {
        id: 'usr_vbm_90241',
        status: 'deleted',
        consentSigned: false,
        consentVersion: 'v1.4-VBM-PRIVACY',
        samples: [],
        modelId: 'VBM-Neural-v4.2-Liveness',
        region: 'us-east1',
        deletionStatus: 'completed',
        deletionTxHash: `sha256_del_${Math.random().toString(16).substring(2, 10)}${Math.random().toString(16).substring(2, 10)}`,
        deletionRequestTime: new Date().toISOString(),
      };

      handleUpdateProfile(clearedProfile);
      addAuditLog(
        'BIOMETRIC_PROFILE_PURGED',
        'success',
        'Biometric profile hard-purged. Illinois BIPA consent revoked. Mathematical vectors deleted permanently.'
      );
      setAuditLogs(loadAuditLogs());
    }, 3000);
  };

  const handleResetDeletionStatus = () => {
    if (profile.status === 'deleted') {
      // Fully reset back to unenrolled state
      const cleanProfile: VoiceProfile = {
        id: 'usr_vbm_90241',
        status: 'unenrolled',
        consentSigned: false,
        consentVersion: 'v1.4-VBM-PRIVACY',
        samples: [],
        modelId: 'VBM-Neural-v4.2-Liveness',
        region: 'us-east1',
        deletionStatus: 'none',
      };
      handleUpdateProfile(cleanProfile);
    } else {
      handleUpdateProfile({
        ...profile,
        deletionStatus: 'none',
      });
    }
  };

  // Render current active layout
  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-indigo-500/30 selection:text-indigo-200">
      {/* Top Header Navigation */}
      <header className="bg-slate-900 border-b border-slate-800 sticky top-0 z-40 px-6 py-4 flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-gradient-to-tr from-indigo-600 to-indigo-500 text-slate-950 rounded-2xl shadow-lg shadow-indigo-500/20">
            <Fingerprint className="w-6 h-6 text-slate-950" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <h1 className="font-sans font-bold tracking-tight text-slate-100 text-lg">Voice Biometric Authenticator</h1>
              <span className="bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 font-mono text-[9px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
                gcp node
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-0.5">Enterprise identity directory, sandboxed acoustic calibration & liveness audit log</p>
          </div>
        </div>

        {/* Global tab options */}
        <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs font-mono">
          <button
            type="button"
            onClick={() => setActiveTab('control')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
              activeTab === 'control'
                ? 'bg-slate-800 text-indigo-300 shadow-md border-b-2 border-indigo-500/50'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            <Layers className="w-4 h-4" />
            <span>Identity Portal</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('admin')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
              activeTab === 'admin'
                ? 'bg-slate-800 text-indigo-300 shadow-md border-b-2 border-indigo-500/50'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            <Settings className="w-4 h-4" />
            <span>Policy Admin</span>
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('diagnostics')}
            className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-all ${
              activeTab === 'diagnostics'
                ? 'bg-slate-800 text-indigo-300 shadow-md border-b-2 border-indigo-500/50'
                : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            <Activity className="w-4 h-4" />
            <span>Diagnostics Deck</span>
          </button>
        </div>
      </header>

      {/* Main Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Area (Primary Interaction Portal) - 7 Columns */}
        <div className="lg:col-span-7 space-y-6">
          
          {/* Main Action Tabs Wrapper */}
          {activeTab === 'control' && (
            <AnimatePresence mode="wait">
              
              {/* Wizard Status or Welcome UI */}
              {wizardStep === 'idle' && (
                <motion.div
                  key="vbm-welcome-or-dashboard"
                  initial={{ opacity: 0, y: 15 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -15 }}
                  transition={{ duration: 0.3 }}
                >
                  {profile.status === 'unenrolled' || profile.status === 'deleted' ? (
                    /* Welcome Box (Unenrolled state) */
                    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-8 space-y-6 shadow-2xl relative overflow-hidden" id="card-welcome">
                      {/* Ambient light overlay */}
                      <div className="absolute top-0 right-0 w-64 h-64 bg-indigo-500/5 rounded-full filter blur-3xl" />
                      
                      <div className="space-y-3">
                        <span className="text-[10px] bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 font-mono font-semibold px-2.5 py-1 rounded-md uppercase tracking-widest">
                          AMR METHOD: vbm
                        </span>
                        <h2 className="text-3xl font-sans font-extrabold tracking-tight text-slate-100">
                          Passwordless Biometric Voice Sign-In
                        </h2>
                        <p className="text-sm text-slate-400 leading-relaxed font-sans">
                          SentryVoice converts the unique biological formants of your vocal tract into a high-entropy mathematical representation. 
                          By scanning phase variations, jitter, and deep-layer speech envelopes, the neural engine validates identity in real-time, 
                          completely blocking AI voice deepfakes and physical replay attacks.
                        </p>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 font-mono text-[11px] text-slate-500 pt-2">
                        <div className="bg-slate-950/40 p-4 border border-slate-850 rounded-2xl">
                          <strong className="text-indigo-400 block mb-1">🔐 True Sandboxing</strong>
                          No raw audio file is ever saved on disk. Only encrypted vectors are generated.
                        </div>
                        <div className="bg-slate-950/40 p-4 border border-slate-850 rounded-2xl">
                          <strong className="text-emerald-400 block mb-1">⏱️ Pure Latency</strong>
                          Verifier processing time averages under 450ms globally with zero-cold starts.
                        </div>
                        <div className="bg-slate-950/40 p-4 border border-slate-850 rounded-2xl">
                          <strong className="text-indigo-400 block mb-1">⚖️ Compliance First</strong>
                          Illinois BIPA, CCPA, and EU GDPR compliant with instant self-erasure.
                        </div>
                      </div>

                      <div className="pt-4 flex flex-col sm:flex-row gap-3 items-center">
                        <button
                          type="button"
                          onClick={handleStartEnrollmentWizard}
                          className="w-full sm:w-auto bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-sans font-bold text-xs py-3 px-6 rounded-xl flex items-center justify-center gap-2 transition-all shadow-lg shadow-indigo-500/10"
                          id="btn-start-enroll"
                        >
                          <span>Securely Enroll Voice Profile</span>
                          <ArrowRight className="w-4 h-4 text-slate-950" />
                        </button>
                        <p className="text-[10px] text-slate-500 text-center sm:text-left">
                          Required hardware check: Standard desktop/mobile microphone.
                        </p>
                      </div>
                    </div>
                  ) : (
                    /* Dashboard Box (Enrolled state) */
                    <div className="space-y-6" id="dashboard-active-profile">
                      {/* Primary Profile status display */}
                      <div className="bg-slate-900 border border-slate-800 rounded-3xl p-6 shadow-2xl relative overflow-hidden">
                        <div className="absolute top-0 right-0 w-56 h-56 bg-emerald-500/5 rounded-full filter blur-3xl" />
                        
                        <div className="flex items-start justify-between">
                          <div className="flex items-center gap-3">
                            <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-2xl shadow-inner">
                              <ShieldCheck className="w-6 h-6" />
                            </div>
                            <div>
                              <div className="flex items-center gap-2">
                                <h3 className="font-sans font-semibold tracking-tight text-slate-100 text-lg">Biometric Profile Activated</h3>
                                <span className="bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 font-mono text-[9px] px-2 py-0.5 rounded-full font-bold uppercase tracking-wider">
                                  verified
                                </span>
                              </div>
                              <p className="font-mono text-[10px] text-slate-400 mt-0.5">Directory Reference ID: {profile.id}</p>
                            </div>
                          </div>
                          
                          <button
                            type="button"
                            onClick={() => handleUpdateProfile({ ...profile, deletionStatus: 'none' })}
                            className="text-slate-500 hover:text-rose-400 p-1.5 rounded-lg border border-slate-850 hover:border-rose-900/30 hover:bg-rose-950/10 transition-all flex items-center gap-1.5"
                            title="Delete voice template"
                            id="btn-trigger-deletion-panel"
                          >
                            <Trash2 className="w-3.5 h-3.5" />
                            <span className="text-[10px] font-mono">Purge Profile</span>
                          </button>
                        </div>

                        {/* Interactive testing and verification panel */}
                        <div className="mt-6 border-t border-slate-850/60 pt-5 space-y-4">
                          <div className="flex justify-between items-center text-xs">
                            <span className="font-sans font-semibold text-slate-200">Authenticate Biometric Reference</span>
                            <span className="font-mono text-[10px] text-slate-500">Verify matched phase & jitter</span>
                          </div>

                          {isVerifying ? (
                            <div className="bg-slate-950/60 border border-slate-850 p-5 rounded-2xl space-y-4">
                              <div className="space-y-1 bg-slate-950 p-4 rounded-xl border border-slate-900">
                                <span className="text-[9px] font-mono text-slate-500 block uppercase">challenge phrase</span>
                                <p className="font-sans text-base font-medium text-slate-200 tracking-tight leading-relaxed">
                                  &ldquo;{selectedVerificationChallenge}&rdquo;
                                </p>
                              </div>

                              {/* Ambient Noise Level Policy check feedback during verification */}
                              {(simulatedNoise || (audio.ambientNoiseDb > policy.noiseThresholdDb && audio.ambientNoiseDb > -90)) && (
                                <div className="bg-amber-500/10 border border-amber-500/20 p-3 rounded-xl flex gap-2.5 text-amber-400 text-xs leading-relaxed animate-fade-in" id="verification-noise-warning">
                                  <AlertTriangle className="w-4.5 h-4.5 shrink-0 text-amber-500 mt-0.5" />
                                  <div>
                                    <strong className="text-amber-300 font-sans block">Potential Rejection: Excessive Ambient Noise</strong>
                                    <p className="text-slate-400 mt-0.5 text-[11px]">
                                      Background floor of <span className="text-amber-300 font-mono font-bold">{Math.round(simulatedNoise ? -35 : audio.ambientNoiseDb)} dB</span> exceeds strict safety policies ({policy.noiseThresholdDb} dB). Move to a quieter area.
                                    </p>
                                  </div>
                                </div>
                              )}

                              <div className="flex justify-between items-center">
                                <span className="text-xs text-slate-400 font-mono flex items-center gap-1">
                                  <span className="h-1.5 w-1.5 rounded-full bg-indigo-500 animate-ping" />
                                  <span>{verificationStage === 'recording' ? 'Capture mode live...' : 'Processing biometric formants...'}</span>
                                </span>
                                
                                {verificationStage === 'recording' ? (
                                  <button
                                    type="button"
                                    onClick={handleStopAndProcessVerification}
                                    className="bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-sans font-bold text-xs py-1.5 px-4 rounded-lg transition-colors flex items-center gap-1.5"
                                    id="btn-verification-capture-stop"
                                  >
                                    <Square className="w-3.5 h-3.5" />
                                    <span>Analyze Voice</span>
                                  </button>
                                ) : (
                                  <div className="flex items-center gap-1.5 text-xs text-indigo-400 font-mono">
                                    <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                                    <span>Verifier processing</span>
                                  </div>
                                )}
                              </div>
                            </div>
                          ) : (
                            <div className="bg-slate-950/20 border border-slate-850/60 p-4 rounded-2xl flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
                              <p className="text-xs text-slate-400 leading-normal max-w-sm font-sans">
                                Perform a physical voice authentication query. SentryVoice will parse and match acoustic criteria, presenting a signed cryptographic token.
                              </p>
                              <button
                                type="button"
                                onClick={handleStartVerification}
                                className="w-full sm:w-auto bg-slate-800 hover:bg-slate-750 text-indigo-300 font-sans font-semibold text-xs py-2 px-4 rounded-xl border border-slate-700/80 transition-all flex items-center justify-center gap-1.5 shrink-0"
                                id="btn-authenticate-voice"
                              >
                                <Mic className="w-3.5 h-3.5 text-indigo-400" />
                                <span>Sign In with Voice</span>
                              </button>
                            </div>
                          )}
                        </div>

                        {/* Interactive Sandbox Test controllers */}
                        {isVerifying && (
                          <div className="bg-slate-950 border border-slate-850 p-4 rounded-2xl mt-4 space-y-2">
                            <div className="flex justify-between items-center">
                              <span className="text-[10px] font-mono text-slate-400 uppercase tracking-widest font-bold">Inject Failure Sandbox</span>
                              <span className="text-[9px] bg-slate-900 border border-slate-850 text-slate-500 px-2 py-0.5 rounded">developer block</span>
                            </div>
                            <div className="grid grid-cols-3 gap-2">
                              <button
                                type="button"
                                onClick={() => setSimulatedSpoof(simulatedSpoof === 'replay' ? 'none' : 'replay')}
                                className={`py-1.5 px-2 text-[10px] font-mono rounded border transition-colors ${
                                  simulatedSpoof === 'replay'
                                    ? 'bg-amber-500/10 border-amber-500/40 text-amber-400'
                                    : 'bg-slate-900 border-slate-800 text-slate-500 hover:text-slate-400'
                                }`}
                                id="btn-inject-replay"
                              >
                                Replay Signature
                              </button>
                              <button
                                type="button"
                                onClick={() => setSimulatedSpoof(simulatedSpoof === 'synthetic' ? 'none' : 'synthetic')}
                                className={`py-1.5 px-2 text-[10px] font-mono rounded border transition-colors ${
                                  simulatedSpoof === 'synthetic'
                                    ? 'bg-rose-500/10 border-rose-500/40 text-rose-400'
                                    : 'bg-slate-900 border-slate-800 text-slate-500 hover:text-slate-400'
                                }`}
                                id="btn-inject-deepfake"
                              >
                                Deepfake Attack
                              </button>
                              <button
                                type="button"
                                onClick={() => setSimulatedNoise(!simulatedNoise)}
                                className={`py-1.5 px-2 text-[10px] font-mono rounded border transition-colors ${
                                  simulatedNoise
                                    ? 'bg-indigo-500/10 border-indigo-500/40 text-indigo-400'
                                    : 'bg-slate-900 border-slate-800 text-slate-500 hover:text-slate-400'
                                }`}
                                id="btn-inject-noise"
                              >
                                Ambient Noise
                              </button>
                            </div>
                          </div>
                        )}

                        {/* Enrolled metadata details list */}
                        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs pt-5 mt-5 border-t border-slate-850">
                          <div>
                            <span className="text-slate-500 font-mono text-[10px] block uppercase">MODEL VERSION</span>
                            <span className="font-mono text-slate-200 block font-semibold mt-0.5">{profile.modelId}</span>
                          </div>
                          <div>
                            <span className="text-slate-500 font-mono text-[10px] block uppercase">DATA STORAGE BOUND</span>
                            <span className="font-mono text-emerald-400 block font-semibold mt-0.5">Isolated US-EAST-1</span>
                          </div>
                          <div>
                            <span className="text-slate-500 font-mono text-[10px] block uppercase">TEMPLATE RESOLUTION</span>
                            <span className="font-mono text-slate-200 block font-semibold mt-0.5">AES-256 Vector</span>
                          </div>
                          <div>
                            <span className="text-slate-500 font-mono text-[10px] block uppercase">CONSENT STATUS</span>
                            <span className="font-sans text-emerald-400 block font-semibold mt-0.5">Signed Disclosure</span>
                          </div>
                        </div>
                      </div>

                      {/* Deletion panel display conditionally */}
                      {profile.deletionStatus !== 'none' && (
                        <BiometricDeletionStatus
                          status={profile.deletionStatus}
                          txHash={profile.deletionTxHash}
                          requestTime={profile.deletionRequestTime}
                          onInitiateDelete={handleInitiateDeletion}
                          onResetStatus={handleResetDeletionStatus}
                        />
                      )}
                    </div>
                  )}
                </motion.div>
              )}

              {/* Enrollment Wizard step renderer */}
              {wizardStep === 'consent' && (
                <motion.div
                  key="vbm-consent-step"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  transition={{ duration: 0.25 }}
                >
                  <VoiceConsentRecord
                    onConsentGranted={handleConsentGranted}
                    onConsentDeclined={() => setWizardStep('idle')}
                    initialSignerName=""
                  />
                </motion.div>
              )}

              {wizardStep === 'preflight' && (
                <motion.div
                  key="vbm-preflight-step"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  transition={{ duration: 0.25 }}
                >
                  <MicrophonePreflight
                    permission={audio.permission}
                    isRecording={audio.isRecording}
                    volume={audio.audioStats.volume}
                    db={audio.audioStats.db}
                    onRequestPermission={audio.requestPermission}
                    onRunNoiseTest={() => audio.runNoisePreflight(2500)}
                    noiseLevel={audio.ambientNoiseDb}
                    noiseThreshold={policy.noiseThresholdDb}
                    onPreflightComplete={handlePreflightCompleted}
                    onBack={() => setWizardStep('consent')}
                  />
                </motion.div>
              )}

              {wizardStep === 'recording' && (
                <motion.div
                  key="vbm-recording-step"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  transition={{ duration: 0.25 }}
                >
                  <RecordingControl
                    isRecording={audio.isRecording}
                    audioStats={audio.audioStats}
                    promptText={ENROLLMENT_CHALLENGES[enrollmentIndex]}
                    onStartRecord={audio.startRecording}
                    onStopRecord={audio.stopRecording}
                    currentStep={enrollmentIndex + 1}
                    totalSteps={ENROLLMENT_CHALLENGES.length}
                    onSampleCompleted={handleSampleSaved}
                    onSimulateSpoof={() => setSimulatedSpoof(simulatedSpoof === 'replay' ? 'none' : 'replay')}
                    onSimulateNoise={() => setSimulatedNoise(!simulatedNoise)}
                    onResetStep={() => {
                      audio.stopRecording();
                      setWizardStep('idle');
                    }}
                    ambientNoiseDb={audio.ambientNoiseDb}
                    noiseThreshold={policy.noiseThresholdDb}
                    simulatedNoise={simulatedNoise}
                  />

                  {/* Wizard development feedback block */}
                  <div className="bg-slate-900/30 border border-slate-850 p-4 rounded-xl max-w-2xl mx-auto mt-4 text-[10px] font-mono text-slate-500 leading-normal flex gap-2">
                    <Info className="w-4 h-4 text-indigo-400 shrink-0 mt-0.5" />
                    <span>
                      Active Simulation parameters: Spoof Injection is {simulatedSpoof.toUpperCase()} | High Noise is {simulatedNoise ? 'TRUE' : 'FALSE'}. 
                      Saving this sample with simulated errors will trigger matching verifier reject blocks.
                    </span>
                  </div>
                </motion.div>
              )}

              {wizardStep === 'complete' && (
                <motion.div
                  key="vbm-complete-step"
                  initial={{ opacity: 0, scale: 0.98 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.98 }}
                  transition={{ duration: 0.25 }}
                  className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-xl mx-auto p-8 space-y-6 text-center"
                >
                  <div className="h-16 w-16 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-full flex items-center justify-center mx-auto shadow-inner animate-bounce">
                    <ShieldCheck className="w-8 h-8" />
                  </div>
                  
                  <div className="space-y-2">
                    <h3 className="font-sans font-bold text-slate-100 text-2xl">Acoustic Templates Generated</h3>
                    <p className="text-sm text-slate-400">
                      Congratulations! Your physical voice biometric profile has been successfully integrated into the secure SentryVoice regional directory.
                    </p>
                  </div>

                  <div className="bg-slate-950 rounded-xl p-4 border border-slate-850 text-left space-y-3">
                    <div className="flex items-center gap-2 text-xs font-mono text-indigo-400">
                      <Award className="w-4 h-4" />
                      <span>Security Passport Envelope</span>
                    </div>
                    <ul className="text-xs text-slate-300 space-y-2 list-disc pl-5 font-sans leading-normal">
                      <li>Three distinct challenge phrases successfully analyzed and vectorized.</li>
                      <li>Signed Privacy & Compliance Disclosure version {profile.consentVersion} logged.</li>
                      <li>Acoustic sandboxing cleared under BIPA security guidelines.</li>
                    </ul>
                  </div>

                  <button
                    type="button"
                    onClick={() => setWizardStep('idle')}
                    className="w-full bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-sans font-bold text-xs py-2.5 rounded-lg transition-all"
                    id="btn-wizard-complete-acknowledge"
                  >
                    Enter Identity Portal
                  </button>
                </motion.div>
              )}

            </AnimatePresence>
          )}

          {activeTab === 'admin' && (
            <AdminPolicyPanel
              policy={policy}
              verifier={verifier}
              onSavePolicy={handleUpdatePolicy}
              onSaveVerifier={handleUpdateVerifier}
            />
          )}

          {activeTab === 'diagnostics' && (
            <DiagnosticsDashboard
              summary={diagnostics}
              logs={auditLogs}
              onClearLogs={handleClearAuditLogs}
            />
          )}

          {/* Active Evidence Log JWT Overlay Modal */}
          <AnimatePresence>
            {activeEvidence && (
              <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
                <motion.div
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                  className="w-full max-w-xl"
                >
                  <LivenessEvidenceSummary
                    amrToken={activeEvidence.amrToken}
                    livenessClass={activeEvidence.livenessClass}
                    confidenceScore={activeEvidence.confidenceScore}
                    timeFreshnessMs={activeEvidence.timeFreshnessMs}
                    nonce={activeEvidence.nonce}
                    onClose={() => setActiveEvidence(null)}
                  />
                </motion.div>
              </div>
            )}
          </AnimatePresence>

        </div>

        {/* Right Area (Live Telemetry & Telehealth Status Widgets) - 5 Columns */}
        <div className="lg:col-span-5 space-y-6">
          
          {/* Active Configuration Quick Peek Widget */}
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-4">
            <div>
              <h4 className="font-sans font-semibold text-slate-300 text-xs uppercase tracking-wider">Active Directory State</h4>
              <p className="text-[10px] text-slate-500 mt-0.5">Biometric configuration overview</p>
            </div>

            <div className="space-y-2.5">
              {/* Profile status item */}
              <div className="flex justify-between items-center text-xs bg-slate-950/40 p-3 rounded-xl border border-slate-850/60 font-mono">
                <span className="text-slate-500">PROV_STATUS</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  profile.status === 'enrolled' 
                    ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                    : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                }`}>
                  {profile.status.toUpperCase()}
                </span>
              </div>

              {/* Confidence threshold item */}
              <div className="flex justify-between items-center text-xs bg-slate-950/40 p-3 rounded-xl border border-slate-850/60 font-mono">
                <span className="text-slate-500">MATCH_THRESHOLD</span>
                <span className="text-indigo-300 font-semibold">{policy.minConfidence}% Probability</span>
              </div>

              {/* Liveness enforce item */}
              <div className="flex justify-between items-center text-xs bg-slate-950/40 p-3 rounded-xl border border-slate-850/60 font-mono">
                <span className="text-slate-500">LIVENESS_AUDIT</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  policy.strictLiveness 
                    ? 'bg-indigo-500/10 text-indigo-400 border border-indigo-500/20' 
                    : 'bg-slate-800 text-slate-400'
                }`}>
                  {policy.strictLiveness ? 'STRICT' : 'PASSIVE'}
                </span>
              </div>

              {/* Verifier status item */}
              <div className="flex justify-between items-center text-xs bg-slate-950/40 p-3 rounded-xl border border-slate-850/60 font-mono">
                <span className="text-slate-500">API_HEALTH_NODE</span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                  verifier.healthStatus === 'healthy' 
                    ? 'bg-emerald-500/10 text-emerald-400' 
                    : 'bg-amber-500/10 text-amber-400'
                }`}>
                  {verifier.healthStatus.toUpperCase()}
                </span>
              </div>
            </div>
          </div>

          {/* Real-time WebAudio Visual Spectrogram Node Indicator widget */}
          <div className="bg-slate-900 border border-slate-800 rounded-3xl p-5 shadow-xl space-y-4">
            <div>
              <h4 className="font-sans font-semibold text-slate-300 text-xs uppercase tracking-wider">Acoustic Sandbox Terminal</h4>
              <p className="text-[10px] text-slate-500 mt-0.5">Isolated hardware connection channel</p>
            </div>

            <div className="bg-slate-950 p-4 rounded-2xl border border-slate-850/80 space-y-3 text-xs">
              <div className="flex items-center gap-2.5">
                <div className={`h-2.5 w-2.5 rounded-full ${audio.permission === 'granted' ? 'bg-emerald-500 animate-pulse' : 'bg-rose-500'}`} />
                <div className="font-mono flex-1">
                  <span className="text-slate-400 block font-semibold">
                    {audio.permission === 'granted' ? 'Microphone Active' : 'Microphone Access Required'}
                  </span>
                  <span className="text-[10px] text-slate-500 block mt-0.5">
                    {audio.permission === 'granted' ? 'WebAudio PCM API streaming | 128 channels' : 'OS permission query pending...'}
                  </span>
                </div>
              </div>

              {audio.permission === 'granted' && (
                <div className="border-t border-slate-900 pt-3 space-y-2 font-mono text-[10px] text-slate-400">
                  <div className="flex justify-between">
                    <span>Acoustic Amplitude</span>
                    <span className="text-slate-300 font-semibold">
                      {audio.isRecording ? `${Math.round(audio.audioStats.volume)}%` : 'Silent'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Signal Decibels</span>
                    <span className="text-slate-300 font-semibold">
                      {audio.isRecording ? `${Math.round(audio.audioStats.db)} dB` : '-100 dB'}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span>Voice Frequency Range</span>
                    <span className="text-slate-300 font-semibold">
                      {audio.isRecording ? '85Hz - 255Hz (Vocal)' : 'Unsampled'}
                    </span>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Regulatory & BIPA Disclosure Badge */}
          <div className="bg-slate-950/40 border border-slate-900 rounded-2xl p-4 text-[10px] text-slate-500 leading-normal font-sans space-y-1.5">
            <span className="font-mono text-slate-400 uppercase tracking-wider block font-semibold">compliance enforcement notice</span>
            <p>
              This console fully conforms to the regulatory boundaries established by the Illinois Biometric Information Privacy Act (BIPA) 740 ILCS 14/, 
              GDPR Article 17, and California CCPA guidelines. 
              The private key for the verifier resides in the sovereign KMS key cabinet.
            </p>
          </div>

        </div>

      </main>

      {/* Footer */}
      <footer className="bg-slate-900 border-t border-slate-800 text-center py-5 mt-auto font-mono text-[10px] text-slate-500">
        <p>&copy; 2026 SentryVoice Systems, Inc. GCP Regional Instance | US-EAST-1 Iowa Node. TLS 1.3 AES-256-GCM.</p>
      </footer>
    </div>
  );
}
