import {
  Button,
  CreateResourceDialog,
  DetailPanel,
  FormField,
  InlineMutationResult,
  PageHeader,
  ResourceForm,
  ResourceTable,
  ResourceToolbar,
  StatusBadge
} from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";
import type { KeyRotationEvent } from "../types";

export function KeyEventsPage({
  keyEvents,
  onRotate,
  tenantId
}: {
  keyEvents: KeyRotationEvent[];
  onRotate: (payload: { tenant_id?: string; reason?: string }) => Promise<void>;
  tenantId?: string;
}) {
  const [error, setError] = useState("");
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("operator-requested");
  const [success, setSuccess] = useState("");

  async function submit(event: FormEvent) {
    event.preventDefault();
    setError("");
    setSuccess("");
    try {
      await onRotate({ tenant_id: tenantId, reason: reason.trim() || "operator-requested" });
      setOpen(false);
      setReason("operator-requested");
      setSuccess("Key rotation requested.");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Key rotation request failed.");
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant key events" description="Review tenant key rotation events and request tenant-scoped key rotation." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Key rotation events">
        <ResourceToolbar
          title="Key rotation"
          description="Tenant admins can request rotation for their tenant context."
          createLabel="Request rotation"
          onCreate={() => {
            setOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={keyEvents}
          getRowKey={(event) => event.id}
          emptyTitle="No key events"
          emptyBody="No key rotation events are visible for this tenant."
          columns={[
            { key: "id", header: "Event", render: (event) => <code>{event.id}</code> },
            { key: "tenant", header: "Tenant", render: (event) => event.tenant_id ?? tenantId ?? "current tenant" },
            { key: "status", header: "Status", render: (event) => <StatusBadge tone="info">{event.status ?? "Recorded"}</StatusBadge> },
            { key: "created", header: "Created", render: (event) => event.created_at ?? "unknown" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={open} title="Request key rotation" description="Create a tenant-scoped key rotation event." onClose={() => setOpen(false)}>
        <ResourceForm onSubmit={submit} footer={<Button type="submit">Request rotation</Button>}>
          <FormField label="Reason" value={reason} onChange={(event) => setReason(event.target.value)} required />
        </ResourceForm>
      </CreateResourceDialog>
    </div>
  );
}
