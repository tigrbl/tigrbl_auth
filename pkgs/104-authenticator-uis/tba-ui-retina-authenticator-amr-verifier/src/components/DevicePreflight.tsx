import React, { useState, useEffect } from 'react';
import { RefreshCw, CheckCircle, Cpu, ShieldAlert, Zap, Sun, Target } from 'lucide-react';
import { VerifierDevice } from '../types';

interface DevicePreflightProps {
  onPreflightSuccess: (device: VerifierDevice) => void;
  onPreflightFail: (reason: string) => void;
  onCancel: () => void;
}

export default function DevicePreflight({
  onPreflightSuccess,
  onPreflightFail,
  onCancel,
}: DevicePreflightProps) {
  const [device, setDevice] = useState<VerifierDevice>({
    id: 'VER-990-H1',
    name: 'RetinaScan Prime H100',
    model: 'RP-H100-M1',
    location: 'Primary Secure Vault Booth B3',
    firmwareVersion: 'v4.14.9-secure',
    status: 'calibrating',
    conformanceClass: 'Class-A',
    lastCalibrationDate: new Date().toLocaleDateString(),
    ambientLightLux: 150, // Starts high (needs <= 80)
    cameraResolution: '8K Quad-Spectrum Ocular Sensor',
  });

  const [diagnosticsRunning, setDiagnosticsRunning] = useState(false);
  const [opticalFocus, setOpticalFocus] = useState<number>(45); // Starts out of focus (needs 80-95)
  const [handshakePass, setHandshakePass] = useState(false);
  const [envLightPass, setEnvLightPass] = useState(false);
  const [lensFocusPass, setLensFocusPass] = useState(false);
  const [networkLatencyPass, setNetworkLatencyPass] = useState(true);

  useEffect(() => {
    setEnvLightPass(device.ambientLightLux <= 80);
  }, [device.ambientLightLux]);

  useEffect(() => {
    setLensFocusPass(opticalFocus >= 80 && opticalFocus <= 95);
  }, [opticalFocus]);

  const runFullDiagnostics = () => {
    setDiagnosticsRunning(true);
    setHandshakePass(false);
    setTimeout(() => {
      setHandshakePass(true);
      setDiagnosticsRunning(false);
    }, 1200);
  };

  const isReady = handshakePass && envLightPass && lensFocusPass && networkLatencyPass;

  const handleProceed = () => {
    if (isReady) {
      onPreflightSuccess({
        ...device,
        ambientLightLux: device.ambientLightLux,
        status: 'online',
      });
    }
  };

  return (
    <div id="preflight-container" className="bg-slate-900 border border-slate-800 rounded-2xl p-6 md:p-8 max-w-4xl mx-auto shadow-2xl relative">
      <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />

      <div className="flex items-center justify-between border-b border-slate-800 pb-5 mb-6">
        <div className="flex items-center gap-4">
          <div className="p-3 bg-cyan-500/10 border border-cyan-500/20 rounded-xl text-cyan-400">
            <Cpu className="w-8 h-8" />
          </div>
          <div>
            <span className="text-xs font-mono text-cyan-400 uppercase tracking-wider">Verification Preflight</span>
            <h1 className="text-2xl font-semibold text-slate-100 tracking-tight">Biometric Preflight & Calibration</h1>
            <p className="text-sm text-slate-400">Establish physical verifier readiness & environment compatibility</p>
          </div>
        </div>
        <button
          id="btn-preflight-cancel"
          onClick={onCancel}
          className="text-xs font-mono px-3 py-1.5 rounded border border-slate-800 text-slate-400 hover:text-slate-200 hover:bg-slate-800 transition-all cursor-pointer"
        >
          Cancel
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-7 space-y-6">
          <div className="bg-slate-950/60 rounded-xl p-5 border border-slate-800/80 space-y-4">
            <h3 className="text-xs font-mono uppercase text-cyan-400 tracking-wider">Detected Authenticator Hardware</h3>
            <div className="grid grid-cols-2 gap-y-3 gap-x-4 text-xs font-mono">
              <div>
                <span className="text-slate-500">DEVICE MODEL</span>
                <p className="text-slate-200 font-semibold">{device.name}</p>
              </div>
              <div>
                <span className="text-slate-500">GEOGRAPHIC STATION</span>
                <p className="text-slate-200">{device.location}</p>
              </div>
              <div>
                <span className="text-slate-500">CONFORMANCE RATING</span>
                <p className="text-emerald-400 font-semibold">{device.conformanceClass} (Military Grade)</p>
              </div>
              <div>
                <span className="text-slate-500">ENCLAVE FIRMWARE</span>
                <p className="text-slate-300">{device.firmwareVersion}</p>
              </div>
            </div>
          </div>

          <div className="space-y-3">
            <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider">Diagnostics Checks</h3>
            <div className="space-y-2.5">
              <div className="flex items-center justify-between p-3 bg-slate-950/20 border border-slate-800 rounded-lg">
                <div className="flex items-center gap-3">
                  <Zap className={`w-4 h-4 ${handshakePass ? 'text-emerald-400' : 'text-slate-500'}`} />
                  <div className="text-xs">
                    <p className="font-medium text-slate-200">First-Party Sensor Verification</p>
                    <p className="text-slate-400 text-[11px]">Secure identity cryptographic challenge.</p>
                  </div>
                </div>
                <div>
                  {handshakePass ? (
                    <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">AUTHENTIC</span>
                  ) : diagnosticsRunning ? (
                    <RefreshCw className="w-4 h-4 text-cyan-400 animate-spin" />
                  ) : (
                    <span className="text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded">PENDING</span>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-950/20 border border-slate-800 rounded-lg">
                <div className="flex items-center gap-3">
                  <Sun className={`w-4 h-4 ${envLightPass ? 'text-emerald-400' : 'text-amber-400'}`} />
                  <div className="text-xs">
                    <p className="font-medium text-slate-200">Ambient Illumination Threshold</p>
                    <p className="text-slate-400 text-[11px]">Must be ≤ 80 Lux. Current: {device.ambientLightLux} Lux.</p>
                  </div>
                </div>
                <div>
                  {envLightPass ? (
                    <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">COMPLIANT</span>
                  ) : (
                    <span className="text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded">TOO LIGHT</span>
                  )}
                </div>
              </div>

              <div className="flex items-center justify-between p-3 bg-slate-950/20 border border-slate-800 rounded-lg">
                <div className="flex items-center gap-3">
                  <Target className={`w-4 h-4 ${lensFocusPass ? 'text-emerald-400' : 'text-amber-400'}`} />
                  <div className="text-xs">
                    <p className="font-medium text-slate-200">Ocular Lens Focal Depth</p>
                    <p className="text-slate-400 text-[11px]">Alignment plane depth (80-95). Current: {opticalFocus}.</p>
                  </div>
                </div>
                <div>
                  {lensFocusPass ? (
                    <span className="text-[10px] font-mono bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-2 py-0.5 rounded">OPTIMAL</span>
                  ) : (
                    <span className="text-[10px] font-mono bg-amber-500/10 text-amber-400 border border-amber-500/20 px-2 py-0.5 rounded">OUT OF FOCUS</span>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-5 bg-slate-950/40 border border-slate-800 rounded-xl p-5 space-y-6">
          <h3 className="text-xs font-mono uppercase text-slate-400 tracking-wider border-b border-slate-800 pb-2">Simulator Diagnostics Calibration</h3>
          <div className="space-y-5 text-xs font-mono">
            <div className="space-y-2">
              <div className="flex justify-between items-center text-[11px]">
                <span className="text-slate-400">AMBIENT CHAMBER LIGHT</span>
                <span className={device.ambientLightLux <= 80 ? 'text-emerald-400' : 'text-amber-400'}>
                  {device.ambientLightLux} Lux (Target ≤ 80)
                </span>
              </div>
              <input
                id="slider-ambient-light"
                type="range"
                min="10"
                max="250"
                value={device.ambientLightLux}
                onChange={(e) => {
                  const val = parseInt(e.target.value);
                  setDevice(prev => ({ ...prev, ambientLightLux: val }));
                }}
                className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
              <p className="text-[10px] text-slate-500">
                💡 <span className="text-cyan-400">Action:</span> Slide left (dim environment) to satisfy constraints.
              </p>
            </div>

            <div className="space-y-2">
              <div className="flex justify-between items-center text-[11px]">
                <span className="text-slate-400">LENS FOCAL DEPTH</span>
                <span className={opticalFocus >= 80 && opticalFocus <= 95 ? 'text-emerald-400' : 'text-amber-400'}>
                  Value: {opticalFocus} (Target: 80 - 95)
                </span>
              </div>
              <input
                id="slider-focal-depth"
                type="range"
                min="10"
                max="100"
                value={opticalFocus}
                onChange={(e) => setOpticalFocus(parseInt(e.target.value))}
                className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
              <p className="text-[10px] text-slate-500">
                💡 <span className="text-cyan-400">Action:</span> Slide focus level to match physical focal zone.
              </p>
            </div>

            <div className="flex items-center justify-between pt-3 border-t border-slate-800/80">
              <span className="text-slate-400">CONNECTION LATENCY STATE</span>
              <button
                id="btn-toggle-latency"
                type="button"
                onClick={() => setNetworkLatencyPass(!networkLatencyPass)}
                className={`text-[10px] font-mono px-2 py-1 rounded border transition-colors cursor-pointer ${
                  networkLatencyPass
                    ? 'border-emerald-500/20 bg-emerald-500/10 text-emerald-400'
                    : 'border-red-500/20 bg-red-500/10 text-red-400'
                }`}
              >
                {networkLatencyPass ? 'Stable (32ms)' : 'Excessive Latency (>300ms)'}
              </button>
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 space-y-3">
            <button
              id="btn-run-diagnostics"
              onClick={runFullDiagnostics}
              disabled={diagnosticsRunning}
              className={`w-full py-2 px-4 rounded-lg font-mono text-xs font-semibold uppercase tracking-wider flex items-center justify-center gap-2 transition-all duration-200 border cursor-pointer ${
                diagnosticsRunning
                  ? 'bg-slate-900 border-slate-800 text-slate-500'
                  : 'bg-slate-950 hover:bg-slate-900 border-slate-800 text-slate-300 hover:text-white'
              }`}
            >
              <RefreshCw className={`w-4 h-4 ${diagnosticsRunning ? 'animate-spin' : ''}`} />
              <span>{diagnosticsRunning ? 'Conducting Identity Shake...' : 'Execute Authenticator Handshake'}</span>
            </button>

            <button
              id="btn-preflight-proceed"
              onClick={handleProceed}
              disabled={!isReady}
              className={`w-full py-2.5 px-4 rounded-lg font-mono text-xs font-semibold uppercase tracking-wider flex items-center justify-center gap-2 transition-all duration-200 ${
                isReady
                  ? 'bg-gradient-to-r from-emerald-500 to-cyan-500 hover:from-emerald-400 hover:to-cyan-400 text-slate-950 font-bold shadow-lg shadow-cyan-500/10 cursor-pointer'
                  : 'bg-slate-800 text-slate-500 border border-slate-700/50 cursor-not-allowed'
              }`}
            >
              <span>Activate Biometric Chamber</span>
              <CheckCircle className="w-4 h-4" />
            </button>

            {!isReady && (
              <div className="bg-amber-950/20 border border-amber-950/40 rounded-lg p-3 flex gap-2 text-[10px] font-mono text-amber-400 leading-normal">
                <ShieldAlert className="w-4 h-4 shrink-0 mt-0.5" />
                <div>
                  <p className="font-semibold uppercase text-amber-300">Preflight Locked</p>
                  <p className="text-slate-400 mt-1">To start retina biometric scan, complete calibration:</p>
                  <ul className="list-disc list-inside mt-1 text-[9px] text-slate-500 space-y-0.5">
                    {!handshakePass && <li>Execute Authenticator Handshake check</li>}
                    {!envLightPass && <li>Slide Ambient Chamber Light slider to ≤ 80 Lux</li>}
                    {!lensFocusPass && <li>Adjust Focal Depth slider between 80 - 95</li>}
                    {!networkLatencyPass && <li>Ensure latency state is set to Stable</li>}
                  </ul>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
