import { DetailPanel, JsonViewer, PageHeader, StatusBadge } from "@tba/ui-primitives";
import type { AdminSession } from "../types";
import { BACKEND_APP_BASE_URL, BACKEND_APP } from "../services/backendSurface";

export function SettingsPage({ session }: { session: AdminSession | null }) {
  return (
    <div className="tba-page-stack">
      <PageHeader title="Platform settings" description="Read-only product surface and runtime context for the platform admin UIX." />
      <DetailPanel title="Surface">
        <dl className="tba-definition-list">
          <dt>Backend app</dt><dd>{BACKEND_APP}</dd>
          <dt>backend-app base URL</dt><dd><code>{BACKEND_APP_BASE_URL}</code></dd>
          <dt>Mode</dt><dd><StatusBadge tone="info">Local dev</StatusBadge></dd>
        </dl>
      </DetailPanel>
      <DetailPanel title="Session payload">
        <JsonViewer value={session} />
      </DetailPanel>
    </div>
  );
}
