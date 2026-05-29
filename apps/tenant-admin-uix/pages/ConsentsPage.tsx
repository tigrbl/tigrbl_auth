import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantConsent } from "../types";

export function ConsentsPage({ consents }: { consents: TenantConsent[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant consents" description="Review user consent records visible to tenant administrators." />
      <DetailPanel title="Consent records">
        <DataTable
          items={consents}
          getRowKey={(consent) => consent.id}
          empty={<EmptyState title="No consents" body="No consent records are visible for this tenant session." />}
          columns={[
            { key: "client", header: "Client", render: (consent) => consent.client_id ?? "unknown" },
            { key: "user", header: "User", render: (consent) => consent.user_id ?? "unknown" },
            { key: "scopes", header: "Scopes", render: (consent) => consent.scopes?.join(", ") || "None" },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Granted</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
