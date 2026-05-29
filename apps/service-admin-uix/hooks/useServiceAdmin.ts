import { useCallback, useEffect, useState } from "react";
import { serviceAdminClient } from "../services/serviceAdminClient";
import type { ApiKeyRecord, IntrospectionResult, ResourceMetadata, ServiceAdminSession, ServiceIdentity, ServiceKey, TokenRecord } from "../types";

const defaultSession: ServiceAdminSession = {
  authenticated: true,
  email: "service-admin@example.test",
  operator_id: "local-service-admin",
  tenant_id: "local-tenant",
  username: "service-admin",
  roles: ["service-admin", "workload-admin"]
};

async function optional<T>(load: () => Promise<T>, fallback: T): Promise<T> {
  try {
    return await load();
  } catch {
    return fallback;
  }
}

export function useServiceAdmin() {
  const [session, setSession] = useState<ServiceAdminSession | null>(null);
  const [services, setServices] = useState<ServiceIdentity[]>([]);
  const [serviceKeys, setServiceKeys] = useState<ServiceKey[]>([]);
  const [apiKeys, setApiKeys] = useState<ApiKeyRecord[]>([]);
  const [tokenRecords, setTokenRecords] = useState<TokenRecord[]>([]);
  const [metadata, setMetadata] = useState<ResourceMetadata | null>(null);
  const [introspection, setIntrospection] = useState<IntrospectionResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    if (!session?.authenticated) return;
    setLoading(true);
    setError("");
    try {
      const [nextServices, nextServiceKeys, nextApiKeys, nextTokenRecords, nextMetadata] = await Promise.all([
        optional(() => serviceAdminClient.services(), []),
        optional(() => serviceAdminClient.serviceKeys(), []),
        optional(() => serviceAdminClient.apiKeys(), []),
        optional(() => serviceAdminClient.tokenRecords(), []),
        optional(() => serviceAdminClient.resourceMetadata(), null)
      ]);
      setServices(nextServices);
      setServiceKeys(nextServiceKeys);
      setApiKeys(nextApiKeys);
      setTokenRecords(nextTokenRecords);
      setMetadata(nextMetadata);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unable to load service administration data.");
    } finally {
      setLoading(false);
    }
  }, [session?.authenticated]);

  useEffect(() => {
    void refresh();
  }, [refresh]);

  async function login(username: string, email: string, tenantId: string) {
    setSession({
      ...defaultSession,
      email: email.trim() || defaultSession.email,
      operator_id: username.trim() || defaultSession.operator_id,
      tenant_id: tenantId.trim() || defaultSession.tenant_id,
      username: username.trim() || defaultSession.username
    });
  }

  function logout() {
    setSession(null);
    setServices([]);
    setServiceKeys([]);
    setApiKeys([]);
    setTokenRecords([]);
    setMetadata(null);
    setIntrospection(null);
  }

  async function runIntrospection(token: string) {
    const result = await optional(() => serviceAdminClient.introspect(token), { active: false });
    setIntrospection(result);
  }

  return {
    apiKeys,
    error,
    introspection,
    loading,
    login,
    logout,
    metadata,
    refresh,
    runIntrospection,
    serviceKeys,
    services,
    session,
    tokenRecords
  };
}
