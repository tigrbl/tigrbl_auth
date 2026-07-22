import React, { useState } from 'react';
import { ProviderProfile } from '../types';
import { Activity, ShieldAlert, CheckCircle, RefreshCw, Layers, Edit3, Save, AlertTriangle } from 'lucide-react';

interface ProviderConfigHealthProps {
  providers: ProviderProfile[];
  onUpdateProvider: (updated: ProviderProfile) => void;
}

export default function ProviderConfigHealth({ providers, onUpdateProvider }: ProviderConfigHealthProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editForm, setEditForm] = useState<Partial<ProviderProfile>>({});
  const [testPayload, setTestPayload] = useState<string>(
    JSON.stringify({
      iss: "https://auth.enterprise-idp.com",
      sub: "usr_9921",
      amr: ["hw", "user", "fpt"],
      uv: true,
      nonce: "4a2c91ea",
      device_trust: "certified_secure_enclave"
    }, null, 2)
  );
  
  const [mappedResult, setMappedResult] = useState<any>(null);
  const [mappingError, setMappingError] = useState<string | null>(null);

  // Simulated metrics
  const errorMetrics = {
    outagesCount: 1,
    invalidSignatures: 3,
    staleEvidence: 12,
    unsupportedClaims: 8,
    transformationFailures: 4
  };

  const handleStartEdit = (p: ProviderProfile) => {
    setEditingId(p.id);
    setEditForm(p);
  };

  const handleSave = () => {
    if (editingId && editForm) {
      onUpdateProvider(editForm as ProviderProfile);
      setEditingId(null);
    }
  };

  const runMappingSimulation = () => {
    try {
      setMappingError(null);
      const parsed = JSON.parse(testPayload);
      
      // Look up matching provider
      const activeProvider = providers.find(p => p.issuerUrl === parsed.iss || testPayload.includes(p.issuerUrl));
      if (!activeProvider) {
        setMappingError(`No registered provider matches issuer: ${parsed.iss}`);
        setMappedResult(null);
        return;
      }

      if (activeProvider.status === 'outage') {
        setMappingError(`Transformation aborted: Provider [${activeProvider.name}] is currently in an OUTAGE state.`);
        setMappedResult(null);
        return;
      }

      // Execute transformation mapping rules
      const containsFpt = parsed.amr && parsed.amr.includes('fpt');
      const containsUv = parsed.uv === true || (parsed.amr && parsed.amr.includes('uv'));
      
      let finalAmr = [...(parsed.amr || [])];
      let transformedEvidence = false;

      if (activeProvider.mappingRule === 'map_strict_fpt') {
        if (containsFpt) {
          transformedEvidence = true;
        } else {
          setMappingError("Strict mapping rule failed: 'fpt' was not present in the raw upstream amr list.");
        }
      } else if (activeProvider.mappingRule === 'infer_fpt_from_trust') {
        if (containsUv && parsed.device_trust === 'certified_secure_enclave') {
          transformedEvidence = true;
          if (!finalAmr.includes('fpt')) finalAmr.push('fpt');
        } else {
          setMappingError("Inference rule failed: requires both user verification and certified_secure_enclave state.");
        }
      }

      setMappedResult({
        issuer: activeProvider.name,
        upstreamAmr: parsed.amr || [],
        userVerificationFlag: containsUv,
        normalizedAmrs: finalAmr,
        evidenceFptVerified: transformedEvidence,
        directVsTransformed: activeProvider.mappingRule === 'map_strict_fpt' ? 'direct' : 'transformed',
        mappingApplied: activeProvider.mappingRule,
        trustEvaluation: transformedEvidence ? "TRUSTED_FINGERPRINT_AMR_APPROVED" : "GENERIC_USER_VERIFICATION_ONLY",
        fptTimestamp: new Date().toISOString()
      });
    } catch (e: any) {
      setMappingError(`Parsing Syntax Error: ${e.message}`);
      setMappedResult(null);
    }
  };

  return (
    <div className="space-y-6" id="provider-config-section">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h2 className="text-xl font-semibold text-slate-100 flex items-center gap-2">
            <Layers className="text-sky-400 w-5 h-5" />
            Upstream Identity Providers & Health
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Govern cryptographically federated OIDC/SAML assertion transforms and monitor service degradation.
          </p>
        </div>
        
        <div className="bg-slate-900 border border-slate-800 rounded-lg px-3 py-1.5 text-xs font-mono text-slate-400 flex items-center gap-2">
          <Activity className="text-emerald-400 w-3.5 h-3.5 animate-pulse" />
          <span>Transformation System Active</span>
        </div>
      </div>

      {/* Provider Cards */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-4" id="providers-grid">
        {providers.map((p) => {
          const isEditing = editingId === p.id;
          return (
            <div 
              key={p.id} 
              id={`provider-card-${p.id}`}
              className={`border rounded-xl p-4 transition-all duration-200 ${
                p.status === 'online' 
                  ? 'bg-slate-950/60 border-slate-800/80 hover:border-slate-700' 
                  : p.status === 'degraded'
                  ? 'bg-amber-950/10 border-amber-800/50 hover:border-amber-700/80'
                  : 'bg-rose-950/10 border-rose-900/60'
              }`}
            >
              <div className="flex justify-between items-start gap-2 mb-3">
                <div>
                  <span className={`text-2xs font-semibold uppercase tracking-wider px-2 py-0.5 rounded-full ${
                    p.status === 'online'
                      ? 'bg-emerald-400/10 text-emerald-400'
                      : p.status === 'degraded'
                      ? 'bg-amber-400/10 text-amber-400'
                      : 'bg-rose-400/10 text-rose-400'
                  }`}>
                    {p.status}
                  </span>
                  {isEditing ? (
                    <input 
                      type="text" 
                      className="mt-2 bg-slate-900 text-slate-100 text-sm font-semibold rounded px-2 py-1 border border-slate-700 w-full"
                      value={editForm.name || ''}
                      onChange={(e) => setEditForm({...editForm, name: e.target.value})}
                    />
                  ) : (
                    <h3 className="font-semibold text-slate-200 text-sm mt-1">{p.name}</h3>
                  )}
                </div>
                
                <button 
                  onClick={() => isEditing ? handleSave() : handleStartEdit(p)}
                  className="text-slate-400 hover:text-slate-200 p-1 rounded hover:bg-slate-800 transition"
                >
                  {isEditing ? <Save className="w-4 h-4 text-emerald-400" /> : <Edit3 className="w-4 h-4" />}
                </button>
              </div>

              <div className="space-y-2 text-xs font-mono text-slate-400">
                <div>
                  <span className="text-slate-500 block text-2xs uppercase">Issuer URL:</span>
                  {isEditing ? (
                    <input 
                      type="text" 
                      className="bg-slate-900 text-slate-300 text-2xs rounded px-2 py-1 border border-slate-700 w-full font-mono mt-1"
                      value={editForm.issuerUrl || ''}
                      onChange={(e) => setEditForm({...editForm, issuerUrl: e.target.value})}
                    />
                  ) : (
                    <span className="text-slate-300 truncate block">{p.issuerUrl}</span>
                  )}
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Mapping rule:</span>
                  {isEditing ? (
                    <select 
                      className="bg-slate-900 text-slate-300 text-xs rounded px-2 py-1 border border-slate-700 w-full mt-1"
                      value={editForm.mappingRule || ''}
                      onChange={(e) => setEditForm({...editForm, mappingRule: e.target.value as any})}
                    >
                      <option value="map_strict_fpt">Map Strict 'fpt' Claim</option>
                      <option value="infer_fpt_from_trust">Infer from Certified Hardware Enclave</option>
                      <option value="untrusted_fallback_generic">Untrusted (Yield generic UV only)</option>
                    </select>
                  ) : (
                    <span className="text-indigo-400">
                      {p.mappingRule === 'map_strict_fpt' 
                        ? 'Strict Explicit Match (fpt)' 
                        : p.mappingRule === 'infer_fpt_from_trust'
                        ? 'Verified Hardware Enclave Inference'
                        : 'Untrusted/Generic'}
                    </span>
                  )}
                </div>

                <div>
                  <span className="text-slate-500 block text-2xs uppercase font-sans">Freshness Window:</span>
                  {isEditing ? (
                    <div className="flex items-center gap-1 mt-1">
                      <input 
                        type="number" 
                        className="bg-slate-900 text-slate-300 text-xs rounded px-2 py-1 border border-slate-700 w-20"
                        value={editForm.freshnessLimitSeconds || 0}
                        onChange={(e) => setEditForm({...editForm, freshnessLimitSeconds: parseInt(e.target.value) || 60})}
                      />
                      <span className="text-slate-500 text-2xs">sec</span>
                    </div>
                  ) : (
                    <span className="text-slate-300">{p.freshnessLimitSeconds} seconds max age</span>
                  )}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* Trust & Diagnostic Failures Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-5" id="diagnostics-metrics-section">
        {/* Diagnostics Metrics */}
        <div className="bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-200 text-sm flex items-center gap-2">
            <ShieldAlert className="text-rose-400 w-4 h-4" />
            Governance Failure Metrics (Real-time Diagnostic Counts)
          </h3>
          <p className="text-xs text-slate-400 leading-relaxed">
            The platform tracks non-compliant or failed assertions to protect against brute-forcing and token manipulation.
          </p>

          <div className="grid grid-cols-2 sm:grid-cols-3 gap-3 font-mono text-center">
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-3">
              <span className="text-slate-500 text-2xs uppercase block">Outages Tracked</span>
              <span className="text-xl font-bold text-rose-400 block mt-1">{errorMetrics.outagesCount}</span>
            </div>
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-3">
              <span className="text-slate-500 text-2xs uppercase block">Bad Signatures</span>
              <span className="text-xl font-bold text-amber-500 block mt-1">{errorMetrics.invalidSignatures}</span>
            </div>
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-3">
              <span className="text-slate-500 text-2xs uppercase block">Stale Evidence</span>
              <span className="text-xl font-bold text-yellow-400 block mt-1">{errorMetrics.staleEvidence}</span>
            </div>
            <div className="bg-slate-900/60 border border-slate-800/80 rounded-lg p-3">
              <span className="text-slate-500 text-2xs uppercase block">Unsupported Claim</span>
              <span className="text-xl font-bold text-sky-400 block mt-1">{errorMetrics.unsupportedClaims}</span>
            </div>
            <div className="col-span-2 sm:col-span-1 bg-slate-900/60 border border-slate-800/80 rounded-lg p-3">
              <span className="text-slate-500 text-2xs uppercase block">Transform Error</span>
              <span className="text-xl font-bold text-slate-300 block mt-1">{errorMetrics.transformationFailures}</span>
            </div>
          </div>
        </div>

        {/* Dynamic Transformation Simulation Lab */}
        <div className="bg-slate-950 border border-slate-900 rounded-xl p-5 space-y-4">
          <h3 className="font-semibold text-slate-200 text-sm flex items-center gap-2">
            <RefreshCw className="text-indigo-400 w-4 h-4 animate-spin-slow" />
            Provider Transformation Sandbox
          </h3>
          <p className="text-xs text-slate-400">
            Edit simulated raw JSON claims below, then execute transformations according to registered mappings.
          </p>

          <div className="grid grid-cols-1 sm:grid-cols-12 gap-3">
            <div className="sm:col-span-6 space-y-1">
              <label className="text-2xs text-slate-500 uppercase block font-mono">Simulated Raw JWT Claims:</label>
              <textarea 
                className="bg-slate-900 text-slate-200 text-2xs font-mono p-2.5 rounded-lg border border-slate-800 w-full focus:outline-none focus:border-indigo-500"
                rows={7}
                value={testPayload}
                onChange={(e) => setTestPayload(e.target.value)}
              />
              <button 
                onClick={runMappingSimulation}
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-medium rounded-lg text-xs transition duration-200"
              >
                Execute Transformer Map
              </button>
            </div>

            <div className="sm:col-span-6 flex flex-col justify-between">
              <div>
                <span className="text-2xs text-slate-500 uppercase block font-mono mb-1">Server Normalized Result:</span>
                
                {mappingError && (
                  <div className="bg-rose-950/20 border border-rose-900/50 text-rose-300 text-2xs p-3 rounded-lg flex items-start gap-1.5 font-mono">
                    <AlertTriangle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
                    <span>{mappingError}</span>
                  </div>
                )}

                {mappedResult && (
                  <div className="bg-slate-900 text-slate-300 font-mono text-2xs p-3 rounded-lg border border-slate-800 space-y-1">
                    <div className="flex justify-between border-b border-slate-800 pb-1 mb-1">
                      <span className="text-slate-500">Issuer Mapped:</span>
                      <span className="text-slate-100 font-bold">{mappedResult.issuer}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Evidence FPT Mapped:</span>
                      <span className={mappedResult.evidenceFptVerified ? "text-emerald-400 font-bold" : "text-amber-400"}>
                        {mappedResult.evidenceFptVerified ? "TRUE (Verified)" : "FALSE"}
                      </span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Direct vs Transformed:</span>
                      <span className="text-indigo-400">{mappedResult.directVsTransformed}</span>
                    </div>
                    <div className="flex justify-between">
                      <span className="text-slate-500">Normalized AMRs:</span>
                      <span className="text-slate-300">[{mappedResult.normalizedAmrs.join(', ')}]</span>
                    </div>
                    <div className="text-2xs text-slate-500 mt-2 border-t border-slate-800 pt-1 flex justify-between">
                      <span>Result Action:</span>
                      <span className="text-slate-300">{mappedResult.trustEvaluation}</span>
                    </div>
                  </div>
                )}

                {!mappedResult && !mappingError && (
                  <div className="h-36 bg-slate-900/40 border border-slate-800 border-dashed rounded-lg flex items-center justify-center text-slate-500 text-xs text-center p-4">
                    Click "Execute Transformer Map" to view the converted, production-safe identity record.
                  </div>
                )}
              </div>
              <p className="text-3xs text-slate-500 leading-normal mt-2">
                *Diagnostics ensure raw client identifiers and physical biometrics are never imported or stored.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
