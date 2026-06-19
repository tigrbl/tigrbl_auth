
import { OidcConfig } from '../types';
import { buildTigrblAuthOidcConfig } from '../services/tigrblAuthDiscovery';

export const getEnvVar = (key: string): string => {
  const lsKey = `tigrbl_auth_env_${key}`;
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

export const getTigrblAuthProviderConfig = async (): Promise<OidcConfig> => {
  const clientId = getEnvVar('VITE_TIGRBL_AUTH_CLIENT_ID') || 'tigrbl-auth-public-uix';
  return buildTigrblAuthOidcConfig(clientId);
};
