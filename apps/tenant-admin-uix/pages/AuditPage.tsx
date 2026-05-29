import { DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { TenantAdminSession } from "../types";

export function AuditPage({ session }: { session: TenantAdminSession | null }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant audit" description="Tenant-scoped operational audit view." />
      <DetailPanel title="Audit event stream">
        <StatusBadge tone="info">Planned</StatusBadge>
        <p>Tenant audit event filtering should be added once the tenant-admin API exposes a tenant-scoped audit event resource.</p>
      </DetailPanel>
      <DetailPanel title="Audit scope">
        {session?.tenant_id ? <code>{session.tenant_id}</code> : <EmptyState title="No tenant scope" body="No tenant identifier is available in the current session." />}
      </DetailPanel>
    </div>
  );
}
