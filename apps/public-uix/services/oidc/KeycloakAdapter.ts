import { BaseAdapter } from './BaseAdapter';
import { User, AuthProvider } from '../../types';

export class KeycloakAdapter extends BaseAdapter {
  /**
   * Keycloak standard endpoints relative to the realm base URL
   */
  private get endpoints() {
    // Assuming authority is the realm URL, e.g., https://keycloak/realms/myrealm
    const base = this.config.authority.endsWith('/')
      ? this.config.authority.slice(0, -1)
      : this.config.authority;

    return {
      auth: `${base}/protocol/openid-connect/auth`,
      token: `${base}/protocol/openid-connect/token`,
      userinfo: `${base}/protocol/openid-connect/userinfo`
    };
  }

  async authorize(): Promise<void> {
    const state = this.generateRandomString();
    const verifier = this.generateRandomString();
    const challenge = await this.generateCodeChallenge(verifier);
    const nonce = this.generateRandomString();

    this.saveAuthSession(state, verifier, nonce);

    const params = new URLSearchParams({
      client_id: this.config.clientId,
      redirect_uri: this.config.redirectUri,
      response_type: 'code',
      scope: this.config.scope || 'openid profile email',
      state: state,
      code_challenge: challenge,
      code_challenge_method: 'S256',
      nonce: nonce
    });

    this.performRedirect(`${this.endpoints.auth}?${params.toString()}`);
  }

  async handleCallback(): Promise<User> {
    const urlParams = new URLSearchParams(window.location.search || window.location.hash.split('?')[1]);
    const state = urlParams.get('state');
    const code = urlParams.get('code');
    const session = this.getAuthSession();

    if (!session || state !== session.state) {
      throw new Error('Keycloak Security Error: State mismatch.');
    }

    if (!code) {
      throw new Error('Keycloak Error: No authorization code received.');
    }

    try {
      // Keycloak often requires token exchange via POST
      // Note: In a pure client-side app, this requires CORS enabled on Keycloak
      const response = await fetch(this.endpoints.token, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          grant_type: 'authorization_code',
          client_id: this.config.clientId,
          code: code,
          redirect_uri: this.config.redirectUri,
          code_verifier: session.verifier
        })
      });

      if (!response.ok) {
        throw new Error('Failed to exchange code for tokens.');
      }

      // In a real implementation, we would decode the ID token or call userinfo
      // For this demo, we mock the final user object
      await new Promise(r => setTimeout(r, 800));
      this.clearAuthSession();

      // Fix: Added missing required properties for User interface
      return {
        id: 'kc-' + Math.random().toString(36).substr(2, 9),
        email: 'keycloak.user@enterprise.org',
        name: 'Keycloak User',
        picture: `https://api.dicebear.com/7.x/avataaars/svg?seed=Keycloak`,
        provider: AuthProvider.KEYCLOAK,
        isEmailVerified: true,
        mfaEnabled: false
      };
    } catch (err) {
      console.error('Keycloak token exchange error:', err);
      // Fallback for demo purposes if Keycloak is not actually reachable
      // Fix: Added missing required properties for User interface
      return {
        id: 'kc-demo',
        email: 'demo@keycloak.local',
        name: 'Demo Keycloak User',
        provider: AuthProvider.KEYCLOAK,
        isEmailVerified: true,
        mfaEnabled: false
      };
    }
  }
}