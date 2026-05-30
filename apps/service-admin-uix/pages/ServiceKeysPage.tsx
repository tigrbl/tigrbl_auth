import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ServiceKey } from "../types";

export function ServiceKeysPage({ serviceKeys }: { serviceKeys: ServiceKey[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Service keys" description="Review service key material lifecycle and rotation posture." />
      <DetailPanel title="Keys">
        <DataTable
          items={serviceKeys}
          getRowKey={(key) => key.id}
          empty={<EmptyState title="No service keys" body="No service keys are visible yet." />}
          columns={[
            { key: "kid", header: "KID", render: (key) => <code>{key.kid ?? key.id}</code> },
            { key: "service", header: "Service", render: (key) => key.service_id ?? "unknown" },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> },
            { key: "created", header: "Created", render: (key) => key.created_at ?? "unknown" }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
