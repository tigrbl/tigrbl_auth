
import { OidcConfig, AuthProvider } from '../types';
import { BaseAdapter } from './oidc/BaseAdapter';
import { GenericAdapter } from './oidc/GenericAdapter';

export type { BaseAdapter };

/**
 * Factory for OIDC Adapters
 */
export class OidcAdapterFactory {
  static getAdapter(provider: AuthProvider, config: OidcConfig): BaseAdapter {
    if (provider !== AuthProvider.GENERIC) {
      throw new Error(`Provider ${provider} is not governed by tigrbl_auth discovery.`);
    }
    return new GenericAdapter(config);
  }
}
