import { DataTable, DetailPanel, EmptyState, PageHeader } from "@tigrbl-auth/uix-core";
import type { ClientRegistration } from "../types";

export function ClientMetadataPage({ registrations }: { registrations: ClientRegistration[] }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Client metadata" description="Review registered client metadata, auth method, and redirect configuration." />
      <DetailPanel title="Registration records">
        <DataTable
          items={registrations}
          getRowKey={(registration) => registration.id}
          empty={<EmptyState title="No client metadata" body="No client registration records are visible yet." />}
          columns={[
            { key: "name", header: "Client", render: (registration) => registration.client_name ?? registration.client_id ?? registration.id },
            { key: "auth", header: "Auth method", render: (registration) => registration.token_endpoint_auth_method ?? "default" },
            { key: "redirects", header: "Redirect URIs", render: (registration) => registration.redirect_uris?.length ?? 0 }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
