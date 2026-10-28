import React, { useState } from 'react';
import { DecisionRecord } from '../types';
import { 
  ArrowLeft, ShieldCheck, ShieldAlert, GitMerge, FileText, Lock, 
  Activity, CheckCircle2, AlertTriangle, Clock, Server, Eye, 
  SearchCode, EyeOff, UserCheck, Check, HelpCircle
} from 'lucide-react';
import LineageGraph from './LineageGraph';

export default function DecisionDetail({ decision, onBack }: { decision: DecisionRecord, onBack: () => void }) {
  const [activeTab, setActiveTab] = useState<'overview' | 'lineage' | 'facts' | 'policy' | 'enforcement'>('overview');
  const [roleProjection, setRoleProjection] = useState<'analyst' | 'auditor'>('analyst');

  const isPermit = decision.effect === 'permit';
  const EffectIcon = isPermit ? ShieldCheck : ShieldAlert;

  // Redaction helper for Auditor Projection mode
  const redact = (value: string, isSubject = false) => {
    if (roleProjection === 'analyst') return value;
    if (isSubject) {
      return value.split(' ').map(w => w[0] + '*'.repeat(Math.max(1, w.length - 1))).join(' ') + ' (Redacted)';
    }
    return value.substring(0, 3) + '********';
  };

  const redactValue = (value: any) => {
    if (roleProjection === 'analyst') return JSON.stringify(value);
    const str = JSON.stringify(value);
    return str.substring(0, Math.min(10, str.length)) + '... [REDACTED_AUDIT_SIG]';
  };

  // 5-Stage Decision Outcome status calculation
  const getStageStatus = (stage: 'issued' | 'delivered' | 'enforced' | 'obligations' | 'succeeded') => {
    switch (stage) {
      case 'issued':
        return { status: 'success', label: 'Decision Issued', details: `PDP Engine ${decision.engineVersion}` };
      case 'delivered':
        return { status: 'success', label: 'Decision Delivered', details: `Secure trace sealed with ${decision.integritySeal.toUpperCase()} key` };
      case 'enforced':
        if (!decision.enforcement) return { status: 'missing', label: 'Enforcement Pending', details: 'No PEP receipt received' };
        return decision.enforcement.status === 'enforced' 
          ? { status: 'success', label: 'Decision Enforced', details: `Enforced by ${decision.enforcement.pepId}` }
          : { status: 'mismatch', label: 'Enforcement Mismatch', details: 'PEP reported failure/mismatch' };
      case 'obligations':
        if (decision.obligations.length === 0) return { status: 'na', label: 'No Obligations', details: 'No obligations emitted' };
        const allFulfilled = decision.obligations.every(o => o.status === 'fulfilled');
        const anyPending = decision.obligations.some(o => o.status === 'pending');
        if (allFulfilled) return { status: 'success', label: 'Obligations Fulfilled', details: `${decision.obligations.length} action(s) registered` };
        if (anyPending) return { status: 'pending', label: 'Obligations Pending', details: 'Fulfillment confirmation pending' };
        return { status: 'failed', label: 'Obligations Failed', details: 'One or more obligations failed' };
      case 'succeeded':
        const enforcedSuccess = decision.enforcement && decision.enforcement.status === 'enforced';
        const obligationsSuccess = decision.obligations.length === 0 || decision.obligations.every(o => o.status === 'fulfilled');
        if (enforcedSuccess && obligationsSuccess) {
          return { status: 'success', label: 'Operation Succeeded', details: 'Complete end-to-end trace complete' };
        }
        if (!decision.enforcement) {
          return { status: 'warning', label: 'Operation Incomplete', details: 'Lacks end-to-end enforcement receipts' };
        }
        return { status: 'failed', label: 'Operation Failed', details: 'Enforcement or obligations failed' };
    }
  };

  // Authority derivation paths for accessible display
  const getAuthorityPath = () => {
    if (decision.id === 'dec_01HQ7K9X8M5V2Z3F4G6H8J9K') {
      return [
        { level: '1. Root Certificate', type: 'Platform Authority', details: 'Corp Trust Framework Root', status: 'verified' },
        { level: '2. Role Binding', type: 'RBAC Assignment', details: 'Finance Auditor assigned to Sarah Connor', status: 'verified' },
        { level: '3. Effective Access', type: 'Rule Match', details: 'rule_permit_auditor allows read on confidential drafts', status: 'verified' }
      ];
    }
    if (decision.id === 'dec_01HQ7KB4X9M2C3V4B5N6M7L') {
      return [
        { level: '1. Ingress Constraint', type: 'Sovereignty / ABAC', details: 'Action forbidden from network_origin ap-south-1', status: 'failed' },
        { level: '2. Admin Override', type: 'RBAC Override', details: 'rule_permit_db_admin was skipped due to sovereignty precedence', status: 'skipped' }
      ];
    }
    if (decision.id === 'dec_01HQ7KC9X2M4V5B6N7M8L9K') {
      return [
        { level: '1. Delegator Assignment', type: 'Direct Grant', details: 'Alice Manager holds customer write clearance', status: 'verified' },
        { level: '2. Delegation Chain', type: 'Trust Registry Delegation', details: 'Delegation to CRM Sync Bot verified matching scope constraints', status: 'verified' },
        { level: '3. Dynamic Resolution', type: 'Least Authority Path', details: 'Write access allowed via delegated attenuation path', status: 'verified' }
      ];
    }
    // Default
    return [
      { level: '1. Baseline Constraint', type: 'Identity verification', details: 'Subject credentials authenticated', status: 'verified' },
      { level: '2. Rule Match', type: 'ABAC / RBAC rules', details: decision.reason, status: isPermit ? 'verified' : 'failed' }
    ];
  };

  return (
    <div className="flex flex-col h-full bg-white">
      {/* Header */}
      <div className="p-6 border-b border-slate-200 shrink-0">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-4">
          <button onClick={onBack} className="flex items-center text-sm font-medium text-slate-500 hover:text-indigo-600 transition-colors">
            <ArrowLeft className="w-4 h-4 mr-1" /> Back to Search
          </button>

          {/* Role projection toggles */}
          <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
            <button 
              onClick={() => setRoleProjection('analyst')}
              className={`flex items-center px-3 py-1 rounded-md font-semibold transition-all ${
                roleProjection === 'analyst' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              <Eye className="w-3.5 h-3.5 mr-1.5" /> Security Analyst (Full View)
            </button>
            <button 
              onClick={() => setRoleProjection('auditor')}
              className={`flex items-center px-3 py-1 rounded-md font-semibold transition-all ${
                roleProjection === 'auditor' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-900'
              }`}
            >
              <EyeOff className="w-3.5 h-3.5 mr-1.5" /> Compliance Auditor (Redacted)
            </button>
          </div>
        </div>

        <div className="flex justify-between items-start">
          <div>
            <div className="flex items-center space-x-3 mb-2">
              <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-semibold border ${
                isPermit ? 'bg-emerald-50 text-emerald-700 border-emerald-200' : 'bg-rose-50 text-rose-700 border-rose-200'
              }`}>
                <EffectIcon className="w-4 h-4 mr-1.5" /> {decision.effect.toUpperCase()}
              </span>
              <span className="text-slate-400 font-mono text-sm">ID: {decision.id}</span>
              {decision.integritySeal === 'valid' && (
                <span className="inline-flex items-center text-xs text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded border border-indigo-100">
                  <Lock className="w-3 h-3 mr-1" /> Sealed
                </span>
              )}
            </div>
            <h1 className="text-xl font-semibold text-slate-900 mt-2">
              <span className="text-slate-500 font-normal">Subject </span>
              {redact(decision.subject.name, true)}
              <span className="text-slate-500 font-normal mx-2">requested to</span>
              <span className="bg-slate-100 text-slate-700 px-2 py-0.5 rounded text-sm mx-1 uppercase border border-slate-200">{decision.action}</span>
              <span className="text-slate-500 font-normal mx-2">on</span>
              {redact(decision.resource.name)}
            </h1>
            <p className="text-slate-600 mt-3 flex items-start bg-slate-50 p-3 rounded-lg border border-slate-100">
              <SearchCode className="w-5 h-5 text-slate-400 mr-2 shrink-0 mt-0.5" />
              <span><span className="font-medium">Causal Reason:</span> {decision.reason}</span>
            </p>
          </div>
          <div className="text-right hidden sm:block">
            <p className="text-sm font-medium text-slate-900 flex items-center justify-end">
              <Clock className="w-4 h-4 text-slate-400 mr-1.5" />
              {new Date(decision.timestamp).toLocaleString()}
            </p>
            <p className="text-xs text-slate-500 mt-1">Tenant: {decision.tenant}</p>
          </div>
        </div>
        
        {/* Tabs */}
        <div className="flex space-x-6 mt-8 border-b border-slate-200">
          <TabButton active={activeTab === 'overview'} onClick={() => setActiveTab('overview')} icon={Eye} label="Overview & Ledger" />
          <TabButton active={activeTab === 'lineage'} onClick={() => setActiveTab('lineage')} icon={GitMerge} label="Lineage Graph & Path" />
          <TabButton active={activeTab === 'facts'} onClick={() => setActiveTab('facts')} icon={FileText} label="Facts & Context" />
          <TabButton active={activeTab === 'policy'} onClick={() => setActiveTab('policy')} icon={Activity} label="Evaluation Steps" />
          <TabButton active={activeTab === 'enforcement'} onClick={() => setActiveTab('enforcement')} icon={Server} label="Enforcement & PEP" />
        </div>
      </div>

      {/* Content Area */}
      <div className="flex-1 overflow-auto bg-slate-50 p-6">
        <div className="max-w-5xl mx-auto space-y-6">
          
          {activeTab === 'overview' && (
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              
              {/* Request Details Info Cards */}
              <div className="lg:col-span-2 space-y-6">
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
                  <InfoCard title="Request Identity Parameters">
                    <DetailRow label="Subject Principal" value={redact(decision.subject.name, true)} subValue={`Type: ${decision.subject.type}`} />
                    {decision.subject.delegatedFrom && (
                      <DetailRow label="Delegated From" value={redact(decision.subject.delegatedFrom, true)} subValue="Verified delegation lineage" alert />
                    )}
                    <DetailRow label="Resource Targeted" value={redact(decision.resource.name)} subValue={`Type: ${decision.resource.type}`} />
                  </InfoCard>
                  
                  <InfoCard title="Execution Metadata">
                    <DetailRow label="Policy Bundle Version" value={decision.policyVersion} />
                    <DetailRow label="Engine Model Version" value={decision.engineVersion} />
                    <DetailRow label="Durable Replay Stability" value={decision.replayable ? "Yes (Deterministic)" : "No (Missing stale artifacts)"} />
                    <DetailRow label="Stable Identity Key" value={decision.decisionKey} isMono />
                  </InfoCard>
                </div>

                {/* Obligations List */}
                <InfoCard title="Obligations & Advice">
                  {decision.obligations.length > 0 ? (
                    <ul className="divide-y divide-slate-100">
                      {decision.obligations.map(obl => (
                        <li key={obl.id} className="py-3 flex justify-between items-center text-xs">
                          <div>
                            <p className="font-bold text-slate-800">{obl.type}</p>
                            <p className="text-slate-500 mt-0.5">{obl.description}</p>
                          </div>
                          <StatusBadge status={obl.status} />
                        </li>
                      ))}
                    </ul>
                  ) : (
                    <p className="text-xs text-slate-400 italic py-2">No active obligations emitted by PDP.</p>
                  )}
                </InfoCard>
              </div>

              {/* 5-Stage Decision Outcome Ledger */}
              <div className="lg:col-span-1">
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-6">
                  <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Causal Lineage Ledger</h3>
                  
                  <div className="relative border-l border-slate-200 pl-4 ml-2 space-y-6">
                    {(['issued', 'delivered', 'enforced', 'obligations', 'succeeded'] as const).map((stage, idx) => {
                      const item = getStageStatus(stage);
                      return (
                        <div key={idx} className="relative">
                          {/* Dot indicator */}
                          <span className={`absolute -left-[21px] top-1 h-3.5 w-3.5 rounded-full border-2 border-white flex items-center justify-center ${
                            item.status === 'success' ? 'bg-emerald-500' :
                            item.status === 'pending' ? 'bg-amber-500' :
                            item.status === 'failed' ? 'bg-rose-500' :
                            item.status === 'warning' ? 'bg-amber-500 animate-pulse' :
                            'bg-slate-300'
                          }`}>
                            {item.status === 'success' && <Check className="w-2 h-2 text-white stroke-[4]" />}
                          </span>
                          
                          <div>
                            <h4 className="text-xs font-bold text-slate-800">{item.label}</h4>
                            <p className="text-[10px] text-slate-500 mt-0.5">{item.details}</p>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </div>
              </div>

            </div>
          )}

          {activeTab === 'lineage' && (
            <div className="space-y-6">
              
              {/* Lineage visual graph */}
              <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm overflow-x-auto">
                <LineageGraph decision={decision} />
              </div>

              {/* Accessible tabular authority path representation */}
              <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
                <div>
                  <h3 className="text-sm font-semibold text-slate-900 tracking-tight">Authority Derivation Timeline</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Step-by-step verification trace linking active privileges back to authenticated root anchors</p>
                </div>

                <div className="border border-slate-200 rounded-lg overflow-hidden">
                  <table className="min-w-full divide-y divide-slate-200 text-xs">
                    <thead className="bg-slate-50">
                      <tr>
                        <th className="px-4 py-2.5 text-left font-bold text-slate-500">Chronological Path</th>
                        <th className="px-4 py-2.5 text-left font-bold text-slate-500">Authority Type</th>
                        <th className="px-4 py-2.5 text-left font-bold text-slate-500">Derivation Context Details</th>
                        <th className="px-4 py-2.5 text-left font-bold text-slate-500">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-100 bg-white">
                      {getAuthorityPath().map((path, idx) => (
                        <tr key={idx}>
                          <td className="px-4 py-3 font-semibold text-slate-700">{path.level}</td>
                          <td className="px-4 py-3 font-mono text-indigo-600">{path.type}</td>
                          <td className="px-4 py-3 text-slate-600">{path.details}</td>
                          <td className="px-4 py-3 whitespace-nowrap">
                            {path.status === 'verified' ? (
                              <span className="text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100">Verified Path</span>
                            ) : path.status === 'failed' ? (
                              <span className="text-[10px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-100">Failed Requirement</span>
                            ) : (
                              <span className="text-[10px] font-bold text-slate-500 bg-slate-50 px-2 py-0.5 rounded border border-slate-100">Skipped/Unused</span>
                            )}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </div>

            </div>
          )}

          {activeTab === 'facts' && (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm overflow-hidden">
              <table className="min-w-full divide-y divide-slate-200">
                <thead className="bg-slate-50">
                  <tr>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Fact Type</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Resolved Snapshot Value</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Source Registry & Version</th>
                    <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Freshness Audit</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-200">
                  {decision.facts.map(fact => (
                    <tr key={fact.id}>
                      <td className="px-6 py-4 whitespace-nowrap text-xs font-bold text-slate-900 uppercase tracking-wider">{fact.type}</td>
                      <td className="px-6 py-4 text-xs font-mono bg-slate-50/50 text-slate-700 border-l border-slate-200">
                        <code>{redactValue(fact.value)}</code>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-xs text-slate-500">
                        {fact.source} <span className="text-[10px] font-semibold bg-slate-100 px-1.5 py-0.5 rounded ml-1 border border-slate-200">{fact.version}</span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {fact.freshness === 'fresh' ? (
                          <span className="inline-flex items-center text-[10px] font-bold text-emerald-700 bg-emerald-50 px-2 py-0.5 rounded border border-emerald-100"><CheckCircle2 className="w-3 h-3 mr-1" /> Fresh Snapshot</span>
                        ) : fact.freshness === 'stale' ? (
                          <span className="inline-flex items-center text-[10px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-100"><AlertTriangle className="w-3 h-3 mr-1" /> Cache Stale</span>
                        ) : (
                          <span className="inline-flex items-center text-[10px] font-bold text-amber-700 bg-amber-50 px-2 py-0.5 rounded border border-amber-100">Unverified / Missing</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}

          {activeTab === 'policy' && (
            <div className="space-y-4">
              {decision.steps.map((step, index) => (
                <div key={step.id} className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="w-8 h-8 rounded-full bg-indigo-50 text-indigo-600 flex items-center justify-center text-xs font-bold mr-4 border border-indigo-100">
                      {index + 1}
                    </div>
                    <div>
                      <h4 className="text-xs font-bold text-slate-900 font-mono tracking-wider">{step.ruleId}</h4>
                      <p className="text-[10px] text-slate-500 mt-1 uppercase tracking-wider">PDP Subsystem: {step.evaluator} • Evaluation Latency: {step.durationMs}ms</p>
                    </div>
                  </div>
                  <div>
                    <StepOutcomeBadge outcome={step.outcome} />
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'enforcement' && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              
              <div className="md:col-span-2">
                <InfoCard title="PEP Enforcement Proof Certificate">
                  {decision.enforcement ? (
                    <div className="space-y-4">
                      <DetailRow label="Enforcement Receipt Hash" value={decision.enforcement.id} isMono />
                      <DetailRow label="Resource Enforcement Node (PEP)" value={decision.enforcement.pepId} isMono />
                      <DetailRow label="Receipt Generation Time" value={new Date(decision.enforcement.timestamp).toLocaleString()} />
                      
                      <div className="mt-4 pt-4 border-t border-slate-100 flex items-center justify-between">
                        <span className="text-xs font-bold text-slate-400 uppercase">Verification Status</span>
                        {decision.enforcement.status === 'enforced' ? (
                          <span className="inline-flex items-center px-3 py-1 rounded-md text-xs font-bold bg-emerald-50 text-emerald-800 border border-emerald-200 uppercase">
                            <CheckCircle2 className="w-4 h-4 mr-1.5 text-emerald-600" /> Authenticated Receipt Matching
                          </span>
                        ) : (
                          <span className="inline-flex items-center px-3 py-1 rounded-md text-xs font-bold bg-amber-50 text-amber-800 border border-amber-200 uppercase animate-pulse">
                            <AlertTriangle className="w-4 h-4 mr-1.5 text-amber-600" /> Enforcement Drift Alert
                          </span>
                        )}
                      </div>
                    </div>
                  ) : (
                    <div className="py-8 text-center text-slate-500 flex flex-col items-center justify-center">
                      <AlertTriangle className="w-10 h-10 mb-2 text-amber-400" />
                      <p className="font-semibold text-slate-800">Lacks Ingested Enforcement Receipt</p>
                      <p className="text-xs mt-1 text-slate-500 max-w-sm">
                        This authorization decision has not been matched with a Policy Enforcement Point receipt. 
                        It remains unproven whether the resource server successfully implemented this instruction.
                      </p>
                    </div>
                  )}
                </InfoCard>
              </div>

              {/* Secure PEP Info */}
              <div className="md:col-span-1">
                <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6 space-y-4">
                  <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider">PEP Verification Guidelines</h3>
                  <p className="text-xs text-slate-600 leading-relaxed">
                    Following NIST SP 800-171, returning a decision to a Policy Enforcement Point (PEP) is not sufficient evidence of access control. 
                    The PEP must log a deterministic receipt back to this provenance server to fully complete the audit trail.
                  </p>
                </div>
              </div>

            </div>
          )}

        </div>
      </div>
    </div>
  );
}

function TabButton({ active, onClick, icon: Icon, label }: any) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center pb-3 text-sm font-semibold border-b-2 transition-colors ${
        active ? 'border-indigo-600 text-indigo-600' : 'border-transparent text-slate-500 hover:text-slate-700 hover:border-slate-300'
      }`}
    >
      <Icon className="w-4 h-4 mr-2" />
      {label}
    </button>
  );
}

function InfoCard({ title, children }: any) {
  return (
    <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-6">
      <h3 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-4 border-b pb-2">{title}</h3>
      <div className="space-y-4">
        {children}
      </div>
    </div>
  );
}

function DetailRow({ label, value, subValue, isMono, alert }: any) {
  return (
    <div>
      <p className="text-[10px] font-bold text-slate-400 uppercase mb-1">{label}</p>
      <p className={`text-sm ${isMono ? 'font-mono text-slate-600 bg-slate-50 p-1 rounded inline-block border border-slate-200' : 'font-medium text-slate-900'} ${alert ? 'text-indigo-700 bg-indigo-50 border border-indigo-100 px-2 py-0.5 rounded' : ''}`}>
        {value}
      </p>
      {subValue && <p className="text-[11px] text-slate-400 mt-0.5">{subValue}</p>}
    </div>
  );
}

function StatusBadge({ status }: { status: string }) {
  if (status === 'fulfilled') return <span className="text-[10px] font-bold bg-emerald-50 text-emerald-800 px-2 py-0.5 border border-emerald-200 rounded-full uppercase">Fulfilled</span>;
  if (status === 'pending') return <span className="text-[10px] font-bold bg-amber-50 text-amber-800 px-2 py-0.5 border border-amber-200 rounded-full uppercase">Pending</span>;
  return <span className="text-[10px] font-bold bg-slate-50 text-slate-800 px-2 py-0.5 border border-slate-200 rounded-full uppercase">{status}</span>;
}

function StepOutcomeBadge({ outcome }: { outcome: string }) {
  if (outcome === 'matched') return <span className="text-xs font-bold bg-emerald-50 text-emerald-800 px-2.5 py-1 rounded border border-emerald-200 uppercase">Matched</span>;
  if (outcome === 'failed') return <span className="text-xs font-bold bg-rose-50 text-rose-800 px-2.5 py-1 rounded border border-rose-200 uppercase">Failed</span>;
  if (outcome === 'short_circuited') return <span className="text-xs font-bold bg-slate-50 text-slate-600 px-2.5 py-1 rounded border border-slate-200 uppercase">Short Circuited</span>;
  return <span className="text-xs font-bold bg-slate-50 text-slate-500 px-2.5 py-1 rounded border border-slate-200 uppercase">{outcome.replace('_', ' ')}</span>;
}
