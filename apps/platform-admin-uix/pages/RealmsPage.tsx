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
import { useMemo, useState } from "react";
import type { FormEvent } from "react";
import { ShortId } from "../components/ShortId";
import type { CreateRealmInput, Realm, UpdateRealmInput } from "../types";

const emptyCreateForm: CreateRealmInput = { slug: "", name: "", issuer_path: "", description: "" };

export function RealmsPage({
  onCreate,
  onDelete,
  onSelect,
  onUpdate,
  realms,
  selectedRealmId
}: {
  onCreate: (payload: CreateRealmInput) => Promise<void>;
  onDelete: (realmId: string) => Promise<void>;
  onSelect: (realmId: string) => void;
  onUpdate: (realmId: string, payload: UpdateRealmInput) => Promise<void>;
  realms: Realm[];
  selectedRealmId: string;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState<CreateRealmInput>(emptyCreateForm);
  const [deleteRealm, setDeleteRealm] = useState<Realm | null>(null);
  const [editRealm, setEditRealm] = useState<Realm | null>(null);
  const [editForm, setEditForm] = useState<UpdateRealmInput>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const selectedRealm = useMemo(
    () => realms.find((realm) => realm.id === selectedRealmId) ?? null,
    [realms, selectedRealmId]
  );

  function beginEdit(realm: Realm) {
    setEditRealm(realm);
    setEditForm({
      description: realm.description ?? "",
      issuer_path: realm.issuer_path,
      name: realm.name,
      slug: realm.slug
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
      setError(nextError instanceof Error ? nextError.message : "Realm mutation failed.");
    }
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        description: createForm.description?.trim() || null,
        issuer_path: createForm.issuer_path?.trim() || null,
        name: createForm.name.trim(),
        slug: createForm.slug.trim().toLowerCase()
      });
      setCreateForm(emptyCreateForm);
      setCreateOpen(false);
    }, "Realm provisioned.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editRealm) return;
    await runMutation(async () => {
      await onUpdate(editRealm.id, {
        description: editForm.description?.trim() || null,
        issuer_path: editForm.issuer_path?.trim() || null,
        name: editForm.name?.trim(),
        slug: editForm.slug?.trim().toLowerCase()
      });
      setEditRealm(null);
    }, "Realm updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Realm lifecycle" description="Create and manage issuer namespaces above tenant administration." />
      <InlineMutationResult error={error} success={success} />

      <DetailPanel title="Selected realm">
        {selectedRealm ? (
          <div className="tigrbl-summary-grid">
            <div>
              <span className="tigrbl-label">Realm</span>
              <strong>{selectedRealm.name}</strong>
              <p>{selectedRealm.slug} / {selectedRealm.issuer_path || "default issuer"}</p>
            </div>
            <div>
              <span className="tigrbl-label">Status</span>
              <StatusBadge tone="success">Active</StatusBadge>
            </div>
            <div>
              <span className="tigrbl-label">ID</span>
              <ShortId id={selectedRealm.id} />
            </div>
          </div>
        ) : (
          <p>No realm context is selected.</p>
        )}
      </DetailPanel>

      <DetailPanel title="Realms">
        <ResourceToolbar
          title="Platform realms"
          description="Realms are platform-owned issuer and namespace boundaries."
          createLabel="Create realm"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={realms}
          getRowKey={(realm) => realm.id}
          emptyTitle="No realms"
          emptyBody="No realms are visible for this platform session."
          columns={[
            {
              key: "name",
              header: "Realm",
              render: (realm) => (
                <button className="tigrbl-link-button" type="button" onClick={() => onSelect(realm.id)}>
                  <strong>{realm.name}</strong>
                  <span>{realm.slug} / {realm.issuer_path || "default issuer"}</span>
                </button>
              )
            },
            {
              key: "context",
              header: "Context",
              render: (realm) => (selectedRealmId === realm.id ? <StatusBadge tone="success">Selected</StatusBadge> : <StatusBadge>Available</StatusBadge>)
            },
            { key: "id", header: "ID", render: (realm) => <ShortId id={realm.id} /> }
          ]}
          actions={[
            { label: "Select", onClick: (realm) => onSelect(realm.id), tone: "primary" },
            { label: "Edit", onClick: beginEdit },
            { label: "Delete", onClick: setDeleteRealm, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create realm" description="Provision a platform issuer namespace." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create realm</Button>}>
          <FormField label="Slug" value={createForm.slug} onChange={(event) => setCreateForm({ ...createForm, slug: event.target.value })} required />
          <FormField label="Name" value={createForm.name} onChange={(event) => setCreateForm({ ...createForm, name: event.target.value })} required />
          <FormField label="Issuer path" value={createForm.issuer_path ?? ""} onChange={(event) => setCreateForm({ ...createForm, issuer_path: event.target.value })} />
          <FormField label="Description" value={createForm.description ?? ""} onChange={(event) => setCreateForm({ ...createForm, description: event.target.value })} />
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editRealm)} title="Edit realm" description={editRealm?.name} onClose={() => setEditRealm(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save realm</Button>}>
          <FormField label="Slug" value={editForm.slug ?? ""} onChange={(event) => setEditForm({ ...editForm, slug: event.target.value })} required />
          <FormField label="Name" value={editForm.name ?? ""} onChange={(event) => setEditForm({ ...editForm, name: event.target.value })} required />
          <FormField label="Issuer path" value={editForm.issuer_path ?? ""} onChange={(event) => setEditForm({ ...editForm, issuer_path: event.target.value })} />
          <FormField label="Description" value={editForm.description ?? ""} onChange={(event) => setEditForm({ ...editForm, description: event.target.value })} />
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteRealm)}
        title="Delete realm"
        body={`Delete ${deleteRealm?.name ?? "this realm"}? Realms that still own tenants cannot be deleted.`}
        confirmLabel="Delete realm"
        onCancel={() => setDeleteRealm(null)}
        onConfirm={() => {
          if (!deleteRealm) return;
          const realmId = deleteRealm.id;
          setDeleteRealm(null);
          void runMutation(() => onDelete(realmId), "Realm deleted.");
        }}
      />
    </div>
  );
}
