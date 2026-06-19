import {
  Button,
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

export function RedirectUrisPage({
  registrations,
  onUpdate
}: {
  registrations: ClientRegistration[];
  onUpdate: (registrationId: string, payload: UpdateClientRegistrationInput) => Promise<void>;
}) {
  const [editRegistration, setEditRegistration] = useState<ClientRegistration | null>(null);
  const [error, setError] = useState("");
  const [redirectUris, setRedirectUris] = useState("");
  const [success, setSuccess] = useState("");
  const rows = registrations.flatMap((registration) => (registration.redirect_uris ?? []).map((uri) => ({
    client: registration.client_name ?? registration.client_id ?? registration.id,
    registration,
    uri
  })));

  function beginEdit(registration: ClientRegistration) {
    setEditRegistration(registration);
    setRedirectUris(registration.redirect_uris?.join(", ") ?? "");
    setError("");
    setSuccess("");
  }

  async function submit(event: FormEvent) {
    event.preventDefault();
    if (!editRegistration) return;
    setError("");
    setSuccess("");
    try {
      await onUpdate(editRegistration.id, { redirect_uris: listFromText(redirectUris) });
      setEditRegistration(null);
      setSuccess("Redirect URIs updated.");
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Redirect URI update failed.");
    }
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Redirect URIs" description="Inspect and edit callback URLs configured across developer-owned clients." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Configured redirect URIs">
        <ResourceTable
          items={rows}
          getRowKey={(row) => `${row.registration.id}:${row.uri}`}
          emptyTitle="No redirect URIs"
          emptyBody="No redirect URIs are visible in the current registration records."
          columns={[
            { key: "client", header: "Client", render: (row) => row.client },
            { key: "uri", header: "URI", render: (row) => <code>{row.uri}</code> }
          ]}
          actions={[{ label: "Edit client URIs", onClick: (row) => beginEdit(row.registration), tone: "primary" }]}
        />
      </DetailPanel>

      <EditResourceDialog open={Boolean(editRegistration)} title="Edit redirect URIs" description={editRegistration?.client_name ?? editRegistration?.client_id ?? editRegistration?.id} onClose={() => setEditRegistration(null)}>
        <ResourceForm onSubmit={submit} footer={<Button type="submit">Save redirect URIs</Button>}>
          <FormField label="Redirect URIs" value={redirectUris} onChange={(event) => setRedirectUris(event.target.value)} required />
        </ResourceForm>
      </EditResourceDialog>
    </div>
  );
}
