import React, { useState } from 'react';
import { mockDecisions } from '../data/mockData';
import { DecisionRecord, TraceFact, TraceStep, DecisionEffect } from '../types';
import { 
  RefreshCw, Play, Settings, AlertCircle, ArrowRight, CheckCircle2, 
  HelpCircle, Sliders, Database, FileText, Sparkles, ShieldAlert, ShieldCheck, 
  Clock, GitCompare, ChevronRight, Info
} from 'lucide-react';

export default function ReplayWorkbench() {
  const [selectedDecision, setSelectedDecision] = useState<DecisionRecord>(mockDecisions[0]);
  const [replayMode, setReplayMode] = useState<'exact' | 'engine' | 'current' | 'counterfactual'>('exact');
  const [purpose, setPurpose] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [progress, setProgress] = useState<string[]>([]);
  const [result, setResult] = useState<any | null>(null);

  // Counterfactual state edits
  const [editedFacts, setEditedFacts] = useState<TraceFact[]>([]);
  const [selectedPolicyVersion, setSelectedPolicyVersion] = useState(selectedDecision.policyVersion);
  const [selectedEngineVersion, setSelectedEngineVersion] = useState(selectedDecision.engineVersion);

  // Handle selecting a new starting decision
  const handleDecisionChange = (decisionId: string) => {
    const dec = mockDecisions.find(d => d.id === decisionId);
    if (dec) {
      setSelectedDecision(dec);
      setEditedFacts(JSON.parse(JSON.stringify(dec.facts)));
      setSelectedPolicyVersion(dec.policyVersion);
      setSelectedEngineVersion(dec.engineVersion);
      setResult(null);
      setProgress([]);
    }
  };

  // Initialize facts if empty
  React.useEffect(() => {
    if (selectedDecision) {
      setEditedFacts(JSON.parse(JSON.stringify(selectedDecision.facts)));
      setSelectedPolicyVersion(selectedDecision.policyVersion);
      setSelectedEngineVersion(selectedDecision.engineVersion);
    }
  }, [selectedDecision]);

  // Handle modifying a fact value for counterfactual testing
  const handleFactValueChange = (factId: string, key: string, val: any) => {
    setEditedFacts(prev => prev.map(f => {
      if (f.id === factId) {
        return {
          ...f,
          value: {
            ...f.value,
            [key]: val
          }
        };
      }
      return f;
    }));
  };

  // Run the simulation
  const handleRunReplay = () => {
    if (!purpose.trim()) {
      alert('Please specify the replay investigation purpose/reason.');
      return;
    }

    setIsRunning(true);
    setProgress([]);
    setResult(null);

    const steps = [
      'Locking execution sandbox...',
      'Retrieving versioned schema & resolving dependencies...',
      'Binding historical request attributes...',
      'Mocking resolver calls to authenticated sources...',
      'Evaluating engine policies...'
    ];

    let delay = 0;
    steps.forEach((step, idx) => {
      delay += idx === 4 ? 600 : 400;
      setTimeout(() => {
        setProgress(p => [...p, step]);
        if (idx === steps.length - 1) {
          // Final evaluation result calculation
          setTimeout(() => {
            calculateReplayResult();
            setIsRunning(false);
          }, 500);
        }
      }, delay);
    });
  };

  const calculateReplayResult = () => {
    // Determine the outcome based on mode and counterfactual changes
    let finalEffect: DecisionEffect = selectedDecision.effect;
    let reason = selectedDecision.reason;
    let mutatedSteps: TraceStep[] = JSON.parse(JSON.stringify(selectedDecision.steps));
    let mutatedObligations = JSON.parse(JSON.stringify(selectedDecision.obligations));
    let hasDrift = false;

    if (replayMode === 'exact') {
      if (!selectedDecision.replayable) {
        finalEffect = 'indeterminate';
        reason = 'Replay failed: Stale facts or missing cached context prevents perfect reproduction.';
      } else {
        finalEffect = selectedDecision.effect;
        reason = `Verified 100% stable: ${selectedDecision.reason}`;
      }
    } else if (replayMode === 'engine') {
      // Simulate engine drift
      if (selectedDecision.id === 'dec_01HQ7K9X8M5V2Z3F4G6H8J9K') { // standard permit
        // Maybe core 2.0 flags warning
        finalEffect = 'permit';
        reason = 'Allowed by Finance Auditor, but engine pdp_core_2.0.0 raised deprecation on legacy RBAC rules.';
        hasDrift = true;
      } else {
        finalEffect = selectedDecision.effect;
        reason = `${selectedDecision.reason} (Evaluated on current pdp_core_2.0.0 engine)`;
      }
    } else if (replayMode === 'current') {
      // Current-state replay (stale evaluation, or expired delegation)
      if (selectedDecision.id === 'dec_01HQ7KC9X2M4V5B6N7M8L9K') { // Alice delegation
        finalEffect = 'deny';
        reason = 'Denied under current state: Alice Manager delegation has expired (expired 2023-10-27).';
        hasDrift = true;
        mutatedSteps[0].outcome = 'failed';
        mutatedSteps[1].outcome = 'skipped';
      } else {
        finalEffect = selectedDecision.effect;
        reason = `Re-evaluated against current state. No drift detected.`;
      }
    } else if (replayMode === 'counterfactual') {
      // Look at edited facts
      if (selectedDecision.id === 'dec_01HQ7KB4X9M2C3V4B5N6M7L') { // Geopolitical deny
        const originRegionFact = editedFacts.find(f => f.type === 'network_origin');
        if (originRegionFact && originRegionFact.value.region === 'us-east-1') {
          finalEffect = 'permit';
          reason = 'Permitted: Geopolitical region modified to us-east-1, bypassing the sovereignty constraint.';
          hasDrift = true;
          mutatedSteps[0].outcome = 'not_matched';
          mutatedSteps[1].outcome = 'matched';
          mutatedSteps[1].durationMs = 3;
        } else {
          finalEffect = 'deny';
          reason = `Denied: Sovereign constraint matches modified region "${originRegionFact?.value.region}".`;
        }
      } else if (selectedDecision.id === 'dec_01HQ7K9X8M5V2Z3F4G6H8J9K') { // Finance standard permit
        const roleFact = editedFacts.find(f => f.type === 'role_assignment');
        if (roleFact && roleFact.value.role !== 'Finance Auditor') {
          finalEffect = 'deny';
          reason = `Denied: Subject role modified to "${roleFact.value.role}", which lacks Finance Auditor clearance.`;
          hasDrift = true;
          mutatedSteps[1].outcome = 'failed';
        }
      } else {
        // Fallback for general counterfactual
        hasDrift = true;
        finalEffect = 'deny';
        reason = 'Counterfactual scenario matches edited state. Access denied under default fallback.';
      }
    }

    setResult({
      effect: finalEffect,
      reason,
      hasDrift,
      steps: mutatedSteps,
      obligations: mutatedObligations,
      policyVersion: selectedPolicyVersion,
      engineVersion: selectedEngineVersion,
      simulatedFacts: editedFacts,
      timestamp: new Date().toISOString()
    });
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto h-full overflow-y-auto bg-slate-50">
      <div>
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Replay Workbench</h1>
        <p className="text-slate-500 mt-1">Simulate, trace, and debug authorization decisions under isolated configurations</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left Hand Panel: Config */}
        <div className="lg:col-span-1 space-y-6">
          <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
            <h2 className="text-md font-semibold text-slate-900 border-b pb-3 flex items-center">
              <Settings className="w-4 h-4 mr-2 text-indigo-500" />
              Replay Configuration
            </h2>

            {/* Step 1: Select Starting Decision */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Source Decision Event</label>
              <select 
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                value={selectedDecision.id}
                onChange={(e) => handleDecisionChange(e.target.value)}
              >
                {mockDecisions.map(d => (
                  <option key={d.id} value={d.id}>
                    {d.subject.name} - {d.action.toUpperCase()} {d.resource.name} ({d.id.substring(0, 8)}...)
                  </option>
                ))}
              </select>
              <div className="bg-slate-50 p-3 rounded-lg border border-slate-200 text-xs text-slate-500 space-y-1">
                <p><span className="font-medium text-slate-700">Original Effect:</span> <span className={`font-semibold uppercase ${selectedDecision.effect === 'permit' ? 'text-emerald-600' : 'text-rose-600'}`}>{selectedDecision.effect}</span></p>
                <p><span className="font-medium text-slate-700">Policy:</span> {selectedDecision.policyVersion} • <span className="font-medium text-slate-700">Engine:</span> {selectedDecision.engineVersion}</p>
                <p><span className="font-medium text-slate-700">Replayable:</span> {selectedDecision.replayable ? 'Yes (Deterministic)' : 'No (Context missing)'}</p>
              </div>
            </div>

            {/* Step 2: Select Mode */}
            <div className="space-y-3">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">Simulation Mode</label>
              <div className="grid grid-cols-1 gap-2">
                {[
                  { id: 'exact', name: 'Exact Historical Replay', desc: 'Verify reproducibility using frozen request, facts, and policy artifacts.' },
                  { id: 'engine', name: 'Engine Drift Analysis', desc: 'Evaluate historical parameters against the current PDP engine version.' },
                  { id: 'current', name: 'Current-State Re-eval', desc: 'Determine what would happen now using latest fact updates and active rules.' },
                  { id: 'counterfactual', name: 'Counterfactual Sandbox', desc: 'Surgically edit inputs or mock rules to perform isolated "what-if" impact testing.' }
                ].map((mode) => (
                  <button
                    key={mode.id}
                    onClick={() => {
                      setReplayMode(mode.id as any);
                      setResult(null);
                    }}
                    className={`text-left p-3 rounded-lg border transition-all ${
                      replayMode === mode.id 
                        ? 'border-indigo-500 bg-indigo-50/50 ring-1 ring-indigo-500' 
                        : 'border-slate-200 hover:bg-slate-50'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <p className="text-sm font-semibold text-slate-800">{mode.name}</p>
                      <input 
                        type="radio" 
                        checked={replayMode === mode.id} 
                        readOnly 
                        className="h-4 w-4 text-indigo-600 border-slate-300 focus:ring-indigo-500"
                      />
                    </div>
                    <p className="text-xs text-slate-500 mt-1">{mode.desc}</p>
                  </button>
                ))}
              </div>
            </div>

            {/* Purpose & Authorization */}
            <div className="space-y-2">
              <label className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
                Investigation Purpose <span className="text-rose-500">*</span>
              </label>
              <textarea 
                placeholder="E.g., Incident response verification for John Doe, auditing regional sovereignty restrictions..."
                className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500 h-20"
                value={purpose}
                onChange={(e) => setPurpose(e.target.value)}
              />
              <p className="text-[10px] text-slate-400">All replay executions are securely logged to the append-only tamper-evident ledger.</p>
            </div>

            {/* Run Button */}
            <button 
              onClick={handleRunReplay}
              disabled={isRunning}
              className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 text-white font-medium text-sm rounded-lg shadow-sm hover:shadow transition-all disabled:bg-indigo-300 flex items-center justify-center space-x-2"
            >
              {isRunning ? (
                <>
                  <RefreshCw className="w-4 h-4 animate-spin" />
                  <span>Simulating Engine...</span>
                </>
              ) : (
                <>
                  <Play className="w-4 h-4 fill-white" />
                  <span>Run Replay Simulation</span>
                </>
              )}
            </button>
          </div>
        </div>

        {/* Right Hand / Main Content Panel */}
        <div className="lg:col-span-2 space-y-6">
          
          {/* Conditional Counterfactual inputs if Mode is Counterfactual */}
          {replayMode === 'counterfactual' && (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
              <div className="flex justify-between items-center border-b pb-3">
                <h2 className="text-md font-semibold text-slate-900 flex items-center">
                  <Sliders className="w-4 h-4 mr-2 text-indigo-500" />
                  Surgical Input Mocking (Sandbox)
                </h2>
                <span className="text-xs text-indigo-600 bg-indigo-50 font-semibold px-2 py-0.5 rounded border border-indigo-100 uppercase">Interactive</span>
              </div>
              <p className="text-xs text-slate-500">Modify inputs below to alter PDP fact resolution without affecting production tables.</p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                {editedFacts.map(fact => (
                  <div key={fact.id} className="p-4 border border-slate-200 rounded-lg bg-slate-50/50 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs font-bold text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded uppercase">{fact.type}</span>
                      <span className="text-[10px] text-slate-400 font-mono">Source: {fact.source}</span>
                    </div>
                    
                    <div className="space-y-2">
                      {Object.keys(fact.value).map(key => (
                        <div key={key} className="flex flex-col gap-1">
                          <label className="text-[10px] font-bold text-slate-500 uppercase">{key}</label>
                          {key === 'region' ? (
                            <select
                              value={fact.value[key]}
                              onChange={(e) => handleFactValueChange(fact.id, key, e.target.value)}
                              className="px-2 py-1 bg-white border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            >
                              <option value="ap-south-1">ap-south-1 (Sovereignty Constraint)</option>
                              <option value="us-east-1">us-east-1 (Permitted Region)</option>
                              <option value="eu-central-1">eu-central-1 (EU Residency Only)</option>
                            </select>
                          ) : key === 'role' ? (
                            <select
                              value={fact.value[key]}
                              onChange={(e) => handleFactValueChange(fact.id, key, e.target.value)}
                              className="px-2 py-1 bg-white border border-slate-300 rounded text-xs focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            >
                              <option value="Finance Auditor">Finance Auditor (Authorized)</option>
                              <option value="General Intern">General Intern (Denied)</option>
                              <option value="Senior Trader">Senior Trader (Trading Only)</option>
                            </select>
                          ) : (
                            <input 
                              type="text" 
                              value={fact.value[key]}
                              onChange={(e) => handleFactValueChange(fact.id, key, e.target.value)}
                              className="px-2 py-1 bg-white border border-slate-300 rounded text-xs font-mono focus:outline-none focus:ring-1 focus:ring-indigo-500"
                            />
                          )}
                        </div>
                      ))}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Execution Progress / State Terminal */}
          {isRunning && (
            <div className="bg-slate-900 text-slate-300 p-6 rounded-xl border border-slate-800 shadow-xl font-mono text-xs space-y-2">
              <div className="flex justify-between items-center border-b border-slate-800 pb-2 mb-4 text-slate-500">
                <span>REPLAY SESSION RUNNING</span>
                <span className="h-2 w-2 rounded-full bg-indigo-400 animate-ping"></span>
              </div>
              {progress.map((prog, idx) => (
                <p key={idx} className="flex items-center">
                  <span className="text-indigo-400 mr-2">❯</span> {prog}
                </p>
              ))}
              <div className="pt-2 animate-pulse text-indigo-400">Evaluating active rules against target context...</div>
            </div>
          )}

          {/* Replay Results Card */}
          {!isRunning && result && (
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              
              {/* Outcome Header */}
              <div className="flex justify-between items-start border-b pb-4">
                <div>
                  <h3 className="text-md font-semibold text-slate-900">Simulation Complete</h3>
                  <p className="text-xs text-slate-500 mt-0.5">Execution evaluated on isolated worker sandbox</p>
                </div>
                
                {result.hasDrift ? (
                  <span className="bg-amber-50 text-amber-700 border border-amber-200 text-xs font-bold px-3 py-1 rounded-full flex items-center">
                    <AlertCircle className="w-3.5 h-3.5 mr-1 text-amber-500" /> Behavioral Drift Detected
                  </span>
                ) : (
                  <span className="bg-emerald-50 text-emerald-700 border border-emerald-200 text-xs font-bold px-3 py-1 rounded-full flex items-center">
                    <CheckCircle2 className="w-3.5 h-3.5 mr-1 text-emerald-500" /> 100% Deterministic Consistency
                  </span>
                )}
              </div>

              {/* Side-by-Side Comparison */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6 bg-slate-50 p-5 rounded-xl border border-slate-200">
                
                {/* Before State */}
                <div className="space-y-4">
                  <p className="text-xs font-bold text-slate-500 uppercase tracking-wider">Historical Decision</p>
                  
                  <div className="bg-white p-4 rounded-lg border border-slate-200 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-slate-500">Effect</span>
                      {selectedDecision.effect === 'permit' ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 uppercase">
                          <ShieldCheck className="w-3 h-3 mr-1" /> Permit
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 uppercase">
                          <ShieldAlert className="w-3 h-3 mr-1" /> Deny
                        </span>
                      )}
                    </div>

                    <div>
                      <p className="text-[10px] text-slate-400 uppercase">Causal Explanation</p>
                      <p className="text-xs text-slate-700 mt-1 font-medium">{selectedDecision.reason}</p>
                    </div>

                    <div>
                      <p className="text-[10px] text-slate-400 uppercase">Active Rule Matching</p>
                      <p className="text-xs font-mono text-slate-600 mt-1">
                        {selectedDecision.steps.find(s => s.outcome === 'matched')?.ruleId || 'No active rules matched'}
                      </p>
                    </div>
                  </div>
                </div>

                {/* After State */}
                <div className="space-y-4">
                  <p className="text-xs font-bold text-indigo-600 uppercase tracking-wider flex items-center">
                    <Sparkles className="w-3 h-3 mr-1 animate-pulse" /> Simulated Replay Result
                  </p>
                  
                  <div className="bg-white p-4 rounded-lg border border-indigo-200 ring-1 ring-indigo-100 space-y-3">
                    <div className="flex justify-between items-center">
                      <span className="text-xs text-slate-500">Effect</span>
                      {result.effect === 'permit' ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-emerald-50 text-emerald-700 border border-emerald-200 uppercase">
                          <ShieldCheck className="w-3 h-3 mr-1" /> Permit
                        </span>
                      ) : result.effect === 'deny' ? (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-rose-50 text-rose-700 border border-rose-200 uppercase">
                          <ShieldAlert className="w-3 h-3 mr-1" /> Deny
                        </span>
                      ) : (
                        <span className="inline-flex items-center px-2 py-0.5 rounded text-xs font-bold bg-amber-50 text-amber-700 border border-amber-200 uppercase">
                          Indeterminate
                        </span>
                      )}
                    </div>

                    <div>
                      <p className="text-[10px] text-indigo-500 font-semibold uppercase">Simulated Causal Explanation</p>
                      <p className="text-xs text-slate-700 mt-1 font-semibold">{result.reason}</p>
                    </div>

                    <div>
                      <p className="text-[10px] text-slate-400 uppercase">Active Rule Matching</p>
                      <p className="text-xs font-mono text-indigo-600 mt-1">
                        {result.steps.find((s: any) => s.outcome === 'matched')?.ruleId || 'No rules matched'}
                      </p>
                    </div>
                  </div>
                </div>

              </div>

              {/* Steps Evaluation comparison */}
              <div className="space-y-3">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">Evaluation Steps Verification</h4>
                <div className="space-y-2">
                  {result.steps.map((step: any, idx: number) => {
                    const originalStep = selectedDecision.steps[idx];
                    const changed = originalStep?.outcome !== step.outcome;
                    return (
                      <div key={step.id} className={`p-3 rounded-lg border text-xs flex justify-between items-center ${changed ? 'bg-amber-50/50 border-amber-200' : 'bg-slate-50/50 border-slate-200'}`}>
                        <div>
                          <p className="font-mono font-medium text-slate-700">{step.ruleId}</p>
                          <p className="text-[10px] text-slate-400 mt-0.5">Evaluator: {step.evaluator} • Original: <span className="font-medium">{originalStep?.outcome || 'N/A'}</span></p>
                        </div>
                        <div className="flex items-center space-x-2">
                          {changed && <span className="text-[10px] text-amber-700 font-bold bg-amber-100 px-1.5 py-0.5 rounded mr-1">Outcome Changed</span>}
                          <span className={`px-2 py-0.5 rounded font-mono font-bold text-[10px] border ${
                            step.outcome === 'matched' ? 'bg-emerald-50 text-emerald-700 border-emerald-200' :
                            step.outcome === 'failed' ? 'bg-rose-50 text-rose-700 border-rose-200' :
                            'bg-slate-100 text-slate-600 border-slate-200'
                          }`}>
                            {step.outcome.toUpperCase()}
                          </span>
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>

            </div>
          )}

          {/* Standard Workbench Explanation Card */}
          {!result && !isRunning && (
            <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-center items-center text-center space-y-4">
              <div className="h-12 w-12 rounded-full bg-indigo-50 flex items-center justify-center text-indigo-600">
                <RefreshCw className="w-6 h-6 animate-pulse" />
              </div>
              <div className="max-w-md">
                <h3 className="text-md font-semibold text-slate-900">Sandbox Worker Ready</h3>
                <p className="text-sm text-slate-500 mt-1">
                  Configure your starting decision and replay mode on the left panel, specify an audit purpose, and execute.
                </p>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-left w-full pt-4">
                <div className="p-4 border border-slate-100 rounded-lg bg-slate-50">
                  <p className="text-xs font-semibold text-slate-800 flex items-center">
                    <Info className="w-3.5 h-3.5 text-indigo-500 mr-1.5" /> Deterministic Verification
                  </p>
                  <p className="text-[11px] text-slate-500 mt-1">Confirm that authorization outcomes remain perfectly reproducible under identical constraints.</p>
                </div>
                <div className="p-4 border border-slate-100 rounded-lg bg-slate-50">
                  <p className="text-xs font-semibold text-slate-800 flex items-center">
                    <Sliders className="w-3.5 h-3.5 text-indigo-500 mr-1.5" /> What-If Sandbox Testing
                  </p>
                  <p className="text-[11px] text-slate-500 mt-1">Alter factors, update roles, change regions, or deploy target policy versions to analyze behavioral change.</p>
                </div>
              </div>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
