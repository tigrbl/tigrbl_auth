import { DataTable, DetailPanel, EmptyState, PageHeader, StatusBadge } from "@tigrbl-auth/uix-core";
import type { DeveloperApplication, IssuerMetadata } from "../types";

export function ScopesPage({ applications, metadata }: { applications: DeveloperApplication[]; metadata: IssuerMetadata | null }) {
  const scopes = metadata?.scopes_supported ?? Array.from(new Set(applications.flatMap((app) => app.scopes ?? [])));
  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Scopes" description="Review issuer-supported and application-requested scopes." />
      <DetailPanel title="Scope catalogue">
        <DataTable
          items={scopes.map((scope) => ({ scope }))}
          getRowKey={(row) => row.scope}
          empty={<EmptyState title="No scopes" body="No scopes are visible from issuer metadata or application records." />}
          columns={[
            { key: "scope", header: "Scope", render: (row) => <code>{row.scope}</code> },
            { key: "source", header: "Source", render: () => <StatusBadge tone="info">{metadata?.scopes_supported ? "Issuer" : "Application"}</StatusBadge> }
          ]}
        />
      </DetailPanel>
    </div>
  );
}
