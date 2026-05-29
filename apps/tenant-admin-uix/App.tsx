import { AppShell, AuthProvider, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { useEffect, useState } from "react";
import { useTenantAdmin } from "./hooks/useTenantAdmin";
import { AuditPage } from "./pages/AuditPage";
import { ClientsPage } from "./pages/ClientsPage";
import { ConsentsPage } from "./pages/ConsentsPage";
import { DashboardPage } from "./pages/DashboardPage";
import { GroupsRolesPage } from "./pages/GroupsRolesPage";
import { IdentitiesPage } from "./pages/IdentitiesPage";
import { KeyEventsPage } from "./pages/KeyEventsPage";
import { LoginPage } from "./pages/LoginPage";
import { SessionsPage } from "./pages/SessionsPage";
import { API_BASE_URL, PRODUCT_API } from "./services/backendSurface";

const navigation = [
  { href: "#/dashboard", label: "Dashboard" },
  { href: "#/identities", label: "Identities" },
  { href: "#/groups", label: "Groups / Roles" },
  { href: "#/clients", label: "Clients" },
  { href: "#/consents", label: "Consents" },
  { href: "#/sessions", label: "Sessions" },
  { href: "#/keys", label: "Key Events" },
  { href: "#/audit", label: "Audit" }
];

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/dashboard");
  const tenant = useTenantAdmin();

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/dashboard");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/dashboard";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const authValue = {
    loading: tenant.loading,
    logout: tenant.logout,
    refresh: tenant.refresh,
    session: tenant.session
      ? {
          authenticated: tenant.session.authenticated,
          email: tenant.session.email ?? undefined,
          permissions: tenant.session.roles ?? [],
          subject: tenant.session.user_id ?? undefined,
          tenantId: tenant.session.tenant_id ?? undefined,
          username: tenant.session.username ?? undefined
        }
      : null
  };

  return (
    <AuthProvider value={authValue}>
      <AppShell
        activeHref={currentHash}
        apiBaseUrl={API_BASE_URL}
        navigation={navigation}
        onLogout={tenant.session?.authenticated ? () => void tenant.logout() : undefined}
        productApi={PRODUCT_API}
        sessionLabel={describeSession(authValue.session)}
        title="Tenant Admin"
      >
        {!tenant.session?.authenticated ? (
          <LoginPage error={tenant.error} onLogin={tenant.login} />
        ) : (
          <RequireAuth>
            {tenant.error && <div style={{ marginBottom: "16px" }}><Toast message={tenant.error} tone="danger" /></div>}
            {currentHash.startsWith("#/identities") && <IdentitiesPage identities={tenant.identities} />}
            {currentHash.startsWith("#/groups") && <GroupsRolesPage identities={tenant.identities} />}
            {currentHash.startsWith("#/clients") && <ClientsPage clients={tenant.clients} />}
            {currentHash.startsWith("#/consents") && <ConsentsPage consents={tenant.consents} />}
            {currentHash.startsWith("#/sessions") && <SessionsPage session={tenant.session} />}
            {currentHash.startsWith("#/keys") && <KeyEventsPage keyEvents={tenant.keyEvents} />}
            {currentHash.startsWith("#/audit") && <AuditPage session={tenant.session} />}
            {(currentHash.startsWith("#/dashboard") || !navigation.some((item) => currentHash.startsWith(item.href))) && (
              <DashboardPage clients={tenant.clients} consents={tenant.consents} identities={tenant.identities} keyEvents={tenant.keyEvents} session={tenant.session} />
            )}
          </RequireAuth>
        )}
      </AppShell>
    </AuthProvider>
  );
}
