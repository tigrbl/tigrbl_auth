import { DataTable, DetailPanel, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AdminSession, Identity, Tenant } from "../types";

export function DashboardPage({ identities, session, tenants }: { identities: Identity[]; session: AdminSession | null; tenants: Tenant[] }) {
  const adminCount = identities.filter((identity) => identity.is_admin || identity.is_superuser).length;

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Platform dashboard" description="Operator view for tenant lifecycle, authority, and platform control-plane posture." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Visible tenants" value={tenants.length} />
        <MetricCard label="Selected identities" value={identities.length} />
        <MetricCard label="Administrators" value={adminCount} />
        <MetricCard label="Operator" value={session?.is_superuser ? "Superuser" : "Admin"} />
      </div>
      <DetailPanel title="Tenant summary">
        <DataTable
          items={tenants.slice(0, 6)}
          getRowKey={(tenant) => tenant.id}
          columns={[
            { key: "name", header: "Tenant", render: (tenant) => <><strong>{tenant.name}</strong><div>{tenant.slug}</div></> },
            { key: "email", header: "Contact", render: (tenant) => tenant.email },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Active</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
