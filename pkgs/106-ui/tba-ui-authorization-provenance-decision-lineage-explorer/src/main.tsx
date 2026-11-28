import { dashboard, element, json, type Row } from "../../_prototype/dashboard";
import { ReplayMode } from "./types";
import "../../_prototype/styles.css";

const main = dashboard("Decision Lineage Explorer", "Filter sample decisions by subject, resource, action, or outcome.", [
  {
    "name": "Decisions",
    "path": "/api/decisions",
    "columns": [
      [
        "Decision",
        "id"
      ],
      [
        "Subject",
        "subject.id"
      ],
      [
        "Resource",
        "resource.id"
      ],
      [
        "Action",
        "action"
      ],
      [
        "Outcome",
        "effect"
      ],
      [
        "Reason",
        "safeReason"
      ]
    ]
  },
  {
    "name": "Replays",
    "path": "/api/replays",
    "columns": [
      [
        "Target",
        "targetDecisionId"
      ],
      [
        "Mode",
        "mode"
      ],
      [
        "Outcome",
        "result.replayedOutcome"
      ]
    ]
  }
]);

const panel = element("section");
panel.className = "panel";
const button = element("button", "Replay latest decision");
const output = element("p", "Compare the latest trace with the same sample policy and inputs.");
output.setAttribute("role", "status");
panel.append(element("h2", "Historical replay"), button, output);
main.append(panel);

button.addEventListener("click", async () => {
  button.disabled = true;
  output.textContent = "Replaying…";
  try {
    const decisions = await json("/api/decisions") as Row[];
    if (!decisions.length) throw new Error("There is no decision to replay.");
    const replay = await json("/api/replays", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ targetDecisionId: decisions[0].id, mode: ReplayMode.EXACT_HISTORICAL }),
    }) as { result: { isReproducible: boolean; originalOutcome: string; replayedOutcome: string } };
    const { result } = replay;
    output.textContent = (result.isReproducible ? "Replay matched" : "Replay differed") +
      ": " + result.originalOutcome + " → " + result.replayedOutcome + ".";
  } catch (error) {
    output.textContent = error instanceof Error ? error.message : "Replay failed.";
  } finally {
    button.disabled = false;
  }
});
