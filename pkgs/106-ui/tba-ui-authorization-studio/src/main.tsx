import { dashboard, element, json, type Row } from "../../_prototype/dashboard";
import "../../_prototype/styles.css";

const main = dashboard("Authorization Studio", "Inspect sample policies and evaluate a fixture in the local policy simulator.", [
  { name: "Policies", path: "/api/admin/authorization/db", select: data => (data as Row).policies,
    columns: [["Policy", "name"], ["Effect", "effect"], ["Action", "action"], ["Status", "status"]] },
  { name: "Decisions", path: "/api/admin/authorization/db", select: data => (data as Row).traces,
    columns: [["Trace", "id"], ["Tenant", "tenantId"], ["Decision", "decision"], ["Time", "evaluatedAt"]] },
]);

const panel = element("section");
panel.className = "panel";
const label = element("label", "Sample action");
const action = element("select");
action.append(element("option", "read"), element("option", "delete"));
label.append(action);
const run = element("button", "Evaluate sample request");
run.type = "button";
const output = element("p", "Use Alice’s sample account and the demo document.");
output.setAttribute("role", "status");
panel.append(element("h2", "Policy simulator"), label, element("br"), run, output);
main.append(panel);

run.addEventListener("click", async () => {
  run.disabled = true;
  output.textContent = "Evaluating…";
  try {
    const result = await json("/api/access/v1/evaluation", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ tenantId: "demo", subject: { id: "alice" },
        action: { name: action.value }, resource: { type: "document", id: "demo-document" } }),
    }) as Row;
    output.textContent = result.decision + ": " + result.safeReason;
  } catch (error) {
    output.textContent = error instanceof Error ? error.message : "Evaluation failed.";
  } finally {
    run.disabled = false;
  }
});
