import { Activity, BookOpen, Key, Settings, CheckCircle2 } from 'lucide-react';
import { TabId } from '../lib/data';

interface SidebarProps {
  activeTab: TabId;
  onTabChange: (tab: TabId) => void;
}

export function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  const navItems: { id: TabId; label: string; icon: React.ReactNode }[] = [
    { id: 'overview', label: 'Overview', icon: <Activity className="w-5 h-5" /> },
    { id: 'metadata', label: 'Metadata Explorer', icon: <BookOpen className="w-5 h-5" /> },
    { id: 'jwks', label: 'JWKS Explorer', icon: <Key className="w-5 h-5" /> },
    { id: 'config', label: 'Verifier Config', icon: <Settings className="w-5 h-5" /> },
    { id: 'validation', label: 'Validation Workbench', icon: <CheckCircle2 className="w-5 h-5" /> },
  ];

  return (
    <div className="w-64 bg-slate-900 border-r border-slate-800 flex flex-col h-screen shrink-0 text-slate-300">
      <div className="p-4 border-b border-slate-800">
        <h1 className="text-lg font-bold text-slate-100 flex items-center gap-2">
          <CheckCircle2 className="w-5 h-5 text-indigo-400" />
          Resource Val UIX
        </h1>
        <p className="text-xs text-slate-500 mt-1">tigrbl-auth-api</p>
      </div>
      <nav className="flex-1 overflow-y-auto py-4">
        <ul className="space-y-1 px-2">
          {navItems.map((item) => (
            <li key={item.id}>
              <button
                onClick={() => onTabChange(item.id)}
                className={`w-full flex items-center gap-3 px-3 py-2 text-sm rounded-md transition-colors ${
                  activeTab === item.id
                    ? 'bg-indigo-500/10 text-indigo-400 font-medium'
                    : 'hover:bg-slate-800/50 hover:text-slate-200'
                }`}
              >
                {item.icon}
                {item.label}
              </button>
            </li>
          ))}
        </ul>
      </nav>
      <div className="p-4 border-t border-slate-800 text-xs text-slate-500">
        <div className="flex items-center gap-2 mb-2">
          <div className="w-2 h-2 rounded-full bg-emerald-500" />
          <span>API Connected</span>
        </div>
        <div>v2.4.0-stable</div>
      </div>
    </div>
  );
}
