import { Button, DataTable, DetailPanel, EmptyState, FormField, PageHeader, ResourceForm, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";
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
    if (!selectedTenantId) return;
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
      <PageHeader title="Platform identities" description="Review tenant administrators and provision platform-visible identities." />
      {feedback && <Toast tone="success" message={feedback} />}
      <DetailPanel title="Tenant context">
        <select
          value={selectedTenantId}
          onChange={(event) => onSelectTenant(event.target.value)}
          style={{ border: "1px solid #bccbc5", borderRadius: "6px", font: "inherit", minHeight: "36px", minWidth: "280px", padding: "0 10px" }}
        >
          {tenants.map((tenant) => (
            <option key={tenant.id} value={tenant.id}>{tenant.name}</option>
          ))}
        </select>
      </DetailPanel>
      <DetailPanel title="Create identity">
        <ResourceForm onSubmit={submit} footer={<Button type="submit" disabled={!selectedTenantId}>Create identity</Button>}>
          <FormField label="Username" value={form.username} onChange={(event) => setForm({ ...form, username: event.target.value })} required />
          <FormField label="Email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} type="email" required />
          <FormField label="Temporary password" value={form.password} onChange={(event) => setForm({ ...form, password: event.target.value })} type="password" required />
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
        </ResourceForm>
      </DetailPanel>
      <DetailPanel title="Visible identities">
        <DataTable
          items={identities}
          getRowKey={(identity) => identity.id}
          empty={<EmptyState title="No identities" body="No identities are visible for the selected tenant." />}
          columns={[
            { key: "username", header: "Identity", render: (identity) => <><strong>{identity.username}</strong><div>{identity.email}</div></> },
            { key: "role", header: "Role", render: (identity) => identity.is_superuser ? "Superuser" : identity.is_admin ? "Admin" : "User" },
            { key: "status", header: "Status", render: (identity) => <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Inactive"}</StatusBadge> },
            { key: "password", header: "Password", render: (identity) => identity.must_change_password ? <StatusBadge tone="warning">Must change</StatusBadge> : <StatusBadge tone="success">Current</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
