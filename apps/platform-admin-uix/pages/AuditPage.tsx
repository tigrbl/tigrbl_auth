import { DetailPanel, EmptyState, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AdminSession, Tenant } from "../types";

export function AuditPage({ session, tenants }: { session: AdminSession | null; tenants: Tenant[] }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Platform posture" description="Operational summary for platform-level tenant and authority administration." />
      <DetailPanel title="Current operator">
        {session?.authenticated ? (
          <div style={{ display: "grid", gap: "8px" }}>
            <strong>{session.username || session.email}</strong>
            <span>{session.is_superuser ? "Superuser" : "Administrator"} / tenant {session.tenant_id}</span>
          </div>
        ) : (
          <EmptyState title="No session" body="No authenticated platform administrator session." />
        )}
      </DetailPanel>
      <DetailPanel title="Tenant coverage">
        <div className="tigrbl-metric-grid">
          <MetricCard label="Visible tenants" value={tenants.length} />
          <MetricCard label="Configured contacts" value={tenants.filter((tenant) => tenant.email).length} />
          <MetricCard label="Default public tenant" value={tenants.some((tenant) => tenant.slug === "public") ? "Present" : "Not visible"} />
        </div>
      </DetailPanel>
      <DetailPanel title="Audit event stream">
        <StatusBadge tone="info">Planned</StatusBadge>
        <p>Audit event review belongs here once the platform admin API exposes a filtered audit event view.</p>
      </DetailPanel>
    </div>
  );
}
