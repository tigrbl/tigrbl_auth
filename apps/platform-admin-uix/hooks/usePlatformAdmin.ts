import { useCallback, useEffect, useState } from "react";
import { platformAdminClient } from "../services/platformAdminClient";
import type { AdminSession, CreateIdentityInput, CreateTenantInput, Identity, Tenant } from "../types";

export function usePlatformAdmin() {
  const [session, setSession] = useState<AdminSession | null>(null);
  const [tenants, setTenants] = useState<Tenant[]>([]);
  const [identities, setIdentities] = useState<Identity[]>([]);
  const [selectedTenantId, setSelectedTenantId] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadTenants = useCallback(async () => {
    const rows = await platformAdminClient.tenants();
    setTenants(rows);
    setSelectedTenantId((current) => current || rows[0]?.id || "");
    return rows;
  }, []);

  const loadSession = useCallback(async () => {
    try {
      const nextSession = await platformAdminClient.session();
      setSession(nextSession);
      return nextSession;
    } catch {
      setSession(null);
      return null;
    }
  }, []);

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const nextSession = await loadSession();
      if (nextSession?.authenticated) {
        await loadTenants();
      }
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unable to load platform console.");
    } finally {
      setLoading(false);
    }
  }, [loadSession, loadTenants]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  useEffect(() => {
    if (!selectedTenantId || !session?.authenticated) {
      setIdentities([]);
      return;
    }
    let cancelled = false;
    platformAdminClient
      .identities(selectedTenantId)
      .then((rows) => {
        if (!cancelled) {
          setIdentities(rows);
        }
      })
      .catch((nextError) => {
        if (!cancelled) {
          const message = nextError instanceof Error ? nextError.message : "";
          if (message === "No runtime operation matched request.") {
            setIdentities([]);
            return;
          }
          setError(message || "Unable to load identities.");
        }
      });
    return () => {
      cancelled = true;
    };
  }, [selectedTenantId, session?.authenticated]);

  async function login(identifier: string, password: string) {
    setError("");
    const nextSession = await platformAdminClient.login(identifier, password);
    setSession(nextSession);
    await loadTenants();
  }

  async function logout() {
    await platformAdminClient.logout();
    setSession(null);
    setTenants([]);
    setIdentities([]);
  }

  async function createTenant(payload: CreateTenantInput) {
    const tenant = await platformAdminClient.createTenant(payload);
    await loadTenants();
    setSelectedTenantId(tenant.id);
  }

  async function deleteTenant(tenantId: string) {
    await platformAdminClient.deleteTenant(tenantId);
    const rows = await loadTenants();
    if (selectedTenantId === tenantId) {
      setSelectedTenantId(rows[0]?.id || "");
    }
  }

  async function createIdentity(payload: CreateIdentityInput) {
    await platformAdminClient.createIdentity(payload);
    setIdentities(await platformAdminClient.identities(payload.tenant_id));
  }

  return {
    createIdentity,
    createTenant,
    deleteTenant,
    error,
    identities,
    loading,
    login,
    logout,
    refresh,
    selectedTenantId,
    session,
    setSelectedTenantId,
    tenants
  };
}
