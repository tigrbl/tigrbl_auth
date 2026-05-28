import { useEffect, useState } from "react";
import { Layout } from "./components/Layout";
import { Notice } from "./components/UI";
import { usePlatformAdmin } from "./hooks/usePlatformAdmin";
import { AuditPage } from "./pages/AuditPage";
import { IdentitiesPage } from "./pages/IdentitiesPage";
import { LoginPage } from "./pages/LoginPage";
import { TenantsPage } from "./pages/TenantsPage";

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/tenants");
  const platform = usePlatformAdmin();

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/tenants");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/tenants";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  if (platform.loading) {
    return (
      <Layout currentHash={currentHash} session={platform.session} onLogout={() => void platform.logout()}>
        <p>Loading platform console...</p>
      </Layout>
    );
  }

  if (!platform.session?.authenticated) {
    return (
      <Layout currentHash={currentHash} session={platform.session} onLogout={() => void platform.logout()}>
        <LoginPage error={platform.error} onLogin={platform.login} />
      </Layout>
    );
  }

  let content = null;
  if (currentHash.startsWith("#/identities")) {
    content = (
      <IdentitiesPage
        identities={platform.identities}
        onCreate={platform.createIdentity}
        onSelectTenant={platform.setSelectedTenantId}
        selectedTenantId={platform.selectedTenantId}
        tenants={platform.tenants}
      />
    );
  } else if (currentHash.startsWith("#/audit")) {
    content = <AuditPage session={platform.session} tenants={platform.tenants} />;
  } else {
    content = (
      <TenantsPage
        selectedTenantId={platform.selectedTenantId}
        tenants={platform.tenants}
        onCreate={platform.createTenant}
        onDelete={platform.deleteTenant}
        onSelect={platform.setSelectedTenantId}
      />
    );
  }

  return (
    <Layout currentHash={currentHash} session={platform.session} onLogout={() => void platform.logout()}>
      {platform.error && <div style={{ marginBottom: "16px" }}><Notice tone="error">{platform.error}</Notice></div>}
      {content}
    </Layout>
  );
}
