import { DataTable, DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AdminSession, Identity, Tenant } from "../types";

export function DashboardPage({ identities, session, tenants }: { identities: Identity[]; session: AdminSession | null; tenants: Tenant[] }) {
  const adminCount = identities.filter((identity) => identity.is_admin || identity.is_superuser).length;

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Platform dashboard" description="Operator view for tenant lifecycle, authority, and platform control-plane posture." />
      <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
        <Metric label="Visible tenants" value={tenants.length} />
        <Metric label="Selected identities" value={identities.length} />
        <Metric label="Administrators" value={adminCount} />
        <Metric label="Operator" value={session?.is_superuser ? "Superuser" : "Admin"} />
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

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <article style={{ background: "#ffffff", border: "1px solid #d7dfdb", borderRadius: "8px", padding: "14px" }}>
      <div style={{ color: "#60766e", fontSize: "0.82rem" }}>{label}</div>
      <strong style={{ display: "block", fontSize: "1.6rem", marginTop: "6px" }}>{value}</strong>
    </article>
  );
}
