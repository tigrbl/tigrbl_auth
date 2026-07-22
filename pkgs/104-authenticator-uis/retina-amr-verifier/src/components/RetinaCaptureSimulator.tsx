import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import { Eye, Shield, RefreshCw, AlertTriangle, Play, HelpCircle, Volume2, VolumeX, CheckCircle, Info } from 'lucide-react';
import { VerifierDevice, LivenessStep } from '../types';

interface RetinaCaptureSimulatorProps {
  device: VerifierDevice;
  ceremonyType: 'enrollment' | 'verification' | 'step-up';
  onCaptureSuccess: (signature: string, livenessClass: string) => void;
  onCaptureFail: (reason: string) => void;
  onCancel: () => void;
}

export default function RetinaCaptureSimulator({
  device,
  ceremonyType,
  onCaptureSuccess,
  onCaptureFail,
  onCancel,
}: RetinaCaptureSimulatorProps) {
  const [scanState, setScanState] = useState<'idle' | 'aligning' | 'liveness_check' | 'scanning' | 'processing' | 'success' | 'failed'>('idle');
  const [statusMessage, setStatusMessage] = useState('Position eye within sensor range');
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [livenessProgress, setLivenessProgress] = useState(0); // 0 to 100
  const [scanProgress, setScanProgress] = useState(0); // 0 to 100
  const [retryCount, setRetryCount] = useState(0);
  const [spoofDetected, setSpoofDetected] = useState(false);
  const [failureType, setFailureType] = useState<'quality' | 'liveness' | 'hardware' | 'none'>('none');

  // Liveness dot positioning
  const [targetDot, setTargetDot] = useState({ x: 50, y: 50 }); // percentages inside the frame
  const [userEye, setUserEye] = useState({ x: 50, y: 50 }); // user controlled eye cursor
  const [isEyeAligned, setIsEyeAligned] = useState(false);
  const [currentLivenessStep, setCurrentLivenessStep] = useState(0);

  const trackingAreaRef = useRef<HTMLDivElement>(null);
  const audioContextRef = useRef<AudioContext | null>(null);

  // Web Audio Synthesizer
  const playSound = (type: 'beep' | 'success' | 'fail' | 'scan' | 'click') => {
    if (!soundEnabled) return;
    try {
      if (!audioContextRef.current) {
        audioContextRef.current = new (window.AudioContext || (window as any).webkitAudioContext)();
      }
      const ctx = audioContextRef.current;
      if (ctx.state === 'suspended') {
        ctx.resume();
      }

      const osc = ctx.createOscillator();
      const gain = ctx.createGain();
      osc.connect(gain);
      gain.connect(ctx.destination);

      if (type === 'beep') {
        osc.type = 'sine';
        osc.frequency.setValueAtTime(880, ctx.currentTime);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
        osc.start();
        osc.stop(ctx.currentTime + 0.15);
      } else if (type === 'click') {
        osc.type = 'triangle';
        osc.frequency.setValueAtTime(440, ctx.currentTime);
        gain.gain.setValueAtTime(0.12, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.05);
        osc.start();
        osc.stop(ctx.currentTime + 0.05);
      } else if (type === 'scan') {
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(150, ctx.currentTime);
        osc.frequency.linearRampToValueAtTime(300, ctx.currentTime + 0.8);
        gain.gain.setValueAtTime(0.02, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.8);
        osc.start();
        osc.stop(ctx.currentTime + 0.85);
      } else if (type === 'success') {
        // High ascending scale
        const now = ctx.currentTime;
        osc.type = 'sine';
        osc.frequency.setValueAtTime(523.25, now); // C5
        osc.frequency.setValueAtTime(659.25, now + 0.1); // E5
        osc.frequency.setValueAtTime(783.99, now + 0.2); // G5
        osc.frequency.setValueAtTime(1046.50, now + 0.3); // C6
        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.5);
        osc.start();
        osc.stop(now + 0.5);
      } else if (type === 'fail') {
        // Harsh buzzer
        osc.type = 'sawtooth';
        osc.frequency.setValueAtTime(110, ctx.currentTime);
        osc.frequency.setValueAtTime(105, ctx.currentTime + 0.15);
        gain.gain.setValueAtTime(0.08, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.4);
        osc.start();
        osc.stop(ctx.currentTime + 0.4);
      }
    } catch (e) {
      console.warn('Audio synthesis failed to initialize:', e);
    }
  };

  // Pre-defined liveness coordinates to track
  const livenessSteps: LivenessStep[] = [
    { id: 1, instruction: "Track target to Top Right", targetX: 80, targetY: 20, durationMs: 2000 },
    { id: 2, instruction: "Track target to Center Left", targetX: 20, targetY: 50, durationMs: 2000 },
    { id: 3, instruction: "Track target to Bottom Center", targetX: 50, targetY: 80, durationMs: 2000 },
  ];

  // Start the actual ceremony
  const startCeremony = () => {
    playSound('beep');
    setScanState('aligning');
    setStatusMessage('Hold verifier steady. Align central visual axis.');
    setUserEye({ x: 15, y: 35 }); // Start far away
    setIsEyeAligned(false);
  };

  // Aligning simulation
  useEffect(() => {
    if (scanState !== 'aligning') return;

    const interval = setInterval(() => {
      // Guide user cursor toward center
      setUserEye(prev => {
        const dx = 50 - prev.x;
        const dy = 50 - prev.y;
        
        // Move closer to center by a random amount to simulate user adjustments
        const stepX = dx * 0.15 + (Math.random() * 4 - 2);
        const stepY = dy * 0.15 + (Math.random() * 4 - 2);
        
        const nextX = Math.max(0, Math.min(100, prev.x + stepX));
        const nextY = Math.max(0, Math.min(100, prev.y + stepY));

        const dist = Math.sqrt((nextX - 50) ** 2 + (nextY - 50) ** 2);
        if (dist < 4) {
          setIsEyeAligned(true);
          playSound('success');
          clearInterval(interval);
          startLivenessCheck();
        } else {
          playSound('click');
        }

        return { x: nextX, y: nextY };
      });
    }, 250);

    return () => clearInterval(interval);
  }, [scanState]);

  // Start active liveness dot tracking
  const startLivenessCheck = () => {
    setScanState('liveness_check');
    setCurrentLivenessStep(0);
    setLivenessProgress(0);
    setTargetDot({ x: livenessSteps[0].targetX, y: livenessSteps[0].targetY });
    setStatusMessage(livenessSteps[0].instruction);
  };

  // Interactive mouse tracking of the liveness dot
  const handleMouseMove = (e: React.MouseEvent<HTMLDivElement>) => {
    if (scanState !== 'liveness_check') return;
    if (!trackingAreaRef.current) return;

    const rect = trackingAreaRef.current.getBoundingClientRect();
    const x = ((e.clientX - rect.left) / rect.width) * 100;
    const y = ((e.clientY - rect.top) / rect.height) * 100;
    
    setUserEye({ x, y });

    // Check distance between user ocular gaze (mouse cursor) and current target dot
    const dist = Math.sqrt((x - targetDot.x) ** 2 + (y - targetDot.y) ** 2);
    if (dist < 8) {
      // Gaze matched target dot! Progress liveness
      setLivenessProgress(prev => {
        const next = prev + 1;
        if (next >= 100) {
          // Liveness completed! Proceed to scan phase
          playSound('success');
          startBiometricScan();
          return 100;
        }

        // Cycle through target coordinates based on progress thresholds
        if (next === 33) {
          playSound('beep');
          setCurrentLivenessStep(1);
          setTargetDot({ x: livenessSteps[1].targetX, y: livenessSteps[1].targetY });
          setStatusMessage(livenessSteps[1].instruction);
        } else if (next === 66) {
          playSound('beep');
          setCurrentLivenessStep(2);
          setTargetDot({ x: livenessSteps[2].targetX, y: livenessSteps[2].targetY });
          setStatusMessage(livenessSteps[2].instruction);
        }

        return next;
      });
    }
  };

  // Start retinal capturing
  const startBiometricScan = () => {
    setScanState('scanning');
    setScanProgress(0);
    setStatusMessage('Hold still. Capturing vascular retinal mapping...');
  };

  // Scanning simulation
  useEffect(() => {
    if (scanState !== 'scanning') return;

    const timer = setInterval(() => {
      setScanProgress(prev => {
        if (prev % 10 === 0) playSound('scan');
        if (prev >= 100) {
          clearInterval(timer);
          processOcularSignature();
          return 100;
        }
        return prev + 2;
      });
    }, 50);

    return () => clearInterval(timer);
  }, [scanState]);

  // Cryptographic evaluation of template on device
  const processOcularSignature = () => {
    setScanState('processing');
    setStatusMessage('Validating signed hardware payload & anti-spoof checks...');

    setTimeout(() => {
      // Simulate quality and liveness check outcomes based on retry count
      const isSimulationStable = Math.random() > 0.15; // 85% success rate on first try

      if (isSimulationStable || retryCount >= 1) {
        // Success
        setScanState('success');
        playSound('success');
        setStatusMessage('Biometric verified. EMITTED: retina.');
        const fakeSig = `retina_sig_${Math.random().toString(36).substr(2, 12)}_${Date.now()}`;
        onCaptureSuccess(fakeSig, 'Level-3 (Active Saccadic Check)');
      } else {
        // Failed
        const isSpoof = Math.random() > 0.7; // 30% chance of a mock spoof fail
        setRetryCount(prev => prev + 1);
        playSound('fail');

        if (isSpoof) {
          setSpoofDetected(true);
          setFailureType('liveness');
          setScanState('failed');
          setStatusMessage('Spoof threat identified. Alignment vector invalid.');
          onCaptureFail('Liveness verify failed: active tracking vector signature invalid.');
        } else {
          setFailureType('quality');
          setScanState('failed');
          setStatusMessage('Lens glare/retina image contrast insufficient.');
        }
      }
    }, 2000);
  };

  const retryCeremony = () => {
    setSpoofDetected(false);
    setFailureType('none');
    setScanProgress(0);
    setLivenessProgress(0);
    startCeremony();
  };

  return (
    <div id="capture-container" className="bg-slate-950 border border-slate-800 rounded-2xl p-6 max-w-4xl mx-auto shadow-2xl overflow-hidden relative">
      {/* HUD Frame borders */}
      <div className="absolute top-0 left-0 w-8 h-8 border-t-2 border-l-2 border-cyan-500 rounded-tl-lg m-2 pointer-events-none opacity-40" />
      <div className="absolute top-0 right-0 w-8 h-8 border-t-2 border-r-2 border-cyan-500 rounded-tr-lg m-2 pointer-events-none opacity-40" />
      <div className="absolute bottom-0 left-0 w-8 h-8 border-b-2 border-l-2 border-cyan-500 rounded-bl-lg m-2 pointer-events-none opacity-40" />
      <div className="absolute bottom-0 right-0 w-8 h-8 border-b-2 border-r-2 border-cyan-500 rounded-br-lg m-2 pointer-events-none opacity-40" />

      {/* Grid Background */}
      <div className="absolute inset-0 bg-[linear-gradient(to_right,#020617_1px,transparent_1px),linear-gradient(to_bottom,#020617_1px,transparent_1px)] bg-[size:4rem_4rem] [mask-image:radial-gradient(ellipse_60%_50%_at_50%_50%,#000_70%,transparent_100%)] opacity-30" />

      {/* Control Panel Header */}
      <div className="flex items-center justify-between border-b border-slate-800/80 pb-4 mb-6 relative z-10">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-cyan-500/10 border border-cyan-500/20 rounded-lg text-cyan-400">
            <Eye className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider">
              {ceremonyType} CEREMONY • ACTIVE TERMINAL
            </h2>
            <p className="text-xs text-slate-400 font-mono">{device.name} [STATION B3]</p>
          </div>
        </div>

        <div className="flex items-center gap-3">
          <button
            id="btn-toggle-sound"
            type="button"
            onClick={() => setSoundEnabled(!soundEnabled)}
            className="text-slate-400 hover:text-slate-200 p-2 bg-slate-900 border border-slate-800 rounded-lg cursor-pointer"
            title="Toggle Synthesizer Sound"
          >
            {soundEnabled ? <Volume2 className="w-4 h-4 text-emerald-400" /> : <VolumeX className="w-4 h-4 text-slate-500" />}
          </button>
          <button
            id="btn-cancel-capture"
            onClick={onCancel}
            className="text-xs font-mono px-3 py-1.5 rounded border border-slate-800 bg-slate-900 text-slate-400 hover:text-slate-200 hover:bg-slate-800 cursor-pointer"
          >
            Abort Ceremony
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-12 gap-6 relative z-10">
        {/* Main Viewfinder / Canvas Area */}
        <div className="md:col-span-8 bg-slate-950 border border-slate-800/80 rounded-xl p-4 flex flex-col justify-between h-[450px] relative">
          
          {/* Alignment Guidance Overlays */}
          <div className="absolute top-3 left-3 bg-slate-900/90 border border-slate-800 rounded px-2.5 py-1 text-[10px] font-mono text-cyan-400 flex items-center gap-2">
            <Shield className="w-3 h-3 animate-pulse" />
            <span>ENCLAVE LOCKOUT ACTIVE: LEVEL 3 BIOMETRIC CERTIFIED</span>
          </div>

          <div className="absolute bottom-3 right-3 bg-slate-900/90 border border-slate-800 rounded px-2 py-0.5 text-[9px] font-mono text-slate-400">
            {scanState === 'liveness_check' ? `LIVENESS: ${livenessProgress}%` : scanState === 'scanning' ? `SCAN: ${scanProgress}%` : `STATE: ${scanState.toUpperCase()}`}
          </div>

          {/* Interactive Scanning HUD Stage */}
          <div 
            id="ocular-viewfinder"
            ref={trackingAreaRef}
            onMouseMove={handleMouseMove}
            className={`flex-1 w-full flex items-center justify-center relative overflow-hidden rounded-lg bg-slate-950/80 border border-slate-900/80 cursor-none select-none transition-all duration-300 ${
              scanState === 'liveness_check' ? 'border-cyan-500/30 ring-1 ring-cyan-500/10' : ''
            }`}
          >
            {/* Ambient Eye Illustration / Ring Background */}
            <div className="relative w-72 h-72 rounded-full border border-slate-800/60 flex items-center justify-center">
              
              {/* Outer Alignment Circle */}
              <div className="absolute inset-4 rounded-full border border-dashed border-slate-700/40 animate-[spin_40s_linear_infinite]" />
              
              {/* Glowing Scan Ring */}
              <div className={`absolute inset-8 rounded-full border-2 transition-all duration-300 ${
                scanState === 'aligning' ? 'border-amber-500/30 border-dashed animate-pulse' :
                scanState === 'liveness_check' ? 'border-cyan-500/40 animate-pulse' :
                scanState === 'scanning' ? 'border-emerald-500/60 ring-2 ring-emerald-500/10' :
                scanState === 'success' ? 'border-emerald-500' : 'border-slate-800'
              }`} />

              {/* Grid calibration crosshair */}
              <div className="absolute w-full h-[1px] bg-slate-800/40" />
              <div className="absolute h-full w-[1px] bg-slate-800/40" />

              {/* Eye Vector Graphic representation */}
              <div className="absolute w-36 h-20 rounded-full border border-slate-700/30 flex items-center justify-center overflow-hidden">
                <div className="w-16 h-16 rounded-full border border-slate-600/40 bg-slate-950/40 flex items-center justify-center">
                  <div className="w-10 h-10 rounded-full border border-dashed border-slate-500/40" />
                </div>
              </div>

              {/* USER SIMULATED EYE Gaze Cursor (Mouse Tracking) */}
              <AnimatePresence>
                {(scanState === 'aligning' || scanState === 'liveness_check' || scanState === 'scanning' || scanState === 'success') && (
                  <motion.div
                    style={{ 
                      position: 'absolute',
                      left: `${userEye.x}%`,
                      top: `${userEye.y}%`,
                      transform: 'translate(-50%, -50%)',
                      zIndex: 30
                    }}
                    transition={{ type: 'spring', stiffness: 220, damping: 25 }}
                  >
                    {/* Inner Pupil / Biometric Anchor */}
                    <div className="relative flex items-center justify-center">
                      <div className={`w-10 h-10 rounded-full border-2 bg-slate-950/90 flex items-center justify-center shadow-lg transition-colors duration-300 ${
                        isEyeAligned || scanState === 'liveness_check' || scanState === 'scanning' ? 'border-cyan-400' : 'border-amber-400'
                      }`}>
                        <div className={`w-3 h-3 rounded-full ${
                          isEyeAligned || scanState === 'liveness_check' || scanState === 'scanning' ? 'bg-cyan-400 shadow-lg shadow-cyan-400/50' : 'bg-amber-400'
                        }`} />
                      </div>
                      
                      {/* Compass Pointer / Reticle */}
                      <div className={`absolute w-14 h-14 rounded-full border border-dashed transition-colors ${
                        isEyeAligned || scanState === 'liveness_check' || scanState === 'scanning' ? 'border-cyan-400/50' : 'border-amber-400/50'
                      }`} />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* ACTIVE LIVENESS CHALLENGE TARGET DOT */}
              <AnimatePresence>
                {scanState === 'liveness_check' && (
                  <motion.div
                    id="liveness-dot"
                    style={{
                      position: 'absolute',
                      left: `${targetDot.x}%`,
                      top: `${targetDot.y}%`,
                      transform: 'translate(-50%, -50%)',
                      zIndex: 40
                    }}
                    initial={{ scale: 0 }}
                    animate={{ scale: [1, 1.4, 1] }}
                    transition={{ repeat: Infinity, duration: 1.5 }}
                  >
                    <div className="relative flex items-center justify-center">
                      {/* Active target element */}
                      <div className="w-5 h-5 rounded-full bg-emerald-500/20 border-2 border-emerald-400 flex items-center justify-center shadow-lg shadow-emerald-400/40">
                        <div className="w-1.5 h-1.5 rounded-full bg-emerald-400" />
                      </div>
                      
                      {/* Pulse ring */}
                      <div className="absolute w-10 h-10 rounded-full border border-emerald-400/30 animate-ping" />
                    </div>
                  </motion.div>
                )}
              </AnimatePresence>

              {/* Scanning laser sweep line animation */}
              <AnimatePresence>
                {scanState === 'scanning' && (
                  <motion.div 
                    className="absolute left-0 right-0 h-0.5 bg-gradient-to-r from-transparent via-emerald-400 to-transparent shadow-[0_0_8px_#34d399] z-20 pointer-events-none"
                    initial={{ top: '20%' }}
                    animate={{ top: '80%' }}
                    transition={{ repeat: Infinity, repeatType: 'reverse', duration: 1.5, ease: 'easeInOut' }}
                  />
                )}
              </AnimatePresence>
            </div>

            {/* Simulated camera video overlay or static eye placeholder when idle */}
            {scanState === 'idle' && (
              <div className="flex flex-col items-center gap-4 text-center p-6 relative z-10 bg-slate-950/80 max-w-sm rounded-xl border border-slate-800">
                <div className="w-16 h-16 rounded-full bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400">
                  <Eye className="w-8 h-8 animate-pulse" />
                </div>
                <div>
                  <h3 className="text-xs font-mono font-semibold text-slate-100 uppercase tracking-wider">Ocular Sensor Offline</h3>
                  <p className="text-xs text-slate-400 mt-1 font-sans">
                    Alignment plane calibrators loaded. Align your head with the physical scanning station before activating.
                  </p>
                </div>
                <button
                  id="btn-start-ceremony"
                  onClick={startCeremony}
                  className="px-5 py-2 rounded bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase tracking-wider transition-colors cursor-pointer"
                >
                  Start Scanning Ceremony
                </button>
              </div>
            )}

            {/* Processing State HUD Overlay */}
            {scanState === 'processing' && (
              <div className="absolute inset-0 bg-slate-950/80 flex flex-col items-center justify-center gap-4 z-50">
                <RefreshCw className="w-10 h-10 text-cyan-400 animate-spin" />
                <div className="text-center font-mono space-y-1">
                  <p className="text-xs text-slate-200 uppercase tracking-wider animate-pulse">Running Cryptographic Proof Checks</p>
                  <p className="text-[10px] text-slate-500">Checking biometric zero-trust signatures...</p>
                </div>
              </div>
            )}

            {/* Error state HUD panel */}
            {scanState === 'failed' && (
              <div className="absolute inset-0 bg-slate-950/95 flex flex-col items-center justify-center gap-4 p-6 z-50">
                <div className="p-3 bg-red-500/10 border border-red-500/20 rounded-full text-red-400">
                  <AlertTriangle className="w-8 h-8" />
                </div>
                <div className="text-center max-w-sm font-mono space-y-1.5">
                  <h4 className="text-xs font-bold text-red-400 uppercase tracking-wider">
                    {failureType === 'liveness' ? 'Active Liveness Fault' : 'Optical Contrast Fault'}
                  </h4>
                  <p className="text-xs text-slate-300 font-sans leading-relaxed">
                    {failureType === 'liveness' 
                      ? 'Ocular saccade rate or dot correlation check failed. Movement tracking does not match dynamic challenge target.'
                      : 'Optical glare detected or pupil alignment lost. Please hold head completely still and repeat the alignment phase.'}
                  </p>
                </div>
                <div className="flex gap-3 mt-2">
                  <button
                    id="btn-retry-ceremony"
                    onClick={retryCeremony}
                    className="px-4 py-2 bg-slate-900 border border-slate-800 hover:border-slate-700 text-slate-200 hover:text-white font-mono text-xs font-bold rounded uppercase tracking-wider transition-all cursor-pointer"
                  >
                    Repeat Scan
                  </button>
                  <button
                    id="btn-failed-fallback"
                    onClick={() => onCaptureFail(spoofDetected ? 'Liveness lock' : 'Contrast timeout')}
                    className="px-4 py-2 bg-red-950/30 hover:bg-red-950/50 border border-red-900/40 text-red-400 font-mono text-xs font-bold rounded uppercase tracking-wider transition-colors cursor-pointer"
                  >
                    Bypass to Fallback
                  </button>
                </div>
              </div>
            )}
          </div>

          {/* Status Message Footer */}
          <div className="border-t border-slate-900 pt-3.5 mt-3 flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className={`w-2 h-2 rounded-full ${
                scanState === 'success' ? 'bg-emerald-400' :
                scanState === 'failed' ? 'bg-red-400' :
                scanState === 'idle' ? 'bg-slate-700' : 'bg-cyan-400 animate-pulse'
              }`} />
              <span className="text-[11px] font-mono text-slate-300 uppercase tracking-wide">
                {statusMessage}
              </span>
            </div>
            {retryCount > 0 && (
              <span className="text-[10px] font-mono text-amber-500 bg-amber-500/10 border border-amber-500/20 px-2 py-0.5 rounded">
                RETRY ATTEMPT: {retryCount}
              </span>
            )}
          </div>
        </div>

        {/* HUD Operations Instructions Sidepanel */}
        <div className="md:col-span-4 flex flex-col justify-between space-y-4">
          <div className="bg-slate-900 border border-slate-800 rounded-xl p-5 space-y-4 flex-1">
            <h3 className="text-xs font-mono uppercase text-cyan-400 tracking-wider border-b border-slate-800 pb-2 flex items-center justify-between">
              <span>Biometric Ceremony Guides</span>
              <Info className="w-3.5 h-3.5 text-slate-500" />
            </h3>

            {/* Static walkthrough details based on current active step */}
            <div className="space-y-4 text-xs">
              <div className={`p-3 rounded-lg border transition-all duration-300 ${
                scanState === 'idle' ? 'border-cyan-500/30 bg-cyan-500/5 text-cyan-200' : 'border-slate-800/80 bg-slate-950/30 text-slate-400'
              }`}>
                <p className="font-mono font-semibold uppercase text-[10px] text-slate-300">Phase 1: Pre-Ceremony Alignment</p>
                <p className="mt-1 font-sans leading-relaxed text-[11px]">
                  Click the "Start Scanning Ceremony" button in the HUD. The verifier will automatically begin head positioning guidance.
                </p>
              </div>

              <div className={`p-3 rounded-lg border transition-all duration-300 ${
                scanState === 'aligning' ? 'border-cyan-500/30 bg-cyan-500/5 text-cyan-200' : 'border-slate-800/80 bg-slate-950/30 text-slate-400'
              }`}>
                <p className="font-mono font-semibold uppercase text-[10px] text-slate-300">Phase 2: Center Alignment</p>
                <p className="mt-1 font-sans leading-relaxed text-[11px]">
                  The scanner matches your pupil axis. Gaze vectors are checking that your head is locked into the focal plane.
                </p>
              </div>

              <div className={`p-3 rounded-lg border transition-all duration-300 ${
                scanState === 'liveness_check' ? 'border-cyan-500/30 bg-cyan-500/5 text-cyan-200' : 'border-slate-800/80 bg-slate-950/30 text-slate-400'
              }`}>
                <p className="font-mono font-semibold uppercase text-[10px] text-emerald-400 flex items-center justify-between">
                  <span>Phase 3: Active Liveness</span>
                  <span className="font-mono text-[9px] bg-emerald-500/10 border border-emerald-500/20 px-1 rounded animate-pulse">INTERACTIVE TASK</span>
                </p>
                <p className="mt-1 font-sans leading-relaxed text-[11px] text-slate-300">
                  👉 <span className="text-cyan-400 font-semibold font-mono">Action:</span> Move your mouse cursor into the viewfinder and 
                  <strong> hover your circular pupil cursor on the pulsing green target dot</strong> as it hops to verify muscular liveness!
                </p>
                
                {/* Visual Step indicators */}
                <div className="flex gap-1.5 mt-2">
                  <div className={`flex-1 h-1 rounded ${currentLivenessStep >= 0 && scanState === 'liveness_check' ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-slate-800'}`} />
                  <div className={`flex-1 h-1 rounded ${currentLivenessStep >= 1 && scanState === 'liveness_check' ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-slate-800'}`} />
                  <div className={`flex-1 h-1 rounded ${currentLivenessStep >= 2 && scanState === 'liveness_check' ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' : 'bg-slate-800'}`} />
                </div>
              </div>

              <div className={`p-3 rounded-lg border transition-all duration-300 ${
                scanState === 'scanning' ? 'border-cyan-500/30 bg-cyan-500/5 text-cyan-200' : 'border-slate-800/80 bg-slate-950/30 text-slate-400'
              }`}>
                <p className="font-mono font-semibold uppercase text-[10px] text-slate-300">Phase 4: Retinal Vascular Scan</p>
                <p className="mt-1 font-sans leading-relaxed text-[11px]">
                  Laser sweep captures your unique eye pattern. Zero-trust template generation begins. Hold perfectly still.
                </p>
              </div>
            </div>
          </div>

          {/* Secure Enclave Spec disclosure */}
          <div className="bg-slate-950/60 p-4 border border-slate-800 rounded-xl space-y-2 text-[10px] font-mono text-slate-500 leading-normal">
            <div className="flex items-center gap-1.5 text-cyan-500/80 uppercase tracking-wider text-[9px]">
              <Shield className="w-3.5 h-3.5" />
              <span>Biometric Sandbox Guarantee</span>
            </div>
            <p>
              Under biometric regulations, raw retinal templates remain strictly isolated. 
              The application only consumes the cryptographic verification payload representing the 'retina' authentication factor.
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}
