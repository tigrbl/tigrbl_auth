import { DetailPanel, JsonViewer, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantAdminSession } from "../types";

export function SessionsPage({ session }: { session: TenantAdminSession | null }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant sessions" description="Review the current tenant administrator session. Session listing and revocation should use dedicated tenant API paths once exposed." />
      <DetailPanel title="Current session">
        <StatusBadge tone={session?.authenticated ? "success" : "warning"}>{session?.authenticated ? "Authenticated" : "Unauthenticated"}</StatusBadge>
        <JsonViewer value={session} />
      </DetailPanel>
    </div>
  );
}
