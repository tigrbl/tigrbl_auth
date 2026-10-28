import { DetailPanel, EmptyState, JsonViewer, PageHeader } from "@tba/ui-primitives";
import type { IssuerMetadata } from "../types";

export function DiscoveryPage({ metadata }: { metadata: IssuerMetadata | null }) {
  return (
    <div className="tba-page-stack">
      <PageHeader title="Issuer discovery" description="Inspect OIDC issuer metadata used by developer applications." />
      {metadata ? (
        <DetailPanel title={metadata.issuer ?? "Issuer metadata"}>
          <JsonViewer value={metadata} />
        </DetailPanel>
      ) : (
        <EmptyState title="Discovery unavailable" body="The developer API did not return issuer metadata for this local session." />
      )}
    </div>
  );
}
