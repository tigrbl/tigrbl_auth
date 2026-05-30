import { Card, DetailPanel, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AccountProfile, AccountSession, AuthorizedApp, Consent } from "../types";

function MetricCard({ label, value, tone = "info" }: { label: string; value: string | number; tone?: "info" | "success" | "warning" }) {
  return (
    <Card tone="compact">
      <p className="tigrbl-eyebrow">{label}</p>
      <h2 style={{ fontSize: "2rem", margin: "8px 0 0" }}>{value}</h2>
      <StatusBadge tone={tone}>{label}</StatusBadge>
    </Card>
  );
}

export function OverviewPage({
  apps,
  consents,
  profile,
  sessions
}: {
  apps: AuthorizedApp[];
  consents: Consent[];
  profile: AccountProfile;
  sessions: AccountSession[];
}) {
  const activeSessions = sessions.filter((session) => session.state !== "revoked" && !session.ended_at).length;
  const activeConsents = consents.filter((consent) => consent.state !== "revoked").length;

  return (
    <div className="tigrbl-page-stack">
      <PageHeader
        title="Account overview"
        description="Review the current signed-in subject, active sessions, and application grants."
      />
      <div className="tigrbl-metric-grid">
        <MetricCard label="Sessions" value={activeSessions} tone={activeSessions > 0 ? "success" : "warning"} />
        <MetricCard label="Authorized apps" value={apps.length} tone={apps.length > 0 ? "info" : "warning"} />
        <MetricCard label="Consent grants" value={activeConsents} tone={activeConsents > 0 ? "info" : "warning"} />
        <MetricCard label="Roles" value={profile.roles.length} tone={profile.roles.length > 0 ? "success" : "warning"} />
      </div>
      <DetailPanel title="Current subject">
        <div className="tigrbl-metric-grid">
          <Card tone="compact">
            <p className="tigrbl-eyebrow">Subject</p>
            <code>{profile.id}</code>
          </Card>
          <Card tone="compact">
            <p className="tigrbl-eyebrow">Tenant</p>
            <code>{profile.tenant_id}</code>
          </Card>
          <Card tone="compact">
            <p className="tigrbl-eyebrow">Status</p>
            <StatusBadge tone={profile.is_active ? "success" : "warning"}>{profile.is_active ? "Active" : "Inactive"}</StatusBadge>
          </Card>
        </div>
      </DetailPanel>
    </div>
  );
}
