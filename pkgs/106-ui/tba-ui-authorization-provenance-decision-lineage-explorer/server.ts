/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from "express";
import fs from "fs";
import path from "path";
import dotenv from "dotenv";
import { INITIAL_DECISIONS, MockPolicyEngine, generateStableKey, calculateSimpleHash } from "./src/data.ts";
import { DecisionTrace, EvaluationOutcome, ReplayJob, ReplayMode, ComparisonReport, StepOutcome, AuthorityType } from "./src/types.ts";

dotenv.config();

const app = express();
app.use(express.json());

const PORT = 3000;

// In-Memory Database State
let decisions: DecisionTrace[] = [...INITIAL_DECISIONS];
let replayJobs: ReplayJob[] = [];

// API: Search & Bounded Query Filter for Decisions
app.get("/api/decisions", (req, res) => {
  const { tenant, env, search, effect, subjectId, resourceId, action } = req.query;
  
  let filtered = decisions;

  if (tenant) {
    filtered = filtered.filter(d => d.tenantId === tenant);
  }
  if (env) {
    filtered = filtered.filter(d => d.environment === env);
  }
  if (effect) {
    filtered = filtered.filter(d => d.effect === effect);
  }
  if (subjectId) {
    filtered = filtered.filter(d => d.subject.id === subjectId);
  }
  if (resourceId) {
    filtered = filtered.filter(d => d.resource.id === resourceId);
  }
  if (action) {
    filtered = filtered.filter(d => d.action === action);
  }
  
  if (search) {
    const q = (search as string).toLowerCase();
    filtered = filtered.filter(d => 
      d.id.toLowerCase().includes(q) ||
      d.correlationId.toLowerCase().includes(q) ||
      d.subject.id.toLowerCase().includes(q) ||
      d.resource.id.toLowerCase().includes(q) ||
      d.action.toLowerCase().includes(q) ||
      d.safeReason.toLowerCase().includes(q)
    );
  }

  res.json(filtered);
});

// API: GET Single Decision
app.get("/api/decisions/:id", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) {
    return res.status(404).json({ error: "Decision trace not found" });
  }
  res.json(decision);
});

// API: Nested Lineage Projection
app.get("/api/decisions/:id/lineage", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  res.json(decision.policyLineage);
});

// API: Authorized projections for Facts
app.get("/api/decisions/:id/facts", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  // In a real system, we'd apply field-level authorization here.
  res.json(decision.facts);
});

// API: Steps Projection
app.get("/api/decisions/:id/steps", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  res.json(decision.steps);
});

// API: Authority Paths Projection
app.get("/api/decisions/:id/authority-paths", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  res.json(decision.authorityPaths);
});

// API: Linked Delegation Projection
app.get("/api/decisions/:id/delegation", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  // Returns delegation facts and delegation-typed authority paths
  const delegationPaths = decision.authorityPaths.filter(p => p.type === "delegation_grant");
  const delegationFacts = decision.facts.filter(f => f.type === "delegation_proof");
  res.json({ delegationPaths, delegationFacts });
});

// API: Tokens, Sessions, and Outcomes Linkage
app.get("/api/decisions/:id/tokens-sessions-outcomes", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  res.json({
    tokenId: decision.outcomeLink?.tokenId,
    sessionId: decision.sessionId,
    transactionId: decision.transactionId,
    outcome: decision.outcomeLink
  });
});

// API: Enforcement Outcome Projection
app.get("/api/decisions/:id/enforcement", (req, res) => {
  const decision = decisions.find(d => d.id === req.params.id);
  if (!decision) return res.status(404).json({ error: "Decision trace not found" });
  res.json(decision.outcomeLink || { error: "No enforcement link present for this decision" });
});

