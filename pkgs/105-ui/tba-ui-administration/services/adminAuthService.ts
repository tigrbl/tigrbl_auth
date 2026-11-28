import { extractResponseErrorMessage, parseResponseBody } from './errorMessages';

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

const postJson = async <T>(path: string, body: JsonObject): Promise<T> => {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const parsed = await parseResponseBody(response);
  if (!response.ok) {
    throw new Error(extractResponseErrorMessage(response, parsed.payload, { requestBody: body, fallback: `HTTP ${response.status}` }));
  }
  return parsed.payload as T;
};

const getJson = async <T>(path: string): Promise<T> => {
  const response = await fetch(path, { headers: { Accept: 'application/json' } });
  const parsed = await parseResponseBody(response);
  if (!response.ok) {
    throw new Error(extractResponseErrorMessage(response, parsed.payload, { fallback: `HTTP ${response.status}` }));
  }
  return parsed.payload as T;
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
