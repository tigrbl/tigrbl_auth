import { useCallback, useEffect, useState } from "react";
import { tenantAdminClient } from "../services/tenantAdminClient";
import type {
  CreateTenantClientInput,
  CreateTenantIdentityInput,
  KeyRotationEvent,
  TenantAdminSession,
  TenantClient,
  TenantConsent,
  TenantIdentity,
  UpdateTenantClientInput,
  UpdateTenantIdentityInput
} from "../types";

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

  async function createIdentity(payload: CreateTenantIdentityInput) {
    await tenantAdminClient.createIdentity(payload);
    setIdentities(await optional(() => tenantAdminClient.identities(), []));
  }

  async function updateIdentity(identityId: string, payload: UpdateTenantIdentityInput) {
    await tenantAdminClient.updateIdentity(identityId, payload);
    setIdentities(await optional(() => tenantAdminClient.identities(), []));
  }

  async function lockIdentity(identityId: string) {
    await tenantAdminClient.lockIdentity(identityId);
    setIdentities(await optional(() => tenantAdminClient.identities(), []));
  }

  async function unlockIdentity(identityId: string) {
    await tenantAdminClient.unlockIdentity(identityId);
    setIdentities(await optional(() => tenantAdminClient.identities(), []));
  }

  async function deleteIdentity(identityId: string) {
    await tenantAdminClient.deleteIdentity(identityId);
    setIdentities(await optional(() => tenantAdminClient.identities(), []));
  }

  async function createClient(payload: CreateTenantClientInput) {
    await tenantAdminClient.createClient(payload);
    setClients(await optional(() => tenantAdminClient.clients(), []));
  }

  async function updateClient(clientId: string, payload: UpdateTenantClientInput) {
    await tenantAdminClient.updateClient(clientId, payload);
    setClients(await optional(() => tenantAdminClient.clients(), []));
  }

  async function deleteClient(clientId: string) {
    await tenantAdminClient.deleteClient(clientId);
    setClients(await optional(() => tenantAdminClient.clients(), []));
  }

  async function revokeConsent(consentId: string) {
    await tenantAdminClient.revokeConsent(consentId);
    setConsents(await optional(() => tenantAdminClient.consents(), []));
  }

  async function triggerKeyRotation(payload: { tenant_id?: string; reason?: string }) {
    await tenantAdminClient.triggerKeyRotation(payload);
    setKeyEvents(await optional(() => tenantAdminClient.keyEvents(), []));
  }

  return {
    clients,
    consents,
    createClient,
    createIdentity,
    deleteClient,
    deleteIdentity,
    error,
    identities,
    keyEvents,
    lockIdentity,
    loading,
    login,
    logout,
    refresh,
    revokeConsent,
    session,
    triggerKeyRotation,
    unlockIdentity,
    updateClient,
    updateIdentity
  };
}
