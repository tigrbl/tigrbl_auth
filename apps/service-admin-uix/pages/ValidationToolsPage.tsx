import { Button, DetailPanel, EmptyState, FormField, JsonViewer, PageHeader, ResourceForm } from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";
import type { IntrospectionResult, ResourceMetadata } from "../types";

export function ValidationToolsPage({
  introspection,
  metadata,
  onIntrospect
}: {
  introspection: IntrospectionResult | null;
  metadata: ResourceMetadata | null;
  onIntrospect: (token: string) => Promise<void>;
}) {
  const [token, setToken] = useState("local-demo-token");

  async function submit(event: FormEvent) {
    event.preventDefault();
    await onIntrospect(token);
  }

  return (
    <div style={{ display: "grid", gap: "18px" }}>
      <PageHeader title="Validation tools" description="Inspect protected-resource metadata and test token introspection." />
      <DetailPanel title="Protected resource metadata">
        {metadata ? <JsonViewer value={metadata} /> : <EmptyState title="Metadata unavailable" body="Resource metadata was not returned by the service admin API." />}
      </DetailPanel>
      <DetailPanel title="Token introspection">
        <ResourceForm onSubmit={submit} footer={<Button type="submit">Introspect token</Button>}>
          <FormField label="Token" value={token} onChange={(event) => setToken(event.target.value)} required />
        </ResourceForm>
        {introspection && <JsonViewer value={introspection} />}
      </DetailPanel>
    </div>
  );
}
