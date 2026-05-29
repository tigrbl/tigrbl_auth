import { DetailPanel, EmptyState, JsonViewer, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ClientRegistration, DeveloperApplication } from "../types";

export function ApplicationDetailPage({ application, registration }: { application: DeveloperApplication | null; registration: ClientRegistration | null }) {
  const record = application ?? registration;
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Application detail" description="Inspect the selected application/client record." />
      {record ? (
        <DetailPanel title={application?.name ?? registration?.client_name ?? record.id}>
          <StatusBadge tone="info">Read-only</StatusBadge>
          <JsonViewer value={record} />
        </DetailPanel>
      ) : (
        <EmptyState title="No application selected" body="Create or load an application to inspect details." />
      )}
    </div>
  );
}
