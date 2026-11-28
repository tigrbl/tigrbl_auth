import { useEffect } from "react";
import { authenticateWithPublicKeyCredential } from "../services/webauthn";
import "./PasskeyConditionalSignIn.css";

export function PasskeyConditionalSignIn({ onAuthenticated }: { onAuthenticated(result: Record<string, unknown>): void }) {
  useEffect(() => {
    if (!("PublicKeyCredential" in globalThis)) return;
    const available = PublicKeyCredential.isConditionalMediationAvailable?.();
    available?.then((supported) => {
      if (supported) authenticateWithPublicKeyCredential({ conditional: true }).then(onAuthenticated).catch(() => undefined);
    });
  }, [onAuthenticated]);
  return null;
}
