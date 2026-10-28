/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import express from "express";
import path from "path";
import { createServer as createViteServer } from "vite";
import { dbInstance } from "./src/db";
import { AuthorizationEngine, generateId } from "./src/engine";
import {
  AuthZenEvaluationRequest,
  Policy,
  PolicyLifecycle,
  Role,
  RoleAssignment,
  DelegationGrant,
  RelationshipTuple,
  Permission
} from "./src/types";

async function startServer() {
  const app = express();
  const PORT = 3000;

  // Middleware for body parsing
  app.use(express.json());

  // Log incoming requests for debugging in the sandbox
  app.use((req, res, next) => {
    console.log(`[API ${new Date().toISOString()}] ${req.method} ${req.url}`);
    next();
  });

  // --- DECISION PLANE ENDPOINTS (AuthZEN Aligned) ---

  /**
   * POST /api/access/v1/evaluation
   * Evaluates a single access request against active policies
   */
  app.post("/api/access/v1/evaluation", (req, res) => {
    try {
      const evaluationRequest = req.body as AuthZenEvaluationRequest;
      const state = dbInstance.get();
      const engine = new AuthorizationEngine({
        ...state,
        tuples: state.relationshipTuples
      });

      const result = engine.evaluate(evaluationRequest);

      // Persist the redacted trace and the non-bearer decision receipt
      dbInstance.logDecisionResult(result.trace, result.receipt);

      res.status(200).json(result.response);
    } catch (error: any) {
      console.error("Evaluation PDP Failure:", error);
      res.status(500).json({
        decision: "deny",
        policySetVersion: "fail-closed",
        safeReason: `Internal PDP Server Error: ${error.message || error}`,
        obligations: [],
        advice: [],
        decisionId: generateId("err_"),
        expirySeconds: 0,
        evaluatedAt: new Date().toISOString()
      });
    }
  });

  /**
   * POST /api/access/v1/evaluations
   * Batch/Boxcar evaluation for multiple requests
   */
  app.post("/api/access/v1/evaluations", (req, res) => {
    try {
      const { requests } = req.body as { requests: AuthZenEvaluationRequest[] };
      if (!Array.isArray(requests)) {
        res.status(400).json({ error: "Batch request requires a top-level 'requests' array." });
        return;
      }

      const state = dbInstance.get();
      const engine = new AuthorizationEngine({
        ...state,
        tuples: state.relationshipTuples
      });
      const responses = requests.map((item) => {
        const result = engine.evaluate(item);
        dbInstance.logDecisionResult(result.trace, result.receipt);
        return result.response;
      });

      res.status(200).json({ responses });
    } catch (error: any) {
      console.error("Batch Evaluation PDP Failure:", error);
      res.status(500).json({ error: "Batch evaluation engine fail-closed: " + error.message });
    }
  });


  // --- MANAGEMENT PLANE ENDPOINTS (Policy Studio API) ---

  // Expose entire DB payload for front-end visualizers and graph explorers
  app.get("/api/admin/authorization/db", (req, res) => {
    res.status(200).json(dbInstance.get());
  });

  // Catalogs
  app.post("/api/admin/authorization/catalogs/register", (req, res) => {
    const { permission, actorId, rationale } = req.body as { permission: Permission; actorId: string; rationale: string };
    if (!permission || !actorId) {
      res.status(400).json({ error: "Permission definition and actorId are required." });
      return;
    }
    dbInstance.registerPermission(permission, actorId, rationale || "API Catalog Registration");
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.post("/api/admin/authorization/catalogs/deprecate", (req, res) => {
    const { permissionId, replacementId, actorId, rationale } = req.body as { permissionId: string; replacementId?: string; actorId: string; rationale: string };
    if (!permissionId || !actorId) {
      res.status(400).json({ error: "PermissionId and actorId are required." });
      return;
    }
    dbInstance.deprecatePermission(permissionId, replacementId, actorId, rationale || "Deprecation flow");
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  // Roles & Assignments
  app.post("/api/admin/authorization/roles", (req, res) => {
    const { role, actorId, rationale, isEdit } = req.body as { role: Role; actorId: string; rationale: string; isEdit: boolean };
    if (!role || !actorId) {
      res.status(400).json({ error: "Role and actorId are required." });
      return;
    }
    if (isEdit) {
      dbInstance.updateRole(role, actorId, rationale);
    } else {
      dbInstance.createRole(role, actorId, rationale);
    }
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.delete("/api/admin/authorization/roles/:id", (req, res) => {
    const roleId = req.params.id;
    const { tenantId, actorId, rationale } = req.query as { tenantId: string; actorId: string; rationale: string };
    if (!tenantId || !actorId) {
      res.status(400).json({ error: "tenantId and actorId query parameters are required." });
      return;
    }
    dbInstance.deleteRole(roleId, tenantId, actorId, rationale || "Administrative deletion");
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.post("/api/admin/authorization/assignments", (req, res) => {
    const { assignment, actorId, rationale } = req.body as { assignment: RoleAssignment; actorId: string; rationale: string };
    if (!assignment || !actorId) {
      res.status(400).json({ error: "Assignment and actorId are required." });
      return;
    }
    dbInstance.createAssignment(assignment, actorId, rationale);
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.delete("/api/admin/authorization/assignments/:id", (req, res) => {
    const asgId = req.params.id;
    const { tenantId, actorId, rationale } = req.query as { tenantId: string; actorId: string; rationale: string };
    if (!tenantId || !actorId) {
      res.status(400).json({ error: "tenantId and actorId query parameters are required." });
      return;
    }
    dbInstance.revokeAssignment(asgId, tenantId, actorId, rationale || "Administrative revocation");
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  // Policies
  app.post("/api/admin/authorization/policies", (req, res) => {
    const { policy, actorId, rationale, isEdit } = req.body as { policy: Policy; actorId: string; rationale: string; isEdit: boolean };
    if (!policy || !actorId) {
      res.status(400).json({ error: "Policy and actorId are required." });
      return;
    }
    if (isEdit) {
      dbInstance.updatePolicy(policy, actorId, rationale);
    } else {
      dbInstance.createPolicy(policy, actorId, rationale);
    }
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.post("/api/admin/authorization/policies/status", (req, res) => {
    const { policyId, status, tenantId, actorId, rationale } = req.body as { policyId: string; status: PolicyLifecycle; tenantId: string; actorId: string; rationale: string };
    if (!policyId || !status || !tenantId || !actorId) {
      res.status(400).json({ error: "policyId, status, tenantId, and actorId are required." });
      return;
    }
    dbInstance.changePolicyLifecycle(policyId, status, tenantId, actorId, rationale);
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  // Delegations
  app.post("/api/admin/authorization/delegations", (req, res) => {
    const { delegation, actorId, rationale } = req.body as { delegation: DelegationGrant; actorId: string; rationale: string };
    if (!delegation || !actorId) {
      res.status(400).json({ error: "Delegation and actorId are required." });
      return;
    }
    dbInstance.createDelegation(delegation, actorId, rationale);
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.delete("/api/admin/authorization/delegations/:id", (req, res) => {
    const delegationId = req.params.id;
    const { tenantId, actorId, rationale } = req.query as { tenantId: string; actorId: string; rationale: string };
    if (!tenantId || !actorId) {
      res.status(400).json({ error: "tenantId and actorId query parameters are required." });
      return;
    }
    dbInstance.revokeDelegation(delegationId, tenantId, actorId, rationale || "Administrative expiry/revocation");
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  // ReBAC Relationships
  app.post("/api/admin/authorization/relationships/tuples", (req, res) => {
    const { tuple, actorId } = req.body as { tuple: RelationshipTuple; actorId: string };
    if (!tuple || !actorId) {
      res.status(400).json({ error: "Tuple and actorId are required." });
      return;
    }
    dbInstance.createRelationshipTuple(tuple, actorId);
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  app.delete("/api/admin/authorization/relationships/tuples/:id", (req, res) => {
    const tupleId = req.params.id;
    const { tenantId, actorId } = req.query as { tenantId: string; actorId: string };
    if (!tenantId || !actorId) {
      res.status(400).json({ error: "tenantId and actorId query parameters are required." });
      return;
    }
    dbInstance.deleteRelationshipTuple(tupleId, tenantId, actorId);
    res.status(200).json({ status: "success", db: dbInstance.get() });
  });

  /**
   * POST /api/admin/authorization/simulations
   * Side-effect-free evaluation lab comparing ACTIVE policies versus a PROPOSED policy change.
   */
  app.post("/api/admin/authorization/simulations", (req, res) => {
    try {
      const { fixtures, proposedPolicy } = req.body as {
        fixtures: AuthZenEvaluationRequest[];
        proposedPolicy: Policy;
      };

      if (!Array.isArray(fixtures)) {
        res.status(400).json({ error: "Fixtures array is required." });
        return;
      }

      const state = dbInstance.get();
      const currentEngine = new AuthorizationEngine({
        ...state,
        tuples: state.relationshipTuples
      });

      // Create an overridden policy list for proposed simulation dry-runs
      let proposedPolicies = [...state.policies];
      if (proposedPolicy) {
        const existingIdx = proposedPolicies.findIndex((p) => p.id === proposedPolicy.id);
        if (existingIdx !== -1) {
          proposedPolicies[existingIdx] = proposedPolicy;
        } else {
          proposedPolicies.push(proposedPolicy);
        }
      }

      const simulationEngine = new AuthorizationEngine({
        ...state,
        tuples: state.relationshipTuples
      });

      const results = fixtures.map((reqFixture) => {
        // Evaluate active engine
        const currentRes = currentEngine.evaluate(reqFixture);
        // Evaluate proposed engine with sandboxed policy set override
        const proposedRes = simulationEngine.evaluate(reqFixture, proposedPolicies);

        // Compute least-authority differences
        const addedPermissions: string[] = [];
        const removedPermissions: string[] = [];

        if (currentRes.response.decision === "deny" && proposedRes.response.decision === "permit") {
          addedPermissions.push(`${reqFixture.action.name} on ${reqFixture.resource.type}:${reqFixture.resource.id}`);
        } else if (currentRes.response.decision === "permit" && proposedRes.response.decision === "deny") {
          removedPermissions.push(`${reqFixture.action.name} on ${reqFixture.resource.type}:${reqFixture.resource.id}`);
        }

        const obligationsChanged =
          JSON.stringify(currentRes.response.obligations) !== JSON.stringify(proposedRes.response.obligations);

        return {
          requestId: generateId("sim_"),
          request: reqFixture,
          currentDecision: currentRes.response.decision,
          currentTraceId: currentRes.response.traceReference,
          proposedDecision: proposedRes.response.decision,
          proposedTraceId: proposedRes.response.traceReference,
          decisionChanged: currentRes.response.decision !== proposedRes.response.decision,
          obligationsChanged,
          leastAuthorityDiff: {
            addedPermissions,
            removedPermissions
          }
        };
      });

      res.status(200).json({ results });
    } catch (error: any) {
      console.error("Simulation Lab evaluation failure:", error);
      res.status(500).json({ error: "Simulation lab crash: " + error.message });
    }
  });


  // --- STATIC ASSET SERVING & SPA ROUTING ---

  if (process.env.NODE_ENV !== "production") {
    const vite = await createViteServer({
      server: { middlewareMode: true },
      appType: "spa"
    });
    app.use(vite.middlewares);
  } else {
    const distPath = path.join(process.cwd(), "dist");
    app.use(express.static(distPath));
    app.get("*", (req, res) => {
      res.sendFile(path.join(distPath, "index.html"));
    });
  }

  app.listen(PORT, "0.0.0.0", () => {
    console.log(`[Tigrbl Server] Running at http://0.0.0.0:${PORT}`);
  });
}

startServer().catch((err) => {
  console.error("Failed to start server:", err);
});
