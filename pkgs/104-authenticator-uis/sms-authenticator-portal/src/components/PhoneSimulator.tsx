import React from 'react';
import { Smartphone, Wifi, Battery, ShieldAlert, CheckCircle, RefreshCw, AlertTriangle, MessageSquare, Copy } from 'lucide-react';
import { SmsLog } from '../types';

interface PhoneSimulatorProps {
  logs: SmsLog[];
  onCopyCode: (code: string) => void;
  simSwapRisk: 'low' | 'medium' | 'high';
  setSimSwapRisk: (risk: 'low' | 'medium' | 'high') => void;
  networkCondition: 'good' | 'congested' | 'outage';
  setNetworkCondition: (cond: 'good' | 'congested' | 'outage') => void;
}

export const PhoneSimulator: React.FC<PhoneSimulatorProps> = ({
  logs,
  onCopyCode,
  simSwapRisk,
  setSimSwapRisk,
  networkCondition,
  setNetworkCondition
}) => {
  const activeSms = logs.length > 0 ? logs[0] : null;

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-3xl p-4 shadow-2xl relative max-w-sm mx-auto w-full font-sans overflow-hidden">
      {/* Top notch */}
      <div className="absolute top-0 left-1/2 -translate-x-1/2 w-40 h-5 bg-black rounded-b-xl z-20 flex items-center justify-around px-4">
        <div className="w-2 h-2 rounded-full bg-slate-800"></div>
        <div className="w-12 h-1 bg-slate-800 rounded-full"></div>
      </div>

      {/* Internal Phone Screen Container */}
      <div className="bg-[#0f172a] rounded-2xl border border-slate-950 p-3 pt-6 min-h-[500px] flex flex-col justify-between relative text-slate-100">
        {/* Status bar */}
        <div className="flex justify-between items-center text-[10px] text-slate-400 font-mono px-2 mb-3">
          <span>Carrier SIM</span>
          <div className="flex items-center gap-1">
            <Wifi className={`w-3 h-3 ${networkCondition === 'good' ? 'text-emerald-400' : networkCondition === 'congested' ? 'text-amber-400' : 'text-rose-500'}`} />
            <Battery className="w-3 h-3" />
            <span>100%</span>
          </div>
        </div>

        {/* Messaging Interface */}
        <div className="flex-1 flex flex-col justify-between">
          <div className="space-y-4">
            <div className="flex items-center justify-between border-b border-slate-800 pb-2">
              <div className="flex items-center gap-2">
                <div className="w-8 h-8 rounded-full bg-indigo-900/60 flex items-center justify-center text-indigo-400 font-bold text-xs">
                  TX
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-slate-200">AuthGateway</h4>
                  <p className="text-[9px] text-slate-400 font-mono">Sender ID: SMS-AUTH</p>
                </div>
              </div>
              <span className="text-[9px] text-slate-500 bg-slate-800/60 px-1.5 py-0.5 rounded font-mono">
                {networkCondition.toUpperCase()}
              </span>
            </div>

            {/* Simulated Chat bubble list */}
            <div className="space-y-3 min-h-[260px] overflow-y-auto max-h-[300px] pr-1">
              {logs.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-48 text-center text-slate-500">
                  <MessageSquare className="w-10 h-10 mb-2 opacity-30 text-slate-400" />
                  <p className="text-xs">No active sessions or messages</p>
                  <p className="text-[10px] opacity-60">Initiate enrollment or login to receive OTP</p>
                </div>
              ) : (
                [...logs].reverse().map((log) => (
                  <div key={log.id} className="bg-slate-800/80 border border-slate-700/50 rounded-xl p-3 shadow-md">
                    <div className="flex justify-between items-start mb-1 text-[9px] font-mono text-slate-400">
                      <span>{new Date(log.timestamp).toLocaleTimeString()}</span>
                      <div className="flex items-center gap-1">
                        {log.state === 'delivered' && (
                          <span className="text-emerald-400 flex items-center gap-0.5">
                            <CheckCircle className="w-2.5 h-2.5" /> Delivered
                          </span>
                        )}
                        {log.state === 'queued' && (
                          <span className="text-blue-400 flex items-center gap-0.5">
                            <RefreshCw className="w-2.5 h-2.5 animate-spin" /> Queued
                          </span>
                        )}
                        {log.state === 'delayed' && (
                          <span className="text-amber-400 flex items-center gap-0.5">
                            <AlertTriangle className="w-2.5 h-2.5" /> Delayed
                          </span>
                        )}
                        {log.state === 'failed' && (
                          <span className="text-rose-400 flex items-center gap-0.5">
                            <ShieldAlert className="w-2.5 h-2.5" /> Failed
                          </span>
                        )}
                      </div>
                    </div>

                    <p className="text-xs text-slate-200 mt-1 leading-relaxed">
                      Your security verification code is <span className="font-mono font-bold text-indigo-400 text-sm tracking-wider">{log.code}</span>. It expires in 5 minutes. Do not share this code with anyone.
                    </p>

                    <div className="mt-2.5 flex justify-between items-center bg-slate-900/60 p-1.5 rounded-lg border border-slate-800">
                      <span className="text-[9px] text-indigo-300 font-mono">OTP: {log.code}</span>
                      <button
                        onClick={() => onCopyCode(log.code)}
                        className="text-[10px] text-indigo-400 hover:text-indigo-300 flex items-center gap-1 hover:bg-indigo-950/40 px-2 py-0.5 rounded transition"
                      >
                        <Copy className="w-3 h-3" /> Copy
                      </button>
                    </div>
                  </div>
                ))
              )}
            </div>
          </div>

          {/* Quick Input Panel to represent simulated hardware states */}
          <div className="mt-4 pt-3 border-t border-slate-800">
            <h5 className="text-[10px] uppercase font-semibold text-slate-400 tracking-wider mb-2 flex items-center gap-1">
              <ShieldAlert className="w-3 h-3 text-indigo-400" /> SIM &amp; Network Simulation Controls
            </h5>
            
            <div className="grid grid-cols-2 gap-2 text-[10px]">
              <div>
                <label className="text-slate-500 block mb-1">SIM Swap Risk</label>
                <select
                  value={simSwapRisk}
                  onChange={(e) => setSimSwapRisk(e.target.value as any)}
                  className="w-full bg-slate-900 border border-slate-800 rounded px-1.5 py-1 text-slate-300 focus:outline-none focus:border-indigo-500 font-mono"
                >
                  <option value="low">Low Risk</option>
                  <option value="medium">Medium Risk</option>
                  <option value="high">High Risk (Block!)</option>
                </select>
              </div>

              <div>
                <label className="text-slate-500 block mb-1">Network Condition</label>
                <select
                  value={networkCondition}
                  onChange={(e) => setNetworkCondition(e.target.value as any)}
                  className="w-full bg-slate-900 border border-slate-800 rounded px-1.5 py-1 text-slate-300 focus:outline-none focus:border-indigo-500 font-mono"
                >
                  <option value="good">Good Network</option>
                  <option value="congested">Congested (Delay)</option>
                  <option value="outage">Provider Outage</option>
                </select>
              </div>
            </div>

            <div className="mt-2 bg-slate-900/40 p-2 rounded text-[9px] text-slate-400 font-mono flex items-center gap-1.5">
              <div className={`w-1.5 h-1.5 rounded-full ${simSwapRisk === 'high' ? 'bg-rose-500 animate-pulse' : 'bg-emerald-500'}`} />
              <span>
                {simSwapRisk === 'high' 
                  ? 'High risk flagged by carrier signals. Verification blocked!' 
                  : 'SIM lifecycle signal normal. Carrier: Twilio-TIGR'}
              </span>
            </div>
          </div>
        </div>

        {/* Home button indicator */}
        <div className="w-24 h-1 bg-slate-700 mx-auto rounded-full mt-2"></div>
      </div>
    </div>
  );
};
