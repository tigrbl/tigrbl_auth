import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ServiceKey } from "../types";

export function RotationEventsPage({ serviceKeys }: { serviceKeys: ServiceKey[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Rotation events" description="Review service key lifecycle posture. Dedicated rotation event resources can be wired here when exposed." />
      <DetailPanel title="Key rotation posture">
        <DataTable
          items={serviceKeys}
          getRowKey={(key) => key.id}
          empty={<EmptyState title="No rotation posture" body="No service keys are visible to infer rotation posture." />}
          columns={[
            { key: "key", header: "Key", render: (key) => key.kid ?? key.id },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> },
            { key: "created", header: "Created", render: (key) => key.created_at ?? "unknown" }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
