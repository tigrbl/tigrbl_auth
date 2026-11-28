import { useAuthContext } from "../auth/AuthProvider";
import { hasAnyPermission, hasEveryPermission } from "../auth/permissions";

export function usePermissions() {
  const { session } = useAuthContext();
  const permissions = session?.permissions ?? [];
  return {
    permissions,
    hasAny: (required: string[]) => hasAnyPermission(permissions, required),
    hasEvery: (required: string[]) => hasEveryPermission(permissions, required)
  };
}

