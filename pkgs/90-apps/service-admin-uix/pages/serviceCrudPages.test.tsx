import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { ApiKeysPage } from "./ApiKeysPage";
import { ServiceKeysPage } from "./ServiceKeysPage";
import { ServicesPage } from "./ServicesPage";
import type { ApiKeyRecord, ServiceIdentity, ServiceKey } from "../types";

const services: ServiceIdentity[] = [
  { id: "service-1", name: "Orders", subject: "svc:orders", tenant_id: "tenant-1", is_active: true }
];

const serviceKeys: ServiceKey[] = [
  { id: "key-1", kid: "orders-key-1", service_id: "service-1", status: "active" }
];

const apiKeys: ApiKeyRecord[] = [
  { id: "api-key-1", name: "Deploy", service_id: "service-1", scopes: ["orders:read"], status: "active" }
];

describe("service-admin CRUD pages", () => {
  it("renders service identity CRUD controls", () => {
    const html = renderToStaticMarkup(
      <ServicesPage
        services={services}
        onCreate={async () => undefined}
        onDelete={async () => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create service");
    expect(html).toContain("Orders");
    expect(html).toContain("Edit");
    expect(html).toContain("Activate");
    expect(html).toContain("Suspend");
    expect(html).toContain("Delete");
  });

  it("renders service key create and revoke controls", () => {
    const html = renderToStaticMarkup(
      <ServiceKeysPage
        services={services}
        serviceKeys={serviceKeys}
        onCreate={async () => undefined}
        onRevoke={async () => undefined}
      />
    );

    expect(html).toContain("Create service key");
    expect(html).toContain("orders-key-1");
    expect(html).toContain("Revoke");
  });

  it("renders API key create, edit, and revoke controls", () => {
    const html = renderToStaticMarkup(
      <ApiKeysPage
        apiKeys={apiKeys}
        services={services}
        onCreate={async () => undefined}
        onRevoke={async () => undefined}
        onUpdate={async () => undefined}
      />
    );

    expect(html).toContain("Create API key");
    expect(html).toContain("Deploy");
    expect(html).toContain("Edit");
    expect(html).toContain("Revoke");
  });
});
