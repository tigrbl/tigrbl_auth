import { DetailPanel, EmptyState, JsonViewer, PageHeader, SecretField, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ClientRegistration, DeveloperApplication } from "../types";

export function ClientCredentialsPage({ application, registration }: { application: DeveloperApplication | null; registration: ClientRegistration | null }) {
  const clientId = application?.client_id ?? registration?.client_id ?? null;
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Client credentials" description="Review client identifiers and planned credential rotation controls." />
      {clientId ? (
        <DetailPanel title="Selected client">
          <SecretField label="Client ID" value={clientId} />
          <p><StatusBadge tone="info">Secret rotation planned</StatusBadge></p>
          <JsonViewer value={{ client_id: clientId, credential_management: "planned" }} />
        </DetailPanel>
      ) : (
        <EmptyState title="No client selected" body="No client credential material is visible yet." />
      )}
    </div>
  );
}
