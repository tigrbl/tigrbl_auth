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
import type { ClientRegistration, CreateClientRegistrationInput, DeveloperApplication, UpdateClientRegistrationInput } from "../types";

type ApplicationRow = {
  id: string;
  client_id?: string | null;
  name?: string | null;
  redirect_uris?: string[];
  source: "application" | "registration";
};

const emptyForm = {
  client_name: "",
  redirect_uris: "",
  grant_types: "authorization_code,refresh_token",
  response_types: "code",
  scope: "openid profile email",
  token_endpoint_auth_method: "client_secret_basic"
};

function listFromText(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

function rowsFrom(applications: DeveloperApplication[], registrations: ClientRegistration[]): ApplicationRow[] {
  if (applications.length) {
    return applications.map((application) => ({ ...application, source: "application" }));
  }
  return registrations.map((registration) => ({
    id: registration.id,
    client_id: registration.client_id,
    name: registration.client_name,
    redirect_uris: registration.redirect_uris,
    source: "registration"
  }));
}

export function ApplicationsPage({
  applications,
  registrations,
  onCreate,
  onDeleteApplication,
  onDeleteRegistration,
  onUpdateApplication,
  onUpdateRegistration
}: {
  applications: DeveloperApplication[];
  registrations: ClientRegistration[];
  onCreate: (payload: CreateClientRegistrationInput) => Promise<void>;
  onDeleteApplication: (clientId: string) => Promise<void>;
  onDeleteRegistration: (registrationId: string) => Promise<void>;
  onUpdateApplication: (clientId: string, payload: UpdateClientRegistrationInput) => Promise<void>;
  onUpdateRegistration: (registrationId: string, payload: UpdateClientRegistrationInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState(emptyForm);
  const [deleteRow, setDeleteRow] = useState<ApplicationRow | null>(null);
  const [editRow, setEditRow] = useState<ApplicationRow | null>(null);
  const [editForm, setEditForm] = useState(emptyForm);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const rows = rowsFrom(applications, registrations);

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Application mutation failed.");
    }
  }

  function createPayload(): CreateClientRegistrationInput {
    return {
      client_name: createForm.client_name.trim(),
      redirect_uris: listFromText(createForm.redirect_uris),
      grant_types: listFromText(createForm.grant_types),
      response_types: listFromText(createForm.response_types),
      scope: createForm.scope.trim(),
      token_endpoint_auth_method: createForm.token_endpoint_auth_method.trim()
    };
  }

  function updatePayload(): UpdateClientRegistrationInput {
    return {
      client_name: editForm.client_name.trim(),
      redirect_uris: listFromText(editForm.redirect_uris),
      grant_types: listFromText(editForm.grant_types),
      token_endpoint_auth_method: editForm.token_endpoint_auth_method.trim()
    };
  }

  function beginEdit(row: ApplicationRow) {
    setEditRow(row);
    setEditForm({
      ...emptyForm,
      client_name: row.name ?? row.client_id ?? row.id,
      redirect_uris: row.redirect_uris?.join(", ") ?? ""
    });
    setError("");
    setSuccess("");
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate(createPayload());
      setCreateForm(emptyForm);
      setCreateOpen(false);
    }, "Application registered.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editRow) return;
    await runMutation(async () => {
      if (editRow.source === "application") {
        await onUpdateApplication(editRow.id, updatePayload());
      } else {
        await onUpdateRegistration(editRow.id, updatePayload());
      }
      setEditRow(null);
    }, "Application updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Applications" description="Register, edit, and delete OAuth/OIDC applications in the current tenant developer context." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Developer applications">
        <ResourceToolbar
          title="Applications"
          description="Applications map to developer-owned client registration records."
          createLabel="Register application"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={rows}
          getRowKey={(app) => app.id}
          emptyTitle="No applications"
          emptyBody="No developer applications are visible yet."
          columns={[
            { key: "name", header: "Application", render: (app) => <><strong>{app.name ?? app.client_id ?? app.id}</strong><div>{app.client_id ?? app.id}</div></> },
            { key: "redirects", header: "Redirect URIs", render: (app) => app.redirect_uris?.length ?? 0 },
            { key: "source", header: "Source", render: (app) => <StatusBadge tone="info">{app.source}</StatusBadge> },
            { key: "status", header: "Status", render: () => <StatusBadge tone="success">Visible</StatusBadge> }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Delete", onClick: setDeleteRow, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Register application" description="Create a dynamic client registration." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Register application</Button>}>
          <FormField label="Application name" value={createForm.client_name} onChange={(event) => setCreateForm({ ...createForm, client_name: event.target.value })} required />
          <FormField label="Redirect URIs" value={createForm.redirect_uris} onChange={(event) => setCreateForm({ ...createForm, redirect_uris: event.target.value })} required />
          <FormField label="Grant types" value={createForm.grant_types} onChange={(event) => setCreateForm({ ...createForm, grant_types: event.target.value })} />
          <FormField label="Response types" value={createForm.response_types} onChange={(event) => setCreateForm({ ...createForm, response_types: event.target.value })} />
          <FormField label="Scope" value={createForm.scope} onChange={(event) => setCreateForm({ ...createForm, scope: event.target.value })} />
          <FormField label="Token endpoint auth method" value={createForm.token_endpoint_auth_method} onChange={(event) => setCreateForm({ ...createForm, token_endpoint_auth_method: event.target.value })} />
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editRow)} title="Edit application" description={editRow?.client_id ?? editRow?.id} onClose={() => setEditRow(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save application</Button>}>
          <FormField label="Application name" value={editForm.client_name} onChange={(event) => setEditForm({ ...editForm, client_name: event.target.value })} required />
          <FormField label="Redirect URIs" value={editForm.redirect_uris} onChange={(event) => setEditForm({ ...editForm, redirect_uris: event.target.value })} required />
          <FormField label="Grant types" value={editForm.grant_types} onChange={(event) => setEditForm({ ...editForm, grant_types: event.target.value })} />
          <FormField label="Token endpoint auth method" value={editForm.token_endpoint_auth_method} onChange={(event) => setEditForm({ ...editForm, token_endpoint_auth_method: event.target.value })} />
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteRow)}
        title="Delete application"
        body={`Delete ${deleteRow?.name ?? deleteRow?.client_id ?? "this application"}?`}
        confirmLabel="Delete application"
        onCancel={() => setDeleteRow(null)}
        onConfirm={() => {
          if (!deleteRow) return;
          const row = deleteRow;
          setDeleteRow(null);
          void runMutation(
            () => row.source === "application" ? onDeleteApplication(row.id) : onDeleteRegistration(row.id),
            "Application deleted."
          );
        }}
      />
    </div>
  );
}
