
import { OidcConfig, AuthProvider } from '../types';
import { BaseAdapter } from './oidc/BaseAdapter';
import { GoogleAdapter } from './oidc/GoogleAdapter';
import { GitHubAdapter } from './oidc/GitHubAdapter';
import { GenericAdapter } from './oidc/GenericAdapter';
import { KeycloakAdapter } from './oidc/KeycloakAdapter';

export type { BaseAdapter };

/**
 * Factory for OIDC Adapters
 */
export class OidcAdapterFactory {
  static getAdapter(provider: AuthProvider, config: OidcConfig): BaseAdapter {
    switch (provider) {
      case AuthProvider.GOOGLE:
        return new GoogleAdapter(config);
      case AuthProvider.GITHUB:
        return new GitHubAdapter(config);
      case AuthProvider.GENERIC:
        return new GenericAdapter(config);
      case AuthProvider.KEYCLOAK:
        return new KeycloakAdapter(config);
      default:
        throw new Error(`Provider ${provider} not supported`);
    }
  }
}
