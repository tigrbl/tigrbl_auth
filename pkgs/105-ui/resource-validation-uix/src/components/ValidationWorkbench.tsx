import { useState, useEffect } from 'react';
import { FIXTURES } from '../lib/data';
import { Play, RotateCcw, AlertTriangle, ShieldCheck, XCircle, CheckCircle2 } from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

type StageStatus = 'pending' | 'success' | 'error' | 'skipped' | 'current';

interface Stage {
  id: string;
  name: string;
  description: string;
}

const STAGES: Stage[] = [
  { id: 'input', name: 'Input Recognition', description: 'Parse token format (JWT).' },
  { id: 'metadata', name: 'Issuer Resolution', description: 'Match issuer against configuration.' },
  { id: 'signature', name: 'Signature Validation', description: 'Verify cryptographic signature via JWKS.' },
  { id: 'temporal', name: 'Temporal Validation', description: 'Check exp and nbf claims.' },
  { id: 'audience', name: 'Audience Validation', description: 'Verify aud claim matches intended resource.' },
  { id: 'scope', name: 'Scope Validation', description: 'Check for required permissions/scopes.' },
];

export function ValidationWorkbench() {
  const [tokenInput, setTokenInput] = useState('');
  const [activeFixture, setActiveFixture] = useState<string | null>(null);
  const [isRunning, setIsRunning] = useState(false);
  const [stageResults, setStageResults] = useState<Record<string, { status: StageStatus, message?: string }>>({});
  const [finalResult, setFinalResult] = useState<'allow' | 'deny' | null>(null);

  // Clear token on unmount for security
  useEffect(() => {
    return () => {
      setTokenInput('');
    };
  }, []);

  const runValidation = async (fixtureId?: string) => {
    setIsRunning(true);
    setFinalResult(null);
    setStageResults({});
    setTokenInput(''); // Immediately clear input for security

    const selected = fixtureId || activeFixture || 'custom';
    
    // Simulate multi-stage validation delays
    const newResults: Record<string, { status: StageStatus, message?: string }> = {};
    
    for (const stage of STAGES) {
      newResults[stage.id] = { status: 'current' };
      setStageResults({ ...newResults });
      
      await new Promise(r => setTimeout(r, 400)); // Artificial delay for UIX

      let status: StageStatus = 'success';
      let message = '';

      if (selected === 'malformed' && stage.id === 'input') {
        status = 'error'; message = 'Failed to parse JWT. Invalid header/payload base64.';
      } else if (selected === 'wrong-issuer' && stage.id === 'metadata') {
        status = 'error'; message = 'iss claim "https://evil.auth" does not match configured issuer.';
      } else if (selected === 'invalid-sig' && stage.id === 'signature') {
        status = 'error'; message = 'Signature verification failed. Unknown kid or tampered payload.';
      } else if (selected === 'expired' && stage.id === 'temporal') {
        status = 'error'; message = 'Token expired. "exp" timestamp is in the past.';
      } else if (selected === 'wrong-audience' && stage.id === 'audience') {
        status = 'error'; message = 'Audience mismatch. Expected "api://resource-server-1".';
      } else if (selected === 'missing-scope' && stage.id === 'scope') {
        status = 'error'; message = 'Missing required scope. Found "openid profile". Expected "api:read".';
      }

      newResults[stage.id] = { status, message };
      setStageResults({ ...newResults });

      if (status === 'error') {
        setFinalResult('deny');
        setIsRunning(false);
        return; // Halt validation
      }
    }

    setFinalResult('allow');
    setIsRunning(false);
  };

  const handleReset = () => {
    setTokenInput('');
    setActiveFixture(null);
    setStageResults({});
    setFinalResult(null);
  };

  const renderStageIcon = (status: StageStatus) => {
    switch (status) {
      case 'success': return <CheckCircle2 className="w-5 h-5 text-emerald-500" />;
      case 'error': return <XCircle className="w-5 h-5 text-rose-500" />;
      case 'current': return <div className="w-5 h-5 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin" />;
      case 'skipped': return <div className="w-5 h-5 rounded-full border-2 border-slate-300" />;
      default: return <div className="w-5 h-5 rounded-full border-2 border-slate-200" />;
    }
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-6xl">
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-bold text-slate-900">Validation Workbench</h2>
          <p className="text-slate-500 mt-1">Test token validation deterministically without mutating production state.</p>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-5 space-y-6">
          <div className="bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3">
            <AlertTriangle className="w-5 h-5 text-amber-600 flex-shrink-0" />
            <div>
              <h4 className="text-sm font-semibold text-amber-900 mb-1">Privacy Warning</h4>
              <p className="text-xs text-amber-800 leading-relaxed">
                Tokens pasted here are processed locally or via a safe backend-for-frontend. They are never persisted in history, telemetry, or logs. <strong>Input is immediately cleared upon test execution.</strong>
              </p>
            </div>
          </div>

          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 className="font-semibold text-slate-800 mb-4">Input Selection</h3>
            
            <div className="space-y-4">
               <div>
                 <label className="block text-xs font-medium text-slate-700 mb-2">Deterministic Fixtures</label>
                 <div className="grid grid-cols-2 gap-2">
                   {FIXTURES.map(f => (
                     <button
                       key={f.id}
                       onClick={() => { setActiveFixture(f.id); setTokenInput(''); }}
                       className={`text-left px-3 py-2 text-xs rounded-md border transition-colors ${
                         activeFixture === f.id 
                           ? 'bg-indigo-50 border-indigo-200 text-indigo-700 font-medium' 
                           : 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50 hover:border-slate-300'
                       }`}
                     >
                       {f.name}
                     </button>
                   ))}
                 </div>
               </div>

               <div className="relative">
                 <div className="absolute inset-0 flex items-center" aria-hidden="true">
                   <div className="w-full border-t border-slate-200" />
                 </div>
                 <div className="relative flex justify-center text-xs">
                   <span className="px-2 bg-white text-slate-500">OR</span>
                 </div>
               </div>

               <div>
                 <label className="block text-xs font-medium text-slate-700 mb-2">Paste Bearer Token</label>
                 <textarea
                   value={tokenInput}
                   onChange={(e) => { setTokenInput(e.target.value); setActiveFixture(null); }}
                   placeholder="ey..."
                   className="w-full h-24 font-mono text-xs p-3 border border-slate-300 rounded-md focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 resize-none outline-none"
                 />
               </div>

               <div className="flex gap-3 pt-2">
                 <button
                   disabled={isRunning || (!tokenInput && !activeFixture)}
                   onClick={() => runValidation()}
                   className="flex-1 flex items-center justify-center gap-2 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed text-white px-4 py-2 rounded-md text-sm font-medium transition-colors"
                 >
                   <Play className="w-4 h-4" />
                   Run Validation
                 </button>
                 <button
                   onClick={handleReset}
                   disabled={isRunning}
                   className="px-4 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-md text-sm font-medium transition-colors"
                 >
                   <RotateCcw className="w-4 h-4" />
                 </button>
               </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-7">
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden h-full flex flex-col">
            <div className="bg-slate-50 border-b border-slate-200 p-4">
              <h3 className="font-semibold text-slate-800">Validation Trace</h3>
            </div>
            
            <div className="p-6 flex-1 flex flex-col">
              {Object.keys(stageResults).length === 0 ? (
                <div className="flex-1 flex flex-col items-center justify-center text-slate-400">
                  <ShieldCheck className="w-12 h-12 mb-3 text-slate-300" />
                  <p className="text-sm">Select a fixture or paste a token to begin trace.</p>
                </div>
              ) : (
                <div className="space-y-6">
                  <div className="relative border-l-2 border-slate-100 ml-3 space-y-8">
                    {STAGES.map((stage) => {
                      const result = stageResults[stage.id] || { status: 'pending' };
                      return (
                        <div key={stage.id} className="relative pl-6">
                          <div className="absolute -left-[11px] bg-white">
                            {renderStageIcon(result.status)}
                          </div>
                          <div>
                            <h4 className={`text-sm font-medium ${result.status === 'current' ? 'text-indigo-700' : 'text-slate-800'}`}>
                              {stage.name}
                            </h4>
                            <p className="text-xs text-slate-500 mt-0.5">{stage.description}</p>
                            
                            <AnimatePresence>
                              {result.message && (
                                <motion.div 
                                  initial={{ opacity: 0, height: 0 }} 
                                  animate={{ opacity: 1, height: 'auto' }}
                                  className={`mt-2 p-3 rounded-md text-xs border ${
                                    result.status === 'error' ? 'bg-rose-50 border-rose-100 text-rose-800' : 'bg-slate-50 border-slate-200 text-slate-700'
                                  }`}
                                >
                                  {result.message}
                                </motion.div>
                              )}
                            </AnimatePresence>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {finalResult && (
                    <motion.div 
                      initial={{ opacity: 0, scale: 0.95 }}
                      animate={{ opacity: 1, scale: 1 }}
                      className={`p-4 rounded-xl border flex items-center justify-between ${
                        finalResult === 'allow' 
                          ? 'bg-emerald-50 border-emerald-200 text-emerald-900' 
                          : 'bg-rose-50 border-rose-200 text-rose-900'
                      }`}
                    >
                      <div className="flex items-center gap-3">
                        {finalResult === 'allow' ? <CheckCircle2 className="w-6 h-6 text-emerald-500" /> : <XCircle className="w-6 h-6 text-rose-500" />}
                        <div>
                          <h3 className="font-bold text-base">{finalResult === 'allow' ? 'Access Allowed' : 'Access Denied'}</h3>
                          <p className="text-xs opacity-80 mt-0.5">
                            {finalResult === 'allow' 
                              ? 'All validation stages passed successfully.' 
                              : 'Validation halted due to policy violation.'}
                          </p>
                        </div>
                      </div>
                      <button className="px-3 py-1.5 bg-white border border-black/10 rounded-md text-xs font-medium shadow-sm hover:bg-black/5 transition-colors">
                        Export Safe Summary
                      </button>
                    </motion.div>
                  )}
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
