import { useState, useCallback } from 'react';
import { AuthProvider } from '../types';
import { OidcAdapterFactory } from '../services/oidc-adapters';
import { getTigrblAuthProviderConfig } from './useOidc';
import { safeProblemMessage } from '../services/tigrblAuthDiscovery';
import {
  buildBrowserJsonRequestInit,
  getOrCreateCsrfToken,
} from '../services/publicUxPolicy';
import { resolveAuthorizationContinuation } from '../services/publicRouting';

interface LoginCredentials {
  identifier: string;
  password: string;
}

interface LoginProblem {
  title?: string;
  detail?: string;
  error_description?: string;
  error?: string;
}

async function readLoginProblem(response: Response): Promise<LoginProblem> {
  try {
    return await response.json() as LoginProblem;
  } catch {
    return {};
  }
}

async function createBrowserSession(credentials: LoginCredentials): Promise<boolean> {
  const config = await getTigrblAuthProviderConfig();
  if (!config.loginEndpoint) {
    throw new Error('login is not available from the discovered tigrbl_auth endpoints.');
  }
  const response = await fetch(
    config.loginEndpoint,
    buildBrowserJsonRequestInit(credentials, getOrCreateCsrfToken()),
  );
  if (response.ok) {
    return false;
  }
  const body = await readLoginProblem(response);
  if (response.status === 428 && body.error === 'password_change_required') {
    return true;
  }
  throw new Error(safeProblemMessage(
    body.title || body.detail || body.error_description || body.error || 'HTTP ' + response.status,
  ));
}

async function continueAuthorization(provider: AuthProvider): Promise<void> {
  const continuation = resolveAuthorizationContinuation(
    window.location.pathname,
    window.location.search,
  );
  if (continuation) {
    window.location.assign(continuation);
    return;
  }
  const config = await getTigrblAuthProviderConfig();
  localStorage.setItem('tigrbl_auth_pending_provider', provider);
  const adapter = OidcAdapterFactory.getAdapter(provider, config);
  await adapter.authorize();
}

export const useLogin = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [requiredPasswordChange, setRequiredPasswordChange] = useState<LoginCredentials | null>(null);
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
      if (credentials) {
        const passwordChangeRequired = await createBrowserSession(credentials);
        if (passwordChangeRequired) {
          setRequiredPasswordChange(credentials);
          setIsLoading(false);
          return;
        }
      }
      await continueAuthorization(provider);
    } catch (err: any) {
      setError(safeProblemMessage(err));
      setIsLoading(false);
    }
  }, []);

  const changeRequiredPassword = useCallback(async (newPassword: string) => {
    if (!requiredPasswordChange) {
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const config = await getTigrblAuthProviderConfig();
      if (!config.loginEndpoint) {
        throw new Error('password change is not available from the discovered tigrbl_auth endpoints.');
      }
      const endpoint = new URL(config.loginEndpoint);
      endpoint.pathname = endpoint.pathname.replace(/\/+$/, '') + '/password-change';
      const response = await fetch(
        endpoint.toString(),
        buildBrowserJsonRequestInit(
          {
            current_password: requiredPasswordChange.password,
            new_password: newPassword,
          },
          getOrCreateCsrfToken(),
        ),
      );
      if (!response.ok) {
        const body = await readLoginProblem(response);
        throw new Error(safeProblemMessage(
          body.title || body.detail || body.error_description || body.error || 'HTTP ' + response.status,
        ));
      }
      const credentials = {
        identifier: requiredPasswordChange.identifier,
        password: newPassword,
      };
      setRequiredPasswordChange(null);
      if (await createBrowserSession(credentials)) {
        throw new Error('The identity provider did not clear the required password change.');
      }
      await continueAuthorization(AuthProvider.GENERIC);
    } catch (err: any) {
      setError(safeProblemMessage(err));
      setIsLoading(false);
    }
  }, [requiredPasswordChange]);

  return {
    login,
    changeRequiredPassword,
    passwordChangeRequired: requiredPasswordChange !== null,
    mfaPending,
    setMfaPending,
    isLoading,
    error,
    setError,
  };
};
