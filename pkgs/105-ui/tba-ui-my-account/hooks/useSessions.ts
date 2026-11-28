import { useEffect, useState } from "react";
import { myAccountClient } from "../services/myAccountClient";
import type { AccountSession } from "../types";

export function useSessions(enabled = true) {
  const [sessions, setSessions] = useState<AccountSession[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function refresh() {
    if (!enabled) {
      setSessions([]);
      return;
    }
    setLoading(true);
    setError(null);
    try {
      setSessions(await myAccountClient.sessions());
    } catch (error) {
      setError(error instanceof Error ? error.message : "Unable to load sessions");
    } finally {
      setLoading(false);
    }
  }

  async function revoke(sessionId: string) {
    await myAccountClient.revokeSession(sessionId);
    await refresh();
  }

  useEffect(() => {
    void refresh();
  }, [enabled]);

  return { sessions, error, loading, refresh, revoke };
}
