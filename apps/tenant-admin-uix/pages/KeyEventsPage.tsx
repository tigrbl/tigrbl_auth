import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { KeyRotationEvent } from "../types";

export function KeyEventsPage({ keyEvents }: { keyEvents: KeyRotationEvent[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant key events" description="Review tenant key rotation event records without platform-wide key authority." />
      <DetailPanel title="Key rotation events">
        <DataTable
          items={keyEvents}
          getRowKey={(event) => event.id}
          empty={<EmptyState title="No key events" body="No key rotation events are visible for this tenant." />}
          columns={[
            { key: "id", header: "Event", render: (event) => <code>{event.id}</code> },
            { key: "status", header: "Status", render: (event) => <StatusBadge tone="info">{event.status ?? "Recorded"}</StatusBadge> },
            { key: "created", header: "Created", render: (event) => event.created_at ?? "unknown" }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
