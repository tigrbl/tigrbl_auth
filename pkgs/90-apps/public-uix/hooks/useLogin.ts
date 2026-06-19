
import { useState, useCallback } from 'react';
import { AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getTigrblAuthProviderConfig } from './useOidc';
import { safeProblemMessage } from '../services/tigrblAuthDiscovery';
import {
  buildBrowserJsonRequestInit,
  getOrCreateCsrfToken,
} from '../services/publicUxPolicy';

interface LoginCredentials {
  identifier: string;
  password: string;
}

async function createBrowserSession(credentials: LoginCredentials): Promise<void> {
  const config = await getTigrblAuthProviderConfig();
  if (!config.loginEndpoint) {
    throw new Error('login is not available from the discovered tigrbl_auth endpoints.');
  }
  const response = await fetch(
    config.loginEndpoint,
    buildBrowserJsonRequestInit(credentials, getOrCreateCsrfToken()),
  );
  if (!response.ok) {
    let message = `HTTP ${response.status}`;
    try {
      const body = await response.json();
      message = body.title || body.detail || body.error_description || body.error || message;
    } catch {
      // Keep the status-based message when the response is not JSON.
    }
    throw new Error(safeProblemMessage(message));
  }
}

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

  const login = useCallback(async (
    provider: AuthProvider,
    remember: boolean = false,
    credentials?: LoginCredentials,
  ) => {
    setIsLoading(true);
    setError(null);
    try {
      const config = await getTigrblAuthProviderConfig();
      if (credentials) {
        await createBrowserSession(credentials);
      }
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
