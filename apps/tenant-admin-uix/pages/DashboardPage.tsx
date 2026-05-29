import { DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
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
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Tenant dashboard" description="Tenant-scoped administration overview for identities, client applications, consent, and key posture." />
      <div style={{ display: "grid", gap: "12px", gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
        <Metric label="Identities" value={identities.length} />
        <Metric label="Clients" value={clients.length} />
        <Metric label="Consents" value={consents.length} />
        <Metric label="Key events" value={keyEvents.length} />
      </div>
      <DetailPanel title="Current tenant context">
        <dl style={{ display: "grid", gap: "10px", gridTemplateColumns: "160px 1fr" }}>
          <dt>Tenant ID</dt><dd><code>{session?.tenant_id ?? "unknown"}</code></dd>
          <dt>Operator</dt><dd>{session?.username ?? session?.email ?? "unknown"}</dd>
          <dt>Authority</dt><dd><StatusBadge tone={session?.is_superuser ? "danger" : "info"}>{session?.is_superuser ? "Superuser" : "Tenant admin"}</StatusBadge></dd>
        </dl>
      </DetailPanel>
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <article style={{ background: "#ffffff", border: "1px solid #d7dfdb", borderRadius: "8px", padding: "14px" }}>
      <div style={{ color: "#60766e", fontSize: "0.82rem" }}>{label}</div>
      <strong style={{ display: "block", fontSize: "1.6rem", marginTop: "6px" }}>{value}</strong>
    </article>
  );
}
