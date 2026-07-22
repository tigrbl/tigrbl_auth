/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { 
  Shield, 
  Users, 
  Settings, 
  FileCode, 
  Server, 
  AlertTriangle, 
  CheckCircle2, 
  Clock, 
  Play, 
  UserPlus, 
  X,
  Plus,
  RefreshCw,
  Cpu,
  Terminal,
  Activity,
  Heart,
  HelpCircle,
  Copy,
  ChevronRight,
  UserCheck
} from 'lucide-react';

import { 
  MfaFactor, 
  MfaPolicy, 
  UserPosture, 
  AuditEvent, 
  FactorClass,
  FactorType
} from './types';

import { 
  INITIAL_FACTORS, 
  INITIAL_POLICIES, 
  INITIAL_USER_POSTURES, 
  INITIAL_PROVIDER_HEALTH, 
  INITIAL_AUDIT_EVENTS,
  getStoredState,
  setStoredState
} from './mockData';

import CeremonyShell from './components/CeremonyShell';
import MyAuthenticators from './components/MyAuthenticators';
import TenantPolicyAdmin from './components/TenantPolicyAdmin';

interface Toast {
  id: string;
  message: string;
  type: 'success' | 'failure' | 'warning' | 'info';
}

export default function App() {
  // --- STATE CORE ---
  const [currentTab, setCurrentTab] = useState<'dashboard' | 'ceremony' | 'authenticators' | 'policy' | 'audit'>(() => {
    return getStoredState<'dashboard' | 'ceremony' | 'authenticators' | 'policy' | 'audit'>('currentTab', 'dashboard');
  });

  const [policy, setPolicy] = useState<MfaPolicy>(() => {
    return getStoredState<MfaPolicy>('policy', INITIAL_POLICIES[0]);
  });

  const [users, setUsers] = useState<UserPosture[]>(() => {
    return getStoredState<UserPosture[]>('users', INITIAL_USER_POSTURES);
  });

  const [activeUserId, setActiveUserId] = useState<string>(() => {
    return getStoredState<string>('activeUserId', 'u-1');
  });

  const [auditEvents, setAuditEvents] = useState<AuditEvent[]>(() => {
    return getStoredState<AuditEvent[]>('auditEvents', INITIAL_AUDIT_EVENTS);
  });

  const [providerHealth, setProviderHealth] = useState<Record<string, 'operational' | 'degraded' | 'outage'>>(() => {
    const saved = localStorage.getItem('mfa_console_providerHealth');
    if (saved) {
      try { return JSON.parse(saved); } catch (e) {}
    }
    return {
      passkey: 'operational',
      security_key: 'operational',
      totp: 'operational',
      push: 'operational',
      email_otp: 'degraded',
    };
  });

  // --- INTERACTIVE ACTIVE STATE ---
  const [activeScenario, setActiveScenario] = useState<{
    id: string;
    name: string;
    purpose: string;
    requiredClasses: FactorClass[];
  } | null>(null);

  const [toasts, setToasts] = useState<Toast[]>([]);
  const [auditSearch, setAuditSearch] = useState('');
  const [auditTypeFilter, setAuditTypeFilter] = useState('ALL');
  const [auditStatusFilter, setAuditStatusFilter] = useState('ALL');

  // Sync state to local storage on changes
  useEffect(() => {
    setStoredState('currentTab', currentTab);
  }, [currentTab]);

  useEffect(() => {
    setStoredState('policy', policy);
  }, [policy]);

  useEffect(() => {
    setStoredState('users', users);
  }, [users]);

  useEffect(() => {
    setStoredState('activeUserId', activeUserId);
  }, [activeUserId]);

  useEffect(() => {
    setStoredState('auditEvents', auditEvents);
  }, [auditEvents]);

  useEffect(() => {
    localStorage.setItem('mfa_console_providerHealth', JSON.stringify(providerHealth));
  }, [providerHealth]);

  // Derived Active User
  const activeUser = users.find(u => u.id === activeUserId) || users[0];

  // --- NOTIFICATION ENGINE ---
  const triggerToast = (message: string, type: Toast['type'] = 'info') => {
    const newToast: Toast = { id: `${Date.now()}-${Math.random()}`, message, type };
    setToasts(prev => [...prev, newToast]);
    setTimeout(() => {
      setToasts(prev => prev.filter(t => t.id !== newToast.id));
    }, 4500);
  };

  // --- AUDIT EVENT ENGINE ---
  const addAuditEvent = (event: Omit<AuditEvent, 'id' | 'timestamp'>) => {
    const newEvent: AuditEvent = {
      ...event,
      id: `evt-${Date.now()}-${Math.random()}`,
      timestamp: new Date().toISOString(),
    };
    const updated = [newEvent, ...auditEvents];
    setAuditEvents(updated);
    triggerToast(event.detail, event.status === 'success' ? 'success' : event.status === 'failure' ? 'failure' : event.status === 'warning' ? 'warning' : 'info');
  };

  // --- AUTHENTICATOR EVENT HANDLERS ---
  const handleAddFactor = (userId: string, newFactor: Omit<MfaFactor, 'id' | 'enrolledAt'>) => {
    const factorWithId: MfaFactor = {
      ...newFactor,
      id: `f-${Date.now()}`,
      enrolledAt: new Date().toISOString(),
    };

    const updatedUsers = users.map(user => {
      if (user.id === userId) {
        const updatedFactors = [...user.factors, factorWithId];
        return {
          ...user,
          factors: updatedFactors,
          factorsCount: updatedFactors.length,
          enrollmentStatus: updatedFactors.length >= 3 
            ? 'fully_enrolled' 
            : updatedFactors.length >= 1 
              ? 'partially_enrolled' 
              : 'no_enrollment' as any,
        };
      }
      return user;
    });

    setUsers(updatedUsers);
  };

  const handleRemoveFactor = (userId: string, factorId: string) => {
    const updatedUsers = users.map(user => {
      if (user.id === userId) {
        const updatedFactors = user.factors.filter(f => f.id !== factorId);
        return {
          ...user,
          factors: updatedFactors,
          factorsCount: updatedFactors.length,
          enrollmentStatus: updatedFactors.length >= 3 
            ? 'fully_enrolled' 
            : updatedFactors.length >= 1 
              ? 'partially_enrolled' 
              : 'no_enrollment' as any,
        };
      }
      return user;
    });

    setUsers(updatedUsers);
  };

  const handleUpdateFactor = (userId: string, factorId: string, updates: Partial<MfaFactor>) => {
    const updatedUsers = users.map(user => {
      if (user.id === userId) {
        const updatedFactors = user.factors.map(f => {
          if (f.id === factorId) {
            return { ...f, ...updates };
          }
          return f;
        });
        return {
          ...user,
          factors: updatedFactors,
        };
      }
      return user;
    });

    setUsers(updatedUsers);
  };

  const handleUpdatePolicy = (updates: Partial<MfaPolicy>) => {
    setPolicy(prev => ({
      ...prev,
      ...updates
    }));
    triggerToast(`Tenant security policy updated to Version ${updates.version || policy.version}`, 'success');
  };

  // --- DEMO UTILITIES ---
  const handleSimulateAttack = () => {
    // Inject failed adversary log
    addAuditEvent({
      eventType: 'SECURITY_THREAT',
      subject: activeUser.email,
      status: 'failure',
      detail: `Adversary brute-force bypass attempt blocked. Session IP flagged for suspicious SSH rotation.`,
      ipAddress: '198.51.100.72',
      userAgent: 'Hydra SSH brute-force client/v9.5',
    });
    triggerToast('Simulated brute-force attack successfully detected and blocked.', 'failure');
  };

  const triggerStepUp = (scenarioId: string) => {
    const scenarios = [
      {
        id: 'signin',
        name: 'Regular Console Login',
        purpose: 'Administrator Dashboard Sign-in Assurance',
        requiredClasses: policy.requiredClasses,
      },
      {
        id: 'wire',
        name: 'Sensitive Treasury Fund Transfer',
        purpose: 'High-Value Wire Authorization ($120,000 to external routing)',
        requiredClasses: ['Possession', 'Knowledge', 'Inherence'] as FactorClass[],
      },
      {
        id: 'ssh',
        name: 'Root SSH Key Injection',
        purpose: 'Production Kubernetes Cluster API configuration step-up',
        requiredClasses: ['Possession', 'Inherence'] as FactorClass[],
      }
    ];

    const found = scenarios.find(s => s.id === scenarioId);
    if (found) {
      setActiveScenario(found);
      setCurrentTab('ceremony');
      addAuditEvent({
        eventType: 'CEREMONY_START',
        subject: activeUser.email,
        status: 'info',
        detail: `Step-up ceremony requested for action: "${found.name}"`,
        ipAddress: '192.168.1.144',
        userAgent: navigator.userAgent,
      });
    }
  };

  const handleCeremonySuccess = (amr: string[], auditRef: string) => {
    addAuditEvent({
      eventType: 'CEREMONY_COMPLETE',
      subject: activeUser.email,
      status: 'success',
      detail: `Assurance requirements fully satisfied. AMR context tokens issued: [${amr.join(', ')}]`,
      ipAddress: '192.168.1.144',
      userAgent: navigator.userAgent,
    });
    triggerToast(`Assurance success! Requested authorization token granted.`, 'success');
    
    // Update factor lastUsedAt
    const updatedUsers = users.map(user => {
      if (user.id === activeUserId) {
        const updatedFactors = user.factors.map(f => {
          // If this factor matches some of the issued AMRs
          const matches = amr.some(a => a.toLowerCase().includes(f.type) || (f.type === 'security_key' && a.toLowerCase().includes('hw')));
          if (matches) {
            return { ...f, lastUsedAt: new Date().toISOString() };
          }
          return f;
        });
        return {
          ...user,
          factors: updatedFactors,
          lastMfaTime: new Date().toISOString(),
        };
      }
      return user;
    });
    setUsers(updatedUsers);
    setActiveScenario(null);
    setCurrentTab('dashboard');
  };

  // --- STATS DERIVATIONS ---
  const activeFactorsCount = users.reduce((sum, u) => sum + u.factors.length, 0);
  const complianceStats = (() => {
    let compliant = 0;
    let grace = 0;
    let blocked = 0;

    users.forEach(u => {
      const uFactorTypes = u.factors.map(f => f.type);
      const hasPasskeyOrSecKey = uFactorTypes.some(f => f === 'passkey' || f === 'security_key');
      const hasAllowed = uFactorTypes.some(f => (policy.allowedFactorTypes || []).includes(f as any));

      if (!hasAllowed) {
        if (u.enrollmentStatus === 'grace_period') grace++;
        else blocked++;
      } else if (policy.enforcePhishingResistant && !hasPasskeyOrSecKey) {
        if (u.enrollmentStatus === 'grace_period') grace++;
        else blocked++;
      } else {
        compliant++;
      }
    });

    const total = users.length;
    return {
      compliantPct: Math.round((compliant / total) * 100),
      compliant,
      grace,
      blocked,
      total
    };
  })();

  // --- FILTERED AUDIT TIMELINE ---
  const filteredEvents = auditEvents.filter(e => {
    const matchesSearch = 
      e.eventType.toLowerCase().includes(auditSearch.toLowerCase()) ||
      e.detail.toLowerCase().includes(auditSearch.toLowerCase()) ||
      e.subject.toLowerCase().includes(auditSearch.toLowerCase()) ||
      e.ipAddress.includes(auditSearch);

    const matchesType = auditTypeFilter === 'ALL' || e.eventType === auditTypeFilter;
    const matchesStatus = auditStatusFilter === 'ALL' || e.status === auditStatusFilter;

    return matchesSearch && matchesType && matchesStatus;
  });

  const uniqueEventTypes = Array.from(new Set(auditEvents.map(e => e.eventType)));

  return (
    <div className="min-h-screen bg-slate-50 flex font-sans antialiased text-slate-800">
      
      {/* SIDEBAR RAIL - Modern dark high-contrast theme */}
      <aside className="w-64 bg-slate-900 text-slate-200 flex flex-col border-r border-slate-950 shrink-0 select-none">
        {/* Core Branding */}
        <div className="p-5 border-b border-slate-800 flex items-center gap-3 bg-slate-950">
          <div className="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center shadow-md">
            <Shield className="w-4.5 h-4.5 text-white" />
          </div>
          <div>
            <h1 className="text-xs font-bold tracking-widest text-slate-100 uppercase">AMR Cockpit</h1>
            <p className="text-[9px] text-slate-400 font-mono">ASSURANCE POLICY V{policy.version.toFixed(1)}</p>
          </div>
        </div>

        {/* User Identity Simulator Hub */}
        <div className="p-4 border-b border-slate-800 bg-slate-900/40">
          <label className="text-[9px] font-bold text-slate-500 uppercase tracking-widest block mb-1.5">Simulation Active User</label>
          <div className="flex items-center gap-2.5 p-2 rounded-lg bg-slate-950 border border-slate-800">
            <div className="w-8 h-8 rounded-full bg-slate-800 flex items-center justify-center border border-slate-700 font-bold text-xs text-indigo-400">
              {activeUser.name.split(' ').map(s => s[0]).join('')}
            </div>
            <div className="min-w-0 flex-1">
              <div className="text-[11px] font-bold text-slate-200 truncate">{activeUser.name}</div>
              <div className="text-[9px] text-slate-500 font-mono truncate">{activeUser.email}</div>
            </div>
          </div>
          <div className="mt-2 flex gap-1 justify-between">
            <span className="text-[9px] font-bold text-slate-400 uppercase">Status:</span>
            <span className={`text-[9px] font-bold font-mono px-1 rounded uppercase ${
              activeUser.enrollmentStatus === 'fully_enrolled' ? 'text-emerald-400 bg-emerald-950/40' :
              activeUser.enrollmentStatus === 'partially_enrolled' ? 'text-blue-400 bg-blue-950/40' :
              activeUser.enrollmentStatus === 'grace_period' ? 'text-amber-400 bg-amber-950/40' :
              'text-rose-400 bg-rose-950/40'
            }`}>
              {activeUser.enrollmentStatus.replace('_', ' ')}
            </span>
          </div>
        </div>

        {/* Navigation Tabs */}
        <nav className="p-3 flex-1 space-y-1">
          <button 
            onClick={() => { setCurrentTab('dashboard'); setActiveScenario(null); }}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
              currentTab === 'dashboard' 
                ? 'bg-indigo-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Cpu className="w-4 h-4" />
              <span>Assurance Console</span>
            </div>
            <ChevronRight className={`w-3 h-3 opacity-60 transition-transform ${currentTab === 'dashboard' ? 'rotate-90 text-white' : ''}`} />
          </button>

          <button 
            onClick={() => setCurrentTab('ceremony')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
              currentTab === 'ceremony' 
                ? 'bg-indigo-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Play className="w-4 h-4" />
              <span>Step-Up Ceremony</span>
            </div>
            {activeScenario && <span className="w-2 h-2 rounded-full bg-rose-500 animate-ping shrink-0" />}
            <ChevronRight className={`w-3 h-3 opacity-60 transition-transform ${currentTab === 'ceremony' ? 'rotate-90 text-white' : ''}`} />
          </button>

          <button 
            onClick={() => setCurrentTab('authenticators')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
              currentTab === 'authenticators' 
                ? 'bg-indigo-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Users className="w-4 h-4" />
              <span>User Authenticators</span>
            </div>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold">
              {activeUser.factors.length}
            </span>
          </button>

          <button 
            onClick={() => setCurrentTab('policy')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
              currentTab === 'policy' 
                ? 'bg-indigo-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Settings className="w-4 h-4" />
              <span>Global Policy Editor</span>
            </div>
            <ChevronRight className={`w-3 h-3 opacity-60 transition-transform ${currentTab === 'policy' ? 'rotate-90 text-white' : ''}`} />
          </button>

          <button 
            onClick={() => setCurrentTab('audit')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
              currentTab === 'audit' 
                ? 'bg-indigo-600 text-white shadow-md' 
                : 'text-slate-400 hover:text-slate-100 hover:bg-slate-800/60'
            }`}
          >
            <div className="flex items-center gap-2.5">
              <Terminal className="w-4 h-4" />
              <span>Audit logs timeline</span>
            </div>
            <span className="text-[10px] font-mono px-1.5 py-0.5 rounded-full bg-slate-800 text-slate-300 font-bold">
              {auditEvents.length}
            </span>
          </button>
        </nav>

        {/* Live Attack Simulator Trigger */}
        <div className="p-4 border-t border-slate-800 bg-slate-950/60 flex flex-col gap-2 shrink-0">
          <div className="text-[9px] font-bold text-slate-500 uppercase tracking-widest">Defensive Testing</div>
          <button 
            onClick={handleSimulateAttack}
            className="w-full py-2 bg-slate-800 hover:bg-rose-900/30 text-rose-400 hover:text-rose-200 border border-slate-700 hover:border-rose-800 rounded-lg text-[10px] font-bold tracking-wider uppercase transition-all flex items-center justify-center gap-1.5 shadow-sm active:scale-98"
          >
            <AlertTriangle className="w-3.5 h-3.5" />
            Simulate Attack
          </button>
        </div>
      </aside>

      {/* MAIN CONTAINER */}
      <main className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        
        {/* TOP HUB BAR */}
        <header className="h-16 bg-white border-b border-slate-200 px-6 flex items-center justify-between shrink-0 select-none">
          <div className="flex items-center gap-3">
            <Server className="w-4 h-4 text-slate-400" />
            <div className="text-xs font-semibold text-slate-500">Tenant: <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-slate-700 text-[10px]">acme-corp-secure</code></div>
            <span className="w-1 h-1 rounded-full bg-slate-300" />
            <div className="flex items-center gap-1 text-[11px] text-slate-500 font-medium">
              <span className="w-2 h-2 rounded-full bg-emerald-500 animate-pulse" />
              <span>Signing Engine FIPS-140-3 Active</span>
            </div>
          </div>

          {/* Quick Active Scenario Indicator */}
          {activeScenario && (
            <div className="flex items-center gap-2 bg-rose-50 border border-rose-200/60 px-3 py-1.5 rounded-lg text-[11px] font-semibold text-rose-700 animate-pulse">
              <span className="w-1.5 h-1.5 rounded-full bg-rose-500" />
              <span>Step-Up Active: {activeScenario.name}</span>
              <button onClick={() => setActiveScenario(null)} className="ml-1 p-0.5 hover:bg-rose-100 rounded text-rose-500 hover:text-rose-700 transition-colors">
                <X className="w-3 h-3" />
              </button>
            </div>
          )}

          {/* Profile Switcher Quick Action */}
          <div className="flex items-center gap-2">
            <span className="text-[10px] font-bold text-slate-400 uppercase">Sim User:</span>
            <select 
              value={activeUserId}
              onChange={(e) => {
                const uid = e.target.value;
                setActiveUserId(uid);
                const matchedUser = users.find(u => u.id === uid);
                if (matchedUser) {
                  triggerToast(`Simulated workspace profile switched to ${matchedUser.name}`, 'info');
                }
              }}
              className="text-xs bg-slate-100 border border-slate-200 hover:bg-slate-200 text-slate-700 font-bold rounded-lg py-1 px-2.5 cursor-pointer outline-none transition-colors"
            >
              {users.map(u => (
                <option key={u.id} value={u.id}>{u.name} ({u.factors.length} keys)</option>
              ))}
            </select>
          </div>
        </header>

        {/* WORKSPACE CONTENT AREA */}
        <div className="p-6 max-w-7xl w-full mx-auto space-y-6">
          
          {/* TAB 1: COCKPIT COCKPIT COCKPIT */}
          {currentTab === 'dashboard' && (
            <div className="space-y-6 animate-fade-in">
              
              {/* SYSTEM HEALTH STATS */}
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="bg-white p-4.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Tenant Compliance Rate</div>
                    <div className="text-2xl font-bold text-slate-900 mt-1">{complianceStats.compliantPct}%</div>
                    <p className="text-[9px] text-slate-400 mt-1.5 flex items-center gap-1 font-mono">
                      <span className="w-1.5 h-1.5 rounded-full bg-emerald-500" />
                      {complianceStats.compliant} of {complianceStats.total} users compliant
                    </p>
                  </div>
                  <div className={`w-12 h-12 rounded-lg flex items-center justify-center font-bold text-sm ${
                    complianceStats.compliantPct >= 75 ? 'bg-emerald-50 text-emerald-600' : 'bg-amber-50 text-amber-600'
                  }`}>
                    {complianceStats.compliantPct}%
                  </div>
                </div>

                <div className="bg-white p-4.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Registered Key Tokens</div>
                    <div className="text-2xl font-bold text-slate-900 mt-1">{activeFactorsCount}</div>
                    <p className="text-[9px] text-slate-400 mt-1.5 font-mono">
                      Avg {Math.round((activeFactorsCount / complianceStats.total) * 10) / 10} keys per user
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-indigo-50 rounded-lg flex items-center justify-center text-indigo-600">
                    <Shield className="w-5 h-5" />
                  </div>
                </div>

                <div className="bg-white p-4.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Assurance Standard</div>
                    <div className="text-xs font-bold text-slate-900 mt-2 truncate max-w-[150px]">
                      {policy.requiredClasses.join(' + ') || 'None (Insecure)'}
                    </div>
                    <p className="text-[9px] text-slate-400 mt-1 flex items-center gap-1 font-mono">
                      {policy.enforcePhishingResistant ? '🛡️ FIDO2 Enforced' : '⚠️ OTP Allowed'}
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-slate-50 rounded-lg flex items-center justify-center text-slate-600">
                    <Cpu className="w-5 h-5" />
                  </div>
                </div>

                <div className="bg-white p-4.5 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
                  <div>
                    <div className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Core Hardware HSM</div>
                    <div className="text-2xl font-bold text-slate-900 mt-1">Operational</div>
                    <p className="text-[9px] text-slate-400 mt-1.5 font-mono">
                      Latency: 2ms | Throughput 140/s
                    </p>
                  </div>
                  <div className="w-12 h-12 bg-emerald-50 rounded-lg flex items-center justify-center text-emerald-600">
                    <Activity className="w-5 h-5" />
                  </div>
                </div>
              </div>

              {/* THREE-COLUMN SUBPANEL ROW */}
              <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                
                {/* COLUMN 1: INTERACTIVE USER DIRECTORY POSTURES (lg:col-span-8) */}
                <section className="lg:col-span-8 bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden">
                  <div className="p-4 border-b border-slate-200 flex items-center justify-between bg-slate-50/50">
                    <div>
                      <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Tenant Identity Directories & Compliance</h3>
                      <p className="text-[10px] text-slate-400 mt-0.5">Simulate individual workspace members and initiate dedicated step-up ceremonies</p>
                    </div>
                    <span className="text-[9px] font-bold font-mono text-slate-400 bg-slate-200/60 px-1.5 py-0.5 rounded-full">
                      {users.length} TOTAL SIMULATED
                    </span>
                  </div>

                  {/* Users Directory Table */}
                  <div className="divide-y divide-slate-150 flex-1">
                    {users.map(user => {
                      // Check user specific compliance status under policy
                      const uFactorTypes = user.factors.map(f => f.type);
                      const hasPasskeyOrSecKey = uFactorTypes.some(f => f === 'passkey' || f === 'security_key');
                      const hasAllowed = uFactorTypes.some(f => (policy.allowedFactorTypes || []).includes(f as any));
                      
                      let complianceStr = 'COMPLIANT';
                      let colorClass = 'bg-emerald-50 text-emerald-700 border-emerald-100';
                      if (!hasAllowed) {
                        if (user.enrollmentStatus === 'grace_period') {
                          complianceStr = 'GRACE PERIOD';
                          colorClass = 'bg-amber-50 text-amber-700 border-amber-100';
                        } else {
                          complianceStr = 'NON-COMPLIANT';
                          colorClass = 'bg-rose-50 text-rose-700 border-rose-100';
                        }
                      } else if (policy.enforcePhishingResistant && !hasPasskeyOrSecKey) {
                        if (user.enrollmentStatus === 'grace_period') {
                          complianceStr = 'GRACE PERIOD';
                          colorClass = 'bg-amber-50 text-amber-700 border-amber-100';
                        } else {
                          complianceStr = 'NON-COMPLIANT';
                          colorClass = 'bg-rose-50 text-rose-700 border-rose-100';
                        }
                      }

                      return (
                        <div key={user.id} className="p-4 flex items-center justify-between hover:bg-slate-50/50 transition-colors">
                          <div className="flex items-center gap-3">
                            <div className="w-9 h-9 rounded-full bg-slate-100 text-slate-600 border border-slate-200 font-bold text-xs flex items-center justify-center">
                              {user.name.split(' ').map(s => s[0]).join('')}
                            </div>
                            <div>
                              <div className="text-xs font-bold text-slate-800 flex items-center gap-2">
                                {user.name}
                                {user.id === activeUserId && (
                                  <span className="text-[8px] bg-indigo-50 text-indigo-600 px-1 py-0.2 rounded font-extrabold tracking-wider border border-indigo-100 uppercase">ACTIVE SIM</span>
                                )}
                              </div>
                              <div className="text-[10px] text-slate-400 font-mono mt-0.5">{user.email}</div>
                              <div className="mt-1.5 flex gap-1 items-center flex-wrap">
                                {user.factors.map(f => (
                                  <span key={f.id} className="text-[8px] font-mono font-semibold px-1 py-0.2 border border-slate-200/60 bg-slate-50 text-slate-500 rounded">
                                    {f.name}
                                  </span>
                                ))}
                                {user.factors.length === 0 && (
                                  <span className="text-[8px] font-mono text-rose-500 italic">No credentials bound</span>
                                )}
                              </div>
                            </div>
                          </div>

                          <div className="flex items-center gap-3 shrink-0">
                            <div className="text-right">
                              <span className={`px-2 py-0.5 text-[8px] font-extrabold rounded uppercase border ${colorClass}`}>
                                {complianceStr}
                              </span>
                              <div className="text-[8px] text-slate-400 font-mono mt-1">
                                Last: {user.lastMfaTime ? new Date(user.lastMfaTime).toLocaleTimeString() : 'Never'}
                              </div>
                            </div>

                            {/* Row Action Panel */}
                            <div className="flex flex-col gap-1">
                              <button 
                                onClick={() => {
                                  setActiveUserId(user.id);
                                  setCurrentTab('authenticators');
                                }}
                                className="px-2 py-1 text-[9px] font-bold bg-white hover:bg-slate-100 border border-slate-200 text-slate-600 rounded-lg transition-all"
                              >
                                Keys
                              </button>
                              <button 
                                onClick={() => {
                                  setActiveUserId(user.id);
                                  triggerStepUp('signin');
                                }}
                                className="px-2 py-1 text-[9px] font-bold bg-slate-900 hover:bg-indigo-600 text-white hover:border-indigo-600 rounded-lg transition-all flex items-center justify-center gap-0.5"
                              >
                                <Play className="w-2 h-2 fill-white text-white" />
                                Login
                              </button>
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>
                </section>

                {/* COLUMN 2: INTEGRATOR PROVIDER INTERRUPTS (lg:col-span-4) */}
                <section className="lg:col-span-4 space-y-6">
                  
                  {/* Provider Health Interrupt Switcher */}
                  <div className="bg-white rounded-xl border border-slate-200 shadow-sm p-4.5 space-y-4">
                    <div>
                      <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Provider Orchestration Control</h3>
                      <p className="text-[10px] text-slate-400 mt-0.5">Toggle live failures to test fallback policy resilience during ceremonies</p>
                    </div>

                    <div className="space-y-3">
                      {[
                        { key: 'passkey', name: 'FIDO2 Passkeys/WebAuthn', desc: 'Secure biometrics & platform modules' },
                        { key: 'totp', name: 'RFC-6238 TOTP Engine', desc: 'Google/Microsoft Authenticator' },
                        { key: 'push', name: 'Transactional Push Service', desc: 'Duo callback notifications' },
                        { key: 'email_otp', name: 'Corporate SMTP OTP Gate', desc: 'Email Pins delivered in cleartext' },
                      ].map((item) => {
                        const status = providerHealth[item.key] || 'operational';
                        return (
                          <div key={item.key} className="p-3 border border-slate-150 rounded-lg bg-slate-50/50 flex flex-col gap-2">
                            <div className="flex items-start justify-between">
                              <div>
                                <span className="text-[11px] font-bold text-slate-800">{item.name}</span>
                                <div className="text-[9px] text-slate-400 leading-tight mt-0.5">{item.desc}</div>
                              </div>

                              <span className={`text-[8px] font-extrabold uppercase font-mono px-1 rounded-sm border shrink-0 ${
                                status === 'operational' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                                status === 'degraded' ? 'bg-amber-50 text-amber-700 border-amber-100' :
                                'bg-rose-50 text-rose-700 border-rose-100'
                              }`}>
                                {status}
                              </span>
                            </div>

                            {/* Mini Toggle Bar */}
                            <div className="flex gap-1">
                              {['operational', 'degraded', 'outage'].map((st) => (
                                <button
                                  key={st}
                                  onClick={() => {
                                    setProviderHealth(prev => ({ ...prev, [item.key]: st as any }));
                                    addAuditEvent({
                                      eventType: 'PROVIDER_STATE_CHANGED',
                                      subject: 'admin@acme.com',
                                      status: st === 'operational' ? 'info' : st === 'degraded' ? 'warning' : 'failure',
                                      detail: `Factor class provider "${item.key}" toggled manually to state "${st.toUpperCase()}".`,
                                      ipAddress: '127.0.0.1',
                                      userAgent: 'System Controller Console',
                                    });
                                  }}
                                  className={`flex-1 py-1 rounded text-[8px] font-bold uppercase border transition-all ${
                                    status === st 
                                      ? 'bg-slate-900 border-slate-900 text-white shadow-xs' 
                                      : 'bg-white border-slate-200 text-slate-500 hover:bg-slate-100'
                                  }`}
                                >
                                  {st.slice(0, 4)}
                                </button>
                              ))}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>

                  {/* Scenario Play Panel */}
                  <div className="bg-slate-900 text-slate-200 rounded-xl p-4.5 space-y-4 shadow-md border border-slate-950">
                    <div>
                      <h3 className="text-xs font-bold text-slate-100 uppercase tracking-wider flex items-center gap-1.5">
                        <Play className="w-3.5 h-3.5 fill-indigo-400 text-indigo-400" />
                        Trigger step-up simulator
                      </h3>
                      <p className="text-[10px] text-slate-400 mt-0.5 leading-tight">Prompt authentication verification ceremonies on the active simulated profile</p>
                    </div>

                    <div className="space-y-2.5">
                      <button 
                        onClick={() => triggerStepUp('signin')}
                        className="w-full p-3 bg-slate-800 hover:bg-slate-750 rounded-lg text-left border border-slate-700 hover:border-slate-600 transition-all block group"
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-bold text-slate-200 group-hover:text-indigo-400">1. Console Session Sign-in</span>
                          <span className="text-[8px] font-mono text-indigo-400 font-extrabold uppercase">Policy required</span>
                        </div>
                        <div className="text-[9px] text-slate-400 mt-1">Normal portal login. Enforces {policy.requiredClasses.join(' + ')} verification.</div>
                      </button>

                      <button 
                        onClick={() => triggerStepUp('wire')}
                        className="w-full p-3 bg-slate-800 hover:bg-slate-750 rounded-lg text-left border border-slate-700 hover:border-slate-600 transition-all block group"
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-bold text-slate-200 group-hover:text-indigo-400">2. External Wire Transfer ($50k+)</span>
                          <span className="text-[8px] font-mono text-emerald-400 font-extrabold uppercase">P0 High Assurance</span>
                        </div>
                        <div className="text-[9px] text-slate-400 mt-1">Strict wire authorization. Demands Knowledge + Possession + Inherence factor classes.</div>
                      </button>

                      <button 
                        onClick={() => triggerStepUp('ssh')}
                        className="w-full p-3 bg-slate-800 hover:bg-slate-750 rounded-lg text-left border border-slate-700 hover:border-slate-600 transition-all block group"
                      >
                        <div className="flex justify-between items-center">
                          <span className="text-[11px] font-bold text-slate-200 group-hover:text-indigo-400">3. Root SSH Key Injection</span>
                          <span className="text-[8px] font-mono text-amber-400 font-extrabold uppercase">FIDO2 SECURE-ONLY</span>
                        </div>
                        <div className="text-[9px] text-slate-400 mt-1">Prod cluster access. Mandates phishing-resistant hardware key verification.</div>
                      </button>
                    </div>
                  </div>
                </section>
              </div>

              {/* RECENT AUDIT TIMELINE MINI PANEL */}
              <section className="bg-white rounded-xl border border-slate-200 shadow-sm p-4.5 space-y-4">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-xs font-bold text-slate-800 uppercase tracking-wider">Live Security Audit Ledger</h3>
                    <p className="text-[10px] text-slate-400 mt-0.5">Real-time telemetry event records for all verification ceremonies, policy updates, and credential changes</p>
                  </div>
                  <button 
                    onClick={() => setCurrentTab('audit')}
                    className="text-[10px] font-bold text-indigo-600 hover:text-indigo-800 transition-colors"
                  >
                    View Filterable Ledger →
                  </button>
                </div>

                <div className="space-y-2 border border-slate-100 rounded-lg overflow-hidden divide-y divide-slate-100 max-h-[220px] overflow-y-auto font-mono text-[10px]">
                  {auditEvents.slice(0, 5).map((e) => (
                    <div key={e.id} className="p-2.5 flex justify-between gap-4 bg-slate-50/20 hover:bg-slate-50 transition-colors">
                      <div className="flex gap-2 min-w-0">
                        <span className={`px-1 py-0.2 rounded font-bold uppercase shrink-0 text-[8px] h-fit border ${
                          e.status === 'success' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                          e.status === 'warning' ? 'bg-amber-50 text-amber-700 border-amber-100' :
                          e.status === 'failure' ? 'bg-rose-50 text-rose-700 border-rose-100' :
                          'bg-slate-100 text-slate-600 border-slate-200'
                        }`}>
                          {e.status}
                        </span>
                        <div className="truncate text-slate-700">
                          <span className="font-semibold text-slate-900">[{e.eventType}]</span> {e.detail}
                        </div>
                      </div>

                      <div className="flex gap-3 shrink-0 text-slate-400 font-normal">
                        <span>{e.subject}</span>
                        <span>{new Date(e.timestamp).toLocaleTimeString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>

            </div>
          )}

          {/* TAB 2: ACTIVE CEREMONY SIMULATOR */}
          {currentTab === 'ceremony' && (
            <div className="space-y-6">
              {activeScenario ? (
                <div className="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                  <div className="mb-6 flex justify-between items-start border-b border-slate-100 pb-4">
                    <div>
                      <div className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">Active Verification Ceremony</div>
                      <h2 className="text-lg font-bold text-slate-900 mt-1">{activeScenario.name}</h2>
                      <p className="text-xs text-slate-500 mt-1 italic">↳ Action Purpose: "{activeScenario.purpose}"</p>
                    </div>
                    <button 
                      onClick={() => {
                        addAuditEvent({
                          eventType: 'CEREMONY_CANCELLED',
                          subject: activeUser.email,
                          status: 'warning',
                          detail: `Verification ceremony cancelled by user for action: "${activeScenario.name}"`,
                          ipAddress: '192.168.1.144',
                          userAgent: navigator.userAgent,
                        });
                        setActiveScenario(null);
                        setCurrentTab('dashboard');
                      }}
                      className="px-3 py-1.5 border border-slate-200 hover:bg-slate-50 text-slate-600 font-bold rounded-lg text-[10px] uppercase transition-colors"
                    >
                      Abrupt Cancel
                    </button>
                  </div>

                  <CeremonyShell 
                    policy={{
                      ...policy,
                      requiredClasses: activeScenario.requiredClasses
                    }}
                    enrolledFactors={activeUser.factors}
                    onCeremonyComplete={handleCeremonySuccess}
                    onCancel={() => {
                      addAuditEvent({
                        eventType: 'CEREMONY_CANCELLED',
                        subject: activeUser.email,
                        status: 'warning',
                        detail: `Assurance requirements incomplete. Ceremony aborted.`,
                        ipAddress: '192.168.1.144',
                        userAgent: navigator.userAgent,
                      });
                      setActiveScenario(null);
                      setCurrentTab('dashboard');
                    }}
                    addAuditEvent={addAuditEvent}
                    providerHealth={providerHealth}
                  />
                </div>
              ) : (
                <div className="bg-white rounded-xl border border-slate-200 p-8 text-center shadow-sm max-w-xl mx-auto space-y-5">
                  <div className="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-full flex items-center justify-center mx-auto border border-indigo-100 shadow-xs">
                    <Shield className="w-6 h-6 animate-pulse" />
                  </div>
                  <div>
                    <h2 className="text-base font-bold text-slate-800">No Verification Ceremony Active</h2>
                    <p className="text-xs text-slate-500 mt-1 max-w-sm mx-auto">
                      Step-up assurance ceremonies are triggered dynamically based on administrative risk factors. Choose a simulation scenario to proceed.
                    </p>
                  </div>

                  <div className="grid grid-cols-1 gap-2 text-left">
                    <button 
                      onClick={() => triggerStepUp('signin')}
                      className="p-3 border border-slate-150 rounded-lg hover:border-indigo-500 hover:bg-indigo-50/10 transition-colors flex justify-between items-center group text-xs"
                    >
                      <div>
                        <strong className="font-bold text-slate-800 block group-hover:text-indigo-600">Standard Console Sign-in</strong>
                        <span className="text-[10px] text-slate-400 mt-0.5 block">Requires active policy criteria ({policy.requiredClasses.join(' + ')}).</span>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-0.5 transition-transform" />
                    </button>

                    <button 
                      onClick={() => triggerStepUp('wire')}
                      className="p-3 border border-slate-150 rounded-lg hover:border-indigo-500 hover:bg-indigo-50/10 transition-colors flex justify-between items-center group text-xs"
                    >
                      <div>
                        <strong className="font-bold text-slate-800 block group-hover:text-indigo-600">Treasury Fund Wire Transfer</strong>
                        <span className="text-[10px] text-slate-400 mt-0.5 block">Demands multi-factor class assurance: Possession, Knowledge, and Inherence.</span>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-0.5 transition-transform" />
                    </button>

                    <button 
                      onClick={() => triggerStepUp('ssh')}
                      className="p-3 border border-slate-150 rounded-lg hover:border-indigo-500 hover:bg-indigo-50/10 transition-colors flex justify-between items-center group text-xs"
                    >
                      <div>
                        <strong className="font-bold text-slate-800 block group-hover:text-indigo-600">Kubernetes SSH Key Injection</strong>
                        <span className="text-[10px] text-slate-400 mt-0.5 block">Strictly mandates phishing-resistant biometric passkey or security keys.</span>
                      </div>
                      <ChevronRight className="w-4 h-4 text-slate-400 group-hover:translate-x-0.5 transition-transform" />
                    </button>
                  </div>
                </div>
              )}
            </div>
          )}

          {/* TAB 3: USER AUTHENTICATOR DEVICE MANAGER */}
          {currentTab === 'authenticators' && (
            <div className="space-y-6">
              
              <div className="bg-indigo-900 text-indigo-100 rounded-xl p-5 shadow-md flex items-center justify-between border border-indigo-950 select-none">
                <div>
                  <div className="text-[9px] font-extrabold uppercase tracking-widest text-indigo-300">Identity Directory Hub</div>
                  <h2 className="text-lg font-bold text-white mt-1">Credentials Inventory: {activeUser.name}</h2>
                  <p className="text-[11px] text-indigo-200 mt-0.5">Manage enrolled security keys, biometrics, software tokens, and emergency recovery codes for simulation.</p>
                </div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold">Manage Profile:</span>
                  <select 
                    value={activeUserId}
                    onChange={(e) => setActiveUserId(e.target.value)}
                    className="text-xs bg-indigo-950 border border-indigo-800 text-indigo-100 font-bold rounded-lg py-1.5 px-3 cursor-pointer outline-none transition-colors"
                  >
                    {users.map(u => (
                      <option key={u.id} value={u.id}>{u.name}</option>
                    ))}
                  </select>
                </div>
              </div>

              <MyAuthenticators 
                factors={activeUser.factors}
                onAddFactor={(newF) => handleAddFactor(activeUserId, newF)}
                onRemoveFactor={(id) => handleRemoveFactor(activeUserId, id)}
                onUpdateFactor={(id, updates) => handleUpdateFactor(activeUserId, id, updates)}
                addAuditEvent={addAuditEvent}
              />
            </div>
          )}

          {/* TAB 4: TENANT GLOBAL POLICY EDITOR */}
          {currentTab === 'policy' && (
            <div className="space-y-6">
              <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-xs flex items-center justify-between">
                <div>
                  <h2 className="text-sm font-extrabold text-slate-800 uppercase tracking-wider">Tenant-wide policy controls</h2>
                  <p className="text-[11px] text-slate-500 mt-0.5">Set mandatory criteria for second-factor enrollment, step-ups, and biometric compliance.</p>
                </div>
                <span className="text-xs font-bold font-mono text-indigo-600 bg-indigo-50 border border-indigo-100 px-2.5 py-1 rounded-full">
                  Active policy: Version {policy.version.toFixed(1)}
                </span>
              </div>

              <TenantPolicyAdmin 
                policy={policy}
                onUpdatePolicy={handleUpdatePolicy}
                users={users}
                addAuditEvent={addAuditEvent}
              />
            </div>
          )}

          {/* TAB 5: DEDICATED AUDIT EVENT TIMELINE LEDGER */}
          {currentTab === 'audit' && (
            <div className="bg-white rounded-xl border border-slate-200 shadow-sm flex flex-col overflow-hidden animate-fade-in select-none">
              
              {/* Timeline Header & Filters */}
              <div className="p-5 border-b border-slate-200 bg-slate-50/50 space-y-4">
                <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-3">
                  <div>
                    <h2 className="text-xs font-extrabold text-slate-800 uppercase tracking-widest flex items-center gap-1.5">
                      <Terminal className="w-4 h-4 text-slate-500" />
                      Assurance Event Timeline Log
                    </h2>
                    <p className="text-[10px] text-slate-400 mt-0.5">Cryptographically sequenced chronological records of verified assurance and tenant events.</p>
                  </div>
                  <button 
                    onClick={() => {
                      setAuditEvents(INITIAL_AUDIT_EVENTS);
                      triggerToast('Audit trail reset to baseline events', 'info');
                    }}
                    className="px-3 py-1.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-600 font-semibold rounded-lg text-[10px] transition-colors flex items-center gap-1 self-start md:self-auto shadow-2xs"
                  >
                    <RefreshCw className="w-3 h-3" />
                    Reset Timeline
                  </button>
                </div>

                {/* Filter Controls Row */}
                <div className="grid grid-cols-1 md:grid-cols-4 gap-2.5 pt-1.5">
                  <div className="relative">
                    <input 
                      type="text" 
                      placeholder="Search detail, user, IP..." 
                      value={auditSearch}
                      onChange={(e) => setAuditSearch(e.target.value)}
                      className="w-full bg-white border border-slate-200 text-xs font-semibold rounded-lg pl-3 pr-8 py-2 outline-none focus:border-indigo-500 placeholder:text-slate-400 text-slate-700"
                    />
                    {auditSearch && (
                      <button onClick={() => setAuditSearch('')} className="absolute right-2.5 top-2.5 text-slate-400 hover:text-slate-600">
                        <X className="w-3.5 h-3.5" />
                      </button>
                    )}
                  </div>

                  <div>
                    <select 
                      value={auditTypeFilter}
                      onChange={(e) => setAuditTypeFilter(e.target.value)}
                      className="w-full bg-white border border-slate-200 text-xs font-semibold rounded-lg px-3 py-2 outline-none cursor-pointer text-slate-700"
                    >
                      <option value="ALL">All Event Types</option>
                      {uniqueEventTypes.map(t => (
                        <option key={t} value={t}>{t}</option>
                      ))}
                    </select>
                  </div>

                  <div>
                    <select 
                      value={auditStatusFilter}
                      onChange={(e) => setAuditStatusFilter(e.target.value)}
                      className="w-full bg-white border border-slate-200 text-xs font-semibold rounded-lg px-3 py-2 outline-none cursor-pointer text-slate-700"
                    >
                      <option value="ALL">All Statuses</option>
                      <option value="success">Success</option>
                      <option value="failure">Failure</option>
                      <option value="warning">Warning</option>
                      <option value="info">Info</option>
                    </select>
                  </div>

                  <div className="flex items-center justify-end text-[10px] text-slate-400 font-mono pr-2">
                    Showing {filteredEvents.length} of {auditEvents.length} events
                  </div>
                </div>
              </div>

              {/* Sequential Event List */}
              <div className="divide-y divide-slate-100 overflow-y-auto max-h-[500px]">
                {filteredEvents.map(e => (
                  <div key={e.id} className="p-4 hover:bg-slate-50/50 transition-colors flex flex-col md:flex-row md:items-start justify-between gap-3 text-xs">
                    <div className="flex items-start gap-3">
                      <span className={`px-1.5 py-0.5 rounded text-[8px] font-extrabold uppercase shrink-0 border mt-0.5 ${
                        e.status === 'success' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' :
                        e.status === 'warning' ? 'bg-amber-50 text-amber-700 border-amber-100' :
                        e.status === 'failure' ? 'bg-rose-50 text-rose-700 border-rose-100' :
                        'bg-slate-50 text-slate-600 border-slate-250'
                      }`}>
                        {e.status}
                      </span>
                      <div className="space-y-1">
                        <div className="font-bold text-slate-800 flex items-center gap-2">
                          <span className="text-[11px] font-mono text-indigo-600">[{e.eventType}]</span>
                          <span className="text-[10px] text-slate-400 font-mono font-normal">@{e.ipAddress}</span>
                        </div>
                        <p className="text-slate-600 leading-normal">{e.detail}</p>
                        {e.factorType && (
                          <div className="flex gap-1.5 items-center text-[10px] text-slate-400 font-mono">
                            <span>Factor Class: <strong>{e.factorClass}</strong></span>
                            <span>|</span>
                            <span>Token Type: <strong>{e.factorType.toUpperCase()}</strong></span>
                          </div>
                        )}
                      </div>
                    </div>

                    <div className="text-left md:text-right shrink-0 space-y-0.5 font-mono text-[10px] text-slate-400">
                      <div className="font-bold text-slate-600">{e.subject}</div>
                      <div>{new Date(e.timestamp).toLocaleDateString()} {new Date(e.timestamp).toLocaleTimeString()}</div>
                      <div className="text-[8px] truncate max-w-[200px] text-slate-300">{e.userAgent}</div>
                    </div>
                  </div>
                ))}

                {filteredEvents.length === 0 && (
                  <div className="p-12 text-center text-slate-400">
                    <Terminal className="w-10 h-10 text-slate-200 mx-auto mb-2" />
                    <span className="text-xs font-semibold">Zero matching audit events found.</span>
                  </div>
                )}
              </div>
            </div>
          )}

        </div>
      </main>

      {/* FLOATING TOAST SYSTEM */}
      <div className="fixed bottom-5 right-5 z-50 space-y-2 max-w-sm pointer-events-none">
        {toasts.map(t => (
          <div 
            key={t.id} 
            className={`p-3.5 rounded-lg border shadow-lg flex items-start gap-2.5 bg-white text-xs text-slate-700 pointer-events-auto transition-all animate-slide-up ${
              t.type === 'success' ? 'border-emerald-300 border-l-4 border-l-emerald-500' :
              t.type === 'failure' ? 'border-rose-300 border-l-4 border-l-rose-500' :
              t.type === 'warning' ? 'border-amber-300 border-l-4 border-l-amber-500' :
              'border-slate-300 border-l-4 border-l-slate-500'
            }`}
          >
            {t.type === 'success' && <CheckCircle2 className="w-4 h-4 text-emerald-500 shrink-0 mt-0.5" />}
            {t.type === 'failure' && <AlertTriangle className="w-4 h-4 text-rose-500 shrink-0 mt-0.5" />}
            {t.type === 'warning' && <AlertTriangle className="w-4 h-4 text-amber-500 shrink-0 mt-0.5" />}
            {t.type === 'info' && <Cpu className="w-4 h-4 text-indigo-500 shrink-0 mt-0.5" />}
            
            <div className="flex-1">
              <p className="font-semibold leading-tight">{t.message}</p>
            </div>
          </div>
        ))}
      </div>

    </div>
  );
}
