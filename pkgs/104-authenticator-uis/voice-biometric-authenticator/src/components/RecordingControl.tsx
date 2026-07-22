import React, { useRef, useEffect, useState } from 'react';
import { Mic, Circle, Square, RefreshCw, Volume2, ShieldAlert, CheckCircle2, AlertTriangle, AlertCircle } from 'lucide-react';

interface RecordingControlProps {
  isRecording: boolean;
  audioStats: {
    volume: number;
    db: number;
    speechDetected: boolean;
    frequencyData: Uint8Array;
  };
  promptText: string;
  onStartRecord: () => void;
  onStopRecord: () => void;
  currentStep: number;
  totalSteps: number;
  onSampleCompleted: (duration: number, noiseDb: number, qualityScore: number) => void;
  onSimulateSpoof: () => void;
  onSimulateNoise: () => void;
  onResetStep: () => void;
  ambientNoiseDb: number;
  noiseThreshold: number;
  simulatedNoise: boolean;
}

export default function RecordingControl({
  isRecording,
  audioStats,
  promptText,
  onStartRecord,
  onStopRecord,
  currentStep,
  totalSteps,
  onSampleCompleted,
  onSimulateSpoof,
  onSimulateNoise,
  onResetStep,
  ambientNoiseDb,
  noiseThreshold,
  simulatedNoise,
}: RecordingControlProps) {
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const [recordSeconds, setRecordSeconds] = useState(0);
  const timerRef = useRef<NodeJS.Timeout | null>(null);
  const [speechCount, setSpeechCount] = useState(0); // tracks ticks of speaking
  const [feedback, setFeedback] = useState<'idle' | 'too_quiet' | 'perfect' | 'too_noisy'>('idle');

  // Timer loop for recording seconds
  useEffect(() => {
    if (isRecording) {
      setRecordSeconds(0);
      setSpeechCount(0);
      timerRef.current = setInterval(() => {
        setRecordSeconds((prev) => prev + 1);
      }, 1000);
    } else {
      if (timerRef.current) {
        clearInterval(timerRef.current);
        timerRef.current = null;
      }
    }
    return () => {
      if (timerRef.current) clearInterval(timerRef.current);
    };
  }, [isRecording]);

  // Audio level checks and guidance feedback
  useEffect(() => {
    if (!isRecording) {
      setFeedback('idle');
      return;
    }

    if (audioStats.volume > 0) {
      if (audioStats.volume > 15 && audioStats.volume < 65) {
        setFeedback('perfect');
        setSpeechCount((c) => c + 1);
      } else if (audioStats.volume >= 65) {
        setFeedback('too_noisy');
      } else {
        setFeedback('too_quiet');
      }
    }
  }, [audioStats.volume, isRecording]);

  // Canvas Drawing of Real-time frequency bars
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    let animationFrameId: number;
    const width = canvas.width;
    const height = canvas.height;

    const draw = () => {
      ctx.clearRect(0, 0, width, height);

      const fData = audioStats.frequencyData;
      const barCount = 42;
      const barWidth = width / barCount - 1.5;

      // Draw neutral grid background
      ctx.strokeStyle = 'rgba(30, 41, 59, 0.4)';
      ctx.lineWidth = 1;
      for (let i = 1; i < 4; i++) {
        const y = (height / 4) * i;
        ctx.beginPath();
        ctx.moveTo(0, y);
        ctx.lineTo(width, y);
        ctx.stroke();
      }

      if (!isRecording || fData.length === 0) {
        // Draw standard flat sine curve
        ctx.beginPath();
        ctx.strokeStyle = 'rgba(79, 70, 229, 0.3)';
        ctx.lineWidth = 2;
        ctx.moveTo(0, height / 2);
        for (let i = 0; i < width; i++) {
          const y = height / 2 + Math.sin(i * 0.05) * 4;
          ctx.lineTo(i, y);
        }
        ctx.stroke();
      } else {
        // Draw frequency bars reflecting actual audio analysis
        for (let i = 0; i < barCount; i++) {
          // Normalize indices across the frequency buffer
          const dataIndex = Math.floor((i / barCount) * fData.length);
          const value = fData[dataIndex] || 0;
          
          // Map value (0-255) to bar height
          const barHeight = Math.min(height - 6, (value / 255) * height * 0.95 + 2);
          const x = i * (barWidth + 1.5);
          const y = height / 2 - barHeight / 2;

          // Color gradient representing activity
          const gradient = ctx.createLinearGradient(0, y, 0, y + barHeight);
          if (audioStats.volume > 65) {
            gradient.addColorStop(0, '#f43f5e'); // rose
            gradient.addColorStop(1, '#9f1239');
          } else if (audioStats.speechDetected) {
            gradient.addColorStop(0, '#10b981'); // emerald
            gradient.addColorStop(1, '#047857');
          } else {
            gradient.addColorStop(0, '#6366f1'); // indigo
            gradient.addColorStop(1, '#3730a3');
          }

          ctx.fillStyle = gradient;
          // Rounded bars
          ctx.beginPath();
          ctx.roundRect(x, y, barWidth, barHeight, 4);
          ctx.fill();
        }
      }

      animationFrameId = requestAnimationFrame(draw);
    };

    draw();

    return () => {
      cancelAnimationFrame(animationFrameId);
    };
  }, [audioStats.frequencyData, isRecording, audioStats.volume, audioStats.speechDetected]);

  // Handle saving the sample
  const handleStopAndSave = () => {
    // Capture the active stats before we stop recording and reset state
    const currentDb = audioStats.db;
    const currentFeedback = feedback;
    const currentSpeechCount = speechCount;

    onStopRecord();

    const duration = Math.max(1, recordSeconds);
    // Calculated mock noise level matching the environmental db checks
    const finalDb = currentDb > -100 ? Math.round(currentDb) : -55;
    
    // Evaluate quality score based on speaking activity and noise feedback
    let score = 92;
    if (currentSpeechCount < 3) {
      score -= 30; // Not enough speech content
    }
    if (currentFeedback === 'too_noisy') {
      score -= 25; // Saturated input or noise
    }
    if (finalDb > -35) {
      score -= 20;
    }
    score = Math.max(25, Math.min(100, score + Math.round(Math.random() * 5)));

    onSampleCompleted(duration, finalDb, score);
  };

  const getGuidanceBadge = () => {
    if (!isRecording) {
      return (
        <span className="bg-slate-950/80 border border-slate-800 text-slate-400 px-3 py-1 rounded-full text-xs flex items-center gap-1">
          <Circle className="w-3 h-3 fill-slate-600 border-none" />
          <span>Awaiting Input</span>
        </span>
      );
    }

    switch (feedback) {
      case 'perfect':
        return (
          <span className="bg-emerald-500/10 border border-emerald-500/30 text-emerald-400 px-3 py-1 rounded-full text-xs flex items-center gap-1 font-medium animate-pulse">
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>Speech Detected: Stable Level</span>
          </span>
        );
      case 'too_quiet':
        return (
          <span className="bg-indigo-500/10 border border-indigo-500/30 text-indigo-400 px-3 py-1 rounded-full text-xs flex items-center gap-1 font-medium">
            <Volume2 className="w-3.5 h-3.5 animate-bounce" />
            <span>Please speak up: Input level low</span>
          </span>
        );
      case 'too_noisy':
        return (
          <span className="bg-rose-500/10 border border-rose-500/30 text-rose-400 px-3 py-1 rounded-full text-xs flex items-center gap-1 font-medium">
            <ShieldAlert className="w-3.5 h-3.5" />
            <span>Level High: Clip/Distortion risk</span>
          </span>
        );
      default:
        return (
          <span className="bg-slate-950 border border-slate-800 text-slate-400 px-3 py-1 rounded-full text-xs flex items-center gap-1">
            <RefreshCw className="w-3 h-3 animate-spin" />
            <span>Listening...</span>
          </span>
        );
    }
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-2xl mx-auto" id="recording-control-container">
      {/* Step Indicator */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
        <div>
          <h4 className="font-sans font-semibold tracking-tight text-slate-200 text-sm">
            Enrollment Sample Capture
          </h4>
          <p className="font-mono text-xs text-slate-500 mt-0.5">Approved verifier sandboxing boundary</p>
        </div>
        <div className="flex items-center gap-1">
          {Array.from({ length: totalSteps }).map((_, idx) => (
            <div
              key={idx}
              className={`h-1.5 rounded-full transition-all duration-300 ${
                idx + 1 === currentStep
                  ? 'w-6 bg-indigo-500'
                  : idx + 1 < currentStep
                  ? 'w-2.5 bg-emerald-500'
                  : 'w-2.5 bg-slate-800'
              }`}
            />
          ))}
          <span className="font-mono text-xs text-indigo-400 ml-2">
            {currentStep}/{totalSteps}
          </span>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Challenge Phrase Box */}
        <div className="bg-slate-950 rounded-xl border border-slate-850 p-5 space-y-3 relative group">
          <span className="absolute top-3 left-4 font-mono text-[10px] text-slate-600 uppercase tracking-wider">
            Randomized Challenge Prompt
          </span>
          <div className="pt-3 text-center px-2">
            <p className="font-sans text-lg font-medium text-slate-100 tracking-tight leading-relaxed select-all">
              &ldquo;{promptText}&rdquo;
            </p>
          </div>
          <div className="flex justify-between items-center text-[10px] text-slate-500 font-mono pt-2 border-t border-slate-900">
            <span>Read phrase naturally, without whispering.</span>
            <span>Est. duration: 3-5s</span>
          </div>
        </div>

        {/* Ambient Noise Level Policy check feedback */}
        {(simulatedNoise || (ambientNoiseDb > noiseThreshold && ambientNoiseDb > -90)) && (
          <div className="bg-amber-500/10 border border-amber-500/20 p-4 rounded-xl flex gap-3 text-amber-400 text-xs leading-relaxed animate-fade-in" id="recording-noise-warning">
            <AlertTriangle className="w-5 h-5 shrink-0 text-amber-500" />
            <div>
              <strong className="text-amber-300 font-sans block mb-1">
                Potential Rejection Risk: High Background Noise Floor
              </strong>
              <p className="text-slate-400">
                Your ambient noise floor is measured at{' '}
                <span className="font-mono text-amber-300 font-bold">{Math.round(simulatedNoise ? -35 : ambientNoiseDb)} dB</span>,
                which exceeds SentryVoice's security policy limit of{' '}
                <span className="font-mono text-indigo-400 font-bold">{noiseThreshold} dB</span>.
              </p>
              <p className="text-slate-500 mt-1">
                Background hums, fans, or acoustic reflections may trigger an automatic rejection. We recommend moving to a quieter space before completing this session.
              </p>
            </div>
          </div>
        )}

        {/* Real-time WebAudio Visualizer Canvas */}
        <div className="relative h-28 bg-slate-950 rounded-xl overflow-hidden border border-slate-850 flex items-center justify-center">
          <canvas
            ref={canvasRef}
            width={580}
            height={112}
            className="w-full h-full block"
          />

          {/* Active Noise Violation warning tag */}
          {(simulatedNoise || (ambientNoiseDb > noiseThreshold && ambientNoiseDb > -90)) && (
            <div className="absolute top-3 left-3 flex items-center gap-1.5 bg-amber-500/15 border border-amber-500/30 px-2.5 py-1 rounded-md font-mono text-[9px] text-amber-400 uppercase tracking-wider animate-pulse">
              <ShieldAlert className="w-3.5 h-3.5 text-amber-500" />
              <span>Excessive Noise Warning</span>
            </div>
          )}

          {/* Timing / Status Indicators overlays */}
          {isRecording && (
            <div className="absolute top-3 right-3 flex items-center gap-2 bg-rose-500/10 border border-rose-500/20 px-2 py-0.5 rounded-md font-mono text-[10px] text-rose-400">
              <span className="h-1.5 w-1.5 rounded-full bg-rose-500 animate-pulse" />
              <span>REC 0:0{recordSeconds}s</span>
            </div>
          )}

          {/* Guidance Status badge Overlay */}
          <div className="absolute bottom-3 left-1/2 -translate-x-1/2">
            {getGuidanceBadge()}
          </div>
        </div>

        {/* Micro-Interaction Guidance */}
        {isRecording && recordSeconds > 1 && speechCount === 0 && (
          <div className="bg-indigo-500/5 border border-indigo-500/10 text-indigo-400 text-xs p-3 rounded-lg flex items-center gap-2">
            <AlertTriangle className="w-4 h-4 shrink-0" />
            <span>No speech registered yet. Please read the highlighted prompt text aloud.</span>
          </div>
        )}

        {/* Primary Recording controls */}
        <div className="flex flex-col items-center gap-4 py-2">
          {!isRecording ? (
            <button
              type="button"
              onClick={onStartRecord}
              className="group h-16 w-16 bg-gradient-to-tr from-indigo-600 to-indigo-500 hover:from-indigo-500 hover:to-indigo-400 rounded-full flex items-center justify-center text-slate-950 shadow-lg shadow-indigo-500/20 active:scale-95 transition-all"
              id="btn-recording-start"
            >
              <Mic className="w-7 h-7 text-slate-950 transition-transform group-hover:scale-110" />
            </button>
          ) : (
            <button
              type="button"
              onClick={handleStopAndSave}
              className="h-16 w-16 bg-rose-500 hover:bg-rose-400 rounded-full flex items-center justify-center text-slate-950 shadow-lg shadow-rose-500/20 active:scale-95 transition-all animate-pulse"
              id="btn-recording-stop"
            >
              <Square className="w-6 h-6 text-slate-950" />
            </button>
          )}

          <p className="font-mono text-xs text-slate-400 uppercase tracking-widest">
            {!isRecording ? 'Click to Start Voice Capture' : 'Click to Save Sample'}
          </p>
        </div>

        {/* Simulation testing tools block - kept clean and compact */}
        <div className="bg-slate-950/40 border border-slate-800/80 p-4 rounded-xl space-y-3">
          <div className="flex justify-between items-center">
            <span className="font-sans font-semibold text-slate-300 text-xs flex items-center gap-1.5">
              <AlertCircle className="w-3.5 h-3.5 text-indigo-400" />
              <span>Biometric Failure Simulation Deck</span>
            </span>
            <span className="font-mono text-[9px] bg-slate-800 px-2 py-0.5 rounded text-slate-400">Sandbox Controls</span>
          </div>
          <p className="text-[11px] text-slate-500 leading-normal">
            Force adverse test criteria to review secure retry and error handlers directly inside the front-end boundaries.
          </p>
          <div className="grid grid-cols-3 gap-2">
            <button
              type="button"
              onClick={onSimulateSpoof}
              className="bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] text-rose-400 py-1.5 px-2 rounded-lg font-mono transition-colors text-left flex flex-col justify-between"
              id="btn-recording-sim-spoof"
            >
              <span>1. Spoof Suspicion</span>
              <span className="text-[9px] text-slate-500 mt-1">Deepfake signature</span>
            </button>
            <button
              type="button"
              onClick={onSimulateNoise}
              className="bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] text-amber-400 py-1.5 px-2 rounded-lg font-mono transition-colors text-left flex flex-col justify-between"
              id="btn-recording-sim-noise"
            >
              <span>2. Ambient Noise</span>
              <span className="text-[9px] text-slate-500 mt-1">Loud background</span>
            </button>
            <button
              type="button"
              onClick={onResetStep}
              className="bg-slate-900 border border-slate-800 hover:bg-slate-800 text-[10px] text-indigo-400 py-1.5 px-2 rounded-lg font-mono transition-colors text-left flex flex-col justify-between"
              id="btn-recording-reset"
            >
              <span>3. Reset Step</span>
              <span className="text-[9px] text-slate-500 mt-1">Clear active profile</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
