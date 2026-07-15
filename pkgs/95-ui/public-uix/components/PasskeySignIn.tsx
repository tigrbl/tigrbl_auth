import { useState } from "react";
import { authenticateWithPublicKeyCredential } from "../services/webauthn";

export interface PasskeySignInProps {
  userName?: string;
  onAuthenticated(result: Record<string, unknown>): void;
}

export function PasskeySignIn({ userName, onAuthenticated }: PasskeySignInProps) {
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  async function signIn() {
    setBusy(true);
    setError(undefined);
    try {
      onAuthenticated(await authenticateWithPublicKeyCredential({ userName }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Passkey sign-in failed");
    } finally {
      setBusy(false);
    }
  }
  return <div>
    <button type="button" disabled={busy} onClick={signIn}>{busy ? "Waiting for passkey…" : "Sign in with a passkey"}</button>
    {error ? <p role="alert">{error}</p> : null}
  </div>;
}
