import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { Identity, Tenant } from "../types";

export function TenantDetailPage({
  identities,
  onSelectTenant,
  selectedTenant,
  selectedTenantId,
  tenants
}: {
  identities: Identity[];
  onSelectTenant: (tenantId: string) => void;
  selectedTenant: Tenant | null;
  selectedTenantId: string;
  tenants: Tenant[];
}) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant detail" description="Inspect tenant metadata, authority context, and tenant-scoped administrators." />
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
      {selectedTenant ? (
        <DetailPanel title={selectedTenant.name}>
          <dl style={{ display: "grid", gap: "10px", gridTemplateColumns: "160px 1fr" }}>
            <dt>Slug</dt><dd>{selectedTenant.slug}</dd>
            <dt>Contact</dt><dd>{selectedTenant.email}</dd>
            <dt>ID</dt><dd><code>{selectedTenant.id}</code></dd>
            <dt>Status</dt><dd><StatusBadge tone="success">Active</StatusBadge></dd>
          </dl>
        </DetailPanel>
      ) : (
        <EmptyState title="No tenant selected" body="Select a tenant to inspect its platform detail." />
      )}
      <DetailPanel title="Tenant administrators">
        <DataTable
          items={identities.filter((identity) => identity.is_admin || identity.is_superuser)}
          getRowKey={(identity) => identity.id}
          empty={<EmptyState title="No administrators" body="No tenant administrators are visible for this tenant." />}
          columns={[
            { key: "identity", header: "Identity", render: (identity) => <><strong>{identity.username}</strong><div>{identity.email}</div></> },
            { key: "authority", header: "Authority", render: (identity) => identity.is_superuser ? "Superuser" : "Admin" },
            { key: "status", header: "Status", render: (identity) => <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Inactive"}</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
