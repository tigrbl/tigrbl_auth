import { useState } from "react";
import { registerPublicKeyCredential } from "../services/passkeys";

export function PasskeyEnrollment({ userName, displayName, onRegistered }: { userName: string; displayName: string; onRegistered(): void }) {
  const [error, setError] = useState<string>();
  async function enroll() {
    try {
      await registerPublicKeyCredential({ userName, displayName });
      onRegistered();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Passkey enrollment failed");
    }
  }
  return <div>
    <button type="button" onClick={enroll}>Add a passkey</button>
    {error ? <p role="alert">{error}</p> : null}
  </div>;
}
