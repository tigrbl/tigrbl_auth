/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React from 'react';
import { HeartPulse, CheckCircle2, AlertTriangle, XCircle, Clock, Key, ShieldAlert } from 'lucide-react';
import { SystemHealthMetric } from '../types';

interface EnterpriseHealthSummaryProps {
  metrics: SystemHealthMetric;
}

export default function EnterpriseHealthSummary({ metrics }: EnterpriseHealthSummaryProps) {
  const getKdcStatusLabel = () => {
    switch (metrics.kdcStatus) {
      case 'healthy':
        return { label: 'Online / Replicated', color: 'text-emerald-700 bg-emerald-50 border-emerald-100', icon: <CheckCircle2 className="w-4 h-4 text-emerald-600" /> };
      case 'degraded':
        return { label: 'Degraded / Slow', color: 'text-amber-700 bg-amber-50 border-amber-100', icon: <AlertTriangle className="w-4 h-4 text-amber-500" /> };
      case 'unreachable':
        return { label: 'OFFLINE', color: 'text-rose-700 bg-rose-50 border-rose-100', icon: <XCircle className="w-4 h-4 text-rose-600" /> };
    }
  };

  const isClockSkewHealthy = Math.abs(metrics.clockDriftSeconds) < 300;
  const isKeyAgeHealthy = metrics.keyAgeDays < 180;

  const kdcStatus = getKdcStatusLabel();

  return (
    <div id="enterprise-health-summary" className="bg-white rounded-2xl border border-slate-200 p-6 space-y-6 shadow-sm">
      <div className="flex justify-between items-center border-b border-slate-100 pb-4">
        <div>
          <h3 className="font-display font-semibold text-slate-800 text-lg flex items-center gap-2">
            <HeartPulse className="w-5 h-5 text-rose-500" />
            Kerberos & Domain Controller Health Status
          </h3>
          <p className="text-xs text-slate-500">Live health telemetry of cross-realm federation tunnels and key distribution centers (KDC).</p>
        </div>
        <div className="text-right">
          <span className={`text-xs font-mono font-semibold px-2 py-0.5 rounded border ${
            metrics.conformanceStatus === 'passed' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
            metrics.conformanceStatus === 'warning' ? 'bg-amber-50 text-amber-700 border-amber-200' :
            'bg-rose-50 text-rose-700 border-rose-200'
          }`}>
            CONFORMANCE: {metrics.conformanceStatus.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        {/* KDC Availability card */}
        <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col justify-between space-y-3">
          <div className="flex justify-between items-start">
            <span className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider">KDC Reachability</span>
            {kdcStatus.icon}
          </div>
          <div>
            <p className="text-lg font-bold text-slate-800 font-mono">Active Directory</p>
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded inline-block mt-1 border ${kdcStatus.color}`}>
              {kdcStatus.label}
            </span>
          </div>
        </div>

        {/* System Clock Drift card */}
        <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col justify-between space-y-3">
          <div className="flex justify-between items-start">
            <span className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider">Clock Offset</span>
            <Clock className={`w-4 h-4 ${isClockSkewHealthy ? 'text-slate-400' : 'text-rose-600 animate-pulse'}`} />
          </div>
          <div>
            <p className={`text-lg font-bold font-mono ${isClockSkewHealthy ? 'text-slate-800' : 'text-rose-600'}`}>
              {metrics.clockDriftSeconds >= 0 ? '+' : ''}{metrics.clockDriftSeconds}s Offset
            </p>
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded inline-block mt-1 border ${
              isClockSkewHealthy ? 'bg-emerald-50 text-emerald-700 border-emerald-150' : 'bg-rose-50 text-rose-700 border-rose-150'
            }`}>
              {isClockSkewHealthy ? 'Synchronized (OK)' : 'CRITICAL DRIFT (>300s)'}
            </span>
          </div>
        </div>

        {/* DNS SRV record map */}
        <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col justify-between space-y-3">
          <div className="flex justify-between items-start">
            <span className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider">DNS SRV Maps</span>
            <CheckCircle2 className="w-4 h-4 text-emerald-600" />
          </div>
          <div>
            <p className="text-lg font-bold text-slate-800 font-mono">_kerberos._tcp</p>
            <span className="text-[11px] font-medium px-2 py-0.5 rounded inline-block mt-1 border bg-emerald-50 text-emerald-700 border-emerald-150">
              SRV Records Resolved
            </span>
          </div>
        </div>

        {/* Kerberos Cryptographic Keytab Age card */}
        <div className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 flex flex-col justify-between space-y-3">
          <div className="flex justify-between items-start">
            <span className="text-[10px] font-mono font-semibold text-slate-400 uppercase tracking-wider">Keytab Key Age</span>
            <Key className="w-4 h-4 text-slate-400" />
          </div>
          <div>
            <p className="text-lg font-bold text-slate-800 font-mono">{metrics.keyAgeDays} Days Old</p>
            <span className={`text-[11px] font-medium px-2 py-0.5 rounded inline-block mt-1 border ${
              isKeyAgeHealthy ? 'bg-emerald-50 text-emerald-700 border-emerald-150' : 'bg-amber-50 text-amber-700 border-amber-150'
            }`}>
              {isKeyAgeHealthy ? 'Key Cryptography Fresh' : 'Rotation Advised'}
            </span>
          </div>
        </div>
      </div>

      {!isClockSkewHealthy && (
        <div className="p-4 bg-rose-50 border border-rose-200 rounded-xl flex gap-3 text-rose-800 text-xs leading-relaxed animate-fadeIn">
          <ShieldAlert className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
          <div>
            <h4 className="font-bold">Active Directory Clock Drift Mismatch Enforced</h4>
            <p className="mt-0.5">
              Workstation system clock offset has exceeded the standard Kerberos KDC drift limit (5 minutes / 300s). Direct automatic logins (AMR wia) are currently blocked. Clock synchronization is required on client hosts to resume silent ticket exchanges.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
