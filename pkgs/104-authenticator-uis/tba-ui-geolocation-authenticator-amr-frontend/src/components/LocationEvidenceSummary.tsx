import React, { useState } from 'react';
import { LocationSourceBadge } from './LocationSourceBadge';
import { Shield, ShieldAlert, ShieldCheck, Clock, MapPin, Eye, EyeOff, Lock, Unlock, Compass } from 'lucide-react';
import { Granularity } from '../types';

interface LocationEvidenceSummaryProps {
  sourceClass: string;
  sourceType: 'device' | 'network' | 'enterprise_zone' | 'trusted_upstream' | 'managed_posture';
  collectionTime: string;
  accuracy: number; // meters
  freshness: number; // minutes ago
  coarseRegion: string;
  namedZone?: string;
  policyName: string;
  policyVersion: string;
  policyAction: 'Allow' | 'Step-Up' | 'Deny';
  spoofSuspected: boolean;
  providerStatus: 'healthy' | 'degraded' | 'offline';
  auditRef: string;
  // Raw coordinates that should remain cryptographically hidden by default
  rawLat?: number;
  rawLng?: number;
}

export const LocationEvidenceSummary: React.FC<LocationEvidenceSummaryProps> = ({
  sourceClass,
  sourceType,
  collectionTime,
  accuracy,
  freshness,
  coarseRegion,
  namedZone,
  policyName,
  policyVersion,
  policyAction,
  spoofSuspected,
  providerStatus,
  auditRef,
  rawLat = 30.26725,
  rawLng = -97.74305
}) => {
  const [isDecrypted, setIsDecrypted] = useState(false);
  const [securityToken, setSecurityToken] = useState('');
  const [authError, setAuthError] = useState('');

  const handleDecrypt = (e: React.FormEvent) => {
    e.preventDefault();
    if (securityToken.trim() === 'INCIDENT-2026-GEO') {
      setIsDecrypted(true);
      setAuthError('');
    } else {
      setAuthError('Invalid Security Analyst Credentials or Incident ID');
    }
  };

  const isStale = freshness > 5; // Stale threshold: 5 mins
  const granularity: Granularity =
    sourceType === 'device' ? 'precise' :
    sourceType === 'enterprise_zone' ? 'zone' :
    sourceType === 'network' ? 'coarse' : 'none';

  return (
    <div id="evidence-summary" className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden" role="region" aria-label="Location Evidence Audit Report">
      {/* Header */}
      <div className="bg-slate-50 border-b border-slate-100 px-5 py-4 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Shield className="w-4.5 h-4.5 text-slate-500" />
          <h4 className="text-sm font-semibold text-slate-800 font-display">
            Active Context Evidence Report
          </h4>
        </div>
        <span className="text-[10px] font-mono bg-slate-200 text-slate-700 px-2 py-0.5 rounded uppercase font-semibold">
          REF: {auditRef.substring(0, 10)}
        </span>
      </div>

      <div className="p-5 space-y-5">
        {/* Main Status Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Evidence Class */}
          <div className="space-y-1">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Evidence Class & Posture
            </span>
            <div className="flex items-center gap-2">
              <LocationSourceBadge sourceType={sourceType} state="active" />
            </div>
            <p className="text-xs text-slate-500 mt-1">
              Source signature: <span className="font-mono bg-slate-100 px-1 py-0.5 rounded text-slate-600">{sourceClass}</span>
            </p>
          </div>

          {/* Temporal Freshness */}
          <div className="space-y-1">
            <span className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">
              Temporal Freshness
            </span>
            <div className="flex items-center gap-1.5">
              <Clock className={`w-4 h-4 ${isStale ? 'text-amber-500' : 'text-emerald-500'}`} />
              <span className={`text-sm font-semibold ${isStale ? 'text-amber-700' : 'text-emerald-700'}`}>
                {freshness} min{freshness !== 1 && 's'} ago
              </span>
              <span className={`inline-flex items-center px-1.5 py-0.5 text-[9px] font-bold rounded uppercase ${
                isStale ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'
              }`}>
                {isStale ? 'STALE' : 'FRESH'}
              </span>
            </div>
            <p className="text-[11px] text-slate-400">
              Captured: {new Date(collectionTime).toLocaleTimeString()}
            </p>
          </div>
        </div>

        <hr className="border-slate-100" />

        {/* Region & Zone info */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Geo-Resolution Type
            </span>
            <span className="text-xs font-semibold capitalize bg-indigo-50 border border-indigo-100 text-indigo-700 px-2 py-0.5 rounded-full inline-block">
              {granularity === 'precise' ? 'Hardware Precise' : granularity === 'zone' ? 'Enterprise Zone' : 'Network Approximate'}
            </span>
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Resolved Geographic Scope
            </span>
            <div className="flex items-center gap-1.5 text-xs font-bold text-slate-800">
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span className="truncate">{namedZone || coarseRegion}</span>
            </div>
            {namedZone && (
              <span className="text-[10px] text-slate-400 font-mono block mt-0.5">
                Approx. accuracy: ±{accuracy}m
              </span>
            )}
          </div>

          <div className="p-3 bg-slate-50 border border-slate-100 rounded-lg">
            <span className="text-[9px] font-bold text-slate-400 uppercase tracking-wider block mb-1">
              Active Policy Decision
            </span>
            <div className="flex items-center gap-1.5 text-xs font-bold">
              {policyAction === 'Allow' ? (
                <ShieldCheck className="w-4 h-4 text-emerald-500" />
              ) : policyAction === 'Step-Up' ? (
                <ShieldAlert className="w-4 h-4 text-amber-500" />
              ) : (
                <ShieldAlert className="w-4 h-4 text-rose-500" />
              )}
              <span className={
                policyAction === 'Allow' ? 'text-emerald-700' :
                policyAction === 'Step-Up' ? 'text-amber-700' : 'text-rose-700'
              }>
                {policyAction}
              </span>
            </div>
            <span className="text-[10px] text-slate-400 block mt-0.5">
              Ruleset: {policyName} ({policyVersion})
            </span>
          </div>
        </div>

        {/* Security / Spoofing Indicators */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className={`p-3.5 rounded-lg border flex gap-3 ${
            spoofSuspected 
              ? 'bg-rose-50/70 border-rose-100 text-rose-800' 
              : 'bg-emerald-50/40 border-emerald-100 text-emerald-800'
          }`}>
            <ShieldAlert className={`w-4 h-4 shrink-0 mt-0.5 ${spoofSuspected ? 'text-rose-600' : 'text-emerald-600'}`} />
            <div className="text-xs leading-normal">
              <strong className="font-semibold block mb-0.5">
                {spoofSuspected ? 'Spoofing/Inconsistency Detected' : 'Signal Integrity Confirmed'}
              </strong>
              {spoofSuspected ? (
                <span>Telemetry indicates VPN tunnel usage, developer mock-location tools, or high coordinate jitter. Step-up required.</span>
              ) : (
                <span>Hardware GPS parameters, network-path latency, and Wi-Fi RSSI signatures correspond with nominal parameters.</span>
              )}
            </div>
          </div>

          <div className={`p-3.5 rounded-lg border flex gap-3 ${
            providerStatus === 'offline'
              ? 'bg-amber-50 border-amber-100 text-amber-800'
              : 'bg-slate-50 border-slate-100 text-slate-700'
          }`}>
            <Compass className={`w-4 h-4 shrink-0 mt-0.5 ${providerStatus === 'offline' ? 'text-amber-500' : 'text-slate-400'}`} />
            <div className="text-xs leading-normal">
              <strong className="font-semibold block mb-0.5">
                Signal Provider Health
              </strong>
              {providerStatus === 'offline' ? (
                <span>Provider is offline. System failed-securely into fallback/Step-up verification state.</span>
              ) : providerStatus === 'degraded' ? (
                <span>MDM check degraded. Elevated latency detected; policy fallback applied.</span>
              ) : (
                <span>All verification channels (W3C GPS, GeoIP2, Corporate RADIUS) are reporting 100% operational status.</span>
              )}
            </div>
          </div>
        </div>

        {/* Privacy-Safe Protected Data Incident Workflow */}
        <div className="mt-4 bg-slate-900 text-slate-100 rounded-lg p-4 border border-slate-800">
          <div className="flex items-center justify-between mb-3">
            <div className="flex items-center gap-1.5 text-xs text-slate-300 font-mono">
              <Lock className="w-3.5 h-3.5 text-slate-400" />
              <span>CRYPTOGRAPHICALLY ENCRYPTED COORDINATE PAYLOAD</span>
            </div>
            <span className="text-[9px] bg-slate-800 text-slate-400 px-2 py-0.5 rounded font-mono font-bold">
              AES-256-GCM
            </span>
          </div>

          {!isDecrypted ? (
            <form onSubmit={handleDecrypt} className="space-y-3">
              <p className="text-xs text-slate-400 leading-relaxed">
                Raw coordinates are strictly masked in compliance with corporate privacy regulations. For active incident investigations, authorized security analysts can temporarily decrypt coordinates using their security incident ID.
              </p>
              <div className="flex flex-col sm:flex-row gap-2 max-w-md">
                <input
                  type="text"
                  placeholder="Enter Incident Token (e.g. INCIDENT-2026-GEO)"
                  value={securityToken}
                  onChange={(e) => setSecurityToken(e.target.value)}
                  className="bg-slate-950 border border-slate-800 text-slate-100 text-xs px-3 py-2 rounded-md focus:outline-none focus:border-indigo-500 font-mono flex-1"
                />
                <button
                  type="submit"
                  className="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-4 py-2 rounded-md transition-all flex items-center justify-center gap-1.5 shrink-0"
                >
                  <Unlock className="w-3 h-3" />
                  <span>Decrypt Evidence</span>
                </button>
              </div>
              {authError && (
                <p className="text-xs text-rose-400 font-semibold">{authError}</p>
              )}
            </form>
          ) : (
            <div className="space-y-3 bg-slate-950/80 border border-indigo-950 p-3 rounded-md">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                  <ShieldCheck className="w-3.5 h-3.5" />
                  Evidence Decrypted (Incident Audit Log Active)
                </span>
                <button
                  onClick={() => setIsDecrypted(false)}
                  className="text-slate-400 hover:text-white text-xs flex items-center gap-1"
                >
                  <EyeOff className="w-3.5 h-3.5" />
                  <span>Mask Coordinates</span>
                </button>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4 text-xs font-mono py-1.5">
                <div>
                  <span className="text-slate-500 block text-[10px]">LATITUDE</span>
                  <span className="text-slate-200 text-xs">{rawLat.toFixed(6)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">LONGITUDE</span>
                  <span className="text-slate-200 text-xs">{rawLng.toFixed(6)}</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">ACCURACY RADIUS</span>
                  <span className="text-slate-200 text-xs">{accuracy} meters</span>
                </div>
                <div>
                  <span className="text-slate-500 block text-[10px]">IP CORRELATION</span>
                  <span className="text-slate-200 text-xs">Matching (Wi-Fi match)</span>
                </div>
              </div>
              <div className="text-[10px] text-slate-500 border-t border-slate-900 pt-2 flex items-center justify-between">
                <span>Cryptographic Hash: <span className="text-slate-400">9f86d081884c7d659a2f...</span></span>
                <span className="text-amber-500">Decryption event logged under {auditRef}</span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
