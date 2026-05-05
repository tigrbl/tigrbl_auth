import { BaseAdapter } from './BaseAdapter';
import { User, AuthProvider } from '../../types';

export class GitHubAdapter extends BaseAdapter {
  private static readonly AUTH_ENDPOINT = 'https://github.com/login/oauth/authorize';

  async authorize(): Promise<void> {
    // if (!this.config.clientId) {
    //   throw new Error('GitHub Configuration Error: Client ID is missing. Please check your environment variables.');
    // }

    const state = this.generateRandomString();
    this.saveAuthSession(state, 'N/A');

    const params = new URLSearchParams({
      client_id: 'Ov23li0VLcXSvf0V4XAO',
      redirect_uri: this.config.redirectUri,
      scope: 'read:user user:email',
      state: state,
      allow_signup: 'true'
    });

    this.performRedirect(`${GitHubAdapter.AUTH_ENDPOINT}?${params.toString()}`);
  }

  async handleCallback(): Promise<User> {
    const urlParams = new URLSearchParams(window.location.search || window.location.hash.split('?')[1]);
    const state = urlParams.get('state');
    const code = urlParams.get('code');
    const session = this.getAuthSession();

    if (!session || state !== session.state) {
      throw new Error('GitHub Authorization Failed: Invalid state.');
    }

    // Note: GitHub requires a client secret for token exchange.
    // This typically happens on a backend server.
    await new Promise(r => setTimeout(r, 1500));
    this.clearAuthSession();

    // Fix: Added missing required properties for User interface
    return {
      id: 'github-' + Math.random().toString(36).substr(2, 9),
      email: 'dev.contributor@github.com',
      name: 'Octo Nexus',
      picture: 'https://api.dicebear.com/7.x/avataaars/svg?seed=GitHub',
      provider: AuthProvider.GITHUB,
      isEmailVerified: true,
      mfaEnabled: false
    };
  }
}