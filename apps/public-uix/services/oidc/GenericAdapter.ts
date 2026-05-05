import { BaseAdapter } from './BaseAdapter';
import { User, AuthProvider } from '../../types';
import { safeProblemMessage } from '../tigrblAuthDiscovery';

export class GenericAdapter extends BaseAdapter {
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

    if (!this.config.authorizationEndpoint) {
      throw new Error('login is not available from the discovered tigrbl_auth endpoints.');
    }
    this.performRedirect(`${this.config.authorizationEndpoint}?${params.toString()}`);
  }

  async handleCallback(): Promise<User> {
    const urlParams = new URLSearchParams(window.location.search || window.location.hash.split('?')[1]);
    const code = urlParams.get('code');
    const state = urlParams.get('state');
    const session = this.getAuthSession();

    if (!code || !state || state !== session?.state) {
      throw new Error('Identity verification failed: State mismatch or missing code.');
    }

    try {
      if (!this.config.tokenEndpoint) {
        throw new Error('callback is not available from the discovered tigrbl_auth endpoints.');
      }
      const tokenResponse = await fetch(this.config.tokenEndpoint, {
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

      const tokens = await tokenResponse.json();
      if (!tokenResponse.ok) {
        throw new Error(safeProblemMessage(tokens.error_description || tokens.error || `HTTP ${tokenResponse.status}`));
      }
      this.clearAuthSession();

      let profile: Record<string, any> = {};
      if (this.config.userinfoEndpoint && tokens.access_token) {
        const userInfoResponse = await fetch(this.config.userinfoEndpoint, {
          headers: {
            Accept: 'application/json',
            Authorization: `Bearer ${tokens.access_token}`,
          },
        });
        if (userInfoResponse.ok) {
          profile = await userInfoResponse.json();
        }
      }

      return {
        id: String(profile.sub || profile.id || 'tigrbl-auth-user'),
        email: String(profile.email || ''),
        name: String(profile.name || profile.preferred_username || profile.email || 'tigrbl_auth user'),
        provider: AuthProvider.GENERIC,
        isEmailVerified: profile.email_verified !== false,
        mfaEnabled: false,
        picture: typeof profile.picture === 'string' ? profile.picture : undefined,
      };
    } catch (e) {
      throw new Error(safeProblemMessage(e));
    }
  }
}
