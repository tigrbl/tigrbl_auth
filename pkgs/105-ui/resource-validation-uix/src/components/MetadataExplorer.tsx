import { MOCK_METADATA } from '../lib/data';
import { Copy, ExternalLink, ShieldAlert } from 'lucide-react';
import { motion } from 'motion/react';

export function MetadataExplorer() {
  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
  };

  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-5xl">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-2xl font-bold text-slate-900">Metadata Explorer</h2>
        <span className="px-3 py-1 bg-slate-100 text-slate-600 text-sm font-medium rounded-full border border-slate-200">
          Static Mode
        </span>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden mb-6">
        <div className="border-b border-slate-200 bg-slate-50 p-4 flex justify-between items-center">
          <div>
            <h3 className="font-semibold text-slate-800">OpenID Configuration</h3>
            <p className="text-xs text-slate-500 mt-0.5">Resolved from /.well-known/openid-configuration</p>
          </div>
          <button 
            onClick={() => copyToClipboard(JSON.stringify(MOCK_METADATA, null, 2))}
            className="p-2 text-slate-400 hover:text-indigo-600 hover:bg-indigo-50 rounded-md transition-colors"
            title="Copy JSON"
          >
            <Copy className="w-4 h-4" />
          </button>
        </div>
        
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-0 divide-y lg:divide-y-0 lg:divide-x divide-slate-200">
          <div className="p-0">
            <div className="p-4 bg-slate-50/50 border-b border-slate-100 text-xs font-semibold text-slate-500 uppercase tracking-wider">
              Human Readable
            </div>
            <div className="p-5 space-y-5">
              <div>
                <span className="text-xs text-slate-500 block mb-1">Issuer (Expected 'iss' claim)</span>
                <span className="font-mono text-sm text-indigo-700 bg-indigo-50 px-2 py-1 rounded break-all">
                  {MOCK_METADATA.issuer}
                </span>
              </div>
              
              <div>
                <span className="text-xs text-slate-500 block mb-1">JWKS URI (Key fetching)</span>
                <div className="flex items-center gap-2">
                  <span className="font-mono text-sm text-slate-800 break-all">{MOCK_METADATA.jwks_uri}</span>
                  <ExternalLink className="w-3 h-3 text-slate-400 flex-shrink-0" />
                </div>
              </div>

              <div>
                <span className="text-xs text-slate-500 block mb-2">Supported Scopes</span>
                <div className="flex flex-wrap gap-2">
                  {MOCK_METADATA.scopes_supported.map(scope => (
                    <span key={scope} className="px-2 py-1 bg-slate-100 text-slate-700 text-xs font-mono rounded border border-slate-200">
                      {scope}
                    </span>
                  ))}
                </div>
              </div>

              <div className="bg-amber-50 border border-amber-200 rounded-lg p-3 flex gap-3">
                <ShieldAlert className="w-5 h-5 text-amber-500 flex-shrink-0" />
                <p className="text-xs text-amber-800 leading-relaxed">
                  This metadata is public and unauthenticated. It represents the claims the authorization server <em>asserts</em> it supports. Your resource server must still independently validate the <code>iss</code> claim against your explicit configuration.
                </p>
              </div>
            </div>
          </div>
          
          <div className="p-0 bg-slate-900">
            <div className="p-4 bg-slate-800 border-b border-slate-700 flex items-center justify-between text-xs font-semibold text-slate-400 uppercase tracking-wider">
              <span>Raw JSON Payload</span>
              <span className="text-emerald-400 lowercase normal-case">HTTP 200 OK</span>
            </div>
            <div className="p-4 overflow-x-auto">
              <pre className="text-xs text-slate-300 font-mono leading-relaxed">
                {JSON.stringify(MOCK_METADATA, null, 2)}
              </pre>
            </div>
          </div>
        </div>
      </div>
    </motion.div>
  );
}
