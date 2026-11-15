import { readFileSync } from "node:fs";
import {
  createEg1Harness,
  createGate,
  createKeyRegistry,
  DEFAULT_GATE_MANIFEST,
  EG1_DEFAULT_ACTION,
  EG1_DEFAULT_SELECTOR,
} from "@emilia-protocol/gate";

const { subject, revoke } = JSON.parse(readFileSync(0, "utf8"));
const action = { ...EG1_DEFAULT_ACTION, payment_instruction_id: `interop-${subject}` };
const h = createEg1Harness({ action });
const registry = createKeyRegistry([{ kid: "interop-issuer", key: h.publicKey }]);
let reachedEntry = false;
let effects = 0;
const gate = createGate({
  manifest: DEFAULT_GATE_MANIFEST,
  keyRegistry: registry,
  approverKeys: h.approverKeys,
  rpId: h.rpId,
  allowedOrigins: h.allowedOrigins,
  allowEphemeralStore: true,
  providerEntryGuard() {
    reachedEntry = true;
    if (revoke) registry.revoke("interop-issuer");
    return registry.status()[0].active
      ? { ok: true }
      : { ok: false, reason: "issuer-revoked-before-effect", reservation: "release" };
  },
});
const input = {
  selector: EG1_DEFAULT_SELECTOR,
  receipt: h.mint({ outcome: "allow_with_signoff" }),
  observedAction: action,
};

try {
  const result = await gate.run(input, async () => ({ effects: ++effects }));
  process.stdout.write(JSON.stringify({
    allow: result.ok,
    reason: result.authorization?.reason ?? "",
    reachedEntry,
    effects,
  }));
} catch (error) {
  process.stdout.write(JSON.stringify({
    allow: false,
    reason: error.reason ?? error.message,
    reachedEntry,
    effects,
  }));
}
