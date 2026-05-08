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
type ValidationIssue = {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
  ctx?: Record<string, unknown>;
};

const safeJson = async <T>(response: Response): Promise<T> => {
  const text = await response.text();
  return text ? (JSON.parse(text) as T) : ({} as T);
};

const fieldLabel = (field: string): string => {
  switch (field) {
    case 'identifier':
      return 'Username or email';
    case 'password':
      return 'Password';
    case 'current_password':
      return 'Current password';
    case 'new_password':
      return 'New password';
    case 'token':
      return 'Reset token';
    default:
      return field.replace(/_/g, ' ').replace(/^\w/, (value) => value.toUpperCase());
  }
};

const firstString = (value: unknown): string | null => {
  return typeof value === 'string' && value.trim() ? value.trim() : null;
};

const fallbackValidationMessage = (body: JsonObject): string | null => {
  const passwordFields = ['password', 'current_password', 'new_password'] as const;
  for (const field of passwordFields) {
    const raw = body[field];
    if (typeof raw === 'string' && raw.length < 8) {
      return `${fieldLabel(field)} must be at least 8 characters.`;
    }
  }
  const identifier = body.identifier;
  if (typeof identifier === 'string' && identifier.trim().length > 0 && identifier.trim().length < 3) {
    return 'Username or email must be at least 3 characters.';
  }
  const token = body.token;
  if (typeof token === 'string' && token.trim().length > 0 && token.trim().length < 16) {
    return 'Reset token is too short.';
  }
  return null;
};

const normalizeValidationIssue = (issue: ValidationIssue): string | null => {
  const field = issue.loc?.length ? String(issue.loc[issue.loc.length - 1]) : null;
  const label = field ? fieldLabel(field) : 'Field';
  const message = firstString(issue.msg);

  if (issue.type === 'string_too_short' || message?.includes('at least')) {
    const minLength = issue.ctx?.min_length;
    if (typeof minLength === 'number') {
      return `${label} must be at least ${minLength} characters.`;
    }
  }
  if (issue.type === 'string_too_long' || message?.includes('at most')) {
    const maxLength = issue.ctx?.max_length;
    if (typeof maxLength === 'number') {
      return `${label} must be no more than ${maxLength} characters.`;
    }
  }
  if (issue.type === 'missing' || message?.toLowerCase().includes('required')) {
    return `${label} is required.`;
  }
  if (message) {
    return `${label}: ${message.replace(/^String\s+/, '')}`;
  }
  return null;
};

const extractApiErrorMessage = (response: Response, payload: any, body?: JsonObject): string => {
  const validationDetails = Array.isArray(payload?.detail) ? payload.detail as ValidationIssue[] : null;
  if (validationDetails && validationDetails.length > 0) {
    const messages = validationDetails
      .map(normalizeValidationIssue)
      .filter((value): value is string => Boolean(value));
    if (messages.length > 0) {
      return Array.from(new Set(messages)).join(' ');
    }
  }

  if (response.status === 422) {
    const fallback = body ? fallbackValidationMessage(body) : null;
    if (fallback) {
      return fallback;
    }
    if (typeof payload?.detail === 'string' && payload.detail.trim()) {
      const detail = payload.detail.trim();
      const lowered = detail.toLowerCase();
      if (lowered.includes('unprocessable') || lowered.includes('validation failed') || lowered.includes('not processable')) {
        return 'One or more fields are invalid. Passwords must be at least 8 characters.';
      }
      return detail;
    }
    return 'One or more fields are invalid. Check the entered values and try again.';
  }

  return String(payload?.detail || payload?.error || `HTTP ${response.status}`);
};

const postJson = async <T>(path: string, body: JsonObject): Promise<T> => {
  const response = await fetch(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });
  const payload = await safeJson<any>(response);
  if (!response.ok) {
    throw new Error(extractApiErrorMessage(response, payload, body));
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
