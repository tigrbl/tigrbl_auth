import { Button, DataTable, DetailPanel, EmptyState, FormField, PageHeader, ResourceForm, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";
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
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant lifecycle" description="Create tenants and select a tenant context for platform administration." />
      {feedback && <Toast tone="success" message={feedback} />}
      <DetailPanel title="Create tenant">
        <ResourceForm onSubmit={submit} footer={<Button type="submit">Create tenant</Button>}>
          <FormField label="Slug" value={form.slug} onChange={(event) => setForm({ ...form, slug: event.target.value })} required />
          <FormField label="Name" value={form.name} onChange={(event) => setForm({ ...form, name: event.target.value })} required />
          <FormField label="Contact email" value={form.email} onChange={(event) => setForm({ ...form, email: event.target.value })} type="email" required />
        </ResourceForm>
      </DetailPanel>
      <DetailPanel title="Tenants">
        <DataTable
          items={tenants}
          getRowKey={(tenant) => tenant.id}
          empty={<EmptyState title="No tenants" body="No tenants are visible for this platform session." />}
          columns={[
            {
              key: "name",
              header: "Tenant",
              render: (tenant) => (
                <button type="button" onClick={() => onSelect(tenant.id)} style={{ background: "transparent", border: 0, cursor: "pointer", font: "inherit", padding: 0, textAlign: "left" }}>
                  <strong>{tenant.name}</strong>
                  <div>{tenant.slug} / {tenant.email}</div>
                </button>
              )
            },
            { key: "status", header: "Context", render: (tenant) => selectedTenantId === tenant.id ? <StatusBadge tone="success">Selected</StatusBadge> : <StatusBadge>Available</StatusBadge> },
            { key: "id", header: "ID", render: (tenant) => <code>{tenant.id}</code> },
            { key: "actions", header: "Actions", render: (tenant) => <Button variant="danger" onClick={() => void onDelete(tenant.id)}>Delete</Button> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
