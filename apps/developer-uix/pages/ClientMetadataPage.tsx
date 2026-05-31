import {
  Button,
  ConfirmDialog,
  DetailPanel,
  EditResourceDialog,
  FormField,
  InlineMutationResult,
  PageHeader,
  ResourceForm,
  ResourceTable
} from "@tigrbl-auth/uix-core";
import { useState } from "react";
import type { FormEvent } from "react";
import type { ClientRegistration, UpdateClientRegistrationInput } from "../types";

function listFromText(value: string) {
  return value
    .split(/[,\n]/)
    .map((item) => item.trim())
    .filter(Boolean);
}

export function ClientMetadataPage({
  registrations,
  onDelete,
  onUpdate
}: {
  registrations: ClientRegistration[];
  onDelete: (registrationId: string) => Promise<void>;
  onUpdate: (registrationId: string, payload: UpdateClientRegistrationInput) => Promise<void>;
}) {
  const [deleteRegistration, setDeleteRegistration] = useState<ClientRegistration | null>(null);
  const [editRegistration, setEditRegistration] = useState<ClientRegistration | null>(null);
  const [error, setError] = useState("");
  const [form, setForm] = useState({ client_name: "", redirect_uris: "", token_endpoint_auth_method: "" });
  const [success, setSuccess] = useState("");

  function beginEdit(registration: ClientRegistration) {
    setEditRegistration(registration);
    setForm({
      client_name: registration.client_name ?? registration.client_id ?? registration.id,
      redirect_uris: registration.redirect_uris?.join(", ") ?? "",
      token_endpoint_auth_method: registration.token_endpoint_auth_method ?? ""
    });
    setError("");
    setSuccess("");
  }

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Client metadata mutation failed.");
    }
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editRegistration) return;
    await runMutation(async () => {
      await onUpdate(editRegistration.id, {
        client_name: form.client_name.trim(),
        redirect_uris: listFromText(form.redirect_uris),
        token_endpoint_auth_method: form.token_endpoint_auth_method.trim()
      });
      setEditRegistration(null);
    }, "Client metadata updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Client metadata" description="Review and edit registered client metadata, auth method, and redirect configuration." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Registration records">
        <ResourceTable
          items={registrations}
          getRowKey={(registration) => registration.id}
          emptyTitle="No client metadata"
          emptyBody="No client registration records are visible yet."
          columns={[
            { key: "name", header: "Client", render: (registration) => registration.client_name ?? registration.client_id ?? registration.id },
            { key: "auth", header: "Auth method", render: (registration) => registration.token_endpoint_auth_method ?? "default" },
            { key: "redirects", header: "Redirect URIs", render: (registration) => registration.redirect_uris?.length ?? 0 }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Delete", onClick: setDeleteRegistration, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <EditResourceDialog open={Boolean(editRegistration)} title="Edit client metadata" description={editRegistration?.client_id ?? editRegistration?.id} onClose={() => setEditRegistration(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save metadata</Button>}>
          <FormField label="Client name" value={form.client_name} onChange={(event) => setForm({ ...form, client_name: event.target.value })} required />
          <FormField label="Redirect URIs" value={form.redirect_uris} onChange={(event) => setForm({ ...form, redirect_uris: event.target.value })} required />
          <FormField label="Token endpoint auth method" value={form.token_endpoint_auth_method} onChange={(event) => setForm({ ...form, token_endpoint_auth_method: event.target.value })} />
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteRegistration)}
        title="Delete client registration"
        body={`Delete ${deleteRegistration?.client_name ?? deleteRegistration?.client_id ?? "this registration"}?`}
        confirmLabel="Delete registration"
        onCancel={() => setDeleteRegistration(null)}
        onConfirm={() => {
          if (!deleteRegistration) return;
          const registrationId = deleteRegistration.id;
          setDeleteRegistration(null);
          void runMutation(() => onDelete(registrationId), "Client registration deleted.");
        }}
      />
    </div>
  );
}
