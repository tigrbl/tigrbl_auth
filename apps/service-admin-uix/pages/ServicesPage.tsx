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
import type { CreateServiceIdentityInput, ServiceIdentity, UpdateServiceIdentityInput } from "../types";

const emptyServiceForm: CreateServiceIdentityInput = {
  name: "",
  subject: "",
  tenant_id: "",
  is_active: true
};

export function ServicesPage({
  services,
  onCreate,
  onDelete,
  onUpdate
}: {
  services: ServiceIdentity[];
  onCreate: (payload: CreateServiceIdentityInput) => Promise<void>;
  onDelete: (serviceId: string) => Promise<void>;
  onUpdate: (serviceId: string, payload: UpdateServiceIdentityInput) => Promise<void>;
}) {
  const [createOpen, setCreateOpen] = useState(false);
  const [createForm, setCreateForm] = useState<CreateServiceIdentityInput>(emptyServiceForm);
  const [deleteService, setDeleteService] = useState<ServiceIdentity | null>(null);
  const [editService, setEditService] = useState<ServiceIdentity | null>(null);
  const [editForm, setEditForm] = useState<UpdateServiceIdentityInput>({});
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  async function runMutation(action: () => Promise<void>, message: string) {
    setError("");
    setSuccess("");
    try {
      await action();
      setSuccess(message);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Service mutation failed.");
    }
  }

  function beginEdit(service: ServiceIdentity) {
    setEditService(service);
    setEditForm({
      name: service.name ?? "",
      subject: service.subject ?? "",
      is_active: service.is_active !== false
    });
    setError("");
    setSuccess("");
  }

  async function submitCreate(event: FormEvent) {
    event.preventDefault();
    await runMutation(async () => {
      await onCreate({
        name: createForm.name.trim(),
        subject: createForm.subject?.trim(),
        tenant_id: createForm.tenant_id?.trim(),
        is_active: createForm.is_active
      });
      setCreateForm(emptyServiceForm);
      setCreateOpen(false);
    }, "Service identity created.");
  }

  async function submitEdit(event: FormEvent) {
    event.preventDefault();
    if (!editService) return;
    await runMutation(async () => {
      await onUpdate(editService.id, {
        name: editForm.name?.trim(),
        subject: editForm.subject?.trim(),
        is_active: editForm.is_active
      });
      setEditService(null);
    }, "Service identity updated.");
  }

  return (
    <div className="tigrbl-page-stack">
      <PageHeader title="Service identities" description="Create, edit, activate, suspend, and delete non-human service and workload principals." />
      <InlineMutationResult error={error} success={success} />
      <DetailPanel title="Visible services">
        <ResourceToolbar
          title="Service identities"
          description="Service identity rows represent workload principals."
          createLabel="Create service"
          onCreate={() => {
            setCreateOpen(true);
            setError("");
            setSuccess("");
          }}
        />
        <ResourceTable
          items={services}
          getRowKey={(service) => service.id}
          emptyTitle="No services"
          emptyBody="No service identities are visible for this service admin session."
          columns={[
            { key: "name", header: "Service", render: (service) => <><strong>{service.name ?? service.subject ?? service.id}</strong><div>{service.subject ?? service.id}</div></> },
            { key: "tenant", header: "Tenant", render: (service) => service.tenant_id ?? "unknown" },
            { key: "status", header: "Status", render: (service) => <StatusBadge tone={service.is_active === false ? "warning" : "success"}>{service.is_active === false ? "Suspended" : "Active"}</StatusBadge> }
          ]}
          actions={[
            { label: "Edit", onClick: beginEdit, tone: "primary" },
            { label: "Activate", onClick: (service) => void runMutation(() => onUpdate(service.id, { is_active: true }), "Service activated.") },
            { label: "Suspend", onClick: (service) => void runMutation(() => onUpdate(service.id, { is_active: false }), "Service suspended."), tone: "danger" },
            { label: "Delete", onClick: setDeleteService, tone: "danger" }
          ]}
        />
      </DetailPanel>

      <CreateResourceDialog open={createOpen} title="Create service" description="Provision a workload/service identity." onClose={() => setCreateOpen(false)}>
        <ResourceForm onSubmit={submitCreate} footer={<Button type="submit">Create service</Button>}>
          <FormField label="Name" value={createForm.name} onChange={(event) => setCreateForm({ ...createForm, name: event.target.value })} required />
          <FormField label="Subject" value={createForm.subject ?? ""} onChange={(event) => setCreateForm({ ...createForm, subject: event.target.value })} />
          <FormField label="Tenant ID" value={createForm.tenant_id ?? ""} onChange={(event) => setCreateForm({ ...createForm, tenant_id: event.target.value })} />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={createForm.is_active !== false} onChange={(event) => setCreateForm({ ...createForm, is_active: event.target.checked })} />
            Active service
          </label>
        </ResourceForm>
      </CreateResourceDialog>

      <EditResourceDialog open={Boolean(editService)} title="Edit service" description={editService?.subject ?? editService?.id} onClose={() => setEditService(null)}>
        <ResourceForm onSubmit={submitEdit} footer={<Button type="submit">Save service</Button>}>
          <FormField label="Name" value={editForm.name ?? ""} onChange={(event) => setEditForm({ ...editForm, name: event.target.value })} required />
          <FormField label="Subject" value={editForm.subject ?? ""} onChange={(event) => setEditForm({ ...editForm, subject: event.target.value })} />
          <label className="tigrbl-choice-row">
            <input type="checkbox" checked={editForm.is_active !== false} onChange={(event) => setEditForm({ ...editForm, is_active: event.target.checked })} />
            Active service
          </label>
        </ResourceForm>
      </EditResourceDialog>

      <ConfirmDialog
        open={Boolean(deleteService)}
        title="Delete service"
        body={`Delete ${deleteService?.name ?? deleteService?.subject ?? "this service"}?`}
        confirmLabel="Delete service"
        onCancel={() => setDeleteService(null)}
        onConfirm={() => {
          if (!deleteService) return;
          const serviceId = deleteService.id;
          setDeleteService(null);
          void runMutation(() => onDelete(serviceId), "Service deleted.");
        }}
      />
    </div>
  );
}
