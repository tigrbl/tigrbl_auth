import { Button, DataTable, DetailPanel, EmptyState, MetricCard, PageHeader, StatusBadge, Toast } from "@tigrbl-auth/uix-core";
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
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Sessions" description="Review and revoke active account sessions." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Visible sessions" value={sessions.length} description="Sessions scoped to the current subject" />
        <MetricCard label="Loading state" value={loading ? "Refreshing" : "Current"} description="Account session data freshness" />
      </div>
      {error ? <Toast tone="danger" message={error} /> : null}
      <DetailPanel title="Active sessions">
        <DataTable
          items={sessions}
          getRowKey={(session) => session.id}
          empty={<EmptyState title="No active sessions" body="No active sessions are visible for this account." />}
          columns={[
            { key: "state", header: "State", render: (session) => <StatusBadge tone="info">{session.state}</StatusBadge> },
            { key: "id", header: "Session", render: (session) => <code>{session.id}</code> },
            { key: "client", header: "Client", render: (session) => session.client_id ?? "current account" },
            { key: "lastSeen", header: "Last seen", render: (session) => session.last_seen_at || "unknown" },
            { key: "actions", header: "Actions", render: (session) => <Button variant="danger" onClick={() => void onRevoke(session.id)}>Revoke</Button> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
