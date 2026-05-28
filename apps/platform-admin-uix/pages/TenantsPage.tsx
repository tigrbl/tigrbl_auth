import { useState } from "react";
import type { FormEvent } from "react";
import { Button, Field, Notice, Panel } from "../components/UI";
import type { CreateTenantInput, Tenant } from "../types";

export function TenantsPage({
  selectedTenantId,
  tenants,
  onCreate,
  onDelete,
  onSelect
}: {
  selectedTenantId: string;
  tenants: Tenant[];
  onCreate: (payload: CreateTenantInput) => Promise<void>;
  onDelete: (tenantId: string) => Promise<void>;
  onSelect: (tenantId: string) => void;
}) {
  const [form, setForm] = useState<CreateTenantInput>({ slug: "", name: "", email: "" });
  const [feedback, setFeedback] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    await onCreate({
      slug: form.slug.trim().toLowerCase(),
      name: form.name.trim(),
      email: form.email.trim().toLowerCase()
    });
    setForm({ slug: "", name: "", email: "" });
    setFeedback("Tenant provisioned.");
  }

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <div>
        <h1 style={{ fontSize: "1.8rem", margin: "0 0 8px" }}>Tenant lifecycle</h1>
        <p style={{ color: "#526960", margin: 0 }}>Create tenants and select a tenant context for platform administration.</p>
      </div>
      {feedback && <Notice tone="success">{feedback}</Notice>}
      <Panel title="Create tenant">
        <form onSubmit={submit} style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(3, minmax(0, 1fr))" }}>
          <Field label="Slug" value={form.slug} onChange={(slug) => setForm({ ...form, slug })} required />
          <Field label="Name" value={form.name} onChange={(name) => setForm({ ...form, name })} required />
          <Field label="Contact email" value={form.email} onChange={(email) => setForm({ ...form, email })} type="email" required />
          <div style={{ alignSelf: "end" }}>
            <Button type="submit">Create tenant</Button>
          </div>
        </form>
      </Panel>
      <Panel title="Tenants">
        <div style={{ display: "grid", gap: "10px" }}>
          {tenants.map((tenant) => (
            <article
              key={tenant.id}
              style={{
                alignItems: "center",
                background: selectedTenantId === tenant.id ? "#eef6f2" : "#ffffff",
                border: "1px solid #d7dfdb",
                borderRadius: "8px",
                display: "grid",
                gap: "12px",
                gridTemplateColumns: "1fr auto auto",
                padding: "12px"
              }}
            >
              <button
                type="button"
                onClick={() => onSelect(tenant.id)}
                style={{ background: "transparent", border: 0, color: "#17211d", cursor: "pointer", font: "inherit", padding: 0, textAlign: "left" }}
              >
                <strong>{tenant.name}</strong>
                <div style={{ color: "#60766e", fontSize: "0.86rem" }}>{tenant.slug} · {tenant.email}</div>
              </button>
              <code style={{ color: "#526960", fontSize: "0.78rem" }}>{tenant.id}</code>
              <Button variant="danger" onClick={() => void onDelete(tenant.id)}>Delete</Button>
            </article>
          ))}
          {tenants.length === 0 && <Notice tone="info">No tenants are visible for this platform session.</Notice>}
        </div>
      </Panel>
    </div>
  );
}
