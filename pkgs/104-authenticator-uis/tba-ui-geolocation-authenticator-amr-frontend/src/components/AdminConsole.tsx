import React, { useState } from 'react';
import { ZonePolicyEditor } from './ZonePolicyEditor';
import { BoundarySimulator } from './BoundarySimulator';
import { SignalProviderHealthCard } from './SignalProviderHealthCard';
import { LocationSourceBadge } from './LocationSourceBadge';
import { 
  ZonePolicy, SimulationProfile, ProviderHealth, LocationSource, AuditRecord 
} from '../types';
import { Settings, Activity, Compass, Database, FileText } from 'lucide-react';

interface AdminConsoleProps {
  policies: ZonePolicy[];
  onSavePolicy: (policy: ZonePolicy) => void;
  onDeletePolicy: (id: string) => void;
  simulationProfiles: SimulationProfile[];
  activeProfile: SimulationProfile;
  onSelectProfile: (profile: SimulationProfile) => void;
  onChangeProfileValue: (key: keyof SimulationProfile, value: any) => void;
  providers: ProviderHealth[];
  onRefreshProvider: (id: string) => void;
  onUpdateProviderStatus: (id: string, status: ProviderHealth['status']) => void;
  auditLogs: AuditRecord[];
  sources: LocationSource[];
}

