import { DetailPanel, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { KeyRotationEvent, TenantAdminSession, TenantClient, TenantConsent, TenantIdentity } from "../types";

export function DashboardPage({
  clients,
  consents,
  identities,
  keyEvents,
  session
}: {
  clients: TenantClient[];
  consents: TenantConsent[];
  identities: TenantIdentity[];
  keyEvents: KeyRotationEvent[];
  session: TenantAdminSession | null;
}) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant dashboard" description="Tenant-scoped administration overview for identities, client applications, consent, and key posture." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Identities" value={identities.length} />
        <MetricCard label="Clients" value={clients.length} />
        <MetricCard label="Consents" value={consents.length} />
        <MetricCard label="Key events" value={keyEvents.length} />
      </div>
      <DetailPanel title="Current tenant context">
        <dl className="tigrbl-definition-list">
          <dt>Tenant ID</dt><dd><code>{session?.tenant_id ?? "unknown"}</code></dd>
          <dt>Operator</dt><dd>{session?.username ?? session?.email ?? "unknown"}</dd>
          <dt>Authority</dt><dd><StatusBadge tone={session?.is_superuser ? "danger" : "info"}>{session?.is_superuser ? "Superuser" : "Tenant admin"}</StatusBadge></dd>
        </dl>
      </DetailPanel>
    </div>
  );
}
