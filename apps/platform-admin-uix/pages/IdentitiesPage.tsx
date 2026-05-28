import { useState } from "react";
import type { FormEvent } from "react";
import { Button, Field, Notice, Panel } from "../components/UI";
import type { CreateIdentityInput, Identity, Tenant } from "../types";

export function IdentitiesPage({
  identities,
  onCreate,
  onSelectTenant,
  selectedTenantId,
  tenants
}: {
  identities: Identity[];
  onCreate: (payload: CreateIdentityInput) => Promise<void>;
  onSelectTenant: (tenantId: string) => void;
  selectedTenantId: string;
  tenants: Tenant[];
}) {
  const [form, setForm] = useState({
    username: "",
    email: "",
    password: "ChangeMe123!",
    is_admin: true,
    is_superuser: false,
    must_change_password: true
  });
  const [feedback, setFeedback] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!selectedTenantId) {
      return;
    }
    await onCreate({
      tenant_id: selectedTenantId,
      username: form.username.trim(),
      email: form.email.trim().toLowerCase(),
      password: form.password,
      is_admin: form.is_admin,
      is_superuser: form.is_superuser,
      must_change_password: form.must_change_password
    });
    setFeedback("Identity provisioned.");
    setForm({ ...form, username: "", email: "", password: "ChangeMe123!" });
  }

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <div>
        <h1 style={{ fontSize: "1.8rem", margin: "0 0 8px" }}>Platform identities</h1>
        <p style={{ color: "#526960", margin: 0 }}>Review tenant administrators and provision platform-visible identities.</p>
      </div>
      {feedback && <Notice tone="success">{feedback}</Notice>}
      <Panel title="Tenant context">
        <select
          value={selectedTenantId}
          onChange={(event) => onSelectTenant(event.target.value)}
          style={{ border: "1px solid #bccbc5", borderRadius: "6px", font: "inherit", minHeight: "36px", minWidth: "280px", padding: "0 10px" }}
        >
          {tenants.map((tenant) => (
            <option key={tenant.id} value={tenant.id}>{tenant.name}</option>
          ))}
        </select>
      </Panel>
      <Panel title="Create identity">
        <form onSubmit={submit} style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(3, minmax(0, 1fr))" }}>
          <Field label="Username" value={form.username} onChange={(username) => setForm({ ...form, username })} required />
          <Field label="Email" value={form.email} onChange={(email) => setForm({ ...form, email })} type="email" required />
          <Field label="Temporary password" value={form.password} onChange={(password) => setForm({ ...form, password })} type="password" required />
          <label style={{ alignItems: "center", display: "flex", gap: "8px" }}>
            <input type="checkbox" checked={form.is_admin} onChange={(event) => setForm({ ...form, is_admin: event.target.checked })} />
            Admin
          </label>
          <label style={{ alignItems: "center", display: "flex", gap: "8px" }}>
            <input type="checkbox" checked={form.is_superuser} onChange={(event) => setForm({ ...form, is_superuser: event.target.checked })} />
            Superuser
          </label>
          <label style={{ alignItems: "center", display: "flex", gap: "8px" }}>
            <input type="checkbox" checked={form.must_change_password} onChange={(event) => setForm({ ...form, must_change_password: event.target.checked })} />
            Force password change
          </label>
          <div>
            <Button type="submit" disabled={!selectedTenantId}>Create identity</Button>
          </div>
        </form>
      </Panel>
      <Panel title="Visible identities">
        <div style={{ display: "grid", gap: "10px" }}>
          {identities.map((identity) => (
            <article key={identity.id} style={{ background: "#ffffff", border: "1px solid #d7dfdb", borderRadius: "8px", padding: "12px" }}>
              <strong>{identity.username}</strong>
              <div style={{ color: "#60766e", fontSize: "0.86rem" }}>{identity.email}</div>
              <div style={{ color: "#425a52", fontSize: "0.82rem", marginTop: "6px" }}>
                {identity.is_superuser ? "Superuser" : identity.is_admin ? "Admin" : "User"} · {identity.is_active ? "Active" : "Inactive"}
              </div>
            </article>
          ))}
          {identities.length === 0 && <Notice tone="info">No identities are visible for the selected tenant.</Notice>}
        </div>
      </Panel>
    </div>
  );
}
