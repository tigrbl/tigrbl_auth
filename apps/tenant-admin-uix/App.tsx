import { AppShell, AuthProvider, AuthShell, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
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
      {!tenant.session?.authenticated ? (
        <AuthShell
          productApi={PRODUCT_API}
          subtitle="Use a tenant-scoped administrator session to manage identities, clients, consents, sessions, and audit posture."
          title="Tenant Admin"
        >
          <LoginPage error={tenant.error} onLogin={tenant.login} />
        </AuthShell>
      ) : (
        <AppShell
          activeHref={currentHash}
          apiBaseUrl={API_BASE_URL}
          navigation={navigation}
          onLogout={() => void tenant.logout()}
          productApi={PRODUCT_API}
          sessionLabel={describeSession(authValue.session)}
          title="Tenant Admin"
        >
          <RequireAuth>
            {tenant.error && <div style={{ marginBottom: "16px" }}><Toast message={tenant.error} tone="danger" /></div>}
            {currentHash.startsWith("#/identities") && (
              <IdentitiesPage
                identities={tenant.identities}
                onCreate={tenant.createIdentity}
                onDelete={tenant.deleteIdentity}
                onLock={tenant.lockIdentity}
                onUnlock={tenant.unlockIdentity}
                onUpdate={tenant.updateIdentity}
              />
            )}
            {currentHash.startsWith("#/groups") && <GroupsRolesPage identities={tenant.identities} />}
            {currentHash.startsWith("#/clients") && (
              <ClientsPage
                clients={tenant.clients}
                onCreate={tenant.createClient}
                onDelete={tenant.deleteClient}
                onUpdate={tenant.updateClient}
              />
            )}
            {currentHash.startsWith("#/consents") && <ConsentsPage consents={tenant.consents} onRevoke={tenant.revokeConsent} />}
            {currentHash.startsWith("#/sessions") && <SessionsPage session={tenant.session} />}
            {currentHash.startsWith("#/keys") && (
              <KeyEventsPage
                keyEvents={tenant.keyEvents}
                tenantId={tenant.session.tenant_id ?? undefined}
                onRotate={tenant.triggerKeyRotation}
              />
            )}
            {currentHash.startsWith("#/audit") && <AuditPage session={tenant.session} />}
            {(currentHash.startsWith("#/dashboard") || !navigation.some((item) => currentHash.startsWith(item.href))) && (
              <DashboardPage clients={tenant.clients} consents={tenant.consents} identities={tenant.identities} keyEvents={tenant.keyEvents} session={tenant.session} />
            )}
          </RequireAuth>
        </AppShell>
      )}
    </AuthProvider>
  );
}
