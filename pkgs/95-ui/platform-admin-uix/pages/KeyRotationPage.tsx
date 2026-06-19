import { Button, DetailPanel, EmptyState, JsonViewer, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { Tenant } from "../types";

export function KeyRotationPage({ selectedTenant, tenants }: { selectedTenant: Tenant | null; tenants: Tenant[] }) {
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Key rotation" description="Platform signing-key posture and rotation front door." />
      <DetailPanel title="Rotation scope">
        {selectedTenant ? (
          <div style={{ display: "grid", gap: "8px" }}>
            <strong>{selectedTenant.name}</strong>
            <span>{selectedTenant.slug} / {selectedTenant.email}</span>
            <StatusBadge tone="info">Manual rotation path planned</StatusBadge>
          </div>
        ) : (
          <EmptyState title="No tenant selected" body="Select a tenant before reviewing tenant-specific key rotation posture." />
        )}
      </DetailPanel>
      <DetailPanel title="Rotation action">
        <p>The platform admin API has key rotation event resources, but the convenience rotation command should be exposed as a dedicated action before this button is enabled.</p>
        <Button type="button" disabled>Rotate signing key</Button>
      </DetailPanel>
      <DetailPanel title="Visible key context">
        <JsonViewer value={{ selectedTenantId: selectedTenant?.id ?? null, visibleTenants: tenants.length, status: "planned-action" }} />
      </DetailPanel>
    </div>
  );
}
