import { createContext, useContext } from "react";
import type { AuthContextValue } from "./types";

const AuthContext = createContext<AuthContextValue>({
  loading: false,
  session: null
});

export const AuthProvider = AuthContext.Provider;

export function useAuthContext(): AuthContextValue {
  return useContext(AuthContext);
}

