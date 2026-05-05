
import { useCallback, useEffect } from 'react';
import { User, AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getTigrblAuthProviderConfig } from './useOidc';
import { usePlatform } from './usePlatform';
import { safeProblemMessage } from '../services/tigrblAuthDiscovery';
import {
  buildPopupCallbackHash,
  isTrustedBrowserOrigin,
  sanitizePublicHashTarget,
} from '../services/publicUxPolicy';

export const useOidcActions = (onAuthSuccess: (user: User) => void) => {
  const platform = usePlatform();
  const callbackTarget = sanitizePublicHashTarget(platform.postLoginRedirectUri, '#/profile');

  const handleCallback = useCallback(async (provider?: AuthProvider) => {
    try {
      const activeProvider = provider || (localStorage.getItem('tigrbl_auth_pending_provider') as AuthProvider);
      if (!activeProvider) throw new Error('Provider context lost.');

      const config = await getTigrblAuthProviderConfig();
      const adapter = OidcAdapterFactory.getAdapter(activeProvider, config);
      const user = await adapter.handleCallback();

      const fullUser: User = { ...user, isEmailVerified: true, mfaEnabled: false };
      onAuthSuccess(fullUser);

      // Use whitelabeled redirect URI
      window.location.hash = callbackTarget;
    } catch (err: any) {
      sessionStorage.setItem('tigrbl_auth_public_error', safeProblemMessage(err));
      window.location.hash = '#/login';
    }
  }, [callbackTarget, onAuthSuccess]);

  useEffect(() => {
    const onMessage = (event: MessageEvent<{ type?: string; payload?: { search?: string } }>) => {
      if (event.data?.type !== 'OIDC_CALLBACK') {
        return;
      }
      if (!isTrustedBrowserOrigin(event.origin, window.location.origin, window.location.origin)) {
        return;
      }
      const callbackHash = buildPopupCallbackHash(event.data.payload?.search);
      if (!callbackHash) {
        return;
      }
      window.location.hash = callbackHash;
      void handleCallback(AuthProvider.GENERIC);
    };

    window.addEventListener('message', onMessage);
    return () => window.removeEventListener('message', onMessage);
  }, [handleCallback]);

  return { handleCallback };
};
