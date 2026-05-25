type JsonObject = Record<string, unknown>;

export type ParsedResponseBody = {
  payload: unknown;
  rawText: string;
  isJson: boolean;
};

export type ValidationIssue = {
  loc?: Array<string | number>;
  msg?: string;
  type?: string;
  ctx?: Record<string, unknown>;
};

export const fieldLabel = (field: string): string => {
  switch (field) {
    case 'identifier':
      return 'Username or email';
    case 'current_password':
      return 'Current password';
    case 'new_password':
      return 'New password';
    case 'tenant_id':
      return 'Tenant';
    case 'client_id':
      return 'Client ID';
    case 'redirect_uris':
      return 'Redirect URIs';
    case 'jwks_uri':
      return 'JWKS URI';
    case 'kid':
      return 'Key ID';
    default:
      return field
        .replace(/_/g, ' ')
        .replace(/\b\w/g, (value) => value.toUpperCase());
  }
};

const firstString = (value: unknown): string | null => (
  typeof value === 'string' && value.trim() ? value.trim() : null
);

const isObject = (value: unknown): value is JsonObject => (
  typeof value === 'object' && value !== null && !Array.isArray(value)
);

const sentence = (value: string): string => {
  const trimmed = value.trim();
  if (!trimmed) {
    return trimmed;
  }
  return `${trimmed.charAt(0).toUpperCase()}${trimmed.slice(1)}`;
};

export const parseResponseBody = async (response: Response): Promise<ParsedResponseBody> => {
  const rawText = await response.text().catch(() => '');
  if (!rawText) {
    return { payload: null, rawText, isJson: false };
  }
  try {
    return { payload: JSON.parse(rawText), rawText, isJson: true };
  } catch {
    return { payload: rawText, rawText, isJson: false };
  }
};

const normalizeValidationIssue = (issue: ValidationIssue): string | null => {
  const field = issue.loc?.length ? String(issue.loc[issue.loc.length - 1]) : null;
  const label = field ? fieldLabel(field) : 'Field';
  const message = firstString(issue.msg);

  if (issue.type === 'string_too_short' || message?.toLowerCase().includes('at least')) {
    const minLength = issue.ctx?.min_length;
    if (typeof minLength === 'number') {
      return `${label} must be at least ${minLength} characters.`;
    }
  }
  if (issue.type === 'string_too_long' || message?.toLowerCase().includes('at most')) {
    const maxLength = issue.ctx?.max_length;
    if (typeof maxLength === 'number') {
      return `${label} must be no more than ${maxLength} characters.`;
    }
  }
  if (issue.type === 'missing' || message?.toLowerCase().includes('required')) {
    return `${label} is required.`;
  }
  if (message) {
    return `${label}: ${sentence(message.replace(/^String\s+/i, ''))}`;
  }
  return null;
};

const fallbackValidationMessage = (body?: JsonObject): string | null => {
  if (!body) {
    return null;
  }
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

const messageFromValue = (value: unknown): string | null => {
  const direct = firstString(value);
  if (direct) {
    return direct;
  }
  if (Array.isArray(value)) {
    const messages = value
      .map((item) => (isObject(item) ? normalizeValidationIssue(item as ValidationIssue) : messageFromValue(item)))
      .filter((item): item is string => Boolean(item));
    return messages.length > 0 ? Array.from(new Set(messages)).join(' ') : null;
  }
  if (isObject(value)) {
    return (
      messageFromValue(value.message)
      ?? messageFromValue(value.detail)
      ?? messageFromValue(value.error)
      ?? messageFromValue(value.reason)
      ?? messageFromValue(value.description)
    );
  }
  return null;
};

export const extractApiErrorMessage = (
  response: Pick<Response, 'status' | 'statusText'>,
  payload: unknown,
  options: { requestBody?: JsonObject; fallback?: string } = {},
): string => {
  if (response.status === 422) {
    const fallback = fallbackValidationMessage(options.requestBody);
    const direct = isObject(payload)
      ? (
        messageFromValue(payload.detail)
        ?? messageFromValue(payload.error)
        ?? messageFromValue(payload.message)
      )
      : messageFromValue(payload);
    const generic = direct?.toLowerCase() ?? '';
    if (fallback && (
      !direct
      || generic.includes('unprocessable')
      || generic.includes('validation failed')
      || generic.includes('not processable')
    )) {
      return fallback;
    }
  }

  if (isObject(payload)) {
    const fromPayload = (
      messageFromValue(payload.detail)
      ?? messageFromValue(payload.error)
      ?? messageFromValue(payload.message)
      ?? messageFromValue(payload.reason)
      ?? messageFromValue(payload.description)
    );
    if (fromPayload) {
      return sentence(fromPayload);
    }
  }

  const fromValue = messageFromValue(payload);
  if (fromValue) {
    return sentence(fromValue);
  }

  if (response.status === 422) {
    return 'One or more fields are invalid. Check the entered values and try again.';
  }

  return options.fallback
    ?? response.statusText
    ?? `HTTP ${response.status}`;
};

export const expectedJsonErrorMessage = (path: string, body: ParsedResponseBody, contentType: string): string => {
  const preview = body.rawText ? ` Body starts with: ${body.rawText.slice(0, 120)}` : '';
  return `Expected JSON response from ${path}, received ${contentType || 'unknown content type'}.${preview}`;
};

export const humanizeError = (error: unknown, fallback = 'Request failed.'): string => {
  if (error instanceof Error && error.message.trim()) {
    return sentence(error.message);
  }
  return fallback;
};
