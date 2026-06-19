import { beforeEach, describe, expect, it, vi } from 'vitest';

import { adminAuthService } from './adminAuthService';

describe('adminAuthService validation messaging', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it('surfaces a friendly password-length message from validation detail arrays', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      text: async () => JSON.stringify({
        detail: [
          {
            type: 'string_too_short',
            loc: ['new_password'],
            msg: 'String should have at least 8 characters',
            ctx: { min_length: 8 },
          },
        ],
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(
      adminAuthService.changePassword('AdminPass123!', 'short'),
    ).rejects.toThrow('New password must be at least 8 characters.');
  });

  it('falls back to a readable password-length message when the backend only says unprocessable', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      text: async () => JSON.stringify({
        detail: 'entity not processable',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(
      adminAuthService.resetPassword('debug-reset-token-1234', 'short'),
    ).rejects.toThrow('Password must be at least 8 characters.');
  });

  it('maps validation-failed 422 strings to the same readable password guidance', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 422,
      text: async () => JSON.stringify({
        detail: 'Unprocessable Entity: validation failed',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(
      adminAuthService.changePassword('AdminPass123!', 'tiny'),
    ).rejects.toThrow('New password must be at least 8 characters.');
  });

  it('preserves non-validation backend messages', async () => {
    const fetchMock = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      text: async () => JSON.stringify({
        detail: 'invalid current password',
      }),
    });
    vi.stubGlobal('fetch', fetchMock);

    await expect(
      adminAuthService.changePassword('wrong-password', 'LongEnough123!'),
    ).rejects.toThrow('Invalid current password');
  });
});
