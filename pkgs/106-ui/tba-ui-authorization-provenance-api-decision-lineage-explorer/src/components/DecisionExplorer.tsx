import React, { useState } from 'react';
import { mockDecisions } from '../data/mockData';
import { Search, Filter, ShieldCheck, ShieldAlert, ChevronRight, Clock, Box, CheckCircle2, AlertTriangle } from 'lucide-react';
import DecisionDetail from './DecisionDetail';

export default function DecisionExplorer({ selectedId, onSelect }: { selectedId: string | null, onSelect: (id: string | null) => void }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [filterEffect, setFilterEffect] = useState<string>('all');

  const filteredDecisions = mockDecisions.filter(d => {
    const matchesSearch = d.subject.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
                          d.resource.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                          d.id.includes(searchTerm);
    const matchesEffect = filterEffect === 'all' || d.effect === filterEffect;
    return matchesSearch && matchesEffect;
  });

  if (selectedId) {
    const decision = mockDecisions.find(d => d.id === selectedId);
    if (decision) {
      return <DecisionDetail decision={decision} onBack={() => onSelect(null)} />;
    }
  }

  return (
    <div className="flex flex-col h-full bg-slate-50">
      <div className="p-6 border-b border-slate-200 bg-white shrink-0">
        <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Decision Explorer</h1>
        <p className="text-slate-500 text-sm mt-1">Search and analyze historical authorization decisions</p>
        
        <div className="mt-6 flex gap-4">
          <div className="relative flex-1 max-w-xl">
            <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
              <Search className="h-5 w-5 text-slate-400" />
            </div>
            <input
              type="text"
              className="block w-full pl-10 pr-3 py-2 border border-slate-300 rounded-md leading-5 bg-white placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              placeholder="Search by subject, resource, or decision ID..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          
          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-500" />
            <select 
              className="pl-3 pr-8 py-2 border border-slate-300 rounded-md text-sm focus:outline-none focus:ring-2 focus:ring-indigo-500"
              value={filterEffect}
              onChange={(e) => setFilterEffect(e.target.value)}
            >
              <option value="all">All Effects</option>
              <option value="permit">Permit</option>
              <option value="deny">Deny</option>
            </select>
          </div>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6">
        <div className="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden">
          <table className="min-w-full divide-y divide-slate-200">
            <thead className="bg-slate-50">
              <tr>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Decision ID & Time</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Subject</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Action & Resource</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Effect</th>
                <th scope="col" className="px-6 py-3 text-left text-xs font-semibold text-slate-500 uppercase tracking-wider">Enforcement</th>
                <th scope="col" className="relative px-6 py-3"><span className="sr-only">View</span></th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-slate-200">
              {filteredDecisions.map((decision) => (
                <tr 
                  key={decision.id} 
                  onClick={() => onSelect(decision.id)}
                  className="hover:bg-slate-50 cursor-pointer transition-colors group"
                >
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-mono text-indigo-600">{decision.id.substring(0, 15)}...</div>
                    <div className="text-xs text-slate-500 flex items-center mt-1">
                      <Clock className="w-3 h-3 mr-1" />
                      {new Date(decision.timestamp).toLocaleTimeString()}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-slate-900">{decision.subject.name}</div>
                    <div className="text-xs text-slate-500">{decision.subject.type}</div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="text-sm font-medium text-slate-900 flex items-center">
                      <span className="bg-slate-100 text-slate-600 px-2 py-0.5 rounded text-xs mr-2 border border-slate-200 uppercase">{decision.action}</span>
                      {decision.resource.name}
                    </div>
                    <div className="text-xs text-slate-500 mt-1 flex items-center">
                      <Box className="w-3 h-3 mr-1" /> {decision.resource.type}
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    {decision.effect === 'permit' ? (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-emerald-100 text-emerald-800 border border-emerald-200">
                        <ShieldCheck className="w-3.5 h-3.5 mr-1" /> Permit
                      </span>
                    ) : (
                      <span className="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-rose-100 text-rose-800 border border-rose-200">
                        <ShieldAlert className="w-3.5 h-3.5 mr-1" /> Deny
                      </span>
                    )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-slate-500">
                     {decision.enforcement ? (
                       decision.enforcement.status === 'enforced' 
                        ? <span className="text-emerald-600 flex items-center"><CheckCircle2 className="w-4 h-4 mr-1" /> Enforced</span>
                        : <span className="text-amber-600 flex items-center"><AlertTriangle className="w-4 h-4 mr-1" /> Mismatch</span>
                     ) : (
                       <span className="text-slate-400">None</span>
                     )}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <ChevronRight className="w-5 h-5 text-slate-400 group-hover:text-indigo-600 transition-colors inline-block" />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {filteredDecisions.length === 0 && (
            <div className="p-12 text-center text-slate-500">
              No decisions found matching your criteria.
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
