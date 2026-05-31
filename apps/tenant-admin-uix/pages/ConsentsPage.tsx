import {
  ConfirmDialog,
  DetailPanel,
  InlineMutationResult,
  PageHeader,
  ResourceTable,
  StatusBadge
} from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { TenantConsent } from "../types";

export function ConsentsPage({
  consents,
  onRevoke
}: {
  consents: TenantConsent[];
  onRevoke: (consentId: string) => Promise<void>;
}) {
  const [error, setError] = useState("");
  const [revokeConsent, setRevokeConsent] = useState<TenantConsent | null>(null);
  const [success, setSuccess] = useState("");

  async function runRevoke(consentId: string) {
    setError("");
    setSuccess("");
    try {
      await onRevoke(consentId);
      setSuccess("Consent revoked.");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Consent revoke failed.");
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant consents" description="Review and revoke user consent grants visible to tenant administrators." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Consent records">
        <ResourceTable
          items={consents}
          getRowKey={(consent) => consent.id}
          emptyTitle="No consents"
          emptyBody="No consent records are visible for this tenant session."
          columns={[
            { key: "client", header: "Client", render: (consent) => consent.client_id ?? "unknown" },
            { key: "user", header: "User", render: (consent) => consent.user_id ?? "unknown" },
            { key: "scopes", header: "Scopes", render: (consent) => consent.scopes?.join(", ") || "None" },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Granted</StatusBadge> }
          ]}
          actions={[{ label: "Revoke", onClick: setRevokeConsent, tone: "danger" }]}
        />
      </DetailPanel>

      <ConfirmDialog
        open={Boolean(revokeConsent)}
        title="Revoke consent"
        body={`Revoke consent ${revokeConsent?.id ?? ""}?`}
        confirmLabel="Revoke consent"
        onCancel={() => setRevokeConsent(null)}
        onConfirm={() => {
          if (!revokeConsent) return;
          const consentId = revokeConsent.id;
          setRevokeConsent(null);
          void runRevoke(consentId);
        }}
      />
    </div>
  );
}
