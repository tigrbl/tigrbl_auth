export interface UixSession {
  authenticated: boolean;
  email?: string;
  expiresAt?: string;
  permissions?: string[];
  subject?: string;
  tenantId?: string;
  username?: string;
}

export interface AuthContextValue {
  loading: boolean;
  login?: (credentials: Record<string, string>) => Promise<void>;
  logout?: () => Promise<void> | void;
  refresh?: () => Promise<void>;
  session: UixSession | null;
}

