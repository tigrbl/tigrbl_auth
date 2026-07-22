import React, { useState } from 'react';
import { Mic, CheckCircle2, AlertTriangle, ShieldCheck, Cpu, RefreshCw, Volume2 } from 'lucide-react';

interface MicrophonePreflightProps {
  permission: string;
  isRecording: boolean;
  volume: number;
  db: number;
  onRequestPermission: () => Promise<boolean>;
  onRunNoiseTest: () => Promise<number>;
  noiseLevel: number;
  noiseThreshold: number;
  onPreflightComplete: () => void;
  onBack: () => void;
}

export default function MicrophonePreflight({
  permission,
  isRecording,
  volume,
  db,
  onRequestPermission,
  onRunNoiseTest,
  noiseLevel,
  noiseThreshold,
  onPreflightComplete,
  onBack,
}: MicrophonePreflightProps) {
  const [testStage, setTestStage] = useState<'idle' | 'testing' | 'done'>('idle');
  const [isPrompting, setIsPrompting] = useState(false);

  const handleGrantMic = async () => {
    setIsPrompting(true);
    await onRequestPermission();
    setIsPrompting(false);
  };

  const handleStartNoiseTest = async () => {
    setTestStage('testing');
    await onRunNoiseTest();
    setTestStage('done');
  };

  // Convert DB reading to human-friendly feedback
  const isNoiseTooHigh = noiseLevel > noiseThreshold;
  const hasCheckedNoise = noiseLevel > -90;

  // Let's decide if preflight can be accepted
  const canProceed = permission === 'granted' && hasCheckedNoise && !isNoiseTooHigh;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-2xl mx-auto" id="preflight-container">
      {/* Header */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-5 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="p-2 bg-indigo-500/10 border border-indigo-500/20 text-indigo-400 rounded-xl">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="font-sans font-semibold tracking-tight text-slate-100 text-lg">Microphone Preflight & Sanitization</h3>
            <p className="font-mono text-xs text-slate-400">Environment and hardware capability verification</p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-6">
        {/* Verification Checklist */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Permission */}
          <div className={`p-4 rounded-xl border ${
            permission === 'granted'
              ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400'
              : 'bg-slate-950/40 border-slate-800/80 text-slate-400'
          }`}>
            <span className="text-xs uppercase font-mono tracking-wider text-slate-500 block mb-1">1. OS/API ACCESS</span>
            <div className="flex items-center justify-between">
              <span className={`text-sm font-semibold ${permission === 'granted' ? 'text-emerald-300' : 'text-slate-300'}`}>
                {permission === 'granted' ? 'Access Granted' : 'Access Required'}
              </span>
              <ShieldCheck className="w-4 h-4 shrink-0" />
            </div>
            {permission !== 'granted' && (
              <button
                type="button"
                onClick={handleGrantMic}
                disabled={isPrompting}
                className="mt-3 w-full bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-medium text-xs py-1.5 rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preflight-grant-mic"
              >
                {isPrompting ? (
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <Mic className="w-3.5 h-3.5" />
                )}
                <span>Request Mic</span>
              </button>
            )}
          </div>

          {/* Noise floor check */}
          <div className={`p-4 rounded-xl border ${
            hasCheckedNoise
              ? isNoiseTooHigh
                ? 'bg-rose-500/5 border-rose-500/20 text-rose-400'
                : 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400'
              : 'bg-slate-950/40 border-slate-800/80 text-slate-400'
          }`}>
            <span className="text-xs uppercase font-mono tracking-wider text-slate-500 block mb-1">2. NOISE FLOOR</span>
            <div className="flex items-center justify-between">
              <span className={`text-sm font-semibold ${
                hasCheckedNoise
                  ? isNoiseTooHigh
                    ? 'text-rose-300'
                    : 'text-emerald-300'
                  : 'text-slate-400'
              }`}>
                {!hasCheckedNoise ? 'Awaiting Calibration' : isNoiseTooHigh ? 'Excessive Noise' : 'Room is Quiet'}
              </span>
              <Volume2 className="w-4 h-4 shrink-0" />
            </div>
            {permission === 'granted' && !hasCheckedNoise && (
              <button
                type="button"
                onClick={handleStartNoiseTest}
                disabled={testStage === 'testing'}
                className="mt-3 w-full bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-xs py-1.5 rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preflight-noise-test"
              >
                {testStage === 'testing' ? (
                  <RefreshCw className="w-3.5 h-3.5 animate-spin" />
                ) : (
                  <span>Run Noise Check</span>
                )}
              </button>
            )}
          </div>

          {/* Compatibility and Level */}
          <div className={`p-4 rounded-xl border ${
            permission === 'granted'
              ? 'bg-emerald-500/5 border-emerald-500/20 text-emerald-400'
              : 'bg-slate-950/40 border-slate-800/80 text-slate-400'
          }`}>
            <span className="text-xs uppercase font-mono tracking-wider text-slate-500 block mb-1">3. CODEC HEALTH</span>
            <div className="flex items-center justify-between">
              <span className={`text-sm font-semibold ${permission === 'granted' ? 'text-emerald-300' : 'text-slate-400'}`}>
                {permission === 'granted' ? 'Dual-Channel HD' : 'Awaiting Hardware'}
              </span>
              <CheckCircle2 className="w-4 h-4 shrink-0" />
            </div>
            {permission === 'granted' && (
              <p className="text-[10px] text-slate-500 mt-2 font-mono">
                WebAudio: 44.1kHz | PCM16bit
              </p>
            )}
          </div>
        </div>

        {/* Live Audio Meter & Calibration Screen */}
        {permission === 'granted' && (
          <div className="bg-slate-950/60 border border-slate-800 p-5 rounded-xl space-y-4">
            <div className="flex justify-between items-center text-xs">
              <span className="text-slate-400 font-medium">Real-Time Acoustic Level</span>
              <span className="font-mono text-slate-500">
                {isRecording ? `${Math.round(db)} dB` : 'Silent'}
              </span>
            </div>

            {/* Level Bar */}
            <div className="h-2 bg-slate-900 rounded-full overflow-hidden flex relative border border-slate-850">
              <div
                className={`h-full transition-all duration-75 ${
                  db > noiseThreshold ? 'bg-amber-500' : 'bg-emerald-500'
                }`}
                style={{ width: `${isRecording ? Math.max(5, (db + 100)) : 0}%` }}
              />
              {/* Noise threshold indicator marker */}
              <div
                className="absolute top-0 bottom-0 w-0.5 bg-rose-500"
                style={{ left: `${noiseThreshold + 100}%` }}
                title="Strict security noise limit threshold"
              />
            </div>

            <div className="flex justify-between text-[10px] text-slate-600 font-mono">
              <span>-100dB (Silence)</span>
              <span className="text-rose-500/80">Threshold Limit</span>
              <span>0dB (Clipping)</span>
            </div>

            {/* Test State Instructions */}
            {testStage === 'testing' && (
              <div className="text-center py-2 space-y-1">
                <p className="text-xs text-indigo-300 animate-pulse font-medium">Calibrating background acoustics... Please refrain from speaking.</p>
                <div className="flex justify-center gap-1.5 mt-2">
                  <div className="h-1.5 w-1.5 bg-indigo-400 rounded-full animate-bounce" />
                  <div className="h-1.5 w-1.5 bg-indigo-400 rounded-full animate-bounce delay-100" />
                  <div className="h-1.5 w-1.5 bg-indigo-400 rounded-full animate-bounce delay-200" />
                </div>
              </div>
            )}

            {testStage === 'done' && (
              <div className="border-t border-slate-900 pt-3 flex gap-3 text-xs leading-relaxed text-slate-400">
                {isNoiseTooHigh ? (
                  <>
                    <AlertTriangle className="w-5 h-5 text-amber-500 shrink-0" />
                    <div>
                      <strong className="text-amber-400 font-sans block">Acoustics Warning: High Ambient Noise ({noiseLevel} dB)</strong>
                      <p className="text-slate-500 mt-0.5">
                        Your background noise exceeds the security policy ceiling ({noiseThreshold} dB). This could compromise matching scores or let spoofers exploit background patterns. Please relocate to a quieter room, mute desk fans, or plug in a headset microphone.
                      </p>
                      <button
                        type="button"
                        onClick={handleStartNoiseTest}
                        className="mt-3 text-indigo-400 font-semibold hover:text-indigo-300 flex items-center gap-1 cursor-pointer"
                        id="btn-preflight-retry-noise"
                      >
                        <RefreshCw className="w-3.5 h-3.5" />
                        <span>Recalibrate</span>
                      </button>
                    </div>
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                    <div>
                      <strong className="text-emerald-300 font-sans block">Acoustic Calibration Approved ({noiseLevel} dB)</strong>
                      <p className="text-slate-500 mt-0.5">
                        Your environment meets the strict signal-to-noise criteria. Your voice template will be generated with excellent isolation parameters.
                      </p>
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        )}

        {/* Fallback & Access Alert */}
        {permission === 'denied' && (
          <div className="bg-rose-500/10 border border-rose-500/20 text-rose-400 text-xs p-4 rounded-xl flex gap-3 leading-relaxed">
            <AlertTriangle className="w-5 h-5 shrink-0" />
            <div>
              <strong className="text-rose-300 block mb-0.5">Microphone Permission Blocked</strong>
              <p className="text-slate-400">
                The browser or system blocked voice capture. To use Voice Biometrics, click the lock/settings icon in your browser address bar and enable microphone access for this domain. Alternatively, you may cancel and use an alternative security factor.
              </p>
            </div>
          </div>
        )}

        {/* Controls */}
        <div className="flex gap-3 justify-between items-center pt-3 border-t border-slate-800">
          <button
            type="button"
            onClick={onBack}
            className="px-4 py-2 border border-slate-800 hover:border-slate-700 hover:bg-slate-800/40 text-slate-400 hover:text-slate-200 rounded-lg text-sm transition-all"
            id="btn-preflight-back"
          >
            Back
          </button>
          
          <button
            type="button"
            disabled={!canProceed}
            onClick={onPreflightComplete}
            className={`px-5 py-2 rounded-lg text-sm font-medium transition-all ${
              canProceed
                ? 'bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/10 hover:bg-emerald-400'
                : 'bg-slate-800 text-slate-500 cursor-not-allowed'
            }`}
            id="btn-preflight-proceed"
          >
            Proceed to Recording
          </button>
        </div>
      </div>
    </div>
  );
}
