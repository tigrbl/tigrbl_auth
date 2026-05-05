
import { useState, useCallback } from 'react';
import { AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getProviderConfig, getTigrblAuthProviderConfig } from './useOidc';

export const useLogin = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [mfaPending, setMfaPending] = useState(false);

  const login = useCallback(async (provider: AuthProvider, remember: boolean = false) => {
    setIsLoading(true);
    setError(null);
    try {
      const config = provider === AuthProvider.GENERIC
        ? await getTigrblAuthProviderConfig()
        : getProviderConfig(provider);
      localStorage.setItem('nexus_pending_provider', provider);
      const adapter = OidcAdapterFactory.getAdapter(provider, config);
      await adapter.authorize();
    } catch (err: any) {
      setError(err.message);
      setIsLoading(false);
    }
  }, []);

  return { login, mfaPending, setMfaPending, isLoading, error, setError };
};
