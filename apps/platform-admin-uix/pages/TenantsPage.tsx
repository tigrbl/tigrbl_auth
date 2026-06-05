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
import type { CreateTenantInput, Realm, Tenant, UpdateTenantInput } from "../types";

const emptyCreateForm: CreateTenantInput = { slug: "", name: "", email: "" };

function tenantStatus(tenant: Tenant) {
  return tenant.is_active === false ? "Suspended" : "Active";
}

export function TenantsPage({
  selectedTenantId,
  selectedRealmId,
  realms,
  tenants,
  onCreate,
  onDelete,
  onDisable,
  onEnable,
  onSelect,
  onUpdate
}: {
  selectedTenantId: string;
  selectedRealmId?: string;
  realms?: Realm[];
  tenants: Tenant[];
  onCreate: (payload: CreateTenantInput) => Promise<void>;
  onDelete: (tenantId: string) => Promise<void>;
  onDisable: (tenantId: string) => Promise<void>;
  onEnable: (tenantId: string) => Promise<void>;
  onSelect: (tenantId: string) => void;
  onUpdate: (tenantId: string, payload: UpdateTenantInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState<CreateTenantInput>(emptyCreateForm);
  const [deleteTenant, setDeleteTenant] = useState<Tenant | null>(null);
  const [editTenant, setEditTenant] = useState<Tenant | null>(null);
  const [editForm, setEditForm] = useState<UpdateTenantInput>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const selectedTenant = useMemo(
    () => tenants.find((tenant) => tenant.id === selectedTenantId) ?? null,
    [selectedTenantId, tenants]
  );
  const selectedRealm = useMemo(
    () => (realms ?? []).find((realm) => realm.id === selectedRealmId) ?? null,
    [realms, selectedRealmId]
  );

  function beginEdit(tenant: Tenant) {
    setEditTenant(tenant);
    setEditForm({
      email: tenant.email,
      is_active: tenant.is_active !== false,
      name: tenant.name,
      slug: tenant.slug
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
      setError(nextError instanceof Error ? nextError.message : "Tenant mutation failed.");
    }
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        realm_id: selectedRealmId || null,
        slug: createForm.slug.trim().toLowerCase(),
        name: createForm.name.trim(),
        email: createForm.email.trim().toLowerCase()
      });
      setCreateForm(emptyCreateForm);
      setCreateOpen(false);
    }, "Tenant provisioned.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editTenant) return;
    await runMutation(async () => {
      await onUpdate(editTenant.id, {
        slug: editForm.slug?.trim().toLowerCase(),
        name: editForm.name?.trim(),
        email: editForm.email?.trim().toLowerCase(),
        is_active: editForm.is_active
      });
      setEditTenant(null);
    }, "Tenant updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Tenant lifecycle" description="Create, edit, suspend, resume, and delete platform tenants." />
      <InlineMutationResult error={error} success={success} />

      <DetailPanel title="Selected tenant">
        {selectedTenant ? (
          <div className="tigrbl-summary-grid">
            <div>
              <span className="tigrbl-label">Tenant</span>
              <strong>{selectedTenant.name}</strong>
              <p>{selectedTenant.slug} / {selectedTenant.email}</p>
            </div>
            <div>
              <span className="tigrbl-label">Realm</span>
              <strong>{selectedRealm?.name ?? "Default realm"}</strong>
              <p>{selectedRealm?.slug ?? selectedTenant.realm_id ?? "default"}</p>
            </div>
            <div>
              <span className="tigrbl-label">Status</span>
              <StatusBadge tone={selectedTenant.is_active === false ? "warning" : "success"}>{tenantStatus(selectedTenant)}</StatusBadge>
            </div>
            <div>
              <span className="tigrbl-label">ID</span>
              <ShortId id={selectedTenant.id} />
            </div>
          </div>
        ) : (
          <p>No tenant context is selected.</p>
        )}
      </DetailPanel>

      <DetailPanel title="Tenants">
        <ResourceToolbar
          title="Platform tenants"
          description="Tenant rows are platform-owned control-plane resources."
          createLabel="Create tenant"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={tenants}
          getRowKey={(tenant) => tenant.id}
          emptyTitle="No tenants"
          emptyBody="No tenants are visible for this platform session."
          columns={[
            {
              key: "name",
              header: "Tenant",
              render: (tenant) => (
                <button className="tigrbl-link-button" type="button" onClick={() => onSelect(tenant.id)}>
                  <strong>{tenant.name}</strong>
                  <span>{tenant.slug} / {tenant.email}</span>
                </button>
              )
            },
            {
              key: "realm",
              header: "Realm",
              render: (tenant) => {
                const realm = (realms ?? []).find((item) => item.id === tenant.realm_id);
                return <span>{realm?.slug ?? tenant.realm_id ?? "default"}</span>;
              }
            },
            {
              key: "status",
              header: "Status",
              render: (tenant) => (
                <StatusBadge tone={tenant.is_active === false ? "warning" : "success"}>{tenantStatus(tenant)}</StatusBadge>
              )
            },
            {
              key: "context",
              header: "Context",
              render: (tenant) => (selectedTenantId === tenant.id ? <StatusBadge tone="success">Selected</StatusBadge> : <StatusBadge>Available</StatusBadge>)
            },
            { key: "id", header: "ID", render: (tenant) => <ShortId id={tenant.id} /> }
          ]}
          actions={[
            { label: "Select", onClick: (tenant) => onSelect(tenant.id), tone: "primary" },
            { label: "Edit", onClick: beginEdit },
            {
              label: "Enable",
              onClick: (tenant) => void runMutation(() => onEnable(tenant.id), "Tenant enabled.")
            },
            {
              label: "Suspend",
              onClick: (tenant) => void runMutation(() => onDisable(tenant.id), "Tenant suspended."),
              tone: "danger"
            },
            { label: "Delete", onClick: setDeleteTenant, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create tenant" description="Provision a platform-owned tenant." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create tenant</Button>}>
          <FormField label="Slug" value={createForm.slug} onChange={(event) => setCreateForm({ ...createForm, slug: event.target.value })} required />
          <FormField label="Name" value={createForm.name} onChange={(event) => setCreateForm({ ...createForm, name: event.target.value })} required />
          <FormField label="Contact email" value={createForm.email} onChange={(event) => setCreateForm({ ...createForm, email: event.target.value })} type="email" required />
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editTenant)} title="Edit tenant" description={editTenant?.name} onClose={() => setEditTenant(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save tenant</Button>}>
          <FormField label="Slug" value={editForm.slug ?? ""} onChange={(event) => setEditForm({ ...editForm, slug: event.target.value })} required />
          <FormField label="Name" value={editForm.name ?? ""} onChange={(event) => setEditForm({ ...editForm, name: event.target.value })} required />
          <FormField label="Contact email" value={editForm.email ?? ""} onChange={(event) => setEditForm({ ...editForm, email: event.target.value })} type="email" required />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={editForm.is_active !== false} onChange={(event) => setEditForm({ ...editForm, is_active: event.target.checked })} />
            Active tenant
          </label>
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteTenant)}
        title="Delete tenant"
        body={`Delete ${deleteTenant?.name ?? "this tenant"}? This removes the platform tenant row from this surface.`}
        confirmLabel="Delete tenant"
        onCancel={() => setDeleteTenant(null)}
        onConfirm={() => {
          if (!deleteTenant) return;
          const tenantId = deleteTenant.id;
          setDeleteTenant(null);
          void runMutation(() => onDelete(tenantId), "Tenant deleted.");
        }}
      />
    </div>
  );
}
