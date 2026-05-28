import { useEffect, useState } from "react";
import { myAccountClient } from "../services/myAccountClient";
import type { AuthorizedApp, Consent } from "../types";

export function useConsents() {
  const [apps, setApps] = useState<AuthorizedApp[]>([]);
  const [consents, setConsents] = useState<Consent[]>([]);

  async function refresh() {
    const [authorizedApps, consentRows] = await Promise.all([
      myAccountClient.authorizedApps(),
      myAccountClient.consents()
    ]);
    setApps(authorizedApps);
    setConsents(consentRows);
  }

  async function revokeApp(clientId: string) {
    await myAccountClient.revokeAuthorizedApp(clientId);
    await refresh();
  }

  async function revokeConsent(consentId: string) {
    await myAccountClient.revokeConsent(consentId);
    await refresh();
  }

  useEffect(() => {
    void refresh();
  }, []);

  return { apps, consents, refresh, revokeApp, revokeConsent };
}
