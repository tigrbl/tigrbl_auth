import { useEffect, useMemo, useState } from "react";
import { AppShell, AuthProvider, AuthShell, ErrorState, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { usePlatformAdmin } from "./hooks/usePlatformAdmin";
import { AuditPage } from "./pages/AuditPage";
import { AuthorityPage } from "./pages/AuthorityPage";
import { DashboardPage } from "./pages/DashboardPage";
import { IdentitiesPage } from "./pages/IdentitiesPage";
import { KeyRotationPage } from "./pages/KeyRotationPage";
import { LoginPage } from "./pages/LoginPage";
import { RealmsPage } from "./pages/RealmsPage";
import { SettingsPage } from "./pages/SettingsPage";
import { TenantsPage } from "./pages/TenantsPage";
import { API_BASE_URL, PRODUCT_API } from "./services/backendSurface";

const navigation = [
  { href: "#/dashboard", label: "Dashboard" },
  { href: "#/realms", label: "Realms" },
  { href: "#/tenants", label: "Tenants" },
  { href: "#/identities", label: "Identities" },
  { href: "#/authority", label: "Authority" },
  { href: "#/keys", label: "Key Rotation" },
  { href: "#/audit", label: "Audit" },
  { href: "#/settings", label: "Settings" }
];

function routeSegments(hash: string) {
  return hash.replace(/^#/, "").split("/").filter(Boolean).map((segment) => decodeURIComponent(segment));
}

function navigateToResource(resource: "realms" | "tenants" | "identities", id: string) {
  window.location.hash = `#/${resource}/${encodeURIComponent(id)}`;
}

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/dashboard");
  const platform = usePlatformAdmin();
  const segments = useMemo(() => routeSegments(currentHash), [currentHash]);
  const [resource, resourceId] = segments;

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/dashboard");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/dashboard";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  useEffect(() => {
    if (currentHash.startsWith("#/tenant-detail")) {
      window.location.hash = platform.selectedTenantId ? `#/tenants/${encodeURIComponent(platform.selectedTenantId)}` : "#/tenants";
    }
  }, [currentHash, platform.selectedTenantId]);

  useEffect(() => {
    if (resource === "realms" && resourceId && platform.realms.some((realm) => realm.id === resourceId)) {
      platform.setSelectedRealmId(resourceId);
    }
  }, [platform.realms, platform.setSelectedRealmId, resource, resourceId]);

  useEffect(() => {
    if (resource === "tenants" && resourceId && platform.tenants.some((tenant) => tenant.id === resourceId)) {
      platform.setSelectedTenantId(resourceId);
    }
  }, [platform.setSelectedTenantId, platform.tenants, resource, resourceId]);

  const authValue = {
    loading: platform.loading,
    logout: platform.logout,
    refresh: platform.refresh,
    session: platform.session
      ? {
          authenticated: platform.session.authenticated,
          email: platform.session.email ?? undefined,
          permissions: platform.session.roles,
          subject: platform.session.user_id ?? undefined,
          tenantId: platform.session.tenant_id ?? undefined,
          username: platform.session.username ?? undefined
        }
      : null
  };

  const selectedTenant = platform.tenants.find((tenant) => tenant.id === platform.selectedTenantId) ?? null;
  const selectedIdentityId = resource === "identities" ? resourceId : undefined;

  return (
    <AuthProvider value={authValue}>
      {!platform.session?.authenticated ? (
        <AuthShell
          productApi={PRODUCT_API}
          subtitle="Use an operator session to manage tenant lifecycle, platform authority, signing posture, and audit state."
          title="Platform Admin"
        >
          <LoginPage error={platform.error} onLogin={platform.login} />
        </AuthShell>
      ) : (
        <AppShell
          activeHref={currentHash}
          apiBaseUrl={API_BASE_URL}
          navigation={navigation}
          onLogout={() => void platform.logout()}
          productApi={PRODUCT_API}
          sessionLabel={describeSession(authValue.session)}
          title="Platform Admin"
        >
          <RequireAuth>
            {platform.error && <div style={{ marginBottom: "16px" }}><Toast message={platform.error} tone="danger" /></div>}
            {currentHash.startsWith("#/tenants") && (
              <TenantsPage
                realms={platform.realms}
                selectedRealmId={platform.selectedRealmId}
                selectedTenantId={platform.selectedTenantId}
                tenants={platform.tenants}
                onCreate={platform.createTenant}
                onDelete={platform.deleteTenant}
                onDisable={platform.disableTenant}
                onEnable={platform.enableTenant}
                onSelect={(tenantId) => {
                  platform.setSelectedTenantId(tenantId);
                  navigateToResource("tenants", tenantId);
                }}
                onUpdate={platform.updateTenant}
              />
            )}
            {currentHash.startsWith("#/realms") && (
              <RealmsPage
                realms={platform.realms}
                selectedRealmId={platform.selectedRealmId}
                onCreate={platform.createRealm}
                onDelete={platform.deleteRealm}
                onSelect={(realmId) => {
                  platform.setSelectedRealmId(realmId);
                  navigateToResource("realms", realmId);
                }}
                onUpdate={platform.updateRealm}
              />
            )}
            {currentHash.startsWith("#/identities") && (
              <IdentitiesPage
                identities={platform.identities}
                onCreate={platform.createIdentity}
                onDelete={platform.deleteIdentity}
                onSelect={(identityId) => navigateToResource("identities", identityId)}
                onSelectTenant={platform.setSelectedTenantId}
                onUpdate={platform.updateIdentity}
                selectedIdentityId={selectedIdentityId}
                selectedTenantId={platform.selectedTenantId}
                tenants={platform.tenants}
              />
            )}
            {currentHash.startsWith("#/authority") && (
              <AuthorityPage identities={platform.identities} selectedTenant={selectedTenant} tenants={platform.tenants} />
            )}
            {currentHash.startsWith("#/keys") && (
              <KeyRotationPage selectedTenant={selectedTenant} tenants={platform.tenants} />
            )}
            {currentHash.startsWith("#/audit") && <AuditPage session={platform.session} tenants={platform.tenants} />}
            {currentHash.startsWith("#/settings") && <SettingsPage session={platform.session} />}
            {(currentHash.startsWith("#/dashboard") || !navigation.some((item) => currentHash.startsWith(item.href))) && (
              <DashboardPage identities={platform.identities} session={platform.session} tenants={platform.tenants} />
            )}
          </RequireAuth>
          {platform.loading && <ErrorState title="Refreshing platform data" message="The platform console is loading the latest state." />}
        </AppShell>
      )}
    </AuthProvider>
  );
}
