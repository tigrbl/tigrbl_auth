import { renderToStaticMarkup } from "react-dom/server";
import { describe, expect, it } from "vitest";
import { AuthorizedAppsPage } from "./AuthorizedAppsPage";
import { ProfilePage } from "./ProfilePage";
import { SecurityPage } from "./SecurityPage";
import { SessionsPage } from "./SessionsPage";
import type { AccountProfile, AccountSession, AuthorizedApp, Consent } from "../types";

const profile: AccountProfile = {
  id: "subject-1",
  tenant_id: "tenant-1",
  username: "alice",
  email: "alice@example.test",
  is_active: true,
  must_change_password: false,
  roles: ["user"]
};

const sessions: AccountSession[] = [
  {
    id: "session-1",
    tenant_id: "tenant-1",
    user_id: "subject-1",
    username: "alice",
    client_id: "portal",
    state: "active"
  }
];

const apps: AuthorizedApp[] = [
  {
    client_id: "portal",
    tenant_id: "tenant-1",
    scope: "openid profile",
    consent_state: "granted"
  }
];

const consents: Consent[] = [
  {
    id: "consent-1",
    tenant_id: "tenant-1",
    user_id: "subject-1",
    client_id: "portal",
    scope: "openid profile",
    state: "granted"
  }
];

describe("my-account self-service pages", () => {
  it("renders profile update controls", () => {
    const html = renderToStaticMarkup(<ProfilePage profile={profile} onSave={async () => undefined} />);

    expect(html).toContain("Save profile");
    expect(html).toContain("alice@example.test");
    expect(html).toContain("subject-1");
  });

  it("renders password change controls", () => {
    const html = renderToStaticMarkup(<SecurityPage mustChangePassword={false} onChangePassword={async () => undefined} />);

    expect(html).toContain("Password current");
    expect(html).toContain("Change password");
    expect(html).toContain("Current password");
    expect(html).toContain("New password");
  });

  it("renders session revoke controls with confirmation-oriented action text", () => {
    const html = renderToStaticMarkup(
      <SessionsPage sessions={sessions} loading={false} onRevoke={async () => undefined} />
    );

    expect(html).toContain("Visible sessions");
    expect(html).toContain("session-1");
    expect(html).toContain("Revoke");
  });

  it("renders authorized app and consent revoke controls", () => {
    const html = renderToStaticMarkup(
      <AuthorizedAppsPage
        apps={apps}
        consents={consents}
        loading={false}
        onRevokeApp={async () => undefined}
        onRevokeConsent={async () => undefined}
      />
    );

    expect(html).toContain("Applications");
    expect(html).toContain("Revoke app");
    expect(html).toContain("Revoke consent");
    expect(html).toContain("consent-1");
  });
});
