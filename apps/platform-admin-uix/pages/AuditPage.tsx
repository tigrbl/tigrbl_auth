import { DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AdminSession, Tenant } from "../types";

export function AuditPage({ session, tenants }: { session: AdminSession | null; tenants: Tenant[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
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
        <div style={{ display: "grid", gap: "8px", gridTemplateColumns: "repeat(3, minmax(0, 1fr))" }}>
          <Metric label="Visible tenants" value={tenants.length} />
          <Metric label="Configured contacts" value={tenants.filter((tenant) => tenant.email).length} />
          <Metric label="Default public tenant" value={tenants.some((tenant) => tenant.slug === "public") ? "Present" : "Not visible"} />
        </div>
      </DetailPanel>
      <DetailPanel title="Audit event stream">
        <StatusBadge tone="info">Planned</StatusBadge>
        <p>Audit event review belongs here once the platform admin API exposes a filtered audit event view.</p>
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
