import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { IdentitiesPage } from "./IdentitiesPage";
import { RealmsPage } from "./RealmsPage";
import { IdentityMemberPage, RealmMemberPage, TenantMemberPage } from "./ResourceMemberPages";
import { TenantsPage } from "./TenantsPage";
import type { Identity, Realm, Tenant } from "../types";

const tenants: Tenant[] = [
  {
    id: "12345678-tenant-0000-0000-00000000abcd",
    realm_id: "12345678-realm-0000-0000-00000000abcd",
    slug: "acme",
    name: "Acme",
    email: "ops@acme.test",
    is_active: true
  },
  {
    id: "87654321-tenant-0000-0000-00000000dcba",
    realm_id: "87654321-realm-0000-0000-00000000dcba",
    slug: "paused",
    name: "Paused",
    email: "ops@paused.test",
    is_active: false
  }
];

const realms: Realm[] = [
  { id: "12345678-realm-0000-0000-00000000abcd", slug: "demo", name: "Demo", issuer_path: "/demo" },
  { id: "87654321-realm-0000-0000-00000000dcba", slug: "external", name: "External", issuer_path: "/external" }
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
  },
  {
    id: "87654321-identity-0000-0000-00000000dcba",
    tenant_id: "87654321-tenant-0000-0000-00000000dcba",
    username: "mallory",
    email: "mallory@paused.test",
    is_active: true,
    is_admin: true,
    is_superuser: false,
    must_change_password: false,
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

  it("renders realm member routes without the realms collection", () => {
    const html = renderToStaticMarkup(
      <RealmMemberPage
        identities={identities}
        realmId="12345678-realm-0000-0000-00000000abcd"
        realms={realms}
        tenants={tenants}
      />
    );

    expect(html).toContain("Realm details");
    expect(html).toContain("Tenants in realm");
    expect(html).toContain("Realm administrators");
    expect(html).toContain("1 active / 0 suspended");
    expect(html).toContain("Acme");
    expect(html).toContain("alice@acme.test");
    expect(html).toContain("#/tenants/12345678-tenant-0000-0000-00000000abcd");
    expect(html).toContain("#/identities/12345678-identity-0000-0000-00000000abcd");
    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
    expect(html).not.toContain("Platform realms");
    expect(html).not.toContain("Create realm");
  });

  it("does not leak tenants or administrators from other realms on realm member routes", () => {
    const html = renderToStaticMarkup(
      <RealmMemberPage
        identities={identities}
        realmId="12345678-realm-0000-0000-00000000abcd"
        realms={realms}
        tenants={tenants}
      />
    );

    expect(html).toContain("Acme");
    expect(html).toContain("alice@acme.test");
    expect(html).not.toContain("Paused");
    expect(html).not.toContain("mallory@paused.test");
  });

  it("renders tenant member routes without the tenants collection", () => {
    const html = renderToStaticMarkup(
      <TenantMemberPage
        identities={identities}
        realms={realms}
        tenantId="12345678-tenant-0000-0000-00000000abcd"
        tenants={tenants}
      />
    );

    expect(html).toContain("Tenant details");
    expect(html).toContain("Tenant administrators");
    expect(html).toContain("Identities in tenant");
    expect(html).toContain("#/realms/12345678-realm-0000-0000-00000000abcd");
    expect(html).toContain("#/identities/12345678-identity-0000-0000-00000000abcd");
    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
    expect(html).not.toContain("Platform tenants");
    expect(html).not.toContain("Create tenant");
  });

  it("does not leak identities from other tenants on tenant member routes", () => {
    const html = renderToStaticMarkup(
      <TenantMemberPage
        identities={identities}
        realms={realms}
        tenantId="12345678-tenant-0000-0000-00000000abcd"
        tenants={tenants}
      />
    );

    expect(html).toContain("alice@acme.test");
    expect(html).not.toContain("mallory@paused.test");
  });

  it("renders identity member routes without the identities collection", () => {
    const html = renderToStaticMarkup(
      <IdentityMemberPage
        identities={identities}
        identityId="12345678-identity-0000-0000-00000000abcd"
        realms={realms}
        tenants={tenants}
      />
    );

    expect(html).toContain("Identity details");
    expect(html).toContain("Assigned roles");
    expect(html).toContain("#/tenants/12345678-tenant-0000-0000-00000000abcd");
    expect(html).toContain("#/realms/12345678-realm-0000-0000-00000000abcd");
    expect(html).toContain("tenant-admin");
    expect(html).toContain("12345678...abcd");
    expect(html).toContain("Copy full ID");
    expect(html).not.toContain("Tenant identities");
    expect(html).not.toContain("Create identity");
  });

  it("renders not-found recovery for unknown identity member routes", () => {
    const html = renderToStaticMarkup(
      <IdentityMemberPage
        identities={identities}
        identityId="ffffffff-identity-0000-0000-00000000ffff"
        realms={realms}
        tenants={tenants}
      />
    );

    expect(html).toContain("Not found");
    expect(html).toContain("The requested row is not visible to this platform session.");
    expect(html).toContain("#/identities");
    expect(html).toContain("ffffffff...ffff");
  });
});
