import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { Identity, Tenant } from "../types";

export function AuthorityPage({ identities, selectedTenant, tenants }: { identities: Identity[]; selectedTenant: Tenant | null; tenants: Tenant[] }) {
  const platformOperators = identities.filter((identity) => identity.is_superuser);
  const tenantAdmins = identities.filter((identity) => identity.is_admin && !identity.is_superuser);

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Authority" description="Review platform authority assignment and tenant administration posture." />
      <DetailPanel title="Authority scope">
        <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(3, minmax(0, 1fr))" }}>
          <Metric label="Selected tenant" value={selectedTenant?.name ?? "None"} />
          <Metric label="Platform operators" value={platformOperators.length} />
          <Metric label="Tenant administrators" value={tenantAdmins.length} />
        </div>
      </DetailPanel>
      <DetailPanel title="Authority assignments">
        <DataTable
          items={identities}
          getRowKey={(identity) => identity.id}
          empty={<EmptyState title="No authority assignments" body="Select a tenant with visible identities to review authority." />}
          columns={[
            { key: "identity", header: "Identity", render: (identity) => <><strong>{identity.username}</strong><div>{identity.email}</div></> },
            { key: "role", header: "Role", render: (identity) => identity.is_superuser ? <StatusBadge tone="danger">Superuser</StatusBadge> : identity.is_admin ? <StatusBadge tone="info">Admin</StatusBadge> : <StatusBadge>User</StatusBadge> },
            { key: "tenant", header: "Tenant", render: (identity) => tenants.find((tenant) => tenant.id === identity.tenant_id)?.name ?? identity.tenant_id }
          ]}
        />
      </DetailPanel>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <article style={{ background: "#ffffff", border: "1px solid #d7dfdb", borderRadius: "8px", padding: "14px" }}>
      <div style={{ color: "#60766e", fontSize: "0.82rem" }}>{label}</div>
      <strong style={{ display: "block", fontSize: "1.2rem", marginTop: "6px" }}>{value}</strong>
    </article>
  );
}
