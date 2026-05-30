import { DataTable, DetailPanel, EmptyState, JsonViewer, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ApiKeyRecord, ServiceIdentity, ServiceKey } from "../types";

export function ServiceDetailPage({ apiKeys, service, serviceKeys }: { apiKeys: ApiKeyRecord[]; service: ServiceIdentity | null; serviceKeys: ServiceKey[] }) {
  if (!service) {
    return <EmptyState title="No service selected" body="No service identity is available to inspect yet." />;
  }

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Service detail" description="Inspect the selected workload principal and related credentials." />
      <DetailPanel title={service.name ?? service.subject ?? service.id}>
        <StatusBadge tone={service.is_active === false ? "warning" : "success"}>{service.is_active === false ? "Inactive" : "Active"}</StatusBadge>
        <JsonViewer value={service} />
      </DetailPanel>
      <DetailPanel title="Attached keys">
        <DataTable
          items={serviceKeys.filter((key) => !key.service_id || key.service_id === service.id)}
          getRowKey={(key) => key.id}
          empty={<EmptyState title="No keys" body="No keys are visible for this service." />}
          columns={[
            { key: "kid", header: "Key", render: (key) => key.kid ?? key.id },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> }
          ]}
        />
      </DetailPanel>
      <DetailPanel title="API keys">
        <DataTable
          items={apiKeys.filter((key) => !key.service_id || key.service_id === service.id)}
          getRowKey={(key) => key.id}
          empty={<EmptyState title="No API keys" body="No API keys are visible for this service." />}
          columns={[
            { key: "name", header: "Name", render: (key) => key.name ?? key.id },
            { key: "scopes", header: "Scopes", render: (key) => key.scopes?.join(", ") || "None" }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
