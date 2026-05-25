import { describe, expect, it } from 'vitest';

import { extractApiErrorMessage, humanizeError, parseResponseBody } from './errorMessages';

const response = (status: number, body: string, contentType = 'application/json'): Response => (
  new Response(body, {
    status,
    statusText: status === 409 ? 'Conflict' : 'Error',
    headers: { 'content-type': contentType },
  })
);

describe('admin UI error message normalization', () => {
  it('parses JSON bodies even when a runtime labels them text/plain', async () => {
    const parsed = await parseResponseBody(response(
      409,
      JSON.stringify({ detail: 'tenant slug, name, or email already exists' }),
      'text/plain; charset=utf-8',
    ));

    expect(parsed.isJson).toBe(true);
    expect(extractApiErrorMessage({ status: 409, statusText: 'Conflict' }, parsed.payload)).toBe(
      'Tenant slug, name, or email already exists',
    );
  });

  it('turns validation detail arrays into readable field messages', () => {
    const message = extractApiErrorMessage(
      { status: 422, statusText: 'Unprocessable Entity' },
      {
        detail: [
          {
            loc: ['body', 'new_password'],
            msg: 'String should have at least 8 characters',
            type: 'string_too_short',
            ctx: { min_length: 8 },
          },
          {
            loc: ['body', 'email'],
            msg: 'Field required',
            type: 'missing',
          },
        ],
      },
    );

    expect(message).toBe('New password must be at least 8 characters. Email is required.');
  });

  it('extracts nested JSON-RPC error messages', () => {
    expect(extractApiErrorMessage(
      { status: 400, statusText: 'Bad Request' },
      { error: { code: -32000, message: 'policy denied tenant mutation' } },
    )).toBe('Policy denied tenant mutation');
  });

  it('humanizes thrown errors before visual display', () => {
    expect(humanizeError(new Error('network request failed'))).toBe('Network request failed');
    expect(humanizeError('bad')).toBe('Request failed.');
  });
});
