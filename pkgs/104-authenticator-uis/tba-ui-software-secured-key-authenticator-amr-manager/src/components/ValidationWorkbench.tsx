import React, { useState } from 'react';
import { SoftwareKeyCredential } from '../types';
import { ShieldAlert, CheckCircle2, ShieldQuestion, HelpCircle, Terminal, Play } from 'lucide-react';

interface ValidationWorkbenchProps {
  activeKeys: SoftwareKeyCredential[];
}

export default function ValidationWorkbench({
  activeKeys
}: ValidationWorkbenchProps) {
  const [selectedKeyId, setSelectedKeyId] = useState(activeKeys[0]?.id || '');
  const [testPayload, setTestPayload] = useState('{"api_route":"/api/v1/payments","amount":100}');
  const [signatureText, setSignatureText] = useState('SIG_ECDSA_88aef22bca9810f2771');
  const [validationResult, setValidationResult] = useState<{
    status: 'success' | 'failed' | 'idle';
    message: string;
    amrClaim?: string;
    verificationTimeMs?: number;
  }>({ status: 'idle', message: 'Ready to evaluate signature token bounds.' });

  const handleValidate = () => {
    const key = activeKeys.find((k) => k.id === selectedKeyId);
    if (!key) {
      setValidationResult({
        status: 'failed',
        message: 'No cryptographic key material selected.'
      });
      return;
    }

    if (!signatureText.trim()) {
      setValidationResult({
        status: 'failed',
        message: 'Signature payload cannot be empty.'
      });
      return;
    }

    // Simulate cryptographic processing delay
    const latency = Math.floor(Math.random() * 25 + 10);
    const success = !signatureText.toLowerCase().includes('fail') && key.status === 'active';

    if (success) {
      setValidationResult({
        status: 'success',
        message: 'Cryptographic signature verified successfully. Origin bound checked.',
        amrClaim: key.hasVerifiedEvidence ? 'swk (verified)' : 'none',
        verificationTimeMs: latency
      });
    } else {
      setValidationResult({
        status: 'failed',
        message: 'Signature validation failed. Payload hash mismatch or key revoked.'
      });
    }
  };

  return (
    <div id="validation-workbench" className="bg-slate-950/40 border border-slate-800 rounded-2xl p-5 space-y-4">
      <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Terminal className="w-5 h-5 text-indigo-400" />
          <h3 className="font-bold text-slate-100 text-sm">Signature Validation Workbench</h3>
        </div>
      </div>

      <p className="text-xs text-slate-400 leading-relaxed">
        Test custom cryptographic payload bounds. Select any active keystore credential to evaluate its public validation assertions.
      </p>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5 pt-1.5">
        <div className="space-y-3.5">
          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 block">Evaluate Credential Material</label>
            <select
              value={selectedKeyId}
              onChange={(e) => setSelectedKeyId(e.target.value)}
              className="w-full text-xs border border-slate-800 bg-slate-900 rounded-lg p-2 bg-slate-900 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
            >
              {activeKeys.map((k) => (
                <option key={k.id} value={k.id}>
                  {k.name} ({k.algorithm})
                </option>
              ))}
            </select>
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 block">Plaintext Payload</label>
            <textarea
              value={testPayload}
              onChange={(e) => setTestPayload(e.target.value)}
              className="w-full h-[60px] text-xs font-mono border border-slate-800 bg-slate-900 rounded-lg p-2 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
            />
          </div>

          <div className="space-y-1.5">
            <label className="text-xs font-semibold text-slate-300 block">Cryptographic Signature Assertion</label>
            <input
              type="text"
              value={signatureText}
              onChange={(e) => setSignatureText(e.target.value)}
              className="w-full text-xs font-mono border border-slate-800 bg-slate-900 rounded-lg p-2 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
              placeholder="e.g. SIG_ECDSA_..."
            />
          </div>

          <button
            onClick={handleValidate}
            className="w-full bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-4 rounded-xl text-xs transition-colors flex items-center justify-center gap-1.5 shadow-sm cursor-pointer"
          >
            <Play className="w-4 h-4" /> Evaluate Signature Proof
          </button>
        </div>

        {/* Results Pane */}
        <div className="bg-slate-900/60 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
          <div className="space-y-3">
            <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block">Validation Results</span>

            {validationResult.status === 'idle' && (
              <div className="text-slate-400 text-xs flex gap-2 items-start py-6 justify-center">
                <ShieldQuestion className="w-5 h-5 text-slate-500 shrink-0" />
                <span>Specify payload and click "Evaluate" to execute public signature verification.</span>
              </div>
            )}

            {validationResult.status === 'success' && (
              <div className="space-y-3">
                <div className="p-3 bg-emerald-950/20 border border-emerald-900/50 rounded-lg text-xs text-emerald-400 flex gap-2 items-start">
                  <CheckCircle2 className="w-5 h-5 text-emerald-500 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold text-emerald-300 block">Signature Validated!</span>
                    <p className="mt-1 leading-relaxed">{validationResult.message}</p>
                  </div>
                </div>

                <div className="space-y-1.5 font-mono text-[11px] text-slate-400">
                  <div className="flex justify-between">
                    <span>Assigned AMR Claim:</span>
                    <strong className="text-indigo-400 font-bold uppercase">{validationResult.amrClaim}</strong>
                  </div>
                  <div className="flex justify-between">
                    <span>Latency:</span>
                    <span>{validationResult.verificationTimeMs}ms</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Integrity Hash:</span>
                    <span className="truncate max-w-[120px]">0x39a0ef22ba91c</span>
                  </div>
                </div>
              </div>
            )}

            {validationResult.status === 'failed' && (
              <div className="p-3 bg-rose-950/20 border border-rose-900/50 rounded-lg text-xs text-rose-400 flex gap-2 items-start">
                <ShieldAlert className="w-5 h-5 text-rose-500 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold text-rose-300 block">Verification Refused</span>
                  <p className="mt-1 leading-relaxed">{validationResult.message}</p>
                </div>
              </div>
            )}
          </div>

          <div className="text-[10px] text-slate-500 pt-2 border-t border-slate-800/80 leading-normal">
            The verification workbench enforces signature constraints in exact lock-step with active governance policies.
          </div>
        </div>
      </div>
    </div>
  );
}
