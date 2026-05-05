
import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import IdentityManagement from './components/IdentityManagement';
import PolicyEditor from './components/PolicyEditor';
import RealmManagement from './components/RealmManagement';
import RealmDetail from './components/RealmDetail';
import SecurityManagement from './components/SecurityManagement';
import AbuseManagement from './components/AbuseManagement';
import ClientManagement from './components/ClientManagement';
import ServiceInfrastructure from './components/ServiceInfrastructure';
import Administration from './components/Administration';
import { Icons } from './constants';
import { controlPlaneStateService } from './services/controlPlaneStateService';
import { Realm } from './types';
import { backendService } from './services/backendService';

const App: React.FC = () => {
  const [active_tab, set_active_tab] = useState('dashboard');
  const [realms, set_realms] = useState<Realm[]>([]);
  const [current_realm, set_current_realm] = useState<Realm | null>(null);
  const [selected_realm_detail, set_selected_realm_detail] = useState<Realm | null>(null);
  const [loading, set_loading] = useState(true);
  const [bootstrap_error, set_bootstrap_error] = useState<string | null>(null);
  const [is_lockdown, set_is_lockdown] = useState(controlPlaneStateService.get_lockdown());

  const refresh_realms = async () => {
    const fetched_realms = await backendService.getRealms();

    if (fetched_realms.length === 0) {
      set_bootstrap_error('No realms were returned by the backend.');
    } else {
      set_bootstrap_error(null);
    }

    set_realms(fetched_realms);
    set_current_realm((current) => {
      if (current && fetched_realms.find((realm) => realm.id === current.id)) {
        return current;
      }
      return fetched_realms[0] ?? null;
    });
  };

  useEffect(() => {
    const bootstrap = async () => {
      try {
        await refresh_realms();
      } catch (error) {
        console.error('Failed to load realms from backend', error);
        set_bootstrap_error('Failed to load realms from backend.');
      } finally {
        setTimeout(() => set_loading(false), 1200);
      }
    };

    void bootstrap();
  }, []);

  useEffect(() => {
    const interval = setInterval(() => {
      set_is_lockdown(controlPlaneStateService.get_lockdown());
    }, 500);
    return () => clearInterval(interval);
  }, []);

  const handle_select_realm_for_detail = (realm: Realm) => {
    set_selected_realm_detail(realm);
    set_active_tab('realm_detail');
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-[#1a1a1a] flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-8 text-white font-bold tracking-[4px] text-xs animate-pulse uppercase">Booting AEGIS.CORE</p>
      </div>
    );
  }

  if (!current_realm) {
    return (
      <div className="fixed inset-0 bg-[#1a1a1a] flex flex-col items-center justify-center px-8">
        <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-8 text-white font-bold tracking-[4px] text-xs animate-pulse uppercase">Boot Sequence Interrupted</p>
        <p className="mt-4 text-[#d0d0cc] text-sm text-center max-w-md">
          {bootstrap_error ?? 'A realm could not be selected. Verify backend authentication and realm data, then retry.'}
        </p>
        <button
          className="btn-parian mt-8"
          onClick={() => {
            set_loading(true);
            set_bootstrap_error(null);
            void (async () => {
              try {
                await refresh_realms();
              } catch (error) {
                console.error('Failed to refresh realms from backend', error);
                set_bootstrap_error('Failed to load realms from backend.');
              } finally {
                set_loading(false);
              }
            })();
          }}
        >
          Retry Bootstrap
        </button>
      </div>
    );
  }

  const is_admin_realm = current_realm.slug === 'admin';

  const render_content = () => {
    switch (active_tab) {
      case 'dashboard': return <Dashboard realm_id={current_realm.id} />;
      case 'realms': return <RealmManagement realms={realms} on_refresh={refresh_realms} on_select_realm={handle_select_realm_for_detail} />;
      case 'realm_detail':
        return selected_realm_detail ? (
          <RealmDetail
            realm={selected_realm_detail}
            on_back={() => {
              set_selected_realm_detail(null);
              set_active_tab('realms');
            }}
          />
        ) : null;
      case 'identities': return <IdentityManagement />;
      case 'policies': return <PolicyEditor realm_id={current_realm.id} />;
      case 'clients': return <ClientManagement realm_id={current_realm.id} />;
      case 'security': return <SecurityManagement />;
      case 'abuse': return <AbuseManagement />;
      case 'services': return <ServiceInfrastructure />;
      case 'platform_settings':
      case 'audit_logs':
      case 'tenancy_stats':
        return <Administration tab={active_tab} />;
      default: return (
        <div className="flex flex-col items-center justify-center h-full text-center space-y-4 py-20">
          <div className="w-16 h-16 bg-[#ebebe5] border-etched flex items-center justify-center text-[#1a1a1a]">
            <Icons.Settings />
          </div>
          <h2 className="text-xl font-bold">Module Offline</h2>
          <p className="text-[#55554e] max-w-sm">This component is currently undergoing architectural synthesis.</p>
          <button onClick={() => set_active_tab('dashboard')} className="btn-parian">Return to Flux</button>
        </div>
      );
    }
  };

  return (
    <div className={`flex items-center justify-center h-screen w-screen transition-all duration-700 ${is_lockdown ? 'grayscale contrast-125' : ''}`}>
      <div className="lattice-overlay"></div>
      <div className={`arterial-pulse ${is_lockdown ? 'opacity-100' : 'opacity-30'}`}></div>

      <div className={`polylith w-[96vw] h-[92vh] bg-[#f4f4f0] border-etched shadow-milled grid grid-cols-[280px_1fr] grid-rows-[60px_1fr] overflow-hidden relative ${is_lockdown ? 'border-[#ff2d00] border-2 shadow-[0_0_50px_rgba(255,45,0,0.3)]' : ''}`}>

        {is_lockdown && (
          <div className="absolute top-0 left-0 right-0 h-1 bg-[#ff2d00] z-[1000] animate-pulse"></div>
        )}

        <header className={`col-span-full border-b border-[#1a1a1a] flex items-center justify-between px-6 transition-colors duration-500 ${is_lockdown ? 'bg-[#1a1a1a] text-[#ff2d00]' : 'bg-[#ebebe5]'}`}>
          <div className="flex items-center space-x-3 font-bold text-lg tracking-tight">
             <div className={`w-6 h-6 flex items-center justify-center transition-colors ${is_lockdown ? 'bg-[#ff2d00] text-[#1a1a1a]' : 'bg-[#1a1a1a] text-white'}`}>
                <Icons.Shield />
             </div>
             <span>AEGIS.GATEWAY {is_lockdown && '[EMERGENCY_LOCKDOWN]'}</span>
          </div>

          <div className="flex items-center space-x-12">
            {!is_lockdown && (
              <div className="flex items-center space-x-3 cursor-pointer group">
                <span className="text-[10px] font-bold text-[#55554e] uppercase tracking-widest">Active Realm:</span>
                <select
                  value={current_realm.id}
                  onChange={(e) => {
                    const found = realms.find(r => r.id === e.target.value);
                    if(found) {
                      set_current_realm(found);
                      set_active_tab('dashboard');
                    }
                  }}
                  className={`text-xs font-bold bg-white border border-[#1a1a1a] px-2 py-1 outline-none transition-all cursor-pointer ${is_admin_realm ? 'border-[#ff2d00] text-[#ff2d00]' : ''}`}
                >
                  {realms.map(r => (
                    <option key={r.id} value={r.id}>{r.name.toUpperCase()}</option>
                  ))}
                </select>
              </div>
            )}
            <div className="flex items-center space-x-2 text-[10px] font-bold uppercase tracking-widest">
                <div className={`w-2 h-2 rounded-full animate-pulse ${is_lockdown ? 'bg-[#ff2d00]' : 'bg-[#00ffcc]'}`}></div>
                <span>Sync Status: {is_lockdown ? 'ISOLATED' : '14ms'}</span>
            </div>
          </div>
        </header>

        <Sidebar active_tab={active_tab} set_active_tab={set_active_tab} is_admin={is_admin_realm} />

        <main className="p-10 overflow-y-auto bg-[radial-gradient(circle_at_top_right,#ffffff,#f4f4f0)] relative no-scrollbar">
          {render_content()}
        </main>
      </div>
    </div>
  );
};

export default App;
