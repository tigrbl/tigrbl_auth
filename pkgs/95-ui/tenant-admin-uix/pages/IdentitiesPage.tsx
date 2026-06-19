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
import type { CreateTenantIdentityInput, TenantIdentity, UpdateTenantIdentityInput } from "../types";

const emptyIdentityForm: CreateTenantIdentityInput = {
  username: "",
  email: "",
  password: "ChangeMe123!",
  is_admin: false,
  must_change_password: true,
  roles: []
};

function roleLabel(identity: TenantIdentity) {
  if (identity.is_superuser) return "Superuser";
  if (identity.is_admin) return "Admin";
  return "User";
}

export function IdentitiesPage({
  identities,
  onCreate,
  onDelete,
  onLock,
  onUnlock,
  onUpdate
}: {
  identities: TenantIdentity[];
  onCreate: (payload: CreateTenantIdentityInput) => Promise<void>;
  onDelete: (identityId: string) => Promise<void>;
  onLock: (identityId: string) => Promise<void>;
  onUnlock: (identityId: string) => Promise<void>;
  onUpdate: (identityId: string, payload: UpdateTenantIdentityInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState<CreateTenantIdentityInput>(emptyIdentityForm);
  const [deleteIdentity, setDeleteIdentity] = useState<TenantIdentity | null>(null);
  const [editIdentity, setEditIdentity] = useState<TenantIdentity | null>(null);
  const [editForm, setEditForm] = useState<UpdateTenantIdentityInput>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Identity mutation failed.");
    }
  }

  function beginEdit(identity: TenantIdentity) {
    setEditIdentity(identity);
    setEditForm({
      username: identity.username ?? "",
      email: identity.email ?? "",
      is_active: identity.is_active !== false,
      is_admin: Boolean(identity.is_admin),
      must_change_password: Boolean(identity.must_change_password),
      roles: identity.roles ?? []
    });
    setError("");
    setSuccess("");
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        ...createForm,
        username: createForm.username.trim(),
        email: createForm.email.trim().toLowerCase()
      });
      setCreateForm(emptyIdentityForm);
      setCreateOpen(false);
    }, "Identity created.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editIdentity) return;
    await runMutation(async () => {
      await onUpdate(editIdentity.id, {
        username: editForm.username?.trim(),
        email: editForm.email?.trim().toLowerCase(),
        is_active: editForm.is_active,
        is_admin: editForm.is_admin,
        must_change_password: editForm.must_change_password,
        roles: editForm.roles
      });
      setEditIdentity(null);
    }, "Identity updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant identities" description="Create, edit, lock, unlock, and delete tenant users and administrators." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Visible identities">
        <ResourceToolbar
          title="Tenant identities"
          description="Identity mutations are scoped to this tenant admin session."
          createLabel="Create identity"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={identities}
          getRowKey={(identity) => identity.id}
          emptyTitle="No identities"
          emptyBody="No identities are visible for this tenant admin session."
          columns={[
            { key: "identity", header: "Identity", render: (identity) => <><strong>{identity.username ?? identity.id}</strong><div>{identity.email ?? "No email"}</div></> },
            { key: "role", header: "Role", render: roleLabel },
            { key: "status", header: "Status", render: (identity) => <StatusBadge tone={identity.is_active === false ? "warning" : "success"}>{identity.is_active === false ? "Locked" : "Active"}</StatusBadge> },
            { key: "password", header: "Password", render: (identity) => identity.must_change_password ? <StatusBadge tone="warning">Must change</StatusBadge> : <StatusBadge>Normal</StatusBadge> }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Unlock", onClick: (identity) => void runMutation(() => onUnlock(identity.id), "Identity unlocked.") },
            { label: "Lock", onClick: (identity) => void runMutation(() => onLock(identity.id), "Identity locked."), tone: "danger" },
            { label: "Delete", onClick: setDeleteIdentity, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create identity" description="Provision a tenant-scoped user or administrator." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create identity</Button>}>
          <FormField label="Username" value={createForm.username} onChange={(event) => setCreateForm({ ...createForm, username: event.target.value })} required />
          <FormField label="Email" value={createForm.email} onChange={(event) => setCreateForm({ ...createForm, email: event.target.value })} type="email" required />
          <FormField label="Temporary password" value={createForm.password} onChange={(event) => setCreateForm({ ...createForm, password: event.target.value })} type="password" required />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(createForm.is_admin)} onChange={(event) => setCreateForm({ ...createForm, is_admin: event.target.checked })} />
            Tenant administrator
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(createForm.must_change_password)} onChange={(event) => setCreateForm({ ...createForm, must_change_password: event.target.checked })} />
            Force password change
          </label>
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editIdentity)} title="Edit identity" description={editIdentity?.email ?? editIdentity?.id} onClose={() => setEditIdentity(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save identity</Button>}>
          <FormField label="Username" value={editForm.username ?? ""} onChange={(event) => setEditForm({ ...editForm, username: event.target.value })} required />
          <FormField label="Email" value={editForm.email ?? ""} onChange={(event) => setEditForm({ ...editForm, email: event.target.value })} type="email" required />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={editForm.is_active !== false} onChange={(event) => setEditForm({ ...editForm, is_active: event.target.checked })} />
            Active
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(editForm.is_admin)} onChange={(event) => setEditForm({ ...editForm, is_admin: event.target.checked })} />
            Tenant administrator
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(editForm.must_change_password)} onChange={(event) => setEditForm({ ...editForm, must_change_password: event.target.checked })} />
            Force password change
          </label>
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteIdentity)}
        title="Delete identity"
        body={`Delete ${deleteIdentity?.username ?? "this identity"} from the tenant?`}
        confirmLabel="Delete identity"
        onCancel={() => setDeleteIdentity(null)}
        onConfirm={() => {
          if (!deleteIdentity) return;
          const identityId = deleteIdentity.id;
          setDeleteIdentity(null);
          void runMutation(() => onDelete(identityId), "Identity deleted.");
        }}
      />
    </div>
  );
}
