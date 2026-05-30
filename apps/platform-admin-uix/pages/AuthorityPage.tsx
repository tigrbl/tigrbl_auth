import { DataTable, DetailPanel, EmptyState, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { Identity, Tenant } from "../types";

export function AuthorityPage({ identities, selectedTenant, tenants }: { identities: Identity[]; selectedTenant: Tenant | null; tenants: Tenant[] }) {
  const platformOperators = identities.filter((identity) => identity.is_superuser);
  const tenantAdmins = identities.filter((identity) => identity.is_admin && !identity.is_superuser);

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Authority" description="Review platform authority assignment and tenant administration posture." />
      <DetailPanel title="Authority scope">
        <div className="tigrbl-metric-grid">
          <MetricCard label="Selected tenant" value={selectedTenant?.name ?? "None"} />
          <MetricCard label="Platform operators" value={platformOperators.length} />
          <MetricCard label="Tenant administrators" value={tenantAdmins.length} />
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
