/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState } from 'react';
import { Shield, LayoutDashboard, Search, RefreshCw, GitCompare, Archive, Settings, LogOut, Menu } from 'lucide-react';
import Dashboard from './components/Dashboard';
import DecisionExplorer from './components/DecisionExplorer';
import ReplayWorkbench from './components/ReplayWorkbench';
import PolicyComparison from './components/PolicyComparison';
import EvidenceRoom from './components/EvidenceRoom';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [selectedDecisionId, setSelectedDecisionId] = useState<string | null>(null);

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <Dashboard onNavigate={(tab) => setActiveTab(tab)} />;
      case 'explorer':
        return <DecisionExplorer 
          selectedId={selectedDecisionId} 
          onSelect={(id) => setSelectedDecisionId(id)} 
        />;
      case 'replay':
        return <ReplayWorkbench />;
      case 'comparison':
        return <PolicyComparison />;
      case 'evidence':
        return <EvidenceRoom />;
      default:
        return <Dashboard onNavigate={(tab) => setActiveTab(tab)} />;
    }
  };

  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'explorer', label: 'Decision Explorer', icon: Search },
    { id: 'replay', label: 'Replay Workbench', icon: RefreshCw },
    { id: 'comparison', label: 'Policy Drift', icon: GitCompare },
    { id: 'evidence', label: 'Evidence Room', icon: Archive },
  ];

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-slate-800">
          <Shield className="w-6 h-6 text-indigo-400 mr-3" />
          <span className="font-semibold text-white tracking-tight">Tigrbl Authz</span>
        </div>
        <nav className="flex-1 py-6 px-3 space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  if (item.id !== 'explorer') setSelectedDecisionId(null);
                }}
                className={`w-full flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors ${
                  activeTab === item.id 
                    ? 'bg-indigo-500/10 text-indigo-400' 
                    : 'hover:bg-slate-800 hover:text-white'
                }`}
              >
                <Icon className="w-4 h-4 mr-3" />
                {item.label}
              </button>
            );
          })}
        </nav>
        <div className="p-4 border-t border-slate-800">
          <button className="flex items-center w-full px-3 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors">
            <Settings className="w-4 h-4 mr-3" /> Settings
          </button>
          <button className="flex items-center w-full px-3 py-2 text-sm font-medium text-slate-400 hover:text-white transition-colors mt-1">
            <LogOut className="w-4 h-4 mr-3" /> Sign Out
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col h-screen overflow-hidden">
        {/* Mobile Header */}
        <header className="h-16 md:hidden bg-white border-b border-slate-200 flex items-center px-4 justify-between shrink-0">
          <div className="flex items-center">
            <Shield className="w-6 h-6 text-indigo-600 mr-2" />
            <span className="font-semibold tracking-tight">Tigrbl</span>
          </div>
          <button className="p-2 text-slate-500"><Menu className="w-5 h-5" /></button>
        </header>
        
        <div className="flex-1 overflow-auto">
          {renderContent()}
        </div>
      </main>
    </div>
  );
}
