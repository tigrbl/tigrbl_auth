import { useCallback, useEffect, useState } from "react";
import { developerClient } from "../services/developerClient";
import type { ClientRegistration, DeveloperApplication, DeveloperSession, IssuerMetadata } from "../types";

const defaultSession: DeveloperSession = {
  authenticated: true,
  developer_id: "local-developer",
  email: "developer@example.test",
  tenant_id: "local-tenant",
  username: "developer",
  roles: ["tenant-developer"]
};

async function optional<T>(load: () => Promise<T>, fallback: T): Promise<T> {
  try {
    return await load();
  } catch {
    return fallback;
  }
}

export function useDeveloperPortal() {
  const [session, setSession] = useState<DeveloperSession | null>(null);
  const [applications, setApplications] = useState<DeveloperApplication[]>([]);
  const [registrations, setRegistrations] = useState<ClientRegistration[]>([]);
  const [metadata, setMetadata] = useState<IssuerMetadata | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const refresh = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const [nextApplications, nextRegistrations, nextMetadata] = await Promise.all([
        optional(() => developerClient.applications(), []),
        optional(() => developerClient.clientRegistrations(), []),
        optional(() => developerClient.discovery(), null)
      ]);
      setApplications(nextApplications);
      setRegistrations(nextRegistrations);
      setMetadata(nextMetadata);
    } catch (nextError) {
      setError(nextError instanceof Error ? nextError.message : "Unable to load developer portal.");
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    if (session?.authenticated) {
      void refresh();
    } else {
      setLoading(false);
    }
  }, [refresh, session?.authenticated]);

  async function login(username: string, email: string, tenantId: string) {
    setSession({
      ...defaultSession,
      developer_id: username.trim() || defaultSession.developer_id,
      email: email.trim() || defaultSession.email,
      tenant_id: tenantId.trim() || defaultSession.tenant_id,
      username: username.trim() || defaultSession.username
    });
  }

  function logout() {
    setSession(null);
    setApplications([]);
    setRegistrations([]);
    setMetadata(null);
  }

  return {
    applications,
    error,
    loading,
    login,
    logout,
    metadata,
    refresh,
    registrations,
    session
  };
}
