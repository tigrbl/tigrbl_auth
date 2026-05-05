import { beforeEach, describe, expect, it, vi } from 'vitest';

import { JsonRpcService } from './jsonRpcService';
import type { PolicyGate } from '../types';

describe('JsonRpcService', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('uses JSON-RPC request envelopes for admin methods', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ jsonrpc: '2.0', result: { status: 'ok' }, id: '1' }),
    });
    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');
    const policy: PolicyGate = {
      id: 'policy-123',
      realm_id: 'realm-1',
      name: 'Sample Policy',
      type: 'CEDAR',
      content: 'permit(principal, action, resource);',
      is_active: true,
      version: 1,
    };

    await service.syncPolicy(policy);

    const [, options] = fetchMock.mock.calls[0];
    const body = JSON.parse(options.body as string);

    expect(body.method).toBe('Policy.sync');
    expect(body.params.policy).toEqual(policy);
  });

  it('uses the repo-local admin API key storage without embedding a fallback secret', async () => {
    const localStorageMock = {
      getItem: vi.fn().mockReturnValue('local-admin-key'),
    };

    const fetchMock = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => ({ jsonrpc: '2.0', result: [], id: '1' }),
    });

    vi.stubGlobal('localStorage', localStorageMock);
    vi.stubGlobal('fetch', fetchMock);

    const service = new JsonRpcService('/rpc');
    await service.call('Realm.list', {});

    expect(fetchMock).toHaveBeenCalledTimes(1);

    const [, options] = fetchMock.mock.calls[0];

    expect(localStorageMock.getItem).toHaveBeenCalledWith('tigrbl_auth_admin_api_key');
    expect((options.headers as Record<string, string>)['X-API-Key']).toBe('local-admin-key');
    expect((options.headers as Record<string, string>).Authorization).toBe('Bearer local-admin-key');
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
    await expect(service.hasMethod('Policy.sync')).resolves.toBe(false);
  });
});
