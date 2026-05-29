import { AppShell, AuthProvider, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { useEffect, useState } from "react";
import { useDeveloperPortal } from "./hooks/useDeveloperPortal";
import { ApplicationDetailPage } from "./pages/ApplicationDetailPage";
import { ApplicationsPage } from "./pages/ApplicationsPage";
import { ClientCredentialsPage } from "./pages/ClientCredentialsPage";
import { ClientMetadataPage } from "./pages/ClientMetadataPage";
import { DashboardPage } from "./pages/DashboardPage";
import { DiscoveryPage } from "./pages/DiscoveryPage";
import { LoginPage } from "./pages/LoginPage";
import { OAuthFlowTesterPage } from "./pages/OAuthFlowTesterPage";
import { RedirectUrisPage } from "./pages/RedirectUrisPage";
import { ScopesPage } from "./pages/ScopesPage";
import { API_BASE_URL, PRODUCT_API } from "./services/backendSurface";

const navigation = [
  { href: "#/dashboard", label: "Dashboard" },
  { href: "#/apps", label: "Applications" },
  { href: "#/app-detail", label: "App Detail" },
  { href: "#/metadata", label: "Client Metadata" },
  { href: "#/redirects", label: "Redirect URIs" },
  { href: "#/credentials", label: "Credentials" },
  { href: "#/scopes", label: "Scopes" },
  { href: "#/oauth-test", label: "OAuth Tester" },
  { href: "#/discovery", label: "Discovery" }
];

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/dashboard");
  const developer = useDeveloperPortal();

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/dashboard");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/dashboard";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const authValue = {
    loading: developer.loading,
    logout: developer.logout,
    refresh: developer.refresh,
    session: developer.session
      ? {
          authenticated: developer.session.authenticated,
          email: developer.session.email,
          permissions: developer.session.roles,
          subject: developer.session.developer_id,
          tenantId: developer.session.tenant_id,
          username: developer.session.username
        }
      : null
  };

  const selectedApplication = developer.applications[0] ?? null;
  const selectedRegistration = developer.registrations[0] ?? null;

  return (
    <AuthProvider value={authValue}>
      <AppShell
        activeHref={currentHash}
        apiBaseUrl={API_BASE_URL}
        navigation={navigation}
        onLogout={developer.session?.authenticated ? () => developer.logout() : undefined}
        productApi={PRODUCT_API}
        sessionLabel={describeSession(authValue.session)}
        title="Developer Portal"
      >
        {!developer.session?.authenticated ? (
          <LoginPage error={developer.error} onLogin={developer.login} />
        ) : (
          <RequireAuth>
            {developer.error && <div style={{ marginBottom: "16px" }}><Toast message={developer.error} tone="danger" /></div>}
            {currentHash.startsWith("#/apps") && <ApplicationsPage applications={developer.applications} registrations={developer.registrations} />}
            {currentHash.startsWith("#/app-detail") && <ApplicationDetailPage application={selectedApplication} registration={selectedRegistration} />}
            {currentHash.startsWith("#/metadata") && <ClientMetadataPage registrations={developer.registrations} />}
            {currentHash.startsWith("#/redirects") && <RedirectUrisPage registrations={developer.registrations} />}
            {currentHash.startsWith("#/credentials") && <ClientCredentialsPage application={selectedApplication} registration={selectedRegistration} />}
            {currentHash.startsWith("#/scopes") && <ScopesPage applications={developer.applications} metadata={developer.metadata} />}
            {currentHash.startsWith("#/oauth-test") && <OAuthFlowTesterPage application={selectedApplication} metadata={developer.metadata} />}
            {currentHash.startsWith("#/discovery") && <DiscoveryPage metadata={developer.metadata} />}
            {(currentHash.startsWith("#/dashboard") || !navigation.some((item) => currentHash.startsWith(item.href))) && (
              <DashboardPage applications={developer.applications} metadata={developer.metadata} registrations={developer.registrations} session={developer.session} />
            )}
          </RequireAuth>
        )}
      </AppShell>
    </AuthProvider>
  );
}
