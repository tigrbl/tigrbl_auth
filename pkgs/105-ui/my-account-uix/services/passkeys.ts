import { registerPublicKeyCredential } from "@tigrbl-auth/uix-core";

export { registerPublicKeyCredential };

export async function listPasskeys(): Promise<Record<string, unknown>[]> {
  const response = await fetch("/webauthn/credentials", { credentials: "include" });
  if (!response.ok) throw new Error("Unable to load passkeys");
  return response.json();
}

export async function renamePasskey(credentialId: string, displayName: string): Promise<void> {
  const response = await fetch(`/webauthn/credentials/${encodeURIComponent(credentialId)}`, {
    method: "PATCH",
    headers: { "content-type": "application/json" },
    credentials: "include",
    body: JSON.stringify({ display_name: displayName }),
  });
  if (!response.ok) throw new Error("Unable to rename passkey");
}

export async function revokePasskey(credentialId: string): Promise<void> {
  const response = await fetch(`/webauthn/credentials/${encodeURIComponent(credentialId)}`, {
    method: "DELETE",
    credentials: "include",
  });
  if (!response.ok) throw new Error("Unable to revoke passkey");
}
