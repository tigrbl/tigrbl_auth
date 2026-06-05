import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { IdentitiesPage } from "./IdentitiesPage";
import { RealmsPage } from "./RealmsPage";
import { TenantsPage } from "./TenantsPage";
import type { Identity, Realm, Tenant } from "../types";

const tenants: Tenant[] = [
  { id: "12345678-tenant-0000-0000-00000000abcd", slug: "acme", name: "Acme", email: "ops@acme.test", is_active: true },
  { id: "tenant-2", slug: "paused", name: "Paused", email: "ops@paused.test", is_active: false }
];

const realms: Realm[] = [
  { id: "12345678-realm-0000-0000-00000000abcd", slug: "demo", name: "Demo", issuer_path: "/demo" }
];

const identities: Identity[] = [
  {
    id: "12345678-identity-0000-0000-00000000abcd",
    tenant_id: "12345678-tenant-0000-0000-00000000abcd",
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
  it("renders realm links with truncated copyable identifiers", () => {
    const html = renderToStaticMarkup(
      <RealmsPage
        selectedRealmId="12345678-realm-0000-0000-00000000abcd"
        realms={realms}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onSelect={() => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
    expect(html).toContain("Demo");
  });

  it("renders tenant CRUD controls and selected tenant state", () => {
    const html = renderToStaticMarkup(
      <TenantsPage
        selectedTenantId="12345678-tenant-0000-0000-00000000abcd"
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
    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
  });

  it("renders identity CRUD controls scoped to the selected tenant", () => {
    const html = renderToStaticMarkup(
      <IdentitiesPage
        identities={identities}
        selectedIdentityId="12345678-identity-0000-0000-00000000abcd"
        selectedTenantId="12345678-tenant-0000-0000-00000000abcd"
        tenants={tenants}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onSelect={() => undefined}
        onSelectTenant={() => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create identity");
    expect(html).toContain("Selected identity");
    expect(html).toContain("alice@acme.test");
    expect(html).toContain("Edit");
    expect(html).toContain("Activate");
    expect(html).toContain("Suspend");
    expect(html).toContain("Delete");
    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
  });
});
