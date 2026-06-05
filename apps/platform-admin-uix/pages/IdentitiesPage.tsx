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
import type { CreateIdentityInput, Identity, Tenant, UpdateIdentityInput } from "../types";

const emptyIdentityForm = {
  username: "",
  email: "",
  password: "ChangeMe123!",
  is_admin: true,
  is_superuser: false,
  must_change_password: true
};

function identityRole(identity: Pick<Identity, "is_admin" | "is_superuser">) {
  if (identity.is_superuser) return "Superuser";
  if (identity.is_admin) return "Admin";
  return "User";
}

export function IdentitiesPage({
  identities,
  onCreate,
  onDelete,
  onSelect,
  onSelectTenant,
  onUpdate,
  selectedIdentityId,
  selectedTenantId,
  tenants
}: {
  identities: Identity[];
  onCreate: (payload: CreateIdentityInput) => Promise<void>;
  onDelete: (identityId: string) => Promise<void>;
  onSelect: (identityId: string) => void;
  onSelectTenant: (tenantId: string) => void;
  onUpdate: (identityId: string, payload: UpdateIdentityInput) => Promise<void>;
  selectedIdentityId?: string;
  selectedTenantId: string;
  tenants: Tenant[];
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState(emptyIdentityForm);
  const [deleteIdentity, setDeleteIdentity] = useState<Identity | null>(null);
  const [editIdentity, setEditIdentity] = useState<Identity | null>(null);
  const [editForm, setEditForm] = useState<UpdateIdentityInput>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const selectedIdentity = useMemo(
    () => identities.find((identity) => identity.id === selectedIdentityId) ?? null,
    [identities, selectedIdentityId]
  );

  function beginEdit(identity: Identity) {
    setEditIdentity(identity);
    setEditForm({
      email: identity.email,
      is_active: identity.is_active,
      is_admin: identity.is_admin,
      is_superuser: identity.is_superuser,
      must_change_password: identity.must_change_password,
      roles: identity.roles,
      username: identity.username
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
      setError(nextError instanceof Error ? nextError.message : "Identity mutation failed.");
    }
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    if (!selectedTenantId) return;
    await runMutation(async () => {
      await onCreate({
        tenant_id: selectedTenantId,
        username: createForm.username.trim(),
        email: createForm.email.trim().toLowerCase(),
        password: createForm.password,
        is_admin: createForm.is_admin,
        is_superuser: createForm.is_superuser,
        must_change_password: createForm.must_change_password
      });
      setCreateForm(emptyIdentityForm);
      setCreateOpen(false);
    }, "Identity provisioned.");
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
        is_superuser: editForm.is_superuser,
        must_change_password: editForm.must_change_password,
        roles: editForm.roles
      });
      setEditIdentity(null);
    }, "Identity updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Platform identities" description="Create, edit, suspend, activate, and delete tenant-bound identities." />
      <InlineMutationResult error={error} success={success} />

      <DetailPanel title="Tenant context">
        <select
          className="tigrbl-control"
          value={selectedTenantId}
          onChange={(event) => onSelectTenant(event.target.value)}
        >
          {tenants.map((tenant) => (
            <option key={tenant.id} value={tenant.id}>{tenant.name}</option>
          ))}
        </select>
      </DetailPanel>

      <DetailPanel title="Selected identity">
        {selectedIdentity ? (
          <div className="tigrbl-summary-grid">
            <div>
              <span className="tigrbl-label">Identity</span>
              <strong>{selectedIdentity.username}</strong>
              <p>{selectedIdentity.email}</p>
            </div>
            <div>
              <span className="tigrbl-label">Role</span>
              <StatusBadge tone={selectedIdentity.is_superuser || selectedIdentity.is_admin ? "success" : "info"}>{identityRole(selectedIdentity)}</StatusBadge>
            </div>
            <div>
              <span className="tigrbl-label">Status</span>
              <StatusBadge tone={selectedIdentity.is_active ? "success" : "warning"}>{selectedIdentity.is_active ? "Active" : "Suspended"}</StatusBadge>
            </div>
            <div>
              <span className="tigrbl-label">ID</span>
              <ShortId id={selectedIdentity.id} />
            </div>
          </div>
        ) : (
          <p>No identity context is selected.</p>
        )}
      </DetailPanel>

      <DetailPanel title="Visible identities">
        <ResourceToolbar
          title="Tenant identities"
          description="Platform-visible identities are scoped to the selected tenant."
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
          emptyBody="No identities are visible for the selected tenant."
          columns={[
            {
              key: "username",
              header: "Identity",
              render: (identity) => (
                <button className="tigrbl-link-button" type="button" onClick={() => onSelect(identity.id)}>
                  <strong>{identity.username}</strong>
                  <span>{identity.email}</span>
                </button>
              )
            },
            { key: "role", header: "Role", render: (identity) => identityRole(identity) },
            { key: "status", header: "Status", render: (identity) => <StatusBadge tone={identity.is_active ? "success" : "warning"}>{identity.is_active ? "Active" : "Suspended"}</StatusBadge> },
            { key: "password", header: "Password", render: (identity) => identity.must_change_password ? <StatusBadge tone="warning">Must change</StatusBadge> : <StatusBadge tone="success">Current</StatusBadge> },
            { key: "id", header: "ID", render: (identity) => <ShortId id={identity.id} /> }
          ]}
          actions={[
            { label: "Select", onClick: (identity) => onSelect(identity.id), tone: "primary" },
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            {
              label: "Activate",
              onClick: (identity) => void runMutation(() => onUpdate(identity.id, { is_active: true }), "Identity activated.")
            },
            {
              label: "Suspend",
              onClick: (identity) => void runMutation(() => onUpdate(identity.id, { is_active: false }), "Identity suspended."),
              tone: "danger"
            },
            { label: "Delete", onClick: setDeleteIdentity, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create identity" description="Provision an identity inside the selected tenant context." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit" disabled={!selectedTenantId}>Create identity</Button>}>
          <FormField label="Username" value={createForm.username} onChange={(event) => setCreateForm({ ...createForm, username: event.target.value })} required />
          <FormField label="Email" value={createForm.email} onChange={(event) => setCreateForm({ ...createForm, email: event.target.value })} type="email" required />
          <FormField label="Temporary password" value={createForm.password} onChange={(event) => setCreateForm({ ...createForm, password: event.target.value })} type="password" required />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={createForm.is_admin} onChange={(event) => setCreateForm({ ...createForm, is_admin: event.target.checked })} />
            Admin
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={createForm.is_superuser} onChange={(event) => setCreateForm({ ...createForm, is_superuser: event.target.checked })} />
            Superuser
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={createForm.must_change_password} onChange={(event) => setCreateForm({ ...createForm, must_change_password: event.target.checked })} />
            Force password change
          </label>
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editIdentity)} title="Edit identity" description={editIdentity?.email} onClose={() => setEditIdentity(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save identity</Button>}>
          <FormField label="Username" value={editForm.username ?? ""} onChange={(event) => setEditForm({ ...editForm, username: event.target.value })} required />
          <FormField label="Email" value={editForm.email ?? ""} onChange={(event) => setEditForm({ ...editForm, email: event.target.value })} type="email" required />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={editForm.is_active !== false} onChange={(event) => setEditForm({ ...editForm, is_active: event.target.checked })} />
            Active identity
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(editForm.is_admin)} onChange={(event) => setEditForm({ ...editForm, is_admin: event.target.checked })} />
            Admin
          </label>
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={Boolean(editForm.is_superuser)} onChange={(event) => setEditForm({ ...editForm, is_superuser: event.target.checked })} />
            Superuser
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
        body={`Delete ${deleteIdentity?.username ?? "this identity"}? This removes the identity row from the platform control plane.`}
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
