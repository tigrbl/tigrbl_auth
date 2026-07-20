import { useState } from 'react';
import { MOCK_METADATA } from '../lib/data';
import { Copy, Terminal } from 'lucide-react';
import { motion } from 'motion/react';

export function VerifierConfig() {
  const [audience, setAudience] = useState('api://resource-server-1');
  const [requiredScopes, setRequiredScopes] = useState('api:read');
  const [clockTolerance, setClockTolerance] = useState('30');

  const pythonSnippet = `
from tigrbl_authz_resource_server import Verifier, Config

config = Config(
    issuer="${MOCK_METADATA.issuer}",
    jwks_uri="${MOCK_METADATA.jwks_uri}",
    audience="${audience}",
    clock_skew_tolerance=${clockTolerance},
    required_scopes=[${requiredScopes.split(' ').map(s => `"${s}"`).join(', ')}]
)

verifier = Verifier(config)

@app.middleware("http")
async def auth_middleware(request: Request, call_next):
    token = request.headers.get("Authorization", "").removeprefix("Bearer ")
    try:
        claims = await verifier.verify(token)
        request.state.user = claims
    except verifier.ValidationError as e:
        return JSONResponse({"error": str(e)}, status_code=401)
    
    return await call_next(request)
  `.trim();

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-5xl">
       <div className="mb-6">
        <h2 className="text-2xl font-bold text-slate-900">Verifier Configuration Builder</h2>
        <p className="text-slate-500 mt-1">Generate deterministic configuration for your API Gateway or middleware.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-4 space-y-6">
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
            <h3 className="font-semibold text-slate-800 mb-4 border-b border-slate-100 pb-2">Configuration State</h3>
            
            <div className="space-y-4">
              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Expected Issuer</label>
                <input 
                  type="text" 
                  readOnly 
                  value={MOCK_METADATA.issuer}
                  className="w-full bg-slate-50 border border-slate-200 rounded-md px-3 py-2 text-sm text-slate-500 font-mono cursor-not-allowed"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Expected Audience (aud)</label>
                <input 
                  type="text" 
                  value={audience}
                  onChange={(e) => setAudience(e.target.value)}
                  placeholder="api://my-service"
                  className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Required Scopes (space separated)</label>
                <input 
                  type="text" 
                  value={requiredScopes}
                  onChange={(e) => setRequiredScopes(e.target.value)}
                  className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm text-slate-900 font-mono focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow outline-none"
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-700 mb-1">Clock Tolerance (seconds)</label>
                <input 
                  type="number" 
                  value={clockTolerance}
                  onChange={(e) => setClockTolerance(e.target.value)}
                  className="w-full border border-slate-300 rounded-md px-3 py-2 text-sm text-slate-900 focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 transition-shadow outline-none"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="lg:col-span-8">
          <div className="bg-slate-900 rounded-xl overflow-hidden shadow-sm flex flex-col h-full border border-slate-800">
            <div className="bg-slate-800 p-3 px-4 flex items-center justify-between border-b border-slate-700">
              <div className="flex items-center gap-2 text-slate-300 text-sm font-medium">
                <Terminal className="w-4 h-4" />
                Python Middleware (tigrbl-authz)
              </div>
              <button 
                onClick={() => copyToClipboard(pythonSnippet)}
                className="flex items-center gap-1.5 px-3 py-1.5 bg-slate-700 hover:bg-slate-600 text-slate-200 text-xs rounded transition-colors"
              >
                <Copy className="w-3 h-3" /> Copy
              </button>
            </div>
            <div className="p-4 overflow-x-auto flex-1">
              <pre className="text-slate-300 font-mono text-sm leading-relaxed">
                <code>{pythonSnippet}</code>
              </pre>
            </div>
            <div className="bg-slate-950 p-3 text-xs text-slate-500 border-t border-slate-800">
              Compatible with <code>tigrbl_authz_resource_server &gt;= 2.0.0</code>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
