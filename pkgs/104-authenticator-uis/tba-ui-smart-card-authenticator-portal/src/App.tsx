import { useState, useEffect } from 'react';
import { SmartCard, TrustAnchor, MTLSConfig, AuditLog } from './types';
import { mockCards, mockTrustAnchors, mockMTLSConfigs, mockAuditLogs } from './data/mockData';
import { SmartCardPreflight } from './components/SmartCardPreflight';
import { CeremonyShell } from './components/CeremonyShell';
import { UserLifecycleManager } from './components/UserLifecycleManager';
import { AdminOperations } from './components/AdminOperations';
import { CliDiagnostics } from './components/CliDiagnostics';
import { 
  Cpu, HardDrive, KeyRound, Network, ClipboardList, RefreshCw, 
  Terminal, ShieldCheck, Sliders, Play, Settings, ShieldAlert, Layers
} from 'lucide-react';

export default function App() {
  // Core Smart-Card data models
  const [cards, setCards] = useState<SmartCard[]>(mockCards);
  const [trustAnchors, setTrustAnchors] = useState<TrustAnchor[]>(mockTrustAnchors);
  const [mTLSConfigs, setMTLSConfigs] = useState<MTLSConfig[]>(mockMTLSConfigs);
  const [auditLogs, setAuditLogs] = useState<AuditLog[]>(mockAuditLogs);

  // Active workspace tab
  const [activeTab, setActiveTab] = useState<'auth' | 'lifecycle' | 'admin' | 'cli'>('auth');

  // Simulated hardware / interface states
  const [browserCompatible, setBrowserCompatible] = useState(true);
  const [middlewareRunning, setMiddlewareRunning] = useState(true);
  const [readerConnected, setReaderConnected] = useState(true);
  const [cardInserted, setCardInserted] = useState(true);
  const [selectedReaderName, setSelectedReaderName] = useState('SCR-3310 Contactless Smart Card Reader');
  const [trustOutage, setTrustOutage] = useState(false);

  // UTC time tracking
  const [utcTime, setUtcTime] = useState('');

  useEffect(() => {
    const updateTime = () => {
      const now = new Date();
      setUtcTime(now.toUTCString());
    };
    updateTime();
    const interval = setInterval(updateTime, 1000);
    return () => clearInterval(interval);
  }, []);

  // Preset state toggler helpers for tester's convenience
  const applyPreset = (preset: 'optimal' | 'no-reader' | 'no-card' | 'trust-outage') => {
    switch (preset) {
      case 'optimal':
        setBrowserCompatible(true);
        setMiddlewareRunning(true);
        setReaderConnected(true);
        setCardInserted(true);
        setTrustOutage(false);
        break;
      case 'no-reader':
        setBrowserCompatible(true);
        setMiddlewareRunning(true);
        setReaderConnected(false);
        setCardInserted(false);
        setTrustOutage(false);
        break;
      case 'no-card':
        setBrowserCompatible(true);
        setMiddlewareRunning(true);
        setReaderConnected(true);
        setCardInserted(false);
        setTrustOutage(false);
        break;
      case 'trust-outage':
        setBrowserCompatible(true);
        setMiddlewareRunning(true);
        setReaderConnected(true);
        setCardInserted(true);
        setTrustOutage(true);
        break;
    }

    // Log the configuration adjustment
    handleLogIncident({
      event: 'sim.context.adjusted',
      actor: 'SIMULATOR_HOST',
      status: 'warning',
      details: `Hardware environment context set to preset: "${preset.toUpperCase()}"`,
      ipAddress: '127.0.0.1'
    });
  };

  const handleLogIncident = (newLog: Omit<AuditLog, 'id' | 'timestamp'>) => {
    const fullLog: AuditLog = {
      ...newLog,
      id: `audit-${Date.now()}`,
      timestamp: new Date().toISOString(),
    };
    setAuditLogs(prev => [fullLog, ...prev]);
  };

  const handleRefreshHardware = () => {
    handleLogIncident({
      event: 'sc.hardware.rescan',
      actor: 'MIDDLEWARE_HOST',
      status: 'success',
      details: 'Polled local USB endpoints. CCID slots verified.',
      ipAddress: '127.0.0.1'
    });
    // Trigger small flash/re-evaluation
    const originalReader = readerConnected;
    setReaderConnected(false);
    setTimeout(() => {
      setReaderConnected(originalReader);
    }, 400);
  };

  // Card modifications handler (P1)
  const handleAddCard = (newCard: SmartCard) => {
    setCards(prev => [...prev, newCard]);
  };

  const handleRemoveCard = (id: string) => {
    setCards(prev => prev.filter(c => c.id !== id));
  };

  const handleUpdateCardStatus = (id: string, status: SmartCard['status']) => {
    setCards(prev => prev.map(c => c.id === id ? { ...c, status } : c));
  };

  // Trust Anchor operations (P2)
  const handleAddTrustAnchor = (anchor: TrustAnchor) => {
    setTrustAnchors(prev => [...prev, anchor]);
  };

  const handleRemoveTrustAnchor = (id: string) => {
    setTrustAnchors(prev => prev.filter(a => a.id !== id));
  };

  // mTLS operations (P2)
  const handleAddMTLSConfig = (config: MTLSConfig) => {
    setMTLSConfigs(prev => [...prev, config]);
  };

  const handleRemoveMTLSConfig = (id: string) => {
    setMTLSConfigs(prev => prev.filter(m => m.id !== id));
  };

  const handleAuthSuccess = (card: SmartCard) => {
    // Record last used timestamp on successful login/challenge
    setCards(prev => prev.map(c => c.id === card.id ? { ...c, lastUsed: new Date().toLocaleTimeString() } : c));
  };

  return (
    <div className="min-h-screen bg-slate-100 flex flex-col font-sans text-slate-800" id="main-app-container">
      {/* Top Banner Hub */}
      <header className="bg-slate-900 text-white border-b border-slate-800 px-6 py-4 flex flex-col md:flex-row md:items-center justify-between gap-4 select-none">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-indigo-600 rounded-lg text-white shadow-md shadow-indigo-600/10">
            <Cpu className="w-5 h-5 animate-pulse" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white uppercase">Smart Card Authentication Portal</h1>
            <p className="text-xs text-slate-400 mt-0.5">High-Assurance PIV/CAC Possession Factor Console</p>
          </div>
        </div>

        {/* Real-Time stats and Clock */}
        <div className="flex flex-wrap items-center gap-4 text-xs font-mono">
          <div className="bg-slate-950 px-3 py-1.5 rounded border border-slate-800 text-slate-300">
            <span className="text-slate-500 uppercase font-bold text-[10px] mr-1.5 select-none">SYS_CLOCK_UTC:</span>
            <span>{utcTime || 'Synching...'}</span>
          </div>
          <div className="flex gap-2">
            <span className={`px-2.5 py-1.5 rounded-full text-[10px] font-bold uppercase border flex items-center gap-1.5 ${
              readerConnected && cardInserted && middlewareRunning && !trustOutage
                ? 'bg-emerald-500/10 text-emerald-300 border-emerald-500/20'
                : 'bg-amber-500/10 text-amber-300 border-amber-500/20'
            }`}>
              <span className={`h-1.5 w-1.5 rounded-full ${readerConnected && cardInserted && middlewareRunning && !trustOutage ? 'bg-emerald-400' : 'bg-amber-400'}`}></span>
              {readerConnected && cardInserted && middlewareRunning && !trustOutage ? 'State Secure' : 'Alert Pending'}
            </span>
          </div>
        </div>
      </header>

      {/* Main Workspace Frame */}
      <div className="flex-1 max-w-[1440px] w-full mx-auto p-4 md:p-6 grid grid-cols-1 lg:grid-cols-12 gap-6">
        
        {/* Left Hand: Interactive Hardware Sandbox & Preflight Checker (Release Gating feedback) */}
        <div className="lg:col-span-4 space-y-6 flex flex-col">
          
          {/* Sandbox State Toggles */}
          <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm" id="sandbox-card">
            <div className="flex items-center gap-2 mb-3.5 pb-2.5 border-b border-slate-100">
              <Sliders className="w-4.5 h-4.5 text-indigo-600" />
              <h3 className="font-semibold text-slate-800 text-sm">Sandbox Hardware & Environment</h3>
            </div>
            
            <p className="text-xs text-slate-500 mb-4 leading-relaxed">
              Use these state switches to test the authenticator. Change reader connections, extract tokens, or trigger outages, and inspect how the front-end ceremony and logs adapt instantly.
            </p>

            {/* Presets Quickbar */}
            <div className="grid grid-cols-2 gap-2 mb-4">
              <button
                onClick={() => applyPreset('optimal')}
                className="py-1.5 px-2 bg-emerald-50 hover:bg-emerald-100 text-emerald-800 border border-emerald-200 text-[10px] font-bold rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preset-optimal"
              >
                🟢 Optimal State
              </button>
              <button
                onClick={() => applyPreset('no-card')}
                className="py-1.5 px-2 bg-slate-50 hover:bg-slate-150 text-slate-700 border border-slate-200 text-[10px] font-bold rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preset-no-card"
              >
                🔒 Card Absent
              </button>
              <button
                onClick={() => applyPreset('no-reader')}
                className="py-1.5 px-2 bg-amber-50 hover:bg-amber-100 text-amber-800 border border-amber-200 text-[10px] font-bold rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preset-no-reader"
              >
                ⚠️ No Reader
              </button>
              <button
                onClick={() => applyPreset('trust-outage')}
                className="py-1.5 px-2 bg-rose-50 hover:bg-rose-100 text-rose-800 border border-rose-200 text-[10px] font-bold rounded-lg transition-colors flex items-center justify-center gap-1"
                id="btn-preset-outage"
              >
                🛑 OCSP Outage
              </button>
            </div>

            {/* Individual Switches */}
            <div className="space-y-3.5 pt-1">
              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <HardDrive className="w-4 h-4 text-slate-400" />
                  USB Reader connected
                </span>
                <button
                  onClick={() => {
                    setReaderConnected(!readerConnected);
                    if (readerConnected) setCardInserted(false); // Can't have card without reader
                  }}
                  className={`w-10 h-5.5 rounded-full p-0.5 transition-colors focus:outline-none ${readerConnected ? 'bg-indigo-600' : 'bg-slate-300'}`}
                  id="toggle-reader"
                >
                  <div className={`bg-white w-4.5 h-4.5 rounded-full shadow-sm transition-transform ${readerConnected ? 'translate-x-4.5' : 'translate-x-0'}`}></div>
                </button>
              </div>

              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <KeyRound className="w-4 h-4 text-slate-400" />
                  PIV/CAC Token inserted
                </span>
                <button
                  disabled={!readerConnected}
                  onClick={() => setCardInserted(!cardInserted)}
                  className={`w-10 h-5.5 rounded-full p-0.5 transition-colors focus:outline-none disabled:opacity-50 disabled:cursor-not-allowed ${cardInserted ? 'bg-indigo-600' : 'bg-slate-300'}`}
                  id="toggle-card"
                >
                  <div className={`bg-white w-4.5 h-4.5 rounded-full shadow-sm transition-transform ${cardInserted ? 'translate-x-4.5' : 'translate-x-0'}`}></div>
                </button>
              </div>

              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <Cpu className="w-4 h-4 text-slate-400" />
                  Middleware service active
                </span>
                <button
                  onClick={() => setMiddlewareRunning(!middlewareRunning)}
                  className={`w-10 h-5.5 rounded-full p-0.5 transition-colors focus:outline-none ${middlewareRunning ? 'bg-indigo-600' : 'bg-slate-300'}`}
                  id="toggle-middleware"
                >
                  <div className={`bg-white w-4.5 h-4.5 rounded-full shadow-sm transition-transform ${middlewareRunning ? 'translate-x-4.5' : 'translate-x-0'}`}></div>
                </button>
              </div>

              <div className="flex items-center justify-between text-xs font-semibold text-slate-700">
                <span className="flex items-center gap-1.5">
                  <Network className="w-4 h-4 text-slate-400" />
                  OCSP Trust service outage
                </span>
                <button
                  onClick={() => setTrustOutage(!trustOutage)}
                  className={`w-10 h-5.5 rounded-full p-0.5 transition-colors focus:outline-none ${trustOutage ? 'bg-rose-600' : 'bg-slate-300'}`}
                  id="toggle-outage"
                >
                  <div className={`bg-white w-4.5 h-4.5 rounded-full shadow-sm transition-transform ${trustOutage ? 'translate-x-4.5' : 'translate-x-0'}`}></div>
                </button>
              </div>

              {/* Reader name customizer */}
              <div className="pt-2 border-t border-slate-100 space-y-1.5">
                <label className="text-[10px] font-bold text-slate-400 uppercase block">Active Reader Driver</label>
                <select
                  value={selectedReaderName}
                  onChange={(e) => setSelectedReaderName(e.target.value)}
                  disabled={!readerConnected}
                  className="w-full px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-xs text-slate-700 focus:outline-none disabled:bg-slate-50 disabled:text-slate-400 font-mono"
                  id="select-reader-name"
                >
                  <option value="SCR-3310 Contactless Smart Card Reader">SCR-3310 Contactless Reader</option>
                  <option value="Omnikey 5022 CL Smart Card Reader">Omnikey 5022 CL RFID</option>
                  <option value="Athena ASEDrive IIIe USB CCID Keyboard">Athena ASEDrive IIIe Keyboard</option>
                </select>
              </div>
            </div>
          </div>

          {/* Core preflight status */}
          <SmartCardPreflight
            browserCompatible={browserCompatible}
            middlewareRunning={middlewareRunning}
            readerConnected={readerConnected}
            cardInserted={cardInserted}
            selectedReaderName={selectedReaderName}
            onRefresh={handleRefreshHardware}
          />
        </div>

        {/* Right Hand: Navigable Workspace Area (P0, P1, P2 modules) */}
        <div className="lg:col-span-8 flex flex-col gap-6">
          
          {/* Top workspace navigation bar */}
          <nav className="bg-white border border-slate-200 rounded-xl p-2.5 shadow-sm flex flex-wrap gap-2 justify-between items-center select-none" id="workspace-nav">
            <span className="text-xs font-bold text-slate-400 uppercase tracking-wider pl-2 hidden md:inline">Workspace Modules:</span>
            <div className="flex flex-wrap gap-1.5">
              <button
                onClick={() => setActiveTab('auth')}
                className={`px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
                  activeTab === 'auth' 
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/15' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
                }`}
                id="workspace-tab-auth"
              >
                <ShieldCheck className="w-4 h-4" />
                P0 — Possession Ceremony
              </button>
              <button
                onClick={() => setActiveTab('lifecycle')}
                className={`px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
                  activeTab === 'lifecycle' 
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/15' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
                }`}
                id="workspace-tab-lifecycle"
              >
                <Sliders className="w-4 h-4" />
                P1 — Lifecycle & Enrollment
              </button>
              <button
                onClick={() => setActiveTab('admin')}
                className={`px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
                  activeTab === 'admin' 
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/15' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
                }`}
                id="workspace-tab-admin"
              >
                <Settings className="w-4 h-4" />
                P2 — Admin Console
              </button>
              <button
                onClick={() => setActiveTab('cli')}
                className={`px-4 py-2 text-xs font-bold rounded-lg transition-all flex items-center gap-1.5 ${
                  activeTab === 'cli' 
                    ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/15' 
                    : 'text-slate-600 hover:bg-slate-100 hover:text-slate-800'
                }`}
                id="workspace-tab-cli"
              >
                <Terminal className="w-4 h-4" />
                CLI Tools
              </button>
            </div>
          </nav>

          {/* Tab switches */}
          <div className="flex-1">
            {activeTab === 'auth' && (
              <CeremonyShell
                cards={cards}
                browserCompatible={browserCompatible}
                middlewareRunning={middlewareRunning}
                readerConnected={readerConnected}
                cardInserted={cardInserted}
                selectedReaderName={selectedReaderName}
                onRefreshHardware={handleRefreshHardware}
                trustOutage={trustOutage}
                onLogIncident={handleLogIncident}
                onAuthSuccess={handleAuthSuccess}
              />
            )}

            {activeTab === 'lifecycle' && (
              <UserLifecycleManager
                cards={cards}
                onAddCard={handleAddCard}
                onRemoveCard={handleRemoveCard}
                onUpdateCardStatus={handleUpdateCardStatus}
                onLogIncident={handleLogIncident}
                readerConnected={readerConnected}
                cardInserted={cardInserted}
              />
            )}

            {activeTab === 'admin' && (
              <AdminOperations
                cards={cards}
                trustAnchors={trustAnchors}
                mTLSConfigs={mTLSConfigs}
                auditLogs={auditLogs}
                onAddTrustAnchor={handleAddTrustAnchor}
                onRemoveTrustAnchor={handleRemoveTrustAnchor}
                onAddMTLSConfig={handleAddMTLSConfig}
                onRemoveMTLSConfig={handleRemoveMTLSConfig}
                trustOutage={trustOutage}
                onToggleTrustOutage={() => setTrustOutage(!trustOutage)}
                onLogIncident={handleLogIncident}
              />
            )}

            {activeTab === 'cli' && (
              <div className="space-y-4">
                <div className="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
                  <h4 className="text-sm font-bold text-slate-800">Native Desktop / CLI Connectivity Helper</h4>
                  <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                    Test your smart-card enrollment parameters, list PKCS#11 slots, construct path chains, and inspect OCSP statuses without exposing secure on-card private keys to application scope.
                  </p>
                </div>
                <CliDiagnostics
                  cards={cards}
                  readerConnected={readerConnected}
                  selectedReaderName={selectedReaderName}
                />
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Footer credits and information */}
      <footer className="bg-slate-900 border-t border-slate-800 py-4 px-6 text-center select-none text-[10.5px] text-slate-500 font-mono">
        <div>Smart Card Authenticator Suite v1.4.0 • Compliant with FIPS-201, SP 800-73-4, and WebAuthn AMR profiles</div>
      </footer>
    </div>
  );
}
