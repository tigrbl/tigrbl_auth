
import { useState, useCallback } from 'react';
import { AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getTigrblAuthProviderConfig } from './useOidc';
import { safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const useLogin = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(() => {
    if (typeof sessionStorage === 'undefined') {
      return null;
    }
    const callbackError = sessionStorage.getItem('tigrbl_auth_public_error');
    if (callbackError) {
      sessionStorage.removeItem('tigrbl_auth_public_error');
    }
    return callbackError;
  });
  const [mfaPending, setMfaPending] = useState(false);

  const login = useCallback(async (provider: AuthProvider, remember: boolean = false) => {
    setIsLoading(true);
    setError(null);
    try {
      const config = await getTigrblAuthProviderConfig();
      localStorage.setItem('tigrbl_auth_pending_provider', provider);
      const adapter = OidcAdapterFactory.getAdapter(provider, config);
      await adapter.authorize();
    } catch (err: any) {
      setError(safeProblemMessage(err));
      setIsLoading(false);
    }
  }, []);

  return { login, mfaPending, setMfaPending, isLoading, error, setError };
};
