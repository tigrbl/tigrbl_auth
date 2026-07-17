import { DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { ServiceAdminSession } from "../types";

export function AuditPage({ session }: { session: ServiceAdminSession | null }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Service audit" description="Workload administration audit posture." />
      <DetailPanel title="Audit event stream">
        <StatusBadge tone="info">Planned</StatusBadge>
        <p>Service/workload audit events should be wired when the service-admin API exposes a scoped audit view.</p>
      </DetailPanel>
      <DetailPanel title="Audit scope">
        {session?.tenant_id ? <code>{session.tenant_id}</code> : <EmptyState title="No tenant scope" body="No tenant identifier is available in the current session." />}
      </DetailPanel>
    </div>
  );
}
