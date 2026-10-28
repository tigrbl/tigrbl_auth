import { MOCK_JWKS } from '../lib/data';
import { KeyRound, ShieldAlert, Fingerprint } from 'lucide-react';
import { motion } from 'motion/react';

export function JWKSExplorer() {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-5xl">
       <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-900">JWKS Explorer</h2>
        <span className="px-3 py-1 bg-slate-100 text-slate-600 text-sm font-medium rounded-full border border-slate-200">
          Global Keys
        </span>
      </div>

      <div className="bg-indigo-50 border border-indigo-100 rounded-xl p-4 mb-6 flex gap-3">
        <ShieldAlert className="w-5 h-5 text-indigo-500 flex-shrink-0" />
        <div className="text-sm text-indigo-900">
          <p className="font-semibold mb-1">Public Key Material Only</p>
          <p className="opacity-80">
            This explorer only parses and displays public components (`n`, `e`, etc.). It strictly enforces a fail-closed policy against parsing or rendering private key parameters (`d`, `p`, `q`, etc.) even if maliciously included in an upstream response.
          </p>
        </div>
      </div>

      <div className="space-y-4">
        {MOCK_JWKS.keys.map((key, idx) => (
          <div key={key.kid} className="bg-white border border-slate-200 rounded-xl overflow-hidden shadow-sm">
            <div className="bg-slate-50 border-b border-slate-200 p-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`p-2 rounded-lg ${idx === 0 ? 'bg-emerald-100 text-emerald-600' : 'bg-slate-200 text-slate-500'}`}>
                  <KeyRound className="w-5 h-5" />
                </div>
                <div>
                  <h3 className="font-mono text-sm font-bold text-slate-800">{key.kid}</h3>
                  <p className="text-xs text-slate-500">Key ID (kid)</p>
                </div>
              </div>
              {idx === 0 ? (
                <span className="px-2.5 py-1 bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold rounded-md">Primary</span>
              ) : (
                <span className="px-2.5 py-1 bg-slate-100 border border-slate-200 text-slate-600 text-xs font-semibold rounded-md">Rollover / Inactive</span>
              )}
            </div>
            
            <div className="p-5 grid grid-cols-2 md:grid-cols-4 gap-6">
              <div>
                <p className="text-xs text-slate-500 mb-1">Key Type (kty)</p>
                <p className="font-mono text-sm text-slate-900">{key.kty}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Algorithm (alg)</p>
                <p className="font-mono text-sm text-slate-900">{key.alg}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Use (use)</p>
                <p className="font-mono text-sm text-slate-900">{key.use === 'sig' ? 'Signature' : key.use}</p>
              </div>
              <div>
                <p className="text-xs text-slate-500 mb-1">Safe Fingerprint</p>
                <div className="flex items-center gap-1.5 font-mono text-xs text-slate-600 bg-slate-50 px-2 py-1 rounded">
                  <Fingerprint className="w-3 h-3 text-slate-400" />
                  {key.kid.substring(0, 8)}...
                </div>
              </div>
            </div>
            
            <div className="p-4 border-t border-slate-100 bg-slate-50/50">
               <p className="text-xs text-slate-500 mb-2">Modulus Summary (n)</p>
               <p className="font-mono text-xs text-slate-400 break-all bg-white border border-slate-200 p-2 rounded">
                 {key.n?.substring(0, 30)}...[TRUNCATED FOR DISPLAY]
               </p>
            </div>
          </div>
        ))}
      </div>
    </motion.div>
  );
}
