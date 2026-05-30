import { DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
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
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Service admin dashboard" description="Workload identity posture for service principals, keys, API keys, and token validation." />
      <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(5, minmax(0, 1fr))" }}>
        <Metric label="Services" value={services.length} />
        <Metric label="Service keys" value={serviceKeys.length} />
        <Metric label="API keys" value={apiKeys.length} />
        <Metric label="Tokens" value={tokenRecords.length} />
        <Metric label="Metadata" value={metadata?.resource ? "Ready" : "Unavailable"} />
      </div>
      <DetailPanel title="Operator authority">
        <StatusBadge tone="info">{session?.roles.join(", ") || "service-admin"}</StatusBadge>
      </DetailPanel>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <article style={{ background: "#ffffff", border: "1px solid #d7dfdb", borderRadius: "8px", padding: "14px" }}>
      <div style={{ color: "#60766e", fontSize: "0.82rem" }}>{label}</div>
      <strong style={{ display: "block", fontSize: "1.2rem", marginTop: "6px" }}>{value}</strong>
    </article>
  );
}
