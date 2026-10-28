import React, { useState, useEffect } from "react";
import {
  FileText,
  RefreshCw,
  GitCommit,
  CheckCircle2,
  XCircle,
  AlertTriangle,
  ArrowRight,
  ShieldCheck,
  FileJson,
  Sparkles,
  HelpCircle,
} from "lucide-react";
import { FederationConnection } from "../types";
import CodeBlock from "./CodeBlock";

interface ChainInspectorProps {
  connections: FederationConnection[];
}

export default function ChainInspector({ connections }: ChainInspectorProps) {
  const [selectedConnId, setSelectedConnId] = useState("");
  const [activeTab, setActiveTab] = useState<"statement" | "diff" | "policy">("statement");
  
  // Diff simulation state
  const [diffData, setDiffData] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (connections.length > 0 && !selectedConnId) {
      setSelectedConnId(connections[0].id);
    }
  }, [connections, selectedConnId]);

  const activeConn = connections.find((c) => c.id === selectedConnId);

  const fetchMetadataDiff = async (connId: string) => {
    setLoading(true);
    try {
      const res = await fetch(`/api/federation/connections/${connId}/metadata:diff`);
      const data = await res.json();
      setDiffData(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (selectedConnId) {
      fetchMetadataDiff(selectedConnId);
    }
  }, [selectedConnId]);

  // Mock policy transformations applied for OpenID Federation 1.0 (Sec 5)
  const mockTransformations = [
    { step: 1, name: "Resolve Trust Anchor Constraints", action: "Load allowed key algorithm set", result: "Permitted: RS256, ES256, ES384. Rejection of: 'none'" },
    { step: 2, name: "Apply Regional Authority Policy", action: "Limit token endpoint response modes", result: "Enforce: 'fragment', 'query_jwt' standard outputs only" },
    { step: 3, name: "Claim Restriction Filter", action: "Filter non-authorized scope attributes", result: "Removed: 'internal_clearance_id' from final metadata block" },
    { step: 4, name: "Derive Final Metadata Output", action: "Construct effective OIDC provider config", result: "Compilation complete with deterministic cached hash signature." }
  ];

  return (
    <div className="bg-slate-900/30 border border-slate-800 rounded-2xl p-6" id="chain-inspector-surface">
      {/* Selector Area */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-850 pb-5 mb-6">
        <div>
          <h3 className="text-base font-semibold text-white flex items-center gap-1.5">
            <FileText className="h-5 w-5 text-indigo-400" />
            Metadata & Signed Chain Inspector
          </h3>
          <p className="text-xs text-slate-400 mt-0.5">
            Compare active and candidate keys, trace metadata transformation steps, and inspect JOSE headers.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400">Connection:</span>
          <select
            value={selectedConnId}
            onChange={(e) => setSelectedConnId(e.target.value)}
            className="px-3 py-1.5 bg-slate-950 border border-slate-800 rounded-lg text-xs text-white focus:outline-none"
            id="conn-inspector-selector"
          >
            {connections.map((c) => (
              <option key={c.id} value={c.id}>
                {c.displayName} ({c.protocol === "OPENID_FEDERATION" ? "OpenID Fed" : "OIDC"})
              </option>
            ))}
          </select>
        </div>
      </div>

      {activeConn ? (
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Sub Navigation */}
          <div className="lg:col-span-1 space-y-2">
            {[
              { id: "statement", label: "Signed Statements (JWT)" },
              { id: "diff", label: "Semantic Metadata Diff" },
              { id: "policy", label: "Metadata Policy (Sec 5)" },
            ].map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id as any)}
                className={`w-full text-left px-4 py-2.5 rounded-lg text-xs font-semibold flex items-center justify-between transition ${
                  activeTab === tab.id
                    ? "bg-indigo-600/10 border border-indigo-800/80 text-white"
                    : "bg-transparent text-slate-400 hover:bg-slate-850 hover:text-white"
                }`}
              >
                <span>{tab.label}</span>
                <ArrowRight className="h-3 w-3" />
              </button>
            ))}

            {/* Quick Connection Health widget */}
            <div className="mt-6 bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-3">
              <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Health Assessment</span>
              <div className="flex items-center gap-2">
                <span className={`h-2.5 w-2.5 rounded-full ${
                  activeConn.health === "healthy" ? "bg-emerald-500" :
                  activeConn.health === "degraded" ? "bg-amber-400" :
                  "bg-red-500"
                }`}></span>
                <span className="text-xs text-slate-300 font-semibold uppercase">{activeConn.health}</span>
              </div>
              <div className="text-[10px] text-slate-500 leading-relaxed">
                Last validated: {activeConn.lastValidation ? new Date(activeConn.lastValidation).toLocaleString() : "Never"}
              </div>
            </div>
          </div>

          {/* Detailed Workspace */}
          <div className="lg:col-span-3 space-y-6">
            {/* Tab 1: Signed Statements Details */}
            {activeTab === "statement" && (
              <div className="space-y-6" id="inspector-statement-tab">
                {/* Header warning */}
                {activeConn.health !== "healthy" && activeConn.errorMessage && (
                  <div className="bg-amber-950/20 border border-amber-800/50 p-4 rounded-xl text-amber-300 text-xs flex items-start gap-3">
                    <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5 text-amber-400" />
                    <div>
                      <span className="font-semibold text-white">Active Cryptographic Signal Alert:</span>
                      <p className="mt-1 text-amber-200">{activeConn.errorMessage}</p>
                    </div>
                  </div>
                )}

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  {/* Left: Metadata properties */}
                  <div className="space-y-4">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Statement Provenance</h4>
                    
                    <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-3 font-mono text-xs text-slate-300">
                      <div>
                        <span className="text-[10px] text-slate-500 font-sans font-bold block">ISSUER</span>
                        <span className="break-all">{activeConn.issuer}</span>
                      </div>
                      <div className="grid grid-cols-2 gap-2">
                        <div>
                          <span className="text-[10px] text-slate-500 font-sans font-bold block">SIGNING ALGORITHM</span>
                          <span>RS256</span>
                        </div>
                        <div>
                          <span className="text-[10px] text-slate-500 font-sans font-bold block">KEY ID (kid)</span>
                          <span>{activeConn.id === "conn-edu-gain" ? "edugain-key-3" : "key-okta-v1"}</span>
                        </div>
                      </div>
                      <div>
                        <span className="text-[10px] text-slate-500 font-sans font-bold block">LAST REFRESH CACHE DIGEST</span>
                        <span className="text-indigo-400">{activeConn.lastKnownGoodDigest || "None recorded"}</span>
                      </div>
                    </div>
                  </div>

                  {/* Right: JOSE Headers and claims inspect */}
                  <div className="space-y-4">
                    <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Signed Statement JWT Mock Header</h4>
                    <CodeBlock
                      code={{
                        "alg": "RS255",
                        "typ": "entity-statement+jwt",
                        "kid": activeConn.id === "conn-edu-gain" ? "edugain-key-3" : "key-okta-v1"
                      }}
                      language="json"
                      maxHeight="max-h-56"
                    />
                  </div>
                </div>
              </div>
            )}

            {/* Tab 2: Semantic Metadata Diff */}
            {activeTab === "diff" && (
              <div className="space-y-6" id="inspector-diff-tab">
                {loading ? (
                  <div className="py-12 flex justify-center">
                    <RefreshCw className="h-6 w-6 animate-spin text-indigo-400" />
                  </div>
                ) : diffData ? (
                  <div className="space-y-4">
                    <div className="bg-indigo-950/20 border border-indigo-850 p-4 rounded-xl flex items-start gap-3">
                      <Sparkles className="h-5 w-5 text-indigo-400 mt-0.5 shrink-0" />
                      <div>
                        <h4 className="text-xs font-bold text-white uppercase tracking-wider">Semantic Drift Explainer (Gemini Analysed)</h4>
                        <p className="text-xs text-indigo-200 mt-1 italic leading-relaxed">
                          "{diffData.diffSummary}"
                        </p>
                      </div>
                    </div>

                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
                      <div className="space-y-2">
                        <span className="text-[10px] font-sans font-bold text-slate-500 uppercase">PINNED ACTIVE METADATA</span>
                        <CodeBlock
                          code={diffData.activeMetadata}
                          language="json"
                          maxHeight="max-h-60"
                        />
                      </div>
                      <div className="space-y-2">
                        <span className="text-[10px] font-sans font-bold text-indigo-400 uppercase">CANDIDATE / OBSERVED REMOTE METADATA</span>
                        <CodeBlock
                          code={diffData.currentMetadata}
                          language="json"
                          maxHeight="max-h-60"
                        />
                      </div>
                    </div>
                  </div>
                ) : null}
              </div>
            )}

            {/* Tab 3: Policy Transformation Trace */}
            {activeTab === "policy" && (
              <div className="space-y-6" id="inspector-policy-tab">
                <div className="flex items-center gap-1.5 text-xs text-slate-400">
                  <ShieldCheck className="h-4 w-4 text-emerald-400" />
                  OpenID Federation Section 5 Metadata Policy Execution Timeline
                </div>

                <div className="relative border-l border-slate-800 ml-3 pl-6 space-y-6">
                  {mockTransformations.map((t) => (
                    <div key={t.step} className="relative">
                      {/* Timeline dot */}
                      <span className="absolute -left-[31px] top-1 bg-slate-950 border border-indigo-500 rounded-full h-4 w-4 flex items-center justify-center text-[9px] font-bold text-indigo-300">
                        {t.step}
                      </span>
                      <div className="space-y-1 bg-slate-950/40 border border-slate-850 p-4 rounded-xl">
                        <h4 className="text-xs font-semibold text-white">{t.name}</h4>
                        <div className="text-[11px] text-slate-500 font-mono mt-1">ACTION: {t.action}</div>
                        <div className="mt-2">
                          <CodeBlock
                            code={t.result}
                            language="logs"
                            maxHeight="max-h-24"
                          />
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="text-center py-12 text-slate-500">
          No connections currently drafted or active. Use Connection Wizard to begin.
        </div>
      )}
    </div>
  );
}
