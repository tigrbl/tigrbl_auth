import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantIdentity } from "../types";

export function GroupsRolesPage({ identities }: { identities: TenantIdentity[] }) {
  const rows = identities.flatMap((identity) => (identity.roles ?? []).map((role) => ({ identity, role })));

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Groups and roles" description="Review tenant-local role assignments derived from visible identities." />
      <DetailPanel title="Role assignments">
        <DataTable
          items={rows}
          getRowKey={(row) => `${row.identity.id}:${row.role}`}
          empty={<EmptyState title="No role assignments" body="No explicit roles are visible for tenant identities." />}
          columns={[
            { key: "identity", header: "Identity", render: (row) => row.identity.username ?? row.identity.id },
            { key: "role", header: "Role", render: (row) => <StatusBadge tone="info">{row.role}</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
