import { Card, FormError, FormField, ResourceForm, SubmitButton } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";

export function LoginPage({ error, onLogin }: { error: string; onLogin: (identifier: string, password: string) => Promise<void> }) {
  const [identifier, setIdentifier] = useState("admin");
  const [password, setPassword] = useState("AdminPass123!");
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
    <Card tone="hero" style={{ maxWidth: "520px", width: "100%" }}>
      {(localError || error) && <FormError>{localError || error}</FormError>}
      <ResourceForm onSubmit={submit} footer={<SubmitButton loading={submitting} loadingLabel="Signing in...">Sign in</SubmitButton>}>
        <FormField label="Identifier" value={identifier} onChange={(event) => setIdentifier(event.target.value)} required />
        <FormField label="Password" value={password} onChange={(event) => setPassword(event.target.value)} type="password" required />
      </ResourceForm>
    </Card>
  );
}
