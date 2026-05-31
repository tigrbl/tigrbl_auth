import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { IdentitiesPage } from "./IdentitiesPage";
import { TenantsPage } from "./TenantsPage";
import type { Identity, Tenant } from "../types";

const tenants: Tenant[] = [
  { id: "tenant-1", slug: "acme", name: "Acme", email: "ops@acme.test", is_active: true },
  { id: "tenant-2", slug: "paused", name: "Paused", email: "ops@paused.test", is_active: false }
];

const identities: Identity[] = [
  {
    id: "identity-1",
    tenant_id: "tenant-1",
    username: "alice",
    email: "alice@acme.test",
    is_active: true,
    is_admin: true,
    is_superuser: false,
    must_change_password: true,
    roles: ["tenant-admin"]
  }
];

describe("platform-admin CRUD pages", () => {
  it("renders tenant CRUD controls and selected tenant state", () => {
    const html = renderToStaticMarkup(
      <TenantsPage
        selectedTenantId="tenant-1"
        tenants={tenants}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onDisable={async () => undefined}
        onEnable={async () => undefined}
        onSelect={() => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create tenant");
    expect(html).toContain("Edit");
    expect(html).toContain("Enable");
    expect(html).toContain("Suspend");
    expect(html).toContain("Delete");
    expect(html).toContain("Selected");
  });

  it("renders identity CRUD controls scoped to the selected tenant", () => {
    const html = renderToStaticMarkup(
      <IdentitiesPage
        identities={identities}
        selectedTenantId="tenant-1"
        tenants={tenants}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onSelectTenant={() => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create identity");
    expect(html).toContain("alice@acme.test");
    expect(html).toContain("Edit");
    expect(html).toContain("Activate");
    expect(html).toContain("Suspend");
    expect(html).toContain("Delete");
  });
});
