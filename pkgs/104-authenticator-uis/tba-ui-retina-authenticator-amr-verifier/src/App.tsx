import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { ShieldCheck, User, Cpu, Activity, RefreshCw, KeyRound, Info, AlertTriangle, Play, HelpCircle, CheckCircle, Ban, Eye, Lock } from 'lucide-react';
import { 
  BiometricConsentRecord, 
  VerifierDevice, 
  AuditLog, 
  BiometricPolicy, 
  RetinaEnrollment, 
  BiometricStatus 
} from './types';

// Component Imports
import BiometricConsent from './components/BiometricConsent';
import DevicePreflight from './components/DevicePreflight';
import RetinaCaptureSimulator from './components/RetinaCaptureSimulator';
import LifecycleManager from './components/LifecycleManager';
import AdminDashboard from './components/AdminDashboard';

export default function App() {
  const [activePerspective, setActivePerspective] = useState<'ceremony' | 'lifecycle' | 'admin'>('ceremony');
  
  // App Core State
  const [consent, setConsent] = useState<BiometricConsentRecord | null>(null);
  const [enrollment, setEnrollment] = useState<RetinaEnrollment | null>(null);
  const [hasOtherFactors, setHasOtherFactors] = useState(false); // To test deletion lockout
  
  // Active Ceremony State
  const [ceremonyState, setCeremonyState] = useState<'idle' | 'consent' | 'preflight' | 'scanning' | 'success' | 'fallback_routing'>('idle');
  const [ceremonyType, setCeremonyType] = useState<'enrollment' | 'verification' | 'step-up'>('enrollment');
  const [selectedDevice, setSelectedDevice] = useState<VerifierDevice | null>(null);
  
  // Feedback alerts
  const [ceremonyMessage, setCeremonyMessage] = useState<{ text: string; type: 'success' | 'info' | 'error' } | null>(null);

  // Policy default setup
  const [policy, setPolicy] = useState<BiometricPolicy>({
    eligibilityScope: 'all_users',
    requiredLivenessLevel: 'Level-3',
    retentionPeriodMonths: 6,
    allowWebFallback: true,
    geofenceEnabled: false,
    geofencedRegions: ['USA-EAST-1'],
  });

  // Verifier Fleet default setup
  const [devices, setDevices] = useState<VerifierDevice[]>([
    {
      id: 'VER-990-H1',
      name: 'RetinaScan Prime H100',
      model: 'RP-H100-M1',
      location: 'Primary Secure Vault Booth B3',
      firmwareVersion: 'v4.14.9-secure',
      status: 'online',
      conformanceClass: 'Class-A',
      lastCalibrationDate: new Date().toLocaleDateString(),
      ambientLightLux: 45,
      cameraResolution: '8K Quad-Spectrum Ocular Sensor',
    },
    {
      id: 'VER-744-T5',
      name: 'RetinaScan Tactical T50',
      model: 'RP-T50-M5',
      location: 'Mobile Security Terminal Alpha',
      firmwareVersion: 'v3.2.1-secure',
      status: 'calibrating',
      conformanceClass: 'Class-B',
      lastCalibrationDate: new Date(Date.now() - 86400000 * 2).toLocaleDateString(),
      ambientLightLux: 120,
      cameraResolution: '4K Multi-Spectrum Mobile Lens',
    },
    {
      id: 'VER-112-S9',
      name: 'RetinaScan Entry S12',
      model: 'RP-S12-M2',
      location: 'External Intake Gate Room 4',
      firmwareVersion: 'v5.0.4-secure',
      status: 'maintenance',
      conformanceClass: 'Class-C',
      lastCalibrationDate: new Date(Date.now() - 86400000 * 15).toLocaleDateString(),
      ambientLightLux: 350,
      cameraResolution: 'Dual-Spectrum IR Gate Imager',
    }
  ]);

  // Central Operational Auditing Logs
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>([
    {
      id: 'log_01',
      timestamp: new Date(Date.now() - 3600000).toISOString(),
      eventType: 'device_calibration',
      subjectId: 'SYSTEM-OPS',
      deviceId: 'VER-990-H1',
      outcome: 'success',
      livenessClass: 'None',
      matchScoreClass: 'N/A',
      details: 'Automatic 24-hour optical sweep complete. Divergence drift within specs.',
    },
    {
      id: 'log_02',
      timestamp: new Date(Date.now() - 1800000).toISOString(),
      eventType: 'policy_change',
      subjectId: 'ADMIN-USR-01',
      deviceId: 'WEB-CONSOLE',
      outcome: 'success',
      livenessClass: 'None',
      matchScoreClass: 'N/A',
      details: 'Assurance guidelines update: Required active saccadic tracking Level-3 globally.',
    },
    {
      id: 'log_03',
      timestamp: new Date(Date.now() - 900000).toISOString(),
      eventType: 'preflight_pass',
      subjectId: 'SUBJ-USR-773',
      deviceId: 'VER-990-H1',
      outcome: 'success',
      livenessClass: 'Level-3',
      matchScoreClass: 'N/A',
      details: 'Specialized device handshake complete. Lens calibration compliant.',
    }
  ]);

  const addAuditLog = (
    eventType: AuditLog['eventType'],
    subjectId: string,
    deviceId: string,
    outcome: AuditLog['outcome'],
    livenessClass: AuditLog['livenessClass'],
    matchScoreClass: AuditLog['matchScoreClass'],
    details: string
  ) => {
    const newLog: AuditLog = {
      id: `log_${Math.random().toString(36).substr(2, 9)}`,
      timestamp: new Date().toISOString(),
      eventType,
      subjectId,
      deviceId,
      outcome,
      livenessClass,
      matchScoreClass,
      details,
    };
    setAuditLogs(prev => [newLog, ...prev]);
  };

  // Run initial wizard workflow checks
  const handleStartEnrollment = () => {
    setCeremonyType('enrollment');
    setCeremonyState('consent');
    setCeremonyMessage(null);
  };

  const handleStartVerification = () => {
    if (!enrollment) {
      setCeremonyMessage({ text: 'Error: No active retina template found. Please enroll first.', type: 'error' });
      return;
    }
    if (enrollment.status === 'suspended') {
      setCeremonyMessage({ text: 'Error: Biometric credentials temporarily suspended. Activate in Lifecycle Panel.', type: 'error' });
      return;
    }
    if (enrollment.status === 'revoked') {
      setCeremonyMessage({ text: 'Error: Biometric credentials revoked. You must re-enroll to recover access.', type: 'error' });
      return;
    }
    setCeremonyType('verification');
    setCeremonyState('preflight');
    setCeremonyMessage(null);
  };

  const handleConsentGiven = (record: BiometricConsentRecord) => {
    setConsent(record);
    addAuditLog('consent_accept', 'SUBJ-USR-773', 'VER-990-H1', 'success', 'None', 'N/A', `biometric processing consent accepted for version ${record.version}`);
    setCeremonyState('preflight');
  };

  const handleConsentDeclined = (alternative: string) => {
    addAuditLog('consent_withdraw', 'SUBJ-USR-773', 'VER-990-H1', 'warning', 'None', 'N/A', `user declined retina mapping, requested fallback routing to ${alternative}`);
    setCeremonyState('fallback_routing');
    setCeremonyMessage({ 
      text: `Biometric consent declined. Access redirected to fallback factor: ${alternative.toUpperCase()}`, 
      type: 'info' 
    });
  };

  const handlePreflightSuccess = (device: VerifierDevice) => {
    setSelectedDevice(device);
    addAuditLog('preflight_pass', 'SUBJ-USR-773', device.id, 'success', 'None', 'N/A', 'Ocular lens preflight passed. Ambient light level verified.');
    setCeremonyState('scanning');
  };

  const handlePreflightFail = (reason: string) => {
    addAuditLog('preflight_fail', 'SUBJ-USR-773', 'VER-990-H1', 'failed', 'None', 'N/A', `Preflight calibration fault: ${reason}`);
    setCeremonyMessage({ text: `Device preflight failed: ${reason}`, type: 'error' });
  };

  const handleCaptureSuccess = (signature: string, livenessClass: string) => {
    if (ceremonyType === 'enrollment') {
      const newEnrollment: RetinaEnrollment = {
        id: `enroll_${Math.random().toString(36).substr(2, 9)}`,
        subjectId: 'SUBJ-USR-773',
        deviceId: selectedDevice?.id || 'VER-990-H1',
        enrolledAt: new Date().toISOString(),
        status: 'active',
        calibrationScore: 98.6,
        consentVersion: consent?.version || '1.0',
        lastUsedAt: new Date().toISOString(),
        expiresAt: new Date(Date.now() + 180 * 24 * 3600 * 1000).toISOString(), // 180 days out
      };
      setEnrollment(newEnrollment);
      addAuditLog('enrollment_success', 'SUBJ-USR-773', selectedDevice?.id || 'VER-990-H1', 'success', livenessClass as any, 'high_confidence', 'biometric ocular enrollment template successfully compiled and bound');
      setCeremonyMessage({ text: 'Ocular capture complete. Specialized biometric credentials successfully bound & activated.', type: 'success' });
    } else {
      // Verification
      if (enrollment) {
        setEnrollment({
          ...enrollment,
          lastUsedAt: new Date().toISOString(),
        });
      }
      addAuditLog('verification_success', 'SUBJ-USR-773', selectedDevice?.id || 'VER-990-H1', 'success', livenessClass as any, 'high_confidence', 'Retina scan match certified. Secure proof emitted.');
      setCeremonyMessage({ text: 'Retina verified successfully. Authentication proof factor "retina" emitted.', type: 'success' });
    }
    setCeremonyState('success');
  };

  const handleCaptureFail = (reason: string) => {
    addAuditLog('verification_fail', 'SUBJ-USR-773', selectedDevice?.id || 'VER-990-H1', 'failed', 'None', 'no_match', `Biometric ceremony failed: ${reason}`);
    setCeremonyMessage({ text: `Biometric matching failed: ${reason}. Access denied.`, type: 'error' });
    setCeremonyState('idle');
  };

  const handleWithdrawConsent = () => {
    setConsent(null);
    setEnrollment(null);
    addAuditLog('template_delete', 'SUBJ-USR-773', 'VER-990-H1', 'success', 'None', 'N/A', 'biometric template shredded from enclave following consent revocation');
    setCeremonyState('idle');
    setCeremonyMessage({ text: 'Retinal templates permanently erased. Consent withdrawn.', type: 'info' });
  };

  const handleEnrollmentStatusChange = (newStatus: BiometricStatus) => {
    if (enrollment) {
      setEnrollment({
        ...enrollment,
        status: newStatus,
      });
      addAuditLog(
        newStatus === 'suspended' ? 'preflight_fail' : 'enrollment_start',
        'SUBJ-USR-773',
        'VER-990-H1',
        'warning',
        'None',
        'N/A',
        `Biometric status manually set to ${newStatus}`
      );
    }
  };

  return (
    <div id="app-viewport" className="min-h-screen bg-slate-950 text-slate-100 flex flex-col font-sans">
      
      {/* Master Security Header */}
      <header className="bg-slate-900/90 border-b border-slate-800/80 sticky top-0 z-50 backdrop-blur">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">
          
          {/* Logo & Method Identity */}
          <div className="flex items-center gap-3">
            <div className="p-2 bg-gradient-to-tr from-cyan-500/20 to-emerald-500/20 border border-cyan-500/30 rounded-xl text-cyan-400">
              <Eye className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <span className="text-[10px] font-mono text-emerald-400 uppercase tracking-widest block font-semibold leading-none">Biometric AMR</span>
              <h1 className="text-base font-bold text-slate-200 tracking-tight font-mono">RETINA SECURE VERIFIER</h1>
            </div>
          </div>

          {/* Perspective Navigation Tabs */}
          <nav className="flex bg-slate-950 p-1 rounded-lg border border-slate-800/80">
            <button
              id="btn-persp-ceremony"
              onClick={() => {
                setActivePerspective('ceremony');
                setCeremonyMessage(null);
              }}
              className={`px-3 py-1.5 font-mono text-xs font-semibold rounded-md flex items-center gap-1.5 transition-all cursor-pointer ${
                activePerspective === 'ceremony' ? 'bg-slate-900 text-cyan-400 shadow' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <ShieldCheck className="w-3.5 h-3.5" />
              Ceremony Terminal
            </button>

            <button
              id="btn-persp-lifecycle"
              onClick={() => {
                setActivePerspective('lifecycle');
                setCeremonyMessage(null);
              }}
              className={`px-3 py-1.5 font-mono text-xs font-semibold rounded-md flex items-center gap-1.5 transition-all cursor-pointer ${
                activePerspective === 'lifecycle' ? 'bg-slate-900 text-cyan-400 shadow' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <User className="w-3.5 h-3.5" />
              Ocular Lifecycle
            </button>

            <button
              id="btn-persp-admin"
              onClick={() => {
                setActivePerspective('admin');
                setCeremonyMessage(null);
              }}
              className={`px-3 py-1.5 font-mono text-xs font-semibold rounded-md flex items-center gap-1.5 transition-all cursor-pointer ${
                activePerspective === 'admin' ? 'bg-slate-900 text-cyan-400 shadow' : 'text-slate-400 hover:text-slate-200'
              }`}
            >
              <Cpu className="w-3.5 h-3.5" />
              Fleet Operations
            </button>
          </nav>

          {/* Subject Identity Status Indicator */}
          <div className="hidden md:flex items-center gap-3 bg-slate-950 px-3 py-1.5 rounded-lg border border-slate-800/60 text-xs font-mono">
            <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse" />
            <span className="text-slate-400">SESSION:</span>
            <span className="text-slate-200 font-bold">SUBJ-USR-773 (Subject)</span>
          </div>
        </div>
      </header>

      {/* Main Container Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-8">
        
        {/* Dynamic Alerts Banner */}
        <AnimatePresence>
          {ceremonyMessage && (
            <motion.div
              id="alert-banner"
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className={`p-4 rounded-xl border flex items-start gap-3 text-xs leading-normal font-sans ${
                ceremonyMessage.type === 'success' ? 'bg-emerald-950/20 border-emerald-500/20 text-emerald-400' :
                ceremonyMessage.type === 'error' ? 'bg-red-950/20 border-red-500/20 text-red-400' :
                'bg-cyan-950/20 border-cyan-500/20 text-cyan-400'
              }`}
            >
              {ceremonyMessage.type === 'success' ? (
                <CheckCircle className="w-4 h-4 shrink-0 mt-0.5" />
              ) : (
                <AlertTriangle className="w-4 h-4 shrink-0 mt-0.5" />
              )}
              <div className="flex-1">
                <p className="font-semibold uppercase font-mono text-[10px] tracking-wide">
                  {ceremonyMessage.type === 'success' ? 'System Affirmation' : ceremonyMessage.type === 'error' ? 'Security Exception' : 'Access Handoff Trace'}
                </p>
                <p className="mt-1 font-medium">{ceremonyMessage.text}</p>
              </div>
              <button
                id="btn-close-alert"
                onClick={() => setCeremonyMessage(null)}
                className="text-slate-400 hover:text-slate-200 font-bold px-1"
              >
                ✕
              </button>
            </motion.div>
          )}
        </AnimatePresence>

        {/* Perspective Contents rendering */}
        <AnimatePresence mode="wait">
          {activePerspective === 'ceremony' && (
            <motion.div
              key="ceremony"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="space-y-6"
            >
              {/* Dynamic Step Wizard Router */}
              {ceremonyState === 'idle' && (
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 max-w-2xl mx-auto shadow-2xl space-y-6 text-center">
                  <div className="w-16 h-16 rounded-full bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 mx-auto">
                    <KeyRound className="w-8 h-8 animate-pulse" />
                  </div>
                  <div className="space-y-2">
                    <h2 className="text-xl font-semibold tracking-tight text-slate-100">Specialized Biometric Access Gate</h2>
                    <p className="text-sm text-slate-400 font-sans max-w-md mx-auto">
                      Authorized retina scan authentication requires a dedicated physical verifier. Select your biometric goal below.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-4">
                    <button
                      id="btn-dashboard-start-enroll"
                      onClick={handleStartEnrollment}
                      className="p-5 rounded-xl border border-slate-800 hover:border-cyan-500/40 bg-slate-950/40 hover:bg-slate-950/80 transition-all text-left space-y-2 group cursor-pointer"
                    >
                      <span className="text-xs font-mono text-cyan-400 uppercase tracking-wider block">First Use</span>
                      <h3 className="text-sm font-semibold text-slate-200 group-hover:text-cyan-400 transition-colors">Retina Enrollment</h3>
                      <p className="text-xs text-slate-500 font-sans leading-normal">
                        Submit consent, confirm preflight, and map eye blood vessels in the secure enclave.
                      </p>
                    </button>

                    <button
                      id="btn-dashboard-start-verify"
                      onClick={handleStartVerification}
                      className="p-5 rounded-xl border border-slate-800 hover:border-emerald-500/40 bg-slate-950/40 hover:bg-slate-950/80 transition-all text-left space-y-2 group cursor-pointer"
                    >
                      <span className="text-xs font-mono text-emerald-400 uppercase tracking-wider block">Existing User</span>
                      <h3 className="text-sm font-semibold text-slate-200 group-hover:text-emerald-400 transition-colors">Retina Sign-In</h3>
                      <p className="text-xs text-slate-500 font-sans leading-normal">
                        Complete active ocular liveness tracking to emit signed 'retina' factor evidence.
                      </p>
                    </button>
                  </div>
                </div>
              )}

              {ceremonyState === 'consent' && (
                <BiometricConsent
                  currentVersion="1.4-Compliance"
                  onConsentGiven={handleConsentGiven}
                  onConsentDeclined={handleConsentDeclined}
                />
              )}

              {ceremonyState === 'preflight' && (
                <DevicePreflight
                  onPreflightSuccess={handlePreflightSuccess}
                  onPreflightFail={handlePreflightFail}
                  onCancel={() => setCeremonyState('idle')}
                />
              )}

              {ceremonyState === 'scanning' && (
                <RetinaCaptureSimulator
                  device={selectedDevice || devices[0]}
                  ceremonyType={ceremonyType}
                  onCaptureSuccess={handleCaptureSuccess}
                  onCaptureFail={handleCaptureFail}
                  onCancel={() => setCeremonyState('idle')}
                />
              )}

              {ceremonyState === 'fallback_routing' && (
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 max-w-md mx-auto text-center space-y-5 shadow-2xl">
                  <div className="p-3 bg-red-500/10 border border-red-500/20 text-red-400 rounded-full w-12 h-12 flex items-center justify-center mx-auto">
                    <Lock className="w-6 h-6 animate-bounce" />
                  </div>
                  <div>
                    <h3 className="text-sm font-mono font-bold uppercase text-red-400">Fallback Routing In Progress</h3>
                    <p className="text-xs text-slate-400 mt-2 font-sans leading-relaxed">
                      Retina biometric method was declined or unavailable. Diverting cryptographic transaction purpose verification safely to your alternative key.
                    </p>
                  </div>
                  <button
                    id="btn-fallback-clear"
                    onClick={() => {
                      setCeremonyState('idle');
                      setCeremonyMessage(null);
                    }}
                    className="w-full py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-xs font-mono uppercase tracking-wider rounded transition-all cursor-pointer"
                  >
                    Return to Selection
                  </button>
                </div>
              )}

              {ceremonyState === 'success' && (
                <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 max-w-md mx-auto text-center space-y-6 shadow-2xl">
                  <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 rounded-full w-14 h-14 flex items-center justify-center mx-auto">
                    <CheckCircle className="w-8 h-8" />
                  </div>
                  <div>
                    <h2 className="text-lg font-mono font-bold uppercase text-emerald-400">Ceremony Approved</h2>
                    <p className="text-xs text-slate-400 mt-2 font-sans leading-relaxed">
                      The enclave verified active ocular liveness parameters successfully. 
                      Evidence payload containing <strong className="text-slate-200">AMR: ["retina"]</strong> has been securely emitted.
                    </p>
                  </div>

                  <div className="bg-slate-950 p-3 rounded border border-slate-800 font-mono text-[10px] text-left text-cyan-400 space-y-1">
                    <p className="text-slate-500 uppercase font-bold border-b border-slate-900 pb-1 mb-1 text-[9px]">ENCLAVE VERDICT</p>
                    <p><span className="text-slate-500">Subject:</span> SUBJ-USR-773</p>
                    <p><span className="text-slate-500">Method:</span> retina (biometric_proof)</p>
                    <p><span className="text-slate-500">Liveness:</span> Level-3 Active Saccades</p>
                    <p><span className="text-slate-500">Signature:</span> PROOF_SIGNED_RSA_4096_VALID</p>
                  </div>

                  <div className="flex gap-2">
                    <button
                      id="btn-success-profile"
                      onClick={() => {
                        setActivePerspective('lifecycle');
                        setCeremonyState('idle');
                        setCeremonyMessage(null);
                      }}
                      className="flex-1 py-2 bg-slate-950 hover:bg-slate-800 border border-slate-800 text-xs font-mono uppercase tracking-wider rounded transition-all cursor-pointer"
                    >
                      View Credentials
                    </button>
                    <button
                      id="btn-success-close"
                      onClick={() => {
                        setCeremonyState('idle');
                        setCeremonyMessage(null);
                      }}
                      className="flex-1 py-2 bg-emerald-500 hover:bg-emerald-400 text-slate-950 text-xs font-mono font-bold uppercase tracking-wider rounded transition-all cursor-pointer"
                    >
                      Complete
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          )}

          {activePerspective === 'lifecycle' && (
            <motion.div
              key="lifecycle"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <LifecycleManager
                enrollment={enrollment}
                onEnrollmentStatusChange={handleEnrollmentStatusChange}
                onTriggerReEnrollment={() => {
                  setCeremonyType('enrollment');
                  setCeremonyState('preflight');
                  setActivePerspective('ceremony');
                }}
                onWithdrawConsent={handleWithdrawConsent}
                onAddAlternativeFactor={() => {
                  setHasOtherFactors(true);
                  alert('FIDO2 hardware security key added successfully to personal logins. Deletion lockout is now cleared.');
                }}
                hasOtherFactors={hasOtherFactors}
                auditLogs={auditLogs}
              />
            </motion.div>
          )}

          {activePerspective === 'admin' && (
            <motion.div
              key="admin"
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
            >
              <AdminDashboard
                devices={devices}
                policy={policy}
                auditLogs={auditLogs}
                onUpdatePolicy={(p) => setPolicy(p)}
                onUpdateDevices={(devs) => setDevices(devs)}
              />
            </motion.div>
          )}
        </AnimatePresence>

        {/* Dynamic Sandbox Simulator Controls Drawer */}
        <section id="simulation-playground" className="border border-dashed border-slate-800 bg-slate-950/40 rounded-2xl p-5 space-y-4">
          <div className="flex items-center gap-2 border-b border-slate-900 pb-2">
            <Info className="w-4 h-4 text-cyan-400" />
            <h3 className="text-xs font-mono font-bold uppercase tracking-wider text-slate-400">
              Biometric Scenario & Testing Sandbox
            </h3>
          </div>

          <p className="text-[11px] text-slate-500 font-sans leading-relaxed">
            Use these controls to instantly toggle edge cases required in the Retina AMR brief. Watch how the UI safely adapts!
          </p>

          <div className="flex flex-wrap gap-3">
            {/* Toggle Other Factors (tests P1 deletion lock) */}
            <button
              id="sandbox-toggle-other-factors"
              onClick={() => {
                setHasOtherFactors(!hasOtherFactors);
                addAuditLog('policy_change', 'SYSTEM-OPS', 'WEB-CONSOLE', 'warning', 'None', 'N/A', `Toggled alternative registered login factors status to: ${!hasOtherFactors}`);
              }}
              className={`px-3 py-1.5 rounded font-mono text-[10px] border transition-all cursor-pointer ${
                hasOtherFactors 
                  ? 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400' 
                  : 'border-amber-500/20 bg-amber-500/10 text-amber-400'
              }`}
            >
              Alternative Login Factor: {hasOtherFactors ? 'REGISTERED' : 'MISSING (Triggers Deletion Lock)'}
            </button>

            {/* Toggle Primary Verifier Outage (tests preflight/diagnostics fail) */}
            <button
              id="sandbox-simulate-fleet-outage"
              onClick={() => {
                const nextStatus = devices[0].status === 'offline' ? 'online' : 'offline';
                const updated = devices.map((d, idx) => idx === 0 ? { ...d, status: nextStatus as any } : d);
                setDevices(updated);
                addAuditLog('device_outage', 'SYSTEM-OPS', 'VER-990-H1', 'failed', 'None', 'N/A', `Primary device state toggled to: ${nextStatus}`);
              }}
              className={`px-3 py-1.5 rounded font-mono text-[10px] border transition-all cursor-pointer ${
                devices[0].status === 'offline' 
                  ? 'border-red-500/20 bg-red-500/10 text-red-400 animate-pulse' 
                  : 'border-slate-800 bg-slate-950 text-slate-400'
              }`}
            >
              Verifier Prime Status: {devices[0].status.toUpperCase()}
            </button>

            {/* Simulate Ocular Drift Calibration Drift */}
            <button
              id="sandbox-trigger-focal-drift"
              onClick={() => {
                const updated = devices.map((d, idx) => idx === 0 ? { ...d, ambientLightLux: 180 } : d);
                setDevices(updated);
                addAuditLog('device_calibration', 'SYSTEM-OPS', 'VER-990-H1', 'warning', 'None', 'N/A', 'Ocular alignment focus drifting. Lens recalibration warning flagged.');
                alert('Primary Verifier ambient light level bumped above threshold. Open preflight to re-calibrate.');
              }}
              className="px-3 py-1.5 rounded border border-slate-800 bg-slate-950 hover:bg-slate-900 text-slate-400 hover:text-slate-200 font-mono text-[10px] transition-colors cursor-pointer"
            >
              Simulate Focal/Light Drift (Needs Calibration)
            </button>

            {/* Simulate Spoof / Liveness attack log */}
            <button
              id="sandbox-simulate-threat"
              onClick={() => {
                addAuditLog('verification_fail', 'ATTACKER_MASKED_X', 'VER-990-H1', 'failed', 'None', 'spoof_detected', 'Retinal vascular challenge fail: Pupil movement did not match random target dots. Biometric lock triggered.');
                alert('Spoofing threat logged in central audit. View logs under Central Audit & Diagnostics.');
              }}
              className="px-3 py-1.5 rounded border border-red-900/40 bg-red-950/20 text-red-400 font-mono text-[10px] hover:bg-red-950/40 transition-colors cursor-pointer"
            >
              Simulate Spoof Attack Log
            </button>
          </div>
        </section>
      </main>

      {/* Security Footer */}
      <footer className="bg-slate-900 border-t border-slate-800/80 py-6 mt-12 text-center text-xs font-mono text-slate-500">
        <div className="max-w-7xl mx-auto px-4 space-y-1">
          <p>Class-A Retina Authentication Method (AMR) • Secure Enclave Enlistment Specification</p>
          <p>© 2026 Sovereign Biometric Governance Network. Zero-Trust Architecture.</p>
        </div>
      </footer>
    </div>
  );
}
