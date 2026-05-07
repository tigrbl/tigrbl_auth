import { beforeEach, describe, expect, it, vi } from 'vitest';

import { backendService } from './backendService';

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
});
