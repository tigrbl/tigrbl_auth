import { beforeEach, describe, expect, it, vi } from 'vitest';

import { backendService, normalizeTenantJwksPublication } from './backendService';

describe('backendService tenant admin surface', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('lists tenants from the session-backed admin tenant route', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ([
        {
          id: 'tenant-1',
          name: 'Tenant One',
          slug: 'tenant-one',
          email: 'tenant-one@example.test',
          created_at: '2026-05-07T00:00:00Z',
        },
      ]),
    });
    vi.stubGlobal('fetch', fetchMock);

    const tenants = await backendService.getTenants();

    expect(fetchMock).toHaveBeenCalledWith('/admin/tenants', expect.any(Object));
    expect(tenants).toEqual([
      {
        id: 'tenant-1',
        name: 'Tenant One',
        slug: 'tenant-one',
        email: 'tenant-one@example.test',
        created_at: '2026-05-07T00:00:00Z',
        description: undefined,
      },
    ]);
  });

  it('creates a tenant through the session-backed admin tenant route', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        id: 'tenant-2',
        name: 'Tenant Two',
        slug: 'tenant-two',
        email: 'tenant-two@example.test',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    const tenant = await backendService.createTenant({
      name: 'Tenant Two',
      slug: 'tenant-two',
      email: 'tenant-two@example.test',
    });

    expect(fetchMock).toHaveBeenCalledWith(
      '/admin/tenants',
      expect.objectContaining({
        method: 'POST',
        headers: expect.objectContaining({ 'Content-Type': 'application/json' }),
      }),
    );
    const [, init] = fetchMock.mock.calls[0];
    expect(init?.body).toBe(JSON.stringify({
      name: 'Tenant Two',
      slug: 'tenant-two',
      email: 'tenant-two@example.test',
    }));
    expect(tenant.email).toBe('tenant-two@example.test');
  });

  it('normalizes tenant JWKS publication without leaking cross-tenant inventory', () => {
    const view = normalizeTenantJwksPublication(
      { id: 'tenant-a-id', name: 'Tenant A', slug: 'tenant-a' },
      {
        issuer: 'https://id.example.com/tenants/tenant-a',
        jwks_uri: 'https://id.example.com/tenants/tenant-a/.well-known/jwks.json',
      },
      {
        keys: [
          { kid: 'kid-a-active', alg: 'ES256', kty: 'EC', use: 'sig', crv: 'P-256', status: 'active', d: 'private' },
          { kid: 'kid-a-next', alg: 'ES256', kty: 'EC', use: 'sig', crv: 'P-256', status: 'next' },
        ],
      },
      [
        { id: 'kid-a-retired', tenant: 'tenant-a', status: 'retired', data: { kid: 'kid-a-retired', alg: 'ES256', kty: 'EC', use: 'sig' } },
        { id: 'kid-b-active', tenant: 'tenant-b', status: 'active', data: { kid: 'kid-b-active', alg: 'ES256' } },
      ],
    );

    expect(view.publication_status).toBe('published');
    expect(view.keys_by_lifecycle.active.map((key) => key.kid)).toEqual(['kid-a-active']);
    expect(view.keys_by_lifecycle.next.map((key) => key.kid)).toEqual(['kid-a-next']);
    expect(view.keys_by_lifecycle.retired.map((key) => key.kid)).toEqual(['kid-a-retired']);
    expect(JSON.stringify(view)).not.toContain('kid-b-active');
    expect(JSON.stringify(view)).not.toContain('private');
  });
});
