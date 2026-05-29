import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantClient } from "../types";

export function ClientsPage({ clients }: { clients: TenantClient[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant clients" description="Inspect tenant-local OAuth/OIDC clients and client registration metadata." />
      <DetailPanel title="Client applications">
        <DataTable
          items={clients}
          getRowKey={(client) => client.id}
          empty={<EmptyState title="No clients" body="No tenant clients are visible for this session." />}
          columns={[
            { key: "client", header: "Client", render: (client) => <><strong>{client.name ?? client.client_id ?? client.id}</strong><div>{client.client_id ?? client.id}</div></> },
            { key: "redirects", header: "Redirect URIs", render: (client) => client.redirect_uris?.length ?? 0 },
            { key: "grants", header: "Grant types", render: (client) => client.grant_types?.join(", ") || "Default" },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Visible</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
