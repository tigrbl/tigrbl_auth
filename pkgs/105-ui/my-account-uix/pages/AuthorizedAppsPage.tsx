import { ConfirmDialog, DetailPanel, InlineMutationResult, MetricCard, PageHeader, ResourceTable, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";
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
  const [mutationError, setMutationError] = useState<string | null>(null);
  const [revokeApp, setRevokeApp] = useState<AuthorizedApp | null>(null);
  const [revokeConsent, setRevokeConsent] = useState<Consent | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function runMutation(action: () => Promise<void>, message: string) {
    setMutationError(null);
    setSuccess(null);
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setMutationError(nextError instanceof Error ? nextError.message : "Authorization update failed.");
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Authorized apps" description="Review applications and consent grants authorized for your account." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Applications" value={apps.length} description="Clients authorized by this account" />
        <MetricCard label="Consent grants" value={consents.length} description="Scope grants visible to the subject" />
        <MetricCard label="Loading state" value={loading ? "Refreshing" : "Current"} description="Authorization data freshness" />
      </div>
      {error ? <Toast tone="danger" message={error} /> : null}
      <InlineMutationResult error={mutationError} success={success} />
      <DetailPanel title="Authorized applications">
        <ResourceTable
          items={apps}
          getRowKey={(app) => app.client_id}
          emptyTitle="No authorized applications"
          emptyBody="No applications are currently authorized."
          columns={[
            { key: "client", header: "Client", render: (app) => <code>{app.client_id}</code> },
            { key: "scope", header: "Scope", render: (app) => app.scope },
            { key: "state", header: "State", render: (app) => <StatusBadge tone={app.consent_state === "revoked" ? "warning" : "success"}>{app.consent_state}</StatusBadge> }
          ]}
          actions={[{ label: "Revoke app", onClick: setRevokeApp, tone: "danger" }]}
        />
      </DetailPanel>
      <DetailPanel title="Consent grants">
        <ResourceTable
          items={consents}
          getRowKey={(consent) => consent.id}
          emptyTitle="No consent grants"
          emptyBody="No consent grants are currently visible."
          columns={[
            { key: "id", header: "Grant", render: (consent) => <code>{consent.id}</code> },
            { key: "client", header: "Client", render: (consent) => <code>{consent.client_id}</code> },
            { key: "scope", header: "Scope", render: (consent) => consent.scope },
            { key: "state", header: "State", render: (consent) => <StatusBadge tone={consent.state === "revoked" ? "warning" : "success"}>{consent.state}</StatusBadge> }
          ]}
          actions={[{ label: "Revoke consent", onClick: setRevokeConsent, tone: "danger" }]}
        />
      </DetailPanel>
      <ConfirmDialog
        open={Boolean(revokeApp)}
        title="Revoke authorized app"
        body={`Revoke application ${revokeApp?.client_id ?? ""}?`}
        confirmLabel="Revoke app"
        onCancel={() => setRevokeApp(null)}
        onConfirm={() => {
          if (!revokeApp) return;
          const clientId = revokeApp.client_id;
          setRevokeApp(null);
          void runMutation(() => onRevokeApp(clientId), "Authorized app revoked.");
        }}
      />
      <ConfirmDialog
        open={Boolean(revokeConsent)}
        title="Revoke consent grant"
        body={`Revoke consent ${revokeConsent?.id ?? ""}?`}
        confirmLabel="Revoke consent"
        onCancel={() => setRevokeConsent(null)}
        onConfirm={() => {
          if (!revokeConsent) return;
          const consentId = revokeConsent.id;
          setRevokeConsent(null);
          void runMutation(() => onRevokeConsent(consentId), "Consent revoked.");
        }}
      />
    </div>
  );
}
