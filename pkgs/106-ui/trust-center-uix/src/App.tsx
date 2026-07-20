import React, { useState, useEffect } from "react";
import {
  Compass,
  Globe,
  Network,
  FileText,
  Code,
  ShieldAlert,
  Activity,
  Sparkles,
  HelpCircle,
  Menu,
  X,
  RefreshCw,
  Cpu,
} from "lucide-react";
import Dashboard from "./components/Dashboard";
import ConnectionWizard from "./components/ConnectionWizard";
import TrustGraph from "./components/TrustGraph";
import ChainInspector from "./components/ChainInspector";
import MappingLab from "./components/MappingLab";
import OperationsIncidentConsole from "./components/OperationsIncidentConsole";
import { FederationConnection, IncidentRecord, TrustNode, TrustEdge } from "./types";

export default function App() {
  const [activeTab, setActiveTab] = useState<string>("dashboard");
  const [connections, setConnections] = useState<FederationConnection[]>([]);
  const [incidents, setIncidents] = useState<IncidentRecord[]>([]);
  const [trustNodes, setTrustNodes] = useState<TrustNode[]>([]);
  const [trustEdges, setTrustEdges] = useState<TrustEdge[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [mobileMenuOpen, setMobileMenuOpen] = useState<boolean>(false);

  // Fetch initial telemetry and seed data
  const fetchTelemetryData = async () => {
    setLoading(true);
    try {
      const connRes = await fetch("/api/federation/connections");
      const connectionsData = await connRes.json();
      setConnections(connectionsData);

      const incRes = await fetch("/api/federation/incidents");
      const incidentsData = await incRes.json();
      setIncidents(incidentsData);

      // Fetch static/dynamic trust graph data
      // Represent nodes and edges directly in console state
      const defaultNodes: TrustNode[] = [
        { id: "n-root", label: "Tigrbl Global Root", type: "anchor", entityId: "https://trust.auth.tigrbl.com", health: "healthy" },
        { id: "n-se-gov", label: "Swedish Government Anchor", type: "anchor", entityId: "https://trust.gov.se/federation", health: "healthy" },
        { id: "n-edugain", label: "eduGAIN Anchor", type: "anchor", entityId: "https://edugain.org/anchor", health: "healthy" },
        { id: "n-inter-se", label: "Swedish Gov Intermediate", type: "intermediate", entityId: "https://intermediate.trust.sweden.se", health: "healthy" },
        { id: "n-inter-edu", label: "eduGAIN Academic Intermediate", type: "intermediate", entityId: "https://anchors.edugain.org/keys", health: "failing" },
        { id: "n-leaf-okta", label: "Okta Enterprise Workforce IdP", type: "op", entityId: "https://tigrbl-enterprise.okta.com/oauth2/default", health: "healthy" },
        { id: "n-leaf-swedish", label: "Swedish National Federation", type: "op", entityId: "https://fed.trust.sweden.se", health: "degraded" },
        { id: "n-leaf-edugain", label: "eduGAIN Research & Academic Trust", type: "op", entityId: "https://edugain.org/federation", health: "failing" },
        { id: "n-rp-portal", label: "Tigrbl Auth Portal (RP)", type: "rp", entityId: "https://auth.tigrbl.com/tenant-default/federation", health: "healthy" }
      ];

      const defaultEdges: TrustEdge[] = [
        { id: "e1", source: "n-root", target: "n-leaf-okta", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2027-01-15" },
        { id: "e2", source: "n-se-gov", target: "n-inter-se", exchangeKind: "subordinate", state: "active", constraints: "{}", validUntil: "2026-12-31" },
        { id: "e3", source: "n-inter-se", target: "n-leaf-swedish", exchangeKind: "subordinate", state: "active", constraints: "{}", validUntil: "2026-11-30" },
        { id: "e4", source: "n-edugain", target: "n-inter-edu", exchangeKind: "subordinate", state: "active", constraints: "{}", validUntil: "2026-10-15" },
        { id: "e5", source: "n-inter-edu", target: "n-leaf-edugain", exchangeKind: "subordinate", state: "active", constraints: "{}", validUntil: "2026-08-31" },
        { id: "e6", source: "n-rp-portal", target: "n-root", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2028-01-01" },
        { id: "e7", source: "n-rp-portal", target: "n-se-gov", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2027-07-01" },
        { id: "e8", source: "n-rp-portal", target: "n-edugain", exchangeKind: "anchor_association", state: "active", constraints: "{}", validUntil: "2026-12-31" }
      ];

      setTrustNodes(defaultNodes);
      setTrustEdges(defaultEdges);

    } catch (e) {
      console.error("Failed to connect with Trust Center API endpoints:", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTelemetryData();
  }, []);

  // API Callbacks for the Connection Wizard
  const handleAddConnection = async (draftConn: any) => {
    try {
      const res = await fetch("/api/federation/connections", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(draftConn),
      });
      const data = await res.json();
      if (res.ok) {
        setConnections([...connections, data]);
        return data;
      } else {
        alert(data.error || "Failed to register connection draft.");
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleUpdateConnection = async (id: string, updates: any) => {
    try {
      const res = await fetch(`/api/federation/connections/${id}`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });
      const data = await res.json();
      if (res.ok) {
        setConnections(connections.map((c) => (c.id === id ? data : c)));
        return data;
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleTriggerTest = async (id: string) => {
    try {
      const res = await fetch(`/api/federation/connections/${id}/test`, { method: "POST" });
      const data = await res.json();
      return data;
    } catch (err) {
      console.error(err);
    }
  };

  const handleTriggerValidate = async (id: string) => {
    try {
      const res = await fetch(`/api/federation/connections/${id}/validate`, { method: "POST" });
      const data = await res.json();
      // Update local connection list health
      setConnections(connections.map((c) => (c.id === id ? { ...c, health: data.health, lastValidation: data.lastValidation } : c)));
      return data;
    } catch (err) {
      console.error(err);
    }
  };

  const handleActivateConnection = async (id: string) => {
    try {
      const res = await fetch(`/api/federation/connections/${id}/activate`, { method: "POST" });
      const data = await res.json();
      if (res.ok) {
        setConnections(connections.map((c) => (c.id === id ? { ...c, state: data.state, activeVersion: data.activeVersion } : c)));
        // Also refresh incidents
        const incRes = await fetch("/api/federation/incidents");
        const incidentsData = await incRes.json();
        setIncidents(incidentsData);
        return data;
      }
    } catch (err) {
      console.error(err);
    }
  };

  // API Callbacks for the Incident & Operations Board
  const handleMitigateIncident = async (id: string) => {
    try {
      const res = await fetch(`/api/federation/incidents/${id}/mitigate`, { method: "POST" });
      const data = await res.json();
      if (res.ok) {
        setIncidents(incidents.map((i) => (i.id === id ? data : i)));
        // Refresh connection lists as one might have gotten suspended
        const connRes = await fetch("/api/federation/connections");
        const connectionsData = await connRes.json();
        setConnections(connectionsData);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleResolveIncident = async (id: string) => {
    try {
      const res = await fetch(`/api/federation/incidents/${id}/resolve`, { method: "POST" });
      const data = await res.json();
      if (res.ok) {
        setIncidents(incidents.map((i) => (i.id === id ? data : i)));
        // Refresh connections
        const connRes = await fetch("/api/federation/connections");
        const connectionsData = await connRes.json();
        setConnections(connectionsData);
      }
    } catch (err) {
      console.error(err);
    }
  };

  // Graph edge revocation
  const handleRevokeEdge = async (edgeId: string) => {
    try {
      const res = await fetch(`/api/federation/edges/${edgeId}/revoke`, { method: "POST" });
      const data = await res.json();
      if (res.ok) {
        setTrustEdges(trustEdges.map((e) => (e.id === edgeId ? { ...e, state: "revoked" } : e)));
        alert(`Trust relationship '${edgeId}' successfully revoked. Blast radius quarantine applied to downstream workloads.`);
      }
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="min-h-screen flex flex-col bg-slate-950 text-slate-100" id="trust-center-app-root">
      {/* Upper Navigation Header Bar */}
      <header className="border-b border-slate-850 bg-slate-900/40 backdrop-blur-md sticky top-0 z-50 px-4 sm:px-6 py-4 flex justify-between items-center">
        <div className="flex items-center gap-2.5">
          <div className="p-2 bg-indigo-600 rounded-lg text-white font-bold flex items-center justify-center shadow-lg shadow-indigo-600/20">
            <Cpu className="h-5 w-5" />
          </div>
          <div>
            <h1 className="text-sm font-bold text-white tracking-tight flex items-center gap-1.5">
              Tigrbl Auth Trust Center
              <span className="px-1.5 py-0.5 bg-indigo-950 text-indigo-400 text-[9px] font-bold rounded-md uppercase tracking-wider border border-indigo-800/40">
                OIDC FED 1.0
              </span>
            </h1>
            <p className="text-[10px] text-slate-400">Federation & Policy Governance Engine</p>
          </div>
        </div>

        {/* Desktop Navigation Tabs */}
        <nav className="hidden lg:flex items-center gap-1.5 bg-slate-950 p-1 rounded-lg border border-slate-850">
          {[
            { id: "dashboard", label: "Dashboard", icon: Compass },
            { id: "wizard", label: "Connection Wizard", icon: Globe },
            { id: "graph", label: "Trust Graph Explorer", icon: Network },
            { id: "inspector", label: "Chain Inspector", icon: FileText },
            { id: "mapping", label: "Mapping Lab", icon: Code },
            { id: "operations", label: "Operations & Incident", icon: ShieldAlert },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`px-3 py-1.5 text-xs font-semibold rounded-md flex items-center gap-1.5 transition ${
                  isActive
                    ? "bg-slate-900 border border-slate-800 text-white"
                    : "text-slate-400 hover:text-white hover:bg-slate-900/50"
                }`}
                id={`nav-${tab.id}`}
              >
                <Icon className={`h-3.5 w-3.5 ${isActive ? "text-indigo-400" : ""}`} />
                {tab.label}
              </button>
            );
          })}
        </nav>

        {/* Right side Metadata Indicators */}
        <div className="hidden lg:flex items-center gap-4 text-xs font-mono text-slate-500">
          <div className="flex items-center gap-1.5">
            <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
            <span className="text-slate-400">TENANT ROUTER TRUTH ACTIVE</span>
          </div>
        </div>

        {/* Mobile Menu Toggle Button */}
        <button
          onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          className="lg:hidden p-1.5 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 hover:text-white"
          id="mobile-menu-toggle"
        >
          {mobileMenuOpen ? <X className="h-5 w-5" /> : <Menu className="h-5 w-5" />}
        </button>
      </header>

      {/* Mobile Drawer Overlay Menu */}
      {mobileMenuOpen && (
        <div className="lg:hidden bg-slate-950 border-b border-slate-850 px-4 py-4 space-y-2 z-40 relative">
          {[
            { id: "dashboard", label: "Dashboard", icon: Compass },
            { id: "wizard", label: "Connection Wizard", icon: Globe },
            { id: "graph", label: "Trust Graph Explorer", icon: Network },
            { id: "inspector", label: "Chain Inspector", icon: FileText },
            { id: "mapping", label: "Mapping Lab", icon: Code },
            { id: "operations", label: "Operations & Incident", icon: ShieldAlert },
          ].map((tab) => {
            const Icon = tab.icon;
            const isActive = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                onClick={() => {
                  setActiveTab(tab.id);
                  setMobileMenuOpen(false);
                }}
                className={`w-full px-4 py-2.5 text-xs font-semibold rounded-lg flex items-center gap-2.5 transition ${
                  isActive ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white hover:bg-slate-900"
                }`}
              >
                <Icon className="h-4 w-4" />
                {tab.label}
              </button>
            );
          })}
        </div>
      )}

      {/* Main Content Workspace Container */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8 space-y-6">
        {loading ? (
          <div className="h-96 flex flex-col items-center justify-center space-y-4 text-slate-500" id="main-loader">
            <RefreshCw className="h-10 w-10 animate-spin text-indigo-400" />
            <div className="text-xs font-mono">Initializing Runtime Trust Plane Telemetry...</div>
          </div>
        ) : (
          <>
            {/* Dynamic Content Views */}
            {activeTab === "dashboard" && (
              <Dashboard
                connections={connections}
                incidents={incidents}
                onNavigate={(tab) => setActiveTab(tab)}
                onRefresh={fetchTelemetryData}
              />
            )}

            {activeTab === "wizard" && (
              <ConnectionWizard
                connections={connections}
                onAddConnection={handleAddConnection}
                onUpdateConnection={handleUpdateConnection}
                onTriggerTest={handleTriggerTest}
                onTriggerValidate={handleTriggerValidate}
                onActivate={handleActivateConnection}
              />
            )}

            {activeTab === "graph" && (
              <TrustGraph nodes={trustNodes} edges={trustEdges} onRevokeEdge={handleRevokeEdge} />
            )}

            {activeTab === "inspector" && <ChainInspector connections={connections} />}

            {activeTab === "mapping" && <MappingLab />}

            {activeTab === "operations" && (
              <OperationsIncidentConsole
                incidents={incidents}
                onMitigateIncident={handleMitigateIncident}
                onResolveIncident={handleResolveIncident}
                onRefresh={fetchTelemetryData}
              />
            )}
          </>
        )}
      </main>

      {/* Footer bar */}
      <footer className="border-t border-slate-850 py-4 px-6 text-center text-[10px] text-slate-500 font-mono">
        <div>Tigrbl-Auth-Router-Federation-Trust • Complies with OpenID Federation 1.0 Spec Standard 2026</div>
        <div className="mt-1 text-slate-600">Secure Sandboxed Container Port Ingress mapping active</div>
      </footer>
    </div>
  );
}