// API: Ingest dynamic new Trace
app.post("/api/ingest", (req, res) => {
  const traceInput = req.body;
  if (!traceInput.subject || !traceInput.resource || !traceInput.action) {
    return res.status(400).json({ error: "Invalid ingestion envelope. Missing subject, resource, or action." });
  }

  // Calculate deterministic keys and hashes
  const decisionId = `dec-${Date.now()}-${Math.floor(Math.random() * 1000)}`;
  const timestamp = new Date().toISOString();
  const policyVersion = traceInput.policyVersion || "1.0.0";
  
  // Dynamic calculation using Mock Engine
  const roles = traceInput.subject.roles || ["employee"];
  const classification = traceInput.resource.classification || "unclassified";
  const deviceScore = parseInt(traceInput.context?.device_trust_score || "80", 10);
  const mfa = traceInput.context?.mfa_verified === "true";
  const destRegion = traceInput.context?.destination_region || "";
  const isEmergency = traceInput.context?.is_emergency_mode === "true";

  const evaluation = MockPolicyEngine.evaluate(
    roles,
    classification,
    deviceScore,
    mfa,
    traceInput.context?.ip_address || "127.0.0.1",
    destRegion,
    isEmergency,
    policyVersion
  );

  const newTrace: DecisionTrace = {
    id: decisionId,
    decisionKey: generateStableKey(traceInput.subject.id, traceInput.resource.id, traceInput.action, policyVersion),
    tenantId: traceInput.tenantId || "tenant-acme-corp",
    environment: traceInput.environment || "production",
    region: traceInput.region || "us-east1",
    correlationId: traceInput.correlationId || `corr-ingest-${Date.now()}`,
    requestId: traceInput.requestId || `req-ingest-${Date.now()}`,
    sessionId: traceInput.sessionId || "sess-dynamic-active",
    transactionId: traceInput.transactionId,
    timestamp,
    durationMs: Math.floor(Math.random() * 15) + 5,
    expiryDeadline: new Date(Date.now() + 300000).toISOString(),
    subject: {
      id: traceInput.subject.id,
      type: "user",
      roles
    },
    resource: {
      id: traceInput.resource.id,
      type: traceInput.resource.type || "document",
      attributes: {
        classification,
        region: traceInput.region || "us-east1",
        ...traceInput.resource.attributes
      }
    },
    action: traceInput.action,
    context: traceInput.context || {},
    effect: evaluation.effect,
    safeReason: evaluation.reason,
    obligations: evaluation.obligations.map(name => ({
      name,
      status: "fulfilled",
      receiptId: `rec-ing-${Date.now()}`
    })),
    policyLineage: {
      bundleId: "pb-finance-docs",
      bundleVersion: policyVersion,
      bundleHash: calculateSimpleHash(`bundle-${policyVersion}`),
      engineVersion: "MockRegoEngine/v3.0",
      applicableRules: evaluation.steps.map(s => s.ruleName),
      combiningAlgorithm: "deny-overrides",
      hasConflicts: false
    },
    facts: [
      {
        id: `f-${Date.now()}-1`,
        type: "role_assignment",
        schemaVersion: "1.0",
        associatedWith: "subject",
        key: "subject.roles",
        rawValue: JSON.stringify(roles),
        isRedacted: false,
        sourceSystem: "IdentityMfaStore",
        resolver: "OktaRoleResolver",
        version: "v1.0",
        observedAt: timestamp,
        effectiveAt: timestamp,
        confidence: 1.0,
        cacheStatus: "hit",
        digest: calculateSimpleHash(JSON.stringify(roles))
      },
      {
        id: `f-${Date.now()}-2`,
        type: "device_telemetry",
        schemaVersion: "1.0",
        associatedWith: "context",
        key: "context.device_trust_score",
        rawValue: String(deviceScore),
        isRedacted: false,
        sourceSystem: "CrowdStrike",
        resolver: "SentinelEndpointResolver",
        version: "v1.0",
        observedAt: timestamp,
        effectiveAt: timestamp,
        confidence: 0.95,
        cacheStatus: "miss",
        digest: calculateSimpleHash(String(deviceScore))
      }
    ],
    steps: evaluation.steps,
    authorityPaths: roles.map((r, idx) => ({
      id: `ap-${Date.now()}-${idx}`,
      type: AuthorityType.DIRECT_ASSIGNMENT,
      source: `role-group/${r}`,
      target: `permission/${traceInput.action}`,
      isVerified: true,
      freshnessSeconds: 120,
      confidence: 1.0
    })),
    outcomeLink: {
      pepId: traceInput.pepId || "pep-dynamic-ingress",
      pepVersion: "Envoy/v1.26.0",
      enforcementStatus: "operation_succeeded",
      enforcedAt: timestamp,
      receiptSignature: calculateSimpleHash(`signature-enforce-${decisionId}`)
    },
    integritySeal: calculateSimpleHash(`seal-${decisionId}`),
    isLegalHold: false,
    retentionExpiresAt: new Date(Date.now() + 315360000000).toISOString() // 10 years
  };

  decisions.unshift(newTrace);
  res.status(201).json(newTrace);
});

