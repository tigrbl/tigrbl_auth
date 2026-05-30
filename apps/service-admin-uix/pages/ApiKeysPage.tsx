import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ApiKeyRecord } from "../types";

export function ApiKeysPage({ apiKeys }: { apiKeys: ApiKeyRecord[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="API keys" description="Issue, inspect, and revoke scoped API keys for workload integrations." />
      <DetailPanel title="API key records">
        <DataTable
          items={apiKeys}
          getRowKey={(key) => key.id}
          empty={<EmptyState title="No API keys" body="No API key records are visible yet." />}
          columns={[
            { key: "name", header: "Name", render: (key) => key.name ?? key.id },
            { key: "service", header: "Service", render: (key) => key.service_id ?? "unknown" },
            { key: "scopes", header: "Scopes", render: (key) => key.scopes?.join(", ") || "None" },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
