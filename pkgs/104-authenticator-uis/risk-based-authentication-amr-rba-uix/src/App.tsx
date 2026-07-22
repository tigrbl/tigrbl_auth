import React, { useState, useMemo } from 'react';
import Header from './components/Header';
import AdaptiveUserCeremony from './components/AdaptiveUserCeremony';
import PolicySimulatorWorkbench from './components/PolicySimulatorWorkbench';
import AdminPolicyEditor from './components/AdminPolicyEditor';
import SecurityInvestigationLogs from './components/SecurityInvestigationLogs';

import { 
  INITIAL_SIGNALS, 
  INITIAL_POLICY_RULES, 
  SIMULATION_SCENARIOS, 
  INITIAL_PROVIDER_HEALTH, 
  INITIAL_AUDIT_LOGS, 
  INITIAL_SESSIONS,
  AUTHENTICATORS
} from './data';
import { 
  RiskSignal, 
  PolicyRule, 
  ProviderHealth, 
  AuditLog, 
  ActiveSession, 
  RiskDecision, 
  RiskLevel, 
  SignalStatus,
  SimulationScenario
} from './types';

import { Sliders, Shield, Database, LayoutGrid, Info, ShieldAlert } from 'lucide-react';

export default function App() {
  // Application Data States
  const [activeSignals, setActiveSignals] = useState<RiskSignal[]>(INITIAL_SIGNALS);
  const [policyRules, setPolicyRules] = useState<PolicyRule[]>(INITIAL_POLICY_RULES);
  const [providerHealth, setProviderHealth] = useState<ProviderHealth[]>(INITIAL_PROVIDER_HEALTH);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(INITIAL_AUDIT_LOGS);
  const [activeSessions, setActiveSessions] = useState<ActiveSession[]>(INITIAL_SESSIONS);
  
  const [activeScenarioId, setActiveScenarioId] = useState<string>('scen_known_good');
  const [isEvaluating, setIsEvaluating] = useState<boolean>(false);

  // Active navigation tab for the administrative/ops pane
  const [adminTab, setAdminTab] = useState<'simulator' | 'rules' | 'audit'>('simulator');

  // RBA Live Decision Matching Engine
  const computedOutputs = useMemo(() => {
    // 1. Calculate general computed risk level based on signals status
    let highestRisk: RiskLevel = 'low';
    const statuses = activeSignals.map(s => s.status);
    
    if (statuses.includes('compromised')) {
      highestRisk = 'critical';
    } else if (statuses.includes('suspicious')) {
      highestRisk = 'high';
    } else if (statuses.includes('unavailable')) {
      highestRisk = 'medium';
    }

    // 2. Sequential rule-matching algorithm
    // We prioritize rule evaluation based on riskLevel precedence: critical -> high -> medium -> low
    const rulePriorityOrder: RiskLevel[] = ['critical', 'high', 'medium', 'low'];
    let matchedRule: PolicyRule | null = null;

    // Filter enabled rules and sort them by priority level first
    const activeRules = policyRules.filter(r => r.enabled);

    for (const level of rulePriorityOrder) {
      const levelRules = activeRules.filter(r => r.riskLevel === level);
      for (const rule of levelRules) {
        // Evaluate conditions
        const isMatch = rule.conditions.every(cond => {
          const signal = activeSignals.find(s => s.id === cond.field);
          if (!signal) return false;
          
          if (cond.operator === 'equals') {
            return signal.status === cond.value;
          }
          return false;
        });

        if (isMatch) {
          matchedRule = rule;
          break;
        }
      }
      if (matchedRule) break;
    }

    // 3. Fallback default behavior if no rules matched but we have bad signal state
    if (!matchedRule) {
      if (highestRisk === 'critical') {
        return {
          decision: 'deny' as RiskDecision,
          riskLevel: 'critical' as RiskLevel,
          eligibleMethods: [] as string[],
          fallbackMethod: 'auth_email_otp',
          ruleName: 'Default System Critical Fallback Isolation'
        };
      } else if (highestRisk === 'high') {
        return {
          decision: 'step-up' as RiskDecision,
          riskLevel: 'high' as RiskLevel,
          eligibleMethods: ['auth_passkey', 'auth_hardware_key'] as string[],
          fallbackMethod: 'auth_email_otp',
          ruleName: 'Default System High-Assurance Step-up Forced'
        };
      } else if (highestRisk === 'medium') {
        return {
          decision: 'step-up' as RiskDecision,
          riskLevel: 'medium' as RiskLevel,
          eligibleMethods: ['auth_passkey', 'auth_app_push', 'auth_totp'] as string[],
          fallbackMethod: 'auth_email_otp',
          ruleName: 'Default System Moderate Step-up Forced'
        };
      }

      // Safe Normal state
      return {
        decision: 'continue' as RiskDecision,
        riskLevel: 'low' as RiskLevel,
        eligibleMethods: [] as string[],
        fallbackMethod: 'auth_email_otp',
        ruleName: 'Standard Authentication Policy (Safe Bypass)'
      };
    }

    return {
      decision: matchedRule.outcome,
      riskLevel: matchedRule.riskLevel,
      eligibleMethods: matchedRule.eligibleMethods,
      fallbackMethod: matchedRule.fallbackMethod,
      ruleName: matchedRule.name
    };
  }, [activeSignals, policyRules]);

  // Handler: Selecting a Simulation Scenario Preset
  const handleSelectScenario = (scenario: SimulationScenario) => {
    setActiveScenarioId(scenario.id);
    
    // Map signal statuses from scenario
    const updatedSignals = activeSignals.map(sig => {
      const scenOverride = scenario.signals[sig.id];
      if (scenOverride) {
        return {
          ...sig,
          status: scenOverride.status,
          value: scenOverride.value,
          confidence: scenOverride.confidence,
          freshness: 'Just updated'
        };
      }
      return sig;
    });

    setActiveSignals(updatedSignals);
    setIsEvaluating(true); // Automatically run evaluation loading effect
  };

  // Handler: Tweaking individual signal status manual overrides
  const handleUpdateSignalStatus = (signalId: string, status: SignalStatus, customValue?: string) => {
    setActiveScenarioId('custom');
    
    const updated = activeSignals.map(sig => {
      if (sig.id === signalId) {
        return {
          ...sig,
          status,
          value: customValue || sig.value,
          freshness: '1s ago'
        };
      }
      return sig;
    });

    setActiveSignals(updated);
  };

  // Handler: Revoking user active sessions (P1)
  const handleRevokeSession = (sessionId: string) => {
    const sessionToRevoke = activeSessions.find(s => s.id === sessionId);
    setActiveSessions(activeSessions.filter(s => s.id !== sessionId));
    
    // Add audit log
    if (sessionToRevoke) {
      const newAudit: AuditLog = {
        id: 'aud_' + Math.random().toString(36).substring(2, 8),
        timestamp: new Date().toISOString(),
        trackingId: 'REV-SESS-' + Math.random().toString(36).substring(2, 6).toUpperCase(),
        subject: 'jick.68.0@gmail.com',
        action: `Enforced Session Revoked: ${sessionToRevoke.device}`,
        policyVersion: 'RBA-v1.4.2',
        signalClasses: sessionToRevoke.signalsVerified.map(s => s.replace('sig_', '')),
        decision: 'continue',
        achievedMethods: [],
        redactedEvidence: `Manual administrative override: cookie invalidated. Location context was ${sessionToRevoke.location}`,
        freshnessMet: true,
        tenantId: 'tenant-demo-default'
      };
      setAuditLogs([newAudit, ...auditLogs]);
    }
  };

  // Handler: Report Unfamiliar Activity and Revoke/Lockout (P1)
  const handleReportUnfamiliarActivity = (sessionId: string) => {
    const session = activeSessions.find(s => s.id === sessionId);
    if (!session) return;

    // Immediately isolate
    setActiveSessions(activeSessions.filter(s => s.id !== sessionId));

    // Force strict deny on next action by setting impossible travel to compromised
    const updatedSignals = activeSignals.map(sig => {
      if (sig.id === 'sig_impossible_travel') {
        return {
          ...sig,
          status: 'compromised' as SignalStatus,
          value: 'ATTACK REPORTED: Threat-vector flagged by user session isolation.',
          freshness: 'Now'
        };
      }
      return sig;
    });
    setActiveSignals(updatedSignals);

    // Create critical security audit incident log
    const incidentAudit: AuditLog = {
      id: 'aud_' + Math.random().toString(36).substring(2, 8),
      timestamp: new Date().toISOString(),
      trackingId: 'INC-RAPID-BLOCK',
      subject: 'jick.68.0@gmail.com',
      action: 'USER UNFAMILIAR ACTIVITY THREAT Isolation',
      policyVersion: 'RBA-v1.4.2',
      signalClasses: ['location', 'network', 'device'],
      decision: 'deny',
      achievedMethods: [],
      redactedEvidence: `CRITICAL ATTACK REPORTED BY ACCOUNT OWNER. Invalidated session ${session.id} from IP: ${session.ipAddress}. System locked to deny outcomes.`,
      freshnessMet: true,
      tenantId: 'tenant-demo-default'
    };
    setAuditLogs([incidentAudit, ...auditLogs]);
    setIsEvaluating(true);
  };

  // Helper: Trigger manual re-evaluation sequence
  const handleTriggerEvaluation = () => {
    setIsEvaluating(true);
  };

  // Audit tracker trigger (e.g. from subcomponents to append events)
  const handleTriggerAudit = (action: string, decision: RiskDecision, achieved: string[], evidence: string) => {
    const classes = activeSignals.filter(s => s.status !== 'safe').map(s => s.category);
    const newLog: AuditLog = {
      id: 'aud_' + Math.random().toString(36).substring(2, 8),
      timestamp: new Date().toISOString(),
      trackingId: 'TX-' + Math.floor(1000 + Math.random() * 9000) + '-' + Math.random().toString(36).substring(2, 6).toUpperCase(),
      subject: 'jick.68.0@gmail.com',
      action,
      policyVersion: 'RBA-v1.4.2',
      signalClasses: classes.length > 0 ? classes : ['bypass'],
      decision,
      achievedMethods: achieved,
      redactedEvidence: evidence,
      freshnessMet: true,
      tenantId: 'tenant-demo-default'
    };
    setAuditLogs([newLog, ...auditLogs]);
  };

  const handleClearAuditTrail = () => {
    setAuditLogs([]);
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
      {/* 1. Header with Clock & Context Info */}
      <Header />

      {/* 2. Main Dashboard Container */}
      <main className="flex-1 w-full max-w-7xl mx-auto px-4 md:px-6 py-6 space-y-6">
        
        {/* Banner Informational Notice */}
        <div className="rounded-xl border border-blue-100 bg-blue-50/70 p-4 text-xs text-blue-800 space-y-1 font-sans">
          <p className="font-semibold flex items-center gap-1.5 font-display text-blue-900">
            <Info className="h-4.5 w-4.5 text-blue-600" />
            <span>Risk-Based Authentication (rba) Sandbox Guide</span>
          </p>
          <p className="leading-relaxed text-blue-700">
            To test the full P0 journey, click any <strong>Preset Risk Template</strong> in the Simulator Workbench on the right (e.g. "Impossible Travel Alert"), click <strong>"Inject Context &amp; Start Ceremony"</strong>, and watch the user-facing login card on the left automatically adapt its verification requirements, permitted authenticators, and safe support messages.
          </p>
        </div>

        {/* Cohesive Dual Column Layout */}
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-start">
          
          {/* LEFT PANEL (Lg: 5 columns) - The Release Gate P0 User Ceremony Card */}
          <section className="lg:col-span-5 h-full flex flex-col">
            <div className="mb-3 px-1 flex items-center justify-between">
              <span className="text-xs font-mono font-bold text-slate-500 uppercase tracking-wider block">
                User-Visible Adaptive Journey (P0)
              </span>
              <span className="inline-flex h-2 w-2 rounded-full bg-emerald-500 animate-ping"></span>
            </div>

            <AdaptiveUserCeremony
              activeDecision={computedOutputs.decision}
              riskLevel={computedOutputs.riskLevel}
              activeSignals={activeSignals}
              eligibleMethods={computedOutputs.eligibleMethods}
              fallbackMethod={computedOutputs.fallbackMethod}
              allMethods={AUTHENTICATORS}
              onTriggerAudit={handleTriggerAudit}
              onRefreshEvaluation={handleTriggerEvaluation}
              activeSession={activeSessions[0] || INITIAL_SESSIONS[0]}
              onRevokeSession={handleRevokeSession}
              onReportUnfamiliarActivity={handleReportUnfamiliarActivity}
              isEvaluating={isEvaluating}
              setIsEvaluating={setIsEvaluating}
            />
          </section>

          {/* RIGHT PANEL (Lg: 7 columns) - Admin & Ops Workbenches */}
          <section className="lg:col-span-7 space-y-6">
            
            {/* Navigational Tabs for Admin/Ops */}
            <div className="flex border-b border-slate-200 bg-white rounded-xl p-1 shadow-xs border">
              <button
                onClick={() => setAdminTab('simulator')}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-lg transition duration-150 ${
                  adminTab === 'simulator' 
                    ? 'bg-slate-900 text-white' 
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Sliders className="h-4 w-4" />
                <span>Simulation Workbench (P2)</span>
              </button>
              
              <button
                onClick={() => setAdminTab('rules')}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-lg transition duration-150 ${
                  adminTab === 'rules' 
                    ? 'bg-slate-900 text-white' 
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Shield className="h-4 w-4" />
                <span>Active Policies Editor (P2)</span>
              </button>
              
              <button
                onClick={() => setAdminTab('audit')}
                className={`flex-1 flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-lg transition duration-150 ${
                  adminTab === 'audit' 
                    ? 'bg-slate-900 text-white' 
                    : 'text-slate-600 hover:text-slate-900 hover:bg-slate-50'
                }`}
              >
                <Database className="h-4 w-4" />
                <span>Security Investigations (P1/P2)</span>
              </button>
            </div>

            {/* Admin/Ops Content Pane */}
            <div className="transition-all duration-200">
              {adminTab === 'simulator' && (
                <PolicySimulatorWorkbench
                  scenarios={SIMULATION_SCENARIOS}
                  activeScenarioId={activeScenarioId}
                  onSelectScenario={handleSelectScenario}
                  signals={activeSignals}
                  onUpdateSignalStatus={handleUpdateSignalStatus}
                  computedDecision={computedOutputs.decision}
                  computedRiskLevel={computedOutputs.riskLevel}
                  matchingRuleName={computedOutputs.ruleName}
                  onTriggerEvaluation={handleTriggerEvaluation}
                />
              )}

              {adminTab === 'rules' && (
                <AdminPolicyEditor
                  policyRules={policyRules}
                  onUpdateRules={setPolicyRules}
                  providerHealth={providerHealth}
                  allMethods={AUTHENTICATORS}
                />
              )}

              {adminTab === 'audit' && (
                <SecurityInvestigationLogs
                  auditLogs={auditLogs}
                  activeSessions={activeSessions}
                  onRevokeSession={handleRevokeSession}
                  onClearAuditTrail={handleClearAuditTrail}
                />
              )}
            </div>

          </section>

        </div>
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-200 bg-white py-6 mt-12 text-center text-xs font-mono text-slate-400">
        <div className="max-w-7xl mx-auto px-4">
          <p>Risk-Based Authentication (rba) • Enforced in Cryptographic Verification Clusters</p>
          <p className="mt-1">ISO 27001 compliant • Redacted telemetry schemas in local memory environment</p>
        </div>
      </footer>
    </div>
  );
}
