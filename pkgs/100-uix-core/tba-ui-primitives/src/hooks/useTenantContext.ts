import { useAuthContext } from "../auth/AuthProvider";

export function useTenantContext() {
  const { session } = useAuthContext();
  return {
    tenantId: session?.tenantId ?? null,
    hasTenantContext: Boolean(session?.tenantId)
  };
}

