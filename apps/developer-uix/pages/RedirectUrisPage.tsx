import { DataTable, DetailPanel, EmptyState, PageHeader } from "@tigrbl-auth/uix-core";
import type { ClientRegistration } from "../types";

export function RedirectUrisPage({ registrations }: { registrations: ClientRegistration[] }) {
  const rows = registrations.flatMap((registration) => (registration.redirect_uris ?? []).map((uri) => ({ client: registration.client_name ?? registration.client_id ?? registration.id, uri })));
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Redirect URIs" description="Inspect callback URLs configured across developer-owned clients." />
      <DetailPanel title="Configured redirect URIs">
        <DataTable
          items={rows}
          getRowKey={(row) => `${row.client}:${row.uri}`}
          empty={<EmptyState title="No redirect URIs" body="No redirect URIs are visible in the current registration records." />}
          columns={[
            { key: "client", header: "Client", render: (row) => row.client },
            { key: "uri", header: "URI", render: (row) => <code>{row.uri}</code> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
