import { DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
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
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Developer dashboard" description="Self-service view for OAuth/OIDC application registration and client metadata." />
      <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
        <Metric label="Applications" value={applications.length} />
        <Metric label="Registrations" value={registrations.length} />
        <Metric label="Issuer" value={metadata?.issuer ? "Discovered" : "Unavailable"} />
        <Metric label="Tenant" value={session?.tenant_id ?? "unknown"} />
      </div>
      <DetailPanel title="Developer authority">
        <StatusBadge tone="info">{session?.roles.join(", ") || "tenant-developer"}</StatusBadge>
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
