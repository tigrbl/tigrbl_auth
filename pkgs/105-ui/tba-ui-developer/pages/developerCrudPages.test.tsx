import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { ApplicationsPage } from "./ApplicationsPage";
import { ClientMetadataPage } from "./ClientMetadataPage";
import { RedirectUrisPage } from "./RedirectUrisPage";
import type { ClientRegistration, DeveloperApplication } from "../types";

const applications: DeveloperApplication[] = [
  {
    id: "app-1",
    client_id: "portal",
    name: "Portal",
    redirect_uris: ["https://app.example.test/callback"]
  }
];

const registrations: ClientRegistration[] = [
  {
    id: "reg-1",
    client_id: "portal",
    client_name: "Portal",
    redirect_uris: ["https://app.example.test/callback"],
    token_endpoint_auth_method: "client_secret_basic"
  }
];

describe("developer UIX CRUD pages", () => {
  it("renders application registration, edit, and delete controls", () => {
    const html = renderToStaticMarkup(
      <ApplicationsPage
        applications={applications}
        registrations={registrations}
        onCreate={async () => undefined}
        onDeleteApplication={async () => undefined}
        onDeleteRegistration={async () => undefined}
        onUpdateApplication={async () => undefined}
        onUpdateRegistration={async () => undefined}
      />
    );

    expect(html).toContain("Register application");
    expect(html).toContain("Portal");
    expect(html).toContain("Edit");
    expect(html).toContain("Delete");
  });

  it("renders client metadata edit and delete controls", () => {
    const html = renderToStaticMarkup(
      <ClientMetadataPage registrations={registrations} onDelete={async () => undefined} onUpdate={async () => undefined} />
    );

    expect(html).toContain("client_secret_basic");
    expect(html).toContain("Edit");
    expect(html).toContain("Delete");
  });

  it("renders redirect URI edit controls", () => {
    const html = renderToStaticMarkup(<RedirectUrisPage registrations={registrations} onUpdate={async () => undefined} />);

    expect(html).toContain("https://app.example.test/callback");
    expect(html).toContain("Edit client URIs");
  });
});
