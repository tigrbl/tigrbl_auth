import { beforeEach, describe, expect, it, vi } from 'vitest';

import { backendService, normalizeTenantJwksPublication } from './backendService';
import { gateway_rpc } from './jsonRpcService';

describe('backendService tenant admin surface', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('lists tenants from the session-backed admin tenant route', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      headers: new Headers({ 'content-type': 'application/json' }),
      text: async () => JSON.stringify([
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
      headers: new Headers({ 'content-type': 'application/json' }),
      text: async () => JSON.stringify({
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

  it('accepts valid JSON tenant responses even when the content type is text/plain', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      headers: new Headers({ 'content-type': 'text/plain; charset=utf-8' }),
      text: async () => JSON.stringify({
        id: 'tenant-plain',
        name: 'Tenant Plain',
        slug: 'tenant-plain',
        email: 'tenant-plain@example.test',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    const tenant = await backendService.createTenant({
      name: 'Tenant Plain',
      slug: 'tenant-plain',
      email: 'tenant-plain@example.test',
    });

    expect(tenant).toEqual({
      id: 'tenant-plain',
      name: 'Tenant Plain',
      slug: 'tenant-plain',
      email: 'tenant-plain@example.test',
      description: undefined,
      created_at: undefined,
    });
  });

  it('surfaces tenant provisioning conflicts from the admin tenant route', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      headers: new Headers({ 'content-type': 'application/json' }),
      text: async () => JSON.stringify({
        detail: 'tenant slug, name, or email already exists',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(backendService.createTenant({
      name: 'Tenant Two',
      slug: 'tenant-two',
      email: 'tenant-two@example.test',
    })).rejects.toThrow('Tenant slug, name, or email already exists');
  });

  it('calls tenant JWKS key mutation methods with tenant scope', async () => {
    vi.spyOn(gateway_rpc, 'hasMethod').mockResolvedValue(true);
    const callMock = vi.spyOn(gateway_rpc, 'call').mockResolvedValue({ result: { status: 'ok' } } as any);
    const tenant = { id: 'tenant-a-id', name: 'Tenant A', slug: 'tenant-a' };

    await backendService.seedTenantJwksKey(tenant);
    await backendService.createTenantJwksKey(tenant, { kid: 'kid-a', status: 'active', x: 'pub-a' });
    await backendService.updateTenantJwksKey(tenant, { kid: 'kid-a', status: 'retired', publish: false });
    await backendService.deleteTenantJwksKey(tenant, 'kid-a');

    expect(callMock).toHaveBeenNthCalledWith(1, 'tenant.keys.seed', { tenant: 'tenant-a', tenant_id: 'tenant-a-id' });
    expect(callMock).toHaveBeenNthCalledWith(2, 'tenant.keys.create', expect.objectContaining({ tenant: 'tenant-a', kid: 'kid-a', x: 'pub-a' }));
    expect(callMock).toHaveBeenNthCalledWith(3, 'tenant.keys.update', expect.objectContaining({ tenant: 'tenant-a', kid: 'kid-a', status: 'retired', publish: false }));
    expect(callMock).toHaveBeenNthCalledWith(4, 'tenant.keys.delete', { tenant: 'tenant-a', tenant_id: 'tenant-a-id', kid: 'kid-a' });
  });

  it('rejects HTML fallback responses for tenant JWKS discovery', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      headers: new Headers({ 'content-type': 'text/html' }),
      text: async () => '<!doctype html><html><body>Admin UIX</body></html>',
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(backendService.getTenantJwksPublication({
      id: 'tenant-a-id',
      name: 'Tenant A',
      slug: 'tenant-a',
    })).rejects.toThrow('Expected JSON response from /tenants/tenant-a/.well-known/openid-configuration');
    expect(fetchMock).toHaveBeenCalledTimes(1);
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