// API: Replay Workbench Trigger
app.post("/api/replays", (req, res) => {
  const { mode, targetDecisionId, substitutions, policyBundleVersion, purpose } = req.body;
  
  const targetTrace = decisions.find(d => d.id === targetDecisionId);
  if (!targetTrace) {
    return res.status(404).json({ error: "Target decision trace for replay not found" });
  }

  const jobId = `job-${Date.now()}`;
  const timestamp = new Date().toISOString();

  // Mode calculations
  let isReproducible = true;
  let replayedOutcome = targetTrace.effect;
  const differences: string[] = [];
  const missingEvidence: string[] = [];

  // Map inputs from original trace, merging substitutions
  const roles = targetTrace.subject.roles;
  const classification = substitutions["resource.classification"] || targetTrace.resource.attributes.classification || "unclassified";
  const deviceScore = parseInt(substitutions["context.device_trust_score"] || targetTrace.context.device_trust_score || "80", 10);
  const mfa = (substitutions["context.mfa_verified"] !== undefined) 
    ? substitutions["context.mfa_verified"] === "true" 
    : targetTrace.context.mfa_verified === "true";
  const destRegion = substitutions["context.destination_region"] || targetTrace.context.destination_region || "";
  const isEmergency = substitutions["context.is_emergency_mode"] === "true" || targetTrace.context.is_emergency_mode === "true";

  const targetVersion = policyBundleVersion || targetTrace.policyLineage.bundleVersion;

  // Execute replay through the mock engine
  const evalResult = MockPolicyEngine.evaluate(
    roles,
    classification,
    deviceScore,
    mfa,
    targetTrace.context.ip_address || "127.0.0.1",
    destRegion,
    isEmergency,
    targetVersion,
    substitutions
  );

  replayedOutcome = evalResult.effect;

  if (mode === ReplayMode.EXACT_HISTORICAL) {
    // If exact historical replay, verify that inputs match and output is identical
    const changedFields = Object.keys(substitutions || {});
    if (changedFields.length > 0) {
      isReproducible = false;
      differences.push(`Substitutions present: ${changedFields.join(", ")}. Sandbox bypasses historical purity.`);
    }
    if (replayedOutcome !== targetTrace.effect) {
      isReproducible = false;
      differences.push(`Outcome Drift: Original was '${targetTrace.effect}', but replayed is '${replayedOutcome}'.`);
    }
  } else if (mode === ReplayMode.CURRENT_ENGINE) {
    if (replayedOutcome !== targetTrace.effect) {
      differences.push(`Behavioral Engine Drift: Original effect was '${targetTrace.effect}', replayed outcome is '${replayedOutcome}' under the latest compilation schema.`);
    }
  } else if (mode === ReplayMode.CURRENT_STATE) {
    // Check what would happen now - represents dynamic changes
    if (replayedOutcome !== targetTrace.effect) {
      differences.push(`State Shift: Replaying historical context with active policy yields '${replayedOutcome}' instead of '${targetTrace.effect}'.`);
    }
  } else if (mode === ReplayMode.COUNTERFACTUAL) {
    // Intended changes
    if (replayedOutcome !== targetTrace.effect) {
      differences.push(`Counterfactual delta confirmed: Effect flipped from '${targetTrace.effect}' to '${replayedOutcome}'.`);
    } else {
      differences.push(`No Effect Drift: The outcome remained '${replayedOutcome}' despite counterfactual injections.`);
    }
  }

  const jobResult: ReplayJob = {
    id: jobId,
    mode,
    targetDecisionId,
    timestamp,
    runBy: "jick.68.0@gmail.com",
    status: "completed",
    substitutions: substitutions || {},
    policyBundleVersionUsed: targetVersion,
    expectedCostSecs: 0.25,
    purpose: purpose || "Forensic lineage validation",
    result: {
      isReproducible: isReproducible && (replayedOutcome === targetTrace.effect),
      originalOutcome: targetTrace.effect,
      replayedOutcome,
      durationMs: Math.floor(Math.random() * 8) + 2,
      differences,
      missingEvidence
    }
  };

  replayJobs.unshift(jobResult);
  res.status(201).json(jobResult);
});

