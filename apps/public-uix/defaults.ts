
import { PlatformConfig } from './types';

/**
 * Utility to resolve environment variables or local storage overrides
 */
const resolveEnv = (key: string, fallback: string): string => {
  if (typeof window !== 'undefined') {
    const local = localStorage.getItem(`tigrbl_auth_platform_${key.toLowerCase().replace('vite_platform_', '')}`);
    if (local) return local;
  }

  const env = (import.meta as any).env;
  if (env && env[key]) return env[key];

  try {
    const penv = (process as any).env;
    if (penv && penv[key]) return penv[key];
  } catch { /* node env not available */ }

  return fallback;
};

const resolveEnvBoolean = (key: string, fallback: boolean): boolean => {
  return resolveEnv(key, fallback ? 'true' : 'false').toLowerCase() === 'true';
};

export const DEFAULT_PLATFORM_CONFIG: PlatformConfig = {
  name: resolveEnv('VITE_PLATFORM_NAME', 'tigrbl_auth'),
  logoLetter: resolveEnv('VITE_PLATFORM_LOGOLETTER', 'T'),

  // Visuals
  primaryColor: resolveEnv('VITE_PLATFORM_PRIMARYCOLOR', '#4f46e5'),
  secondaryColor: resolveEnv('VITE_PLATFORM_SECONDARYCOLOR', '#1e1b4b'),
  backgroundColor: resolveEnv('VITE_PLATFORM_BACKGROUNDCOLOR', '#f8fafc'),
  borderRadius: resolveEnv('VITE_PLATFORM_BORDERRADIUS', '12px'),

  // Navigation
  postLoginRedirectUri: resolveEnv(
    'VITE_TIGRBL_AUTH_POST_LOGIN_REDIRECT',
    resolveEnv('VITE_PLATFORM_POSTLOGINREDIRECTURI', '#/profile')
  ),

  // Labels
  loginTitle: resolveEnv('VITE_PLATFORM_LOGINTITLE', 'Sign in'),
  loginSubtitle: resolveEnv('VITE_PLATFORM_LOGINSUBTITLE', 'Use your tigrbl_auth identity provider.'),
  registerTitle: resolveEnv('VITE_PLATFORM_REGISTERTITLE', 'Create an account'),
  registerSubtitle: resolveEnv('VITE_PLATFORM_REGISTERSUBTITLE', 'Register with the configured public identity surface.'),
  footerText: resolveEnv('VITE_PLATFORM_FOOTERTEXT', 'OIDC and OAuth public UIX for tigrbl_auth.'),
  supportEmail: resolveEnv('VITE_PLATFORM_SUPPORTEMAIL', 'support@example.com'),

  // Embed Metadata
  embedTitle: resolveEnv('VITE_PLATFORM_EMBED_TITLE', 'tigrbl_auth Public UIX'),
  embedDescription: resolveEnv(
    'VITE_PLATFORM_EMBED_DESCRIPTION',
    'A public OAuth and OIDC UIX adapted to the tigrbl_auth public contract and discovery metadata.'
  ),
  embedImage: resolveEnv('VITE_PLATFORM_EMBED_IMAGE', '/favicon.svg'),
  embedUrl: resolveEnv('VITE_PLATFORM_EMBED_URL', ''),

  // Feature Flags
  enableBrandingSettings: resolveEnvBoolean('VITE_PLATFORM_ENABLE_BRANDING_SETTINGS', false),
  enableAdapterSettings: resolveEnvBoolean('VITE_PLATFORM_ENABLE_ADAPTER_SETTINGS', false)
};
