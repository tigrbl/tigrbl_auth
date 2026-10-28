import React, { useState } from 'react';
import { 
  Plus, 
  Trash2, 
  Check, 
  Activity, 
  ShieldCheck, 
  AlertTriangle, 
  Clock, 
  Sliders, 
  Database,
  RefreshCw,
  Eye,
  Settings,
  ToggleLeft,
  ToggleRight,
  Info
} from 'lucide-react';
import { PolicyRule, ProviderHealth, RiskLevel, RiskDecision, AuthMethod } from '../types';

interface AdminPolicyEditorProps {
  policyRules: PolicyRule[];
  onUpdateRules: (newRules: PolicyRule[]) => void;
  providerHealth: ProviderHealth[];
  allMethods: AuthMethod[];
}

export default function AdminPolicyEditor({
  policyRules,
  onUpdateRules,
  providerHealth,
  allMethods
}: AdminPolicyEditorProps) {
  // Local state for adding a new rule
  const [showAddRuleForm, setShowAddRuleForm] = useState<boolean>(false);
  const [newRule, setNewRule] = useState<Partial<PolicyRule>>({
    name: '',
    riskLevel: 'medium',
    conditions: [{ field: 'sig_impossible_travel', operator: 'equals', value: 'compromised' }],
    outcome: 'step-up',
    eligibleMethods: ['auth_passkey'],
    fallbackMethod: 'auth_email_otp',
    freshnessThreshold: 300,
    missingSignalBehavior: 'fail-closed',
    enabled: true
  });

  const toggleRuleEnabled = (ruleId: string) => {
    const updated = policyRules.map(rule => {
      if (rule.id === ruleId) {
        return { ...rule, enabled: !rule.enabled };
      }
      return rule;
    });
    onUpdateRules(updated);
  };

  const deleteRule = (ruleId: string) => {
    const updated = policyRules.filter(rule => rule.id !== ruleId);
    onUpdateRules(updated);
  };

  const handleAddConditionFieldChange = (idx: number, field: string) => {
    const conds = [...(newRule.conditions || [])];
    conds[idx] = { ...conds[idx], field };
    setNewRule({ ...newRule, conditions: conds });
  };

  const handleAddConditionValueChange = (idx: number, value: string) => {
    const conds = [...(newRule.conditions || [])];
    conds[idx] = { ...conds[idx], value };
    setNewRule({ ...newRule, conditions: conds });
  };

  const handleToggleEligibleMethod = (methodId: string) => {
    const active = [...(newRule.eligibleMethods || [])];
    if (active.includes(methodId)) {
      setNewRule({ ...newRule, eligibleMethods: active.filter(m => m !== methodId) });
    } else {
      setNewRule({ ...newRule, eligibleMethods: [...active, methodId] });
    }
  };

  const submitNewRule = (e: React.FormEvent) => {
    e.preventDefault();
    if (!newRule.name) return;

    const finalRule: PolicyRule = {
      id: 'rule_' + Math.random().toString(36).substring(2, 7),
      name: newRule.name,
      riskLevel: newRule.riskLevel as RiskLevel,
      conditions: newRule.conditions || [],
      outcome: newRule.outcome as RiskDecision,
      eligibleMethods: newRule.eligibleMethods || [],
      fallbackMethod: newRule.fallbackMethod || 'auth_email_otp',
      freshnessThreshold: Number(newRule.freshnessThreshold) || 300,
      missingSignalBehavior: newRule.missingSignalBehavior as 'fail-closed' | 'fail-open' | 'step-up',
      enabled: true
    };

    onUpdateRules([finalRule, ...policyRules]);
    setShowAddRuleForm(false);
    // Reset form
    setNewRule({
      name: '',
      riskLevel: 'medium',
      conditions: [{ field: 'sig_impossible_travel', operator: 'equals', value: 'compromised' }],
      outcome: 'step-up',
      eligibleMethods: ['auth_passkey'],
      fallbackMethod: 'auth_email_otp',
      freshnessThreshold: 300,
      missingSignalBehavior: 'fail-closed',
      enabled: true
    });
  };

  return (
    <div id="admin-policy-editor" className="space-y-6">
      
      {/* 1. Rule Engine Section */}
      <div className="rounded-2xl border border-slate-200 bg-white shadow-xs p-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
          <div>
            <div className="flex items-center gap-2">
              <Sliders className="h-5 w-5 text-slate-700" />
              <h3 className="font-display text-lg font-bold text-slate-900">Adaptive Risk Rules Builder</h3>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-sans">
              Deploy named condition matrices. Prioritized from top to bottom. Order of enforcement matters.
            </p>
          </div>

          <button
            onClick={() => setShowAddRuleForm(!showAddRuleForm)}
            className="inline-flex items-center gap-1.5 rounded-xl bg-slate-900 hover:bg-slate-800 text-white py-2 px-3.5 text-xs font-semibold shadow-xs transition"
          >
            {showAddRuleForm ? 'Hide Form' : 'Add Custom Rule'}
            {!showAddRuleForm && <Plus className="h-4.5 w-4.5" />}
          </button>
        </div>

        {/* Custom Rule Creation Form */}
        {showAddRuleForm && (
          <form onSubmit={submitNewRule} className="mb-6 p-4 rounded-xl border border-slate-200 bg-slate-50 space-y-4">
            <h4 className="font-display font-semibold text-xs text-slate-900 uppercase tracking-wider border-b border-slate-200 pb-2">
              Create New Policy Constraint
            </h4>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase">Rule Name</label>
                <input
                  type="text"
                  required
                  placeholder="e.g. Impossible Travel high-assurance"
                  value={newRule.name}
                  onChange={e => setNewRule({ ...newRule, name: e.target.value })}
                  className="w-full text-xs border border-slate-200 rounded-lg p-2.5 bg-white"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase">Condition Logic Match</label>
                {newRule.conditions?.map((cond, idx) => (
                  <div key={idx} className="flex gap-2 items-center">
                    <select
                      value={cond.field}
                      onChange={e => handleAddConditionFieldChange(idx, e.target.value)}
                      className="text-xs border border-slate-200 rounded-lg p-2 bg-white flex-1"
                    >
                      <option value="sig_impossible_travel">Impossible Travel</option>
                      <option value="sig_device_integrity">Device Attestation</option>
                      <option value="sig_behavioral_typing">Keystroke Dynamics</option>
                      <option value="sig_ip_reputation">IP Reputation</option>
                      <option value="sig_network_vpn">VPN Connection</option>
                    </select>

                    <span className="text-xs font-mono text-slate-400">IS</span>

                    <select
                      value={cond.value}
                      onChange={e => handleAddConditionValueChange(idx, e.target.value)}
                      className="text-xs border border-slate-200 rounded-lg p-2 bg-white flex-1"
                    >
                      <option value="compromised">compromised</option>
                      <option value="suspicious">suspicious</option>
                      <option value="unavailable">unavailable</option>
                      <option value="safe">safe</option>
                    </select>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 pt-2">
              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase">Adaptive Outcome</label>
                <select
                  value={newRule.outcome}
                  onChange={e => setNewRule({ ...newRule, outcome: e.target.value as RiskDecision })}
                  className="w-full text-xs border border-slate-200 rounded-lg p-2 bg-white"
                >
                  <option value="continue">Continue (Allow Bypass)</option>
                  <option value="step-up">Step-up (MF required)</option>
                  <option value="review">Review Pending (Ops Queue)</option>
                  <option value="deny">Deny Access (Strict Block)</option>
                  <option value="recover">Recover (Re-keying Workspace)</option>
                </select>
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase">Freshness Threshold (sec)</label>
                <input
                  type="number"
                  min={10}
                  max={3600}
                  value={newRule.freshnessThreshold}
                  onChange={e => setNewRule({ ...newRule, freshnessThreshold: Number(e.target.value) })}
                  className="w-full text-xs border border-slate-200 rounded-lg p-2 bg-white font-mono"
                />
              </div>

              <div>
                <label className="block text-xs font-mono text-slate-500 mb-1.5 uppercase">Missing Signal Fail behavior</label>
                <select
                  value={newRule.missingSignalBehavior}
                  onChange={e => setNewRule({ ...newRule, missingSignalBehavior: e.target.value as any })}
                  className="w-full text-xs border border-slate-200 rounded-lg p-2 bg-white"
                >
                  <option value="fail-closed">Fail Closed (Lockout)</option>
                  <option value="fail-open">Fail Open (Allow)</option>
                  <option value="step-up">Enforce Step-up</option>
                </select>
              </div>
            </div>

            {/* Step-up Allowed Authenticators Selection */}
            {newRule.outcome === 'step-up' && (
              <div className="pt-2 border-t border-slate-200">
                <label className="block text-xs font-mono text-slate-500 mb-2 uppercase">Allowed High-Assurance Authenticators</label>
                <div className="flex flex-wrap gap-2">
                  {allMethods.map(m => {
                    const isSelected = newRule.eligibleMethods?.includes(m.id);
                    return (
                      <button
                        type="button"
                        key={m.id}
                        onClick={() => handleToggleEligibleMethod(m.id)}
                        className={`text-xs px-2.5 py-1 rounded-md border font-sans transition ${
                          isSelected 
                            ? 'bg-slate-900 border-slate-900 text-white' 
                            : 'bg-white border-slate-200 text-slate-600 hover:border-slate-400'
                        }`}
                      >
                        {m.name}
                      </button>
                    );
                  })}
                </div>
              </div>
            )}

            <div className="flex justify-end gap-2 pt-3 border-t border-slate-200">
              <button
                type="button"
                onClick={() => setShowAddRuleForm(false)}
                className="rounded-lg border border-slate-200 bg-white py-1.5 px-3 text-xs font-semibold text-slate-700 hover:bg-slate-50"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="rounded-lg bg-slate-900 hover:bg-slate-800 py-1.5 px-3 text-xs font-semibold text-white shadow-sm"
              >
                Deploy Rule
              </button>
            </div>
          </form>
        )}

        {/* Policy Rules List */}
        <div className="space-y-3.5">
          {policyRules.map((rule, index) => {
            return (
              <div
                key={rule.id}
                className={`flex flex-col md:flex-row md:items-center justify-between gap-4 p-4 rounded-xl border transition duration-150 ${
                  rule.enabled 
                    ? 'bg-white border-slate-200 hover:border-slate-300' 
                    : 'bg-slate-50 border-slate-200/60 opacity-65'
                }`}
              >
                {/* Left Rule details */}
                <div className="space-y-1.5 flex-1">
                  <div className="flex items-center gap-2">
                    <span className="text-xs font-mono font-medium text-slate-400">
                      #{index + 1}
                    </span>
                    <h4 className="font-display font-bold text-sm text-slate-900">{rule.name}</h4>
                    <span className={`inline-flex items-center rounded-sm px-1.5 py-0.2 text-[10px] font-mono font-medium border ${
                      rule.riskLevel === 'critical' ? 'bg-red-50 text-red-700 border-red-200'
                      : rule.riskLevel === 'high' ? 'bg-orange-50 text-orange-700 border-orange-200'
                      : rule.riskLevel === 'medium' ? 'bg-amber-50 text-amber-700 border-amber-200'
                      : 'bg-emerald-50 text-emerald-700 border-emerald-200'
                    }`}>
                      {rule.riskLevel.toUpperCase()}
                    </span>
                  </div>

                  {/* Conditions details */}
                  <div className="flex flex-wrap items-center gap-2 text-xs font-mono text-slate-500">
                    <span className="text-slate-400">Enforcement:</span>
                    {rule.conditions.map((cond, cIdx) => (
                      <span key={cIdx} className="bg-slate-100 px-2 py-0.5 rounded text-slate-700">
                        {cond.field === 'sig_impossible_travel' ? 'Impossible Travel' 
                        : cond.field === 'sig_device_integrity' ? 'Device Attestation'
                        : cond.field === 'sig_behavioral_typing' ? 'Keystroke Dynamics'
                        : cond.field === 'sig_ip_reputation' ? 'IP Reputation'
                        : 'VPN Detector'} {cond.operator.replace('_', ' ')} <strong className="text-slate-900">{cond.value}</strong>
                      </span>
                    ))}
                  </div>

                  {/* Adaptive fallback and behaviors info */}
                  <div className="flex flex-wrap gap-4 text-[11px] font-sans text-slate-500">
                    <span>Freshness: <strong className="text-slate-700">{rule.freshnessThreshold}s max</strong></span>
                    <span>Fail mode: <strong className="text-slate-700 capitalize">{rule.missingSignalBehavior}</strong></span>
                    {rule.outcome === 'step-up' && (
                      <span className="truncate max-w-[250px]">
                        Allowed MF: <strong className="text-slate-700">{rule.eligibleMethods.map(m => m.replace('auth_', '')).join(', ')}</strong>
                      </span>
                    )}
                  </div>
                </div>

                {/* Outcome Actions & Toggles */}
                <div className="flex items-center gap-4 flex-shrink-0 border-t md:border-t-0 pt-3 md:pt-0 border-slate-100">
                  <div className="text-right">
                    <span className="text-[10px] text-slate-400 font-mono block">ADAPTIVE ACTION</span>
                    <span className={`text-xs font-mono font-bold capitalize px-2 py-0.5 rounded ${
                      rule.outcome === 'deny' ? 'bg-red-100 text-red-800'
                      : rule.outcome === 'step-up' ? 'bg-amber-100 text-amber-800'
                      : rule.outcome === 'review' ? 'bg-indigo-100 text-indigo-800'
                      : 'bg-emerald-100 text-emerald-800'
                    }`}>
                      {rule.outcome}
                    </span>
                  </div>

                  <button
                    onClick={() => toggleRuleEnabled(rule.id)}
                    className="text-slate-400 hover:text-slate-900 transition"
                    title={rule.enabled ? 'Disable rule' : 'Enable rule'}
                  >
                    {rule.enabled ? (
                      <ToggleRight className="h-7 w-7 text-emerald-500" />
                    ) : (
                      <ToggleLeft className="h-7 w-7 text-slate-300" />
                    )}
                  </button>

                  <button
                    onClick={() => deleteRule(rule.id)}
                    className="text-slate-300 hover:text-red-600 transition"
                    title="Delete rule"
                  >
                    <Trash2 className="h-4.5 w-4.5" />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* 2. Provider Registry & Health */}
      <div id="signal-provider-health" className="rounded-2xl border border-slate-200 bg-white shadow-xs p-6">
        <div className="flex items-center justify-between mb-4">
          <div>
            <div className="flex items-center gap-2">
              <Activity className="h-5 w-5 text-slate-700" />
              <h3 className="font-display text-lg font-bold text-slate-900">Signal Provider Health (P2)</h3>
            </div>
            <p className="text-xs text-slate-500 mt-1 font-sans">
              Monitoring telemetry pipeline latencies, authentication event error spikes, and source freshness.
            </p>
          </div>

          <span className="inline-flex items-center rounded-full bg-emerald-50 px-2.5 py-0.5 text-xs font-mono font-medium text-emerald-700 ring-1 ring-inset ring-emerald-600/20">
            Pipeline: 100% Active
          </span>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {providerHealth.map(provider => {
            const hasError = provider.errorRate > 0.3;
            const isDegraded = provider.status === 'degraded' || hasError;
            return (
              <div 
                key={provider.id} 
                className="border border-slate-100 bg-slate-50/50 p-4 rounded-xl space-y-3.5"
              >
                <div className="flex items-center justify-between">
                  <div className="min-w-0">
                    <h4 className="font-display font-semibold text-xs text-slate-900 truncate" title={provider.name}>
                      {provider.name}
                    </h4>
                    <span className="text-[9px] font-mono text-slate-400 uppercase tracking-wider block">
                      {provider.type} provider
                    </span>
                  </div>

                  <span className={`h-2 w-2 rounded-full flex-shrink-0 ${
                    provider.status === 'active' ? 'bg-emerald-500' 
                    : provider.status === 'degraded' ? 'bg-amber-400'
                    : 'bg-rose-500'
                  }`} />
                </div>

                <div className="grid grid-cols-3 gap-1 text-[10px] font-mono text-slate-500">
                  <div>
                    <span className="block text-slate-400 uppercase text-[8px]">Latency</span>
                    <span className="font-bold text-slate-800 mt-0.5 block">{provider.latency}ms</span>
                  </div>
                  <div>
                    <span className="block text-slate-400 uppercase text-[8px]">Error Rate</span>
                    <span className={`font-bold mt-0.5 block ${hasError ? 'text-rose-600' : 'text-slate-800'}`}>
                      {provider.errorRate}%
                    </span>
                  </div>
                  <div>
                    <span className="block text-slate-400 uppercase text-[8px]">Uptime</span>
                    <span className="font-bold text-slate-800 mt-0.5 block">{provider.freshness}</span>
                  </div>
                </div>

                <div className="flex justify-between items-center text-[9px] font-mono text-slate-400 pt-2 border-t border-slate-200/50">
                  <span>Last verified: {provider.lastChecked}</span>
                  <span>Health: OK</span>
                </div>
              </div>
            );
          })}
        </div>
      </div>

    </div>
  );
}
