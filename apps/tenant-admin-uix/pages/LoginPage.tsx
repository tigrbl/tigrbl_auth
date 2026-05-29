import { Button, DetailPanel, ErrorState, FormField, PageHeader, ResourceForm } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";

export function LoginPage({ error, onLogin }: { error: string; onLogin: (identifier: string, password: string) => Promise<void> }) {
  const [identifier, setIdentifier] = useState("admin");
  const [password, setPassword] = useState("Admin123!");
  const [submitting, setSubmitting] = useState(false);
  const [localError, setLocalError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setSubmitting(true);
    setLocalError("");
    try {
      await onLogin(identifier, password);
    } catch (nextError) {
      setLocalError(nextError instanceof Error ? nextError.message : "Unable to sign in.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div style={{ display: "grid", gap: "18px", maxWidth: "520px" }}>
      <PageHeader title="Tenant administrator sign in" description="Use a tenant-scoped administrator session to manage identities, clients, consents, and keys." />
      {(localError || error) && <ErrorState message={localError || error} />}
      <DetailPanel title="Tenant admin credentials">
        <ResourceForm onSubmit={submit} footer={<Button type="submit" disabled={submitting}>{submitting ? "Signing in..." : "Sign in"}</Button>}>
          <FormField label="Identifier" value={identifier} onChange={(event) => setIdentifier(event.target.value)} required />
          <FormField label="Password" value={password} onChange={(event) => setPassword(event.target.value)} type="password" required />
        </ResourceForm>
      </DetailPanel>
    </div>
  );
}
