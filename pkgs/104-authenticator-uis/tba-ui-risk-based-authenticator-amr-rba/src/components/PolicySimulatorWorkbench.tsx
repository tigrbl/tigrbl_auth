import React from 'react';
import { 
  ShieldAlert, 
  HelpCircle, 
  Play, 
  Info, 
  UserCheck, 
  Compass, 
  ChevronRight,
  ShieldAlert as AlertIcon,
  PlusCircle,
  Database
} from 'lucide-react';
import { SimulationScenario, RiskSignal, SignalStatus, RiskDecision, RiskLevel } from '../types';

interface PolicySimulatorWorkbenchProps {
  scenarios: SimulationScenario[];
  activeScenarioId: string;
  onSelectScenario: (scenario: SimulationScenario) => void;
  signals: RiskSignal[];
  onUpdateSignalStatus: (signalId: string, status: SignalStatus, customValue?: string) => void;
  computedDecision: RiskDecision;
  computedRiskLevel: RiskLevel;
  matchingRuleName: string;
  onTriggerEvaluation: () => void;
}

export default function PolicySimulatorWorkbench({
  scenarios,
  activeScenarioId,
  onSelectScenario,
  signals,
  onUpdateSignalStatus,
  computedDecision,
  computedRiskLevel,
  matchingRuleName,
  onTriggerEvaluation
}: PolicySimulatorWorkbenchProps) {

  // Helper color map for status badges
  const getStatusColor = (status: SignalStatus) => {
    switch (status) {
      case 'safe':
        return 'bg-emerald-50 text-emerald-700 border-emerald-200';
      case 'suspicious':
        return 'bg-amber-50 text-amber-700 border-amber-200';
      case 'compromised':
        return 'bg-rose-50 text-rose-700 border-rose-200';
      case 'unavailable':
        return 'bg-slate-100 text-slate-600 border-slate-200';
      default:
        return 'bg-slate-50 text-slate-600 border-slate-100';
    }
  };

  return (
    <div id="policy-simulation-workbench" className="rounded-2xl border border-slate-200 bg-white shadow-xs p-6 space-y-6">
      
      {/* Header */}
      <div>
        <div className="flex items-center gap-2">
          <div className="h-2 w-2 rounded-full bg-indigo-500 animate-pulse"></div>
          <h3 className="font-display text-lg font-bold text-slate-900">Policy Simulator Workbench</h3>
        </div>
        <p className="text-xs text-slate-500 mt-1 font-sans">
          Load threat scenarios or tweak telemetry feeds manually. Decisions update instantly on the user's terminal.
        </p>
      </div>

      {/* 1. Prepackaged Scenarios Grid */}
      <div>
        <label className="block text-xs font-mono font-medium text-slate-500 uppercase tracking-wider mb-3">
          Preset Risk Templates
        </label>
        
        <div className="grid grid-cols-2 md:grid-cols-3 gap-2.5">
          {scenarios.map(scen => {
            const isActive = activeScenarioId === scen.id;
            return (
              <button
                key={scen.id}
                onClick={() => onSelectScenario(scen)}
                className={`text-left p-3 rounded-xl border text-xs transition duration-150 ${
                  isActive 
                    ? 'bg-slate-900 text-white border-slate-900 ring-1 ring-slate-900 shadow-sm' 
                    : 'bg-slate-50 hover:bg-slate-100 text-slate-700 border-slate-200'
                }`}
              >
                <div className="font-display font-bold truncate">{scen.name}</div>
                <div className={`mt-1 font-sans line-clamp-2 leading-relaxed text-[10px] ${
                  isActive ? 'text-slate-300' : 'text-slate-500'
                }`}>
                  {scen.description}
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Divider */}
      <div className="h-px bg-slate-100"></div>

      {/* 2. Real-time Telemetry Control Panel */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <label className="block text-xs font-mono font-medium text-slate-500 uppercase tracking-wider">
            Live Risk Signals (Active Overrides)
          </label>
          <span className="text-[10px] text-slate-400 font-mono">5 Telemetry Channels active</span>
        </div>

        <div className="space-y-3.5">
          {signals.map(sig => {
            return (
              <div 
                key={sig.id} 
                className="flex flex-col gap-2 p-3.5 rounded-xl border border-slate-100 bg-slate-50/70"
              >
                {/* Name, Category and Freshness */}
                <div className="flex items-center justify-between gap-2">
                  <div className="flex items-center gap-1.5 min-w-0">
                    <span className="h-1.5 w-1.5 rounded-full bg-slate-400"></span>
                    <span className="font-display font-semibold text-xs text-slate-800 truncate">{sig.name}</span>
                    <span className="text-[10px] font-mono bg-slate-200/60 px-1 py-0.2 rounded text-slate-500 capitalize flex-shrink-0">
                      {sig.category}
                    </span>
                  </div>
                  <span className="text-[10px] font-mono text-slate-400">{sig.freshness}</span>
                </div>

                {/* Status Switcher & Output Details */}
                <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mt-1 pt-1.5 border-t border-slate-200/50">
                  <div className="text-[11px] font-mono text-slate-600 bg-white py-1 px-2.5 rounded border border-slate-100 truncate flex-1">
                    Value: <span className="text-slate-900 font-medium">{sig.value}</span>
                  </div>

                  <div className="flex gap-1 flex-shrink-0">
                    {(['safe', 'suspicious', 'compromised', 'unavailable'] as SignalStatus[]).map(st => {
                      const isSelected = sig.status === st;
                      let activeBtnClass = '';
                      if (isSelected) {
                        if (st === 'safe') activeBtnClass = 'bg-emerald-600 text-white border-emerald-600';
                        else if (st === 'suspicious') activeBtnClass = 'bg-amber-500 text-white border-amber-500';
                        else if (st === 'compromised') activeBtnClass = 'bg-rose-600 text-white border-rose-600';
                        else activeBtnClass = 'bg-slate-600 text-white border-slate-600';
                      } else {
                        activeBtnClass = 'bg-white hover:bg-slate-100 text-slate-600 border-slate-200';
                      }

                      return (
                        <button
                          key={st}
                          onClick={() => {
                            let customVal = sig.value;
                            if (st === 'safe') {
                              if (sig.id === 'sig_impossible_travel') customVal = '0.0 km/h (Cohesive locations)';
                              if (sig.id === 'sig_device_integrity') customVal = 'Attestation Verified: Enclave Intact';
                              if (sig.id === 'sig_behavioral_typing') customVal = '98% typing match cadence';
                              if (sig.id === 'sig_ip_reputation') customVal = 'Score: 0.01 (Residential)';
                              if (sig.id === 'sig_network_vpn') customVal = 'Standard ISP. No VPN';
                            } else if (st === 'suspicious') {
                              if (sig.id === 'sig_impossible_travel') customVal = '18.4 km/h (Possible commute travel)';
                              if (sig.id === 'sig_device_integrity') customVal = 'Attestation Warnings: API out-of-date';
                              if (sig.id === 'sig_behavioral_typing') customVal = '34% match (Higher keystroke jitter)';
                              if (sig.id === 'sig_ip_reputation') customVal = 'Score: 0.65 (Flagged forum spam IP)';
                              if (sig.id === 'sig_network_vpn') customVal = 'VPN node detected: NordVPN Server';
                            } else if (st === 'compromised') {
                              if (sig.id === 'sig_impossible_travel') customVal = '8,300 km/h (Chicago - London mismatch)';
                              if (sig.id === 'sig_device_integrity') customVal = 'Play Integrity Failed: Rooted Bootloader';
                              if (sig.id === 'sig_behavioral_typing') customVal = '11% match (Extreme speed difference)';
                              if (sig.id === 'sig_ip_reputation') customVal = 'Score: 0.99 (Known brute force botnet)';
                              if (sig.id === 'sig_network_vpn') customVal = 'Active Tor exit node relay';
                            } else {
                              customVal = 'Collector Payload Unavailable / Timeout';
                            }
                            onUpdateSignalStatus(sig.id, st, customVal);
                          }}
                          className={`text-[9px] font-mono px-2 py-1 rounded border capitalize transition-all duration-100 ${activeBtnClass}`}
                        >
                          {st}
                        </button>
                      );
                    })}
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>

      {/* Divider */}
      <div className="h-px bg-slate-100"></div>

      {/* 3. Output Decision Simulation Box */}
      <div className="rounded-2xl bg-slate-900 p-5 text-white space-y-4">
        <div className="flex items-center justify-between">
          <span className="text-[10px] font-mono text-slate-400 tracking-wider uppercase">Computed Engine Output</span>
          <span className="inline-flex items-center rounded-md bg-indigo-500/10 px-2 py-0.5 text-[10px] font-mono font-medium text-indigo-400 ring-1 ring-inset ring-indigo-400/30">
            Real-time Evaluation
          </span>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <span className="text-[11px] text-slate-400 font-mono block">Computed Decision:</span>
            <span className={`text-lg font-display font-extrabold capitalize mt-1 block tracking-tight ${
              computedDecision === 'continue' ? 'text-emerald-400'
              : computedDecision === 'step-up' ? 'text-amber-400'
              : computedDecision === 'review' ? 'text-indigo-400'
              : computedDecision === 'deny' ? 'text-rose-400'
              : 'text-sky-400'
            }`}>
              {computedDecision === 'continue' ? 'Continue (Allow)' : computedDecision}
            </span>
          </div>

          <div>
            <span className="text-[11px] text-slate-400 font-mono block">Computed Risk Level:</span>
            <span className={`text-lg font-display font-extrabold capitalize mt-1 block tracking-tight ${
              computedRiskLevel === 'low' ? 'text-emerald-400'
              : computedRiskLevel === 'medium' ? 'text-amber-400'
              : computedRiskLevel === 'high' ? 'text-orange-400'
              : 'text-rose-500 animate-pulse'
            }`}>
              {computedRiskLevel.toUpperCase()}
            </span>
          </div>
        </div>

        <div className="border-t border-slate-800 pt-3 flex flex-col gap-1.5 text-xs font-mono">
          <div className="flex justify-between">
            <span className="text-slate-400">Triggered Policy Rule:</span>
            <span className="text-slate-200 truncate max-w-[200px]" title={matchingRuleName}>
              {matchingRuleName}
            </span>
          </div>
          <div className="flex justify-between">
            <span className="text-slate-400">Support / Lockout Impact:</span>
            <span className="text-slate-200">
              {computedDecision === 'deny' ? 'High Lockout (Strict isolation)' 
              : computedDecision === 'review' ? 'Held queue (Manual SLA)'
              : computedDecision === 'step-up' ? 'Medium ceremony friction'
              : 'Seamless (Bypass)'}
            </span>
          </div>
        </div>

        <button
          onClick={onTriggerEvaluation}
          className="w-full flex items-center justify-center gap-1.5 rounded-lg bg-white text-slate-900 hover:bg-slate-100 py-2.5 px-4 text-xs font-semibold transition"
        >
          <Play className="h-3.5 w-3.5 text-slate-900 fill-slate-900" />
          <span>Inject Context &amp; Start User Ceremony</span>
        </button>
      </div>

    </div>
  );
}