export const AdminConsole: React.FC<AdminConsoleProps> = ({
  policies,
  onSavePolicy,
  onDeletePolicy,
  simulationProfiles,
  activeProfile,
  onSelectProfile,
  onChangeProfileValue,
  providers,
  onRefreshProvider,
  onUpdateProviderStatus,
  auditLogs,
  sources
}) => {
  const [activeTab, setActiveTab] = useState<'policy' | 'simulate' | 'health' | 'audit' | 'sources'>('policy');

  return (
    <div className="space-y-6">
      {/* Admin Nav */}
      <div className="flex overflow-x-auto bg-slate-50 border border-slate-200 rounded-lg p-1.5 gap-1.5">
        <button
          onClick={() => setActiveTab('policy')}
          className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-md transition-all ${
            activeTab === 'policy' ? 'bg-white text-indigo-700 shadow-sm border border-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <Settings className="w-4 h-4" />
          <span>Zone Policies</span>
        </button>
        <button
          onClick={() => setActiveTab('simulate')}
          className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-md transition-all ${
            activeTab === 'simulate' ? 'bg-white text-indigo-700 shadow-sm border border-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <Compass className="w-4 h-4" />
          <span>Simulation</span>
        </button>
        <button
          onClick={() => setActiveTab('health')}
          className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-md transition-all ${
            activeTab === 'health' ? 'bg-white text-indigo-700 shadow-sm border border-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <Activity className="w-4 h-4" />
          <span>Provider Health</span>
        </button>
        <button
          onClick={() => setActiveTab('audit')}
          className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-md transition-all ${
            activeTab === 'audit' ? 'bg-white text-indigo-700 shadow-sm border border-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <FileText className="w-4 h-4" />
          <span>Audit Logs</span>
        </button>
        <button
          onClick={() => setActiveTab('sources')}
          className={`flex-1 min-w-[120px] flex items-center justify-center gap-2 py-2 px-3 text-xs font-semibold rounded-md transition-all ${
            activeTab === 'sources' ? 'bg-white text-indigo-700 shadow-sm border border-slate-200' : 'text-slate-600 hover:bg-slate-100 hover:text-slate-900'
          }`}
        >
          <Database className="w-4 h-4" />
          <span>Data Sources</span>
        </button>
      </div>

      {/* Tab Content */}
      <div className="min-h-[500px]">
        {activeTab === 'policy' && (
          <ZonePolicyEditor
            policies={policies}
            onSavePolicy={onSavePolicy}
            onDeletePolicy={onDeletePolicy}
          />
        )}

        {activeTab === 'simulate' && (
          <BoundarySimulator
            simulationProfiles={simulationProfiles}
            activeProfile={activeProfile}
            policies={policies}
            onSelectProfile={onSelectProfile}
            onChangeProfileValue={onChangeProfileValue}
          />
        )}

        {activeTab === 'health' && (
          <SignalProviderHealthCard
            providers={providers}
            onRefreshProvider={onRefreshProvider}
            onUpdateStatus={onUpdateProviderStatus}
          />
        )}

        {activeTab === 'audit' && (
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
            <div className="p-4 border-b border-slate-100 bg-slate-50 flex justify-between items-center">
              <div>
                <h4 className="text-sm font-semibold text-slate-900 font-display">Authentication Audit Provenance</h4>
                <p className="text-xs text-slate-500">Immutable ledger of contextual login decisions and step-up evaluations</p>
              </div>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs" role="table">
                <thead>
                  <tr className="bg-slate-50 border-b border-slate-100 uppercase tracking-wider text-slate-400 font-bold">
                    <th className="py-3 px-4">Time</th>
                    <th className="py-3 px-4">User</th>
                    <th className="py-3 px-4">Source & Decision</th>
                    <th className="py-3 px-4">Context Details</th>
                    <th className="py-3 px-4">Ref</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {auditLogs.map((log) => (
                    <tr key={log.id} className="hover:bg-slate-50/50">
                      <td className="py-3 px-4 font-mono text-slate-500">
                        {new Date(log.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit', second: '2-digit' })}
                      </td>
                      <td className="py-3 px-4 font-semibold text-slate-700">{log.userEmail}</td>
                      <td className="py-3 px-4">
                        <div className="flex flex-col gap-1 items-start">
                          <span className={`inline-flex px-2 py-0.5 rounded text-[10px] font-bold ${
                            log.decision === 'Allow' ? 'bg-emerald-100 text-emerald-800' :
                            log.decision === 'Step-Up' ? 'bg-amber-100 text-amber-800' : 'bg-rose-100 text-rose-800'
                          }`}>
                            {log.decision}
                          </span>
                          <span className="text-[10px] text-slate-500 truncate max-w-[150px]">{log.sourceType}</span>
                        </div>
                      </td>
                      <td className="py-3 px-4 text-[10px] text-slate-500 space-y-0.5">
                        <div className="font-mono">Pol: {log.policyName} ({log.policyVersion})</div>
                        {log.fallbackUsed && (
                          <div className="text-indigo-600 font-semibold flex items-center gap-1">
                            Step-Up: {log.fallbackUsed}
                          </div>
                        )}
                        {log.spoofSuspected && (
                          <div className="text-rose-600 font-bold">SPOOF SUSPECTED</div>
                        )}
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-400 text-[10px]">{log.auditReference.substring(0, 8)}...</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {activeTab === 'sources' && (
          <div className="bg-white border border-slate-200 rounded-xl shadow-sm p-5 space-y-4">
            <div>
              <h4 className="text-sm font-semibold text-slate-900 font-display">Registered Evidence Sources</h4>
              <p className="text-xs text-slate-500">Approved geographic identity telemetry providers</p>
            </div>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {sources.map(source => (
                <div key={source.id} className="border border-slate-150 rounded-lg p-4 space-y-3">
                  <div className="flex justify-between items-start">
                    <LocationSourceBadge sourceType={source.type} state={source.state} />
                    <span className="text-[10px] font-mono text-slate-400">P{source.priority}</span>
                  </div>
                  
                  <div>
                    <div className="text-xs font-semibold text-slate-800">{source.name}</div>
                    <div className="text-[10px] text-slate-500 mt-0.5">ID: {source.id}</div>
                  </div>
                  
                  <div className="grid grid-cols-2 gap-2 text-[10px] font-mono pt-2 border-t border-slate-100">
                    <div>
                      <span className="text-slate-400 block uppercase">Accuracy Thresh</span>
                      <span className="text-slate-700">{source.accuracyThreshold}m</span>
                    </div>
                    <div>
                      <span className="text-slate-400 block uppercase">Freshness</span>
                      <span className="text-slate-700">{source.freshnessLimit} min</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
