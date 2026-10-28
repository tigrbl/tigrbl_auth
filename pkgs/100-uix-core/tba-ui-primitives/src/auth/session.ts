import type { UixSession } from "./types";

export function describeSession(session: UixSession | null): string {
  if (!session?.authenticated) return "Unauthenticated";
  return session.username ?? session.email ?? session.subject ?? "Authenticated session";
}

