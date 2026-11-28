import React, { useState } from 'react';
import { Settings, Shield, Globe, HardDrive, HelpCircle, Activity, Save, RefreshCw, AlertTriangle, CheckCircle2 } from 'lucide-react';
import { PolicyConfig, VerifierConfig } from '../types';

interface AdminPolicyPanelProps {
  policy: PolicyConfig;
  verifier: VerifierConfig;
  onSavePolicy: (policy: PolicyConfig) => void;
  onSaveVerifier: (verifier: VerifierConfig) => void;
}

export default function AdminPolicyPanel({
  policy,
  verifier,
  onSavePolicy,
  onSaveVerifier,
}: AdminPolicyPanelProps) {
  const [activeTab, setActiveTab] = useState<'policy' | 'verifier'>('policy');
  const [localPolicy, setLocalPolicy] = useState<PolicyConfig>({ ...policy });
  const [localVerifier, setLocalVerifier] = useState<VerifierConfig>({ ...verifier });
  const [isPingRunning, setIsPingRunning] = useState(false);
  const [showNotification, setShowNotification] = useState(false);
  const [notifMessage, setNotifMessage] = useState('');

  const triggerNotification = (msg: string) => {
    setNotifMessage(msg);
    setShowNotification(true);
    setTimeout(() => {
      setShowNotification(false);
    }, 3000);
  };

  const handleSavePolicy = (e: React.FormEvent) => {
    e.preventDefault();
    onSavePolicy(localPolicy);
    triggerNotification('Biometric Matching Policy rules saved and deployed.');
  };

  const handleSaveVerifier = (e: React.FormEvent) => {
    e.preventDefault();
    onSaveVerifier(localVerifier);
    triggerNotification('Verifier Endpoint Configuration updated.');
  };

  const runVerifierPing = () => {
    setIsPingRunning(true);
    setTimeout(() => {
      setIsPingRunning(false);
      // Randomly tweak the local verifier health for realism
      const statuses: ('healthy' | 'degraded' | 'offline')[] = ['healthy', 'healthy', 'degraded'];
      const nextHealth = statuses[Math.floor(Math.random() * statuses.length)];
      setLocalVerifier((prev) => ({ ...prev, healthStatus: nextHealth }));
      triggerNotification(`Verifier API ping completed. Status is: ${nextHealth.toUpperCase()}`);
    }, 1200);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl overflow-hidden shadow-2xl max-w-2xl mx-auto" id="admin-policy-container">
      {/* Tabs */}
      <div className="bg-gradient-to-r from-slate-950 via-slate-900 to-slate-950 px-6 py-4 border-b border-slate-800 flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <Settings className="w-5 h-5 text-indigo-400" />
          <h3 className="font-sans font-semibold tracking-tight text-slate-100 text-base">Policy & Verifier Admin Console</h3>
        </div>
        <div className="flex bg-slate-950/60 p-0.5 rounded-lg border border-slate-800 text-xs font-mono">
          <button
            type="button"
            onClick={() => setActiveTab('policy')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'policy' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            Match Policy
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('verifier')}
            className={`px-3 py-1.5 rounded-md transition-all ${
              activeTab === 'verifier' ? 'bg-slate-800 text-slate-200' : 'text-slate-500 hover:text-slate-300'
            }`}
          >
            Verifier API Config
          </button>
        </div>
      </div>

      {showNotification && (
        <div className="bg-emerald-500 text-slate-950 text-xs px-4 py-2 font-mono flex items-center gap-1.5">
          <CheckCircle2 className="w-3.5 h-3.5" />
          <span>{notifMessage}</span>
        </div>
      )}

      {activeTab === 'policy' ? (
        <form onSubmit={handleSavePolicy} className="p-6 space-y-5">
          {/* Matching Confidence Threshold */}
          <div className="space-y-2">
            <div className="flex justify-between items-center text-xs">
              <label className="text-slate-300 font-medium flex items-center gap-1">
                <Shield className="w-3.5 h-3.5 text-indigo-400" />
                <span>Minimum Biometric Matching Threshold</span>
              </label>
              <span className="font-mono text-indigo-400 font-semibold">{localPolicy.minConfidence}% Confidence</span>
            </div>
            <input
              type="range"
              min="60"
              max="95"
              value={localPolicy.minConfidence}
              onChange={(e) => setLocalPolicy((p) => ({ ...p, minConfidence: parseInt(e.target.value) }))}
              className="w-full accent-indigo-500 cursor-pointer h-1 bg-slate-950 rounded-lg"
              id="range-policy-min-confidence"
            />
            <p className="text-[10px] text-slate-500 leading-normal">
              Determines acceptable biometric distance. Higher limits reduce False Acceptance Rates (FAR) but increase False Rejection Rates (FRR).
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
            {/* Strict Liveness Switch */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-xs text-slate-200 font-medium font-sans">Strict Liveness Auditing</span>
                <input
                  type="checkbox"
                  checked={localPolicy.strictLiveness}
                  onChange={(e) => setLocalPolicy((p) => ({ ...p, strictLiveness: e.target.checked }))}
                  className="accent-indigo-500 h-4 w-4 rounded cursor-pointer"
                  id="chk-policy-strict-liveness"
                />
              </div>
              <p className="text-[10px] text-slate-500 leading-normal">
                Requires phase-amplitude jitter checks. Aborts instantly if suspected replay, speech synthesizers, or deepfakes match.
              </p>
            </div>

            {/* Noise Floor Threshold */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans">Max Ambient Noise Limit</label>
              <select
                value={localPolicy.noiseThresholdDb}
                onChange={(e) => setLocalPolicy((p) => ({ ...p, noiseThresholdDb: parseInt(e.target.value) }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-policy-noise-db"
              >
                <option value="-50">-50 dB (Extremely Quiet Studio)</option>
                <option value="-45">-45 dB (Quiet Bedroom)</option>
                <option value="-42">-42 dB (Normal Office Space)</option>
                <option value="-35">-35 dB (Noisy Café Floor)</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Blocks enrollment if background noise exceeds ceiling to prevent faulty model registrations.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-1">
            {/* Fallback Factor Options */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans">Accessible Alternative Factor</label>
              <select
                value={localPolicy.fallbackFactor}
                onChange={(e) => setLocalPolicy((p) => ({ ...p, fallbackFactor: e.target.value as any }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-policy-fallback-factor"
              >
                <option value="fido_passkey">FIDO2 Cryptographic Passkey</option>
                <option value="totp">Time-Based One-Time Password (TOTP)</option>
                <option value="password">Master Security Password</option>
                <option value="security_questions">Preset Security Questions</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Default bypass factor offered to users with speech impediments or failing hardware checks.
              </p>
            </div>

            {/* Retention Days */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans">Biometric Retention Period</label>
              <select
                value={localPolicy.retentionDays}
                onChange={(e) => setLocalPolicy((p) => ({ ...p, retentionDays: parseInt(e.target.value) }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-policy-retention"
              >
                <option value="90">90 Days (GDPR High-Privacy)</option>
                <option value="180">180 Days (Standard Enterprise)</option>
                <option value="365">365 Days (Extended Auditing)</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Inactive profiles are deleted permanently from all verifier nodes after expiration.
              </p>
            </div>
          </div>

          <div className="flex justify-end pt-3 border-t border-slate-800">
            <button
              type="submit"
              className="bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-sans font-semibold text-xs px-5 py-2 rounded-lg flex items-center gap-1.5 transition-all shadow-md shadow-indigo-500/10 cursor-pointer"
              id="btn-policy-save"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Save Matching Rules</span>
            </button>
          </div>
        </form>
      ) : (
        <form onSubmit={handleSaveVerifier} className="p-6 space-y-5">
          {/* Verifier Endpoint and Core info */}
          <div className="space-y-2">
            <label className="block text-xs text-slate-300 font-medium font-sans">Biometric Provider Endpoint</label>
            <input
              type="text"
              value={localVerifier.endpointUrl}
              onChange={(e) => setLocalVerifier((v) => ({ ...v, endpointUrl: e.target.value }))}
              placeholder="API endpoint URL"
              className="w-full bg-slate-950 border border-slate-850 text-slate-300 font-mono text-xs rounded-lg px-3 py-2 focus:outline-none focus:border-indigo-500 transition-colors"
              id="input-verifier-endpoint"
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Host region */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans flex items-center gap-1">
                <Globe className="w-3.5 h-3.5 text-indigo-400" />
                <span>Isolated Hosting Region</span>
              </label>
              <select
                value={localVerifier.region}
                onChange={(e) => setLocalVerifier((v) => ({ ...v, region: e.target.value as any }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-verifier-region"
              >
                <option value="us-east1">us-east1 (Iowa, USA)</option>
                <option value="europe-west1">europe-west1 (Belgium, EU)</option>
                <option value="asia-east1">asia-east1 (Taiwan, APAC)</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Locks verifier database boundaries to strict legal geographies for BIPA and GDPR compliance.
              </p>
            </div>

            {/* Neural Model Version */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans flex items-center gap-1">
                <HardDrive className="w-3.5 h-3.5 text-indigo-400" />
                <span>Active Matching Model</span>
              </label>
              <select
                value={localVerifier.activeModel}
                onChange={(e) => setLocalVerifier((v) => ({ ...v, activeModel: e.target.value }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-verifier-model"
              >
                <option value="VBM-Neural-v4.2-Liveness">VBM-Neural-v4.2-Liveness</option>
                <option value="VBM-CNN-v3.9-Passive">VBM-CNN-v3.9-Passive (Legacy)</option>
                <option value="VBM-Transformer-v5.0-BETA">VBM-Transformer-v5.0-BETA</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Model version specifies vector resolution size and liveness neural layers.
              </p>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Fail behavior */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl space-y-2">
              <label className="block text-xs text-slate-200 font-medium font-sans">Fail Behavior (Outage Recovery)</label>
              <select
                value={localVerifier.failBehavior}
                onChange={(e) => setLocalVerifier((v) => ({ ...v, failBehavior: e.target.value as any }))}
                className="w-full bg-slate-900 border border-slate-800 text-slate-300 rounded-lg px-2.5 py-1.5 text-xs focus:outline-none focus:border-indigo-500 font-mono"
                id="select-verifier-fail-behavior"
              >
                <option value="fail_safe">Fail Safe (Block Voice Logins)</option>
                <option value="fail_open">Fail Open (Downgrade Security Check)</option>
              </select>
              <p className="text-[10px] text-slate-500 leading-normal">
                Specifies access flow parameters if the SentryVoice API clusters go offline or return a 5xx code.
              </p>
            </div>

            {/* Real-time Health checks simulation */}
            <div className="bg-slate-950/40 border border-slate-850 p-4 rounded-xl flex flex-col justify-between">
              <div className="flex items-center justify-between text-xs">
                <span className="text-slate-200 font-medium font-sans flex items-center gap-1.5">
                  <Activity className="w-3.5 h-3.5 text-indigo-400" />
                  <span>Verifier Network Node Status</span>
                </span>
                <span className={`px-2 py-0.5 rounded text-[10px] font-mono border uppercase ${
                  localVerifier.healthStatus === 'healthy'
                    ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400'
                    : localVerifier.healthStatus === 'degraded'
                    ? 'bg-amber-500/10 border-amber-500/20 text-amber-400'
                    : 'bg-rose-500/10 border-rose-500/20 text-rose-400'
                }`}>
                  {localVerifier.healthStatus}
                </span>
              </div>
              
              <div className="flex gap-2 mt-4">
                <button
                  type="button"
                  onClick={runVerifierPing}
                  disabled={isPingRunning}
                  className="w-full bg-slate-900 border border-slate-800 hover:bg-slate-800 text-slate-300 font-mono text-[10px] py-2 rounded-lg flex items-center justify-center gap-1 cursor-pointer"
                  id="btn-verifier-ping"
                >
                  {isPingRunning ? (
                    <RefreshCw className="w-3 h-3 animate-spin" />
                  ) : (
                    <RefreshCw className="w-3 h-3" />
                  )}
                  <span>Ping Host Nodes</span>
                </button>
              </div>
            </div>
          </div>

          <div className="flex justify-end pt-3 border-t border-slate-800">
            <button
              type="submit"
              className="bg-indigo-500 hover:bg-indigo-400 text-slate-950 font-sans font-semibold text-xs px-5 py-2 rounded-lg flex items-center gap-1.5 transition-all shadow-md shadow-indigo-500/10 cursor-pointer"
              id="btn-verifier-save"
            >
              <Save className="w-3.5 h-3.5" />
              <span>Update Verifier Setup</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
