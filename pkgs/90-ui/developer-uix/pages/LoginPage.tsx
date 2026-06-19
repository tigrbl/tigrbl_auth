import { Card, FormError, FormField, ResourceForm, SubmitButton } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";

export function LoginPage({ error, onLogin }: { error: string; onLogin: (username: string, email: string, tenantId: string) => Promise<void> }) {
  const [username, setUsername] = useState("developer");
  const [email, setEmail] = useState("developer@example.test");
  const [tenantId, setTenantId] = useState("local-tenant");
  const [localError, setLocalError] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setLocalError("");
    try {
      await onLogin(username, email, tenantId);
    } catch (nextError) {
      setLocalError(nextError instanceof Error ? nextError.message : "Unable to establish developer session.");
    }
  }

  return (
    <Card tone="hero" style={{ maxWidth: "560px", width: "100%" }}>
      {(localError || error) && <FormError>{localError || error}</FormError>}
      <ResourceForm onSubmit={submit} footer={<SubmitButton>Continue</SubmitButton>}>
        <FormField label="Username" value={username} onChange={(event) => setUsername(event.target.value)} required />
        <FormField label="Email" value={email} onChange={(event) => setEmail(event.target.value)} type="email" required />
        <FormField label="Tenant ID" value={tenantId} onChange={(event) => setTenantId(event.target.value)} required />
      </ResourceForm>
    </Card>
  );
}
