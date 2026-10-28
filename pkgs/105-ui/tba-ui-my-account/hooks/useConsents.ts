import { useEffect, useState } from "react";
import { myAccountClient } from "../services/myAccountClient";
import type { AuthorizedApp, Consent } from "../types";

export function useConsents(enabled = true) {
  const [apps, setApps] = useState<AuthorizedApp[]>([]);
  const [consents, setConsents] = useState<Consent[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function refresh() {
    if (!enabled) {
      setApps([]);
      setConsents([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      const [authorizedApps, consentRows] = await Promise.all([
        myAccountClient.authorizedApps(),
        myAccountClient.consents()
      ]);
      setApps(authorizedApps);
      setConsents(consentRows);
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to load authorized apps");
    } finally {
      setLoading(false);
    }
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
  }, [enabled]);

  return { apps, consents, error, loading, refresh, revokeApp, revokeConsent };
}
