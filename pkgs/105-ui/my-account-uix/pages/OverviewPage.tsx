import { Card, DetailPanel, MetricCard, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { AccountProfile, AccountSession, AuthorizedApp, Consent } from "../types";

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
        <MetricCard label="Sessions" value={activeSessions} description={activeSessions > 0 ? "Active account sessions" : "No active sessions"} />
        <MetricCard label="Authorized apps" value={apps.length} description={apps.length > 0 ? "Current app grants" : "No app grants"} />
        <MetricCard label="Consent grants" value={activeConsents} description={activeConsents > 0 ? "Active consent records" : "No active consents"} />
        <MetricCard label="Roles" value={profile.roles.length} description={profile.roles.length > 0 ? "Assigned account roles" : "No role claims"} />
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
