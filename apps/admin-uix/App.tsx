
import React, { useState, useEffect } from 'react';
import Sidebar from './components/Sidebar';
import Dashboard from './components/Dashboard';
import IdentityManagement from './components/IdentityManagement';
import PolicyEditor from './components/PolicyEditor';
import TenantManagement from './components/TenantManagement';
import TenantDetail from './components/TenantDetail';
import SecurityManagement from './components/SecurityManagement';
import AbuseManagement from './components/AbuseManagement';
import ClientManagement from './components/ClientManagement';
import ServiceInfrastructure from './components/ServiceInfrastructure';
import Administration from './components/Administration';
import { Icons } from './constants';
import { controlPlaneStateService } from './services/controlPlaneStateService';
import { Tenant } from './types';
import { backendService } from './services/backendService';

const App: React.FC = () => {
  const [active_tab, set_active_tab] = useState('dashboard');
  const [tenants, set_tenants] = useState<Tenant[]>([]);
  const [current_tenant, set_current_tenant] = useState<Tenant | null>(null);
  const [selected_tenant_detail, set_selected_tenant_detail] = useState<Tenant | null>(null);
  const [loading, set_loading] = useState(true);
  const [bootstrap_error, set_bootstrap_error] = useState<string | null>(null);
  const [is_lockdown, set_is_lockdown] = useState(controlPlaneStateService.get_lockdown());

  const refresh_tenants = async () => {
    const fetched_tenants = await backendService.getTenants();

    if (fetched_tenants.length === 0) {
      set_bootstrap_error('No tenants were returned by the backend.');
    } else {
      set_bootstrap_error(null);
    }

    set_tenants(fetched_tenants);
    set_current_tenant((current) => {
      if (current && fetched_tenants.find((tenant) => tenant.id === current.id)) {
        return current;
      }
      return fetched_tenants[0] ?? null;
    });
  };

  useEffect(() => {
    const bootstrap = async () => {
      try {
        await refresh_tenants();
      } catch (error) {
        console.error('Failed to load tenants from backend', error);
        set_bootstrap_error('Failed to load tenants from backend.');
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

  const handle_select_tenant_for_detail = (tenant: Tenant) => {
    set_selected_tenant_detail(tenant);
    set_active_tab('tenant_detail');
  };

  if (loading) {
    return (
      <div className="fixed inset-0 bg-[#1a1a1a] flex flex-col items-center justify-center">
        <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-8 text-white font-bold tracking-[4px] text-xs animate-pulse uppercase">Booting TIGRBL_AUTH.CORE</p>
      </div>
    );
  }

  if (!current_tenant) {
    return (
      <div className="fixed inset-0 bg-[#1a1a1a] flex flex-col items-center justify-center px-8">
        <div className="w-12 h-12 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
        <p className="mt-8 text-white font-bold tracking-[4px] text-xs animate-pulse uppercase">Boot Sequence Interrupted</p>
        <p className="mt-4 text-[#d0d0cc] text-sm text-center max-w-md">
          {bootstrap_error ?? 'A tenant could not be selected. Verify backend authentication and tenant data, then retry.'}
        </p>
        <button
          className="btn-parian mt-8"
          onClick={() => {
            set_loading(true);
            set_bootstrap_error(null);
            void (async () => {
              try {
                await refresh_tenants();
              } catch (error) {
                console.error('Failed to refresh tenants from backend', error);
                set_bootstrap_error('Failed to load tenants from backend.');
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

  const is_admin_tenant = current_tenant.slug === 'admin';

  const render_content = () => {
    switch (active_tab) {
      case 'dashboard': return <Dashboard tenant_id={current_tenant.id} />;
      case 'tenants': return <TenantManagement tenants={tenants} on_refresh={refresh_tenants} on_select_tenant={handle_select_tenant_for_detail} />;
      case 'tenant_detail':
        return selected_tenant_detail ? (
          <TenantDetail
            tenant={selected_tenant_detail}
            on_back={() => {
              set_selected_tenant_detail(null);
              set_active_tab('tenants');
            }}
          />
        ) : null;
      case 'identities': return <IdentityManagement />;
      case 'policies': return <PolicyEditor tenant_id={current_tenant.id} />;
      case 'clients': return <ClientManagement tenant_id={current_tenant.id} />;
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
             <span>TIGRBL_AUTH.GATEWAY {is_lockdown && '[EMERGENCY_LOCKDOWN]'}</span>
          </div>

          <div className="flex items-center space-x-12">
            {!is_lockdown && (
              <div className="flex items-center space-x-3 cursor-pointer group">
                <span className="text-[10px] font-bold text-[#55554e] uppercase tracking-widest">Active Tenant:</span>
                <select
                  value={current_tenant.id}
                  onChange={(e) => {
                    const found = tenants.find(r => r.id === e.target.value);
                    if(found) {
                      set_current_tenant(found);
                      set_active_tab('dashboard');
                    }
                  }}
                  className={`text-xs font-bold bg-white border border-[#1a1a1a] px-2 py-1 outline-none transition-all cursor-pointer ${is_admin_tenant ? 'border-[#ff2d00] text-[#ff2d00]' : ''}`}
                >
                  {tenants.map(r => (
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

        <Sidebar active_tab={active_tab} set_active_tab={set_active_tab} is_admin={is_admin_tenant} />

        <main className="p-10 overflow-y-auto bg-[radial-gradient(circle_at_top_right,#ffffff,#f4f4f0)] relative no-scrollbar">
          {render_content()}
        </main>
      </div>
    </div>
  );
};

export default App;
