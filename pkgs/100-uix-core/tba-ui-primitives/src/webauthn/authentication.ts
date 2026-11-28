import { credentialToJSON, requestOptionsFromJSON } from "./browser";
import type { AuthenticationIdentity, WebAuthnResult, WebAuthnTransport } from "./types";

export async function authenticateWithPublicKeyCredential(
  identity: AuthenticationIdentity = {},
  transport: WebAuthnTransport = globalThis,
): Promise<WebAuthnResult> {
  const optionsResponse = await transport.fetch("/webauthn/authentication/options", {
    method: "POST",
    headers: { "content-type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ user_name: identity.userName, conditional: identity.conditional ?? false }),
  });
  if (!optionsResponse.ok) throw new Error("Unable to begin passkey authentication");
  const options = requestOptionsFromJSON(await optionsResponse.json());
  const credential = await navigator.credentials.get({
    publicKey: options,
    mediation: identity.conditional ? "conditional" : "optional",
  });
  if (!(credential instanceof PublicKeyCredential)) throw new Error("Passkey authentication was cancelled");
  const completion = await transport.fetch("/webauthn/authentication/complete", {
    method: "POST",
    headers: { "content-type": "application/json" },
    credentials: "include",
    body: JSON.stringify(credentialToJSON(credential)),
  });
  if (!completion.ok) throw new Error("Unable to complete passkey authentication");
  return completion.json();
}
