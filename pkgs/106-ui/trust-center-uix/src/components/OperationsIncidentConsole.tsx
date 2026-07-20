import React, { useState } from "react";
import {
  Flame,
  ShieldAlert,
  ShieldCheck,
  AlertTriangle,
  Play,
  CheckCircle2,
  XCircle,
  Activity,
  ArrowRight,
  Clock,
  Download,
  Check,
  Sparkles,
} from "lucide-react";
import { IncidentRecord } from "../types";

interface OperationsIncidentConsoleProps {
  incidents: IncidentRecord[];
  onMitigateIncident: (id: string) => Promise<any>;
  onResolveIncident: (id: string) => Promise<any>;
  onRefresh: () => void;
}

export default function OperationsIncidentConsole({
  incidents,
  onMitigateIncident,
  onResolveIncident,
  onRefresh,
}: OperationsIncidentConsoleProps) {
  const [selectedIncident, setSelectedIncident] = useState<IncidentRecord | null>(null);
  const [typedConfirmation, setTypedConfirmation] = useState("");
  const [exportSuccess, setExportSuccess] = useState(false);

  const activeIncidents = incidents.filter((i) => i.status !== "resolved");
  const historicalIncidents = incidents.filter((i) => i.status === "resolved");

  const handleMitigate = async (incId: string) => {
    if (typedConfirmation.trim().toUpperCase() !== "CONTAIN") {
      alert("Please type 'CONTAIN' to confirm the quarantine blast radius.");
      return;
    }
    await onMitigateIncident(incId);
    setTypedConfirmation("");
    setSelectedIncident(null);
  };

  const handleResolve = async (incId: string) => {
    await onResolveIncident(incId);
    setSelectedIncident(null);
  };

  // Incident Bundle Exporter
  const handleExportIncidentBundle = (inc: IncidentRecord) => {
    const bundle = {
      incidentId: inc.id,
      title: inc.title,
      type: inc.type,
      severity: inc.severity,
      timestamp: inc.timestamp,
      exportDate: new Date().toISOString(),
      platformAuthority: "https://auth.tigrbl.com/tenant-default",
      redactedEvidence: {
        blastRadius: {
          impactedTenantsCount: inc.affectedTenants,
          impactedApplicationsCount: inc.affectedApps,
          impactedSessionsCount: inc.affectedSessions
        },
        issuerAudited: inc.connectionId || "multilateral_graph_node",
        cryptographicReasonCodes: [
          "SEC_INC_CHAIN_INTEGRITY_FAIL",
          "SEC_KID_UNKNOWN_ROOT_SIGNER",
          "SEC_CONTAINMENT_QUARANTINE_STAGED"
        ]
      },
      integritySignature: "sha384-signed-integrity-bundle-v1"
    };

    const fileData = JSON.stringify(bundle, null, 2);
    const blob = new Blob([fileData], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `tigrbl-incident-${inc.id}-redacted-bundle.json`;
    link.click();

    setExportSuccess(true);
    setTimeout(() => setExportSuccess(false), 3000);
  };

  // Mock Operations Timeline audit records
  const timelineLogs = [
    { id: "l1", actor: "jick.68.0@gmail.com", action: "Approved claim mapping configuration v2", timestamp: "2026-07-20T08:15:30Z" },
    { id: "l2", actor: "System Daemon", action: "Rotated JWKS cache signing keys", timestamp: "2026-07-20T06:00:00Z" },
    { id: "l3", actor: "System Daemon", action: "Triggered quarantine on eduGAIN Research connection", timestamp: "2026-07-20T03:33:09Z" },
    { id: "l4", actor: "jick.68.0@gmail.com", action: "Drafted connection: Sweden Multilateral Govt Node", timestamp: "2026-07-19T14:40:12Z" }
  ];

  return (
    <div className="space-y-6" id="operations-console-surface">
      {/* Overview stats bar */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-xl flex items-center gap-4">
          <span className="p-3 bg-red-500/10 text-red-500 rounded-lg">
            <Flame className="h-6 w-6 animate-pulse" />
          </span>
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Active Outages / Incidents</div>
            <div className="text-2xl font-bold text-white mt-1">
              {activeIncidents.length}
            </div>
          </div>
        </div>

        <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-xl flex items-center gap-4">
          <span className="p-3 bg-indigo-500/10 text-indigo-400 rounded-lg">
            <Clock className="h-6 w-6" />
          </span>
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Mean Time to Contain (MTTC)</div>
            <div className="text-2xl font-bold text-white mt-1">
              12 min
            </div>
          </div>
        </div>

        <div className="bg-slate-900/40 border border-slate-800 p-5 rounded-xl flex items-center gap-4">
          <span className="p-3 bg-emerald-500/10 text-emerald-500 rounded-lg">
            <ShieldCheck className="h-6 w-6" />
          </span>
          <div>
            <div className="text-xs text-slate-400 font-semibold uppercase">Containment Coverage</div>
            <div className="text-2xl font-bold text-white mt-1">
              100% fail-closed
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Side: Incident List and Audit Trail (2 columns) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Active Incidents */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <h3 className="text-sm font-semibold text-white flex items-center gap-1.5 text-red-400">
              <ShieldAlert className="h-4 w-4" />
              Outstanding Cryptographic & Metadata Incidents ({activeIncidents.length})
            </h3>

            <div className="space-y-3">
              {activeIncidents.map((inc) => (
                <div
                  key={inc.id}
                  onClick={() => setSelectedIncident(inc)}
                  className={`p-4 rounded-xl border cursor-pointer transition flex justify-between items-start ${
                    selectedIncident?.id === inc.id
                      ? "bg-red-950/20 border-red-800"
                      : "bg-slate-900/60 border-slate-800 hover:border-slate-700"
                  }`}
                >
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-semibold text-white">{inc.title}</span>
                      <span className="px-1.5 py-0.5 bg-red-950 text-red-400 text-[9px] font-bold rounded uppercase">
                        {inc.severity}
                      </span>
                    </div>
                    <p className="text-xs text-slate-400 line-clamp-2 max-w-xl">
                      {inc.description}
                    </p>
                    <div className="text-[10px] text-slate-500 font-mono mt-1">
                      Observed: {new Date(inc.timestamp).toLocaleString()}
                    </div>
                  </div>

                  <ArrowRight className="h-4 w-4 text-slate-500 mt-1 shrink-0" />
                </div>
              ))}

              {activeIncidents.length === 0 && (
                <div className="text-center py-6 text-slate-500 text-xs">
                  All systems operating securely. No outstanding cryptographic incidents.
                </div>
              )}
            </div>
          </div>

          {/* Historical Audits & Configurations Timeline */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <h3 className="text-sm font-semibold text-white flex items-center gap-1.5">
              <Activity className="h-4 w-4 text-indigo-400" />
              Tenant Operations & Configuration Logs (Audit)
            </h3>

            <div className="divide-y divide-slate-850">
              {timelineLogs.map((log) => (
                <div key={log.id} className="py-3 flex justify-between items-center text-xs first:pt-0 last:pb-0">
                  <div className="space-y-1">
                    <span className="text-white font-medium">{log.action}</span>
                    <div className="text-[10px] text-slate-500 font-mono">{log.actor}</div>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono">
                    {new Date(log.timestamp).toLocaleTimeString()}
                  </span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side: Incident Details, Quarantine and Compliance Exporter */}
        <div className="bg-slate-900/30 border border-slate-800 rounded-xl p-5 space-y-5">
          {!selectedIncident ? (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500">
              <ShieldCheck className="h-10 w-10 text-emerald-500/20 mb-3" />
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider">Select Incident to Contain</h4>
              <p className="text-xs text-slate-500 mt-1 max-w-xs">
                Select an active incident to trigger quarantine actions, review tenant blast radius, and export compliance evidence.
              </p>
            </div>
          ) : (
            <div className="space-y-5" id="incident-details-box">
              <div className="flex justify-between items-start">
                <div>
                  <span className="text-[10px] font-bold text-red-400 uppercase tracking-wider">Active Outage</span>
                  <h4 className="text-sm font-bold text-white mt-1">{selectedIncident.title}</h4>
                </div>
                <span className="px-2 py-0.5 bg-red-950 text-red-400 text-[10px] rounded font-bold uppercase">
                  {selectedIncident.status}
                </span>
              </div>

              {/* Blast radius numbers */}
              <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-3">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Computed Blast Radius Impact</span>
                
                <div className="grid grid-cols-3 gap-2 text-center text-xs">
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <div className="text-sm font-bold text-white">{selectedIncident.affectedTenants}</div>
                    <div className="text-[9px] text-slate-500 uppercase">Tenants</div>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <div className="text-sm font-bold text-white">{selectedIncident.affectedApps}</div>
                    <div className="text-[9px] text-slate-500 uppercase">Apps</div>
                  </div>
                  <div className="bg-slate-900 p-2 rounded border border-slate-800">
                    <div className="text-sm font-bold text-white">{selectedIncident.affectedSessions}</div>
                    <div className="text-[9px] text-slate-500 uppercase">Sessions</div>
                  </div>
                </div>
              </div>

              {/* Redacted Compliance Exporter Button */}
              <div className="space-y-2">
                <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider">Regulatory Compliance Evidence</span>
                <button
                  type="button"
                  onClick={() => handleExportIncidentBundle(selectedIncident)}
                  className="w-full py-2 bg-slate-850 hover:bg-slate-800 text-slate-200 border border-slate-800 rounded text-xs font-semibold flex items-center justify-center gap-1.5 transition"
                >
                  {exportSuccess ? <Check className="h-4 w-4 text-emerald-400" /> : <Download className="h-4 w-4" />}
                  {exportSuccess ? "Redacted Bundle Downloaded" : "Export Redacted Incident Bundle"}
                </button>
                <p className="text-[9px] text-slate-500 leading-relaxed text-center">
                  Redacts end-user identities and client secrets, exporting signed proof-of-containment audits.
                </p>
              </div>

              {/* Action Forms based on State */}
              {selectedIncident.status === "active" ? (
                <div className="space-y-3 pt-4 border-t border-slate-850">
                  <div className="text-xs font-bold text-red-400 uppercase tracking-wider">Quarantine & Divert Traffic</div>
                  
                  <div className="space-y-2 text-xs">
                    <p className="text-slate-400 leading-relaxed text-[11px]">
                      Type <strong className="text-white">CONTAIN</strong> below to commit emergency quarantine. This immediately suspends matching tokens and isolates downstream routes.
                    </p>
                    <input
                      type="text"
                      value={typedConfirmation}
                      onChange={(e) => setTypedConfirmation(e.target.value)}
                      placeholder="Type CONTAIN to confirm"
                      className="w-full px-3 py-1.5 bg-slate-950 border border-slate-800 rounded text-white font-mono uppercase"
                    />
                    <button
                      type="button"
                      disabled={typedConfirmation.trim().toUpperCase() !== "CONTAIN"}
                      onClick={() => handleMitigate(selectedIncident.id)}
                      className="w-full py-2 bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white font-semibold rounded text-xs transition"
                    >
                      Divert Routing & Isolate Partner
                    </button>
                  </div>
                </div>
              ) : selectedIncident.status === "mitigated" ? (
                <div className="space-y-3 pt-4 border-t border-slate-850">
                  <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider">Resolve Connection Outage</div>
                  <p className="text-xs text-slate-400 leading-relaxed">
                    This incident is currently mitigated via routing diversion. Once the remote partner publishes a valid, verified key configuration statement, click Resolve.
                  </p>
                  <button
                    type="button"
                    onClick={() => handleResolve(selectedIncident.id)}
                    className="w-full py-2 bg-emerald-600 hover:bg-emerald-500 text-white font-semibold rounded text-xs transition"
                  >
                    Mark Incident Resolved
                  </button>
                </div>
              ) : null}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
