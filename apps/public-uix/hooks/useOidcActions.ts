
import { useCallback } from 'react';
import { User, AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getProviderConfig, getTigrblAuthProviderConfig } from './useOidc';
import { usePlatform } from './usePlatform';

export const useOidcActions = (onAuthSuccess: (user: User) => void) => {
  const platform = usePlatform();

  const handleCallback = useCallback(async (provider?: AuthProvider) => {
    try {
      const activeProvider = provider || (localStorage.getItem('nexus_pending_provider') as AuthProvider);
      if (!activeProvider) throw new Error('Provider context lost.');

      const config = activeProvider === AuthProvider.GENERIC
        ? await getTigrblAuthProviderConfig()
        : getProviderConfig(activeProvider);
      const adapter = OidcAdapterFactory.getAdapter(activeProvider, config);
      const user = await adapter.handleCallback();

      const fullUser: User = { ...user, isEmailVerified: true, mfaEnabled: false };
      onAuthSuccess(fullUser);

      // Use whitelabeled redirect URI
      window.location.hash = platform.postLoginRedirectUri;
    } catch (err: any) {
      console.error('OIDC Callback Error:', err);
      window.location.hash = '#/login';
    }
  }, [onAuthSuccess, platform.postLoginRedirectUri]);

  return { handleCallback };
};
