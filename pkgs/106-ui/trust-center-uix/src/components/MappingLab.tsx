import React, { useState } from "react";
import {
  Sparkles,
  HelpCircle,
  Play,
  ArrowRight,
  ShieldCheck,
  Code,
  Users,
  AlertTriangle,
  Activity,
  Plus,
  Trash2,
  RefreshCw,
} from "lucide-react";
import { ClaimMapping } from "../types";
import CodeBlock from "./CodeBlock";

export default function MappingLab() {
  const [sourceClaimsText, setSourceClaimsText] = useState(
    JSON.stringify(
      {
        iss: "https://partner-auth.acme.com",
        sub: "user_id_acme_alice_909",
        email: "ALICE.SECURE@ACME.COM",
        first_name: "Alice",
        last_name: "Acme-Operator",
        roles: "administrators, cloud-operators, security-leads",
        seCivicNumber: "19940412-1234",
      },
      null,
      2
    )
  );

  const [claimMappings, setClaimMappings] = useState<ClaimMapping[]>([
    { id: "m1", sourceSelector: "sub", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
    { id: "m2", sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" },
    { id: "m3", sourceSelector: "first_name", normalizedTarget: "first_name", transformation: "as-is", required: false, privacyClass: "public" },
    { id: "m4", sourceSelector: "roles", normalizedTarget: "assigned_groups", transformation: "split", required: false, privacyClass: "sensitive" },
    { id: "m5", sourceSelector: "seCivicNumber", normalizedTarget: "national_identifier", transformation: "as-is", required: false, privacyClass: "sensitive" },
  ]);

  // Run State
  const [loading, setLoading] = useState(false);
  const [normalizedResult, setNormalizedResult] = useState<any | null>(null);
  const [runLogs, setRunLogs] = useState<string[]>([]);
  const [aiReport, setAiReport] = useState("");

  // Routing Simulator State
  const [simEmail, setSimEmail] = useState("alice@partner.com");
  const [simTenant, setSimTenant] = useState("tenant-default");
  const [simApp, setSimApp] = useState("tigrbl-console-app");
  const [routingMatch, setRoutingMatch] = useState<any | null>(null);

  const handleClaimMappingAdd = () => {
    const newM: ClaimMapping = {
      id: `m-dyn-${Date.now()}`,
      sourceSelector: "",
      normalizedTarget: "",
      transformation: "as-is",
      required: false,
      privacyClass: "public",
    };
    setClaimMappings([...claimMappings, newM]);
  };

  const handleClaimMappingDelete = (id: string) => {
    setClaimMappings(claimMappings.filter((m) => m.id !== id));
  };

  const handleRunNormalization = async () => {
    setLoading(true);
    setNormalizedResult(null);
    setRunLogs([]);
    setAiReport("");

    try {
      let parsedSource = {};
      try {
        parsedSource = JSON.parse(sourceClaimsText);
      } catch (e) {
        alert("Invalid input Source Claims JSON structure.");
        setLoading(false);
        return;
      }

      const res = await fetch("/api/federation/claims:simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          sourceClaims: parsedSource,
          mappings: claimMappings,
        }),
      });

      const data = await res.json();
      if (res.ok) {
        setNormalizedResult(data.normalizedClaims);
        setRunLogs(data.logs);
        setAiReport(data.safetyAnalysis);
      } else {
        alert(data.error || "Failed to normalize claims");
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleRunRoutingSim = () => {
    // Basic home-realm rules evaluation
    const domain = simEmail.split("@")[1] || "";
    let matchText = "";
    let score = 0;

    if (domain === "partner.com") {
      matchText = "MATCH FOUND: Rule priority 10 matches domain 'partner.com'. Routed directly to connection 'conn-okta-workplace'.";
      score = 10;
    } else if (domain.endsWith(".se")) {
      matchText = "MATCH FOUND: Rule priority 5 matches domain '*.se'. Routed directly to Swedish Govt Node.";
      score = 5;
    } else {
      matchText = "FALLBACK TRIGGERED: No explicit domain match. Prompt User with Allowed Multi-Tenant Selector Screen.";
      score = 0;
    }

    setRoutingMatch({ matchText, score, evaluatedRulesCount: 3 });
  };

  return (
    <div className="space-y-6" id="mapping-lab-surface">
      {/* Tab selection */}
      <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800 backdrop-blur-md">
        <h2 className="text-xl font-semibold text-white flex items-center gap-2">
          <Code className="h-5 w-5 text-indigo-400" />
          Claims Normalization Lab & Routing Simulator
        </h2>
        <p className="text-sm text-slate-400 mt-1">
          Perform live claim transformation audits, review PII leakage hazards, and test priority routing weights.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Playbook / Input stage (Left 2 Columns) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Claims Mapper Sandbox */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-sm font-semibold text-white">Upstream JSON Token Payload</h3>
              <span className="text-[10px] text-slate-500 font-mono">Simulated JWT Claims (Editable)</span>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-1.5">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Raw JSON Editor</span>
                <textarea
                  value={sourceClaimsText}
                  onChange={(e) => setSourceClaimsText(e.target.value)}
                  className="w-full h-[180px] px-4 py-3 bg-slate-900 border border-slate-800 rounded-lg text-xs font-mono text-slate-300 focus:outline-none focus:border-indigo-500 resize-none"
                  id="source-claims-textarea"
                />
              </div>
              <div className="space-y-1.5">
                <span className="text-[10px] text-slate-500 uppercase font-bold">Live Syntax Highlights</span>
                <CodeBlock
                  code={sourceClaimsText}
                  language="json"
                  maxHeight="max-h-[180px]"
                />
              </div>
            </div>
          </div>

          {/* Rules Builder */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h3 className="text-sm font-semibold text-white">Active Mapping Presets</h3>
                <p className="text-xs text-slate-500">Transformations are applied in real-time on connection callbacks.</p>
              </div>
              <button
                type="button"
                onClick={handleClaimMappingAdd}
                className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-indigo-400 border border-slate-700 rounded text-xs font-semibold flex items-center gap-1 transition"
              >
                <Plus className="h-3 w-3" /> Add Transformation Line
              </button>
            </div>

            <div className="space-y-3">
              {claimMappings.map((m, idx) => (
                <div key={m.id} className="grid grid-cols-1 sm:grid-cols-5 gap-3 bg-slate-900 p-3 rounded-lg border border-slate-800 items-center">
                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Source Selector</span>
                    <input
                      type="text"
                      value={m.sourceSelector}
                      onChange={(e) => {
                        const updated = [...claimMappings];
                        updated[idx].sourceSelector = e.target.value;
                        setClaimMappings(updated);
                      }}
                      className="w-full px-2 py-1 bg-slate-950 border border-slate-800 text-xs rounded text-white font-mono"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Normalized Target</span>
                    <input
                      type="text"
                      value={m.normalizedTarget}
                      onChange={(e) => {
                        const updated = [...claimMappings];
                        updated[idx].normalizedTarget = e.target.value;
                        setClaimMappings(updated);
                      }}
                      className="w-full px-2 py-1 bg-slate-950 border border-slate-800 text-xs rounded text-white font-mono"
                    />
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Transformation</span>
                    <select
                      value={m.transformation}
                      onChange={(e) => {
                        const updated = [...claimMappings];
                        updated[idx].transformation = e.target.value;
                        setClaimMappings(updated);
                      }}
                      className="w-full px-2 py-1 bg-slate-950 border border-slate-800 text-xs rounded text-white"
                    >
                      <option value="as-is">as-is</option>
                      <option value="lowercase">lowercase</option>
                      <option value="split">split</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Privacy Scope</span>
                    <select
                      value={m.privacyClass}
                      onChange={(e: any) => {
                        const updated = [...claimMappings];
                        updated[idx].privacyClass = e.target.value;
                        setClaimMappings(updated);
                      }}
                      className="w-full px-2 py-1 bg-slate-950 border border-slate-800 text-xs rounded text-white"
                    >
                      <option value="public">Public</option>
                      <option value="internal">Internal</option>
                      <option value="sensitive">Sensitive Masked</option>
                    </select>
                  </div>

                  <div className="flex justify-end pt-3 sm:pt-0">
                    <button
                      type="button"
                      onClick={() => handleClaimMappingDelete(m.id)}
                      className="p-1 text-slate-500 hover:text-red-400 rounded hover:bg-red-950/20 transition"
                    >
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </div>
                </div>
              ))}
            </div>

            <div className="flex justify-end pt-2">
              <button
                type="button"
                onClick={handleRunNormalization}
                disabled={loading}
                className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded-lg flex items-center gap-1.5 transition"
                id="run-claims-normalization-btn"
              >
                {loading ? <RefreshCw className="h-4 w-4 animate-spin" /> : <Play className="h-4 w-4" />}
                Evaluate Claims Normalization
              </button>
            </div>
          </div>
        </div>

        {/* Results / Audit Stage (Right 1 Column) */}
        <div className="space-y-6">
          {/* Claims output & PII masking preview */}
          {normalizedResult && (
            <div className="bg-slate-900/30 border border-slate-800 rounded-xl p-5 space-y-4" id="claims-results-card">
              <div className="flex justify-between items-center">
                <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">Normalized Transaction Preview</h4>
                <span className="px-1.5 py-0.5 bg-emerald-950 text-emerald-400 text-[10px] rounded font-bold">PII SAFE</span>
              </div>

              {/* Masking Preview */}
              <div className="space-y-3">
                {Object.keys(normalizedResult).map((key) => {
                  const val = normalizedResult[key];
                  const mapping = claimMappings.find((m) => m.normalizedTarget === key);
                  const isSensitive = mapping?.privacyClass === "sensitive";
                  
                  let displayVal = Array.isArray(val) ? val.join(", ") : String(val);
                  if (isSensitive) {
                    displayVal = "•••••••••••• (Sensitive Masked)";
                  }

                  return (
                    <div key={key} className="bg-slate-950 p-3 rounded border border-slate-850 flex justify-between items-center text-xs">
                      <span className="font-mono text-slate-400 font-semibold">{key}</span>
                      <span className={`font-mono ${isSensitive ? "text-amber-500 font-bold" : "text-white"}`}>{displayVal}</span>
                    </div>
                  );
                })}
              </div>

              {/* Gemini Privacy risk Assessment */}
              <div className="bg-slate-950 border border-slate-850 p-4 rounded-lg space-y-2">
                <div className="flex items-center gap-1.5 text-xs text-indigo-400 font-bold">
                  <Sparkles className="h-4 w-4 shrink-0" />
                  Gemini Hijack Risk Report
                </div>
                <p className="text-xs text-slate-300 italic leading-relaxed">
                  "{aiReport}"
                </p>
              </div>

              {/* Detailed transformer log */}
              <div className="space-y-1.5">
                <span className="text-[10px] text-slate-500 uppercase tracking-wider font-bold">Mapper Debug logs</span>
                <CodeBlock
                  code={runLogs.join("\n")}
                  language="logs"
                  maxHeight="max-h-36"
                />
              </div>
            </div>
          )}

          {/* HRD Routing Simulator */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider">
              Home-Realm Routing Simulator
            </h4>

            <div className="space-y-3 text-xs">
              <div className="space-y-1">
                <span className="text-slate-400">Input Subject Email / Identifier</span>
                <input
                  type="text"
                  value={simEmail}
                  onChange={(e) => setSimEmail(e.target.value)}
                  placeholder="user@acme.se"
                  className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-white font-mono"
                />
              </div>

              <div className="grid grid-cols-2 gap-2">
                <div className="space-y-1">
                  <span className="text-slate-400">App Scope</span>
                  <input
                    type="text"
                    value={simApp}
                    onChange={(e) => setSimApp(e.target.value)}
                    className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-white font-mono"
                  />
                </div>
                <div className="space-y-1">
                  <span className="text-slate-400">Tenant Context</span>
                  <input
                    type="text"
                    value={simTenant}
                    onChange={(e) => setSimTenant(e.target.value)}
                    className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-white font-mono"
                  />
                </div>
              </div>

              <button
                type="button"
                onClick={handleRunRoutingSim}
                className="w-full py-2 bg-indigo-600 hover:bg-indigo-500 text-white font-semibold rounded transition"
              >
                Simulate Router Ingress Selection
              </button>

              {routingMatch && (
                <div className="p-3 bg-slate-900 border border-slate-850 rounded space-y-1">
                  <div className="text-[10px] text-slate-500 uppercase font-bold">Matching Outcome</div>
                  <div className="font-mono text-indigo-300 text-xs">
                    {routingMatch.matchText}
                  </div>
                  <div className="flex justify-between text-[9px] text-slate-500 pt-1">
                    <span>RULE SCORE MATCH: {routingMatch.score}</span>
                    <span>RULES CHECKED: {routingMatch.evaluatedRulesCount}</span>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
