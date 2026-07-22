import React, { useState } from 'react';
import { SmsPolicy, SmsProvider, SmsLog, AuditLog, Country } from '../types';
import { Shield, Server, FileText, Activity, AlertTriangle, Play, CheckCircle, RefreshCw, XCircle, Globe, Settings, TrendingUp, DollarSign } from 'lucide-react';

interface AdminConsoleProps {
  policy: SmsPolicy;
  setPolicy: (policy: SmsPolicy) => void;
  providers: SmsProvider[];
  setProviders: (providers: SmsProvider[]) => void;
  logs: SmsLog[];
  auditLogs: AuditLog[];
  countries: Country[];
  setCountries: (countries: Country[]) => void;
  onClearLogs: () => void;
}

export const AdminConsole: React.FC<AdminConsoleProps> = ({
  policy,
  setPolicy,
  providers,
  setProviders,
  logs,
  auditLogs,
  countries,
  setCountries,
  onClearLogs
}) => {
  const [activeTab, setActiveTab] = useState<'policy' | 'providers' | 'health' | 'abuse' | 'audit'>('policy');

  // Compute stats
  const totalSent = logs.length;
  const totalDelivered = logs.filter(l => l.state === 'delivered').length;
  const totalFailed = logs.filter(l => l.state === 'failed').length;
  const deliveryRate = totalSent > 0 ? Math.round((totalDelivered / totalSent) * 100) : 100;
  
  const avgLatency = logs.length > 0 
    ? Math.round(logs.reduce((acc, curr) => acc + curr.latencyMs, 0) / logs.length) 
    : 0;

  const totalCost = logs.reduce((acc, curr) => {
    const provider = providers.find(p => p.id === curr.providerId);
    return acc + (provider?.costPerSms || 0.02);
  }, 0);

  const toggleCountry = (code: string) => {
    const updatedCountries = countries.map(c => 
      c.code === code ? { ...c, isAllowed: !c.isAllowed } : c
    );
    setCountries(updatedCountries);
    
    const allowedCodes = updatedCountries.filter(c => c.isAllowed).map(c => c.code);
    setPolicy({ ...policy, allowedCountries: allowedCodes });
  };

  const updateProviderStatus = (id: string, status: SmsProvider['status']) => {
    const updated = providers.map(p => 
      p.id === id ? { ...p, status } : p
    );
    setProviders(updated);
  };

  const updateRoutingWeight = (id: string, weight: number) => {
    const updated = providers.map(p => 
      p.id === id ? { ...p, routingWeight: weight } : p
    );
    // Normalize sum of weights to 100
    setProviders(updated);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-6 shadow-xl text-slate-100">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-slate-800 pb-4 mb-6 gap-4">
        <div>
          <h2 className="text-xl font-bold font-display text-slate-100 flex items-center gap-2">
            <Settings className="w-5 h-5 text-indigo-400" /> Administrative &amp; Operations Control
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Configure regional routing policies, manage carrier failover, review logs, and monitor fraud telemetry.
          </p>
        </div>
        
        {/* Quick Summary Widgets */}
        <div className="flex items-center gap-2 bg-slate-950 p-2 rounded-xl border border-slate-800">
          <div className="text-center px-3 border-r border-slate-800">
            <span className="text-[10px] uppercase text-slate-500 block">Delivery Rate</span>
            <span className="text-sm font-bold text-emerald-400 font-mono">{deliveryRate}%</span>
          </div>
          <div className="text-center px-3 border-r border-slate-800">
            <span className="text-[10px] uppercase text-slate-500 block">Avg Latency</span>
            <span className="text-sm font-bold text-indigo-400 font-mono">{avgLatency}ms</span>
          </div>
          <div className="text-center px-3">
            <span className="text-[10px] uppercase text-slate-500 block">Spent</span>
            <span className="text-sm font-bold text-slate-300 font-mono">${totalCost.toFixed(3)}</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 mb-6 gap-1 overflow-x-auto">
        <button
          onClick={() => setActiveTab('policy')}
          className={`px-4 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 border-b-2 ${activeTab === 'policy' ? 'border-indigo-500 text-indigo-400 bg-slate-800/40' : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-800/20'}`}
        >
          <Shield className="w-4 h-4" /> Global Policy
        </button>
        <button
          onClick={() => setActiveTab('providers')}
          className={`px-4 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 border-b-2 ${activeTab === 'providers' ? 'border-indigo-500 text-indigo-400 bg-slate-800/40' : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-800/20'}`}
        >
          <Server className="w-4 h-4" /> Routing &amp; Providers
        </button>
        <button
          onClick={() => setActiveTab('health')}
          className={`px-4 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 border-b-2 ${activeTab === 'health' ? 'border-indigo-500 text-indigo-400 bg-slate-800/40' : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-800/20'}`}
        >
          <Activity className="w-4 h-4" /> Live Diagnostics
        </button>
        <button
          onClick={() => setActiveTab('abuse')}
          className={`px-4 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 border-b-2 ${activeTab === 'abuse' ? 'border-indigo-500 text-indigo-400 bg-slate-800/40' : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-800/20'}`}
        >
          <AlertTriangle className="w-4 h-4" /> Fraud &amp; Abuse
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`px-4 py-2 text-xs font-semibold rounded-t-lg transition flex items-center gap-1.5 border-b-2 ${activeTab === 'audit' ? 'border-indigo-500 text-indigo-400 bg-slate-800/40' : 'border-transparent text-slate-400 hover:text-slate-300 hover:bg-slate-800/20'}`}
        >
          <FileText className="w-4 h-4" /> System Audits
        </button>
      </div>

      {/* Content Areas */}
      <div className="min-h-[380px]">
        {activeTab === 'policy' && (
          <div className="space-y-6">
            <h3 className="text-sm font-semibold text-slate-200">Tenant-Wide SMS Policy Options</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Basic Options */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider">Authentication Rates</h4>
                
                <div>
                  <label className="text-xs text-slate-400 block mb-1">Max Send Attempts (per window)</label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    value={policy.maxAttempts}
                    onChange={(e) => setPolicy({ ...policy, maxAttempts: parseInt(e.target.value) || 3 })}
                    className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                  />
                  <p className="text-[10px] text-slate-500 mt-1">Locks phone number after consecutive invalid codes.</p>
                </div>

                <div className="grid grid-cols-2 gap-3">
                  <div>
                    <label className="text-xs text-slate-400 block mb-1">Expiry (Minutes)</label>
                    <input
                      type="number"
                      min="1"
                      max="30"
                      value={policy.codeExpiryMinutes}
                      onChange={(e) => setPolicy({ ...policy, codeExpiryMinutes: parseInt(e.target.value) || 5 })}
                      className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                  <div>
                    <label className="text-xs text-slate-400 block mb-1">Resend Delay (Secs)</label>
                    <input
                      type="number"
                      min="10"
                      max="300"
                      value={policy.resendDelaySeconds}
                      onChange={(e) => setPolicy({ ...policy, resendDelaySeconds: parseInt(e.target.value) || 60 })}
                      className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                    />
                  </div>
                </div>

                <div>
                  <label className="text-xs text-slate-400 block mb-1">Monthly SMS Budget Limit ($)</label>
                  <input
                    type="number"
                    value={policy.smsCostLimitMonthly}
                    onChange={(e) => setPolicy({ ...policy, smsCostLimitMonthly: parseFloat(e.target.value) || 500 })}
                    className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-100 font-mono focus:outline-none focus:border-indigo-500"
                  />
                </div>
              </div>

              {/* Carrier Signals & Anti-Abuse Toggle */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-800 space-y-4">
                <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider">Advanced Anti-Fraud Controls</h4>

                <div className="flex items-start gap-3 p-2 rounded hover:bg-slate-900/60 transition">
                  <input
                    type="checkbox"
                    id="simChangeBlock"
                    checked={policy.simChangeBlock}
                    onChange={(e) => setPolicy({ ...policy, simChangeBlock: e.target.checked })}
                    className="mt-1 accent-indigo-500"
                  />
                  <div>
                    <label htmlFor="simChangeBlock" className="text-xs font-semibold text-slate-200 block">
                      Block on Carrier SIM-Swap Flag
                    </label>
                    <p className="text-[10px] text-slate-400 mt-0.5">
                      Query IMSI/ICCID change telemetry and halt SMS dispatch if a swap is detected within 48 hours.
                    </p>
                  </div>
                </div>

                <div className="flex items-start gap-3 p-2 rounded hover:bg-slate-900/60 transition">
                  <input
                    type="checkbox"
                    id="pumpingProtection"
                    checked={policy.pumpingProtection}
                    onChange={(e) => setPolicy({ ...policy, pumpingProtection: e.target.checked })}
                    className="mt-1 accent-indigo-500"
                  />
                  <div>
                    <label htmlFor="pumpingProtection" className="text-xs font-semibold text-slate-200 block">
                      SMS Toll Fraud / Pumping Prevention
                    </label>
                    <p className="text-[10px] text-slate-400 mt-0.5">
                      Intelligently detect rapid requests to premium-rate networks and enforce hard IP rate-limits.
                    </p>
                  </div>
                </div>

                <div>
                  <label className="text-xs text-slate-400 block mb-1">Default Dispatch Template</label>
                  <textarea
                    value={policy.defaultTemplate}
                    onChange={(e) => setPolicy({ ...policy, defaultTemplate: e.target.value })}
                    rows={2}
                    className="w-full bg-slate-900 border border-slate-800 rounded px-3 py-1.5 text-xs text-slate-100 focus:outline-none focus:border-indigo-500 resize-none font-mono"
                  />
                </div>
              </div>
            </div>

            {/* Supported Regions */}
            <div className="bg-slate-950 p-4 rounded-xl border border-slate-800">
              <div className="flex justify-between items-center mb-3">
                <h4 className="text-xs font-bold uppercase text-slate-400 tracking-wider flex items-center gap-1">
                  <Globe className="w-4 h-4 text-indigo-400" /> Supported Regional Delivery Codes
                </h4>
                <span className="text-[10px] text-slate-500">
                  Allowing {countries.filter(c => c.isAllowed).length} of {countries.length} regions
                </span>
              </div>
              <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-5 gap-3">
                {countries.map(country => (
                  <button
                    key={country.code}
                    onClick={() => toggleCountry(country.code)}
                    className={`p-2.5 rounded-lg border text-left transition flex items-center justify-between group ${country.isAllowed ? 'bg-indigo-950/20 border-indigo-500/50 hover:bg-indigo-950/40 text-slate-200' : 'bg-slate-900/40 border-slate-800 text-slate-500 hover:border-slate-700'}`}
                  >
                    <div className="flex items-center gap-2">
                      <span className="text-base">{country.flag}</span>
                      <div>
                        <p className="text-xs font-semibold">{country.name}</p>
                        <p className="text-[9px] font-mono opacity-80">{country.dialCode}</p>
                      </div>
                    </div>
                    <span className={`w-1.5 h-1.5 rounded-full ${country.isAllowed ? 'bg-emerald-400' : 'bg-slate-700'}`} />
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'providers' && (
          <div className="space-y-6">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-semibold text-slate-200">Regional Gateway Providers &amp; Weighted Routing</h3>
              <span className="text-[11px] text-amber-400 flex items-center gap-1 bg-amber-950/20 px-2 py-0.5 rounded border border-amber-500/20">
                <AlertTriangle className="w-3.5 h-3.5" /> Failover triggers automatically on outages
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {providers.map(prov => (
                <div key={prov.id} className="bg-slate-950 border border-slate-800 rounded-xl p-4 flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h4 className="text-xs font-bold text-slate-100 flex items-center gap-1.5">
                          {prov.name}
                          <span className={`text-[9px] font-mono px-1.5 py-0.5 rounded font-semibold ${prov.status === 'active' ? 'bg-emerald-950 text-emerald-400 border border-emerald-500/20' : prov.status === 'degraded' ? 'bg-amber-950 text-amber-400 border border-amber-500/20' : 'bg-rose-950 text-rose-400 border border-rose-500/20'}`}>
                            {prov.status.toUpperCase()}
                          </span>
                        </h4>
                        <p className="text-[9px] text-slate-500 font-mono mt-0.5">ID: {prov.id}</p>
                      </div>
                      <div className="flex gap-1">
                        <button
                          onClick={() => updateProviderStatus(prov.id, 'active')}
                          className="p-1 rounded text-emerald-400 hover:bg-slate-800 text-[10px]"
                          title="Set Active"
                        >
                          <CheckCircle className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => updateProviderStatus(prov.id, 'degraded')}
                          className="p-1 rounded text-amber-400 hover:bg-slate-800 text-[10px]"
                          title="Set Degraded"
                        >
                          <AlertTriangle className="w-3.5 h-3.5" />
                        </button>
                        <button
                          onClick={() => updateProviderStatus(prov.id, 'offline')}
                          className="p-1 rounded text-rose-400 hover:bg-slate-800 text-[10px]"
                          title="Simulate Outage"
                        >
                          <XCircle className="w-3.5 h-3.5" />
                        </button>
                      </div>
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-center text-[10px] font-mono bg-slate-900/60 p-2 rounded border border-slate-800 mb-4">
                      <div>
                        <span className="text-slate-500 block text-[8px] uppercase">Sent</span>
                        <span className="text-slate-300 font-bold">{prov.totalSent}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[8px] uppercase">Failed</span>
                        <span className="text-rose-400 font-bold">{prov.totalFailed}</span>
                      </div>
                      <div>
                        <span className="text-slate-500 block text-[8px] uppercase">Avg Latency</span>
                        <span className="text-indigo-400 font-bold">{prov.avgLatencyMs}ms</span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-2">
                    <div className="flex justify-between items-center text-xs">
                      <span className="text-slate-400">Routing Priority Weight</span>
                      <span className="font-mono font-semibold text-slate-200">{prov.routingWeight}%</span>
                    </div>
                    <input
                      type="range"
                      min="0"
                      max="100"
                      value={prov.routingWeight}
                      onChange={(e) => updateRoutingWeight(prov.id, parseInt(e.target.value) || 0)}
                      className="w-full h-1 bg-slate-800 rounded-lg appearance-none cursor-pointer accent-indigo-500"
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {activeTab === 'health' && (
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-semibold text-slate-200">Real-Time SMS Queue &amp; Carrier Diagnostics</h3>
              <button
                onClick={onClearLogs}
                className="text-[10px] text-rose-400 hover:text-rose-300 hover:underline px-2 py-1 font-mono rounded"
              >
                Clear Log History
              </button>
            </div>

            <div className="overflow-x-auto border border-slate-800 rounded-xl">
              <table className="w-full text-left text-xs text-slate-300">
                <thead className="bg-slate-950 text-[10px] text-slate-400 font-mono uppercase tracking-wider border-b border-slate-800">
                  <tr>
                    <th className="p-3">Timestamp</th>
                    <th className="p-3">Destination (Masked)</th>
                    <th className="p-3">Purpose</th>
                    <th className="p-3">Provider</th>
                    <th className="p-3">Latency</th>
                    <th className="p-3">SIM Risk</th>
                    <th className="p-3 text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono">
                  {logs.length === 0 ? (
                    <tr>
                      <td colSpan={7} className="p-8 text-center text-slate-500 text-xs">
                        No delivery logs in current session. Trigger an authentication event to see telemetry.
                      </td>
                    </tr>
                  ) : (
                    logs.map(log => (
                      <tr key={log.id} className="hover:bg-slate-900/40 transition">
                        <td className="p-3 text-slate-400 text-[11px] whitespace-nowrap">
                          {new Date(log.timestamp).toLocaleTimeString()}
                        </td>
                        <td className="p-3 text-slate-200 font-semibold">{log.maskedRecipient}</td>
                        <td className="p-3">
                          <span className={`px-1.5 py-0.5 rounded text-[10px] ${log.purpose === 'enrollment' ? 'bg-blue-950 text-blue-400 border border-blue-800/30' : log.purpose === 'authentication' ? 'bg-indigo-950 text-indigo-400 border border-indigo-800/30' : 'bg-purple-950 text-purple-400 border border-purple-800/30'}`}>
                            {log.purpose}
                          </span>
                        </td>
                        <td className="p-3 text-slate-300">{log.providerId}</td>
                        <td className="p-3 text-indigo-400">{log.latencyMs}ms</td>
                        <td className="p-3">
                          <span className={`px-1 py-0.5 rounded text-[10px] ${log.simSwapRisk === 'high' ? 'bg-rose-950 text-rose-400' : log.simSwapRisk === 'medium' ? 'bg-amber-950 text-amber-400' : 'bg-slate-900 text-slate-400'}`}>
                            {log.simSwapRisk.toUpperCase()}
                          </span>
                        </td>
                        <td className="p-3 text-right">
                          <span className={`inline-flex items-center gap-1 font-bold text-[11px] ${log.state === 'delivered' ? 'text-emerald-400' : log.state === 'failed' ? 'text-rose-400' : log.state === 'queued' ? 'text-blue-400' : 'text-amber-400'}`}>
                            {log.state === 'delivered' && <CheckCircle className="w-3 h-3" />}
                            {log.state === 'failed' && <XCircle className="w-3 h-3" />}
                            {log.state === 'queued' && <RefreshCw className="w-3 h-3 animate-spin" />}
                            {log.state === 'delayed' && <AlertTriangle className="w-3 h-3" />}
                            {log.state.toUpperCase()}
                          </span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'abuse' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-200">Abuse Detection &amp; Security Alerts</h3>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">SMS Toll Pumping</span>
                <p className="text-sm font-bold text-slate-200 mt-1">Status: Stable</p>
                <div className="mt-2 text-xs text-slate-500">
                  No abnormal premium region velocity triggers detected in this hour.
                </div>
              </div>
              
              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Encountered SIM-Swaps</span>
                <p className="text-sm font-bold text-slate-200 mt-1">
                  Blocked: {logs.filter(l => l.simSwapRisk === 'high').length} requests
                </p>
                <div className="mt-2 text-xs text-slate-500">
                  IMSI update blocks active to defend credential recovery flows.
                </div>
              </div>

              <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
                <span className="text-[10px] text-slate-400 uppercase font-mono block">Abuse Status Posture</span>
                <p className="text-sm font-bold text-emerald-400 mt-1">Normal Operational Posture</p>
                <div className="mt-2 text-xs text-slate-500">
                  No carrier rate-limits or API credential fatigue present.
                </div>
              </div>
            </div>

            <div className="bg-slate-950 border border-slate-800 rounded-xl p-4">
              <h4 className="text-xs font-bold uppercase text-rose-400 tracking-wider mb-2 flex items-center gap-1.5">
                <AlertTriangle className="w-4 h-4" /> Active Abuse &amp; Premium Rate Block Events
              </h4>
              <div className="space-y-2 max-h-40 overflow-y-auto pr-2">
                {logs.filter(l => l.isPumpingRisk || l.simSwapRisk === 'high').length === 0 ? (
                  <p className="text-xs text-slate-500 italic py-4 text-center">No security block events triggered. Check your SIM/Network controls in the simulator to test block responses.</p>
                ) : (
                  logs.filter(l => l.isPumpingRisk || l.simSwapRisk === 'high').map(log => (
                    <div key={log.id} className="bg-rose-950/20 border border-rose-900/40 p-2 rounded-lg text-xs flex justify-between items-center">
                      <div>
                        <span className="font-bold text-rose-400 font-mono">BLOCK: </span>
                        <span className="text-slate-300">Attempted dispatch to {log.maskedRecipient} halted</span>
                        <p className="text-[10px] text-slate-500 mt-0.5">
                          Reason: {log.simSwapRisk === 'high' ? 'High-risk SIM-swap event reported by carrier.' : 'Toll fraud/pumping signature matches.'}
                        </p>
                      </div>
                      <span className="text-[10px] text-slate-400 font-mono">{new Date(log.timestamp).toLocaleTimeString()}</span>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}

        {activeTab === 'audit' && (
          <div className="space-y-4">
            <h3 className="text-sm font-semibold text-slate-200">Tenant Administrator Action Logs</h3>

            <div className="overflow-y-auto max-h-80 pr-2 border border-slate-800 rounded-xl divide-y divide-slate-800">
              {auditLogs.length === 0 ? (
                <div className="p-8 text-center text-slate-500 text-xs italic">
                  No system administrative audit logs recorded yet.
                </div>
              ) : (
                [...auditLogs].reverse().map(audit => (
                  <div key={audit.id} className="p-3 hover:bg-slate-900/40 transition flex justify-between items-start text-xs">
                    <div>
                      <div className="flex items-center gap-2 mb-1">
                        <span className="font-bold text-slate-200 font-mono">{audit.actor}</span>
                        <span className={`px-1.5 py-0.2 rounded text-[9px] font-semibold ${audit.severity === 'critical' ? 'bg-rose-950 text-rose-400' : audit.severity === 'warning' ? 'bg-amber-950 text-amber-400' : 'bg-slate-800 text-slate-300'}`}>
                          {audit.severity.toUpperCase()}
                        </span>
                      </div>
                      <p className="text-slate-300 font-mono">{audit.action}</p>
                      <p className="text-[10px] text-slate-500 mt-0.5">{audit.details}</p>
                    </div>
                    <span className="text-[10px] text-slate-400 font-mono">{new Date(audit.timestamp).toLocaleTimeString()}</span>
                  </div>
                ))
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
