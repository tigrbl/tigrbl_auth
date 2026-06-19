import {
  Button,
  ConfirmDialog,
  CreateResourceDialog,
  DetailPanel,
  EditResourceDialog,
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
import type { ApiKeyRecord, CreateApiKeyInput, ServiceIdentity, UpdateApiKeyInput } from "../types";

const emptyApiKeyForm = {
  service_id: "",
  name: "",
  scopes: ""
};

function listFromText(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function ApiKeysPage({
  apiKeys,
  services,
  onCreate,
  onRevoke,
  onUpdate
}: {
  apiKeys: ApiKeyRecord[];
  services: ServiceIdentity[];
  onCreate: (payload: CreateApiKeyInput) => Promise<void>;
  onRevoke: (apiKeyId: string) => Promise<void>;
  onUpdate: (apiKeyId: string, payload: UpdateApiKeyInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState(emptyApiKeyForm);
  const [editKey, setEditKey] = useState<ApiKeyRecord | null>(null);
  const [editForm, setEditForm] = useState({ name: "", scopes: "", status: "" });
  const [error, setError] = useState("");
  const [revokeKey, setRevokeKey] = useState<ApiKeyRecord | null>(null);
  const [success, setSuccess] = useState("");

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "API key mutation failed.");
    }
  }

  function beginEdit(key: ApiKeyRecord) {
    setEditKey(key);
    setEditForm({
      name: key.name ?? key.id,
      scopes: key.scopes?.join(", ") ?? "",
      status: key.status ?? ""
    });
    setError("");
    setSuccess("");
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        service_id: createForm.service_id.trim(),
        name: createForm.name.trim(),
        scopes: listFromText(createForm.scopes)
      });
      setCreateForm(emptyApiKeyForm);
      setCreateOpen(false);
    }, "API key created.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editKey) return;
    await runMutation(async () => {
      await onUpdate(editKey.id, {
        name: editForm.name.trim(),
        scopes: listFromText(editForm.scopes),
        status: editForm.status.trim() || undefined
      });
      setEditKey(null);
    }, "API key updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="API keys" description="Issue, edit, and revoke scoped API keys for workload integrations." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="API key records">
        <ResourceToolbar
          title="API keys"
          description="API keys are scoped to service identities and workload permissions."
          createLabel="Create API key"
          onCreate={() => {
            setCreateOpen(true);
            setCreateForm({ ...emptyApiKeyForm, service_id: services[0]?.id ?? "" });
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={apiKeys}
          getRowKey={(key) => key.id}
          emptyTitle="No API keys"
          emptyBody="No API key records are visible yet."
          columns={[
            { key: "name", header: "Name", render: (key) => key.name ?? key.id },
            { key: "service", header: "Service", render: (key) => key.service_id ?? "unknown" },
            { key: "scopes", header: "Scopes", render: (key) => key.scopes?.join(", ") || "None" },
            { key: "status", header: "Status", render: (key) => <StatusBadge tone="info">{key.status ?? "Visible"}</StatusBadge> }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Revoke", onClick: setRevokeKey, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create API key" description="Issue an API key for a service identity." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create API key</Button>}>
          <FormField label="Service ID" value={createForm.service_id} onChange={(event) => setCreateForm({ ...createForm, service_id: event.target.value })} required />
          <FormField label="Name" value={createForm.name} onChange={(event) => setCreateForm({ ...createForm, name: event.target.value })} required />
          <FormField label="Scopes" value={createForm.scopes} onChange={(event) => setCreateForm({ ...createForm, scopes: event.target.value })} />
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editKey)} title="Edit API key" description={editKey?.id} onClose={() => setEditKey(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save API key</Button>}>
          <FormField label="Name" value={editForm.name} onChange={(event) => setEditForm({ ...editForm, name: event.target.value })} required />
          <FormField label="Scopes" value={editForm.scopes} onChange={(event) => setEditForm({ ...editForm, scopes: event.target.value })} />
          <FormField label="Status" value={editForm.status} onChange={(event) => setEditForm({ ...editForm, status: event.target.value })} />
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(revokeKey)}
        title="Revoke API key"
        body={`Revoke API key ${revokeKey?.name ?? revokeKey?.id ?? ""}?`}
        confirmLabel="Revoke API key"
        onCancel={() => setRevokeKey(null)}
        onConfirm={() => {
          if (!revokeKey) return;
          const keyId = revokeKey.id;
          setRevokeKey(null);
          void runMutation(() => onRevoke(keyId), "API key revoked.");
        }}
      />
    </div>
  );
}
