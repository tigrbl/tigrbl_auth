import type { ReactNode } from "react";
import { useAuthContext } from "./AuthProvider";
import { hasEveryPermission } from "./permissions";

export function PermissionGate({
  children,
  fallback = null,
  permissions
}: {
  children: ReactNode;
  fallback?: ReactNode;
  permissions: string[];
}) {
  const { session } = useAuthContext();
  return hasEveryPermission(session?.permissions ?? [], permissions) ? <>{children}</> : <>{fallback}</>;
}

