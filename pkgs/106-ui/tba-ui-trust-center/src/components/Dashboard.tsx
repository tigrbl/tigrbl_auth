import React from "react";
import {
  Globe,
  ShieldCheck,
  ShieldAlert,
  Activity,
  Key,
  Flame,
  ArrowRight,
  Sparkles,
  RefreshCw,
  Clock,
  Compass,
} from "lucide-react";
import { FederationConnection, IncidentRecord, FederationProtocol, ConnectionState } from "../types";

interface DashboardProps {
  connections: FederationConnection[];
  incidents: IncidentRecord[];
  onNavigate: (tab: string) => void;
  onRefresh: () => void;
}

export default function Dashboard({ connections, incidents, onNavigate, onRefresh }: DashboardProps) {
  const activeCount = connections.filter((c) => c.state === ConnectionState.ACTIVE).length;
  const draftCount = connections.filter((c) => c.state === ConnectionState.DRAFT || c.state === ConnectionState.REVIEW).length;
  const suspendedCount = connections.filter((c) => c.state === ConnectionState.SUSPENDED).length;
  
  const healthyCount = connections.filter((c) => c.health === "healthy" && c.state === ConnectionState.ACTIVE).length;
  const criticalIncidents = incidents.filter((i) => i.status === "active" && i.severity === "critical");
  const warningIncidents = incidents.filter((i) => i.status === "active" && i.severity === "warning");

  return (
    <div className="space-y-6" id="dashboard-container">
      {/* Top Banner with Actions */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4 bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div>
          <h2 className="text-xl font-semibold text-white flex items-center gap-2">
            <Compass className="h-5 w-5 text-indigo-400" />
            Operations Overview
          </h2>
          <p className="text-sm text-slate-400 mt-1">
            Real-time status of OIDC integrations, OpenID Federation 1.0 trust networks, and cryptographic rollovers.
          </p>
        </div>
        <div className="flex gap-3">
          <button
            onClick={onRefresh}
            className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-medium rounded-lg flex items-center gap-2 transition"
            id="refresh-overview-btn"
          >
            <RefreshCw className="h-4 w-4" />
            Refresh Telemetry
          </button>
          <button
            onClick={() => onNavigate("wizard")}
            className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-lg flex items-center gap-2 shadow-lg shadow-indigo-500/20 transition"
            id="new-connection-btn"
          >
            <Globe className="h-4 w-4" />
            Connect Provider
          </button>
        </div>
      </div>

      {/* Critical System Warnings / Active Incidents banner */}
      {criticalIncidents.length > 0 && (
        <div className="bg-red-950/40 border border-red-800/60 rounded-xl p-4 flex items-start gap-3 text-red-200" id="critical-alert-banner">
          <Flame className="h-5 w-5 text-red-500 shrink-0 mt-0.5 animate-pulse" />
          <div className="flex-1">
            <div className="font-semibold text-white flex items-center gap-2">
              Critical Federation Incidents Active ({criticalIncidents.length})
            </div>
            <p className="text-sm text-red-300 mt-1">
              Authentication transaction failures are imminent. Key verification has failed for active partners.
            </p>
            <div className="mt-2 flex gap-4 text-xs">
              <button
                onClick={() => onNavigate("operations")}
                className="text-white underline font-semibold flex items-center gap-1 hover:text-red-100"
              >
                Access Emergency Controls <ArrowRight className="h-3 w-3" />
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Grid of Key Performance Indicators (KPIs) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4" id="kpi-grid">
        {/* KPI 1: Active Connections */}
        <div className="bg-slate-900/40 p-5 rounded-xl border border-slate-800/80 hover:border-indigo-500/30 transition">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Federated IdPs</span>
            <span className="p-1.5 bg-indigo-500/10 rounded-lg text-indigo-400">
              <Globe className="h-4 w-4" />
            </span>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{activeCount}</span>
            <span className="text-xs text-slate-500">out of {connections.length}</span>
          </div>
          <p className="text-xs text-indigo-300 mt-2 flex items-center gap-1">
            <span className="inline-block h-2 w-2 rounded-full bg-emerald-500"></span>
            {healthyCount} connections healthy
          </p>
        </div>

        {/* KPI 2: Trust Anchor Integrity */}
        <div className="bg-slate-900/40 p-5 rounded-xl border border-slate-800/80 hover:border-emerald-500/30 transition">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Trust Anchor Integrity</span>
            <span className="p-1.5 bg-emerald-500/10 rounded-lg text-emerald-400">
              <ShieldCheck className="h-4 w-4" />
            </span>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-emerald-400">100%</span>
            <span className="text-xs text-slate-500">3 roots pinned</span>
          </div>
          <p className="text-xs text-slate-400 mt-2">
            No unapproved trust extensions
          </p>
        </div>

        {/* KPI 3: Open Incidents */}
        <div className="bg-slate-900/40 p-5 rounded-xl border border-slate-800/80 hover:border-red-500/30 transition">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Active Incidents</span>
            <span className="p-1.5 bg-red-500/10 rounded-lg text-red-400">
              <ShieldAlert className="h-4 w-4" />
            </span>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{incidents.filter(i => i.status === "active").length}</span>
            <span className="text-xs text-slate-500">outstanding</span>
          </div>
          <p className="text-xs text-red-300 mt-2 flex items-center gap-1">
            <span className="h-1.5 w-1.5 rounded-full bg-red-500 animate-ping"></span>
            {criticalIncidents.length} critical, {warningIncidents.length} warnings
          </p>
        </div>

        {/* KPI 4: Pending Approvals */}
        <div className="bg-slate-900/40 p-5 rounded-xl border border-slate-800/80 hover:border-amber-500/30 transition">
          <div className="flex justify-between items-start">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Drafts & Staging</span>
            <span className="p-1.5 bg-amber-500/10 rounded-lg text-amber-400">
              <Activity className="h-4 w-4" />
            </span>
          </div>
          <div className="mt-4 flex items-baseline gap-2">
            <span className="text-3xl font-bold text-white">{draftCount}</span>
            <span className="text-xs text-slate-500">connections</span>
          </div>
          <p className="text-xs text-amber-300 mt-2">
            {connections.filter(c => c.state === ConnectionState.REVIEW).length} awaiting admin approval
          </p>
        </div>
      </div>

      {/* Protocol Badge Highlights & Connection List */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left 2 Columns: Connection Status Overview */}
        <div className="lg:col-span-2 bg-slate-900/30 rounded-xl border border-slate-800 p-6 space-y-4">
          <div className="flex justify-between items-center">
            <h3 className="text-base font-semibold text-white">Federated Integration Pipeline</h3>
            <span className="text-xs text-slate-400">Showing {connections.length} items</span>
          </div>

          <div className="divide-y divide-slate-800">
            {connections.map((c) => (
              <div key={c.id} className="py-4 flex flex-col sm:flex-row sm:items-center justify-between gap-4 first:pt-0 last:pb-0">
                <div className="space-y-1">
                  <div className="flex items-center gap-2">
                    <span className="text-sm font-semibold text-white">{c.displayName}</span>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      c.protocol === FederationProtocol.OPENID_FEDERATION 
                        ? "bg-indigo-950 text-indigo-300 border border-indigo-800/50" 
                        : "bg-slate-800 text-slate-300 border border-slate-700"
                    }`}>
                      {c.protocol === FederationProtocol.OPENID_FEDERATION ? "OpenID Fed 1.0" : "OIDC Core"}
                    </span>
                  </div>
                  <div className="text-xs text-slate-500 font-mono truncate max-w-md">
                    {c.issuer}
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  {/* State badge */}
                  <span className={`px-2 py-1 rounded-md text-xs font-semibold ${
                    c.state === ConnectionState.ACTIVE ? "bg-emerald-500/10 text-emerald-400" :
                    c.state === ConnectionState.SUSPENDED ? "bg-red-500/10 text-red-400" :
                    c.state === ConnectionState.REVIEW ? "bg-amber-500/10 text-amber-300" :
                    "bg-slate-800 text-slate-400"
                  }`}>
                    {c.state}
                  </span>

                  {/* Health status indicator */}
                  <div className="flex items-center gap-1.5" title="Connection Health Status">
                    <span className={`h-2.5 w-2.5 rounded-full ${
                      c.health === "healthy" ? "bg-emerald-500" :
                      c.health === "degraded" ? "bg-amber-400" :
                      "bg-red-500"
                    }`}></span>
                    <span className="text-xs text-slate-400 uppercase font-semibold hidden sm:inline">
                      {c.health}
                    </span>
                  </div>

                  <button
                    onClick={() => {
                      onNavigate("wizard");
                      // Highlight the specific connection
                    }}
                    className="p-1.5 hover:bg-slate-800 rounded-lg text-slate-400 hover:text-white transition"
                    title="Inspect Connection"
                  >
                    <ArrowRight className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Right 1 Column: Standards & Operations Health Board */}
        <div className="bg-slate-900/30 rounded-xl border border-slate-800 p-6 space-y-6">
          <div>
            <h3 className="text-base font-semibold text-white">Conformance & Standards</h3>
            <p className="text-xs text-slate-500 mt-1">Status of cryptographic trust profiles.</p>
          </div>

          <div className="space-y-4">
            {/* Standard 1 */}
            <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800 flex items-start gap-3">
              <span className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg shrink-0">
                <ShieldCheck className="h-5 w-5" />
              </span>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-white">OIDC Core / RFC 8414</span>
                  <span className="px-1.5 py-0.5 bg-emerald-950 text-emerald-400 text-[9px] font-bold rounded">SUPPORTED</span>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Dynamic Client Registration, endpoint publication, metadata signing, and fallback keys verify successfully.
                </p>
              </div>
            </div>

            {/* Standard 2 */}
            <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800 flex items-start gap-3">
              <span className="p-2 bg-indigo-500/10 text-indigo-400 rounded-lg shrink-0">
                <RefreshCw className="h-5 w-5" />
              </span>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-white">OpenID Federation 1.0</span>
                  <span className="px-1.5 py-0.5 bg-indigo-950 text-indigo-400 text-[9px] font-bold rounded">PREVIEW</span>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Finalized February 2026. Includes signed entity-statement resolution, trust-chain calculation, and metadata policy engine.
                </p>
              </div>
            </div>

            {/* Standard 3 */}
            <div className="bg-slate-900/60 p-4 rounded-lg border border-slate-800 flex items-start gap-3">
              <span className="p-2 bg-slate-800 text-slate-400 rounded-lg shrink-0">
                <Clock className="h-5 w-5" />
              </span>
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-sm font-semibold text-white">SAML 2.0 Assertions</span>
                  <span className="px-1.5 py-0.5 bg-slate-850 text-slate-400 text-[9px] font-bold rounded">PLANNED</span>
                </div>
                <p className="text-xs text-slate-400 mt-1">
                  Enterprise identity provider mappings, XML assertions, signature validation, and single logout (SLO).
                </p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
