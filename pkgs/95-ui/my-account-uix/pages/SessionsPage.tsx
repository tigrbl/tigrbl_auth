import { ConfirmDialog, DetailPanel, InlineMutationResult, MetricCard, PageHeader, ResourceTable, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { AccountSession } from "../types";

export function SessionsPage({
  sessions,
  error,
  loading,
  onRevoke
}: {
  sessions: AccountSession[];
  error?: string | null;
  loading?: boolean;
  onRevoke: (sessionId: string) => Promise<void>;
}) {
  const [mutationError, setMutationError] = useState<string | null>(null);
  const [revokeSession, setRevokeSession] = useState<AccountSession | null>(null);
  const [success, setSuccess] = useState<string | null>(null);

  async function runRevoke(sessionId: string) {
    setMutationError(null);
    setSuccess(null);
    try {
      await onRevoke(sessionId);
      setSuccess("Session revoked.");
    } catch (nextError) {
      setMutationError(nextError instanceof Error ? nextError.message : "Session revoke failed.");
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Sessions" description="Review and revoke active account sessions." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Visible sessions" value={sessions.length} description="Sessions scoped to the current subject" />
        <MetricCard label="Loading state" value={loading ? "Refreshing" : "Current"} description="Account session data freshness" />
      </div>
      {error ? <Toast tone="danger" message={error} /> : null}
      <InlineMutationResult error={mutationError} success={success} />
      <DetailPanel title="Active sessions">
        <ResourceTable
          items={sessions}
          getRowKey={(session) => session.id}
          emptyTitle="No active sessions"
          emptyBody="No active sessions are visible for this account."
          columns={[
            { key: "state", header: "State", render: (session) => <StatusBadge tone="info">{session.state}</StatusBadge> },
            { key: "id", header: "Session", render: (session) => <code>{session.id}</code> },
            { key: "client", header: "Client", render: (session) => session.client_id ?? "current account" },
            { key: "lastSeen", header: "Last seen", render: (session) => session.last_seen_at || "unknown" }
          ]}
          actions={[{ label: "Revoke", onClick: setRevokeSession, tone: "danger" }]}
        />
      </DetailPanel>
      <ConfirmDialog
        open={Boolean(revokeSession)}
        title="Revoke session"
        body={`Revoke session ${revokeSession?.id ?? ""}?`}
        confirmLabel="Revoke session"
        onCancel={() => setRevokeSession(null)}
        onConfirm={() => {
          if (!revokeSession) return;
          const sessionId = revokeSession.id;
          setRevokeSession(null);
          void runRevoke(sessionId);
        }}
      />
    </div>
  );
}
