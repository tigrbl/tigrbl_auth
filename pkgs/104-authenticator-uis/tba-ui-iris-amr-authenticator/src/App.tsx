import { useState, useEffect, useRef } from 'react';
import { 
  Shield, 
  Eye, 
  Settings, 
  Activity, 
  CheckCircle2, 
  AlertTriangle, 
  RefreshCw, 
  Trash2, 
  Lock, 
  UserCheck, 
  Key, 
  Info, 
  Sliders, 
  SlidersHorizontal,
  X, 
  ChevronRight, 
  RotateCcw, 
  UserX, 
  LockKeyhole, 
  Globe, 
  FileText, 
  Server, 
  Fingerprint, 
  Camera, 
  Zap, 
  Terminal,
  Clock
} from 'lucide-react';

import { 
  BiometricConsent, 
  IrisEnrollmentStatus, 
  IrisAuthStatus, 
  IrisEnrollmentState, 
  IrisAuthState, 
  BiometricPolicy, 
  ProviderConfig, 
  AuditLogRecord, 
  SimulatorSettings 
} from './types';

import { 
  DEFAULT_POLICY, 
  INITIAL_PROVIDERS, 
  INITIAL_AUDIT_LOGS 
} from './mockData';

import { 
  BiometricService,
  MockBiometricService, 
  ProductionBiometricService 
} from './services/BiometricService';

