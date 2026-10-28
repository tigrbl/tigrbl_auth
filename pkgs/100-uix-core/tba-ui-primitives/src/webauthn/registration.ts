import { creationOptionsFromJSON, credentialToJSON } from "./browser";
import type { RegistrationIdentity, WebAuthnResult, WebAuthnTransport } from "./types";

export async function registerPublicKeyCredential(
  identity: RegistrationIdentity,
  transport: WebAuthnTransport = globalThis,
): Promise<WebAuthnResult> {
  const optionsResponse = await transport.fetch("/webauthn/registration/options", {
    method: "POST",
    headers: { "content-type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ user_name: identity.userName, display_name: identity.displayName }),
  });
  if (!optionsResponse.ok) throw new Error("Unable to begin passkey registration");
  const options = creationOptionsFromJSON(await optionsResponse.json());
  const credential = await navigator.credentials.create({ publicKey: options });
  if (!(credential instanceof PublicKeyCredential)) throw new Error("Passkey registration was cancelled");
  const completion = await transport.fetch("/webauthn/registration/complete", {
    method: "POST",
    headers: { "content-type": "application/json" },
    credentials: "include",
    body: JSON.stringify(credentialToJSON(credential)),
  });
  if (!completion.ok) throw new Error("Unable to complete passkey registration");
  return completion.json();
}
