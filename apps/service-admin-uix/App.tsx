import { AppShell, AuthProvider, AuthShell, RequireAuth, Toast, describeSession } from "@tigrbl-auth/uix-core";
import "@tigrbl-auth/uix-core/styles.css";
import { useEffect, useState } from "react";
import { useServiceAdmin } from "./hooks/useServiceAdmin";
import { ApiKeysPage } from "./pages/ApiKeysPage";
import { AuditPage } from "./pages/AuditPage";
import { DashboardPage } from "./pages/DashboardPage";
import { LoginPage } from "./pages/LoginPage";
import { RotationEventsPage } from "./pages/RotationEventsPage";
import { ServiceDetailPage } from "./pages/ServiceDetailPage";
import { ServiceKeysPage } from "./pages/ServiceKeysPage";
import { ServicesPage } from "./pages/ServicesPage";
import { TokenRecordsPage } from "./pages/TokenRecordsPage";
import { ValidationToolsPage } from "./pages/ValidationToolsPage";
import { API_BASE_URL, PRODUCT_API } from "./services/backendSurface";

const navigation = [
  { href: "#/dashboard", label: "Dashboard" },
  { href: "#/services", label: "Services" },
  { href: "#/service-detail", label: "Service Detail" },
  { href: "#/service-keys", label: "Service Keys" },
  { href: "#/api-keys", label: "API Keys" },
  { href: "#/tokens", label: "Token Records" },
  { href: "#/validation", label: "Validation Tools" },
  { href: "#/rotation", label: "Rotation Events" },
  { href: "#/audit", label: "Audit" }
];

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/dashboard");
  const serviceAdmin = useServiceAdmin();

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/dashboard");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/dashboard";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  const authValue = {
    loading: serviceAdmin.loading,
    logout: serviceAdmin.logout,
    refresh: serviceAdmin.refresh,
    session: serviceAdmin.session
      ? {
          authenticated: serviceAdmin.session.authenticated,
          email: serviceAdmin.session.email,
          permissions: serviceAdmin.session.roles,
          subject: serviceAdmin.session.operator_id,
          tenantId: serviceAdmin.session.tenant_id,
          username: serviceAdmin.session.username
        }
      : null
  };

  const selectedService = serviceAdmin.services[0] ?? null;

  return (
    <AuthProvider value={authValue}>
      {!serviceAdmin.session?.authenticated ? (
        <AuthShell
          productApi={PRODUCT_API}
          subtitle="Use a workload administrator session to manage service principals, API keys, service keys, token records, and validation tools."
          title="Service Admin"
        >
          <LoginPage error={serviceAdmin.error} onLogin={serviceAdmin.login} />
        </AuthShell>
      ) : (
        <AppShell
          activeHref={currentHash}
          apiBaseUrl={API_BASE_URL}
          navigation={navigation}
          onLogout={() => serviceAdmin.logout()}
          productApi={PRODUCT_API}
          sessionLabel={describeSession(authValue.session)}
          title="Service Admin"
        >
          <RequireAuth>
            {serviceAdmin.error && <div style={{ marginBottom: "16px" }}><Toast message={serviceAdmin.error} tone="danger" /></div>}
            {currentHash.startsWith("#/services") && (
              <ServicesPage
                services={serviceAdmin.services}
                onCreate={serviceAdmin.createService}
                onDelete={serviceAdmin.deleteService}
                onUpdate={serviceAdmin.updateService}
              />
            )}
            {currentHash.startsWith("#/service-detail") && <ServiceDetailPage service={selectedService} serviceKeys={serviceAdmin.serviceKeys} apiKeys={serviceAdmin.apiKeys} />}
            {currentHash.startsWith("#/service-keys") && (
              <ServiceKeysPage
                services={serviceAdmin.services}
                serviceKeys={serviceAdmin.serviceKeys}
                onCreate={serviceAdmin.createServiceKey}
                onRevoke={serviceAdmin.revokeServiceKey}
              />
            )}
            {currentHash.startsWith("#/api-keys") && (
              <ApiKeysPage
                apiKeys={serviceAdmin.apiKeys}
                services={serviceAdmin.services}
                onCreate={serviceAdmin.createApiKey}
                onRevoke={serviceAdmin.revokeApiKey}
                onUpdate={serviceAdmin.updateApiKey}
              />
            )}
            {currentHash.startsWith("#/tokens") && <TokenRecordsPage tokenRecords={serviceAdmin.tokenRecords} />}
            {currentHash.startsWith("#/validation") && (
              <ValidationToolsPage
                introspection={serviceAdmin.introspection}
                metadata={serviceAdmin.metadata}
                onIntrospect={serviceAdmin.runIntrospection}
              />
            )}
            {currentHash.startsWith("#/rotation") && <RotationEventsPage serviceKeys={serviceAdmin.serviceKeys} />}
            {currentHash.startsWith("#/audit") && <AuditPage session={serviceAdmin.session} />}
            {(currentHash.startsWith("#/dashboard") || !navigation.some((item) => currentHash.startsWith(item.href))) && (
              <DashboardPage
                apiKeys={serviceAdmin.apiKeys}
                metadata={serviceAdmin.metadata}
                serviceKeys={serviceAdmin.serviceKeys}
                services={serviceAdmin.services}
                session={serviceAdmin.session}
                tokenRecords={serviceAdmin.tokenRecords}
              />
            )}
          </RequireAuth>
        </AppShell>
      )}
    </AuthProvider>
  );
}
