import React from 'react';
import { getDashboardStats } from '../data/mockData';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { ShieldCheck, ShieldAlert, FileSearch, CheckCircle2, AlertTriangle, ArrowRight } from 'lucide-react';

const timeSeriesData = [
  { time: '08:00', permit: 4000, deny: 240, indeterminate: 20 },
  { time: '09:00', permit: 3000, deny: 139, indeterminate: 10 },
  { time: '10:00', permit: 2000, deny: 980, indeterminate: 50 },
  { time: '11:00', permit: 2780, deny: 390, indeterminate: 30 },
  { time: '12:00', permit: 1890, deny: 480, indeterminate: 15 },
  { time: '13:00', permit: 2390, deny: 380, indeterminate: 20 },
  { time: '14:00', permit: 3490, deny: 430, indeterminate: 10 },
];

export default function Dashboard({ onNavigate }: { onNavigate: (tab: string) => void }) {
  const stats = getDashboardStats();

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto h-full overflow-y-auto">
      <div className="flex justify-between items-end">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Authorization Provenance</h1>
          <p className="text-slate-500 mt-1">Tenant: <span className="font-medium text-slate-700">global-prod</span> • Last 24 hours</p>
        </div>
        <button 
          onClick={() => onNavigate('explorer')}
          className="flex items-center text-sm font-medium text-indigo-600 hover:text-indigo-700 bg-indigo-50 hover:bg-indigo-100 px-4 py-2 rounded-md transition-colors"
        >
          Explore Decisions <ArrowRight className="w-4 h-4 ml-1.5" />
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard 
          title="Total Decisions" 
          value={stats.totalDecisions.toLocaleString()} 
          icon={FileSearch} 
          trend="+12% from yesterday" 
        />
        <StatCard 
          title="Permit Rate" 
          value={`${stats.permitRate}%`} 
          icon={ShieldCheck} 
          iconColor="text-emerald-500" 
        />
        <StatCard 
          title="Deny Rate" 
          value={`${stats.denyRate}%`} 
          icon={ShieldAlert} 
          iconColor="text-rose-500" 
          alert={stats.denyRate > 10}
        />
        <StatCard 
          title="Provenance Coverage" 
          value={`${stats.provenanceCoverage}%`} 
          icon={CheckCircle2} 
          iconColor="text-indigo-500" 
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <div className="lg:col-span-2 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
          <h2 className="text-lg font-semibold text-slate-900 mb-6 tracking-tight">Decision Volume (Permit vs Deny)</h2>
          <div className="h-72">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={timeSeriesData} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} dy={10} />
                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#64748b', fontSize: 12 }} />
                <Tooltip 
                  cursor={{ fill: '#f8fafc' }}
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                />
                <Bar dataKey="permit" stackId="a" fill="#10b981" radius={[0, 0, 4, 4]} name="Permit" />
                <Bar dataKey="deny" stackId="a" fill="#f43f5e" radius={[0, 0, 0, 0]} name="Deny" />
                <Bar dataKey="indeterminate" stackId="a" fill="#f59e0b" radius={[4, 4, 0, 0]} name="Indeterminate" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col">
          <h2 className="text-lg font-semibold text-slate-900 mb-6 tracking-tight">System Health</h2>
          
          <div className="space-y-6 flex-1">
            <HealthItem 
              label="Avg Evaluation Latency" 
              value={`${stats.avgLatencyMs}ms`} 
              status="good" 
            />
            <HealthItem 
              label="Enforcement Match Rate" 
              value={`${stats.enforcementMatchRate}%`} 
              status={stats.enforcementMatchRate < 99 ? 'warning' : 'good'} 
              subtitle="Decisions missing valid PEP receipts"
            />
            <HealthItem 
              label="Stale Fact Rate" 
              value="1.4%" 
              status="good" 
            />
            <HealthItem 
              label="Ingestion Backlog" 
              value="0 events" 
              status="good" 
            />
          </div>
          
          <div className="mt-6 pt-6 border-t border-slate-100">
            <div className="flex items-start bg-amber-50 text-amber-800 p-3 rounded-md border border-amber-200">
              <AlertTriangle className="w-5 h-5 shrink-0 mr-2 mt-0.5 text-amber-600" />
              <div>
                <p className="text-sm font-medium">Enforcement mismatch detected</p>
                <p className="text-xs mt-1 text-amber-700">42 permits lacked enforcement receipts in the last hour. <button onClick={() => onNavigate('explorer')} className="underline font-medium hover:text-amber-900">Investigate</button></p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon, iconColor = "text-slate-400", trend, alert = false }: any) {
  return (
    <div className={`bg-white p-5 rounded-xl border shadow-sm ${alert ? 'border-rose-200' : 'border-slate-200'}`}>
      <div className="flex justify-between items-start">
        <p className="text-sm font-medium text-slate-500">{title}</p>
        <Icon className={`w-5 h-5 ${alert ? 'text-rose-500' : iconColor}`} />
      </div>
      <div className="mt-4 flex items-baseline">
        <p className={`text-2xl font-bold ${alert ? 'text-rose-600' : 'text-slate-900'}`}>{value}</p>
      </div>
      {trend && <p className="text-xs text-slate-500 mt-1">{trend}</p>}
    </div>
  );
}

function HealthItem({ label, value, status, subtitle }: any) {
  return (
    <div>
      <div className="flex justify-between items-center mb-1">
        <p className="text-sm font-medium text-slate-700">{label}</p>
        <p className={`text-sm font-bold ${
          status === 'good' ? 'text-emerald-600' : 
          status === 'warning' ? 'text-amber-600' : 'text-rose-600'
        }`}>{value}</p>
      </div>
      {subtitle && <p className="text-xs text-slate-500">{subtitle}</p>}
      <div className="w-full bg-slate-100 rounded-full h-1.5 mt-2">
        <div className={`h-1.5 rounded-full ${
          status === 'good' ? 'bg-emerald-500 w-[95%]' : 
          status === 'warning' ? 'bg-amber-500 w-[85%]' : 'bg-rose-500 w-[40%]'
        }`}></div>
      </div>
    </div>
  );
}
