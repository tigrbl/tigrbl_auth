import { Button, Panel } from "../components/UI";
import type { AccountSession } from "../types";

export function SessionsPage({
  sessions,
  onRevoke
}: {
  sessions: AccountSession[];
  onRevoke: (sessionId: string) => Promise<void>;
}) {
  return (
    <Panel title="Sessions">
      <div style={{ display: "grid", gap: "10px" }}>
        {sessions.length === 0 ? <p>No active sessions.</p> : null}
        {sessions.map((session) => (
          <div
            key={session.id}
            style={{
              alignItems: "center",
              borderTop: "1px solid #d8e2dd",
              display: "grid",
              gap: "8px",
              gridTemplateColumns: "minmax(0, 1fr) auto",
              padding: "12px 0"
            }}
          >
            <div style={{ minWidth: 0 }}>
              <strong>{session.state}</strong>
              <p style={{ color: "#4f6d63", margin: "4px 0 0", overflowWrap: "anywhere" }}>{session.id}</p>
              <p style={{ color: "#4f6d63", margin: "4px 0 0" }}>Last seen: {session.last_seen_at || "unknown"}</p>
            </div>
            <Button variant="danger" onClick={() => void onRevoke(session.id)}>
              Revoke
            </Button>
          </div>
        ))}
      </div>
    </Panel>
  );
}
