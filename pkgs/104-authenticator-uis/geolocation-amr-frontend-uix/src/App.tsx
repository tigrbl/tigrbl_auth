import React, { useState } from 'react';
import { EndUserCeremony } from './components/EndUserCeremony';
import { PrivacyPortal } from './components/PrivacyPortal';
import { AdminConsole } from './components/AdminConsole';
import { ShieldCheck, User, Settings, LayoutGrid } from 'lucide-react';
import { 
  INITIAL_SIMULATIONS, INITIAL_CONSENTS, INITIAL_POLICIES, 
  INITIAL_HEALTH, INITIAL_AUDIT, INITIAL_SOURCES 
} from './data/mockData';
import { ZonePolicy, SimulationProfile, ProviderHealth, AuditRecord } from './types';

function App() {
  const [activeView, setActiveView] = useState<'end_user' | 'privacy' | 'admin'>('end_user');
  
  // State
  const [policies, setPolicies] = useState<ZonePolicy[]>(INITIAL_POLICIES);
  const [simulationProfiles, setSimulationProfiles] = useState<SimulationProfile[]>(INITIAL_SIMULATIONS);
  const [activeProfile, setActiveProfile] = useState<SimulationProfile>(INITIAL_SIMULATIONS[0]);
  const [providers, setProviders] = useState<ProviderHealth[]>(INITIAL_HEALTH);
  const [auditLogs, setAuditLogs] = useState<AuditRecord[]>(INITIAL_AUDIT);
  const [consents, setConsents] = useState(INITIAL_CONSENTS);

  const mockSessionContext = {
    userEmail: 'jick.68.0@gmail.com',
    ipAddress: activeProfile.ipAddress,
    coarseRegion: 'Austin, TX',
    isp: activeProfile.isp,
    lastValidated: new Date().toISOString(),
    accuracy: activeProfile.accuracy,
    auditReference: auditLogs.length > 0 ? auditLogs[0].auditReference : 'tx_pending'
  };

  const handleSavePolicy = (policy: ZonePolicy) => {
    setPolicies(prev => {
      const existing = prev.find(p => p.id === policy.id);
      if (existing) {
        return prev.map(p => p.id === policy.id ? policy : p);
      }
      return [...prev, policy];
    });
  };

  const handleDeletePolicy = (id: string) => {
    setPolicies(prev => prev.filter(p => p.id !== id));
  };

  const handleChangeProfileValue = (key: keyof SimulationProfile, value: any) => {
    setActiveProfile(prev => ({ ...prev, [key]: value }));
  };

  const handleUpdateProviderStatus = (id: string, status: ProviderHealth['status']) => {
    setProviders(prev => prev.map(p => p.id === id ? { ...p, status } : p));
  };

  const handleRefreshProvider = (id: string) => {
    setProviders(prev => prev.map(p => {
      if (p.id === id) {
        return {
          ...p,
          latency: Math.floor(Math.random() * 50) + 10,
          errorRate: Number((Math.random() * 2).toFixed(1)),
          lastSync: new Date().toISOString()
        };
      }
      return p;
    }));
  };

  const handleAuthSuccess = (auditRecord: AuditRecord) => {
    setAuditLogs(prev => [auditRecord, ...prev]);
  };

  const handleRevokeConsent = (id: string) => {
    setConsents(prev => prev.filter(c => c.id !== id));
  };

  const handleEnrollDevice = (deviceDetails: any) => {
    console.log('Enrolled device:', deviceDetails);
  };

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 font-sans selection:bg-indigo-100 selection:text-indigo-900">
      {/* Top Navigation Bar */}
      <header className="bg-white border-b border-slate-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-14 flex items-center justify-between">
          <div className="flex items-center gap-2 text-indigo-600">
            <ShieldCheck className="w-5 h-5" />
            <h1 className="text-sm font-bold tracking-wide uppercase font-display">AMR: Geo Service</h1>
          </div>
          
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-lg">
            <button
              onClick={() => setActiveView('end_user')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                activeView === 'end_user' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <LayoutGrid className="w-4 h-4" />
              <span className="hidden sm:inline">P0 Authentication</span>
            </button>
            <button
              onClick={() => setActiveView('privacy')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                activeView === 'privacy' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <User className="w-4 h-4" />
              <span className="hidden sm:inline">P1 User Privacy</span>
            </button>
            <button
              onClick={() => setActiveView('admin')}
              className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-semibold transition-all ${
                activeView === 'admin' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-500 hover:text-slate-700'
              }`}
            >
              <Settings className="w-4 h-4" />
              <span className="hidden sm:inline">P2 Admin Console</span>
            </button>
          </nav>
        </div>
      </header>

      {/* Main Content Area */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeView === 'end_user' && (
          <div className="animate-in fade-in duration-500">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-slate-900 font-display">
                Contextual Authentication & Step-Up Ceremony
              </h2>
              <p className="text-sm text-slate-500 mt-1 max-w-2xl">
                Location acts as contextual evidence influencing the authentication policy. It is not an identity proof on its own.
              </p>
            </div>
            <EndUserCeremony 
              onSuccess={handleAuthSuccess} 
              selectedSimulationProfile={activeProfile} 
            />
          </div>
        )}

        {activeView === 'privacy' && (
          <div className="animate-in fade-in duration-500">
            <div className="mb-6">
              <h2 className="text-xl font-bold text-slate-900 font-display">
                User Evidence, Privacy & Lifecycle
              </h2>
              <p className="text-sm text-slate-500 mt-1 max-w-2xl">
                Manage location context visibility, consent withdrawals, and device posture registrations.
              </p>
            </div>
            <PrivacyPortal
              sessionContext={mockSessionContext}
              consentList={consents}
              onRevokeConsent={handleRevokeConsent}
              onEnrollDevice={handleEnrollDevice}
            />
          </div>
        )}

        {activeView === 'admin' && (
          <div className="animate-in fade-in duration-500">
            <AdminConsole 
              policies={policies}
              onSavePolicy={handleSavePolicy}
              onDeletePolicy={handleDeletePolicy}
              simulationProfiles={simulationProfiles}
              activeProfile={activeProfile}
              onSelectProfile={setActiveProfile}
              onChangeProfileValue={handleChangeProfileValue}
              providers={providers}
              onRefreshProvider={handleRefreshProvider}
              onUpdateProviderStatus={handleUpdateProviderStatus}
              auditLogs={auditLogs}
              sources={INITIAL_SOURCES}
            />
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
