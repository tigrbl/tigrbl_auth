import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ClientRegistration, DeveloperApplication } from "../types";

export function ApplicationsPage({ applications, registrations }: { applications: DeveloperApplication[]; registrations: ClientRegistration[] }) {
  const rows = applications.length ? applications : registrations.map((registration) => ({
    id: registration.id,
    client_id: registration.client_id,
    name: registration.client_name,
    redirect_uris: registration.redirect_uris
  }));

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Applications" description="Register and inspect OAuth/OIDC applications in the current tenant developer context." />
      <DetailPanel title="Developer applications">
        <DataTable
          items={rows}
          getRowKey={(app) => app.id}
          empty={<EmptyState title="No applications" body="No developer applications are visible yet." />}
          columns={[
            { key: "name", header: "Application", render: (app) => <><strong>{app.name ?? app.client_id ?? app.id}</strong><div>{app.client_id ?? app.id}</div></> },
            { key: "redirects", header: "Redirect URIs", render: (app) => app.redirect_uris?.length ?? 0 },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Visible</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
