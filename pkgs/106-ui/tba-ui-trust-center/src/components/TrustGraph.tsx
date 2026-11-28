import React, { useState } from "react";
import {
  Network,
  ShieldAlert,
  ShieldCheck,
  Activity,
  Trash2,
  Users,
  AlertTriangle,
  Play,
  CheckCircle2,
  ArrowRight,
  HelpCircle,
  Clock,
  Sparkles,
  RefreshCw,
} from "lucide-react";
import { TrustNode, TrustEdge } from "../types";
import CodeBlock from "./CodeBlock";

interface TrustGraphProps {
  nodes: TrustNode[];
  edges: TrustEdge[];
  onRevokeEdge: (id: string) => Promise<any>;
}

export default function TrustGraph({ nodes, edges, onRevokeEdge }: TrustGraphProps) {
  const [selectedNode, setSelectedNode] = useState<TrustNode | null>(null);
  const [selectedEdge, setSelectedEdge] = useState<TrustEdge | null>(null);
  const [activeTab, setActiveTab] = useState<"visual" | "table">("visual");

  // Filtering States
  const [tenantFilter, setTenantFilter] = useState<string>("all");
  const [roleFilter, setRoleFilter] = useState<string>("all");
  const [statusFilter, setStatusFilter] = useState<string>("all");

  const isNodeFiltered = (n: TrustNode) => {
    if (tenantFilter === "all" && roleFilter === "all" && statusFilter === "all") {
      return true;
    }
    // Tenant filter
    if (tenantFilter !== "all") {
      let nodeTenant = "global";
      if (n.entityId.includes("gov.se") || n.entityId.includes("sweden")) {
        nodeTenant = "se-gov";
      } else if (n.entityId.includes("edugain")) {
        nodeTenant = "edugain";
      } else if (n.entityId.includes("okta") || n.entityId.includes("tenant-default") || n.entityId.includes("tigrbl")) {
        nodeTenant = "tenant-default";
      }
      if (nodeTenant !== tenantFilter) return false;
    }
    // Role filter
    if (roleFilter !== "all") {
      if (n.type !== roleFilter) return false;
    }
    // Status filter
    if (statusFilter !== "all") {
      if (statusFilter === "revoked") {
        return false;
      } else if (n.health !== statusFilter) {
        return false;
      }
    }
    return true;
  };

  const isEdgeFiltered = (e: TrustEdge) => {
    const sourceNode = nodes.find(n => n.id === e.source);
    const targetNode = nodes.find(n => n.id === e.target);
    if (!sourceNode || !targetNode) return false;

    if (tenantFilter === "all" && roleFilter === "all" && statusFilter === "all") {
      return true;
    }

    if (statusFilter === "revoked") {
      return e.state === "revoked";
    }

    if (!isNodeFiltered(sourceNode) || !isNodeFiltered(targetNode)) {
      return false;
    }

    return true;
  };

  // Dynamic Path Resolution Sim State
  const [pathResult, setPathResult] = useState<any>(null);
  const [blastResult, setBlastResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  // SVG Coordinates lookup for predictability and perfect alignment
  const coordinates: Record<string, { x: number; y: number }> = {
    "n-root": { x: 120, y: 70 },
    "n-se-gov": { x: 380, y: 70 },
    "n-edugain": { x: 640, y: 70 },
    "n-inter-se": { x: 380, y: 190 },
    "n-inter-edu": { x: 640, y: 190 },
    "n-leaf-okta": { x: 120, y: 310 },
    "n-leaf-swedish": { x: 380, y: 310 },
    "n-leaf-edugain": { x: 640, y: 310 },
    "n-rp-portal": { x: 380, y: 430 },
  };

  const handleNodeClick = async (node: TrustNode) => {
    setSelectedNode(node);
    setSelectedEdge(null);
    setBlastResult(null);
    setLoading(true);

    try {
      // Resolve path up to corresponding anchor
      let anchorId = "https://trust.auth.tigrbl.com";
      if (node.entityId.includes("sweden") || node.entityId.includes("gov.se")) {
        anchorId = "https://trust.gov.se/federation";
      } else if (node.entityId.includes("edugain")) {
        anchorId = "https://edugain.org/anchor";
      }

      const res = await fetch("/api/federation/trust-paths:resolve", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ leafEntityId: node.entityId, anchorEntityId: anchorId }),
      });
      const data = await res.json();
      setPathResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleEdgeClick = (edge: TrustEdge) => {
    setSelectedEdge(edge);
    setSelectedNode(null);
    setPathResult(null);
    setBlastResult(null);
  };

  const handleSimulateRevocation = async (edgeId: string) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/federation/edges/${edgeId}/revoke`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
      });
      const data = await res.json();
      setBlastResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6" id="trust-graph-surface">
      {/* Visual Header / Controls */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3">
        <div>
          <h3 className="text-base font-semibold text-white flex items-center gap-1.5">
            <Network className="h-5 w-5 text-indigo-400" />
            Multilateral Trust Graph Explorer
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Visualize certificates, trust anchors, intermediates, and assess the blast radius of edge revocation.
          </p>
        </div>
        <div className="flex bg-slate-950 p-1 rounded-lg border border-slate-850">
          <button
            onClick={() => setActiveTab("visual")}
            className={`px-3 py-1 text-xs font-semibold rounded-md transition ${
              activeTab === "visual" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
            }`}
          >
            Interactive Diagram
          </button>
          <button
            onClick={() => setActiveTab("table")}
            className={`px-3 py-1 text-xs font-semibold rounded-md transition ${
              activeTab === "table" ? "bg-indigo-600 text-white" : "text-slate-400 hover:text-white"
            }`}
            id="accessible-table-tab"
          >
            Tabular Hierarchy (Accessible)
          </button>
        </div>
      </div>

      {/* Filter Options Control Row */}
      <div className="bg-slate-900/40 p-4 rounded-xl border border-slate-850/60 grid grid-cols-1 sm:grid-cols-3 gap-4" id="trust-graph-filters">
        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Filter by Tenant</label>
          <select
            value={tenantFilter}
            onChange={(e) => setTenantFilter(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-600 transition"
          >
            <option value="all">All Tenants (Global View)</option>
            <option value="tenant-default">Default Tenant (tenant-default)</option>
            <option value="se-gov">Swedish Government (se-gov)</option>
            <option value="edugain">eduGAIN Academic (edugain)</option>
          </select>
        </div>

        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Filter by Role</label>
          <select
            value={roleFilter}
            onChange={(e) => setRoleFilter(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-600 transition"
          >
            <option value="all">All Roles</option>
            <option value="anchor">Trust Anchor (Root)</option>
            <option value="intermediate">Intermediate Authority</option>
            <option value="op">Identity Provider (OP)</option>
            <option value="rp">Relying Party (RP)</option>
          </select>
        </div>

        <div className="space-y-1.5">
          <label className="text-[10px] font-bold text-slate-400 uppercase tracking-wider block">Filter by Status</label>
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-lg px-3 py-1.5 text-xs text-slate-200 focus:outline-none focus:border-indigo-600 transition"
          >
            <option value="all">All Statuses</option>
            <option value="healthy">Healthy</option>
            <option value="degraded">Degraded</option>
            <option value="failing">Failing</option>
            <option value="revoked">Revoked (Relationships)</option>
          </select>
        </div>
      </div>

      {/* Main Split Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Visualization Stage */}
        <div className="lg:col-span-2 bg-slate-950/40 border border-slate-850 rounded-xl p-4 relative min-h-[480px] flex items-center justify-center">
          {activeTab === "visual" ? (
            <svg
              viewBox="0 0 760 500"
              className="w-full h-auto max-w-4xl"
              id="trust-graph-svg"
            >
              {/* Define markers/gradients for beautiful paths */}
              <defs>
                <marker
                  id="arrow"
                  viewBox="0 0 10 10"
                  refX="18"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#334155" />
                </marker>
                <marker
                  id="arrow-revoked"
                  viewBox="0 0 10 10"
                  refX="18"
                  refY="5"
                  markerWidth="6"
                  markerHeight="6"
                  orient="auto-start-reverse"
                >
                  <path d="M 0 0 L 10 5 L 0 10 z" fill="#ef4444" />
                </marker>
              </defs>

              {/* Render edges */}
              {edges.map((e) => {
                const sourceCoord = coordinates[e.source];
                const targetCoord = coordinates[e.target];
                if (!sourceCoord || !targetCoord) return null;

                const isSelected = selectedEdge?.id === e.id;
                const isRevoked = e.state === "revoked";
                const isFiltered = isEdgeFiltered(e);

                return (
                  <g
                    key={e.id}
                    className={`cursor-pointer transition duration-300 ${isFiltered ? "opacity-100" : "opacity-15 pointer-events-none"}`}
                    onClick={() => handleEdgeClick(e)}
                  >
                    <line
                      x1={sourceCoord.x}
                      y1={sourceCoord.y}
                      x2={targetCoord.x}
                      y2={targetCoord.y}
                      stroke={isRevoked ? "#ef4444" : isSelected ? "#6366f1" : "#334155"}
                      strokeWidth={isSelected ? 3 : 1.5}
                      strokeDasharray={e.exchangeKind === "subordinate" ? "5,5" : "none"}
                      markerEnd={isRevoked ? "url(#arrow-revoked)" : "url(#arrow)"}
                      className="transition duration-200"
                    />
                    {/* Tiny edge label tag */}
                    <circle
                      cx={(sourceCoord.x + targetCoord.x) / 2}
                      cy={(sourceCoord.y + targetCoord.y) / 2}
                      r="4"
                      fill={isRevoked ? "#ef4444" : isSelected ? "#6366f1" : "#475569"}
                    />
                  </g>
                );
              })}

              {/* Render Nodes */}
              {nodes.map((n) => {
                const coord = coordinates[n.id];
                if (!coord) return null;

                const isSelected = selectedNode?.id === n.id;
                const isFiltered = isNodeFiltered(n);
                
                // Color codes based on node type
                let strokeColor = "#334155";
                let fillColor = "#0f172a";
                let badgeSymbol = "●";

                if (n.type === "anchor") {
                  strokeColor = "#eab308"; // Gold
                  fillColor = "#1e1b4b";
                  badgeSymbol = "⚓";
                } else if (n.type === "intermediate") {
                  strokeColor = "#a855f7"; // Purple
                  fillColor = "#1a103c";
                  badgeSymbol = "❖";
                } else if (n.type === "op") {
                  strokeColor = "#10b981"; // Emerald OP
                  fillColor = "#022c22";
                } else if (n.type === "rp") {
                  strokeColor = "#06b6d4"; // Teal RP
                  fillColor = "#083344";
                }

                // If node is failing, force red border
                if (n.health === "failing") {
                  strokeColor = "#ef4444";
                }

                return (
                  <g
                    key={n.id}
                    transform={`translate(${coord.x}, ${coord.y})`}
                    className={`cursor-pointer group select-none transition duration-300 ${isFiltered ? "opacity-100" : "opacity-15 pointer-events-none"}`}
                    onClick={() => handleNodeClick(n)}
                  >
                    <circle
                      r={n.type === "anchor" ? 22 : 18}
                      fill={fillColor}
                      stroke={isSelected ? "#818cf8" : strokeColor}
                      strokeWidth={isSelected ? 3 : 2}
                      className="transition duration-200 group-hover:scale-110"
                    />
                    <text
                      textAnchor="middle"
                      dy=".3em"
                      fill="#ffffff"
                      fontSize={n.type === "anchor" ? "12px" : "10px"}
                      className="font-mono"
                    >
                      {badgeSymbol}
                    </text>
                    {/* Node label */}
                    <text
                      y={n.type === "anchor" ? 38 : 34}
                      textAnchor="middle"
                      fill="#e2e8f0"
                      fontSize="9px"
                      fontWeight="600"
                      className="bg-slate-900 pointer-events-none"
                    >
                      {n.label}
                    </text>
                    {/* Tiny Health indicator */}
                    <circle
                      cx={12}
                      cy={-12}
                      r="4"
                      fill={
                        n.health === "healthy" ? "#10b981" :
                        n.health === "degraded" ? "#fbbf24" :
                        "#ef4444"
                      }
                    />
                  </g>
                );
              })}
            </svg>
          ) : (
            /* Accessible Tabular Tree Fallback */
            <div className="w-full p-4 space-y-6" id="accessible-hierarchy-table">
              <div className="text-xs text-slate-400 font-semibold uppercase tracking-wider">
                Authority Path Heirarchy Data Grid
              </div>
              
              <div className="space-y-4">
                {/* Section 1: Anchors */}
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-yellow-500 uppercase">Trust Anchors (Roots)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    {nodes.filter(n => n.type === "anchor").filter(isNodeFiltered).map(n => (
                      <div key={n.id} className="bg-slate-900 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                        <div className="space-y-1">
                          <div className="text-xs font-semibold text-white">{n.label}</div>
                          <div className="text-[10px] text-slate-500 font-mono">{n.entityId}</div>
                        </div>
                        <button onClick={() => handleNodeClick(n)} className="px-2 py-1 bg-slate-800 text-[10px] rounded text-indigo-400 font-bold hover:bg-slate-700">
                          Verify
                        </button>
                      </div>
                    ))}
                    {nodes.filter(n => n.type === "anchor").filter(isNodeFiltered).length === 0 && (
                      <div className="col-span-full text-xs text-slate-500 italic py-2">No matching trust anchors found.</div>
                    )}
                  </div>
                </div>

                {/* Section 2: Intermediates */}
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-purple-400 uppercase">Trust Intermediates</h4>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
                    {nodes.filter(n => n.type === "intermediate").filter(isNodeFiltered).map(n => (
                      <div key={n.id} className="bg-slate-900 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                        <div className="space-y-1">
                          <div className="text-xs font-semibold text-white">{n.label}</div>
                          <div className="text-[10px] text-slate-500 font-mono">{n.entityId}</div>
                        </div>
                        <button onClick={() => handleNodeClick(n)} className="px-2 py-1 bg-slate-800 text-[10px] rounded text-indigo-400 font-bold hover:bg-slate-700">
                          Verify
                        </button>
                      </div>
                    ))}
                    {nodes.filter(n => n.type === "intermediate").filter(isNodeFiltered).length === 0 && (
                      <div className="col-span-full text-xs text-slate-500 italic py-2">No matching trust intermediates found.</div>
                    )}
                  </div>
                </div>

                {/* Section 3: Leaf providers */}
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-emerald-400 uppercase">Federated Identity Providers (Leaf OPs)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    {nodes.filter(n => n.type === "op").filter(isNodeFiltered).map(n => (
                      <div key={n.id} className="bg-slate-900 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                        <div className="space-y-1">
                          <div className="text-xs font-semibold text-white">{n.label}</div>
                          <div className="text-[10px] text-slate-500 font-mono">{n.entityId}</div>
                        </div>
                        <button onClick={() => handleNodeClick(n)} className="px-2 py-1 bg-slate-800 text-[10px] rounded text-indigo-400 font-bold hover:bg-slate-700">
                          Verify
                        </button>
                      </div>
                    ))}
                    {nodes.filter(n => n.type === "op").filter(isNodeFiltered).length === 0 && (
                      <div className="col-span-full text-xs text-slate-500 italic py-2">No matching identity providers found.</div>
                    )}
                  </div>
                </div>

                {/* Section 4: Relying Parties */}
                <div className="space-y-2">
                  <h4 className="text-xs font-bold text-cyan-400 uppercase">Federated Relying Parties (Leaf RPs)</h4>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                    {nodes.filter(n => n.type === "rp").filter(isNodeFiltered).map(n => (
                      <div key={n.id} className="bg-slate-900 p-3 rounded-lg border border-slate-800 flex justify-between items-center">
                        <div className="space-y-1">
                          <div className="text-xs font-semibold text-white">{n.label}</div>
                          <div className="text-[10px] text-slate-500 font-mono">{n.entityId}</div>
                        </div>
                        <button onClick={() => handleNodeClick(n)} className="px-2 py-1 bg-slate-800 text-[10px] rounded text-cyan-400 font-bold hover:bg-slate-700">
                          Verify
                        </button>
                      </div>
                    ))}
                    {nodes.filter(n => n.type === "rp").filter(isNodeFiltered).length === 0 && (
                      <div className="col-span-full text-xs text-slate-500 italic py-2">No matching relying parties found.</div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Right Column: Statement Inspector and Blast Radius Calculator */}
        <div className="bg-slate-900/30 border border-slate-800 rounded-xl p-5 space-y-6">
          {/* Default view */}
          {!selectedNode && !selectedEdge && (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 space-y-3">
              <Network className="h-10 w-10 text-slate-700 animate-pulse" />
              <div>
                <h4 className="text-sm font-semibold text-white">No Graph Item Selected</h4>
                <p className="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
                  Click on any shield/diamond node to verify its signed statement, or select any connecting line to simulate trust revocation blast radius.
                </p>
              </div>
            </div>
          )}

          {/* Node Selected view */}
          {selectedNode && (
            <div className="space-y-4" id="node-details-card">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">{selectedNode.type} detail</span>
                  <h4 className="text-sm font-bold text-white mt-1">{selectedNode.label}</h4>
                </div>
                <span className={`px-2 py-0.5 rounded text-[10px] uppercase font-bold ${
                  selectedNode.health === "healthy" ? "bg-emerald-950 text-emerald-400" :
                  selectedNode.health === "degraded" ? "bg-amber-950 text-amber-400" :
                  "bg-red-950 text-red-400"
                }`}>
                  {selectedNode.health}
                </span>
              </div>

              <div className="space-y-1.5 font-mono text-[11px] bg-slate-950 p-3 rounded border border-slate-850">
                <div className="text-slate-500 uppercase text-[9px] font-sans font-bold">Entity Identifier</div>
                <div className="text-slate-300 break-all select-all">{selectedNode.entityId}</div>
              </div>

              {/* Trust Chain Path Resolution Findings */}
              {loading ? (
                <div className="py-8 flex justify-center">
                  <RefreshCw className="h-5 w-5 animate-spin text-indigo-400" />
                </div>
              ) : pathResult ? (
                <div className="space-y-4 pt-4 border-t border-slate-850">
                  <div className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1">
                    <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                    Chain Resolution Path
                  </div>

                  <div className="space-y-3">
                    {pathResult.validationHops.map((hop: any, idx: number) => (
                      <div key={idx} className="bg-slate-950 p-3 rounded border border-slate-850 space-y-1">
                        <div className="flex justify-between text-[10px] font-semibold text-indigo-400">
                          <span>HOP {idx + 1}</span>
                          <span className={hop.signatureValid ? "text-emerald-400" : "text-red-400 font-bold"}>
                            {hop.signatureValid ? "SIGNATURE VALID" : "SIGNATURE INVALID"}
                          </span>
                        </div>
                        <div className="text-xs text-white font-mono mt-1">{hop.issuer}</div>
                        <p className="text-[11px] text-slate-400 mt-1 leading-relaxed">
                          {hop.findings}
                        </p>
                      </div>
                    ))}
                  </div>

                  <div className="space-y-1">
                    <div className="text-slate-500 uppercase text-[9px] font-sans font-bold">Resolved Metadata Payload</div>
                    <CodeBlock
                      code={pathResult.resolvedMetadata}
                      language="json"
                      maxHeight="max-h-36"
                    />
                  </div>
                </div>
              ) : null}
            </div>
          )}

          {/* Edge Selected view */}
          {selectedEdge && (
            <div className="space-y-5" id="edge-details-card">
              <div>
                <span className="text-[10px] font-bold text-indigo-400 uppercase tracking-wider">Directed Trust Relationship</span>
                <h4 className="text-sm font-bold text-white mt-1">Edge ID: {selectedEdge.id}</h4>
              </div>

              <div className="grid grid-cols-2 gap-3 text-xs bg-slate-950 p-4 rounded border border-slate-850 font-mono">
                <div>
                  <span className="text-[10px] text-slate-500 font-sans font-bold block">RELATIONSHIP</span>
                  <span className="text-slate-300 uppercase">{selectedEdge.exchangeKind}</span>
                </div>
                <div>
                  <span className="text-[10px] text-slate-500 font-sans font-bold block">STATUS</span>
                  <span className={`uppercase font-bold ${selectedEdge.state === "active" ? "text-emerald-400" : "text-red-400"}`}>
                    {selectedEdge.state}
                  </span>
                </div>
                <div className="col-span-2">
                  <span className="text-[10px] text-slate-500 font-sans font-bold block">VALID UNTIL</span>
                  <span className="text-slate-300">{new Date(selectedEdge.validUntil).toLocaleString()}</span>
                </div>
              </div>

              {/* Edge Revoke simulated quarantine controls */}
              <div className="space-y-3 pt-4 border-t border-slate-850">
                <div className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1 text-red-400">
                  <ShieldAlert className="h-4 w-4" />
                  Emergency Quarantine Controls
                </div>

                <p className="text-xs text-slate-400 leading-relaxed">
                  Revoking this relationship isolates subordinate statements instantly. Users routing via matching issuers will fail-closed.
                </p>

                {selectedEdge.state === "active" && (
                  <button
                    type="button"
                    onClick={() => handleSimulateRevocation(selectedEdge.id)}
                    className="w-full py-2 bg-red-950/40 hover:bg-red-900/60 text-red-200 border border-red-800 rounded text-xs font-semibold flex items-center justify-center gap-1.5 transition"
                  >
                    <Trash2 className="h-4 w-4" />
                    Simulate Revocation Impact
                  </button>
                )}

                {/* Blast Radius Result */}
                {loading ? (
                  <div className="py-4 flex justify-center">
                    <RefreshCw className="h-4 w-4 animate-spin text-red-400" />
                  </div>
                ) : blastResult ? (
                  <div className="bg-red-950/20 border border-red-900/40 p-4 rounded-lg space-y-3" id="blast-radius-box">
                    <div className="text-xs font-bold text-white uppercase tracking-wider flex items-center gap-1.5">
                      <AlertTriangle className="h-4 w-4 text-red-500 animate-pulse" />
                      Calculated Blast Radius
                    </div>

                    <div className="grid grid-cols-3 gap-2 text-center">
                      <div className="bg-slate-950 p-2 rounded border border-slate-850">
                        <div className="text-lg font-bold text-white">{blastResult.blastRadius.affectedTenants}</div>
                        <div className="text-[8px] text-slate-500 uppercase">Tenants</div>
                      </div>
                      <div className="bg-slate-950 p-2 rounded border border-slate-850">
                        <div className="text-lg font-bold text-white">{blastResult.blastRadius.affectedApps}</div>
                        <div className="text-[8px] text-slate-500 uppercase">Apps</div>
                      </div>
                      <div className="bg-slate-950 p-2 rounded border border-slate-850">
                        <div className="text-lg font-bold text-white">{blastResult.blastRadius.affectedSessions}</div>
                        <div className="text-[8px] text-slate-500 uppercase">Sessions</div>
                      </div>
                    </div>

                    <div className="space-y-1 bg-slate-950 p-3 rounded border border-slate-850">
                      <span className="text-[9px] text-indigo-400 font-semibold uppercase flex items-center gap-1">
                        <Sparkles className="h-3.5 w-3.5" />
                        Platform Containment Advice
                      </span>
                      <p className="text-xs text-slate-300 italic mt-1 leading-relaxed">
                        "{blastResult.recommendations}"
                      </p>
                    </div>

                    <button
                      onClick={() => onRevokeEdge(selectedEdge.id)}
                      className="w-full py-2 bg-red-600 hover:bg-red-500 text-white text-xs font-bold rounded flex items-center justify-center gap-1.5 transition"
                    >
                      <ShieldAlert className="h-4 w-4" />
                      Commit Emergency Revocation
                    </button>
                  </div>
                ) : null}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