export default function App() {
  // State management
  const [activeTab, setActiveTab] = useState<'auth' | 'lifecycle' | 'policy' | 'health'>('auth');
  const [policy, setPolicy] = useState<BiometricPolicy>(DEFAULT_POLICY);
  const [providers, setProviders] = useState<ProviderConfig[]>(INITIAL_PROVIDERS);
  const [auditLogs, setAuditLogs] = useState<AuditLogRecord[]>(INITIAL_AUDIT_LOGS);
  
  // Dual-mode state & camera controls
  const [operationMode, setOperationMode] = useState<'demo' | 'production'>('demo');
  const [cameraStream, setCameraStream] = useState<MediaStream | null>(null);

  // Consent record state
  const [consent, setConsent] = useState<BiometricConsent>({
    accepted: false,
    version: '2.4.0',
    signedAt: undefined,
    withdrawnAt: undefined,
  });

  // Deletion Queue / Job monitor
  const [deletionQueue, setDeletionQueue] = useState<{
    id: string;
    templateRef: string;
    status: 'pending' | 'completed' | 'failed' | 'manual-review';
    requestedAt: string;
    auditRef: string;
  }[]>([
    {
      id: 'DEL-88129',
      templateRef: 'iris_t_9281_old',
      status: 'completed',
      requestedAt: '2026-07-15T08:10:00-07:00',
      auditRef: 'TX-93650'
    }
  ]);

  // Simulator configurations
  const [simSettings, setSimSettings] = useState<SimulatorSettings>({
    alignmentPerfect: true,
    gazeAligned: true,
    lightingOptimal: true,
    livenessGenuine: true,
    deviceConnected: true,
    providerOutage: false,
  });

  // Active Authenticated user state in Demo App
  const [currentUser, setCurrentUser] = useState<{
    subjectId: string;
    isEnrolled: boolean;
    isActive: boolean;
    isSuspended: boolean;
    hasStepUpCompleted: boolean;
    authenticatedSessions: Array<{
      time: string;
      amr: string;
      provenance: string;
      trust: string;
      auditRef: string;
    }>;
  }>({
    subjectId: 'user_subject_9281',
    isEnrolled: true,
    isActive: true,
    isSuspended: false,
    hasStepUpCompleted: false,
    authenticatedSessions: [
      {
        time: '2026-07-15T10:25:31-07:00',
        amr: 'iris',
        provenance: 'first-party:IrisLink',
        trust: 'high',
        auditRef: 'TX-94021'
      }
    ]
  });

  // P0 Authentication Ceremony states
  const [authCeremony, setAuthCeremony] = useState<IrisAuthState>({
    status: 'idle',
    challengeNonce: '',
    purpose: 'Standard login verification',
    progress: 0,
    gazeAligned: true,
    eyeDetected: true,
    livenessChecked: false,
    attemptsLeft: 3,
  });

  // P1 Enrollment Ceremony states
  const [enrollState, setEnrollState] = useState<IrisEnrollmentState>({
    status: 'unregistered',
    currentStep: 0, // 0: Introduction, 1: Preflight, 2: Capture, 3: Review/Activation
    samplesCollected: 0,
    maxSamples: 5,
    gazeAligned: true,
    calibrationProgress: 0,
    qualityScore: 0,
    livenessVerified: false,
  });

  // Steps in enrollment capture guide
  const gazeDirectives = [
    'Look directly into the glowing center ring',
    'Follow the cursor to the Top-Left quadrant',
    'Follow the cursor to the Top-Right quadrant',
    'Gaze down at the Bottom-Center dot',
    'Hold steady - Finalizing 3D iris map depth'
  ];

  // Helper to append log entries
  const appendAuditLog = (action: string, outcome: 'success' | 'failure' | 'warning', evidence: string, provenance: string, details: string) => {
    const txId = `TX-${Math.floor(10000 + Math.random() * 90000)}`;
    const newLog: AuditLogRecord = {
      id: txId,
      timestamp: new Date().toISOString(),
      actor: currentUser.subjectId,
      action,
      outcome,
      evidenceType: evidence,
      provenance,
      detailsRedacted: details,
    };
    setAuditLogs(prev => [newLog, ...prev]);
    return txId;
  };

  // WebRTC camera helper functions
  const startCamera = async () => {
    if (cameraStream) return cameraStream;
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: { ideal: 400 }, height: { ideal: 400 }, facingMode: "user" }
      });
      setCameraStream(stream);
      return stream;
    } catch (err: any) {
      console.error("Camera access denied or unavailable", err);
      setOperationMode('demo');
      alert("Camera Access Denied or Video Device Missing: Production mode requires camera stream access. Reverting to Simulated Demo Mode.");
      return null;
    }
  };

  const stopCamera = () => {
    if (cameraStream) {
      cameraStream.getTracks().forEach(track => {
        track.stop();
        console.log(`[Camera stream] Released track: ${track.label}`);
      });
      setCameraStream(null);
    }
  };

  // Manage WebRTC camera life-cycles based on ceremony state and mode selection
  useEffect(() => {
    const isAuthActive = ['connecting', 'ready', 'gaze_alignment', 'capturing', 'processing'].includes(authCeremony.status);
    const isEnrollActive = ['preflight', 'capturing'].includes(enrollState.status);
    
    if (operationMode === 'production' && (isAuthActive || isEnrollActive)) {
      startCamera();
    } else {
      stopCamera();
    }

    return () => {
      // Intentionally empty cleanup
    };
  }, [operationMode, authCeremony.status, enrollState.status]);

  // Switch tabs & trigger reset behaviors
  const handleTabChange = (tab: 'auth' | 'lifecycle' | 'policy' | 'health') => {
    setActiveTab(tab);
    resetAuthCeremony();
    if (enrollState.status !== 'activated' && enrollState.status !== 'unregistered') {
      setEnrollState(prev => ({ ...prev, status: 'unregistered', currentStep: 0 }));
    }
    stopCamera();
  };

  const resetAuthCeremony = () => {
    setAuthCeremony({
      status: 'idle',
      challengeNonce: '',
      purpose: 'Standard login verification',
      progress: 0,
      gazeAligned: true,
      eyeDetected: true,
      livenessChecked: false,
      attemptsLeft: 3,
    });
    stopCamera();
  };

  // Simulation / Service effect for P0 Authentication
  useEffect(() => {
    let interval: any = null;
    const service: BiometricService = operationMode === 'demo' ? new MockBiometricService() : new ProductionBiometricService();

    if (authCeremony.status === 'connecting') {
      const duration = 1200;
      const step = 200;
      let elapsed = 0;
      interval = setInterval(() => {
        elapsed += step;
        if (elapsed >= duration) {
          clearInterval(interval);
          if (operationMode === 'demo' && !simSettings.deviceConnected) {
            setAuthCeremony(prev => ({
              ...prev,
              status: 'disconnected',
              errorMessage: 'Hardware connection lost. Please check specialized USB-C sensor or switch to alternative verification.'
            }));
            appendAuditLog('BIOMETRIC_VERIFICATION_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', 'Device disconnect during initial handshake pre-check.');
          } else if (operationMode === 'demo' && simSettings.providerOutage) {
            setAuthCeremony(prev => ({
              ...prev,
              status: 'blocked',
              errorMessage: 'Verification provider reporting fatal server-side response error. Code: 503 Service Unavailable.'
            }));
            appendAuditLog('BIOMETRIC_VERIFICATION_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', 'Provider outage triggered. Remote verification API unreachable.');
          } else {
            setAuthCeremony(prev => ({
              ...prev,
              status: 'ready',
              progress: 0
            }));
          }
        }
      }, step);
    } else if (authCeremony.status === 'ready') {
      const timer = setTimeout(() => {
        setAuthCeremony(prev => ({
          ...prev,
          status: 'gaze_alignment'
        }));
      }, 1000);
      return () => clearTimeout(timer);
    } else if (authCeremony.status === 'gaze_alignment') {
      interval = setInterval(async () => {
        if (operationMode === 'demo' && !simSettings.deviceConnected) {
          setAuthCeremony(prev => ({
            ...prev,
            status: 'disconnected',
            errorMessage: 'Sensor disconnected during gaze alignment ceremony.'
          }));
          appendAuditLog('BIOMETRIC_VERIFICATION_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', 'Specialized device abruptly disconnected during gaze alignment step.');
          clearInterval(interval);
          return;
        }

        const videoElem = document.getElementById('auth-video-feed') as HTMLVideoElement;
        const alignResult = await service.checkGazeAlignment(videoElem, simSettings);
        
        if (alignResult.aligned) {
          clearInterval(interval);
          setAuthCeremony(prev => ({
            ...prev,
            status: 'capturing',
            progress: 10
          }));
        }
      }, 500);
    } else if (authCeremony.status === 'capturing') {
      interval = setInterval(async () => {
        if (operationMode === 'demo' && !simSettings.deviceConnected) {
          setAuthCeremony(prev => ({
            ...prev,
            status: 'disconnected',
            errorMessage: 'Sensor disconnected during biometric capture.'
          }));
          clearInterval(interval);
          return;
        }

        const videoElem = document.getElementById('auth-video-feed') as HTMLVideoElement;
        const lightingResult = await service.measureLighting(videoElem, simSettings);

        setAuthCeremony(prev => {
          const nextProgress = prev.progress + 15;
          if (nextProgress >= 100) {
            clearInterval(interval);
            return {
              ...prev,
              progress: 100,
              status: 'processing'
            };
          }
          return {
            ...prev,
            progress: nextProgress,
            gazeAligned: simSettings.gazeAligned,
            eyeDetected: simSettings.alignmentPerfect,
            errorMessage: lightingResult.lightingOptimal ? undefined : lightingResult.message
          };
        });
      }, 350);
    } else if (authCeremony.status === 'processing') {
      const timer = setTimeout(async () => {
        const videoElem = document.getElementById('auth-video-feed') as HTMLVideoElement;
        const verifyResult = await service.verifyMatch(authCeremony.challengeNonce, authCeremony.purpose, videoElem, simSettings);

        if (!verifyResult.success) {
          const updatedAttempts = authCeremony.attemptsLeft - 1;
          let nextStatus: IrisAuthStatus = 'idle';
          
          if (verifyResult.errorType === 'spoof') {
            nextStatus = updatedAttempts <= 0 ? 'blocked' : 'spoof_detected';
          } else if (verifyResult.errorType === 'disconnect') {
            nextStatus = 'disconnected';
          } else if (verifyResult.errorType === 'outage') {
            nextStatus = 'blocked';
          } else {
            nextStatus = updatedAttempts <= 0 ? 'blocked' : 'retry_needed';
          }

          setAuthCeremony(prev => ({
            ...prev,
            status: nextStatus,
            attemptsLeft: updatedAttempts,
            errorMessage: verifyResult.message
          }));

          appendAuditLog(
            'BIOMETRIC_VERIFICATION_ATTEMPT', 
            'failure', 
            'iris', 
            operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink(Production)', 
            `Verification failed: ${verifyResult.message}. Attempts left: ${updatedAttempts}.`
          );
        } else {
          // Success!
          const auditRef = appendAuditLog(
            'BIOMETRIC_VERIFICATION_ATTEMPT', 
            'success', 
            'iris', 
            operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink(Production)', 
            verifyResult.message
          );
          
          setAuthCeremony(prev => ({
            ...prev,
            status: 'success',
            progress: 100,
            acceptedEvidence: verifyResult.evidence ? {
              ...verifyResult.evidence,
              auditReference: auditRef
            } : {
              amr: 'iris',
              source: 'first-party',
              provenance: operationMode === 'demo' ? 'first-party:IrisLink (USB-C Biometric Sensor)' : 'first-party:IrisLink (Live Optical WebRTC Capture)',
              verifiedAt: new Date().toISOString(),
              trustProfile: 'high',
              livenessResultClass: 'PRESENTATION_ATTACK_DETECTION_PASS',
              ceremonyPurpose: prev.purpose,
              auditReference: auditRef
            }
          }));

          setCurrentUser(prev => ({
            ...prev,
            hasStepUpCompleted: true,
            authenticatedSessions: [
              {
                time: new Date().toISOString(),
                amr: 'iris',
                provenance: operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink (Live Optical)',
                trust: 'high',
                auditRef
              },
              ...prev.authenticatedSessions
            ]
          }));
        }
      }, 1500);
      return () => clearTimeout(timer);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [authCeremony.status, simSettings, operationMode]);

  // Simulation / Service effect for P1 Enrollment
  useEffect(() => {
    let interval: any = null;
    const service = operationMode === 'demo' ? new MockBiometricService() : new ProductionBiometricService();
    
    if (enrollState.status === 'preflight') {
      service.calibrateDevice((progress) => {
        setEnrollState(prev => {
          if (progress >= 100) {
            return {
              ...prev,
              calibrationProgress: 100,
              status: 'capturing',
              currentStep: 2
            };
          }
          return {
            ...prev,
            calibrationProgress: progress,
            gazeAligned: simSettings.gazeAligned
          };
        });
      }, simSettings).catch((err) => {
        setEnrollState(prev => ({
          ...prev,
          status: 'unregistered',
          currentStep: 0,
          retryReason: err.message
        }));
      });
    } else if (enrollState.status === 'capturing') {
      interval = setInterval(async () => {
        if (operationMode === 'demo' && !simSettings.deviceConnected) {
          setEnrollState(prev => ({
            ...prev,
            status: 'unregistered',
            retryReason: 'Preflight failure: Dedicated sensor was unplugged during template acquisition.'
          }));
          appendAuditLog('BIOMETRIC_ENROLLMENT_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', 'Sensor disconnect during template enrollment capture.');
          clearInterval(interval);
          return;
        }

        if (operationMode === 'demo' && !simSettings.livenessGenuine) {
          setEnrollState(prev => ({
            ...prev,
            status: 'unregistered',
            retryReason: 'Liveness validation failed: Presentation attack detected by specialized hardware sensors.'
          }));
          appendAuditLog('BIOMETRIC_ENROLLMENT_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', 'Presentation attack blocking triggered during sample acquisition.');
          clearInterval(interval);
          return;
        }

        const videoElem = document.getElementById('enroll-video-feed') as HTMLVideoElement;
        try {
          const sampleResult = await service.captureSample(enrollState.samplesCollected, videoElem, simSettings);
          
          if (!sampleResult.livenessOk) {
            setEnrollState(prev => ({
              ...prev,
              status: 'unregistered',
              retryReason: `Liveness validation failed: ${sampleResult.feedback}`
            }));
            appendAuditLog('BIOMETRIC_ENROLLMENT_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', `Presentation attack blocking: ${sampleResult.feedback}`);
            clearInterval(interval);
            return;
          }

          if (sampleResult.qualityScore < 50) {
            setEnrollState(prev => ({
              ...prev,
              gazeAligned: false,
              retryReason: sampleResult.feedback
            }));
            return;
          }

          setEnrollState(prev => {
            const nextSamples = prev.samplesCollected + 1;
            const isComplete = nextSamples >= prev.maxSamples;
            
            if (isComplete) {
              clearInterval(interval);
              return {
                ...prev,
                samplesCollected: prev.maxSamples,
                status: 'analyzing',
                retryReason: undefined
              };
            }

            return {
              ...prev,
              samplesCollected: nextSamples,
              qualityScore: sampleResult.qualityScore,
              retryReason: undefined
            };
          });

        } catch (err: any) {
          setEnrollState(prev => ({
            ...prev,
            status: 'unregistered',
            retryReason: `Acquisition interrupted: ${err.message}`
          }));
          appendAuditLog('BIOMETRIC_ENROLLMENT_ATTEMPT', 'failure', 'none', 'first-party:IrisLink', `Sensor exception: ${err.message}`);
          clearInterval(interval);
        }
      }, 1200);
    } else if (enrollState.status === 'analyzing') {
      const timer = setTimeout(async () => {
        const compiled = await service.compileTemplate(currentUser.subjectId);

        setEnrollState(prev => ({
          ...prev,
          status: 'activated',
          currentStep: 3,
          qualityScore: compiled.qualityScore,
          livenessVerified: true
        }));
        
        const auditRef = appendAuditLog(
          'BIOMETRIC_ENROLLMENT_COMPLETE',
          'success',
          'iris',
          operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink(Production)',
          `First-party biometric template compiled (Reference ID: ${compiled.templateRef}). Signature keys synchronized in hardware storage.`
        );

        setCurrentUser(prev => ({
          ...prev,
          isEnrolled: true,
          isActive: true,
          isSuspended: false
        }));

        setConsent(prev => ({
          ...prev,
          signedAt: new Date().toISOString()
        }));

        if (compiled.publicKeyPem) {
          console.log('%c[Iris AMR Cryptographic Credentials Created]', 'color: #14b8a6; font-weight: bold;');
          console.log(compiled.publicKeyPem);
        }
      }, 2000);
      return () => clearTimeout(timer);
    }

    return () => {
      if (interval) clearInterval(interval);
    };
  }, [enrollState.status, simSettings, operationMode]);

  // Handle enrollment button start click
  const startEnrollmentFlow = () => {
    if (!consent.accepted) {
      alert('Informed consent is a hard requirement before biometric device preflight triggers. Please accept the policy agreement.');
      return;
    }
    setEnrollState({
      status: 'preflight',
      currentStep: 1,
      samplesCollected: 0,
      maxSamples: 5,
      gazeAligned: simSettings.gazeAligned,
      calibrationProgress: 0,
      qualityScore: 0,
      livenessVerified: false,
    });
    appendAuditLog(
      'BIOMETRIC_ENROLLMENT_START', 
      'success', 
      'none', 
      operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink(Production)', 
      'Informed consent signed. Preflight sensor calibration test initiated.'
    );
  };

  // Handle first-party biometric login start click
  const startFirstPartyAuth = async () => {
    if (!currentUser.isEnrolled) {
      alert('Subject has no registered first-party iris biometric templates. Please enroll in the Lifecycle tab first.');
      return;
    }
    if (currentUser.isSuspended) {
      alert('Biometric access has been suspended for this subject. Please resume the credential first.');
      return;
    }
    
    setAuthCeremony(prev => ({
      ...prev,
      status: 'connecting',
      attemptsLeft: 3,
      progress: 0
    }));

    try {
      const service: BiometricService = operationMode === 'demo' ? new MockBiometricService() : new ProductionBiometricService();
      const initResult = await service.initializeAuth(authCeremony.purpose);
      
      setAuthCeremony(prev => ({
        ...prev,
        challengeNonce: initResult.challengeNonce
      }));

      appendAuditLog(
        'BIOMETRIC_VERIFICATION_START', 
        'success', 
        'none', 
        operationMode === 'demo' ? 'first-party:IrisLink' : 'first-party:IrisLink(Production)', 
        `Device handshake initialized. Challenge Bound Nonce: ${initResult.challengeNonce}`
      );
    } catch (err: any) {
      setAuthCeremony(prev => ({
        ...prev,
        status: 'idle',
        errorMessage: err.message
      }));
    }
  };

  // Handle federated login emulation
  const startFederatedLogin = () => {
    setAuthCeremony(prev => ({
      ...prev,
      status: 'connecting',
      purpose: 'Federated single sign-on transformation',
      progress: 5
    }));
    
    appendAuditLog('FEDERATED_REDIRECT', 'success', 'none', 'federated:EyeID', 'Federated login redirected to EyeID trusted authority.');

    setTimeout(() => {
      if (simSettings.providerOutage) {
        setAuthCeremony(prev => ({
          ...prev,
          status: 'blocked',
          errorMessage: 'The federated identity provider is currently unreachable. Error Code: EyeID-1002.'
        }));
        appendAuditLog('FEDERATED_CALLBACK', 'failure', 'none', 'federated:EyeID', 'Callback validation failed due to remote identity provider server outage.');
      } else {
        const auditRef = appendAuditLog(
          'FEDERATED_CALLBACK', 
          'success', 
          'iris', 
          'federated:EyeID', 
          'Received signed callback from EyeID. Transformed iris evidence validated. No raw data exposure.'
        );
        
        setAuthCeremony(prev => ({
          ...prev,
          status: 'success',
          acceptedEvidence: {
            amr: 'iris',
            source: 'federated',
            provenance: 'federated:EyeID (Transformed Biometric Token)',
            verifiedAt: new Date().toISOString(),
            trustProfile: 'medium',
            livenessResultClass: 'ASSERTION_PRESENTATION_ATTACK_PASS',
            ceremonyPurpose: 'Federated single sign-on transformation',
            auditReference: auditRef
          }
        }));

        setCurrentUser(prev => ({
          ...prev,
          authenticatedSessions: [
            {
              time: new Date().toISOString(),
              amr: 'iris',
              provenance: 'federated:EyeID',
              trust: 'medium',
              auditRef
            },
            ...prev.authenticatedSessions
          ]
        }));
      }
    }, 2000);
  };

  // Lifecycle actions
  const toggleSuspension = () => {
    const isSuspending = !currentUser.isSuspended;
    setCurrentUser(prev => ({
      ...prev,
      isSuspended: isSuspending
    }));
    
    appendAuditLog(
      isSuspending ? 'BIOMETRIC_TEMPLATE_SUSPEND' : 'BIOMETRIC_TEMPLATE_RESUME',
      'success',
      'iris',
      'first-party:IrisLink',
      `Subject manually ${isSuspending ? 'suspended' : 're-activated'} biometric verification access permissions.`
    );
  };

  const withdrawConsentAndQueueDeletion = () => {
    setConsent(prev => ({
      ...prev,
      accepted: false,
      withdrawnAt: new Date().toISOString()
    }));

    const auditRef = appendAuditLog(
      'BIOMETRIC_CONSENT_WITHDRAWAL',
      'success',
      'none',
      'system',
      'Subject withdrew iris biometric processing consent. Asynchronous deletion pipeline scheduled immediately.'
    );

    // Queue erasure job
    const newJob = {
      id: `DEL-${Math.floor(10000 + Math.random() * 90000)}`,
      templateRef: 'iris_t_9281_active',
      status: 'pending' as const,
      requestedAt: new Date().toISOString(),
      auditRef
    };
    
    setDeletionQueue(prev => [newJob, ...prev]);

    // Simulate completion of asynchronous deletion
    setTimeout(() => {
      setDeletionQueue(prev => 
        prev.map(job => {
          if (job.id === newJob.id) {
            appendAuditLog(
              'BIOMETRIC_TEMPLATE_DELETION_COMPLETE',
              'success',
              'iris',
              'first-party:IrisLink',
              `Deletion job ${job.id} completed. Subject iris template reference definitively cleared from database cluster.`
            );
            return { ...job, status: 'completed' as const };
          }
          return job;
        })
      );
      
      setCurrentUser(prev => ({
        ...prev,
        isEnrolled: false,
        isActive: false
      }));

      setEnrollState(prev => ({
        ...prev,
        status: 'unregistered',
        currentStep: 0
      }));
    }, 4000);
  };

  const startRetraining = () => {
    appendAuditLog(
      'BIOMETRIC_RETRAIN_REQUEST',
      'success',
      'none',
      'first-party:IrisLink',
      'Retraining initiated. Existing template preserved in memory until new registration is completed successfully.'
    );
    // Open registration window immediately
    setActiveTab('lifecycle');
    setEnrollState({
      status: 'preflight',
      currentStep: 1,
      samplesCollected: 0,
      maxSamples: 5,
      gazeAligned: simSettings.gazeAligned,
      calibrationProgress: 0,
      qualityScore: 0,
      livenessVerified: false,
    });
  };

  // Admin config changes
  const handlePolicyChange = (field: keyof BiometricPolicy, value: any) => {
    setPolicy(prev => ({
      ...prev,
      [field]: value
    }));
    
    appendAuditLog(
      'BIOMETRIC_POLICY_UPDATE',
      'warning',
      'none',
      'system',
      `Security policy parameter updated: [${field}] changed to ${JSON.stringify(value)}`
    );
  };

  const handleProviderToggle = (id: string) => {
    setProviders(prev => prev.map(p => {
      if (p.id === id) {
        const nextStatus = p.status === 'active' ? 'suspended' : 'active';
        appendAuditLog(
          'PROVIDER_TRUST_UPDATE',
          nextStatus === 'suspended' ? 'warning' : 'success',
          'none',
          'system',
          `Provider status for ${p.name} updated to ${nextStatus}`
        );
        return { ...p, status: nextStatus };
      }
      return p;
    }));
  };

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans selection:bg-teal-500/30 selection:text-teal-200" id="main-container">
      
      {/* Upper Navigation & Branding Header */}
      <header className="border-b border-slate-900 bg-slate-950/80 backdrop-blur-md sticky top-0 z-40 px-6 py-4 flex flex-col md:flex-row items-center justify-between gap-4" id="app-header">
        <div className="flex items-center gap-3">
          <div className="bg-teal-950/50 border border-teal-500/30 p-2 rounded-xl text-teal-400 shadow-lg shadow-teal-950/20">
            <Eye className="w-6 h-6 animate-pulse" id="header-eye-icon" />
          </div>
          <div>
            <div className="flex items-center gap-2">
              <span className="text-xs tracking-widest font-mono text-teal-500 uppercase font-semibold">AMR VERIFIER</span>
              <span className="text-slate-500 text-xs font-mono">• v1.4-active</span>
            </div>
            <h1 className="text-lg font-bold text-slate-100 tracking-tight" id="app-title">iris-authenticator-portal</h1>
          </div>
        </div>

        {/* Status Indicators & Mode Toggle */}
        <div className="flex flex-wrap items-center gap-4 text-xs font-mono">
          {/* Mode Switcher */}
          <div className="flex items-center gap-1.5 bg-slate-900/90 border border-teal-500/30 p-1 rounded-xl shadow-inner">
            <button
              onClick={() => {
                setOperationMode('demo');
                appendAuditLog('MODE_SWITCH', 'warning', 'none', 'system', 'Operator toggled operation mode to: [Simulated Demo]');
              }}
              className={`px-3 py-1.5 rounded-lg font-mono text-[11px] font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                operationMode === 'demo'
                  ? 'bg-teal-500 text-slate-950 shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
              id="mode-toggle-demo"
            >
              <Sliders className="w-3.5 h-3.5" />
              <span>Simulated Demo</span>
            </button>
            <button
              onClick={() => {
                setOperationMode('production');
                appendAuditLog('MODE_SWITCH', 'success', 'none', 'system', 'Operator toggled operation mode to: [Production Live (Live WebRTC)]');
              }}
              className={`px-3 py-1.5 rounded-lg font-mono text-[11px] font-bold transition-all flex items-center gap-1.5 cursor-pointer ${
                operationMode === 'production'
                  ? 'bg-gradient-to-r from-teal-400 to-emerald-500 text-slate-950 shadow-md'
                  : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/40'
              }`}
              id="mode-toggle-production"
            >
              <Zap className="w-3.5 h-3.5" />
              <span>Production Live</span>
            </button>
          </div>

          <div className="flex items-center gap-2 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
            <span className="text-slate-500">Biometric Template:</span>
            {currentUser.isEnrolled ? (
              currentUser.isSuspended ? (
                <span className="text-amber-500 font-semibold flex items-center gap-1">
                  <span className="w-2 h-2 rounded-full bg-amber-500 inline-block animate-ping"></span>
                  Suspended
                </span>
              ) : (
                <span className="text-emerald-400 font-semibold flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 inline-block"></span>
                  Active
                </span>
              )
            ) : (
              <span className="text-slate-500">Unenrolled</span>
            )}
          </div>

          <div className="flex items-center gap-2 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
            <span className="text-slate-500">Device Handshake:</span>
            {simSettings.deviceConnected ? (
              <span className="text-teal-400 font-semibold flex items-center gap-1">
                <span className="w-1.5 h-1.5 rounded-full bg-teal-400 inline-block"></span>
                Connected
              </span>
            ) : (
              <span className="text-red-400 font-semibold flex items-center gap-1 animate-pulse">
                Offline
              </span>
            )}
          </div>
        </div>
      </header>

      {/* Main Grid: Sandbox Sim + Main Interactive Shell */}
      <main className="flex-1 grid grid-cols-1 xl:grid-cols-12 gap-6 p-6 max-w-[1700px] w-full mx-auto" id="main-content-grid">
        
        {/* Left Column: Hardcore Hardware Sensor Simulator & Diagnostics Controller (xl:span-4) */}
        <section className="xl:col-span-4 bg-slate-900/40 border border-slate-900 rounded-2xl p-5 flex flex-col gap-6" id="simulator-section">
          <div className="flex items-center justify-between border-b border-slate-800/80 pb-3">
            <div className="flex items-center gap-2">
              <Sliders className="w-4 h-4 text-teal-400" />
              <h2 className="font-mono text-sm uppercase tracking-wider font-semibold text-slate-300">Biometric Hardware Simulator</h2>
            </div>
            <span className="text-[10px] px-2 py-0.5 rounded bg-slate-800 text-slate-400 font-mono">Sandbox Controller</span>
          </div>

          <p className="text-xs text-slate-400 leading-relaxed">
            Biometric iris verifications rely on custom hardware inputs. Toggle these environmental and sensor conditions to test how the UI adapts to fail-safes.
          </p>

          {/* SIMULATOR SWITCH CONTROLS */}
          <div className="flex flex-col gap-4 bg-slate-950/50 p-4 rounded-xl border border-slate-800/50">
            
            {/* Toggle 1: Connection */}
            <div className="flex items-center justify-between py-1">
              <div>
                <label className="text-xs font-mono font-medium text-slate-300 block">Sensor USB-C Connection</label>
                <span className="text-[10px] text-slate-500 block">Simulate physical cable status</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, deviceConnected: !p.deviceConnected }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.deviceConnected ? 'bg-teal-500' : 'bg-slate-800'}`}
                id="sim-toggle-connection"
                aria-label="Toggle sensor connection"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.deviceConnected ? 'translate-x-6' : ''}`} />
              </button>
            </div>

            {/* Toggle 2: Liveness/Presentation Attack */}
            <div className="flex items-center justify-between py-1 border-t border-slate-900 pt-3">
              <div>
                <label className="text-xs font-mono font-medium text-slate-300 block">Liveness Validation (Genuine)</label>
                <span className="text-[10px] text-slate-500 block">Disable to simulate a deepfake or high-resolution photo attack</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, livenessGenuine: !p.livenessGenuine }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.livenessGenuine ? 'bg-teal-500' : 'bg-rose-600'}`}
                id="sim-toggle-liveness"
                aria-label="Toggle liveness authenticity"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.livenessGenuine ? 'translate-x-6' : ''}`} />
              </button>
            </div>

            {/* Toggle 3: Gaze Alignment */}
            <div className="flex items-center justify-between py-1 border-t border-slate-900 pt-3">
              <div>
                <label className="text-xs font-mono font-medium text-slate-300 block">Gaze Correctly Centered</label>
                <span className="text-[10px] text-slate-500 block">Simulate looking away or head tilt</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, gazeAligned: !p.gazeAligned }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.gazeAligned ? 'bg-teal-500' : 'bg-amber-600'}`}
                id="sim-toggle-gaze"
                aria-label="Toggle gaze alignment"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.gazeAligned ? 'translate-x-6' : ''}`} />
              </button>
            </div>

            {/* Toggle 4: Camera Target Focus */}
            <div className="flex items-center justify-between py-1 border-t border-slate-900 pt-3">
              <div>
                <label className="text-xs font-mono font-medium text-slate-300 block">Optimal Lighting Condition</label>
                <span className="text-[10px] text-slate-500 block">Disable to simulate dark, shadowy space</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, lightingOptimal: !p.lightingOptimal }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.lightingOptimal ? 'bg-teal-500' : 'bg-amber-600'}`}
                id="sim-toggle-lighting"
                aria-label="Toggle optimal lighting"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.lightingOptimal ? 'translate-x-6' : ''}`} />
              </button>
            </div>

            {/* Toggle 5: Eye Detected */}
            <div className="flex items-center justify-between py-1 border-t border-slate-900 pt-3">
              <div>
                <label className="text-xs font-mono font-medium text-slate-300 block">Pupil Occlusion Protection</label>
                <span className="text-[10px] text-slate-500 block">Disable to simulate eyelids, eyelashes, or frames blocking scan</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, alignmentPerfect: !p.alignmentPerfect }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.alignmentPerfect ? 'bg-teal-500' : 'bg-slate-800'}`}
                id="sim-toggle-alignment"
                aria-label="Toggle pupil occlusion"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.alignmentPerfect ? 'translate-x-6' : ''}`} />
              </button>
            </div>

            {/* Toggle 6: Remote API Outage */}
            <div className="flex items-center justify-between py-1 border-t border-slate-900 pt-3">
              <div>
                <label className="text-xs font-mono font-medium text-red-400 block">Provider API Outage</label>
                <span className="text-[10px] text-slate-500 block">Simulate provider server crash (503)</span>
              </div>
              <button 
                onClick={() => setSimSettings(p => ({ ...p, providerOutage: !p.providerOutage }))}
                className={`w-12 h-6 rounded-full transition-colors relative ${simSettings.providerOutage ? 'bg-rose-500' : 'bg-slate-800'}`}
                id="sim-toggle-outage"
                aria-label="Toggle provider outage"
              >
                <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${simSettings.providerOutage ? 'translate-x-6' : ''}`} />
              </button>
            </div>
          </div>

          {/* SIMULATED HARDWARE READOUT STATE */}
          <div className="bg-slate-950/80 p-4 rounded-xl border border-slate-900 font-mono text-[11px] flex flex-col gap-2.5">
            <div className="text-xs font-bold text-slate-400 border-b border-slate-900 pb-1.5 flex items-center justify-between">
              <span>🔌 HARDWARE LOGS</span>
              <Activity className="w-3.5 h-3.5 text-teal-400 animate-pulse" />
            </div>

            <div className="grid grid-cols-2 gap-y-1.5 gap-x-2 text-slate-300">
              <span className="text-slate-500">USB-C Sensor ID:</span>
              <span className="text-right text-teal-400">IRIS-LINK-USB3922</span>
              
              <span className="text-slate-500">Liveness Target:</span>
              <span className={`text-right font-bold ${simSettings.livenessGenuine ? 'text-emerald-400' : 'text-rose-400 animate-pulse'}`}>
                {simSettings.livenessGenuine ? 'BIOMETRIC_GENUINE' : 'SPOOF_SIGNATURE_ALERT'}
              </span>

              <span className="text-slate-500">Lux Sensor Index:</span>
              <span className={`text-right ${simSettings.lightingOptimal ? 'text-slate-300' : 'text-amber-500'}`}>
                {simSettings.lightingOptimal ? '420 LUX (Optimal)' : '80 LUX (Insufficient)'}
              </span>

              <span className="text-slate-500">Pupil Alignment:</span>
              <span className={`text-right ${simSettings.gazeAligned ? 'text-emerald-400' : 'text-amber-400'}`}>
                {simSettings.gazeAligned ? 'X=0.012, Y=-0.004' : 'X=0.490, Y=0.312 (DRIFT)'}
              </span>

              <span className="text-slate-500">Obstruction Vector:</span>
              <span className={`text-right ${simSettings.alignmentPerfect ? 'text-emerald-500' : 'text-red-400'}`}>
                {simSettings.alignmentPerfect ? '0.00% (Clear)' : '42.80% (Occluded)'}
              </span>
            </div>

            <div className="mt-2 pt-2 border-t border-slate-900 flex justify-between text-[10px] text-slate-500">
              <span>LAST HARDWARE SCANNER RESET:</span>
              <span>10:32:46 UTC</span>
            </div>
          </div>

          {/* Quick Notice */}
          <div className="bg-blue-950/20 border border-blue-500/20 rounded-xl p-3 flex gap-2.5">
            <Info className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
            <div className="text-xs text-slate-400 leading-normal">
              <strong className="text-blue-300">Privacy Protection Mandate:</strong> Biometric samples, eye media feeds, raw match scores, or templates never leave the secure hardware verifier boundary. Only cryptographic signed match results are processed by the server payload.
            </div>
          </div>
        </section>

        {/* Right Column: Complete Tabs Panel (xl:span-8) */}
        <section className="xl:col-span-8 flex flex-col gap-6" id="interactive-shell-section">
          
          {/* Main Module Tabs Nav */}
          <nav className="flex bg-slate-900/60 p-1.5 rounded-xl border border-slate-900/80" aria-label="Main Tabs">
            <button
              onClick={() => handleTabChange('auth')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-3 text-xs md:text-sm font-mono tracking-wide uppercase font-semibold rounded-lg transition-all ${
                activeTab === 'auth' 
                  ? 'bg-slate-900 text-teal-400 border border-slate-800 shadow-md' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              id="tab-auth"
            >
              <LockKeyhole className="w-4 h-4" />
              <span>P0: Authenticate</span>
            </button>

            <button
              onClick={() => handleTabChange('lifecycle')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-3 text-xs md:text-sm font-mono tracking-wide uppercase font-semibold rounded-lg transition-all ${
                activeTab === 'lifecycle' 
                  ? 'bg-slate-900 text-teal-400 border border-slate-800 shadow-md' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              id="tab-lifecycle"
            >
              <UserCheck className="w-4 h-4" />
              <span>P1: User Lifecycle</span>
            </button>

            <button
              onClick={() => handleTabChange('policy')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-3 text-xs md:text-sm font-mono tracking-wide uppercase font-semibold rounded-lg transition-all ${
                activeTab === 'policy' 
                  ? 'bg-slate-900 text-teal-400 border border-slate-800 shadow-md' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              id="tab-policy"
            >
              <SlidersHorizontal className="w-4 h-4" />
              <span>P2: Policies</span>
            </button>

            <button
              onClick={() => handleTabChange('health')}
              className={`flex-1 flex items-center justify-center gap-2 py-3 px-3 text-xs md:text-sm font-mono tracking-wide uppercase font-semibold rounded-lg transition-all ${
                activeTab === 'health' 
                  ? 'bg-slate-900 text-teal-400 border border-slate-800 shadow-md' 
                  : 'text-slate-400 hover:text-slate-200'
              }`}
              id="tab-health"
            >
              <Activity className="w-4 h-4" />
              <span>P2: Diagnostics</span>
            </button>
          </nav>

          {/* TAB CONTENT: 1. P0 AUTHENTICATION CEREMONY */}
          {activeTab === 'auth' && (
            <div className="bg-slate-900/20 border border-slate-900 rounded-2xl p-6 flex flex-col gap-6 animate-fade-in" id="panel-auth">
              
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800/80 pb-4">
                <div>
                  <h3 className="text-lg font-bold text-slate-200">First-Party Biometric Authentication Ceremony</h3>
                  <p className="text-xs text-slate-400 mt-1">
                    Execute a step-up biometric check or federated callback verification using challenge-bound cryptographic handshakes.
                  </p>
                </div>
                <div className="flex items-center gap-2 shrink-0">
                  <span className="text-[10px] font-mono px-2 py-1 bg-slate-950 rounded text-slate-400 border border-slate-800">
                    Scope: {policy.applicationScope.toUpperCase()}
                  </span>
                  <span className="text-[10px] font-mono px-2 py-1 bg-slate-950 rounded text-slate-400 border border-slate-800">
                    Liveness Req: {policy.requireLiveness ? 'MANDATORY' : 'OPTIONAL'}
                  </span>
                </div>
              </div>

              {/* DEMO SELECTOR FOR TRANSACTION PURPOSE */}
              <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/40 grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="text-xs font-mono font-medium text-slate-400 block mb-1.5">Select Demo Transaction Type</label>
                  <select 
                    value={authCeremony.purpose} 
                    onChange={(e) => setAuthCeremony(prev => ({ ...prev, purpose: e.target.value }))}
                    disabled={authCeremony.status !== 'idle'}
                    className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500 font-medium"
                    id="auth-purpose-select"
                  >
                    <option value="Secure Corporate Identity login">Account Login Verification (1FA / 2FA)</option>
                    <option value="Authorize wire transfer of $250,000.00 USD to IBAN CH93...">High-Value Transaction Step-Up ($250,000 Transfer)</option>
                    <option value="Decrypt and unlock secure hardware-bound storage keys">Hardware-bound Storage Decryption Step-up</option>
                    <option value="Revoke primary biometric credential for subject_9281">Critical Administrative Override Safeguard</option>
                  </select>
                </div>

                <div>
                  <label className="text-xs font-mono font-medium text-slate-400 block mb-1.5">Assigned Challenge Nonce (Server State)</label>
                  <div className="flex items-center justify-between bg-slate-900 border border-slate-800 rounded-lg p-2.5 font-mono text-xs">
                    <span className="text-teal-400">
                      {authCeremony.challengeNonce || 'N/A - Nonce assigned at start'}
                    </span>
                    <span className="text-slate-600 text-[10px]">Ceremony Binding: SHA256</span>
                  </div>
                </div>
              </div>

              {/* CEREMONY WORKSPACE SHELL */}
              <div className="border border-slate-850 bg-slate-950/40 rounded-xl p-6 min-h-[380px] flex flex-col items-center justify-center relative overflow-hidden" id="auth-ceremony-shell">
                
                {/* 1. IDLE STATE VIEW */}
                {authCeremony.status === 'idle' && (
                  <div className="text-center max-w-md flex flex-col items-center gap-4 py-8">
                    <div className="w-16 h-16 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center text-teal-400">
                      <Lock className="w-8 h-8" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-200">Start Biometric Authenticator</h4>
                      <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                        In order to proceed, choose the iris authentication mode. Ensure your approved USB-C eye scanner or federated adapter is connected and ready.
                      </p>
                    </div>

                    <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 w-full mt-4">
                      {/* BUTTON: FIRST-PARTY SPECIALIZED IRIS SCANNER */}
                      <button
                        onClick={startFirstPartyAuth}
                        className="bg-gradient-to-r from-teal-500 to-emerald-600 hover:from-teal-400 hover:to-emerald-500 text-slate-950 py-3 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 shadow-lg shadow-teal-950/20 active:scale-95 transition-all cursor-pointer"
                        id="btn-use-first-party-iris"
                      >
                        <Eye className="w-4 h-4 text-slate-950" />
                        <span>Use First-Party Iris</span>
                      </button>

                      {/* BUTTON: FEDERATED ADAPTER */}
                      <button
                        onClick={startFederatedLogin}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 py-3 px-4 rounded-xl text-xs font-semibold flex items-center justify-center gap-2 active:scale-95 transition-all"
                        id="btn-use-federated"
                      >
                        <Globe className="w-4 h-4 text-slate-400" />
                        <span>Federated Adapter</span>
                      </button>
                    </div>

                    <p className="text-[11px] text-slate-500 font-mono mt-2">
                      Authentication requires pre-accepted Privacy Consent Profile v{consent.version}
                    </p>
                  </div>
                )}

                {/* 2. CONNECTING/PREPARING STATE VIEW */}
                {authCeremony.status === 'connecting' && (
                  <div className="text-center flex flex-col items-center gap-4 py-8">
                    <div className="w-16 h-16 rounded-full border-2 border-t-teal-400 border-slate-800 animate-spin flex items-center justify-center">
                      <Server className="w-6 h-6 text-teal-400" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-200 font-mono animate-pulse">Initializing Specialized Device Handshake...</h4>
                      <p className="text-xs text-slate-500 mt-2 font-mono">
                        Establishing secure channel endpoint. Exchanging session cryptographic challenge.
                      </p>
                    </div>
                  </div>
                )}

                {/* 3. READY STATE VIEW */}
                {authCeremony.status === 'ready' && (
                  <div className="text-center flex flex-col items-center gap-4 py-8 animate-fade-in">
                    <div className="w-16 h-16 rounded-full bg-teal-950/30 border border-teal-500/30 flex items-center justify-center text-teal-400">
                      <CheckCircle2 className="w-8 h-8 text-teal-400 animate-bounce" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-200">Interactive Secure Channel Connected</h4>
                      <p className="text-xs text-slate-400 mt-1 max-w-sm">
                        Purpose: <strong className="text-teal-400">{authCeremony.purpose}</strong>
                      </p>
                      <p className="text-xs text-slate-500 mt-2">
                        Calibration confirmed. Direct gaze at target on screen.
                      </p>
                    </div>
                  </div>
                )}

                {/* 4. GAZE ALIGNMENT AND CAPTURING VIEW */}
                {(authCeremony.status === 'gaze_alignment' || authCeremony.status === 'capturing' || authCeremony.status === 'processing') && (
                  <div className="w-full max-w-md flex flex-col items-center gap-6 py-4">
                    
                    {/* VISUAL COMPONENT: IrisAlignmentGuidance CSS Target Finder */}
                    <div className="relative w-40 h-40 rounded-full border border-slate-800 bg-slate-950 flex items-center justify-center overflow-hidden">
                      {operationMode === 'production' && cameraStream && (
                        <video
                          id="auth-video-feed"
                          ref={(el) => {
                            if (el && cameraStream && el.srcObject !== cameraStream) {
                              el.srcObject = cameraStream;
                              el.play().catch(err => console.log('Video play error', err));
                            }
                          }}
                          autoPlay
                          playsInline
                          muted
                          className="absolute inset-0 w-full h-full object-cover rounded-full opacity-60 z-0 scale-x-[-1]"
                        />
                      )}

                      {/* Scanning active laser line */}
                      {authCeremony.status === 'capturing' && (
                        <div className="absolute top-0 w-full h-1 bg-gradient-to-r from-transparent via-teal-400 to-transparent animate-[scan_2s_infinite] z-10" />
                      )}

                      {/* Processing spinning outer dial */}
                      {authCeremony.status === 'processing' && (
                        <div className="absolute inset-2 rounded-full border-2 border-dashed border-teal-400 animate-[spin_8s_linear_infinite]" />
                      )}

                      {/* Center Target Circular Rings */}
                      <div className="absolute inset-6 rounded-full border border-slate-800 flex items-center justify-center">
                        <div className="absolute inset-4 rounded-full border border-teal-500/20 flex items-center justify-center">
                          <div className={`w-12 h-12 rounded-full border transition-all duration-300 flex items-center justify-center ${
                            simSettings.gazeAligned ? 'border-teal-400/80 bg-teal-950/20' : 'border-amber-500/60 bg-amber-950/10'
                          }`}>
                            
                            {/* Inner Iris Dot */}
                            <div className={`w-4 h-4 rounded-full transition-transform duration-300 ${
                              simSettings.gazeAligned 
                                ? 'bg-teal-400 scale-100' 
                                : 'bg-amber-500 translate-x-2.5 translate-y-1.5 animate-pulse'
                            }`} />
                          </div>
                        </div>
                      </div>

                      {/* Dynamic Gaze Guide Pointer */}
                      {!simSettings.gazeAligned && (
                        <div className="absolute top-4 right-4 bg-amber-500/90 text-slate-950 font-mono text-[9px] px-1.5 py-0.5 rounded font-bold uppercase animate-bounce">
                          ALIGN EYE 🡵
                        </div>
                      )}

                      {/* Cryptographic Key overlay when processing */}
                      {authCeremony.status === 'processing' && (
                        <div className="absolute inset-0 bg-slate-950/80 flex items-center justify-center animate-fade-in text-center p-2">
                          <div className="font-mono text-[9px] text-teal-400 flex flex-col items-center gap-1">
                            <Key className="w-5 h-5 text-teal-400 animate-pulse" />
                            <span>COMPUTING MATCH</span>
                            <span className="text-[8px] text-slate-500">SHA256(challenge + T)</span>
                          </div>
                        </div>
                      )}
                    </div>

                    {/* TEXT DESCRIPTION / FEEDBACK */}
                    <div className="text-center w-full">
                      {authCeremony.status === 'gaze_alignment' && (
                        <div>
                          <span className="text-xs font-mono font-bold tracking-wider px-2 py-0.5 bg-amber-950/50 border border-amber-500/30 text-amber-400 rounded-full animate-pulse">
                            AWAITING ALIGNMENT
                          </span>
                          <h5 className="font-semibold text-slate-200 text-sm mt-3">Position Eyes within the Outer Ring</h5>
                          <p className="text-xs text-slate-400 mt-1">
                            {simSettings.gazeAligned 
                              ? 'Perfect gaze alignment detected. Starting optical capture...'
                              : 'Eyes out of bounding focus. Look directly into the lens sensor.'}
                          </p>
                        </div>
                      )}

                      {authCeremony.status === 'capturing' && (
                        <div>
                          <span className="text-xs font-mono font-bold tracking-wider px-2 py-0.5 bg-teal-950/50 border border-teal-500/30 text-teal-400 rounded-full">
                            CAPTURING FRESH SAMPLES...
                          </span>
                          <h5 className="font-semibold text-slate-200 text-sm mt-3">Hold Steady • Capturing Iris Features</h5>
                          <p className="text-xs text-slate-400 mt-1">
                            Evaluating biometric entropy arrays. Liveness presentation check running.
                          </p>

                          {/* Progress bar */}
                          <div className="w-48 bg-slate-900 border border-slate-800 rounded-full h-2 mx-auto mt-4 overflow-hidden">
                            <div 
                              className="bg-teal-500 h-full transition-all duration-300"
                              style={{ width: `${authCeremony.progress}%` }}
                            />
                          </div>
                        </div>
                      )}

                      {authCeremony.status === 'processing' && (
                        <div>
                          <span className="text-xs font-mono font-bold tracking-wider px-2 py-0.5 bg-teal-950/50 border border-teal-500/30 text-teal-400 rounded-full animate-pulse">
                            HARDWARE BOUND MATCHING
                          </span>
                          <h5 className="font-semibold text-slate-200 text-sm mt-3">Validating Signed Payload Proof</h5>
                          <p className="text-xs text-slate-400 mt-1">
                            Computing ephemeral template distance math & challenge sign-offs.
                          </p>
                        </div>
                      )}
                    </div>

                    {/* Safe error message feedback in processing window */}
                    {authCeremony.status === 'gaze_alignment' && !simSettings.gazeAligned && (
                      <div className="w-full bg-slate-900/60 p-3 rounded-lg border border-slate-800 text-center font-mono text-xs text-amber-500">
                        ⚠ SIMULATION ADVICE: Enable "Gaze Correctly Centered" toggle on the left hardware panel to continue.
                      </div>
                    )}
                  </div>
                )}

                {/* 5. SUCCESS STATE VIEW */}
                {authCeremony.status === 'success' && authCeremony.acceptedEvidence && (
                  <div className="w-full p-4 animate-fade-in flex flex-col items-center text-center gap-6">
                    <div className="w-14 h-14 rounded-full bg-emerald-950/40 border border-emerald-500 text-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-950/20">
                      <CheckCircle2 className="w-8 h-8" />
                    </div>

                    <div>
                      <h4 className="text-base font-bold text-slate-100">Biometric Verification Successful</h4>
                      <p className="text-xs text-emerald-400 font-mono mt-1">Status: iris AMR Claim Emitted (100% Assurance)</p>
                    </div>

                    {/* BiometricEvidenceQualifier Component */}
                    <div className="bg-slate-900/80 border border-slate-800 rounded-xl p-4 w-full text-left font-mono text-[11px] flex flex-col gap-2">
                      <div className="text-xs font-bold text-slate-300 border-b border-slate-800 pb-1.5 mb-1">
                        🔒 CRYPTOGRAPHIC EVIDENCE QUALIFIER
                      </div>
                      
                      <div className="grid grid-cols-2 gap-y-1">
                        <span className="text-slate-500">Evidence AMR:</span>
                        <span className="text-right text-emerald-400 font-semibold">{authCeremony.acceptedEvidence.amr.toUpperCase()}</span>

                        <span className="text-slate-500">Provenance / Source:</span>
                        <span className="text-right text-slate-300">{authCeremony.acceptedEvidence.provenance}</span>

                        <span className="text-slate-500">Ceremony Timestamp:</span>
                        <span className="text-right text-slate-300">{new Date(authCeremony.acceptedEvidence.verifiedAt).toLocaleTimeString()}</span>

                        <span className="text-slate-500">Liveness Profile:</span>
                        <span className="text-right text-teal-400 font-medium">{authCeremony.acceptedEvidence.livenessResultClass}</span>

                        <span className="text-slate-500">Trust Framework:</span>
                        <span className="text-right text-emerald-500 font-bold uppercase">{authCeremony.acceptedEvidence.trustProfile}</span>

                        <span className="text-slate-500">Ceremony Bind Nonce:</span>
                        <span className="text-right text-slate-400 text-[10px]">{authCeremony.challengeNonce}</span>

                        <span className="text-slate-500">Redacted Audit Log:</span>
                        <span className="text-right text-teal-500">{authCeremony.acceptedEvidence.auditReference}</span>
                      </div>
                    </div>

                    <div className="flex gap-3 mt-2">
                      <button 
                        onClick={resetAuthCeremony}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 px-4 py-2 rounded-lg text-xs font-semibold"
                        id="btn-auth-done"
                      >
                        Reset / Lock Screen
                      </button>
                    </div>
                  </div>
                )}

                {/* 6. RETRY STATE VIEW */}
                {authCeremony.status === 'retry_needed' && (
                  <div className="text-center max-w-sm flex flex-col items-center gap-4 py-8 animate-fade-in">
                    <div className="w-14 h-14 rounded-full bg-amber-950/30 border border-amber-500 text-amber-500 flex items-center justify-center">
                      <AlertTriangle className="w-7 h-7" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-200">Quality Check Rejected</h4>
                      <p className="text-xs text-amber-400 font-mono mt-1">REASON: {authCeremony.errorMessage}</p>
                      <p className="text-xs text-slate-400 mt-3 leading-relaxed">
                        To maintain high biometric security assurance, our server rejected the captured sample. Make sure your face is illuminated evenly.
                      </p>
                      <p className="text-xs text-slate-500 font-mono mt-2">
                        Remaining attempts before account lockout: <span className="text-red-400 font-bold">{authCeremony.attemptsLeft}</span>
                      </p>
                    </div>

                    <div className="flex gap-3 w-full mt-4">
                      <button
                        onClick={() => {
                          setAuthCeremony(prev => ({
                            ...prev,
                            status: 'gaze_alignment'
                          }));
                        }}
                        className="flex-1 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 py-2.5 rounded-lg text-xs font-semibold"
                        id="btn-retry-capture"
                      >
                        Try Capture Again
                      </button>
                      <button
                        onClick={resetAuthCeremony}
                        className="bg-slate-950 hover:bg-slate-900 text-slate-500 py-2.5 px-4 rounded-lg text-xs"
                        id="btn-cancel-retry"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {/* 7. SPOOF DETECTED STATE VIEW */}
                {authCeremony.status === 'spoof_detected' && (
                  <div className="text-center max-w-sm flex flex-col items-center gap-4 py-8 animate-fade-in">
                    <div className="w-14 h-14 rounded-full bg-rose-950/40 border border-rose-500 text-rose-500 flex items-center justify-center animate-bounce">
                      <UserX className="w-7 h-7" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-rose-400">Presentation Attack Suspicion Triggered</h4>
                      <p className="text-xs text-slate-400 mt-2">
                        Our specialized sensors detected irregular reflective physiological properties on the lens surface (e.g. photo print, high-resolution device projection, or non-human material).
                      </p>
                      <p className="text-xs text-rose-500 font-mono mt-2 font-bold uppercase tracking-wider">
                        SECURITY ALERT: ATTEMPT RECORDED & AUDITED
                      </p>
                      <p className="text-xs text-slate-500 font-mono mt-2">
                        Remaining attempts before authentication block: <span className="text-red-400 font-bold">{authCeremony.attemptsLeft}</span>
                      </p>
                    </div>

                    <div className="flex gap-3 w-full mt-4">
                      <button
                        onClick={() => {
                          setAuthCeremony(prev => ({
                            ...prev,
                            status: 'gaze_alignment'
                          }));
                        }}
                        className="flex-1 bg-rose-950/30 hover:bg-rose-950/50 border border-rose-500/40 text-rose-400 py-2.5 rounded-lg text-xs font-semibold"
                        id="btn-retry-spoof"
                      >
                        Retry Genuine Biometric
                      </button>
                      <button
                        onClick={resetAuthCeremony}
                        className="bg-slate-950 text-slate-500 py-2.5 px-4 rounded-lg text-xs"
                        id="btn-cancel-spoof"
                      >
                        Cancel
                      </button>
                    </div>
                  </div>
                )}

                {/* 8. DISCONNECTED STATE VIEW */}
                {authCeremony.status === 'disconnected' && (
                  <div className="text-center max-w-sm flex flex-col items-center gap-4 py-8 animate-fade-in">
                    <div className="w-14 h-14 rounded-full bg-slate-900 border border-slate-800 text-slate-400 flex items-center justify-center">
                      <AlertTriangle className="w-7 h-7 text-amber-500" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-slate-300">Biometric Sensor Unplugged</h4>
                      <p className="text-xs text-slate-400 mt-2 leading-relaxed">
                        The physical specialized hardware device was disconnected. Please check your connection or select a fallback verification credential.
                      </p>
                    </div>

                    <div className="flex flex-col gap-2 w-full mt-4">
                      <button
                        onClick={() => {
                          setAuthCeremony(prev => ({
                            ...prev,
                            status: 'connecting'
                          }));
                        }}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 py-2.5 rounded-lg text-xs font-semibold"
                        id="btn-reconnect-sensor"
                      >
                        Check Device Connection & Retry
                      </button>

                      <button
                        onClick={() => {
                          alert(`Invoking security policy fallback credential: [${policy.fallbackMethod}]. Proceeding...`);
                          appendAuditLog('FALLBACK_INVOKED', 'success', 'none', 'system', `Biometric unavailable. Switched subject fallback factor: [${policy.fallbackMethod}].`);
                          resetAuthCeremony();
                        }}
                        className="bg-slate-950 hover:bg-slate-900 text-teal-400 py-2 rounded-lg text-xs font-mono font-medium"
                        id="btn-fallback-trigger"
                      >
                        Use Fallback Method: {policy.fallbackMethod.toUpperCase()}
                      </button>
                    </div>
                  </div>
                )}

                {/* 9. BLOCKED / ACCOUNT LOCKOUT STATE VIEW */}
                {authCeremony.status === 'blocked' && (
                  <div className="text-center max-w-sm flex flex-col items-center gap-4 py-8 animate-fade-in">
                    <div className="w-14 h-14 rounded-full bg-red-950/40 border border-red-500 text-red-500 flex items-center justify-center">
                      <Lock className="w-7 h-7" />
                    </div>
                    <div>
                      <h4 className="text-base font-bold text-red-400">Authentication Verification Blocked</h4>
                      <p className="text-xs text-slate-300 mt-2 leading-relaxed">
                        {authCeremony.errorMessage || 'Maximum verification attempts exceeded.'} Access to security-critical transactions has been blocked on this device to protect your identity.
                      </p>
                      <p className="text-xs text-slate-500 font-mono mt-3">
                        Incident recorded under Audit ID: <span className="text-teal-500">TX-93988</span>
                      </p>
                    </div>

                    <button
                      onClick={() => {
                        resetAuthCeremony();
                        appendAuditLog('BIOMETRIC_BLOCKED_RESET', 'warning', 'none', 'system', 'Admin reset block flag on simulator console.');
                      }}
                      className="mt-4 bg-slate-900 hover:bg-slate-800 text-slate-300 border border-slate-800 py-2 px-4 rounded-lg text-xs font-semibold"
                      id="btn-reset-block"
                    >
                      Clear Security Block (Admin Demo Reset)
                    </button>
                  </div>
                )}

              </div>

              {/* TRANSACTIONS EVIDENCE HISTORY */}
              <div>
                <h4 className="text-xs font-mono font-bold uppercase text-slate-400 tracking-wider mb-3">
                  🔐 Active Session Context & Biometric Claims Log
                </h4>
                
                <div className="bg-slate-950/40 rounded-xl border border-slate-900 overflow-hidden">
                  <table className="w-full text-left border-collapse text-xs">
                    <thead>
                      <tr className="bg-slate-900 text-slate-500 font-mono border-b border-slate-850">
                        <th className="py-2.5 px-4 font-normal">Ceremony Time</th>
                        <th className="py-2.5 px-4 font-normal">Emitted AMR</th>
                        <th className="py-2.5 px-4 font-normal">Provenance Detail</th>
                        <th className="py-2.5 px-4 font-normal">Trust Level</th>
                        <th className="py-2.5 px-4 font-normal text-right">Redacted Audit Ref</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-900 font-mono text-[11px] text-slate-300">
                      {currentUser.authenticatedSessions.map((session, idx) => (
                        <tr key={idx} className="hover:bg-slate-900/40 transition-colors">
                          <td className="py-2.5 px-4 text-slate-500">
                            {new Date(session.time).toLocaleTimeString()}
                          </td>
                          <td className="py-2.5 px-4">
                            <span className="bg-teal-950/60 border border-teal-500/30 text-teal-400 px-2 py-0.5 rounded text-[10px] font-bold">
                              {session.amr.toUpperCase()}
                            </span>
                          </td>
                          <td className="py-2.5 px-4 font-sans text-slate-400">
                            {session.provenance}
                          </td>
                          <td className="py-2.5 px-4">
                            <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                              session.trust === 'high' 
                                ? 'bg-emerald-950/60 border border-emerald-500/30 text-emerald-400' 
                                : 'bg-slate-800 text-slate-300'
                            }`}>
                              {session.trust.toUpperCase()}
                            </span>
                          </td>
                          <td className="py-2.5 px-4 text-right text-teal-500">
                            {session.auditRef}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          )}

          {/* TAB CONTENT: 2. P1 ENROLLMENT AND LIFECYCLE */}
          {activeTab === 'lifecycle' && (
            <div className="bg-slate-900/20 border border-slate-900 rounded-2xl p-6 flex flex-col gap-6 animate-fade-in" id="panel-lifecycle">
              
              <div className="border-b border-slate-800/80 pb-4">
                <h3 className="text-lg font-bold text-slate-200">First-Party Biometric Enrollment & Lifecycle</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Manage user consents, calibrate specialized sensors, build 3D iris template hashes, and control account lifecycle status.
                </p>
              </div>

              {/* CURRENT TEMPLATE STATUS BANNER */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/60 flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 block">ENROLLMENT STATUS</span>
                    <strong className="text-base mt-1 block">
                      {currentUser.isEnrolled ? 'Registered Template' : 'Unregistered Subject'}
                    </strong>
                  </div>
                  <div className="mt-3">
                    {currentUser.isEnrolled ? (
                      <span className="inline-flex items-center gap-1 bg-emerald-950 text-emerald-400 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full border border-emerald-500/30">
                        ACTIVE REFERENCE
                      </span>
                    ) : (
                      <span className="inline-flex items-center gap-1 bg-slate-800 text-slate-400 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full">
                        NO TEMPLATE IN STORAGE
                      </span>
                    )}
                  </div>
                </div>

                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/60 flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 block">PRIVACY CONSENT RECORD</span>
                    <strong className="text-base mt-1 block">
                      {consent.accepted ? `Signed Version ${consent.version}` : 'Consent Withdrawn'}
                    </strong>
                  </div>
                  <div className="mt-3 text-xs text-slate-400 font-mono">
                    {consent.signedAt ? (
                      <span className="text-[10px]">Accepted: {new Date(consent.signedAt).toLocaleDateString()}</span>
                    ) : (
                      <span className="text-[10px] text-rose-400">Action Required</span>
                    )}
                  </div>
                </div>

                <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/60 flex flex-col justify-between">
                  <div>
                    <span className="text-[10px] font-mono text-slate-500 block">DELETION SCHEDULES</span>
                    <strong className="text-base mt-1 block">
                      {deletionQueue.filter(q => q.status === 'pending').length} Pending Jobs
                    </strong>
                  </div>
                  <div className="mt-3">
                    <span className="inline-flex items-center gap-1 bg-teal-950 text-teal-400 text-[10px] font-mono font-bold px-2.5 py-0.5 rounded-full">
                      ASYNC PIPELINE: COMPLIANT
                    </span>
                  </div>
                </div>
              </div>

              {/* THE ENROLLMENT FLOW CONTAINER */}
              <div className="bg-slate-950/40 border border-slate-900 rounded-xl p-5" id="enrollment-wizard-shell">
                
                <h4 className="text-sm font-semibold text-slate-300 border-b border-slate-900 pb-2 mb-4 flex items-center gap-2">
                  <Fingerprint className="w-4 h-4 text-teal-400" />
                  <span>Iris Biometric Registration Wizard</span>
                </h4>

                {/* Enrollment Step Indicator */}
                <div className="flex items-center gap-2 mb-6">
                  {['Informed Consent', 'Device Preflight', 'Optical Capture', 'Review & Register'].map((stepName, stepIdx) => (
                    <div key={stepIdx} className="flex-1 flex flex-col gap-1.5">
                      <div className={`h-1 rounded-full transition-colors duration-300 ${
                        enrollState.currentStep === stepIdx 
                          ? 'bg-teal-500' 
                          : enrollState.currentStep > stepIdx 
                            ? 'bg-teal-950 border border-teal-500/20' 
                            : 'bg-slate-800'
                      }`} />
                      <span className={`text-[10px] font-mono text-center tracking-tight hidden md:inline-block ${
                        enrollState.currentStep === stepIdx ? 'text-teal-400 font-semibold' : 'text-slate-500'
                      }`}>
                        {stepIdx + 1}. {stepName}
                      </span>
                    </div>
                  ))}
                </div>

                {/* STEP 0: ELIGIBILITY & CONSENT */}
                {enrollState.currentStep === 0 && (
                  <div className="space-y-4 animate-fade-in" id="enroll-step-consent">
                    <div className="bg-slate-950/80 p-4 rounded-lg border border-slate-900 space-y-3">
                      <h5 className="text-xs font-mono font-bold uppercase text-slate-400 flex items-center gap-2">
                        <FileText className="w-4 h-4 text-teal-500" />
                        <span>INFORMED BIOMETRIC PROCESSING CONSENT (v{consent.version})</span>
                      </h5>
                      
                      <div className="text-xs text-slate-400 leading-relaxed max-h-40 overflow-y-auto space-y-2 pr-2 font-sans border-b border-slate-900 pb-3">
                        <p>
                          <strong>1. Processing Boundaries:</strong> To register an Iris Authenticator credentials reference, specialized optical sensors inside your approved endpoint will capture and analyze the structural patterns of your iris. 
                        </p>
                        <p>
                          <strong>2. Ephemeral Processing:</strong> Raw photographic image frames of your eyes are processed strictly inside the local volatile hardware registers. Zero raw photographic pictures, video footage, or facial pictures are transmitted over networks or written to disk.
                        </p>
                        <p>
                          <strong>3. Template Storage & Erasure:</strong> The mathematical vector hash produced during template processing is stored cryptographically inside the secure system boundary. You can revoke or permanently withdraw consent and request template erasure at any time. Template deletion operations run asynchronously and clear all referencing records.
                        </p>
                        <p>
                          <strong>4. Jurisdiction & Accessible Fallbacks:</strong> Under biometric privacy guidelines (including BIPA and CCPA), alternative registration methods (e.g., standard FIDO Passkeys or physical TOTP hardware keys) are fully supported as equal security fallback alternatives.
                        </p>
                      </div>

                      {/* Consent Acceptance Checkbox */}
                      <div className="flex items-start gap-2.5 pt-2">
                        <input 
                          type="checkbox" 
                          id="consent-checkbox" 
                          checked={consent.accepted} 
                          onChange={(e) => {
                            setConsent(prev => ({
                              ...prev,
                              accepted: e.target.checked,
                              signedAt: e.target.checked ? new Date().toISOString() : undefined,
                              withdrawnAt: undefined
                            }));
                          }}
                          className="mt-1 accent-teal-500"
                        />
                        <label htmlFor="consent-checkbox" className="text-xs text-slate-300 font-medium select-none cursor-pointer">
                          I explicitly consent to the ephemeral acquisition of my iris biometric identifiers as outlined above. I understand that I can withdraw this authorization at any time.
                        </label>
                      </div>
                    </div>

                    <div className="flex justify-end gap-3 pt-2">
                      <button 
                        onClick={() => {
                          if (currentUser.isEnrolled) {
                            setActiveTab('auth');
                          } else {
                            alert('Subject has no active credentials to authenticate with.');
                          }
                        }}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-850 py-2.5 px-4 rounded-lg text-xs"
                      >
                        Cancel
                      </button>
                      <button
                        onClick={startEnrollmentFlow}
                        disabled={!consent.accepted}
                        className={`py-2.5 px-6 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                          consent.accepted 
                            ? 'bg-teal-500 text-slate-950 hover:bg-teal-400' 
                            : 'bg-slate-800 text-slate-500 cursor-not-allowed'
                        }`}
                        id="btn-consent-next"
                      >
                        <span>Begin Device Preflight</span>
                        <ChevronRight className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                )}

                {/* STEP 1: DEVICE PREFLIGHT */}
                {enrollState.currentStep === 1 && (
                  <div className="space-y-4 animate-fade-in" id="enroll-step-preflight">
                    <div className="bg-slate-950 p-4 rounded-lg border border-slate-900 flex flex-col items-center py-6 text-center">
                      <div className="w-12 h-12 rounded-full border border-teal-500/30 bg-teal-950/20 text-teal-400 flex items-center justify-center animate-spin">
                        <RefreshCw className="w-5 h-5" />
                      </div>
                      
                      <h5 className="font-semibold text-slate-200 text-sm mt-4">Running Specialized Biometric Sensor Diagnostics</h5>
                      <p className="text-xs text-slate-400 mt-1 max-w-sm">
                        Confirming device parameters, optical lens calibration arrays, physical connectivity, and workspace ambient light levels.
                      </p>

                      <div className="w-64 bg-slate-900 rounded-full h-1.5 mt-4 overflow-hidden border border-slate-800">
                        <div 
                          className="bg-teal-400 h-full transition-all duration-300"
                          style={{ width: `${enrollState.calibrationProgress}%` }}
                        />
                      </div>

                      <div className="mt-4 text-[10px] font-mono text-slate-500 flex justify-between w-64">
                        <span>CALIBRATING SENSOR:</span>
                        <span>{enrollState.calibrationProgress}% Complete</span>
                      </div>
                    </div>

                    <div className="bg-slate-900/40 p-3 rounded-lg border border-slate-800 text-xs text-slate-400 flex items-start gap-2">
                      <Info className="w-4 h-4 text-teal-400 shrink-0 mt-0.5" />
                      <span>
                        <strong>Calibration Guard:</strong> To pass preflight, ensure the physical USB-C sensor is placed 10-15cm from your face. Real-time calibration status can be altered on the left Hardware simulator panel.
                      </span>
                    </div>

                    <div className="flex justify-between items-center pt-2">
                      <button 
                        onClick={() => setEnrollState(p => ({ ...p, currentStep: 0 }))}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-850 py-2 px-4 rounded-lg text-xs"
                      >
                        Back
                      </button>
                      <div className="text-xs font-mono text-amber-500">
                        {!simSettings.deviceConnected && "⚠ Simulator: Device Disconnected. Connect device to pass preflight."}
                      </div>
                    </div>
                  </div>
                )}

                {/* STEP 2: OPTICAL CAPTURE */}
                {enrollState.currentStep === 2 && (
                  <div className="space-y-4 animate-fade-in" id="enroll-step-capture">
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      
                      {/* Left Side: Gaze targets */}
                      <div className="bg-slate-950 p-4 rounded-lg border border-slate-900 flex flex-col justify-between">
                        <div>
                          <span className="text-[10px] font-mono text-slate-500 block">GAZE DIRECTIVE TARGETS</span>
                          <h5 className="font-semibold text-slate-200 text-xs mt-1">Multi-angle sample synthesis</h5>
                          <p className="text-[11px] text-slate-400 mt-1.5 leading-relaxed">
                            To build a high-entropy 3D biometric template, look at the blinking indicators inside the viewfinder.
                          </p>
                        </div>

                        {/* Interactive dots representing multi-angle gaze shifting */}
                        <div className="my-4 py-4 flex items-center justify-center">
                          <div className="relative w-36 h-36 border border-slate-800 rounded-lg flex items-center justify-center bg-slate-950">
                            
                            {/* Direction guides */}
                            <div className={`absolute top-2 left-2 w-3.5 h-3.5 rounded-full border border-slate-800 transition-colors ${
                              enrollState.samplesCollected === 1 ? 'bg-teal-500 border-teal-400 animate-ping' : ''
                            }`} />
                            <div className={`absolute top-2 right-2 w-3.5 h-3.5 rounded-full border border-slate-800 transition-colors ${
                              enrollState.samplesCollected === 2 ? 'bg-teal-500 border-teal-400 animate-ping' : ''
                            }`} />
                            <div className={`absolute bottom-2 left-2 w-3.5 h-3.5 rounded-full border border-slate-800 transition-colors ${
                              enrollState.samplesCollected === 3 ? 'bg-teal-500 border-teal-400 animate-ping' : ''
                            }`} />
                            <div className={`absolute bottom-2 right-2 w-3.5 h-3.5 rounded-full border border-slate-800 transition-colors ${
                              enrollState.samplesCollected === 4 ? 'bg-teal-500 border-teal-400 animate-ping' : ''
                            }`} />

                            <div className={`w-8 h-8 rounded-full border-2 border-dashed flex items-center justify-center transition-all ${
                              enrollState.samplesCollected === 0 ? 'border-teal-400 animate-pulse' : 'border-slate-800'
                            }`}>
                              <div className={`w-3 h-3 rounded-full ${enrollState.samplesCollected === 0 ? 'bg-teal-400' : 'bg-slate-800'}`} />
                            </div>

                            <div className="absolute inset-0 flex items-center justify-center pointer-events-none text-slate-600 font-mono text-[8px] tracking-widest">
                              ALIGNMENT GRID
                            </div>
                          </div>
                        </div>

                        <div className="bg-slate-900 border border-slate-850 p-2.5 rounded text-center text-xs font-mono text-teal-400 font-bold">
                          {gazeDirectives[Math.min(enrollState.samplesCollected, gazeDirectives.length - 1)]}
                        </div>
                      </div>

                      {/* Right Side: Viewfinder progress & feedback */}
                      <div className="bg-slate-950 p-4 rounded-lg border border-slate-900 flex flex-col justify-between gap-4">
                        <div>
                          <span className="text-[10px] font-mono text-slate-500 block">ACQUISITION STATUS</span>
                          <h5 className="font-bold text-slate-200 text-xs mt-1">Acquiring Secure Local Hashes</h5>
                        </div>

                        {/* Visual Eye Bounding box */}
                        <div className="relative border border-slate-800 bg-slate-950 rounded-lg p-4 flex flex-col items-center justify-center text-center py-6 min-h-[140px] overflow-hidden">
                          {operationMode === 'production' && cameraStream ? (
                            <video
                              id="enroll-video-feed"
                              ref={(el) => {
                                if (el && cameraStream && el.srcObject !== cameraStream) {
                                  el.srcObject = cameraStream;
                                  el.play().catch(err => console.log('Video play error', err));
                                }
                              }}
                              autoPlay
                              playsInline
                              muted
                              className="absolute inset-0 w-full h-full object-cover opacity-50 z-0 scale-x-[-1]"
                            />
                          ) : (
                            <Camera className="w-8 h-8 text-slate-700 mb-1 relative z-10" />
                          )}
                          <div className="font-mono text-[10px] text-slate-500 relative z-10">
                            {operationMode === 'production' ? 'LIVE OPTICAL VIDEO FEED' : 'SPECIALIZED RAW INTERFACE ONLY'}
                          </div>
                          
                          {/* Live Samples counter */}
                          <div className="mt-4 flex gap-1.5">
                            {Array.from({ length: enrollState.maxSamples }).map((_, sIdx) => (
                              <div 
                                key={sIdx} 
                                className={`w-6 h-1.5 rounded-sm transition-colors ${
                                  sIdx < enrollState.samplesCollected 
                                    ? 'bg-teal-500' 
                                    : 'bg-slate-800'
                                }`} 
                              />
                            ))}
                          </div>
                          
                          <div className="mt-2 text-[10px] font-mono text-slate-400">
                            Captured: {enrollState.samplesCollected} / {enrollState.maxSamples} verified frames
                          </div>
                        </div>

                        {/* Warning logs */}
                        {enrollState.retryReason ? (
                          <div className="bg-amber-950/30 border border-amber-500/20 text-amber-500 p-2.5 rounded text-[10px] font-mono flex items-start gap-1.5 leading-normal">
                            <AlertTriangle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                            <span>{enrollState.retryReason}</span>
                          </div>
                        ) : (
                          <div className="bg-slate-900 p-2.5 rounded text-[10px] font-mono text-slate-400">
                            Quality assessment running. Minimum acceptable entropy rating: &gt;90%
                          </div>
                        )}
                      </div>

                    </div>

                    <div className="flex justify-between items-center pt-2">
                      <button 
                        onClick={() => {
                          setEnrollState(p => ({ ...p, status: 'unregistered', currentStep: 0 }));
                          appendAuditLog('BIOMETRIC_ENROLLMENT_CANCEL', 'warning', 'none', 'first-party:IrisLink', 'Subject cancelled biometric registration mid-stream.');
                        }}
                        className="bg-slate-900 hover:bg-slate-800 text-slate-400 border border-slate-850 py-2 px-4 rounded-lg text-xs"
                      >
                        Cancel Enrollment
                      </button>
                      <div className="text-[10px] font-mono text-slate-500 animate-pulse">
                        EPHEMERAL RAM BUFFER ENCRYPTED (AES-256-GCM)
                      </div>
                    </div>
                  </div>
                )}

                {/* STEP 3: REVIEW & ACTIVATION */}
                {enrollState.currentStep === 3 && (
                  <div className="space-y-4 animate-fade-in" id="enroll-step-review">
                    <div className="bg-slate-950 p-5 rounded-lg border border-slate-900 text-center flex flex-col items-center">
                      <div className="w-14 h-14 rounded-full bg-emerald-950/40 border border-emerald-500 text-emerald-400 flex items-center justify-center">
                        <CheckCircle2 className="w-8 h-8" />
                      </div>

                      <h5 className="font-bold text-slate-200 text-base mt-4">Biometric Registration Succeeded</h5>
                      <p className="text-xs text-slate-400 mt-1 max-w-sm">
                        Your first-party iris authenticator credential has been activated. The compiled template reference is registered to your identity.
                      </p>

                      <div className="bg-slate-900 border border-slate-850 rounded-xl p-4 w-full max-w-md text-left font-mono text-[10px] mt-4 space-y-1 text-slate-300">
                        <div className="text-xs font-bold text-slate-400 border-b border-slate-850 pb-1 mb-2">
                          📋 CRYPTOGRAPHIC METADATA EXPORT
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Subject Tenant Reference:</span>
                          <span>iris_sub_9281_prod</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Credential Template ID:</span>
                          <span className="text-teal-400">iris_t_9281_active (AES-GCM Signed)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Security Target AMR Vector:</span>
                          <span className="text-emerald-400 font-bold">["iris", "liveness_pad"]</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Assurance Class Level:</span>
                          <span className="text-emerald-400 uppercase">Level 3 (High)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Enrolled Quality Entropy Score:</span>
                          <span className="text-slate-200">98.4% (Excellent)</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-500">Consent Profile Version:</span>
                          <span>v{consent.version}</span>
                        </div>
                      </div>
                    </div>

                    <div className="flex justify-end gap-3 pt-2">
                      <button 
                        onClick={() => {
                          setEnrollState(p => ({ ...p, status: 'unregistered', currentStep: 0 }));
                          setActiveTab('auth');
                        }}
                        className="bg-gradient-to-r from-teal-500 to-emerald-600 text-slate-950 hover:from-teal-400 hover:to-emerald-500 font-semibold py-2.5 px-6 rounded-lg text-xs"
                      >
                        Proceed to Login Ceremony
                      </button>
                    </div>
                  </div>
                )}

              </div>

              {/* USER CREDENTIAL LIFECYCLE MANAGEMENT PANEL */}
              <div className="bg-slate-950/40 border border-slate-900 rounded-xl p-5" id="lifecycle-actions-shell">
                <h4 className="text-sm font-semibold text-slate-300 border-b border-slate-900 pb-2 mb-4">
                  👤 Active Template Lifecycle Controls & Compliance Queue
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                  
                  {/* Left Column: Direct Action Buttons */}
                  <div className="space-y-4">
                    <p className="text-xs text-slate-400 leading-normal">
                      Under biometric regulations, credential holders must retain full lifecycle control over their template. Actions below take effect instantly across authorization boundaries.
                    </p>

                    <div className="flex flex-wrap gap-3">
                      {/* ACTION 1: SUSPEND / RESUME */}
                      {currentUser.isEnrolled && (
                        <button
                          onClick={toggleSuspension}
                          className={`py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
                            currentUser.isSuspended 
                              ? 'bg-amber-600 text-white hover:bg-amber-500' 
                              : 'bg-slate-900 hover:bg-slate-800 text-amber-500 border border-slate-800'
                          }`}
                          id="btn-suspend-toggle"
                        >
                          <AlertTriangle className="w-4 h-4" />
                          <span>{currentUser.isSuspended ? 'Resume Template Use' : 'Suspend Template Access'}</span>
                        </button>
                      )}

                      {/* ACTION 2: RETRAIN / REPLACE */}
                      {currentUser.isEnrolled && (
                        <button
                          onClick={startRetraining}
                          className="bg-slate-900 hover:bg-slate-800 text-slate-200 border border-slate-800 py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-1.5"
                          id="btn-trigger-retrain"
                        >
                          <RefreshCw className="w-4 h-4 text-teal-400" />
                          <span>Retrain / Replace Scan</span>
                        </button>
                      )}

                      {/* ACTION 3: DELETION AND WITHDRAWAL */}
                      {currentUser.isEnrolled && (
                        <button
                          onClick={withdrawConsentAndQueueDeletion}
                          className="bg-rose-950/40 hover:bg-rose-950/60 text-rose-400 border border-rose-500/30 py-2 px-4 rounded-lg text-xs font-semibold flex items-center gap-1.5"
                          id="btn-withdraw-consent"
                        >
                          <Trash2 className="w-4 h-4" />
                          <span>Withdraw Consent & Delete</span>
                        </button>
                      )}
                    </div>

                    {!currentUser.isEnrolled && (
                      <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800 text-center py-6">
                        <UserX className="w-8 h-8 text-slate-600 mx-auto mb-2" />
                        <h5 className="font-bold text-slate-400 text-xs">No active templates found for subject_9281</h5>
                        <p className="text-[11px] text-slate-500 mt-1 max-w-xs mx-auto">
                          Complete the Informed Consent process above to authorize sensor capture and enroll a new biometric template reference.
                        </p>
                      </div>
                    )}
                  </div>

                  {/* Right Column: Compliant Deletion Queue Status */}
                  <div className="bg-slate-950/80 p-4 rounded-lg border border-slate-900/80 flex flex-col gap-3">
                    <div className="flex items-center justify-between border-b border-slate-900 pb-2">
                      <span className="text-xs font-mono font-bold text-slate-300 uppercase">
                        🧹 Erasure Compliance Job Log
                      </span>
                      <span className="text-[9px] px-1.5 py-0.5 rounded bg-emerald-950 border border-emerald-500/20 text-emerald-400 font-mono">
                        CCPA/BIPA Standard
                      </span>
                    </div>

                    <div className="space-y-3 max-h-48 overflow-y-auto pr-1">
                      {deletionQueue.map((job) => (
                        <div key={job.id} className="bg-slate-900 border border-slate-850 p-2.5 rounded flex items-center justify-between text-xs font-mono">
                          <div>
                            <div className="flex items-center gap-1.5 font-bold">
                              <span className="text-slate-400">Job: {job.id}</span>
                              <span className="text-slate-600">•</span>
                              <span className="text-slate-500 text-[10px]">Reference: {job.templateRef}</span>
                            </div>
                            <div className="text-[10px] text-slate-500 mt-1">
                              Requested: {new Date(job.requestedAt).toLocaleTimeString()}
                            </div>
                          </div>

                          <div>
                            {job.status === 'pending' && (
                              <span className="bg-amber-950/60 border border-amber-500/30 text-amber-500 text-[9px] font-bold px-2 py-0.5 rounded-full animate-pulse">
                                PENDING ERASURE
                              </span>
                            )}
                            {job.status === 'completed' && (
                              <span className="bg-emerald-950/60 border border-emerald-500/30 text-emerald-400 text-[9px] font-bold px-2 py-0.5 rounded-full">
                                COMPLETED
                              </span>
                            )}
                          </div>
                        </div>
                      ))}
                    </div>

                    <p className="text-[10px] text-slate-500 leading-normal font-sans pt-1">
                      *Consent withdrawal triggers immediate authentication revocation followed by synchronous database cluster erasure within 4 seconds (ephemeral nodes cleared instantly).
                    </p>
                  </div>

                </div>
              </div>

            </div>
          )}

          {/* TAB CONTENT: 3. P2 ADMINISTRATIVE SECURITY POLICIES */}
          {activeTab === 'policy' && (
            <div className="bg-slate-900/20 border border-slate-900 rounded-2xl p-6 flex flex-col gap-6 animate-fade-in" id="panel-policy">
              
              <div className="border-b border-slate-800/80 pb-4">
                <h3 className="text-lg font-bold text-slate-200">Biometric Verification Security Policy Editor</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Govern the system-wide authentication standards, trust requirements, acceptable evidence age parameters, and rollouts.
                </p>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* Policy Config Inputs */}
                <div className="space-y-4">
                  
                  {/* Parameter 1: Max Evidence Age */}
                  <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/40">
                    <label className="text-xs font-mono font-bold text-slate-300 uppercase block">
                      Maximum Evidence Freshness (seconds)
                    </label>
                    <span className="text-[10px] text-slate-500 block mb-3">
                      Enforces maximum time since physical capture on specialized hardware before step-up re-verification triggers.
                    </span>
                    <input 
                      type="number"
                      value={policy.maxEvidenceAgeSeconds}
                      onChange={(e) => handlePolicyChange('maxEvidenceAgeSeconds', Number(e.target.value))}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2 text-xs font-mono text-teal-400 focus:outline-none focus:border-teal-500"
                    />
                  </div>

                  {/* Parameter 2: Require Liveness Check */}
                  <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/40 flex items-center justify-between">
                    <div>
                      <label className="text-xs font-mono font-bold text-slate-300 uppercase block">
                        Mandate Liveness / PAD Detection
                      </label>
                      <span className="text-[10px] text-slate-500 block">
                        Reject biometric verification proofs that omit certified presentation-attack audits.
                      </span>
                    </div>
                    <button 
                      onClick={() => handlePolicyChange('requireLiveness', !policy.requireLiveness)}
                      className={`w-12 h-6 rounded-full transition-colors relative shrink-0 ${policy.requireLiveness ? 'bg-teal-500' : 'bg-slate-800'}`}
                      aria-label="Toggle liveness requirement"
                    >
                      <span className={`absolute top-1 left-1 bg-slate-950 w-4 h-4 rounded-full transition-transform ${policy.requireLiveness ? 'translate-x-6' : ''}`} />
                    </button>
                  </div>

                  {/* Parameter 3: Application scope */}
                  <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/40">
                    <label className="text-xs font-mono font-bold text-slate-300 uppercase block mb-1">
                      Biometric Application Scope
                    </label>
                    <span className="text-[10px] text-slate-500 block mb-3">
                      Define where biometric proof is demanded versus when standard password/passkey flows are eligible.
                    </span>
                    <select
                      value={policy.applicationScope}
                      onChange={(e) => handlePolicyChange('applicationScope', e.target.value)}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500 font-medium"
                    >
                      <option value="all">Mandate Iris Recognition for All Authentication Ceremonies (Strict)</option>
                      <option value="step-up-only">Restrict Iris to High-Value Step-up Transactions Only</option>
                      <option value="restricted">Restricted Portal Access (Administrative Users Only)</option>
                    </select>
                  </div>

                  {/* Parameter 4: Fallback options */}
                  <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/40">
                    <label className="text-xs font-mono font-bold text-slate-300 uppercase block mb-1">
                      Eligible Fallback Verification Factor
                    </label>
                    <span className="text-[10px] text-slate-500 block mb-3">
                      Assigns verification bypass factor when physical specialized sensor is offline or malfunctioning.
                    </span>
                    <select
                      value={policy.fallbackMethod}
                      onChange={(e) => handlePolicyChange('fallbackMethod', e.target.value)}
                      className="w-full bg-slate-900 border border-slate-800 rounded-lg p-2.5 text-xs text-slate-200 focus:outline-none focus:border-teal-500 font-medium"
                    >
                      <option value="passkey">FIDO2 WebAuthn Passkey (Highest Assurance Bypass)</option>
                      <option value="totp">Secure Cryptographic Hardware Key (TOTP Token)</option>
                      <option value="supervised-recovery">Supervised Tenant Administrator Custody Recovery</option>
                    </select>
                  </div>

                </div>

                {/* Right Side: Global Rollout Map & Audit Preview */}
                <div className="space-y-4">
                  
                  {/* Regional rollout indicators */}
                  <div className="bg-slate-950/50 p-4 rounded-xl border border-slate-800/40 space-y-3">
                    <label className="text-xs font-mono font-bold text-slate-300 uppercase block">
                      Regional Compliance Rollout
                    </label>
                    <span className="text-[10px] text-slate-500 block">
                      Toggles verification authorization by tenant region. Compliant regional filters are strictly enforced during verification routing.
                    </span>

                    <div className="space-y-2 pt-2">
                      <div className="flex items-center justify-between text-xs bg-slate-900 p-2 rounded border border-slate-850">
                        <span className="flex items-center gap-1.5">
                          <Globe className="w-3.5 h-3.5 text-teal-400" />
                          <span>US-EAST (Virginia / CCPA)</span>
                        </span>
                        <button
                          onClick={() => {
                            const updatedRollout = { ...policy.regionalRollout, usEast: !policy.regionalRollout.usEast };
                            handlePolicyChange('regionalRollout', updatedRollout);
                          }}
                          className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                            policy.regionalRollout.usEast 
                              ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/20' 
                              : 'bg-slate-800 text-slate-500'
                          }`}
                        >
                          {policy.regionalRollout.usEast ? 'AUTHORIZED' : 'RESTRICTED'}
                        </button>
                      </div>

                      <div className="flex items-center justify-between text-xs bg-slate-900 p-2 rounded border border-slate-850">
                        <span className="flex items-center gap-1.5">
                          <Globe className="w-3.5 h-3.5 text-teal-400" />
                          <span>EU-WEST (Dublin / GDPR)</span>
                        </span>
                        <button
                          onClick={() => {
                            const updatedRollout = { ...policy.regionalRollout, euWest: !policy.regionalRollout.euWest };
                            handlePolicyChange('regionalRollout', updatedRollout);
                          }}
                          className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                            policy.regionalRollout.euWest 
                              ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/20' 
                              : 'bg-slate-800 text-slate-500'
                          }`}
                        >
                          {policy.regionalRollout.euWest ? 'AUTHORIZED' : 'RESTRICTED'}
                        </button>
                      </div>

                      <div className="flex items-center justify-between text-xs bg-slate-900 p-2 rounded border border-slate-850">
                        <span className="flex items-center gap-1.5">
                          <Globe className="w-3.5 h-3.5 text-teal-400" />
                          <span>AP-SOUTH (Mumbai)</span>
                        </span>
                        <button
                          onClick={() => {
                            const updatedRollout = { ...policy.regionalRollout, apSouth: !policy.regionalRollout.apSouth };
                            handlePolicyChange('regionalRollout', updatedRollout);
                          }}
                          className={`text-[10px] font-mono px-2 py-0.5 rounded font-bold ${
                            policy.regionalRollout.apSouth 
                              ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/20' 
                              : 'bg-slate-800 text-slate-500'
                          }`}
                        >
                          {policy.regionalRollout.apSouth ? 'AUTHORIZED' : 'RESTRICTED'}
                        </button>
                      </div>
                    </div>
                  </div>

                  {/* Policy Impact Preview panel */}
                  <div className="bg-blue-950/20 border border-blue-500/20 rounded-xl p-4 flex gap-3">
                    <Info className="w-5 h-5 text-blue-400 shrink-0 mt-0.5" />
                    <div className="text-xs space-y-1.5 leading-normal">
                      <strong className="text-blue-300">Policy Impact Assessment:</strong>
                      <p className="text-slate-400">
                        The current configuration dictates that all high-assurance logins are authenticated within <span className="text-blue-200 font-bold">{policy.maxEvidenceAgeSeconds}s</span>. Fallback to <span className="text-blue-200 font-bold">{policy.fallbackMethod.toUpperCase()}</span> will only be routed if liveness checks satisfy physical PAD evaluation standards.
                      </p>
                    </div>
                  </div>

                </div>

              </div>

            </div>
          )}

          {/* TAB CONTENT: 4. P2 DIAGNOSTICS & PROVIDERS HEALTH */}
          {activeTab === 'health' && (
            <div className="bg-slate-900/20 border border-slate-900 rounded-2xl p-6 flex flex-col gap-6 animate-fade-in" id="panel-health">
              
              <div className="border-b border-slate-800/80 pb-4">
                <h3 className="text-lg font-bold text-slate-200">System Conformance & Provider Diagnostics</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Monitor verification telemetry, verify conformance certifications, inspect trust matrices, and analyze redacted system security logs.
                </p>
              </div>

              {/* SECTION 1: PROVIDER CONFIGURATIONS */}
              <div>
                <h4 className="text-xs font-mono font-bold uppercase text-slate-400 tracking-wider mb-3">
                  🏢 REGISTERED PROVIDERS & CONFIDENCE MATRICES
                </h4>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {providers.map((provider) => (
                    <div key={provider.id} className="bg-slate-950/60 border border-slate-900 rounded-xl p-4 flex flex-col justify-between gap-4">
                      
                      {/* Name & Type */}
                      <div>
                        <div className="flex items-center justify-between">
                          <span className="text-[10px] font-mono text-slate-500 uppercase">{provider.type}</span>
                          
                          {provider.status === 'active' && (
                            <span className="bg-emerald-950 text-emerald-400 text-[9px] font-mono px-2 py-0.5 rounded border border-emerald-500/20">
                              ONLINE
                            </span>
                          )}
                          {provider.status === 'suspended' && (
                            <span className="bg-rose-950 text-rose-400 text-[9px] font-mono px-2 py-0.5 rounded border border-rose-500/20">
                              SUSPENDED
                            </span>
                          )}
                        </div>

                        <strong className="text-sm text-slate-200 block mt-1.5">{provider.name}</strong>
                        
                        <div className="mt-2 text-[10px] font-mono text-slate-400 space-y-1">
                          <div className="truncate">API: {provider.apiEndpoint}</div>
                          <div>Data Retention: {provider.retentionDays === 0 ? 'Ephemeral (0 days)' : `${provider.retentionDays} days`}</div>
                        </div>
                      </div>

                      {/* Controls & Certification */}
                      <div className="border-t border-slate-900 pt-3 flex items-center justify-between text-xs">
                        <div className="flex items-center gap-1">
                          <Shield className={`w-3.5 h-3.5 ${provider.conformanceCertified ? 'text-emerald-400' : 'text-slate-600'}`} />
                          <span className="text-[10px] text-slate-400 font-mono">
                            {provider.conformanceCertified ? 'FIDO Certified' : 'Uncertified'}
                          </span>
                        </div>

                        <button
                          onClick={() => handleProviderToggle(provider.id)}
                          className={`text-[10px] font-mono font-bold px-2 py-1 rounded transition-colors ${
                            provider.status === 'active'
                              ? 'bg-rose-950/40 hover:bg-rose-950/60 text-rose-400 border border-rose-500/30'
                              : 'bg-emerald-950/40 hover:bg-emerald-950/60 text-emerald-400 border border-emerald-500/30'
                          }`}
                        >
                          {provider.status === 'active' ? 'SUSPEND' : 'ACTIVATE'}
                        </button>
                      </div>

                    </div>
                  ))}
                </div>
              </div>

              {/* SECTION 2: REDACTED AUDIT LOGS */}
              <div>
                <div className="flex items-center justify-between mb-3">
                  <h4 className="text-xs font-mono font-bold uppercase text-slate-400 tracking-wider">
                    📝 COMPLIANT REDACTED SECURITY AUDIT ARCHIVE
                  </h4>
                  <button 
                    onClick={() => {
                      setAuditLogs(INITIAL_AUDIT_LOGS);
                      appendAuditLog('AUDIT_ARCHIVE_RESET', 'warning', 'none', 'system', 'Diagnostics administrator re-initialized audit sequence logs.');
                    }}
                    className="text-[10px] text-slate-500 hover:text-slate-300 font-mono flex items-center gap-1"
                  >
                    <RotateCcw className="w-3 h-3" />
                    Reset Audit Logs
                  </button>
                </div>

                <div className="bg-slate-950/40 border border-slate-900 rounded-xl overflow-hidden max-h-72 overflow-y-auto pr-1">
                  <table className="w-full text-left border-collapse text-[11px] font-mono">
                    <thead>
                      <tr className="bg-slate-900 text-slate-500 border-b border-slate-850 sticky top-0 z-10">
                        <th className="py-2.5 px-4 font-normal">Audit Reference ID</th>
                        <th className="py-2.5 px-4 font-normal">Timestamp</th>
                        <th className="py-2.5 px-4 font-normal">Security Action</th>
                        <th className="py-2.5 px-4 font-normal">Provenance</th>
                        <th className="py-2.5 px-4 font-normal">Payload Details (Redacted - Privacy Protected)</th>
                        <th className="py-2.5 px-4 font-normal text-right">Outcome</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-900 text-slate-300">
                      {auditLogs.map((log) => (
                        <tr key={log.id} className="hover:bg-slate-900/30 transition-colors">
                          <td className="py-2.5 px-4 text-teal-500 font-bold">{log.id}</td>
                          <td className="py-2.5 px-4 text-slate-500">
                            {new Date(log.timestamp).toLocaleTimeString()}
                          </td>
                          <td className="py-2.5 px-4 font-semibold text-slate-300">{log.action}</td>
                          <td className="py-2.5 px-4 text-slate-400">{log.provenance}</td>
                          <td className="py-2.5 px-4 text-slate-400 font-sans text-xs max-w-xs truncate" title={log.detailsRedacted}>
                            {log.detailsRedacted}
                          </td>
                          <td className="py-2.5 px-4 text-right">
                            <span className={`px-2 py-0.5 rounded text-[9px] font-bold ${
                              log.outcome === 'success' 
                                ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-500/20' 
                                : log.outcome === 'failure' 
                                  ? 'bg-rose-950/60 text-rose-400 border border-rose-500/20 animate-pulse' 
                                  : 'bg-amber-950/60 text-amber-500 border border-amber-500/20'
                            }`}>
                              {log.outcome.toUpperCase()}
                            </span>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                <div className="bg-slate-900/40 border border-slate-850 p-3 rounded-lg text-[10px] text-slate-500 font-mono mt-3 leading-normal">
                  ⚠ <strong>Audit Compliance Safeguard:</strong> This log is strictly redacted. Absolute matches, individual physiological metrics, ocular photography, and unique sensor identifiers are forever excluded from audit storage payloads to protect identity anonymity.
                </div>
              </div>

            </div>
          )}

        </section>

      </main>

      {/* App Footer */}
      <footer className="border-t border-slate-900 bg-slate-950 text-center py-4 text-slate-600 text-xs font-mono" id="app-footer">
        <div className="max-w-7xl mx-auto px-6 flex flex-col sm:flex-row items-center justify-between gap-4">
          <span>First-Party Iris AMR Authenticator Demonstration Shell • ISO/IEC 19794-6 Compliant</span>
          <span className="text-slate-500">Current Session UTC time: 2026-07-15 10:32:46</span>
        </div>
      </footer>

    </div>
  );
}
