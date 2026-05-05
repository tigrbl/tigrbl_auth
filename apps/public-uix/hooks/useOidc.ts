
import { AuthProvider, OidcConfig } from '../types';
import { buildTigrblAuthOidcConfig } from '../services/tigrblAuthDiscovery';

export const getEnvVar = (key: string): string => {
  const lsKey = `nexus_env_${key}`;
  try {
    const lsVal = localStorage.getItem(lsKey);
    if (lsVal) return lsVal;
  } catch { /* ignore */ }
  const viteEnv = (import.meta as any).env;
  if (viteEnv && typeof viteEnv[key] === 'string' && viteEnv[key]) return viteEnv[key];
  try {
    const penv = (process as any).env;
    if (penv && typeof penv[key] === 'string' && penv[key]) return penv[key];
  } catch { /* ignore */ }
  return '';
};

export const getProviderConfig = (provider: AuthProvider): OidcConfig => {
  const configuredRedirectUri = getEnvVar('VITE_OIDC_CALLBACK_URL');
  return {
    clientId: getEnvVar(`VITE_${provider.toUpperCase()}_CLIENT_ID`),
    authority: provider === AuthProvider.GOOGLE ? 'https://accounts.google.com' : getEnvVar(`VITE_${provider.toUpperCase()}_AUTHORITY`),
    redirectUri: configuredRedirectUri || `${window.location.origin}/#/callback`,
    scope: provider === AuthProvider.GITHUB ? 'read:user user:email' : 'openid profile email'
  };
};

export const getTigrblAuthProviderConfig = async (): Promise<OidcConfig> => {
  const clientId = getEnvVar('VITE_TIGRBL_AUTH_CLIENT_ID') || getEnvVar('VITE_GENERIC_CLIENT_ID') || 'tigrbl-auth-public-uix';
  return buildTigrblAuthOidcConfig(clientId);
};
