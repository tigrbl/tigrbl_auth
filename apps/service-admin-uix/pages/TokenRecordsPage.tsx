import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TokenRecord } from "../types";

export function TokenRecordsPage({ tokenRecords }: { tokenRecords: TokenRecord[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Token records" description="Inspect machine-token lifecycle records visible to service administrators." />
      <DetailPanel title="Tokens">
        <DataTable
          items={tokenRecords}
          getRowKey={(token) => token.id}
          empty={<EmptyState title="No token records" body="No token records are visible yet." />}
          columns={[
            { key: "subject", header: "Subject", render: (token) => token.subject ?? "unknown" },
            { key: "client", header: "Client", render: (token) => token.client_id ?? "unknown" },
            { key: "scopes", header: "Scopes", render: (token) => token.scopes?.join(", ") || "None" },
            { key: "status", header: "Status", render: (token) => <StatusBadge tone="info">{token.status ?? "Recorded"}</StatusBadge> },
            { key: "expires", header: "Expires", render: (token) => token.expires_at ?? "unknown" }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
