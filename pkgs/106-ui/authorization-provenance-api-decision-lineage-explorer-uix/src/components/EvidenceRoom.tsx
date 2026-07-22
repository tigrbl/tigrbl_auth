import React, { useState } from 'react';
import { mockDecisions } from '../data/mockData';
import { 
  Archive, ShieldAlert, CheckCircle2, AlertTriangle, HelpCircle, 
  Download, FileText, Lock, ShieldCheck, Activity, Search, RefreshCw,
  Clock, Server, Terminal, Copy, Check, Filter, Trash2
} from 'lucide-react';

export default function EvidenceRoom() {
  const [activeSubTab, setActiveSubTab] = useState<'evidence' | 'incident'>('evidence');
  
  // Evidence Room State
  const [selectedDecision, setSelectedDecision] = useState(mockDecisions[0]);
  const [exportFormat, setExportFormat] = useState<'prov' | 'json' | 'token'>('prov');
  const [exportReason, setExportReason] = useState('');
  const [isSealed, setIsSealed] = useState<boolean | null>(null);
  const [isExporting, setIsExporting] = useState(false);
  const [exportedCode, setExportedCode] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  // Incident Impact State
  const [incidentType, setIncidentType] = useState<'credential' | 'region' | 'policy' | 'delegation'>('credential');
  const [compromisedValue, setCompromisedValue] = useState('usr_john_doe');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [impactReport, setImpactReport] = useState<any | null>(null);

  // Trigger Cryptographic Seal Verification
  const handleVerifySeal = () => {
    setIsSealed(null);
    setTimeout(() => {
      setIsSealed(selectedDecision.integritySeal === 'valid');
    }, 450);
  };

  const handleCopyCode = () => {
    if (exportedCode) {
      navigator.clipboard.writeText(exportedCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Generate Evidence Export (e.g. W3C PROV representation)
  const handleExportEvidence = (e: React.FormEvent) => {
    e.preventDefault();
    if (!exportReason.trim()) {
      alert('Please specify the authorized reason for exporting sensitive evidence.');
      return;
    }

    setIsExporting(true);
    setExportedCode(null);

    setTimeout(() => {
      let code = '';
      if (exportFormat === 'prov') {
        // W3C PROV-O JSON mapping
        code = JSON.stringify({
          "@context": {
            "prov": "http://www.w3.org/ns/prov#",
            "tigrbl": "https://tigrbl.auth/vocab#"
          },
          "entity": {
            [`tigrbl:request:${selectedDecision.id}`]: {
              "prov:type": "tigrbl:NormalizedRequest",
              "tigrbl:action": selectedDecision.action,
              "tigrbl:resource": selectedDecision.resource.id
            },
            [`tigrbl:policy:${selectedDecision.policyVersion}`]: {
              "prov:type": "tigrbl:PolicyBundle",
              "tigrbl:hash": "sha256:d81f21eb79a8360d"
            },
            [`tigrbl:decision:${selectedDecision.id}`]: {
              "prov:type": "tigrbl:AuthorizationDecision",
              "tigrbl:effect": selectedDecision.effect,
              "prov:wasDerivedFrom": [`tigrbl:request:${selectedDecision.id}`, `tigrbl:policy:${selectedDecision.policyVersion}`]
            }
          },
          "activity": {
            [`tigrbl:evaluation:${selectedDecision.id}`]: {
              "prov:type": "tigrbl:PolicyEvaluation",
              "prov:startedAtTime": selectedDecision.timestamp,
              "prov:endedAtTime": selectedDecision.timestamp
            }
          },
          "agent": {
            [`tigrbl:subject:${selectedDecision.subject.id}`]: {
              "prov:type": "prov:Person",
              "tigrbl:name": selectedDecision.subject.name
            },
            "tigrbl:pdp_engine": {
              "prov:type": "prov:SoftwareAgent",
              "tigrbl:version": selectedDecision.engineVersion
            }
          },
          "wasAssociatedWith": {
            "tigrbl:assoc_1": {
              "prov:activity": `tigrbl:evaluation:${selectedDecision.id}`,
              "prov:agent": "tigrbl:pdp_engine"
            }
          }
        }, null, 2);
      } else if (exportFormat === 'json') {
        code = JSON.stringify({
          evidenceMetadata: {
            provenanceEngine: "Tigrbl Authz Provenance API v1.2",
            exportTimestamp: new Date().toISOString(),
            exportPurpose: exportReason,
            integritySeal: "valid",
            sealSignature: "sha256:9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08"
          },
          decisionTrace: selectedDecision
        }, null, 2);
      } else {
        code = `eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6InByb3YtZW5naW5lIn0.${btoa(JSON.stringify({
          sub: selectedDecision.subject.id,
          act: selectedDecision.action,
          res: selectedDecision.resource.id,
          eff: selectedDecision.effect,
          pol: selectedDecision.policyVersion,
          hash: selectedDecision.id
        }))}.SignatureVerifiedValid_TamperProof`;
      }
      setExportedCode(code);
      setIsExporting(false);
    }, 700);
  };

  // Run Incident Impact Analysis
  const handleAnalyzeImpact = () => {
    setIsAnalyzing(true);
    setImpactReport(null);

    setTimeout(() => {
      let affectedDecisions: any[] = [];
      let sessions = 0;
      let riskScore = 'Low';
      let recommendations: string[] = [];
      let explanation = '';

      if (incidentType === 'credential') {
        if (compromisedValue === 'usr_john_doe') {
          affectedDecisions = mockDecisions.filter(d => d.subject.id === 'usr_john_doe');
          sessions = 3;
          riskScore = 'High';
          recommendations = [
            'Instantly rotate usr_john_doe credentials',
            'Surgically purge the local auth PDP cache for tenant corp-engineering',
            'Quarantine the current session across all registered resource gateways'
          ];
          explanation = 'Direct matches found for John Doe in tenant corp-engineering. One deletion attempt was denied but should be audited for suspicious persistence.';
        } else {
          affectedDecisions = mockDecisions.filter(d => d.subject.id === compromisedValue);
          sessions = 1;
          riskScore = 'Medium';
          recommendations = ['Revoke active tokens', 'Force re-authentication'];
          explanation = 'A single standard audit trace detected for this subject. No destructive activities matches found.';
        }
      } else if (incidentType === 'region') {
        affectedDecisions = mockDecisions.filter(d => 
          d.facts.some(f => f.type === 'network_origin' && f.value.region === compromisedValue)
        );
        sessions = 14;
        riskScore = 'Medium';
        recommendations = [
          'Enforce sovereignty rules strictly across ap-south-1 origin routes',
          'Audit all secondary delegated tokens resolved inside ap-south-1 region'
        ];
        explanation = 'Geopolitical sovereignty boundaries triggered access denials from ap-south-1. Replays verify sovereignty restrictions enforced correctly.';
      } else if (incidentType === 'policy') {
        affectedDecisions = mockDecisions.filter(d => d.policyVersion === compromisedValue);
        sessions = 122;
        riskScore = 'Critical';
        recommendations = [
          'Force rolling updates to pol_v2.4.2 active PDP bundle',
          'Review rule changes between pol_v2.4.1 and pol_v2.4.2 to trace unauthorized modifications'
        ];
        explanation = 'Compromised policy bundle version matches decisions in crop-finance and corp-engineering. Immediate drift analysis recommended.';
      } else if (incidentType === 'delegation') {
        affectedDecisions = mockDecisions.filter(d => d.subject.delegatedFrom !== undefined);
        sessions = 2;
        riskScore = 'High';
        recommendations = [
          'Revoke delegation grant parentage in Trust Registry',
          'Audit token exchange mode constraints'
        ];
        explanation = 'Delegated authority found under corp-sales sync bots. Trace shows delegation was active, but subsequent expiry checks require force verification.';
      }

      setImpactReport({
        affectedDecisions,
        sessions,
        riskScore,
        recommendations,
        explanation,
        analyzedAt: new Date().toISOString()
      });
      setIsAnalyzing(false);
    }, 600);
  };

  return (
    <div className="p-8 space-y-8 max-w-7xl mx-auto h-full overflow-y-auto bg-slate-50">
      
      {/* Sub-tab Navigation */}
      <div className="flex justify-between items-center border-b border-slate-200 pb-2">
        <div>
          <h1 className="text-2xl font-bold text-slate-900 tracking-tight">Governance & Incident Response</h1>
          <p className="text-slate-500 text-sm mt-1">Audit evidence bundles, prove compliance, and analyze threat blast-radii</p>
        </div>
        <div className="flex bg-slate-200/60 p-1 rounded-lg">
          <button 
            onClick={() => setActiveSubTab('evidence')}
            className={`px-4 py-1.5 rounded-md text-sm font-semibold transition-all ${
              activeSubTab === 'evidence' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Evidence Room
          </button>
          <button 
            onClick={() => setActiveSubTab('incident')}
            className={`px-4 py-1.5 rounded-md text-sm font-semibold transition-all ${
              activeSubTab === 'incident' ? 'bg-white text-slate-900 shadow-sm' : 'text-slate-600 hover:text-slate-900'
            }`}
          >
            Incident Impact Explorer
          </button>
        </div>
      </div>

      {activeSubTab === 'evidence' ? (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Cryptographic Seal Verification */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              <h2 className="text-md font-semibold text-slate-900 border-b pb-3 flex items-center">
                <Lock className="w-4 h-4 mr-2 text-indigo-500" />
                Evidence Seal Verifier
              </h2>
              
              <div className="space-y-4">
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase block">Select Decision Bundle</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                    value={selectedDecision.id}
                    onChange={(e) => {
                      const dec = mockDecisions.find(d => d.id === e.target.value);
                      if (dec) {
                        setSelectedDecision(dec);
                        setIsSealed(null);
                        setExportedCode(null);
                      }
                    }}
                  >
                    {mockDecisions.map(d => (
                      <option key={d.id} value={d.id}>
                        {d.subject.name} - {d.action.toUpperCase()} ({d.id.substring(0, 8)}...)
                      </option>
                    ))}
                  </select>
                </div>

                <div className="bg-slate-50 p-4 rounded-lg border border-slate-100 text-xs space-y-2">
                  <p><span className="font-medium text-slate-500">Seal Key:</span> <span className="font-mono bg-slate-100 px-1 rounded">{selectedDecision.decisionKey}</span></p>
                  <p><span className="font-medium text-slate-500">Hash ID:</span> <span className="font-mono">{selectedDecision.id}</span></p>
                  <p><span className="font-medium text-slate-500">Sealed at:</span> {selectedDecision.timestamp}</p>
                </div>

                <button
                  onClick={handleVerifySeal}
                  className="w-full py-2 bg-indigo-600 hover:bg-indigo-700 text-white font-semibold text-sm rounded-lg shadow-sm transition-all flex items-center justify-center space-x-2"
                >
                  <ShieldCheck className="w-4 h-4" />
                  <span>Verify Integrity Signature</span>
                </button>

                {isSealed !== null && (
                  <div className={`p-4 rounded-lg border text-xs flex items-start space-x-3 ${
                    isSealed 
                      ? 'bg-emerald-50 border-emerald-200 text-emerald-800' 
                      : 'bg-rose-50 border-rose-200 text-rose-800'
                  }`}>
                    {isSealed ? (
                      <>
                        <CheckCircle2 className="w-5 h-5 text-emerald-600 shrink-0 mt-0.5" />
                        <div>
                          <p className="font-bold">Tamper-Evident Seal Valid</p>
                          <p className="mt-1 text-emerald-700">SHA-256 integrity digest and certificate chain verified matching NIST SP 800-53 requirements.</p>
                        </div>
                      </>
                    ) : (
                      <>
                        <AlertTriangle className="w-5 h-5 text-rose-600 shrink-0 mt-0.5" />
                        <div>
                          <p className="font-bold">Integrity Defect Found</p>
                          <p className="mt-1 text-rose-700">Verification failed. One or more fact states did not match the initial signed envelope hash.</p>
                        </div>
                      </>
                    )}
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Secure Evidence Export */}
          <div className="lg:col-span-2 space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              <h2 className="text-md font-semibold text-slate-900 border-b pb-3 flex items-center">
                <Archive className="w-4 h-4 mr-2 text-indigo-500" />
                Secure Evidence Export
              </h2>

              <form onSubmit={handleExportEvidence} className="space-y-4">
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  
                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-500 uppercase block">Export Specification</label>
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                      value={exportFormat}
                      onChange={(e) => setExportFormat(e.target.value as any)}
                    >
                      <option value="prov">W3C PROV-O Standard mapping</option>
                      <option value="json">Full Cryptographic Decision Trace JSON</option>
                      <option value="token">Signed Token Claims Envelope (JWT)</option>
                    </select>
                  </div>

                  <div className="space-y-1.5">
                    <label className="text-xs font-semibold text-slate-500 uppercase block">Authorized Reason / Purpose</label>
                    <input
                      type="text"
                      placeholder="e.g., GDPR Audit sampling, incident response"
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                      value={exportReason}
                      onChange={(e) => setExportReason(e.target.value)}
                    />
                  </div>

                </div>

                <div className="flex justify-end pt-2">
                  <button
                    type="submit"
                    disabled={isExporting}
                    className="px-4 py-2 bg-indigo-600 hover:bg-indigo-700 text-white text-sm font-semibold rounded-lg shadow-sm transition-all flex items-center space-x-2 disabled:bg-indigo-300"
                  >
                    {isExporting ? (
                      <>
                        <RefreshCw className="w-4 h-4 animate-spin" />
                        <span>Generating bundle...</span>
                      </>
                    ) : (
                      <>
                        <Download className="w-4 h-4" />
                        <span>Export Evidence Bundle</span>
                      </>
                    )}
                  </button>
                </div>
              </form>

              {exportedCode && (
                <div className="space-y-3">
                  <div className="flex justify-between items-center text-xs text-slate-500 border-t pt-4">
                    <span>Generated Cryptographic Evidence Bundle</span>
                    <button 
                      onClick={handleCopyCode}
                      className="text-indigo-600 hover:text-indigo-700 font-medium flex items-center space-x-1"
                    >
                      {copied ? (
                        <>
                          <Check className="w-3.5 h-3.5" />
                          <span>Copied!</span>
                        </>
                      ) : (
                        <>
                          <Copy className="w-3.5 h-3.5" />
                          <span>Copy Clipboard</span>
                        </>
                      )}
                    </button>
                  </div>
                  <pre className="p-4 bg-slate-900 text-slate-200 rounded-xl font-mono text-[11px] overflow-auto max-h-96 leading-relaxed">
                    <code>{exportedCode}</code>
                  </pre>
                </div>
              )}
            </div>
          </div>

        </div>
      ) : (
        /* Incident Impact Explorer */
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          
          {/* Analysis Form */}
          <div className="lg:col-span-1 space-y-6">
            <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
              <h2 className="text-md font-semibold text-slate-900 border-b pb-3 flex items-center">
                <ShieldAlert className="w-4 h-4 mr-2 text-rose-500" />
                Threat Parameters
              </h2>

              <div className="space-y-4">
                
                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase block">Incident Vector Category</label>
                  <select
                    className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                    value={incidentType}
                    onChange={(e) => {
                      const type = e.target.value as any;
                      setIncidentType(type);
                      setImpactReport(null);
                      if (type === 'credential') setCompromisedValue('usr_john_doe');
                      else if (type === 'region') setCompromisedValue('ap-south-1');
                      else if (type === 'policy') setCompromisedValue('pol_v2.4.1');
                      else if (type === 'delegation') setCompromisedValue('usr_alice_manager');
                    }}
                  >
                    <option value="credential">Compromised Credential / Principal</option>
                    <option value="region">Compromised Regional Ingress (Sovereignty)</option>
                    <option value="policy">Compromised Policy Bundle (Stale/Malicious)</option>
                    <option value="delegation">Suspicious Delegation Grant Expiry</option>
                  </select>
                </div>

                <div className="space-y-1.5">
                  <label className="text-xs font-semibold text-slate-500 uppercase block">Target Vector Value</label>
                  {incidentType === 'credential' ? (
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                      value={compromisedValue}
                      onChange={(e) => setCompromisedValue(e.target.value)}
                    >
                      <option value="usr_john_doe">John Doe (corp-engineering user)</option>
                      <option value="usr_sarah_connor">Sarah Connor (corp-finance auditor)</option>
                      <option value="svc_crm_sync">CRM Sync Bot (corp-sales service account)</option>
                    </select>
                  ) : incidentType === 'region' ? (
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                      value={compromisedValue}
                      onChange={(e) => setCompromisedValue(e.target.value)}
                    >
                      <option value="ap-south-1">ap-south-1 (Sovereignty Denied region)</option>
                      <option value="us-east-1">us-east-1 (Primary prod region)</option>
                    </select>
                  ) : incidentType === 'policy' ? (
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                      value={compromisedValue}
                      onChange={(e) => setCompromisedValue(e.target.value)}
                    >
                      <option value="pol_v2.4.1">pol_v2.4.1 (Older stable)</option>
                      <option value="pol_v2.4.2">pol_v2.4.2 (Latest stable)</option>
                    </select>
                  ) : (
                    <select
                      className="w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:outline-none"
                      value={compromisedValue}
                      onChange={(e) => setCompromisedValue(e.target.value)}
                    >
                      <option value="usr_alice_manager">Alice Manager (Delegator)</option>
                    </select>
                  )}
                </div>

                <button
                  onClick={handleAnalyzeImpact}
                  disabled={isAnalyzing}
                  className="w-full py-2.5 bg-rose-600 hover:bg-rose-700 text-white font-semibold text-sm rounded-lg shadow-sm transition-all flex items-center justify-center space-x-2 disabled:bg-rose-300"
                >
                  {isAnalyzing ? (
                    <>
                      <RefreshCw className="w-4 h-4 animate-spin" />
                      <span>Tracing Blast-Radius...</span>
                    </>
                  ) : (
                    <>
                      <Activity className="w-4 h-4" />
                      <span>Trace Incident Blast Radius</span>
                    </>
                  )}
                </button>

              </div>
            </div>
          </div>

          {/* Blast Radius Report Output */}
          <div className="lg:col-span-2 space-y-6">
            {impactReport ? (
              <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6">
                
                {/* Blast Radius Stats Header */}
                <div className="flex justify-between items-center border-b pb-4">
                  <div>
                    <h3 className="text-md font-semibold text-slate-900">Blast Radius Assessment</h3>
                    <p className="text-xs text-slate-500 mt-0.5">Retroactive trace completed against historical state logs</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-bold border uppercase ${
                    impactReport.riskScore === 'Critical' ? 'bg-rose-50 border-rose-200 text-rose-700 animate-pulse' :
                    impactReport.riskScore === 'High' ? 'bg-orange-50 border-orange-200 text-orange-700' :
                    'bg-amber-50 border-amber-200 text-amber-700'
                  }`}>
                    Risk Level: {impactReport.riskScore}
                  </span>
                </div>

                {/* Explanation text */}
                <div className="bg-slate-50 p-4 rounded-xl border border-slate-200 text-xs text-slate-700 leading-relaxed">
                  <p className="font-semibold text-slate-900">Explaining Analysis:</p>
                  <p className="mt-1">{impactReport.explanation}</p>
                </div>

                {/* Impact stats grid */}
                <div className="grid grid-cols-2 md:grid-cols-3 gap-4 text-center">
                  <div className="p-4 border border-slate-200 rounded-lg bg-slate-50">
                    <p className="text-2xl font-bold text-slate-900">{impactReport.affectedDecisions.length}</p>
                    <p className="text-[10px] text-slate-500 font-bold uppercase mt-1">Affected Decisions</p>
                  </div>
                  <div className="p-4 border border-slate-200 rounded-lg bg-slate-50">
                    <p className="text-2xl font-bold text-slate-900">{impactReport.sessions}</p>
                    <p className="text-[10px] text-slate-500 font-bold uppercase mt-1">Suspicious Sessions</p>
                  </div>
                  <div className="p-4 border border-slate-200 rounded-lg bg-slate-50 col-span-2 md:col-span-1">
                    <p className="text-2xl font-bold text-slate-900">100%</p>
                    <p className="text-[10px] text-slate-500 font-bold uppercase mt-1">Audit Traceability</p>
                  </div>
                </div>

                {/* Affected Decisions List */}
                <div className="space-y-3">
                  <h4 className="text-xs font-bold text-slate-400 uppercase">Linked High-Risk Decisions</h4>
                  {impactReport.affectedDecisions.length > 0 ? (
                    <div className="space-y-2 max-h-40 overflow-y-auto">
                      {impactReport.affectedDecisions.map((dec: any) => (
                        <div key={dec.id} className="p-3 border border-slate-200 rounded-lg flex justify-between items-center text-xs">
                          <div>
                            <p className="font-semibold text-slate-900">{dec.subject.name} requested {dec.action.toUpperCase()} on {dec.resource.name}</p>
                            <p className="text-[10px] text-slate-400 mt-0.5">ID: {dec.id.substring(0, 16)}... • Tenant: {dec.tenant}</p>
                          </div>
                          <span className={`px-2 py-0.5 rounded font-bold text-[10px] uppercase border ${
                            dec.effect === 'permit' ? 'bg-emerald-50 text-emerald-700 border-emerald-100' : 'bg-rose-50 text-rose-700 border-rose-100'
                          }`}>
                            {dec.effect}
                          </span>
                        </div>
                      ))}
                    </div>
                  ) : (
                    <p className="text-xs text-slate-400 italic">No historical decisions impacted by this compromised asset vector.</p>
                  )}
                </div>

                {/* Recommendations */}
                <div className="space-y-3 pt-4 border-t border-slate-100">
                  <h4 className="text-xs font-bold text-slate-400 uppercase flex items-center">
                    <Activity className="w-3.5 h-3.5 text-rose-500 mr-1.5" /> Recommended Containment Actions
                  </h4>
                  <ul className="space-y-2">
                    {impactReport.recommendations.map((rec: string, idx: number) => (
                      <li key={idx} className="flex items-start text-xs text-slate-700">
                        <span className="h-5 w-5 rounded-full bg-rose-50 text-rose-600 border border-rose-100 font-bold text-[10px] flex items-center justify-center shrink-0 mr-2.5 mt-0.5">{idx + 1}</span>
                        <p className="mt-0.5 font-medium">{rec}</p>
                      </li>
                    ))}
                  </ul>
                </div>

              </div>
            ) : (
              <div className="bg-white p-8 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-center items-center text-center space-y-4">
                <div className="h-12 w-12 rounded-full bg-rose-50 flex items-center justify-center text-rose-600">
                  <ShieldAlert className="w-6 h-6 animate-pulse" />
                </div>
                <div className="max-w-md">
                  <h3 className="text-md font-semibold text-slate-900">Incident Analyzer Ready</h3>
                  <p className="text-sm text-slate-500 mt-1">
                    Select a suspicious credential, stale policy, or compromised regional ingress route, and trace its exact blast radius across authorization events.
                  </p>
                </div>
              </div>
            )}
          </div>

        </div>
      )}
    </div>
  );
}
