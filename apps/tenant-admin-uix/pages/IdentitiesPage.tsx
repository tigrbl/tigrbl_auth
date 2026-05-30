import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantIdentity } from "../types";

export function IdentitiesPage({ identities }: { identities: TenantIdentity[] }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant identities" description="Manage tenant users, tenant administrators, activation state, and password posture." />
      <DetailPanel title="Visible identities">
        <DataTable
          items={identities}
          getRowKey={(identity) => identity.id}
          empty={<EmptyState title="No identities" body="No identities are visible for this tenant admin session." />}
          columns={[
            { key: "identity", header: "Identity", render: (identity) => <><strong>{identity.username ?? identity.id}</strong><div>{identity.email ?? "No email"}</div></> },
            { key: "role", header: "Role", render: (identity) => identity.is_superuser ? "Superuser" : identity.is_admin ? "Admin" : "User" },
            { key: "status", header: "Status", render: (identity) => <StatusBadge tone={identity.is_active === false ? "warning" : "success"}>{identity.is_active === false ? "Inactive" : "Active"}</StatusBadge> },
            { key: "password", header: "Password", render: (identity) => identity.must_change_password ? <StatusBadge tone="warning">Must change</StatusBadge> : <StatusBadge>Normal</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
