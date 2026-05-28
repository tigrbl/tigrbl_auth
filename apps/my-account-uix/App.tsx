import { useEffect, useState } from "react";
import { Layout } from "./components/Layout";
import { useConsents } from "./hooks/useConsents";
import { useMyAccount } from "./hooks/useMyAccount";
import { useSessions } from "./hooks/useSessions";
import { AuthorizedAppsPage } from "./pages/AuthorizedAppsPage";
import { ProfilePage } from "./pages/ProfilePage";
import { SecurityPage } from "./pages/SecurityPage";
import { SessionsPage } from "./pages/SessionsPage";

export default function App() {
  const [currentHash, setCurrentHash] = useState(window.location.hash || "#/profile");
  const account = useMyAccount();
  const sessions = useSessions();
  const consents = useConsents();

  useEffect(() => {
    const onHashChange = () => setCurrentHash(window.location.hash || "#/profile");
    window.addEventListener("hashchange", onHashChange);
    if (!window.location.hash || window.location.hash === "#/") {
      window.location.hash = "#/profile";
    }
    return () => window.removeEventListener("hashchange", onHashChange);
  }, []);

  let content = null;
  if (account.loading) {
    content = <p>Loading account...</p>;
  } else if (account.error) {
    content = <p style={{ color: "#7f1d1d" }}>{account.error}</p>;
  } else if (!account.profile) {
    content = <p>Account session required.</p>;
  } else if (currentHash.startsWith("#/security")) {
    content = (
      <SecurityPage
        mustChangePassword={account.profile.must_change_password}
        onChangePassword={account.changePassword}
      />
    );
  } else if (currentHash.startsWith("#/sessions")) {
    content = <SessionsPage sessions={sessions.sessions} onRevoke={sessions.revoke} />;
  } else if (currentHash.startsWith("#/apps")) {
    content = (
      <AuthorizedAppsPage
        apps={consents.apps}
        consents={consents.consents}
        onRevokeApp={consents.revokeApp}
        onRevokeConsent={consents.revokeConsent}
      />
    );
  } else {
    content = <ProfilePage profile={account.profile} onSave={account.updateProfile} />;
  }

  return <Layout currentHash={currentHash}>{content}</Layout>;
}
