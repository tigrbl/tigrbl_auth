import { AppShell, AuthProvider, AuthShell, Button, Card, ErrorState, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { useEffect, useState } from "react";
import { API_BASE_URL, PRODUCT_API, PUBLIC_LOGIN_URL } from "./defaults";
import { useConsents } from "./hooks/useConsents";
import { useMyAccount } from "./hooks/useMyAccount";
import { useSessions } from "./hooks/useSessions";
import { AuthorizedAppsPage } from "./pages/AuthorizedAppsPage";
import { OverviewPage } from "./pages/OverviewPage";
import { ProfilePage } from "./pages/ProfilePage";
import { SecurityPage } from "./pages/SecurityPage";
import { SessionsPage } from "./pages/SessionsPage";

const navigation = [
  { href: "#/overview", label: "Overview" },
  { href: "#/profile", label: "Profile" },
  { href: "#/security", label: "Security" },
  { href: "#/sessions", label: "Sessions" },
  { href: "#/apps", label: "Authorized Apps" }
];

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/overview");
  const account = useMyAccount();
  const sessions = useSessions(Boolean(account.profile));
  const consents = useConsents(Boolean(account.profile));

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/overview");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/overview";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const authValue = {
    loading: account.loading,
    refresh: account.refresh,
    session: account.profile
      ? {
          authenticated: true,
          email: account.profile.email,
          permissions: account.profile.roles,
          subject: account.profile.id,
          tenantId: account.profile.tenant_id,
          username: account.profile.username
        }
      : null
  };

  let content = null;
  if (account.loading) {
    content = <Toast message="Loading account..." tone="info" />;
  } else if (account.profile && currentHash.startsWith("#/security")) {
    content = (
      <SecurityPage
        mustChangePassword={account.profile.must_change_password}
        onChangePassword={account.changePassword}
      />
    );
  } else if (account.profile && currentHash.startsWith("#/sessions")) {
    content = <SessionsPage sessions={sessions.sessions} error={sessions.error} loading={sessions.loading} onRevoke={sessions.revoke} />;
  } else if (account.profile && currentHash.startsWith("#/apps")) {
    content = (
      <AuthorizedAppsPage
        apps={consents.apps}
        consents={consents.consents}
        error={consents.error}
        loading={consents.loading}
        onRevokeApp={consents.revokeApp}
        onRevokeConsent={consents.revokeConsent}
      />
    );
  } else if (account.profile && currentHash.startsWith("#/profile")) {
    content = <ProfilePage profile={account.profile} onSave={account.updateProfile} />;
  } else if (account.profile) {
    content = (
      <OverviewPage
        apps={consents.apps}
        consents={consents.consents}
        profile={account.profile}
        sessions={sessions.sessions}
      />
    );
  }

  return (
    <AuthProvider value={authValue}>
      {!account.profile && !account.loading ? (
        <AuthShell
          productApi={PRODUCT_API}
          subtitle="Use the public issuer session to manage your profile, sessions, passwords, authorized apps, and consent grants."
          title="My Account"
        >
          <Card tone="hero">
            <div className="tigrbl-page-stack">
              <ErrorState
                title="Account session required"
                message={account.error ?? "Sign in through the public hosted-login surface before using My Account."}
              />
              <div className="tigrbl-actions">
                <Button type="button" onClick={() => { window.location.href = PUBLIC_LOGIN_URL; }}>
                  Continue to hosted login
                </Button>
                <Button type="button" variant="subtle" onClick={() => void account.refresh()}>
                  Retry account session
                </Button>
              </div>
            </div>
          </Card>
        </AuthShell>
      ) : (
        <AppShell
          activeHref={currentHash}
          apiBaseUrl={API_BASE_URL}
          navigation={navigation}
          productApi={PRODUCT_API}
          sessionLabel={describeSession(authValue.session)}
          title="My Account"
        >
          {account.profile ? <RequireAuth>{content}</RequireAuth> : content}
        </AppShell>
      )}
    </AuthProvider>
  );
}
