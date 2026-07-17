import { DetailPanel, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ApiKeyRecord, ResourceMetadata, ServiceAdminSession, ServiceIdentity, ServiceKey, TokenRecord } from "../types";

export function DashboardPage({
  apiKeys,
  metadata,
  serviceKeys,
  services,
  session,
  tokenRecords
}: {
  apiKeys: ApiKeyRecord[];
  metadata: ResourceMetadata | null;
  serviceKeys: ServiceKey[];
  services: ServiceIdentity[];
  session: ServiceAdminSession | null;
  tokenRecords: TokenRecord[];
}) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Service admin dashboard" description="Workload identity posture for service principals, keys, API keys, and token validation." />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Services" value={services.length} />
        <MetricCard label="Service keys" value={serviceKeys.length} />
        <MetricCard label="API keys" value={apiKeys.length} />
        <MetricCard label="Tokens" value={tokenRecords.length} />
        <MetricCard label="Metadata" value={metadata?.resource ? "Ready" : "Unavailable"} />
      </div>
      <DetailPanel title="Operator authority">
        <StatusBadge tone="info">{session?.roles.join(", ") || "service-admin"}</StatusBadge>
      </DetailPanel>
    </div>
  );
}
