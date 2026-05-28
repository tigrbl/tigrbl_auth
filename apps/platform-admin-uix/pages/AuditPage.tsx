import { Notice, Panel } from "../components/UI";
import type { AdminSession, Tenant } from "../types";

export function AuditPage({ session, tenants }: { session: AdminSession | null; tenants: Tenant[] }) {
  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <div>
        <h1 style={{ fontSize: "1.8rem", margin: "0 0 8px" }}>Platform posture</h1>
        <p style={{ color: "#526960", margin: 0 }}>Operational summary for platform-level tenant and authority administration.</p>
      </div>
      <Panel title="Current operator">
        {session?.authenticated ? (
          <div style={{ display: "grid", gap: "8px" }}>
            <strong>{session.username || session.email}</strong>
            <span>{session.is_superuser ? "Superuser" : "Administrator"} · tenant {session.tenant_id}</span>
          </div>
        ) : (
          <Notice tone="error">No authenticated platform administrator session.</Notice>
        )}
      </Panel>
      <Panel title="Tenant coverage">
        <div style={{ display: "grid", gap: "8px", gridTemplateColumns: "repeat(3, minmax(0, 1fr))" }}>
          <Metric label="Visible tenants" value={tenants.length} />
          <Metric label="Configured contacts" value={tenants.filter((tenant) => tenant.email).length} />
          <Metric label="Default public tenant" value={tenants.some((tenant) => tenant.slug === "public") ? "Present" : "Not visible"} />
        </div>
      </Panel>
      <Notice tone="info">Audit event review belongs here once the platform admin API exposes a filtered audit event view.</Notice>
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
