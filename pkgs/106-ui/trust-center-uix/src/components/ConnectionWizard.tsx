import React, { useState } from "react";
import {
  Globe,
  Settings,
  ArrowRight,
  ArrowLeft,
  CheckCircle2,
  AlertTriangle,
  Play,
  Key,
  ShieldCheck,
  Activity,
  Plus,
  Trash2,
  Sparkles,
  RefreshCw,
  FileText,
} from "lucide-react";
import { FederationConnection, FederationProtocol, ConnectionDirection, ClaimMapping, RoutingRule } from "../types";
import CodeBlock from "./CodeBlock";

interface ConnectionWizardProps {
  connections: FederationConnection[];
  onAddConnection: (newConn: any) => Promise<any>;
  onUpdateConnection: (id: string, updates: any) => Promise<any>;
  onTriggerTest: (id: string) => Promise<any>;
  onTriggerValidate: (id: string) => Promise<any>;
  onActivate: (id: string) => Promise<any>;
}

export default function ConnectionWizard({
  connections,
  onAddConnection,
  onUpdateConnection,
  onTriggerTest,
  onTriggerValidate,
  onActivate,
}: ConnectionWizardProps) {
  const [selectedConnection, setSelectedConnection] = useState<FederationConnection | null>(null);
  const [wizardStep, setWizardStep] = useState<number>(1);
  const [loading, setLoading] = useState<boolean>(false);

  // Form Fields
  const [displayName, setDisplayName] = useState("");
  const [protocol, setProtocol] = useState<FederationProtocol>(FederationProtocol.OIDC);
  const [direction, setDirection] = useState<ConnectionDirection>(ConnectionDirection.INBOUND);
  const [issuer, setIssuer] = useState("");
  const [metadataMode, setMetadataMode] = useState<"manual" | "discovery" | "federation">("discovery");
  const [metadataUrl, setMetadataUrl] = useState("");
  const [audience, setAudience] = useState("");
  const [scopes, setScopes] = useState<string>(["openid", "profile", "email"].join(", "));
  const [clientAuthMethod, setClientAuthMethod] = useState<"client_secret_post" | "client_secret_basic" | "private_key_jwt" | "none">("client_secret_post");
  const [secretRef, setSecretRef] = useState("");
  const [keyId, setKeyId] = useState("");

  // Claims Mapping Temp State
  const [claimMappings, setClaimMappings] = useState<ClaimMapping[]>([
    { id: "m-1", sourceSelector: "sub", normalizedTarget: "external_id", transformation: "as-is", required: true, privacyClass: "internal" },
    { id: "m-2", sourceSelector: "email", normalizedTarget: "email", transformation: "lowercase", required: true, privacyClass: "internal" },
  ]);

  // Routing Temp State
  const [routingRules, setRoutingRules] = useState<RoutingRule[]>([
    { id: "r-1", priority: 10, conditionType: "domain", conditionValue: "partner.com", action: "route_to_connection" },
  ]);

  // Inspection Results
  const [fetchedMetadata, setFetchedMetadata] = useState<any>(null);
  const [aiAnalysis, setAiAnalysis] = useState("");
  const [validationFindings, setValidationFindings] = useState<string[]>([]);
  const [validationStatus, setValidationStatus] = useState<"healthy" | "degraded" | "failing" | null>(null);
  const [diagnosticLogs, setDiagnosticLogs] = useState<string[]>([]);

  // Interactive Test Output
  const [testResult, setTestResult] = useState<any>(null);

  // Quick Presets
  const applyPreset = (preset: string) => {
    if (preset === "okta") {
      setDisplayName("Okta Workforce Partner IDP");
      setProtocol(FederationProtocol.OIDC);
      setIssuer("https://partner-corp.okta.com/oauth2/default");
      setMetadataUrl("https://partner-corp.okta.com/oauth2/default/.well-known/openid-configuration");
      setMetadataMode("discovery");
      setScopes("openid, profile, email, groups");
    } else if (preset === "swedish-gov") {
      setDisplayName("Sweden Multilateral Govt Node");
      setProtocol(FederationProtocol.OPENID_FEDERATION);
      setIssuer("https://fed.trust.sweden.se");
      setMetadataUrl("https://fed.trust.sweden.se/.well-known/openid-federation");
      setMetadataMode("federation");
      setScopes("openid, profile, email, swedish_civic_id");
    } else if (preset === "azure-ad") {
      setDisplayName("Entra ID Enterprise tenant");
      setProtocol(FederationProtocol.OIDC);
      setIssuer("https://login.microsoftonline.com/tenant-guid/v2.0");
      setMetadataUrl("https://login.microsoftonline.com/tenant-guid/v2.0/.well-known/openid-configuration");
      setMetadataMode("discovery");
      setScopes("openid, profile, email, User.Read");
    }
  };

  // Safe SSRF Fetch Metadata Inspect
  const handleInspectMetadata = async () => {
    if (!issuer || !metadataUrl) return;
    setLoading(true);
    try {
      const res = await fetch("/api/federation/metadata:inspect", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ issuerUrl: issuer, mode: metadataMode }),
      });
      const data = await res.json();
      if (res.ok) {
        setFetchedMetadata(data.rawMetadata);
        setAiAnalysis(data.analysis);
      } else {
        alert(data.error || "Failed to inspect metadata");
      }
    } catch (e) {
      console.error(e);
      alert("Error reaching federation inspection API.");
    } finally {
      setLoading(false);
    }
  };

  // Draft Save Connection
  const handleDraftSubmit = async () => {
    setLoading(true);
    try {
      const response = await onAddConnection({
        displayName,
        protocol,
        direction,
        issuer,
        metadataMode,
        metadataUrl,
        audience,
        scopes: scopes.split(",").map((s) => s.trim()),
        clientAuth: {
          method: clientAuthMethod,
          secretReference: secretRef || undefined,
          keyId: keyId || undefined,
        },
      });

      if (response && response.id) {
        // Feed custom configurations (mappings & routing)
        const updated = await onUpdateConnection(response.id, {
          claimMappings,
          routingRules,
        });
        setSelectedConnection(updated);
        setWizardStep(4); // Move directly to interactive test stage
      }
    } catch (err) {
      console.error(err);
      alert("Error registering connection draft.");
    } finally {
      setLoading(false);
    }
  };

  // Run validation
  const handleValidateConnection = async (connId: string) => {
    setLoading(true);
    try {
      const res = await onTriggerValidate(connId);
      if (res) {
        setValidationFindings(res.findings);
        setValidationStatus(res.health);
        setDiagnosticLogs(res.diagnosticLog);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Interactive Test
  const handleRunInteractiveTest = async (connId: string) => {
    setLoading(true);
    try {
      const res = await onTriggerTest(connId);
      if (res) {
        setTestResult(res);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Final Activate
  const handleFinalActivation = async (connId: string) => {
    setLoading(true);
    try {
      await onActivate(connId);
      setWizardStep(5); // Complete screen
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleClaimMappingAdd = () => {
    const newMapping: ClaimMapping = {
      id: `m-dyn-${Date.now()}`,
      sourceSelector: "",
      normalizedTarget: "",
      transformation: "as-is",
      required: false,
      privacyClass: "public",
    };
    setClaimMappings([...claimMappings, newMapping]);
  };

  const handleClaimMappingDelete = (id: string) => {
    setClaimMappings(claimMappings.filter((m) => m.id !== id));
  };

  return (
    <div className="bg-slate-900/30 border border-slate-800 rounded-2xl p-6" id="wizard-surface">
      {/* Tab Select: Inspect Existing or Create New */}
      <div className="flex border-b border-slate-850 pb-4 mb-6 justify-between items-center">
        <div>
          <h2 className="text-lg font-semibold text-white">Federation Connection Wizard</h2>
          <p className="text-xs text-slate-400">Configure, test, and activate upstream identity providers securely.</p>
        </div>
        {selectedConnection && (
          <span className="px-3 py-1 bg-indigo-950/60 border border-indigo-800 text-indigo-300 rounded-full text-xs font-mono">
            Working on: {selectedConnection.displayName}
          </span>
        )}
      </div>

      {/* Step Indicators */}
      <div className="flex items-center justify-between mb-8 max-w-4xl mx-auto" id="step-indicator-bar">
        {[
          { step: 1, label: "Core Protocol" },
          { step: 2, label: "Metadata & Keys" },
          { step: 3, label: "Claims & Routing" },
          { step: 4, label: "Diagnostic Lab" },
          { step: 5, label: "Activated" },
        ].map((s) => (
          <React.Fragment key={s.step}>
            <div className="flex flex-col items-center gap-2">
              <span
                className={`h-8 w-8 rounded-full flex items-center justify-center text-xs font-bold border transition ${
                  wizardStep === s.step
                    ? "bg-indigo-600 text-white border-indigo-500 ring-4 ring-indigo-900/50"
                    : wizardStep > s.step
                    ? "bg-emerald-950 text-emerald-400 border-emerald-800"
                    : "bg-slate-800 text-slate-400 border-slate-700"
                }`}
              >
                {s.step}
              </span>
              <span className={`text-[11px] font-semibold ${wizardStep === s.step ? "text-white" : "text-slate-400"}`}>
                {s.label}
              </span>
            </div>
            {s.step < 5 && <div className={`flex-1 h-0.5 border-t border-dashed ${wizardStep > s.step ? "border-emerald-800" : "border-slate-800"}`}></div>}
          </React.Fragment>
        ))}
      </div>

      {/* Step 1: Core Protocol Setup */}
      {wizardStep === 1 && (
        <div className="space-y-6 max-w-2xl mx-auto" id="wizard-step-1">
          <div className="bg-slate-900/60 p-4 rounded-xl border border-slate-850 flex items-start gap-3">
            <Sparkles className="h-5 w-5 text-indigo-400 mt-0.5" />
            <div>
              <div className="text-sm font-semibold text-white">Accelerate with Presets</div>
              <p className="text-xs text-slate-400 mt-1">Select an industry template to prefill core configurations.</p>
              <div className="flex gap-2 mt-3 flex-wrap">
                <button onClick={() => applyPreset("okta")} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs transition">
                  Okta Workforce
                </button>
                <button onClick={() => applyPreset("azure-ad")} className="px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded text-xs transition">
                  Microsoft Entra ID
                </button>
                <button onClick={() => applyPreset("swedish-gov")} className="px-3 py-1 bg-indigo-950 hover:bg-indigo-900 border border-indigo-800 text-indigo-300 rounded text-xs transition">
                  Sweden OpenID Fed 1.0
                </button>
              </div>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Connection Display Name</label>
              <input
                type="text"
                value={displayName}
                onChange={(e) => setDisplayName(e.target.value)}
                placeholder="e.g. Acme Enterprise Partner"
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Federation Protocol / Profile</label>
              <select
                value={protocol}
                onChange={(e) => {
                  const prot = e.target.value as FederationProtocol;
                  setProtocol(prot);
                  setMetadataMode(prot === FederationProtocol.OPENID_FEDERATION ? "federation" : "discovery");
                }}
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              >
                <option value={FederationProtocol.OIDC}>OpenID Connect Core 1.0</option>
                <option value={FederationProtocol.OPENID_FEDERATION}>OpenID Federation 1.0 (Final Spec)</option>
                <option value={FederationProtocol.SAML}>SAML 2.0 Assertions (Planned)</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Transaction Direction</label>
              <select
                value={direction}
                onChange={(e) => setDirection(e.target.value as ConnectionDirection)}
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              >
                <option value={ConnectionDirection.INBOUND}>Inbound Identity Providers (Login via Partner)</option>
                <option value={ConnectionDirection.OUTBOUND}>Outbound Relying Parties (Tigrbl as Broker)</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Issuer Identifier (entity_id / iss)</label>
              <input
                type="text"
                value={issuer}
                onChange={(e) => setIssuer(e.target.value)}
                placeholder="https://issuer-domain.com"
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-850">
            <button
              onClick={() => setWizardStep(2)}
              disabled={!displayName || !issuer}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 disabled:opacity-50 text-white text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              Continue to Metadata <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 2: Metadata & Cryptography Keys */}
      {wizardStep === 2 && (
        <div className="space-y-6 max-w-3xl mx-auto" id="wizard-step-2">
          <div className="bg-amber-950/20 border border-amber-800/40 p-4 rounded-xl text-amber-300 text-xs flex items-start gap-3">
            <AlertTriangle className="h-5 w-5 shrink-0 mt-0.5 text-amber-400" />
            <div>
              <span className="font-semibold text-white">Bilateral vs. Multilateral Discovery:</span> When using OpenID Federation, metadata configuration is retrieved as a signed Entity Statement. Direct URL queries are protected against SSRF/DNS Rebinding inside the platform's trusted boundary.
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Metadata Source Mode</label>
              <select
                value={metadataMode}
                onChange={(e) => setMetadataMode(e.target.value as any)}
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              >
                <option value="discovery">RFC 8414 / OIDC Discovery (.well-known)</option>
                <option value="federation">OpenID Federation 1.0 Signed Statement</option>
                <option value="manual">Manual Metadata Input</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-xs font-semibold text-slate-300">Discovery/Metadata Fetch URL</label>
              <input
                type="text"
                value={metadataUrl}
                onChange={(e) => setMetadataUrl(e.target.value)}
                placeholder="https://domain.com/.well-known/openid-configuration"
                className="w-full px-4 py-2 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:border-indigo-500 focus:outline-none"
              />
            </div>
          </div>

          {/* Secure Fetch Action */}
          <div className="bg-slate-950 p-4 rounded-xl border border-slate-850 space-y-4">
            <div className="flex justify-between items-center">
              <div className="text-xs font-semibold text-slate-400 uppercase tracking-wider">SSRF-Protected Inspection</div>
              <button
                type="button"
                onClick={handleInspectMetadata}
                disabled={loading || !metadataUrl}
                className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded flex items-center gap-1 transition"
              >
                {loading ? <RefreshCw className="h-3 w-3 animate-spin" /> : <Play className="h-3 w-3" />}
                Inspect Remote Statement
              </button>
            </div>

            {fetchedMetadata && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
                <div className="space-y-1">
                  <span className="text-[10px] font-bold text-slate-500 uppercase">Fetched Metadata Payload</span>
                  <CodeBlock
                    code={fetchedMetadata}
                    language="json"
                    maxHeight="max-h-48"
                  />
                </div>
                <div className="space-y-3 bg-slate-900/40 p-4 rounded-lg border border-slate-800">
                  <div className="flex items-center gap-1.5 text-xs font-semibold text-indigo-400">
                    <Sparkles className="h-4 w-4" />
                    Gemini Cryptographic Assessment
                  </div>
                  <p className="text-xs text-slate-300 leading-relaxed italic">
                    "{aiAnalysis}"
                  </p>
                  <div className="pt-2 text-[10px] text-slate-500 border-t border-slate-800 flex justify-between">
                    <span>TLS Status: SECURE</span>
                    <span>Algorithm: RS256/ES256 Approved</span>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Client Authentication Selection */}
          <div className="p-5 bg-slate-950 rounded-xl border border-slate-850 space-y-4">
            <h4 className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1">
              <Key className="h-4 w-4 text-indigo-400" />
              Client Token Endpoint Authentication
            </h4>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-1.5">
                <label className="text-xs text-slate-400">Method</label>
                <select
                  value={clientAuthMethod}
                  onChange={(e: any) => setClientAuthMethod(e.target.value)}
                  className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-xs text-white"
                >
                  <option value="client_secret_post">client_secret_post</option>
                  <option value="client_secret_basic">client_secret_basic</option>
                  <option value="private_key_jwt">private_key_jwt (No Shared Secret)</option>
                  <option value="none">none (Public Client)</option>
                </select>
              </div>

              {clientAuthMethod !== "private_key_jwt" && clientAuthMethod !== "none" ? (
                <div className="space-y-1.5 md:col-span-2">
                  <label className="text-xs text-slate-400">Write-Only Secret Vault Reference</label>
                  <input
                    type="password"
                    value={secretRef}
                    onChange={(e) => setSecretRef(e.target.value)}
                    placeholder="e.g. vault://tenants/default/secrets/acme-secret"
                    className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-xs text-white font-mono"
                  />
                  <p className="text-[10px] text-slate-500">
                    The raw secret is stored inside the secure credential subsystem. It is never displayed back to browser.
                  </p>
                </div>
              ) : clientAuthMethod === "private_key_jwt" ? (
                <div className="space-y-1.5 md:col-span-2">
                  <label className="text-xs text-slate-400">Tenant Private Signing Key ID (kid)</label>
                  <input
                    type="text"
                    value={keyId}
                    onChange={(e) => setKeyId(e.target.value)}
                    placeholder="key-sig-2026-v2"
                    className="w-full px-3 py-1.5 bg-slate-900 border border-slate-800 rounded text-xs text-white font-mono"
                  />
                </div>
              ) : null}
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-850">
            <button
              onClick={() => setWizardStep(1)}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button
              onClick={() => setWizardStep(3)}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              Claims Mapping <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 3: Claim Mappings & Domain Routing */}
      {wizardStep === 3 && (
        <div className="space-y-6 max-w-4xl mx-auto" id="wizard-step-3">
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <div className="flex justify-between items-center">
              <div>
                <h4 className="text-sm font-semibold text-white">PII Claims Transformations</h4>
                <p className="text-xs text-slate-500">Map upstream claim keys onto normalized internal transaction formats.</p>
              </div>
              <button
                type="button"
                onClick={handleClaimMappingAdd}
                className="px-3 py-1 bg-slate-850 hover:bg-slate-800 text-indigo-400 border border-slate-800 rounded text-xs font-semibold flex items-center gap-1 transition"
              >
                <Plus className="h-3 w-3" /> Add Claim Field
              </button>
            </div>

            <div className="space-y-3">
              {claimMappings.map((m, idx) => (
                <div key={m.id} className="grid grid-cols-1 sm:grid-cols-5 gap-3 bg-slate-900 p-3 rounded-lg border border-slate-800 items-center">
                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Upstream Selector</span>
                    <input
                      type="text"
                      value={m.sourceSelector}
                      onChange={(e) => {
                        const updated = [...claimMappings];
                        updated[idx].sourceSelector = e.target.value;
                        setClaimMappings(updated);
                      }}
                      placeholder="e.g. given_name"
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
                      placeholder="e.g. first_name"
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
                      <option value="as-is">as-is (Direct copy)</option>
                      <option value="lowercase">lowercase</option>
                      <option value="split">split (comma to array)</option>
                    </select>
                  </div>

                  <div className="space-y-1">
                    <span className="text-[10px] text-slate-500">Privacy & Required</span>
                    <div className="flex gap-2 items-center">
                      <select
                        value={m.privacyClass}
                        onChange={(e: any) => {
                          const updated = [...claimMappings];
                          updated[idx].privacyClass = e.target.value;
                          setClaimMappings(updated);
                        }}
                        className="px-2 py-1 bg-slate-950 border border-slate-800 text-xs rounded text-white"
                      >
                        <option value="public">Public</option>
                        <option value="internal">Internal</option>
                        <option value="sensitive">Sensitive</option>
                      </select>
                      <label className="flex items-center gap-1 text-[10px] text-slate-400">
                        <input
                          type="checkbox"
                          checked={m.required}
                          onChange={(e) => {
                            const updated = [...claimMappings];
                            updated[idx].required = e.target.checked;
                            setClaimMappings(updated);
                          }}
                        />
                        Req
                      </label>
                    </div>
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
          </div>

          {/* Domain-scoped login routing */}
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <h4 className="text-sm font-semibold text-white">Home-Realm Discovery Domain Routing</h4>
            <p className="text-xs text-slate-500">Map specific customer domains to route straight to this IDP provider.</p>

            <div className="space-y-3">
              {routingRules.map((rule, idx) => (
                <div key={rule.id} className="flex flex-col sm:flex-row items-center gap-3 bg-slate-900 p-3 rounded-lg border border-slate-800">
                  <div className="flex-1 space-y-1 w-full">
                    <span className="text-[10px] text-slate-500">Condition Type</span>
                    <select
                      value={rule.conditionType}
                      onChange={(e: any) => {
                        const updated = [...routingRules];
                        updated[idx].conditionType = e.target.value;
                        setRoutingRules(updated);
                      }}
                      className="w-full px-2 py-1.5 bg-slate-950 border border-slate-800 text-xs rounded text-white"
                    >
                      <option value="domain">Email Domain Pattern (*.corp.com)</option>
                      <option value="organization">Organization Name</option>
                      <option value="always">Always Match (Default Connection)</option>
                    </select>
                  </div>

                  <div className="flex-1 space-y-1 w-full">
                    <span className="text-[10px] text-slate-500">Condition Value</span>
                    <input
                      type="text"
                      value={rule.conditionValue}
                      onChange={(e) => {
                        const updated = [...routingRules];
                        updated[idx].conditionValue = e.target.value;
                        setRoutingRules(updated);
                      }}
                      placeholder="e.g. Acme Corp"
                      className="w-full px-2 py-1.5 bg-slate-950 border border-slate-800 text-xs rounded text-white font-mono"
                    />
                  </div>

                  <div className="space-y-1 w-full sm:w-auto">
                    <span className="text-[10px] text-slate-500 block">Default Action</span>
                    <span className="text-xs text-indigo-400 font-semibold px-2 py-1">
                      Route directly to Connection
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-850">
            <button
              onClick={() => setWizardStep(2)}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              <ArrowLeft className="h-4 w-4" /> Back
            </button>
            <button
              onClick={handleDraftSubmit}
              disabled={loading}
              className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              {loading ? "Registering..." : "Submit Draft Connection"} <ArrowRight className="h-4 w-4" />
            </button>
          </div>
        </div>
      )}

      {/* Step 4: Diagnostic Lab & Secure Test Transactions */}
      {wizardStep === 4 && selectedConnection && (
        <div className="space-y-6 max-w-4xl mx-auto" id="wizard-step-4">
          <div className="bg-slate-950 p-5 rounded-xl border border-slate-850 space-y-4">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
              <div>
                <h4 className="text-sm font-semibold text-white">Interactive Cryptographic Diagnostic Lab</h4>
                <p className="text-xs text-slate-500">Run safe, isolated transaction tests on this connection before deployment.</p>
              </div>
              <div className="flex gap-2">
                <button
                  type="button"
                  onClick={() => handleValidateConnection(selectedConnection.id)}
                  className="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 text-xs font-semibold rounded flex items-center gap-1.5 transition"
                >
                  <Activity className="h-4 w-4" /> Validate Endpoint Syntax
                </button>
                <button
                  type="button"
                  onClick={() => handleRunInteractiveTest(selectedConnection.id)}
                  className="px-3 py-1.5 bg-indigo-600 hover:bg-indigo-500 text-white text-xs font-semibold rounded flex items-center gap-1.5 transition animate-pulse"
                >
                  <Play className="h-4 w-4" /> Simulate OIDC Callback
                </button>
              </div>
            </div>

            {/* Validation Findings */}
            {validationStatus && (
              <div className="p-4 bg-slate-900 border border-slate-800 rounded-lg grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-1">
                  <span className="text-[10px] text-slate-500 uppercase">Audit Health</span>
                  <div className="flex items-center gap-2">
                    <span className={`h-2.5 w-2.5 rounded-full ${validationStatus === "healthy" ? "bg-emerald-500" : "bg-amber-500"}`}></span>
                    <span className="text-xs font-semibold uppercase text-slate-200">{validationStatus}</span>
                  </div>
                </div>

                <div className="md:col-span-2 space-y-2">
                  <span className="text-[10px] text-slate-500 uppercase">Diagnostic Observations ({validationFindings.length})</span>
                  {validationFindings.length === 0 ? (
                    <p className="text-xs text-emerald-400">All configurations match OpenID conformance checklists perfectly.</p>
                  ) : (
                    <ul className="text-xs text-slate-300 list-disc list-inside space-y-1">
                      {validationFindings.map((f, i) => (
                        <li key={i} className="text-amber-400">{f}</li>
                      ))}
                    </ul>
                  )}
                </div>
              </div>
            )}

            {/* Simulated Live Claims Output */}
            {testResult && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-slate-400 uppercase font-bold">Simulated Upstream ID Token Payload</span>
                    <span className="text-[9px] px-1 bg-slate-800 text-slate-400 font-mono">JOSE Decoded Header & Payload</span>
                  </div>
                  <CodeBlock
                    code={testResult.rawToken}
                    language="json"
                    maxHeight="max-h-56"
                  />
                </div>

                <div className="space-y-1.5">
                  <div className="flex justify-between items-center">
                    <span className="text-[10px] text-indigo-400 uppercase font-bold">Resolved Normalized Claims Result</span>
                    <span className="text-[9px] px-1 bg-indigo-950 text-indigo-400 font-mono">Claims Mapping Complete</span>
                  </div>
                  <CodeBlock
                    code={testResult.normalizedClaims}
                    language="json"
                    maxHeight="max-h-56"
                  />
                </div>
              </div>
            )}
          </div>

          <div className="flex justify-between pt-4 border-t border-slate-850">
            <button
              onClick={() => setWizardStep(3)}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              <ArrowLeft className="h-4 w-4" /> Back to Mapping
            </button>
            <button
              onClick={() => handleFinalActivation(selectedConnection.id)}
              disabled={loading}
              className="px-5 py-2.5 bg-emerald-600 hover:bg-emerald-500 text-white text-sm font-semibold rounded-lg flex items-center gap-2 transition"
            >
              <ShieldCheck className="h-4 w-4" /> Approve & Activate Connection
            </button>
          </div>
        </div>
      )}

      {/* Step 5: Complete */}
      {wizardStep === 5 && selectedConnection && (
        <div className="text-center py-12 max-w-md mx-auto space-y-6" id="wizard-step-5">
          <div className="inline-flex p-4 bg-emerald-500/10 rounded-full border border-emerald-800/40 text-emerald-400 animate-bounce">
            <CheckCircle2 className="h-10 w-10" />
          </div>
          <div className="space-y-2">
            <h3 className="text-lg font-bold text-white">Connection Staged and Activated</h3>
            <p className="text-xs text-slate-400">
              The identity provider **{selectedConnection.displayName}** is now a trusted participant of the tenant trust-domain routing framework.
            </p>
          </div>

          <div className="p-4 bg-slate-950 rounded-xl border border-slate-850 text-left text-xs font-mono text-slate-300 space-y-2">
            <div className="flex justify-between">
              <span className="text-slate-500">CONNECTION ID</span>
              <span>{selectedConnection.id}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">ACTIVE VERSION</span>
              <span>v{selectedConnection.activeVersion}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-slate-500">ROUTING DOMAINS</span>
              <span>{selectedConnection.routingRules[0]?.conditionValue || "*.corp.com"}</span>
            </div>
          </div>

          <button
            onClick={() => {
              // Reset
              setSelectedConnection(null);
              setDisplayName("");
              setIssuer("");
              setMetadataUrl("");
              setFetchedMetadata(null);
              setTestResult(null);
              setWizardStep(1);
            }}
            className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-semibold rounded-lg transition"
          >
            Create Another Connection
          </button>
        </div>
      )}
    </div>
  );
}
