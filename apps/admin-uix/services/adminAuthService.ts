export type AdminSessionState = {
  authenticated: boolean;
  session_id?: string | null;
  user_id?: string | null;
  tenant_id?: string | null;
  username?: string | null;
  email?: string | null;
  is_admin: boolean;
  is_superuser: boolean;
  must_change_password: boolean;
  roles: string[];
  debug_reset_token?: string | null;
};

type JsonObject = Record<string, unknown>;

const safeJson = async <T>(response: Response): Promise<T> => {
  const text = await response.text();
  return text ? (JSON.parse(text) as T) : ({} as T);
};

const postJson = async <T>(path: string, body: JsonObject): Promise<T> => {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const payload = await safeJson<any>(response);
  if (!response.ok) {
    throw new Error(String(payload?.detail || payload?.error || `HTTP ${response.status}`));
  }
  return payload as T;
};

const getJson = async <T>(path: string): Promise<T> => {
  const response = await fetch(path, { headers: { Accept: 'application/json' } });
  const payload = await safeJson<any>(response);
  if (!response.ok) {
    throw new Error(String(payload?.detail || payload?.error || `HTTP ${response.status}`));
  }
  return payload as T;
};

export const adminAuthService = {
  async getSession(): Promise<AdminSessionState> {
    return getJson<AdminSessionState>('/admin/auth/session');
  },

  async login(identifier: string, password: string): Promise<AdminSessionState> {
    return postJson<AdminSessionState>('/admin/auth/login', { identifier, password });
  },

  async logout(): Promise<void> {
    await postJson('/admin/auth/logout', {});
  },

  async requestPasswordReset(identifier: string): Promise<AdminSessionState> {
    return postJson<AdminSessionState>('/admin/auth/forgot-password', { identifier });
  },

  async resetPassword(token: string, password: string): Promise<void> {
    await postJson('/admin/auth/reset-password', { token, password });
  },

  async changePassword(current_password: string, new_password: string): Promise<AdminSessionState> {
    return postJson<AdminSessionState>('/admin/auth/change-password', { current_password, new_password });
  },
};
