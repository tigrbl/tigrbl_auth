import { useState } from "react";
import type { FormEvent } from "react";
import { Button, Field, Notice, Panel } from "../components/UI";

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
      <div>
        <h1 style={{ fontSize: "2rem", margin: "0 0 8px" }}>Platform operator sign in</h1>
        <p style={{ color: "#526960", margin: 0 }}>Use an administrator session to manage tenant lifecycle and platform authority.</p>
      </div>
      {(localError || error) && <Notice tone="error">{localError || error}</Notice>}
      <Panel title="Admin credentials">
        <form onSubmit={submit} style={{ display: "grid", gap: "12px" }}>
          <Field label="Identifier" value={identifier} onChange={setIdentifier} required />
          <Field label="Password" value={password} onChange={setPassword} type="password" required />
          <div>
            <Button type="submit" disabled={submitting}>{submitting ? "Signing in..." : "Sign in"}</Button>
          </div>
        </form>
      </Panel>
    </div>
  );
}
