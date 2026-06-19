import { DetailPanel, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ClientRegistration, DeveloperApplication, DeveloperSession, IssuerMetadata } from "../types";

export function DashboardPage({
  applications,
  metadata,
  registrations,
  session
}: {
  applications: DeveloperApplication[];
  metadata: IssuerMetadata | null;
  registrations: ClientRegistration[];
  session: DeveloperSession | null;
}) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Developer dashboard" description="Self-service view for OAuth/OIDC application registration and client metadata." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Applications" value={applications.length} />
        <MetricCard label="Registrations" value={registrations.length} />
        <MetricCard label="Issuer" value={metadata?.issuer ? "Discovered" : "Unavailable"} />
        <MetricCard label="Tenant" value={session?.tenant_id ?? "unknown"} />
      </div>
      <DetailPanel title="Developer authority">
        <StatusBadge tone="info">{session?.roles.join(", ") || "tenant-developer"}</StatusBadge>
      </DetailPanel>
    </div>
  );
}
