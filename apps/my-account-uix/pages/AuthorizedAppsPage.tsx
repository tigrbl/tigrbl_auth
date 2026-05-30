import { Button, DataTable, DetailPanel, EmptyState, MetricCard, PageHeader, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import type { AuthorizedApp, Consent } from "../types";

export function AuthorizedAppsPage({
  apps,
  consents,
  error,
  loading,
  onRevokeApp,
  onRevokeConsent
}: {
  apps: AuthorizedApp[];
  consents: Consent[];
  error?: string | null;
  loading?: boolean;
  onRevokeApp: (clientId: string) => Promise<void>;
  onRevokeConsent: (consentId: string) => Promise<void>;
}) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Authorized apps" description="Review applications and consent grants authorized for your account." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Applications" value={apps.length} description="Clients authorized by this account" />
        <MetricCard label="Consent grants" value={consents.length} description="Scope grants visible to the subject" />
        <MetricCard label="Loading state" value={loading ? "Refreshing" : "Current"} description="Authorization data freshness" />
      </div>
      {error ? <Toast tone="danger" message={error} /> : null}
      <DetailPanel title="Authorized applications">
        <DataTable
          items={apps}
          getRowKey={(app) => app.client_id}
          empty={<EmptyState title="No authorized applications" body="No applications are currently authorized." />}
          columns={[
            { key: "client", header: "Client", render: (app) => <code>{app.client_id}</code> },
            { key: "scope", header: "Scope", render: (app) => app.scope },
            { key: "state", header: "State", render: (app) => <StatusBadge tone={app.consent_state === "revoked" ? "warning" : "success"}>{app.consent_state}</StatusBadge> },
            { key: "actions", header: "Actions", render: (app) => <Button variant="danger" onClick={() => void onRevokeApp(app.client_id)}>Revoke</Button> }
          ]}
        />
      </DetailPanel>
      <DetailPanel title="Consent grants">
        <DataTable
          items={consents}
          getRowKey={(consent) => consent.id}
          empty={<EmptyState title="No consent grants" body="No consent grants are currently visible." />}
          columns={[
            { key: "client", header: "Client", render: (consent) => <code>{consent.client_id}</code> },
            { key: "scope", header: "Scope", render: (consent) => consent.scope },
            { key: "state", header: "State", render: (consent) => <StatusBadge tone={consent.state === "revoked" ? "warning" : "success"}>{consent.state}</StatusBadge> },
            { key: "actions", header: "Actions", render: (consent) => <Button variant="danger" onClick={() => void onRevokeConsent(consent.id)}>Revoke</Button> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
