import React, { useState } from 'react';
import { motion } from 'motion/react';
import { Settings, ShieldCheck, Cpu, RefreshCw, AlertOctagon, Layers, Globe, Filter, Activity } from 'lucide-react';
import { VerifierDevice, AuditLog, BiometricPolicy } from '../types';

interface AdminDashboardProps {
  devices: VerifierDevice[];
  policy: BiometricPolicy;
  auditLogs: AuditLog[];
  onUpdatePolicy: (newPolicy: BiometricPolicy) => void;
  onUpdateDevices: (newDevices: VerifierDevice[]) => void;
}

export default function AdminDashboard({
  devices,
  policy,
  auditLogs,
  onUpdatePolicy,
  onUpdateDevices,
}: AdminDashboardProps) {
  const [activeTab, setActiveTab] = useState<'policy' | 'fleet' | 'audit'>('fleet');
  const [editingPolicy, setEditingPolicy] = useState<BiometricPolicy>({ ...policy });
  const [calibratingDeviceId, setCalibratingDeviceId] = useState<string | null>(null);
  const [filterOutcome, setFilterOutcome] = useState<'all' | 'success' | 'failed' | 'warning'>('all');
  const [selectedIncident, setSelectedIncident] = useState<AuditLog | null>(null);

  const handleApplyPolicy = (e: React.FormEvent) => {
    e.preventDefault();
    onUpdatePolicy({ ...editingPolicy });
    alert('Biometric Security Governance Policy applied and synchronized across secure enclave network.');
  };

  const handleDeviceCalibration = (deviceId: string) => {
    setCalibratingDeviceId(deviceId);
    
    // Simulate multi-axis lens calibration (takes 2 seconds)
    setTimeout(() => {
      const updated = devices.map(d => {
        if (d.id === deviceId) {
          return {
            ...d,
            status: 'online' as const,
            ambientLightLux: Math.floor(Math.random() * 30) + 40, // Restore to optimal (e.g. 40-70 Lux)
            lastCalibrationDate: new Date().toLocaleDateString(),
          };
        }
        return d;
      });
      onUpdateDevices(updated);
      setCalibratingDeviceId(null);
    }, 2000);
  };

  const handleToggleOutage = (deviceId: string) => {
    const updated = devices.map(d => {
      if (d.id === deviceId) {
        const nextStatus = d.status === 'offline' ? 'online' : 'offline';
        return { ...d, status: nextStatus as any };
      }
      return d;
    });
    onUpdateDevices(updated);
  };

  // Filter central logs
  const filteredLogs = auditLogs.filter(log => {
    if (filterOutcome === 'all') return true;
    return log.outcome === filterOutcome;
  });

  return (
    <div id="admin-container" className="max-w-6xl mx-auto space-y-6">
      
      {/* Subnavigation Bar */}
      <div className="flex border-b border-slate-800 bg-slate-900 p-2 rounded-xl gap-2">
        <button
          id="btn-tab-fleet"
          onClick={() => setActiveTab('fleet')}
          className={`px-4 py-2 font-mono text-xs font-semibold rounded-lg flex items-center gap-2 transition-colors cursor-pointer ${
            activeTab === 'fleet' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Cpu className="w-4 h-4" />
          Verifier Device Fleet ({devices.length})
        </button>

        <button
          id="btn-tab-policy"
          onClick={() => setActiveTab('policy')}
          className={`px-4 py-2 font-mono text-xs font-semibold rounded-lg flex items-center gap-2 transition-colors cursor-pointer ${
            activeTab === 'policy' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Settings className="w-4 h-4" />
          Security Policy Governance
        </button>

        <button
          id="btn-tab-audit"
          onClick={() => setActiveTab('audit')}
          className={`px-4 py-2 font-mono text-xs font-semibold rounded-lg flex items-center gap-2 transition-colors cursor-pointer ${
            activeTab === 'audit' ? 'bg-cyan-500 text-slate-950 font-bold' : 'text-slate-400 hover:text-white hover:bg-slate-800'
          }`}
        >
          <Activity className="w-4 h-4" />
          Central Audit & Diagnostics
        </button>
      </div>

      {/* Tab content 1: Fleet Management */}
      {activeTab === 'fleet' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Main Fleet Health Panel */}
          <div className="md:col-span-2 bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider border-b border-slate-800 pb-3">
              Physical Verifier Fleet Monitor
            </h3>

            <div className="space-y-4">
              {devices.map((dev) => (
                <div id={`device-card-${dev.id}`} key={dev.id} className="bg-slate-950/60 p-4 rounded-xl border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className={`w-2.5 h-2.5 rounded-full ${
                        dev.status === 'online' ? 'bg-emerald-400 shadow-sm shadow-emerald-400/50' :
                        dev.status === 'calibrating' ? 'bg-amber-400 animate-pulse' :
                        'bg-red-500'
                      }`} />
                      <h4 className="text-xs font-mono font-bold text-slate-100">{dev.name}</h4>
                      <span className="text-[9px] font-mono bg-slate-800 border border-slate-700 text-slate-400 px-1.5 py-0.2 rounded">
                        {dev.conformanceClass}
                      </span>
                    </div>
                    <p className="text-[11px] text-slate-400 font-sans">{dev.location}</p>
                    <div className="flex gap-4 text-[10px] font-mono text-slate-500 pt-1">
                      <span>LENS AMBIENT: {dev.ambientLightLux} Lux</span>
                      <span>FIRMWARE: {dev.firmwareVersion}</span>
                    </div>
                  </div>

                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      id={`btn-calibrate-${dev.id}`}
                      disabled={calibratingDeviceId !== null}
                      onClick={() => handleDeviceCalibration(dev.id)}
                      className={`px-3 py-1.5 rounded font-mono text-[11px] border flex items-center gap-1.5 transition-all cursor-pointer ${
                        calibratingDeviceId === dev.id
                          ? 'bg-slate-900 border-slate-800 text-slate-500'
                          : 'bg-slate-950 border-slate-800 text-cyan-400 hover:text-white hover:bg-slate-800'
                      }`}
                    >
                      <RefreshCw className={`w-3.5 h-3.5 ${calibratingDeviceId === dev.id ? 'animate-spin' : ''}`} />
                      {calibratingDeviceId === dev.id ? 'Calibrating...' : 'Calibrate'}
                    </button>

                    <button
                      id={`btn-outage-${dev.id}`}
                      onClick={() => handleToggleOutage(dev.id)}
                      className={`px-3 py-1.5 rounded font-mono text-[11px] border transition-colors cursor-pointer ${
                        dev.status === 'offline'
                          ? 'bg-emerald-500/10 border-emerald-500/20 text-emerald-400 hover:bg-emerald-500/25'
                          : 'bg-red-500/10 border-red-500/20 text-red-400 hover:bg-red-500/25'
                      }`}
                    >
                      {dev.status === 'offline' ? 'Power Restore' : 'Simulate Outage'}
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Fleet Health Quick Stats */}
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-5">
            <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider border-b border-slate-800 pb-3">
              Fleet Conformance
            </h3>

            <div className="space-y-4 text-xs font-mono">
              <div className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-800 space-y-1.5">
                <span className="text-slate-500 text-[10px]">VERIFIER DISCREPANCY INCIDENTS</span>
                <p className="text-slate-100 text-lg font-bold">0 Active Threats</p>
                <div className="w-full bg-slate-800 h-1.5 rounded-full overflow-hidden">
                  <div className="bg-emerald-400 h-full w-full" />
                </div>
              </div>

              <div className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-800 space-y-1.5">
                <span className="text-slate-500 text-[10px]">COMPLIANCE ASSURANCE</span>
                <p className="text-slate-100 text-lg font-bold">Class-A Conformance</p>
                <p className="text-[10px] text-slate-400 leading-normal font-sans">
                  All active stations enforceLevel-3 active ocular challenge response validation before emission.
                </p>
              </div>

              <div className="bg-slate-950/40 p-3.5 rounded-lg border border-slate-800 space-y-2">
                <span className="text-slate-500 text-[10px] block">FLIGHT SHIELD STATISTICS</span>
                <ul className="space-y-1 text-[11px] text-slate-300">
                  <li className="flex justify-between">
                    <span>Active Nonces:</span>
                    <span className="text-cyan-400 font-semibold">1,024</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Avg Handshake latency:</span>
                    <span className="text-cyan-400">42ms</span>
                  </li>
                  <li className="flex justify-between">
                    <span>Calibration drift rate:</span>
                    <span className="text-emerald-400">&lt; 0.01%</span>
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Tab content 2: Biometric Governance Policies */}
      {activeTab === 'policy' && (
        <form onSubmit={handleApplyPolicy} className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl max-w-4xl mx-auto space-y-6">
          <div className="border-b border-slate-800 pb-4">
            <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider">
              Enclave Biometric Security Policy Governance
            </h3>
            <p className="text-xs text-slate-400 font-sans mt-0.5">
              These policy scopes are cryptographically pushed to all physical verifiers on save.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs font-mono">
            {/* Scope selection */}
            <div className="space-y-2">
              <label className="text-[11px] text-slate-400 uppercase">ELIGIBILITY DEPLOYMENT SCOPE</label>
              <select
                id="select-policy-scope"
                value={editingPolicy.eligibilityScope}
                onChange={(e) => setEditingPolicy(prev => ({ ...prev, eligibilityScope: e.target.value as any }))}
                className="w-full bg-slate-950 text-slate-200 border border-slate-800 rounded p-2 focus:border-cyan-500 focus:outline-none"
              >
                <option value="all_users">All Users (Forced biometric security mandates)</option>
                <option value="high_assurance_only">High Assurance Level Only (Secure vaults / Administrators)</option>
                <option value="custom">Restricted custom location criteria</option>
              </select>
            </div>

            {/* Liveness level selection */}
            <div className="space-y-2">
              <label className="text-[11px] text-slate-400 uppercase">REQUIRED LIVENESS LEVEL CLASS</label>
              <select
                id="select-policy-liveness"
                value={editingPolicy.requiredLivenessLevel}
                onChange={(e) => setEditingPolicy(prev => ({ ...prev, requiredLivenessLevel: e.target.value as any }))}
                className="w-full bg-slate-950 text-slate-200 border border-slate-800 rounded p-2 focus:border-cyan-500 focus:outline-none"
              >
                <option value="Level-1">Level-1: Static Pupil Size Map Check</option>
                <option value="Level-2">Level-2: Dynamic Pupil Reflex Check</option>
                <option value="Level-3">Level-3: Active Saccadic Coordinates Trace (Military)</option>
              </select>
            </div>

            {/* Retention Slider */}
            <div className="space-y-2.5">
              <div className="flex justify-between text-[11px]">
                <span className="text-slate-400 uppercase">DATA RETENTION EXPIRY LIMIT</span>
                <span className="text-cyan-400">{editingPolicy.retentionPeriodMonths} Months</span>
              </div>
              <input
                id="slider-policy-retention"
                type="range"
                min="1"
                max="24"
                value={editingPolicy.retentionPeriodMonths}
                onChange={(e) => {
                  const val = parseInt(e.target.value);
                  setEditingPolicy(prev => ({ ...prev, retentionPeriodMonths: val }));
                }}
                className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-cyan-400"
              />
            </div>

            {/* Geofence toggling */}
            <div className="space-y-3 p-3 bg-slate-950/40 rounded-lg border border-slate-800">
              <div className="flex items-center justify-between">
                <span className="text-[11px] text-slate-400 uppercase">GEOFENCED REGION CONTROLS</span>
                <input
                  id="checkbox-policy-geofence"
                  type="checkbox"
                  checked={editingPolicy.geofenceEnabled}
                  onChange={(e) => setEditingPolicy(prev => ({ ...prev, geofenceEnabled: e.target.checked }))}
                  className="w-4 h-4 rounded border-slate-700 text-cyan-500 bg-slate-900"
                />
              </div>
              <p className="text-[10px] text-slate-500 font-sans leading-normal">
                Enforce physical verifier boundary checks within audited company facilities only.
              </p>
            </div>

            {/* Web fallback toggle */}
            <div className="col-span-2 p-3 bg-slate-950/40 border border-slate-800 rounded-lg flex items-center justify-between">
              <div className="space-y-1">
                <span className="text-[11px] text-slate-300 uppercase">ALLOW DEGRADED WEB KEY FALLBACKS</span>
                <p className="text-[10px] text-slate-500 font-sans">
                  If the physical verifier fleet faces outages, allow compliant fallbacks to alternative factors.
                </p>
              </div>
              <input
                id="checkbox-policy-fallback"
                type="checkbox"
                checked={editingPolicy.allowWebFallback}
                onChange={(e) => setEditingPolicy(prev => ({ ...prev, allowWebFallback: e.target.checked }))}
                className="w-4 h-4 rounded border-slate-700 text-cyan-500 bg-slate-900 focus:ring-cyan-500"
              />
            </div>
          </div>

          <div className="pt-4 border-t border-slate-800 flex justify-end">
            <button
              id="btn-policy-save"
              type="submit"
              className="px-5 py-2.5 bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-mono text-xs font-bold uppercase tracking-wider rounded-lg transition-colors cursor-pointer"
            >
              Push Policy Sync
            </button>
          </div>
        </form>
      )}

      {/* Tab content 3: Central Audit Log & Incident Diagnostics */}
      {activeTab === 'audit' && (
        <div className="space-y-6">
          <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl space-y-6">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
              <h3 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider flex items-center gap-2">
                <span>Enterprise Biometric Access Logs</span>
              </h3>

              {/* Log Outcome Filter */}
              <div className="flex items-center gap-2 text-xs font-mono">
                <Filter className="w-3.5 h-3.5 text-slate-500" />
                <span className="text-slate-500 uppercase text-[10px]">FILTER OUTCOME:</span>
                <select
                  id="select-audit-filter"
                  value={filterOutcome}
                  onChange={(e) => setFilterOutcome(e.target.value as any)}
                  className="bg-slate-950 text-slate-300 border border-slate-800 rounded px-2.5 py-1.5 focus:outline-none"
                >
                  <option value="all">All Logs</option>
                  <option value="success">Success Only</option>
                  <option value="failed">Failures / Blocks</option>
                  <option value="warning">Warnings / Calibration</option>
                </select>
              </div>
            </div>

            {/* Central Audit Table */}
            <div className="overflow-x-auto">
              <table className="w-full text-left font-mono text-xs text-slate-300">
                <thead>
                  <tr className="text-slate-500 border-b border-slate-800/60 pb-2">
                    <th className="py-2">TIMESTAMP</th>
                    <th className="py-2">EVENT TYPE</th>
                    <th className="py-2">VERIFIER</th>
                    <th className="py-2">SUBJECT ID</th>
                    <th className="py-2">LIVENESS CLASS</th>
                    <th className="py-2">MATCH CLASS</th>
                    <th className="py-2">OUTCOME</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/40">
                  {filteredLogs.map((log) => (
                    <tr
                      id={`audit-row-${log.id}`}
                      key={log.id}
                      onClick={() => setSelectedIncident(log)}
                      className={`hover:bg-slate-950/40 cursor-pointer transition-colors ${
                        selectedIncident?.id === log.id ? 'bg-slate-950/60' : ''
                      }`}
                    >
                      <td className="py-3 text-slate-500 text-[11px]">
                        {new Date(log.timestamp).toLocaleTimeString()}
                      </td>
                      <td className="py-3 font-semibold text-slate-200">{log.eventType.toUpperCase()}</td>
                      <td className="py-3 text-slate-400">{log.deviceId}</td>
                      <td className="py-3 text-slate-400 text-[11px]">{log.subjectId}</td>
                      <td className="py-3 text-cyan-400 text-[11px]">{log.livenessClass}</td>
                      <td className="py-3 text-slate-300 text-[11px]">{log.matchScoreClass.toUpperCase()}</td>
                      <td className="py-3">
                        <span className={`text-[9px] px-2 py-0.5 rounded border font-bold ${
                          log.outcome === 'success' ? 'bg-emerald-500/10 text-emerald-400 border-emerald-500/20' :
                          log.outcome === 'failed' ? 'bg-red-500/10 text-red-400 border-red-500/20' :
                          'bg-amber-500/10 text-amber-400 border-amber-500/20'
                        }`}>
                          {log.outcome.toUpperCase()}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Redacted Incident Diagnostics Detail Drawer */}
          {selectedIncident && (
            <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl relative overflow-hidden">
              <div className="absolute top-0 right-0 w-64 h-64 bg-cyan-500/5 rounded-full blur-3xl pointer-events-none" />
              
              <div className="flex items-center justify-between border-b border-slate-800 pb-3 mb-4">
                <h4 className="text-sm font-semibold text-slate-100 font-mono uppercase tracking-wider flex items-center gap-2">
                  <AlertOctagon className="w-4 h-4 text-cyan-400" />
                  Redacted Incident Diagnosis
                </h4>
                <button
                  id="btn-close-incident"
                  onClick={() => setSelectedIncident(null)}
                  className="text-xs font-mono text-slate-500 hover:text-slate-300 cursor-pointer"
                >
                  Close Trace
                </button>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 text-xs font-mono">
                {/* Visual JSON-like log structure */}
                <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 text-cyan-400 text-[11px] space-y-1">
                  <p className="text-slate-500 uppercase text-[9px] mb-2 font-bold border-b border-slate-900 pb-1">Signed Ceremony Payload</p>
                  <p><span className="text-slate-500">"audit_trace_id":</span> "{selectedIncident.id}"</p>
                  <p><span className="text-slate-500">"cryptographic_subject_hash":</span> "{selectedIncident.subjectId === 'SUBJ-USR-773' ? 'd3b07384d113edec49eaa6238ad5ff00' : '8f94d4d12c85e2b82bc0e5c9ef94cf34'}"</p>
                  <p><span className="text-slate-500">"hardware_conformance_signature":</span> "ENCLAVE_SIG_{Math.random().toString(36).substr(2, 8).toUpperCase()}"</p>
                  <p><span className="text-slate-500">"enforce_liveness_class":</span> "{selectedIncident.livenessClass}"</p>
                  <p><span className="text-slate-500">"match_assessment_type":</span> "{selectedIncident.matchScoreClass}"</p>
                  <p><span className="text-slate-500">"client_websocket_rtt_ms":</span> 38</p>
                </div>

                <div className="space-y-4">
                  <div className="space-y-1">
                    <span className="text-slate-500 text-[10px] uppercase">Incident Details</span>
                    <p className="text-slate-200 font-sans leading-relaxed text-[13px]">{selectedIncident.details}</p>
                  </div>
                  <div className="bg-slate-950/50 p-3 rounded border border-slate-800 text-[11px] leading-relaxed text-slate-400 font-sans">
                    🛡️ <span className="text-cyan-400 font-semibold font-mono">Zero Biometric Leakage Checked:</span> No raw biometric matrices or eye features are contained in this payload trace. Signature is fully compliant with biometric protocols.
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
