/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { Camera, RefreshCw, CheckCircle2, AlertTriangle, HelpCircle, ShieldAlert } from 'lucide-react';

interface FaceCapturePreflightProps {
  onPreflightComplete: () => void;
  onPreflightFailed: (reason: string) => void;
  onUseFallback: () => void;
}

export const FaceCapturePreflight: React.FC<FaceCapturePreflightProps> = ({
  onPreflightComplete,
  onPreflightFailed,
  onUseFallback
}) => {
  const [permissionState, setPermissionState] = useState<'prompt' | 'granted' | 'denied' | 'permanently_denied'>('prompt');
  const [lightLevel, setLightLevel] = useState<'optimal' | 'low' | 'glare'>('optimal');
  const [verifierHealth, setVerifierHealth] = useState<'healthy' | 'unreachable'>('healthy');
  const [hardwareSensor, setHardwareSensor] = useState<'supported' | 'unsupported_webcam' | 'none'>('supported');
  const [checking, setChecking] = useState(false);

  // Trigger permission request simulating native OS flow
  const requestPermission = async () => {
    setChecking(true);
    // Simulate minor delay
    setTimeout(() => {
      setPermissionState('granted');
      setChecking(false);
    }, 900);
  };

  const runAllChecks = () => {
    setChecking(true);
    setTimeout(() => {
      setChecking(false);
      if (permissionState !== 'granted') {
        onPreflightFailed('Camera permission is required before proceeding.');
        return;
      }
      if (hardwareSensor === 'none') {
        onPreflightFailed('No compatible biometric camera or secure enclave depth sensor was detected.');
        return;
      }
      if (verifierHealth === 'unreachable') {
        onPreflightFailed('The secure verifier boundary is unreachable. Check network status.');
        return;
      }
      if (lightLevel === 'low') {
        // Corrective warning is handled in UI, but if we choose to fail
        onPreflightFailed('Inadequate environment lighting. Please increase lighting.');
        return;
      }
      onPreflightComplete();
    }, 1200);
  };

  return (
    <div id="face-capture-preflight-card" className="bg-white border border-gray-200 rounded-2xl shadow-sm p-6 max-w-lg mx-auto">
      {/* Title */}
      <div className="text-center mb-6">
        <h3 className="text-lg font-bold text-gray-900">Preflight Environment Check</h3>
        <p className="text-xs text-gray-500 mt-1">
          Validating local device profile, sensor capability, and isolated verifier channels.
        </p>
      </div>

      {/* Simulator Controls block to change states live */}
      <div className="bg-gray-50 border border-gray-200 rounded-xl p-3.5 mb-5 text-left">
        <span className="text-[10px] uppercase font-bold text-indigo-600 tracking-wider font-mono">Preflight Simulation Control Unit</span>
        <div className="grid grid-cols-2 gap-3 mt-2 text-xs">
          <div>
            <label className="block text-[11px] font-medium text-gray-500 mb-1">Hardware Sensor</label>
            <select
              value={hardwareSensor}
              onChange={(e) => setHardwareSensor(e.target.value as any)}
              className="w-full bg-white border border-gray-200 rounded-lg p-1.5 font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="supported">IR Enclave Depth Sensor (Valid)</option>
              <option value="unsupported_webcam">Untrusted USB Webcam (Fails Policy)</option>
              <option value="none">No Camera Detected (Outage)</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-gray-500 mb-1">Ambient Lighting</label>
            <select
              value={lightLevel}
              onChange={(e) => setLightLevel(e.target.value as any)}
              className="w-full bg-white border border-gray-200 rounded-lg p-1.5 font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="optimal">Optimal (Diffused Light)</option>
              <option value="low">Sub-Optimal (Low Light)</option>
              <option value="glare">Excessive Backlight / Glare</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-gray-500 mb-1">Verifier Connection</label>
            <select
              value={verifierHealth}
              onChange={(e) => setVerifierHealth(e.target.value as any)}
              className="w-full bg-white border border-gray-200 rounded-lg p-1.5 font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="healthy">Connected (Isolated Tunnel Active)</option>
              <option value="unreachable">Offline / Routing Error</option>
            </select>
          </div>

          <div>
            <label className="block text-[11px] font-medium text-gray-500 mb-1">Permission Mock</label>
            <select
              value={permissionState}
              onChange={(e) => setPermissionState(e.target.value as any)}
              className="w-full bg-white border border-gray-200 rounded-lg p-1.5 font-mono text-[11px] focus:outline-none focus:ring-1 focus:ring-indigo-500"
            >
              <option value="prompt">Prompt User</option>
              <option value="granted">Permission Granted</option>
              <option value="denied">Permission Denied (Explicit)</option>
              <option value="permanently_denied">Permanently Blocked</option>
            </select>
          </div>
        </div>
      </div>

      {/* Checklist Display */}
      <div className="space-y-3 mb-6">
        {/* Permission Row */}
        <div className="flex items-center justify-between p-2.5 border border-gray-100 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="p-1.5 bg-gray-50 rounded-lg">
              <Camera className="w-4 h-4 text-gray-600" />
            </div>
            <div className="text-left">
              <h4 className="text-xs font-semibold text-gray-900">OS Camera Access Permission</h4>
              <p className="text-[10px] text-gray-500">Needed to acquire local facial stream samples.</p>
            </div>
          </div>
          <div>
            {permissionState === 'granted' ? (
              <span className="flex items-center gap-1 text-[11px] font-medium text-green-600 font-mono bg-green-50 px-2 py-0.5 rounded-full">
                <CheckCircle2 className="w-3.5 h-3.5" /> GRANTED
              </span>
            ) : permissionState === 'denied' || permissionState === 'permanently_denied' ? (
              <span className="flex items-center gap-1 text-[11px] font-medium text-red-600 font-mono bg-red-50 px-2 py-0.5 rounded-full">
                <ShieldAlert className="w-3.5 h-3.5" /> DENIED
              </span>
            ) : (
              <button
                type="button"
                onClick={requestPermission}
                className="text-[11px] font-semibold text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-2.5 py-1 rounded-lg transition"
              >
                Grant Access
              </button>
            )}
          </div>
        </div>

        {/* Hardware Modality Check */}
        <div className="flex items-center justify-between p-2.5 border border-gray-100 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="p-1.5 bg-gray-50 rounded-lg">
              <HelpCircle className="w-4 h-4 text-gray-600" />
            </div>
            <div className="text-left">
              <h4 className="text-xs font-semibold text-gray-900">First-Party Sensor Verification</h4>
              <p className="text-[10px] text-gray-500">Validates depth-sensing or true infrared hardware.</p>
            </div>
          </div>
          <div>
            {hardwareSensor === 'supported' ? (
              <span className="text-[11px] font-medium text-green-600 font-mono bg-green-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" /> SECURE HW
              </span>
            ) : hardwareSensor === 'unsupported_webcam' ? (
              <span className="text-[11px] font-medium text-amber-600 font-mono bg-amber-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" /> GENERIC USB
              </span>
            ) : (
              <span className="text-[11px] font-medium text-red-600 font-mono bg-red-50 px-2 py-0.5 rounded-full">
                OUTAGE
              </span>
            )}
          </div>
        </div>

        {/* Lighting Check */}
        <div className="flex items-center justify-between p-2.5 border border-gray-100 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="p-1.5 bg-gray-50 rounded-lg text-gray-600">
              <RefreshCw className="w-4 h-4" />
            </div>
            <div className="text-left">
              <h4 className="text-xs font-semibold text-gray-900">Ambient Lighting Evaluation</h4>
              <p className="text-[10px] text-gray-500">Examines environment light to avoid occlusion.</p>
            </div>
          </div>
          <div>
            {lightLevel === 'optimal' ? (
              <span className="text-[11px] font-medium text-green-600 font-mono bg-green-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" /> OPTIMAL
              </span>
            ) : lightLevel === 'low' ? (
              <span className="text-[11px] font-medium text-amber-600 font-mono bg-amber-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" /> LOW LIGHT
              </span>
            ) : (
              <span className="text-[11px] font-medium text-amber-600 font-mono bg-amber-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <AlertTriangle className="w-3 h-3" /> GLARE
              </span>
            )}
          </div>
        </div>

        {/* Verifier Channel Check */}
        <div className="flex items-center justify-between p-2.5 border border-gray-100 rounded-xl">
          <div className="flex items-center gap-3">
            <div className="p-1.5 bg-gray-50 rounded-lg">
              <RefreshCw className="w-4 h-4 text-gray-600" />
            </div>
            <div className="text-left">
              <h4 className="text-xs font-semibold text-gray-900">Isolated Verifier Channel</h4>
              <p className="text-[10px] text-gray-500">Secure end-to-end telemetry tunnel health.</p>
            </div>
          </div>
          <div>
            {verifierHealth === 'healthy' ? (
              <span className="text-[11px] font-medium text-green-600 font-mono bg-green-50 px-2 py-0.5 rounded-full flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3" /> ESCROWED
              </span>
            ) : (
              <span className="text-[11px] font-medium text-red-600 font-mono bg-red-50 px-2 py-0.5 rounded-full">
                UNREACHABLE
              </span>
            )}
          </div>
        </div>
      </div>

      {/* Corrective/Incompatible Warnings if any checks fail */}
      {hardwareSensor === 'unsupported_webcam' && (
        <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3.5 rounded-xl text-xs mb-5 text-left">
          <p className="font-semibold flex items-center gap-1 mb-1">
            <AlertTriangle className="w-4 h-4 text-amber-600" /> Untrusted Capture Interface Warning
          </p>
          <p className="text-amber-800 text-[11px]">
            Your current hardware profiles indicate a generic external camera. Our current policy dictates that enrollment must occur inside an authenticated First-Party hardware-backed capture module or on an eligible mobile application. We will allow simulation, but a production server would reject this signature.
          </p>
        </div>
      )}

      {permissionState === 'denied' && (
        <div className="bg-red-50 border border-red-200 text-red-900 p-3.5 rounded-xl text-xs mb-5 text-left">
          <p className="font-semibold flex items-center gap-1 mb-1">
            <ShieldAlert className="w-4 h-4 text-red-600" /> Permission Block
          </p>
          <p className="text-red-800 text-[11px]">
            The camera permission was explicitly denied. To enroll in face recognition, please click "Grant Access" or update your system camera privacy settings.
          </p>
        </div>
      )}

      {lightLevel === 'low' && (
        <div className="bg-amber-50 border border-amber-200 text-amber-900 p-3.5 rounded-xl text-xs mb-5 text-left">
          <p className="font-semibold flex items-center gap-1 mb-1">
            <AlertTriangle className="w-4 h-4 text-amber-600" /> Inadequate Light Warning
          </p>
          <p className="text-amber-800 text-[11px]">
            Position yourself facing a stable light source. Low lighting interferes with anti-spoof checks, which might lead to liveness failures during template binding.
          </p>
        </div>
      )}

      {/* Action Triggers */}
      <div className="flex items-center justify-between gap-3 mt-4">
        <button
          type="button"
          onClick={onUseFallback}
          className="text-xs font-semibold text-gray-500 hover:text-gray-700 hover:underline"
        >
          Use FIDO2 security key instead
        </button>

        <button
          type="button"
          disabled={checking}
          onClick={runAllChecks}
          className={`px-5 py-2.5 rounded-xl text-xs font-semibold text-white shadow-sm flex items-center gap-2 ${
            checking
              ? 'bg-indigo-400 cursor-not-allowed'
              : 'bg-indigo-600 hover:bg-indigo-700 cursor-pointer'
          }`}
        >
          {checking && <RefreshCw className="w-3.5 h-3.5 animate-spin" />}
          {checking ? 'Checking Environment...' : 'Initiate Secure Capture'}
        </button>
      </div>
    </div>
  );
};
