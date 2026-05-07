import { beforeEach, describe, expect, it, vi } from 'vitest';

import { JsonRpcService } from './jsonRpcService';
import type { PolicyGate } from '../types';

describe('JsonRpcService', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('uses JSON-RPC request envelopes for admin methods', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          jsonrpc: '2.0',
          result: { active_methods: ['policy.sync'] },
          id: '1',
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ jsonrpc: '2.0', result: { status: 'ok' }, id: '2' }),
      });
    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');
    const policy: PolicyGate = {
      id: 'policy-123',
      tenant_id: 'tenant-1',
      name: 'Sample Policy',
      type: 'CEDAR',
      content: 'permit(principal, action, resource);',
      is_active: true,
      version: 1,
    };

    await service.syncPolicy(policy);

    const [, options] = fetchMock.mock.calls[1];
    const body = JSON.parse(options.body as string);

    expect(body.method).toBe('policy.sync');
    expect(body.params.policy).toEqual(policy);
  });

  it('uses the repo-local admin API key storage without embedding a fallback secret', async () => {
    const localStorageMock = {
      getItem: vi.fn().mockReturnValue('local-admin-key'),
    };

    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({
          jsonrpc: '2.0',
          result: { active_methods: ['Tenant.list'] },
          id: '1',
        }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ jsonrpc: '2.0', result: [], id: '2' }),
      });

    vi.stubGlobal('localStorage', localStorageMock);
    vi.stubGlobal('sessionStorage', {
      getItem: vi.fn().mockReturnValue(null),
    });
    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');
    await service.call('tenant.list', {});

    expect(fetchMock).toHaveBeenCalledTimes(2);

    const [, options] = fetchMock.mock.calls[1];
    const body = JSON.parse(options.body as string);

    expect(localStorageMock.getItem).toHaveBeenCalledWith('tigrbl_auth_admin_api_key');
    expect((options.headers as Record<string, string>)['X-API-Key']).toBe('local-admin-key');
    expect((options.headers as Record<string, string>).Authorization).toBe('Bearer local-admin-key');
    expect(body.method).toBe('Tenant.list');
  });

  it('discovers active admin methods before declaring method support', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({
        jsonrpc: '2.0',
        result: { active_methods: ['tenant.list', 'client.list'] },
        id: '1',
      }),
    });

    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');

    await expect(service.hasMethod('tenant.list')).resolves.toBe(true);
    await expect(service.hasMethod('policy.sync')).resolves.toBe(false);
  });

  it('falls back to the checked-in OpenRPC catalog when runtime discovery is unavailable', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ jsonrpc: '2.0', error: { code: -32601, message: 'missing' }, id: '1' }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ methods: [{ name: 'tenant.list' }, { name: 'client.list' }] }),
      });

    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');

    await expect(service.hasMethod('tenant.list')).resolves.toBe(true);
    await expect(service.hasMethod('policy.sync')).resolves.toBe(false);
  });

  it('maps logical admin aliases onto the live OpenRPC method names', async () => {
    const fetchMock = vi.fn()
      .mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({ jsonrpc: '2.0', error: { code: -32601, message: 'missing' }, id: '1' }),
      })
      .mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ methods: [{ name: 'Tenant.list' }, { name: 'User.list' }, { name: 'Client.list' }] }),
      });

    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');

    await expect(service.hasMethod('tenant.list')).resolves.toBe(true);
    await expect(service.hasMethod('identity.list')).resolves.toBe(true);
    await expect(service.hasMethod('client.list')).resolves.toBe(true);
  });
});
