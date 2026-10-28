import { useAuthContext } from "../auth/AuthProvider";

export function useCurrentUser() {
  return useAuthContext().session;
}

