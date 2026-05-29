import { DetailPanel, JsonViewer, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AdminSession } from "../types";
import { API_BASE_URL, PRODUCT_API } from "../services/backendSurface";

export function SettingsPage({ session }: { session: AdminSession | null }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Platform settings" description="Read-only product surface and runtime context for the platform admin UIX." />
      <DetailPanel title="Surface">
        <dl style={{ display: "grid", gap: "10px", gridTemplateColumns: "160px 1fr" }}>
          <dt>Product API</dt><dd>{PRODUCT_API}</dd>
          <dt>API base URL</dt><dd><code>{API_BASE_URL}</code></dd>
          <dt>Mode</dt><dd><StatusBadge tone="info">Local dev</StatusBadge></dd>
        </dl>
      </DetailPanel>
      <DetailPanel title="Session payload">
        <JsonViewer value={session} />
      </DetailPanel>
    </div>
  );
}