// API: Replays List
app.get("/api/replays", (req, res) => {
  res.json(replayJobs);
});

// API: Decision Stability & Drift Comparison
app.post("/api/comparisons", (req, res) => {
  const { sourceDecisionId, targetDecisionId } = req.body;
  
  const source = decisions.find(d => d.id === sourceDecisionId);
  const target = decisions.find(d => d.id === targetDecisionId);

  if (!source || !target) {
    return res.status(404).json({ error: "Source or Target decision trace not found for comparison" });
  }

  const effectChanged = source.effect !== target.effect;
  const changedAuthorityPaths: string[] = [];
  const changedRules: string[] = [];
  const changedFacts: string[] = [];
  const addedObligations: string[] = [];
  const removedObligations: string[] = [];

  // Compare facts
  const sourceFactKeys = source.facts.map(f => f.key);
  const targetFactKeys = target.facts.map(f => f.key);
  
  sourceFactKeys.forEach(key => {
    const sFact = source.facts.find(f => f.key === key);
    const tFact = target.facts.find(f => f.key === key);
    if (!tFact) {
      changedFacts.push(`Fact key '${key}' missing in target trace.`);
    } else if (sFact && sFact.rawValue !== tFact.rawValue) {
      changedFacts.push(`Fact value drift for '${key}': '${sFact.rawValue}' vs '${tFact.rawValue}'`);
    }
  });

  // Compare obligations
  const sourceObs = source.obligations.map(o => o.name);
  const targetObs = target.obligations.map(o => o.name);

  targetObs.forEach(name => {
    if (!sourceObs.includes(name)) addedObligations.push(name);
  });
  sourceObs.forEach(name => {
    if (!targetObs.includes(name)) removedObligations.push(name);
  });

  // Compare rules evaluated
  const sourceRules = source.policyLineage.applicableRules;
  const targetRules = target.policyLineage.applicableRules;
  
  targetRules.forEach(r => {
    if (!sourceRules.includes(r)) changedRules.push(`Added rule: ${r}`);
  });
  sourceRules.forEach(r => {
    if (!targetRules.includes(r)) changedRules.push(`Removed rule: ${r}`);
  });

  // Compare authority paths
  const sourceAp = source.authorityPaths.map(p => `${p.source}->${p.target}`);
  const targetAp = target.authorityPaths.map(p => `${p.source}->${p.target}`);
  
  targetAp.forEach(ap => {
    if (!sourceAp.includes(ap)) changedAuthorityPaths.push(`Added path: ${ap}`);
  });
  sourceAp.forEach(ap => {
    if (!targetAp.includes(ap)) changedAuthorityPaths.push(`Removed path: ${ap}`);
  });

  const report: ComparisonReport = {
    sourceDecisionId,
    targetDecisionId,
    effectChanged,
    sourceEffect: source.effect,
    targetEffect: target.effect,
    changedAuthorityPaths,
    changedRules,
    changedFacts,
    addedObligations,
    removedObligations,
    warnings: effectChanged ? ["Warning: High impact policy effect flip detected between selected trace nodes."] : []
  };

  res.json(report);
});

