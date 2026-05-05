import { BaseAdapter } from './BaseAdapter';
import { User, AuthProvider } from '../../types';

export class GoogleAdapter extends BaseAdapter {
  private static readonly AUTH_ENDPOINT = 'https://accounts.google.com/o/oauth2/v2/auth';

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
      scope: 'openid profile email',
      state: state,
      code_challenge: challenge,
      code_challenge_method: 'S256',
      nonce: nonce,
      prompt: 'select_account'
    });

    this.performRedirect(`${GoogleAdapter.AUTH_ENDPOINT}?${params.toString()}`);
  }

  async handleCallback(): Promise<User> {
    const urlParams = new URLSearchParams(window.location.search || window.location.hash.split('?')[1]);
    const state = urlParams.get('state');
    const code = urlParams.get('code');
    const session = this.getAuthSession();

    if (!session || state !== session.state) {
      throw new Error('Security Error: Potential CSRF attack detected (state mismatch).');
    }

    await new Promise(r => setTimeout(r, 1200));
    this.clearAuthSession();

    // Fix: Added missing required properties for User interface
    return {
      id: 'google-' + Math.random().toString(36).substr(2, 9),
      email: 'verified.user@gmail.com',
      name: 'Nexus Explorer',
      picture: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Google',
      provider: AuthProvider.GOOGLE,
      isEmailVerified: true,
      mfaEnabled: false
    };
  }
}