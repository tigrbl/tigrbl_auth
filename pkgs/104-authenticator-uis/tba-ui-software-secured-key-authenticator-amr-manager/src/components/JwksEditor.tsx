import React, { useState } from 'react';
import { Code, Plus, Trash2, Key, HelpCircle, AlertCircle } from 'lucide-react';

interface JwksEditorProps {
  initialKeys: any[];
  onAddKey: (jwk: any) => void;
  onRemoveKey: (kid: string) => void;
}

export default function JwksEditor({
  initialKeys,
  onAddKey,
  onRemoveKey
}: JwksEditorProps) {
  const [customJwkJson, setCustomJwkJson] = useState('');
  const [errorMsg, setErrorMsg] = useState<string | null>(null);

  const handleGenerateAndAdd = () => {
    const kid = `swk-generated-${Math.floor(Math.random() * 90000 + 10000)}`;
    const randomKeyObj = {
      kty: "EC",
      use: "sig",
      alg: "ES256",
      crv: "P-256",
      x: Math.random().toString(36).substring(2, 20) + Math.random().toString(36).substring(2, 10),
      y: Math.random().toString(36).substring(2, 20) + Math.random().toString(36).substring(2, 10),
      kid: kid
    };
    onAddKey(randomKeyObj);
    setErrorMsg(null);
  };

  const handleManualSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMsg(null);
    try {
      const parsed = JSON.parse(customJwkJson);
      if (!parsed.kid) {
        parsed.kid = `swk-custom-${Math.floor(Math.random() * 90000)}`;
      }
      if (!parsed.kty) {
        throw new Error('JWK is missing "kty" key type property.');
      }
      onAddKey(parsed);
      setCustomJwkJson('');
    } catch (err: any) {
      setErrorMsg(err?.message || 'Invalid JSON format. Please double-check structure.');
    }
  };

  return (
    <div id="jwks-editor" className="bg-slate-950/40 border border-slate-800 rounded-2xl p-5 space-y-5">
      <div className="border-b border-slate-800 pb-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Code className="w-5 h-5 text-indigo-400" />
          <h3 className="font-bold text-slate-100 text-sm">Server-Side JWKS Public Registry</h3>
        </div>
        <span className="px-2 py-0.5 rounded text-[10px] font-mono bg-indigo-950 text-indigo-400 border border-indigo-900 font-semibold uppercase">
          {initialKeys.length} Registered Keys
        </span>
      </div>

      <p className="text-xs text-slate-400 leading-relaxed">
        The server validates dynamic signature assertions against this live JSON Web Key Set (JWKS). Add custom simulated keys or clean out retired descriptors.
      </p>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Keys Table */}
        <div className="space-y-3">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block">Current Registered JWKs</span>
          
          <div className="space-y-2 max-h-[300px] overflow-y-auto pr-1">
            {initialKeys.length === 0 ? (
              <div className="text-center p-6 border border-dashed border-slate-800 rounded-xl text-xs text-slate-500">
                No active public keys in server registry. Outages expected.
              </div>
            ) : (
              initialKeys.map((key) => {
                const kid = key.kid || 'unknown';
                return (
                  <div key={kid} className="p-3 bg-slate-900/50 border border-slate-850 rounded-xl flex items-center justify-between text-xs font-mono">
                    <div className="space-y-0.5 max-w-[80%]">
                      <div className="flex items-center gap-1.5 font-bold text-slate-300">
                        <Key className="w-3.5 h-3.5 text-slate-500 shrink-0" />
                        <span className="truncate">{kid}</span>
                      </div>
                      <div className="text-[10px] text-slate-500 flex items-center gap-3">
                        <span>kty: {key.kty || 'RSA'}</span>
                        <span>alg: {key.alg || 'RS250'}</span>
                        {key.crv && <span>crv: {key.crv}</span>}
                      </div>
                    </div>
                    <button
                      onClick={() => onRemoveKey(kid)}
                      className="p-1.5 text-slate-500 hover:text-rose-400 hover:bg-rose-950/20 rounded-lg transition-colors cursor-pointer shrink-0"
                      title="Deregister Key"
                    >
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </div>
                );
              })
            )}
          </div>
        </div>

        {/* Input/Generate Form */}
        <div className="space-y-3.5 bg-slate-900/30 p-4 rounded-xl border border-slate-800">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wide block">Inject Simulated Public Material</span>

          <form onSubmit={handleManualSubmit} className="space-y-3">
            <div className="space-y-1">
              <label className="text-[10px] text-slate-400 font-mono">JWK JSON BLOCK</label>
              <textarea
                value={customJwkJson}
                onChange={(e) => setCustomJwkJson(e.target.value)}
                placeholder='{ "kty": "EC", "alg": "ES256", "crv": "P-256", "x": "...", "y": "..." }'
                className="w-full h-[100px] text-xs font-mono border border-slate-800 bg-slate-950 rounded-lg p-2.5 text-slate-200 outline-none focus:ring-1 focus:ring-indigo-500"
              />
            </div>

            {errorMsg && (
              <div className="flex gap-1.5 text-[11px] text-rose-400 items-start leading-normal bg-rose-950/25 border border-rose-900/55 p-2 rounded">
                <AlertCircle className="w-3.5 h-3.5 shrink-0 mt-0.5" />
                <span>{errorMsg}</span>
              </div>
            )}

            <div className="flex gap-2">
              <button
                type="button"
                onClick={handleGenerateAndAdd}
                className="flex-1 text-center bg-slate-800 hover:bg-slate-750 border border-slate-700 text-slate-300 py-1.5 rounded-lg text-xs font-bold transition-colors cursor-pointer"
              >
                Auto-Generate Key
              </button>
              <button
                type="submit"
                className="flex-1 text-center bg-indigo-600 hover:bg-indigo-700 text-white py-1.5 rounded-lg text-xs font-bold transition-colors flex items-center justify-center gap-1 cursor-pointer"
              >
                <Plus className="w-3.5 h-3.5" /> Import Key
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
}
