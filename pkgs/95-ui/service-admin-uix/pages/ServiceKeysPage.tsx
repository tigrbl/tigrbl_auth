import {
  Button,
  ConfirmDialog,
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
import type { CreateServiceKeyInput, ServiceIdentity, ServiceKey } from "../types";

const emptyKeyForm: CreateServiceKeyInput = {
  service_id: "",
  kid: "",
  algorithm: "RS256"
};

export function ServiceKeysPage({
  serviceKeys,
  services,
  onCreate,
  onRevoke
}: {
  serviceKeys: ServiceKey[];
  services: ServiceIdentity[];
  onCreate: (payload: CreateServiceKeyInput) => Promise<void>;
  onRevoke: (keyId: string) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [form, setForm] = useState<CreateServiceKeyInput>(emptyKeyForm);
  const [revokeKey, setRevokeKey] = useState<ServiceKey | null>(null);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Service key mutation failed.");
    }
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        service_id: form.service_id.trim(),
        kid: form.kid?.trim(),
        algorithm: form.algorithm?.trim()
      });
      setForm(emptyKeyForm);
      setCreateOpen(false);
    }, "Service key created.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Service keys" description="Create and revoke service key material for workload identities." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Keys">
        <ResourceToolbar
          title="Service keys"
          description="Service keys bind key material to workload principals."
          createLabel="Create service key"
          onCreate={() => {
            setCreateOpen(true);
            setForm({ ...emptyKeyForm, service_id: services[0]?.id ?? "" });
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={serviceKeys}
          getRowKey={(key) => key.id}
          emptyTitle="No service keys"
          emptyBody="No service keys are visible yet."
          columns={[
            { key: "kid", header: "KID", render: (key) => <code>{key.kid ?? key.id}</code> },
            { key: "service", header: "Service", render: (key) => key.service_id ?? "unknown" },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> },
            { key: "created", header: "Created", render: (key) => key.created_at ?? "unknown" }
          ]}
          actions={[{ label: "Revoke", onClick: setRevokeKey, tone: "danger" }]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create service key" description="Issue key material for a service identity." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submit} footer={<Button type="submit">Create service key</Button>}>
          <FormField label="Service ID" value={form.service_id} onChange={(event) => setForm({ ...form, service_id: event.target.value })} required />
          <FormField label="KID" value={form.kid ?? ""} onChange={(event) => setForm({ ...form, kid: event.target.value })} />
          <FormField label="Algorithm" value={form.algorithm ?? ""} onChange={(event) => setForm({ ...form, algorithm: event.target.value })} />
        </ResourceForm>
      </CreateResourceDialog>

      <ConfirmDialog
        open={Boolean(revokeKey)}
        title="Revoke service key"
        body={`Revoke service key ${revokeKey?.kid ?? revokeKey?.id ?? ""}?`}
        confirmLabel="Revoke key"
        onCancel={() => setRevokeKey(null)}
        onConfirm={() => {
          if (!revokeKey) return;
          const keyId = revokeKey.id;
          setRevokeKey(null);
          void runMutation(() => onRevoke(keyId), "Service key revoked.");
        }}
      />
    </div>
  );
}
