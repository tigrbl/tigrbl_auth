import React, { useState } from 'react';
import { mockDecisions } from '../data/mockData';
import { DecisionRecord, DecisionEffect } from '../types';
import { 
  GitCompare, ArrowRight, ShieldCheck, ShieldAlert, AlertTriangle, 
  CheckCircle2, HelpCircle, FileText, Activity, Layers, AlertCircle, Info
} from 'lucide-react';

export default function PolicyComparison() {
  const [selectedDecision, setSelectedDecision] = useState<DecisionRecord>(mockDecisions[0]);
  const [comparisonVersion, setComparisonVersion] = useState('pol_v2.5.0');
  const [isComparing, setIsComparing] = useState(false);
  const [comparisonResult, setComparisonResult] = useState<any | null>(null);

  const handleRunComparison = () => {
    setIsComparing(true);
    setTimeout(() => {
      calculateDrift();
      setIsComparing(false);
    }, 600);
  };

  const calculateDrift = () => {
    // Generate mock comparative results based on the chosen version
    let changedEffect = false;
    let originalEffect = selectedDecision.effect;
    let targetEffect = selectedDecision.effect;
    let addedObligations: string[] = [];
    let removedObligations: string[] = [];
    let changedRules: Array<{ ruleId: string; before: string; after: string }> = [];
    let changedAuthority = '';

    if (comparisonVersion === 'pol_v2.5.0') {
      if (selectedDecision.id === 'dec_01HQ7K9X8M5V2Z3F4G6H8J9K') { // standard read permit
        // v2.5.0 requires higher assurance, meaning standard permit becomes challenge
        targetEffect = 'challenge';
        changedEffect = true;
        changedRules = [
          { ruleId: 'rule_permit_auditor', before: 'matched', after: 'skipped' },
          { ruleId: 'rule_require_mfa_elevation', before: 'not_matched', after: 'matched' }
        ];
        addedObligations = ['Trigger step-up authentication', 'Log MFA prompt'];
        changedAuthority = 'Upgraded from direct Role assignment clearance to conditional multi-factor assurance paths.';
      } else if (selectedDecision.id === 'dec_01HQ7KB4X9M2C3V4B5N6M7L') { // geopolitical deny
        // v2.5.0 relaxes regional constraint if emergency override is active (simulate no changes here)
        targetEffect = 'deny';
        changedRules = [
          { ruleId: 'rule_deny_cross_region_mutation', before: 'matched', after: 'matched' }
        ];
      } else if (selectedDecision.id === 'dec_01HQ7KC9X2M4V5B6N7M8L9K') { // Alice manager delegation
        // v2.5.0 deprecates Alice's delegation grant
        targetEffect = 'deny';
        changedEffect = true;
        changedRules = [
          { ruleId: 'rule_verify_delegation_chain', before: 'matched', after: 'failed' }
        ];
        removedObligations = [];
        changedAuthority = 'Authority path broken: Delegated grant trust chain revoked by system-wide credential purge.';
      } else if (selectedDecision.id === 'dec_01HQ7KD4X8M2C3V4B5N6M7L') { // stale facts deny
        // v2.5.0 enforces automatic recovery/fallback resolver
        targetEffect = 'permit';
        changedEffect = true;
        changedRules = [
          { ruleId: 'rule_require_fresh_clearance', before: 'failed', after: 'matched' }
        ];
        addedObligations = ['Schedule background credentials sync'];
        changedAuthority = 'Authority path recovered: Background sync triggered automatically to renew security clearance.';
      }
    } else if (comparisonVersion === 'pol_v2.3.0') {
      // Older policy version comparison
      if (selectedDecision.id === 'dec_01HQ7KB4X9M2C3V4B5N6M7L') { // geopolitical deny was permit in v2.3
        targetEffect = 'permit';
        changedEffect = true;
        changedRules = [
          { ruleId: 'rule_deny_cross_region_mutation', before: 'matched', after: 'skipped' }
        ];
        changedAuthority = 'Geopolitical sovereignty boundaries were not enforced in pol_v2.3.0.';
      }
    }

    setComparisonResult({
      originalVersion: selectedDecision.policyVersion,
      targetVersion: comparisonVersion,
      originalEffect,
      targetEffect,
      changedEffect,
      addedObligations,
      removedObligations,
      changedRules,
      changedAuthority: changedAuthority || 'No structural authority derivation shifts detected.',
      comparedAt: new Date().toISOString()
    });
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto h-full overflow-y-auto bg-slate-50">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Policy Drift Analysis</h1>
        <p className="text-slate-500 mt-1">Audit decision behavior stability and structural delta between active policy bundles</p>
      </div>

      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4">
          <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 flex-1">
            
            {/* Step 1: Select Decision */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Decision Event To Test</label>
              <select 
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={selectedDecision.id}
                onChange={(e) => {
                  const dec = mockDecisions.find(d => d.id === e.target.value);
                  if (dec) {
                    setSelectedDecision(dec);
                    setComparisonResult(null);
                  }
                }}
              >
                {mockDecisions.map(d => (
                  <option key={d.id} value={d.id}>
                    {d.subject.name} requested {d.action.toUpperCase()} ({d.id.substring(0, 8)}...)
                  </option>
                ))}
              </select>
            </div>

            {/* Step 2: Compare With */}
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Target Policy Version</label>
              <select 
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={comparisonVersion}
                onChange={(e) => {
                  setComparisonVersion(e.target.value);
                  setComparisonResult(null);
                }}
              >
                <option value="pol_v2.5.0">pol_v2.5.0 (Proposed / Next-Gen)</option>
                <option value="pol_v2.4.2">pol_v2.4.2 (Stable Release)</option>
                <option value="pol_v2.3.0">pol_v2.3.0 (Legacy Archive)</option>
              </select>
            </div>

            {/* Run Button */}
            <div className="flex items-end">
              <button
                onClick={handleRunComparison}
                disabled={isComparing}
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded-lg shadow-sm transition-all disabled:bg-indigo-300 flex items-center justify-center space-x-2"
              >
                {isComparing ? (
                  <>
                    <Activity className="w-4 h-4 animate-spin" />
                    <span>Analyzing Delta...</span>
                  </>
                ) : (
                  <>
                    <GitCompare className="w-4 h-4" />
                    <span>Run Policy Comparison</span>
                  </>
                )}
              </button>
            </div>

          </div>
        </div>
      </div>

      {comparisonResult ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Summary / Outcome Drift */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              <h3 className="text-md font-semibold text-slate-900 border-b pb-3 flex items-center">
                <Layers className="w-4 h-4 mr-2 text-indigo-500" />
                Drift Outcome
              </h3>

              <div className="space-y-4">
                <div className="flex flex-col items-center justify-center p-6 bg-slate-50 rounded-xl border border-slate-200 text-center space-y-3">
                  <div className="flex items-center space-x-3">
                    <span className="text-xs text-slate-500 font-mono">{comparisonResult.originalVersion}</span>
                    <ArrowRight className="w-4 h-4 text-slate-400" />
                    <span className="text-xs font-bold text-indigo-600 font-mono">{comparisonResult.targetVersion}</span>
                  </div>

                  {comparisonResult.changedEffect ? (
                    <div className="space-y-2">
                      <div className="inline-flex items-center text-amber-700 bg-amber-50 border border-amber-200 px-3 py-1 rounded-full text-xs font-bold">
                        <AlertTriangle className="w-4 h-4 mr-1.5" /> Effect Changed
                      </div>
                      <p className="text-sm font-semibold text-slate-700 mt-2">
                        Evaluation drifted from <span className="uppercase font-bold text-slate-950">{comparisonResult.originalEffect}</span> to{' '}
                        <span className={`uppercase font-bold ${comparisonResult.targetEffect === 'permit' ? 'text-emerald-600' : comparisonResult.targetEffect === 'deny' ? 'text-rose-600' : 'text-amber-600'}`}>
                          {comparisonResult.targetEffect}
                        </span>
                      </p>
                    </div>
                  ) : (
                    <div className="space-y-1">
                      <div className="inline-flex items-center text-emerald-700 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-full text-xs font-bold">
                        <CheckCircle2 className="w-4 h-4 mr-1.5" /> Stability Confirmed
                      </div>
                      <p className="text-xs text-slate-500 mt-2">
                        No outcome drift detected. Effect remains <span className="uppercase font-bold text-slate-800">{comparisonResult.originalEffect}</span>.
                      </p>
                    </div>
                  )}
                </div>

                <div className="space-y-2">
                  <p className="text-xs font-bold text-slate-400 uppercase">Authority Transition</p>
                  <div className="bg-indigo-50/50 p-4 rounded-lg border border-indigo-100 text-xs text-slate-700 leading-relaxed flex items-start">
                    <Info className="w-4 h-4 text-indigo-500 mr-2 shrink-0 mt-0.5" />
                    <p>{comparisonResult.changedAuthority}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Rules and Obligations Deltas */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              
              {/* Rules Evaluation Drift */}
              <div className="space-y-3">
                <h3 className="text-md font-semibold text-slate-900 flex items-center">
                  <Activity className="w-4 h-4 mr-2 text-indigo-500" />
                  Rule Matching Drift
                </h3>
                <p className="text-xs text-slate-500">Evaluates how individual rules participated or skipped compared to the baseline run.</p>

                {comparisonResult.changedRules.length > 0 ? (
                  <div className="space-y-2">
                    {comparisonResult.changedRules.map((rule: any, idx: number) => (
                      <div key={idx} className="p-3 border border-slate-200 bg-slate-50 rounded-lg flex justify-between items-center text-xs font-mono">
                        <div>
                          <p className="font-semibold text-slate-800">{rule.ruleId}</p>
                          <p className="text-[10px] text-slate-400 mt-0.5">Rule evaluated under comparison sandbox</p>
                        </div>
                        <div className="flex items-center space-x-2">
                          <span className="text-slate-400">{rule.before}</span>
                          <ArrowRight className="w-3 h-3 text-slate-400" />
                          <span className="text-indigo-600 font-bold bg-indigo-50 border border-indigo-100 px-1.5 py-0.5 rounded">{rule.after}</span>
                        </div>
                      </div>
                    ))}
                  </div>
                ) : (
                  <div className="p-4 bg-slate-50 border border-slate-200 rounded-lg text-xs text-slate-500 italic">
                    All matching rules executed identically between baseline and target versions.
                  </div>
                )}
              </div>

              {/* Obligations Drift */}
              <div className="space-y-4 pt-4 border-t border-slate-100">
                <h3 className="text-md font-semibold text-slate-900 flex items-center">
                  <FileText className="w-4 h-4 mr-2 text-indigo-500" />
                  Obligation Deltas
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
                  
                  {/* Added Obligations */}
                  <div className="border border-slate-200 rounded-lg p-4 space-y-2">
                    <p className="font-bold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded inline-block uppercase text-[10px]">Added Obligations</p>
                    {comparisonResult.addedObligations.length > 0 ? (
                      <ul className="list-disc pl-4 space-y-1.5 text-slate-600 pt-1">
                        {comparisonResult.addedObligations.map((obl: string, idx: number) => (
                          <li key={idx}>{obl}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-slate-400 italic pt-1">No obligations added.</p>
                    )}
                  </div>

                  {/* Removed Obligations */}
                  <div className="border border-slate-200 rounded-lg p-4 space-y-2">
                    <p className="font-bold text-rose-700 bg-rose-50 px-2.5 py-1 rounded inline-block uppercase text-[10px]">Removed Obligations</p>
                    {comparisonResult.removedObligations.length > 0 ? (
                      <ul className="list-disc pl-4 space-y-1.5 text-slate-600 pt-1">
                        {comparisonResult.removedObligations.map((obl: string, idx: number) => (
                          <li key={idx}>{obl}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-slate-400 italic pt-1">No obligations removed.</p>
                    )}
                  </div>

                </div>
              </div>

            </div>
          </div>

        </div>
      ) : (
        <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-center items-center text-center space-y-4">
          <div className="h-12 w-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600">
            <GitCompare className="w-6 h-6 animate-pulse" />
          </div>
          <div className="max-w-md">
            <h3 className="text-md font-semibold text-slate-900">Drift Analyzer Ready</h3>
            <p className="text-sm text-slate-500 mt-1">
              Select any decision event, select a prospective target policy bundle to compare, and run the sandbox comparison engine.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
