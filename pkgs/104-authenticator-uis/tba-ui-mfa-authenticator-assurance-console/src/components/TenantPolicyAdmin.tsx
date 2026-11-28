/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { 
  Shield, 
  ToggleLeft, 
  ToggleRight, 
  HelpCircle, 
  AlertTriangle, 
  CheckCircle, 
  Clock, 
  Lock, 
  Users, 
  Activity, 
  Info,
  RefreshCw,
  TrendingUp,
  Sliders,
  Sparkles,
  ShieldAlert
} from 'lucide-react';
import { MfaPolicy, UserPosture, AuditEvent } from '../types';

interface TenantPolicyAdminProps {
  policy: MfaPolicy;
  onUpdatePolicy: (updates: Partial<MfaPolicy>) => void;
  users: UserPosture[];
  addAuditEvent: (event: Omit<AuditEvent, 'id' | 'timestamp'>) => void;
}

export default function TenantPolicyAdmin({
  policy,
  onUpdatePolicy,
  users,
  addAuditEvent,
}: TenantPolicyAdminProps) {
  // Local state for simulation tuning
  const [phishingResistant, setPhishingResistant] = useState(policy.enforcePhishingResistant);
  const [lockoutThreshold, setLockoutThreshold] = useState(policy.lockoutThreshold);
  const [rememberDeviceDays, setRememberDeviceDays] = useState(policy.rememberDeviceDays);
  const [gracePeriodDays, setGracePeriodDays] = useState(policy.gracePeriodDays);
  const [allowedFactors, setAllowedFactors] = useState(policy.allowedFactorTypes || ['passkey', 'security_key', 'totp', 'push', 'email_otp']);

  // Toggle factor types
  const handleToggleFactor = (type: any) => {
    let nextAllowed = [...allowedFactors];
    if (nextAllowed.includes(type)) {
      if (nextAllowed.length <= 1) {
        alert("Policy safety gate: You must allow at least one authentication factor type to prevent complete tenant lockout.");
        return;
      }
      nextAllowed = nextAllowed.filter(t => t !== type);
    } else {
      nextAllowed.push(type);
    }
    setAllowedFactors(nextAllowed);
  };

  // Run Rollout Predictor / Compliance Checker
  const runSimulation = () => {
    const nextVersion = parseFloat((policy.version + 0.1).toFixed(1));
    
    // Save state back to App state
    onUpdatePolicy({
      enforcePhishingResistant: phishingResistant,
      lockoutThreshold,
      rememberDeviceDays,
      gracePeriodDays,
      allowedFactorTypes: allowedFactors,
      version: nextVersion,
    });

    addAuditEvent({
      eventType: 'POLICY_PUBLISHED',
      subject: 'admin@acme.com',
      status: 'warning',
      policyVersion: nextVersion,
      detail: `Tenant published new Security Policy v${nextVersion}: Phishing Resistant Enforced=${phishingResistant}, Allowed Factors=[${allowedFactors.join(', ')}]`,
      ipAddress: '192.168.1.1',
      userAgent: navigator.userAgent,
    });
  };

  // Calculate simulated compliance status for users
  // Representative profiles:
  // 1. Jane: Passkey, Push, Recovery (Active)
  // 2. John: TOTP, Email OTP (Active, but TOTP isn't phishing-resistant)
  // 3. Alice: Passkey (Grace period)
  // 4. Bob: Email OTP, Recovery (Inactive, grace period elapsed)
  const getSimulationMetrics = () => {
    let compliantCount = 0;
    let graceCount = 0;
    let blockedCount = 0;

    const reports = users.map(user => {
      // Find what factors the user has
      const userFactorTypes = user.factors.map(f => f.type);
      const hasPasskeyOrSecKey = userFactorTypes.some(f => f === 'passkey' || f === 'security_key');
      const hasAllowedFactor = userFactorTypes.some(f => allowedFactors.includes(f));
      
      let status: 'Compliant' | 'Grace Period' | 'Blocked' = 'Compliant';
      let reason = 'All policy conditions fully met.';

      const isGracePeriod = user.enrollmentStatus === 'grace_period';

      // Check if user has ANY allowed factor
      if (!hasAllowedFactor) {
        if (isGracePeriod) {
          status = 'Grace Period';
          reason = `No active policy factor, but in enrollment grace period.`;
          graceCount++;
        } else {
          status = 'Blocked';
          reason = 'Zero active factors matching tenant policy allowed list.';
          blockedCount++;
        }
      } 
      // Check if phishing resistance is required, but user lacks it
      else if (phishingResistant && !hasPasskeyOrSecKey) {
        if (isGracePeriod) {
          status = 'Grace Period';
          reason = 'Lacks phishing-resistant FIDO2 factor. Grace period active.';
          graceCount++;
        } else {
          status = 'Blocked';
          reason = 'Lacks phishing-resistant FIDO2 factor. Enrollment gate elapsed.';
          blockedCount++;
        }
      } else {
        compliantCount++;
      }

      return {
        ...user,
        enrolledFactors: userFactorTypes,
        simStatus: status,
        simReason: reason,
      };
    });

    return {
      reports,
      compliantCount,
      graceCount,
      blockedCount,
      total: users.length,
    };
  };

  const metrics = getSimulationMetrics();
  const compliancePct = Math.round((metrics.compliantCount / metrics.total) * 100);

  return (
    <div className="flex-1 p-6 overflow-y-auto animate-fade-in" id="policy-admin">
      {/* Header */}
      <div className="mb-6 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 tracking-tight">Tenant MFA Policy Administration</h1>
          <p className="text-xs text-slate-500">Configure global cryptographic assurance constraints and enrollment gates.</p>
        </div>
        <div className="bg-slate-100 px-3 py-1.5 rounded-lg border border-slate-200 flex items-center gap-1.5 text-xs text-slate-700">
          <Sliders className="w-3.5 h-3.5 text-indigo-600 animate-pulse" />
          <span>Active Version: <strong className="font-mono text-indigo-700">v{policy.version}</strong></span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Side: Parameters Tuning */}
        <div className="lg:col-span-7 bg-white border border-slate-200 rounded-xl p-5 shadow-3xs space-y-6">
          <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest pb-3 border-b border-slate-100 flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-indigo-600" /> Policy Configuration Console
          </h2>

          {/* Enforce Phishing Resistant */}
          <div className="flex items-start justify-between gap-4">
            <div className="space-y-1">
              <span className="text-xs font-bold text-slate-800 flex items-center gap-1.5">
                Enforce Phishing-Resistant (FIDO2/WebAuthn)
                <span className="bg-emerald-50 text-emerald-800 text-[8px] font-bold px-1.5 py-0.2 rounded border border-emerald-100 uppercase tracking-tight">High Assurance</span>
              </span>
              <p className="text-[11px] text-slate-500 max-w-md">
                Force users to satisfy assurance objectives using asymmetric, hardware-bound credentials. Blocks SMTP OTP, TOTP, and Push fallback options for step-up actions.
              </p>
            </div>
            <button 
              onClick={() => setPhishingResistant(!phishingResistant)}
              className="text-indigo-600 hover:scale-105 transition-transform"
            >
              {phishingResistant ? (
                <ToggleRight className="w-11 h-6 shrink-0" />
              ) : (
                <ToggleLeft className="w-11 h-6 shrink-0 text-slate-300" />
              )}
            </button>
          </div>

          {/* Lockout Threshold */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-800">Challenge Lockout Threshold</label>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded font-mono border border-indigo-100">{lockoutThreshold} attempts</span>
            </div>
            <p className="text-[11px] text-slate-500">
              The number of failed multi-factor challenge attempts allowed before locking out the user's session.
            </p>
            <input 
              type="range" 
              min={2} 
              max={10} 
              value={lockoutThreshold}
              onChange={(e) => setLockoutThreshold(parseInt(e.target.value))}
              className="w-full accent-indigo-600 h-1.5 bg-slate-100 rounded-lg cursor-pointer"
            />
          </div>

          {/* Remember Devices */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-800">Remembered Device TTL</label>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded font-mono border border-indigo-100">{rememberDeviceDays} days</span>
            </div>
            <p className="text-[11px] text-slate-500">
              Number of days a secure device bypasses subsequent MFA step-up challenges for equivalent assurance levels.
            </p>
            <input 
              type="range" 
              min={1} 
              max={90} 
              value={rememberDeviceDays}
              onChange={(e) => setRememberDeviceDays(parseInt(e.target.value))}
              className="w-full accent-indigo-600 h-1.5 bg-slate-100 rounded-lg cursor-pointer"
            />
          </div>

          {/* Grace Period Duration */}
          <div className="space-y-2">
            <div className="flex justify-between items-center">
              <label className="text-xs font-bold text-slate-800">Enrollment Grace Period Duration</label>
              <span className="text-xs font-bold text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded font-mono border border-indigo-100">{gracePeriodDays} days</span>
            </div>
            <p className="text-[11px] text-slate-500">
              The duration newly provisioned accounts are permitted to authenticate before registering required multi-factor policies.
            </p>
            <input 
              type="range" 
              min={0} 
              max={30} 
              value={gracePeriodDays}
              onChange={(e) => setGracePeriodDays(parseInt(e.target.value))}
              className="w-full accent-indigo-600 h-1.5 bg-slate-100 rounded-lg cursor-pointer"
            />
          </div>

          {/* Allowed Factor Types Checklist */}
          <div className="space-y-3">
            <label className="text-xs font-bold text-slate-800 block">Allowed Factor Types</label>
            <p className="text-[11px] text-slate-500">
              Revoking factor types takes immediate effect global-wide, automatically de-registering them as active authentication methods.
            </p>
            <div className="grid grid-cols-2 gap-2.5">
              {[
                { id: 'passkey', name: 'Biometric Passkeys (FIDO2)' },
                { id: 'security_key', name: 'FIDO2 USB Tokens' },
                { id: 'totp', name: 'TOTP Software Apps' },
                { id: 'push', name: 'Push Notifications' },
                { id: 'email_otp', name: 'Email One-Time OTP' },
              ].map((item) => {
                const isSelected = allowedFactors.includes(item.id);
                return (
                  <div 
                    key={item.id}
                    onClick={() => handleToggleFactor(item.id)}
                    className={`p-2.5 border rounded-lg flex items-center justify-between cursor-pointer transition-colors ${
                      isSelected 
                        ? 'border-indigo-500 bg-indigo-50/10 text-slate-800' 
                        : 'border-slate-200 text-slate-400 bg-slate-50/50 hover:bg-slate-50'
                    }`}
                  >
                    <span className="text-[11px] font-semibold">{item.name}</span>
                    <span className={`w-3.5 h-3.5 rounded border flex items-center justify-center ${
                      isSelected ? 'bg-indigo-600 border-indigo-600 text-white' : 'border-slate-300'
                    }`}>
                      {isSelected && <span className="text-[9px]">✓</span>}
                    </span>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Commit Changes */}
          <div className="pt-4 border-t border-slate-100 flex justify-end gap-3">
            <button 
              onClick={() => {
                setPhishingResistant(policy.enforcePhishingResistant);
                setLockoutThreshold(policy.lockoutThreshold);
                setRememberDeviceDays(policy.rememberDeviceDays);
                setGracePeriodDays(policy.gracePeriodDays);
                setAllowedFactors(policy.allowedFactorTypes);
              }}
              className="px-4 py-2 border border-slate-200 text-slate-600 font-bold rounded-lg text-xs hover:bg-slate-50 transition-colors"
            >
              Reset Console
            </button>
            <button 
              onClick={runSimulation}
              className="px-5 py-2 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-lg text-xs shadow-xs hover:shadow-sm transition-all"
            >
              Publish Global Policy Update
            </button>
          </div>
        </div>

        {/* Right Side: Rollout Impact / Lockout Predictor */}
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-3xs flex flex-col justify-between">
            <div>
              <h2 className="text-xs font-bold text-slate-400 uppercase tracking-widest pb-3 border-b border-slate-100 flex items-center gap-1.5">
                <TrendingUp className="w-4 h-4 text-indigo-600" /> Rollout Impact & Lockout Predictor
              </h2>
              <p className="text-[11px] text-slate-500 mt-2">
                Simulated compliance metrics calculated using real user profiles in the directory. Perfect for avoiding widespread lockouts before committing updates.
              </p>

              {/* Chart Visualizer */}
              <div className="my-5 p-4 bg-slate-50 border border-slate-200/50 rounded-xl text-center">
                <div className="relative inline-flex items-center justify-center">
                  {/* Circular progress bar SVG */}
                  <svg className="w-28 h-28 transform -rotate-90">
                    <circle 
                      cx="56" 
                      cy="56" 
                      r="48" 
                      stroke="#f1f5f9" 
                      strokeWidth="8" 
                      fill="transparent" 
                    />
                    <circle 
                      cx="56" 
                      cy="56" 
                      r="48" 
                      stroke={compliancePct >= 75 ? '#10b981' : compliancePct >= 50 ? '#f59e0b' : '#ef4444'} 
                      strokeWidth="8" 
                      fill="transparent" 
                      strokeDasharray={301.6}
                      strokeDashoffset={301.6 - (301.6 * compliancePct) / 100}
                      className="transition-all duration-500"
                    />
                  </svg>
                  <div className="absolute text-center">
                    <span className="text-lg font-bold text-slate-800">{compliancePct}%</span>
                    <span className="block text-[8px] font-bold text-slate-400 uppercase tracking-widest">Compliance</span>
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2.5 mt-4 text-center">
                  <div className="bg-white border border-slate-200/50 rounded-lg p-2">
                    <span className="block text-[11px] font-bold text-emerald-600">{metrics.compliantCount}</span>
                    <span className="text-[9px] text-slate-400 uppercase">Compliant</span>
                  </div>
                  <div className="bg-white border border-slate-200/50 rounded-lg p-2">
                    <span className="block text-[11px] font-bold text-amber-600">{metrics.graceCount}</span>
                    <span className="text-[9px] text-slate-400 uppercase">Grace</span>
                  </div>
                  <div className="bg-white border border-slate-200/50 rounded-lg p-2">
                    <span className="block text-[11px] font-bold text-rose-600">{metrics.blockedCount}</span>
                    <span className="text-[9px] text-slate-400 uppercase">Blocked</span>
                  </div>
                </div>
              </div>

              {/* Detailed Simulation Reports */}
              <div className="space-y-2.5">
                <h4 className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Simulated User Directory Impact</h4>
                
                {metrics.reports.map(user => {
                  return (
                    <div 
                      key={user.id} 
                      className={`p-2.5 rounded-lg border text-left flex justify-between items-start gap-2.5 ${
                        user.simStatus === 'Compliant' ? 'bg-white border-slate-200' :
                        user.simStatus === 'Grace Period' ? 'bg-amber-50/30 border-amber-200/50' :
                        'bg-rose-50/30 border-rose-200/50'
                      }`}
                    >
                      <div className="space-y-0.5">
                        <div className="text-[11px] font-bold text-slate-800 flex items-center gap-1.5">
                          {user.name}
                          <span className="text-[9px] text-slate-400 font-normal">({user.email})</span>
                        </div>
                        <div className="text-[9px] text-slate-400">
                          Tokens: <code className="bg-slate-100 px-1 rounded font-mono text-[8px] text-slate-600">{user.enrolledFactors.join(', ')}</code>
                        </div>
                        <div className="text-[10px] text-slate-500 font-medium italic mt-1 leading-tight">
                          ↳ {user.simReason}
                        </div>
                      </div>

                      <span className={`px-1.5 py-0.5 text-[8px] font-bold rounded uppercase shrink-0 ${
                        user.simStatus === 'Compliant' ? 'bg-emerald-50 text-emerald-700 border border-emerald-100' :
                        user.simStatus === 'Grace Period' ? 'bg-amber-50 text-amber-700 border border-amber-100' :
                        'bg-rose-50 text-rose-700 border border-rose-100'
                      }`}>
                        {user.simStatus}
                      </span>
                    </div>
                  );
                })}
              </div>
            </div>

            {compliancePct < 75 && (
              <div className="mt-5 bg-amber-50 border border-amber-200 rounded-lg p-3 text-xs text-amber-800 flex items-start gap-1.5">
                <ShieldAlert className="w-4 h-4 shrink-0 text-amber-600 mt-0.5" />
                <div>
                  <strong className="font-semibold block">Lockout Hazard Warning</strong>
                  Publishing this policy forces <strong>{(100 - compliancePct)}%</strong> of your users into lockout or grace status immediately. Consider a phased rollout or enabling longer grace periods to avoid tickets.
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
