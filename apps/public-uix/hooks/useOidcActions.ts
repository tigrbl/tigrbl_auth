
import { useCallback } from 'react';
import { User, AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getTigrblAuthProviderConfig } from './useOidc';
import { usePlatform } from './usePlatform';
import { safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const useOidcActions = (onAuthSuccess: (user: User) => void) => {
  const platform = usePlatform();

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
      window.location.hash = platform.postLoginRedirectUri;
    } catch (err: any) {
      sessionStorage.setItem('tigrbl_auth_public_error', safeProblemMessage(err));
      window.location.hash = '#/login';
    }
  }, [onAuthSuccess, platform.postLoginRedirectUri]);

  return { handleCallback };
};
