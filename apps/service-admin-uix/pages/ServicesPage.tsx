import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ServiceIdentity } from "../types";

export function ServicesPage({ services }: { services: ServiceIdentity[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Service identities" description="Manage non-human service and workload principals." />
      <DetailPanel title="Visible services">
        <DataTable
          items={services}
          getRowKey={(service) => service.id}
          empty={<EmptyState title="No services" body="No service identities are visible for this service admin session." />}
          columns={[
            { key: "name", header: "Service", render: (service) => <><strong>{service.name ?? service.subject ?? service.id}</strong><div>{service.subject ?? service.id}</div></> },
            { key: "tenant", header: "Tenant", render: (service) => service.tenant_id ?? "unknown" },
            { key: "status", header: "Status", render: (service) => <StatusBadge tone={service.is_active === false ? "warning" : "success"}>{service.is_active === false ? "Inactive" : "Active"}</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
