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
import type { CreateTenantClientInput, TenantClient, UpdateTenantClientInput } from "../types";

const emptyClientForm = {
  client_name: "",
  redirect_uris: "",
  grant_types: "authorization_code,refresh_token",
  scopes: "openid,profile,email"
};

function listFromText(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function textFromList(value?: string[]) {
  return value?.join(", ") ?? "";
}

export function ClientsPage({
  clients,
  onCreate,
  onDelete,
  onUpdate
}: {
  clients: TenantClient[];
  onCreate: (payload: CreateTenantClientInput) => Promise<void>;
  onDelete: (clientId: string) => Promise<void>;
  onUpdate: (clientId: string, payload: UpdateTenantClientInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState(emptyClientForm);
  const [deleteClient, setDeleteClient] = useState<TenantClient | null>(null);
  const [editClient, setEditClient] = useState<TenantClient | null>(null);
  const [editForm, setEditForm] = useState(emptyClientForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Client mutation failed.");
    }
  }

  function toCreatePayload(): CreateTenantClientInput {
    return {
      client_name: createForm.client_name.trim(),
      redirect_uris: listFromText(createForm.redirect_uris),
      grant_types: listFromText(createForm.grant_types),
      scopes: listFromText(createForm.scopes)
    };
  }

  function beginEdit(client: TenantClient) {
    setEditClient(client);
    setEditForm({
      client_name: client.name ?? client.client_id ?? client.id,
      redirect_uris: textFromList(client.redirect_uris),
      grant_types: textFromList(client.grant_types),
      scopes: ""
    });
    setError("");
    setSuccess("");
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate(toCreatePayload());
      setCreateForm(emptyClientForm);
      setCreateOpen(false);
    }, "Client created.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editClient) return;
    await runMutation(async () => {
      await onUpdate(editClient.id, {
        client_name: editForm.client_name.trim(),
        redirect_uris: listFromText(editForm.redirect_uris),
        grant_types: listFromText(editForm.grant_types),
        scopes: listFromText(editForm.scopes)
      });
      setEditClient(null);
    }, "Client updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant clients" description="Create, edit, and delete tenant-local OAuth/OIDC clients." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Client applications">
        <ResourceToolbar
          title="Client applications"
          description="Client registration changes are tenant-scoped."
          createLabel="Create client"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={clients}
          getRowKey={(client) => client.id}
          emptyTitle="No clients"
          emptyBody="No tenant clients are visible for this session."
          columns={[
            { key: "client", header: "Client", render: (client) => <><strong>{client.name ?? client.client_id ?? client.id}</strong><div>{client.client_id ?? client.id}</div></> },
            { key: "redirects", header: "Redirect URIs", render: (client) => client.redirect_uris?.length ?? 0 },
            { key: "grants", header: "Grant types", render: (client) => client.grant_types?.join(", ") || "Default" },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Visible</StatusBadge> }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Delete", onClick: setDeleteClient, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create client" description="Register a tenant client application." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create client</Button>}>
          <FormField label="Client name" value={createForm.client_name} onChange={(event) => setCreateForm({ ...createForm, client_name: event.target.value })} required />
          <FormField label="Redirect URIs" value={createForm.redirect_uris} onChange={(event) => setCreateForm({ ...createForm, redirect_uris: event.target.value })} required />
          <FormField label="Grant types" value={createForm.grant_types} onChange={(event) => setCreateForm({ ...createForm, grant_types: event.target.value })} />
          <FormField label="Scopes" value={createForm.scopes} onChange={(event) => setCreateForm({ ...createForm, scopes: event.target.value })} />
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editClient)} title="Edit client" description={editClient?.client_id ?? editClient?.id} onClose={() => setEditClient(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save client</Button>}>
          <FormField label="Client name" value={editForm.client_name} onChange={(event) => setEditForm({ ...editForm, client_name: event.target.value })} required />
          <FormField label="Redirect URIs" value={editForm.redirect_uris} onChange={(event) => setEditForm({ ...editForm, redirect_uris: event.target.value })} required />
          <FormField label="Grant types" value={editForm.grant_types} onChange={(event) => setEditForm({ ...editForm, grant_types: event.target.value })} />
          <FormField label="Scopes" value={editForm.scopes} onChange={(event) => setEditForm({ ...editForm, scopes: event.target.value })} />
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteClient)}
        title="Delete client"
        body={`Delete ${deleteClient?.name ?? deleteClient?.client_id ?? "this client"} from the tenant?`}
        confirmLabel="Delete client"
        onCancel={() => setDeleteClient(null)}
        onConfirm={() => {
          if (!deleteClient) return;
          const clientId = deleteClient.id;
          setDeleteClient(null);
          void runMutation(() => onDelete(clientId), "Client deleted.");
        }}
      />
    </div>
  );
}
