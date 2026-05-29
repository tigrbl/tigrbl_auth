import { useCallback, useEffect, useState } from "react";
import { tenantAdminClient } from "../services/tenantAdminClient";
import type { KeyRotationEvent, TenantAdminSession, TenantClient, TenantConsent, TenantIdentity } from "../types";

async function optional<T>(load: () => Promise<T>, fallback: T): Promise<T> {
  try {
    return await load();
  } catch {
    return fallback;
  }
}

export function useTenantAdmin() {
  const [session, setSession] = useState<TenantAdminSession | null>(null);
  const [identities, setIdentities] = useState<TenantIdentity[]>([]);
  const [clients, setClients] = useState<TenantClient[]>([]);
  const [consents, setConsents] = useState<TenantConsent[]>([]);
  const [keyEvents, setKeyEvents] = useState<KeyRotationEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadData = useCallback(async () => {
    const [nextIdentities, nextClients, nextConsents, nextKeyEvents] = await Promise.all([
      optional(() => tenantAdminClient.identities(), []),
      optional(() => tenantAdminClient.clients(), []),
      optional(() => tenantAdminClient.consents(), []),
      optional(() => tenantAdminClient.keyEvents(), [])
    ]);
    setIdentities(nextIdentities);
    setClients(nextClients);
    setConsents(nextConsents);
    setKeyEvents(nextKeyEvents);
  }, []);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const nextSession = await tenantAdminClient.session();
      setSession(nextSession);
      if (nextSession?.authenticated) {
        await loadData();
      }
    } catch {
      setSession(null);
      setIdentities([]);
      setClients([]);
      setConsents([]);
      setKeyEvents([]);
    } finally {
      setLoading(false);
    }
  }, [loadData]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function login(identifier: string, password: string) {
    setError("");
    try {
      const nextSession = await tenantAdminClient.login(identifier, password);
      setSession(nextSession);
      await loadData();
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unable to sign in.");
      throw nextError;
    }
  }

  async function logout() {
    await optional(() => tenantAdminClient.logout(), { authenticated: false });
    setSession(null);
    setIdentities([]);
    setClients([]);
    setConsents([]);
    setKeyEvents([]);
  }

  return {
    clients,
    consents,
    error,
    identities,
    keyEvents,
    loading,
    login,
    logout,
    refresh,
    session
  };
}
