import { MOCK_METADATA, API_BASE } from '../lib/data';
import { Server, ShieldCheck, Globe, Clock, CheckCircle } from 'lucide-react';
import { motion } from 'motion/react';

export function Overview() {
  return (
    <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} className="max-w-4xl">
      <h2 className="text-2xl font-bold text-slate-900 mb-6">Overview & Health</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Target API</h3>
            <Server className="w-5 h-5 text-indigo-500" />
          </div>
          <div className="space-y-3">
            <div>
              <p className="text-xs text-slate-500 mb-1">Base URL</p>
              <p className="font-mono text-sm text-slate-800 break-all">{API_BASE}</p>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-1">Environment</p>
              <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-emerald-100 text-emerald-700">
                Production-Simulated
              </span>
            </div>
            <div>
              <p className="text-xs text-slate-500 mb-1">Profile</p>
              <p className="text-sm text-slate-800">tigrbl-authz-v2</p>
            </div>
          </div>
        </div>

        <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider">Capabilities</h3>
            <ShieldCheck className="w-5 h-5 text-indigo-500" />
          </div>
          <ul className="space-y-3">
            <li className="flex items-start gap-2 text-sm text-slate-700">
              <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5" />
              <span>Static Metadata Discovery</span>
            </li>
            <li className="flex items-start gap-2 text-sm text-slate-700">
              <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5" />
              <span>JWKS Fingerprinting</span>
            </li>
            <li className="flex items-start gap-2 text-sm text-slate-700">
              <CheckCircle className="w-4 h-4 text-emerald-500 mt-0.5" />
              <span>Local Deterministic Validation</span>
            </li>
            <li className="flex items-start gap-2 text-sm text-slate-400">
              <CheckCircle className="w-4 h-4 text-slate-300 mt-0.5" />
              <span>Authorized Introspection (Auth Required)</span>
            </li>
          </ul>
        </div>
      </div>

      <div className="bg-white border border-slate-200 rounded-xl p-6 shadow-sm">
        <h3 className="text-lg font-medium text-slate-900 mb-4 flex items-center gap-2">
          <Globe className="w-5 h-5 text-slate-400" />
          Reachability Status
        </h3>
        <div className="overflow-x-auto">
          <table className="w-full text-sm text-left">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500">
                <th className="py-3 font-medium">Endpoint</th>
                <th className="py-3 font-medium">Status</th>
                <th className="py-3 font-medium">Last Refresh</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr>
                <td className="py-3 font-mono text-xs text-slate-600">/.well-known/openid-configuration</td>
                <td className="py-3">
                  <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    Reachable
                  </span>
                </td>
                <td className="py-3 text-slate-500 flex items-center gap-1"><Clock className="w-3 h-3"/> Just now</td>
              </tr>
              <tr>
                <td className="py-3 font-mono text-xs text-slate-600">/.well-known/oauth-protected-resource</td>
                <td className="py-3">
                  <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    Reachable
                  </span>
                </td>
                <td className="py-3 text-slate-500 flex items-center gap-1"><Clock className="w-3 h-3"/> Just now</td>
              </tr>
              <tr>
                <td className="py-3 font-mono text-xs text-slate-600">/.well-known/jwks.json</td>
                <td className="py-3">
                  <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs font-medium bg-emerald-50 text-emerald-700 border border-emerald-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                    Reachable
                  </span>
                </td>
                <td className="py-3 text-slate-500 flex items-center gap-1"><Clock className="w-3 h-3"/> Just now</td>
              </tr>
              <tr>
                <td className="py-3 font-mono text-xs text-slate-600">/introspect</td>
                <td className="py-3">
                  <span className="inline-flex items-center gap-1.5 px-2 py-1 rounded-md text-xs font-medium bg-amber-50 text-amber-700 border border-amber-200">
                    <span className="w-1.5 h-1.5 rounded-full bg-amber-500" />
                    Auth Required
                  </span>
                </td>
                <td className="py-3 text-slate-400">-</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </motion.div>
  );
}
