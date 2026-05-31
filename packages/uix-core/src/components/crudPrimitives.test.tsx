import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { Button } from "./Button";
import { CodeField } from "./CodeField";
import { DangerZone } from "./DangerZone";
import { DetailDrawer } from "./DetailDrawer";
import { CreateResourceDialog, EditResourceDialog } from "./ResourceDialogs";
import { ResourceTable } from "./ResourceTable";
import { ResourceToolbar } from "./ResourceToolbar";
import { SelectField } from "./SelectField";
import { ToggleField } from "./ToggleField";

describe("CRUD UIX primitives", () => {
  it("renders resource toolbar, table actions, and lifecycle panels", () => {
    const html = renderToStaticMarkup(
      <div>
        <ResourceToolbar createLabel="Create tenant" description="Manage tenant lifecycle." title="Tenants" onCreate={() => undefined} />
        <ResourceTable
          actions={[{ label: "Edit", onClick: () => undefined }, { label: "Suspend", onClick: () => undefined, tone: "danger" }]}
          columns={[{ header: "Name", key: "name", render: (item) => item.name }]}
          getRowKey={(item) => item.id}
          items={[{ id: "tenant-1", name: "Acme" }]}
        />
        <DangerZone action={<Button variant="danger">Delete</Button>}>Suspend or retire this resource.</DangerZone>
      </div>
    );

    expect(html).toContain("tigrbl-resource-toolbar");
    expect(html).toContain("Create tenant");
    expect(html).toContain("tigrbl-row-action-danger");
    expect(html).toContain("tigrbl-danger-zone");
  });

  it("renders dialogs, drawers, and structured fields", () => {
    const html = renderToStaticMarkup(
      <div>
        <CreateResourceDialog open title="Create resource" description="Create a new object." onClose={() => undefined}>
          Form body
        </CreateResourceDialog>
        <EditResourceDialog open title="Edit resource" onClose={() => undefined}>
          Edit body
        </EditResourceDialog>
        <DetailDrawer open title="Resource detail" onClose={() => undefined}>
          Detail body
        </DetailDrawer>
        <SelectField label="Status" defaultValue="active" options={[{ label: "Active", value: "active" }]} />
        <ToggleField checked label="Require approval" readOnly />
        <CodeField label="Metadata" value="{}" readOnly />
      </div>
    );

    expect(html).toContain("Create resource");
    expect(html).toContain("Edit resource");
    expect(html).toContain("tigrbl-drawer");
    expect(html).toContain("tigrbl-toggle-field");
    expect(html).toContain("tigrbl-code-field");
  });
});
