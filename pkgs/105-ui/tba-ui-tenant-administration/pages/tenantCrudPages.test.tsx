import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { ClientsPage } from "./ClientsPage";
import { ConsentsPage } from "./ConsentsPage";
import { IdentitiesPage } from "./IdentitiesPage";
import { KeyEventsPage } from "./KeyEventsPage";
import type { KeyRotationEvent, TenantClient, TenantConsent, TenantIdentity } from "../types";

const identities: TenantIdentity[] = [
  {
    id: "identity-1",
    username: "alice",
    email: "alice@example.test",
    is_active: true,
    is_admin: true,
    must_change_password: true,
    roles: ["tenant-admin"]
  }
];

const clients: TenantClient[] = [
  {
    id: "client-1",
    client_id: "portal",
    name: "Portal",
    redirect_uris: ["https://app.example.test/callback"],
    grant_types: ["authorization_code"]
  }
];

const consents: TenantConsent[] = [
  { id: "consent-1", client_id: "portal", user_id: "identity-1", scopes: ["openid", "profile"] }
];

const keyEvents: KeyRotationEvent[] = [
  { id: "event-1", tenant_id: "tenant-1", status: "recorded", created_at: "2026-05-31T00:00:00Z" }
];

describe("tenant-admin CRUD pages", () => {
  it("renders identity mutation controls", () => {
    const html = renderToStaticMarkup(
      <IdentitiesPage
        identities={identities}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onLock={async () => undefined}
        onUnlock={async () => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create identity");
    expect(html).toContain("alice@example.test");
    expect(html).toContain("Edit");
    expect(html).toContain("Unlock");
    expect(html).toContain("Lock");
    expect(html).toContain("Delete");
  });

  it("renders client mutation controls", () => {
    const html = renderToStaticMarkup(
      <ClientsPage
        clients={clients}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create client");
    expect(html).toContain("Portal");
    expect(html).toContain("Edit");
    expect(html).toContain("Delete");
  });

  it("renders consent revoke controls", () => {
    const html = renderToStaticMarkup(<ConsentsPage consents={consents} onRevoke={async () => undefined} />);

    expect(html).toContain("portal");
    expect(html).toContain("Granted");
    expect(html).toContain("Revoke");
  });

  it("renders tenant key rotation request controls", () => {
    const html = renderToStaticMarkup(
      <KeyEventsPage keyEvents={keyEvents} tenantId="tenant-1" onRotate={async () => undefined} />
    );

    expect(html).toContain("Request rotation");
    expect(html).toContain("event-1");
    expect(html).toContain("tenant-1");
  });
});
