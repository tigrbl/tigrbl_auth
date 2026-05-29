import { DetailPanel, EmptyState, JsonViewer, PageHeader } from "@tigrbl-auth/uix-core";
import type { DeveloperApplication, IssuerMetadata } from "../types";

export function OAuthFlowTesterPage({ application, metadata }: { application: DeveloperApplication | null; metadata: IssuerMetadata | null }) {
  const authorizeUrl = metadata?.authorization_endpoint && application?.client_id
    ? `${metadata.authorization_endpoint}?client_id=${encodeURIComponent(application.client_id)}&response_type=code&scope=openid&redirect_uri=${encodeURIComponent(application.redirect_uris?.[0] ?? "http://localhost/callback")}`
    : null;

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="OAuth flow tester" description="Generate an authorization URL for the selected client and issuer metadata." />
      {authorizeUrl ? (
        <DetailPanel title="Authorization request">
          <code style={{ wordBreak: "break-all" }}>{authorizeUrl}</code>
          <JsonViewer value={{ authorizeUrl }} />
        </DetailPanel>
      ) : (
        <EmptyState title="OAuth test unavailable" body="Load issuer metadata and a client with a client_id to generate an authorization request." />
      )}
    </div>
  );
}
