import type { ReactNode } from "react";
import { EmptyState } from "../components/EmptyState";
import { useAuthContext } from "./AuthProvider";

export function RequireAuth({
  children,
  fallback
}: {
  children: ReactNode;
  fallback?: ReactNode;
}) {
  const { loading, session } = useAuthContext();

  if (loading) {
    return <EmptyState title="Loading session" body="Checking the current authentication state." />;
  }
  if (!session?.authenticated) {
    return fallback ?? <EmptyState title="Session required" body="Sign in to continue." />;
  }
  return <>{children}</>;
}

