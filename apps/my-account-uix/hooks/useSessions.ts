import { useEffect, useState } from "react";
import { myAccountClient } from "../services/myAccountClient";
import type { AccountSession } from "../types";

export function useSessions() {
  const [sessions, setSessions] = useState<AccountSession[]>([]);

  async function refresh() {
    setSessions(await myAccountClient.sessions());
  }

  async function revoke(sessionId: string) {
    await myAccountClient.revokeSession(sessionId);
    await refresh();
  }

  useEffect(() => {
    void refresh();
  }, []);

  return { sessions, refresh, revoke };
}