// API: Incident Impact Explorer API
app.get("/api/impact", (req, res) => {
  const { type, value } = req.query;
  if (!type || !value) {
    return res.status(400).json({ error: "Missing impact scope parameters: type and value required." });
  }

  const targetVal = (value as string).toLowerCase();
  let affected: DecisionTrace[] = [];

  if (type === "credential" || type === "principal") {
    affected = decisions.filter(d => 
      d.subject.id.toLowerCase().includes(targetVal) || 
      d.subject.roles.some(r => r.toLowerCase().includes(targetVal))
    );
  } else if (type === "grant") {
    affected = decisions.filter(d => 
      d.facts.some(f => f.type === "delegation_proof" && f.rawValue.toLowerCase().includes(targetVal)) ||
      d.authorityPaths.some(p => p.via?.toLowerCase()?.includes(targetVal))
    );
  } else if (type === "policy") {
    affected = decisions.filter(d => 
      d.policyLineage.bundleId.toLowerCase().includes(targetVal) ||
      d.policyLineage.applicableRules.some(r => r.toLowerCase().includes(targetVal))
    );
  } else if (type === "pep") {
    affected = decisions.filter(d => d.outcomeLink?.pepId?.toLowerCase()?.includes(targetVal));
  } else if (type === "fact") {
    affected = decisions.filter(d => d.facts.some(f => f.sourceSystem.toLowerCase().includes(targetVal)));
  }

  // Calculate containment actions and vulnerability indexes
  const totalInScope = affected.length;
  const permitBreaches = affected.filter(d => d.effect === EvaluationOutcome.PERMIT).length;
  const distinctResources = Array.from(new Set(affected.map(d => d.resource.id)));
  const legalHoldApplied = affected.filter(d => d.isLegalHold).length;

  res.json({
    type,
    value,
    metrics: {
      totalDecisionTracesAffected: totalInScope,
      compromisedPermitCount: permitBreaches,
      impactedResourceCount: distinctResources.length,
      legalHoldRatio: totalInScope > 0 ? (legalHoldApplied / totalInScope) : 0
    },
    impactedDecisions: affected.map(d => ({
      id: d.id,
      timestamp: d.timestamp,
      subjectId: d.subject.id,
      resourceId: d.resource.id,
      action: d.action,
      effect: d.effect,
      isLegalHold: d.isLegalHold,
      pepId: d.outcomeLink?.pepId || "unknown"
    })),
    containmentStatus: totalInScope > 0 ? "remediation_required" : "fully_contained",
    recommendedActions: [
      `Enforce temporary credentials revocation for all impacted actor bindings: '${targetVal}'`,
      `Place all ${totalInScope} matched decisions on legal audit hold to preserve historical integrity seals.`,
      `Quarantine PEP access nodes interacting with ${distinctResources.length} distinct target resources.`
    ]
  });
});

// API: Legal holds, Tombstones & Retentions
app.post("/api/retention/:id", (req, res) => {
  const { action } = req.body; // "hold", "release", "tombstone"
  const idx = decisions.findIndex(d => d.id === req.params.id);
  if (idx === -1) {
    return res.status(404).json({ error: "Decision trace not found" });
  }

  const decision = decisions[idx];

  if (action === "hold") {
    decision.isLegalHold = true;
    return res.json({ success: true, message: "Decision trace placed on administrative legal hold.", decision });
  } else if (action === "release") {
    decision.isLegalHold = false;
    return res.json({ success: true, message: "Legal hold successfully removed.", decision });
  } else if (action === "tombstone") {
    if (decision.isLegalHold) {
      return res.status(400).json({ error: "Cannot delete or tombstone a trace currently under legal hold restrictions." });
    }
    
    // Perform supersession / tombstone
    const tombstoned: DecisionTrace = {
      ...decision,
      subject: { id: "REDACTED", type: "user", roles: [] },
      resource: { id: "REDACTED", type: "document", attributes: {} },
      context: { ip_address: "REDACTED" },
      safeReason: "[REDACTED - Audit trace was legally deleted and tombstoned per compliance mandate]",
      facts: [],
      steps: [],
      authorityPaths: [],
      outcomeLink: undefined,
      supersededByDecisionId: `tombstone-${Date.now()}`
    };

    decisions[idx] = tombstoned;
    return res.json({ success: true, message: "Trace successfully tombstoned and scrubbed of sensitive identifiers.", decision: tombstoned });
  }

  res.status(400).json({ error: "Invalid action type. Select hold, release, or tombstone." });
});

// Serve frontend build static files in production
async function startServer() {
  if (process.env.NODE_ENV === "production") {
    const distPath = path.resolve(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.resolve(distPath, "index.html"));
    });
  } else {
    // Integrate Vite Dev Server middleware for modern HMR-less full-stack experience
    const { createServer } = await import("vite");
    const vite = await createServer({
      server: { middlewareMode: true },
      appType: "custom"
    });
    
    app.use(vite.middlewares);
    
    app.use("*", async (req, res, next) => {
      const url = req.originalUrl;
      try {
        let template = fs.readFileSync(path.resolve(process.cwd(), "index.html"), "utf-8");
        template = await vite.transformIndexHtml(url, template);
        res.status(200).set({ "Content-Type": "text/html" }).end(template);
      } catch (e: any) {
        vite.ssrFixStacktrace(e);
        next(e);
      }
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`[Auth Provenance Server] plane running on port ${PORT}`);
  });
}

startServer();
