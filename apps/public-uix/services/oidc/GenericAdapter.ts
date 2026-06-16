import { BaseAdapter } from './BaseAdapter';
import { User, AuthProvider } from '../../types';
import { safeProblemMessage } from '../tigrblAuthDiscovery';

const parseJsonResponse = async (response: Response): Promise<Record<string, any>> => {
  try {
    const parsed = await response.json();
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch {
    return {};
  }
};

const responseProblem = async (response: Response, fallback: string): Promise<string> => {
  const body = await parseJsonResponse(response);
  return String(body.title || body.detail || body.error_description || body.error || fallback);
};

const hasScope = (scope: string | undefined, value: string): boolean => {
  return new Set((scope || '').split(/\s+/).filter(Boolean)).has(value);
};

const decodeBase64UrlJson = (value: string): Record<string, unknown> | null => {
  try {
    const base64 = value.replace(/-/g, '+').replace(/_/g, '/');
    const padded = base64.padEnd(base64.length + ((4 - (base64.length % 4)) % 4), '=');
    const json = decodeURIComponent(
      Array.from(atob(padded))
        .map((char) => `%${char.charCodeAt(0).toString(16).padStart(2, '0')}`)
        .join(''),
    );
    const parsed = JSON.parse(json);
    return parsed && typeof parsed === 'object' ? parsed : null;
  } catch {
    return null;
  }
};

const decodeJwtClaims = (token: string): Record<string, unknown> => {
  const parts = token.split('.');
  if (parts.length < 2 || !parts[1]) {
    return {};
  }
  return decodeBase64UrlJson(parts[1]) || {};
};

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

      const accessToken = typeof tokens.access_token === 'string' ? tokens.access_token : '';
      const idToken = typeof tokens.id_token === 'string' ? tokens.id_token : '';
      if (!accessToken) {
        throw new Error('OIDC callback did not return an access token for UserInfo hydration.');
      }
      if (!this.config.userinfoEndpoint) {
        throw new Error('OIDC discovery did not provide a UserInfo endpoint.');
      }

      const userInfoResponse = await fetch(this.config.userinfoEndpoint, {
        headers: {
          Accept: 'application/json',
          Authorization: `Bearer ${accessToken}`,
        },
      });
      if (!userInfoResponse.ok) {
        throw new Error(await responseProblem(userInfoResponse, `UserInfo failed with HTTP ${userInfoResponse.status}`));
      }
      const profile = await parseJsonResponse(userInfoResponse);
      const subject = typeof profile.sub === 'string' && profile.sub.trim()
        ? profile.sub
        : typeof profile.id === 'string' && profile.id.trim()
          ? profile.id
          : '';
      if (!subject) {
        throw new Error('UserInfo response did not include a subject claim.');
      }
      const email = typeof profile.email === 'string' ? profile.email : '';
      if (hasScope(this.config.scope, 'email') && !email) {
        throw new Error('UserInfo response did not include the requested email claim.');
      }
      const idTokenClaims = decodeJwtClaims(idToken);
      const accessTokenClaims = decodeJwtClaims(accessToken);

      return {
        id: subject,
        email,
        name: String(profile.name || profile.preferred_username || profile.email || subject),
        provider: AuthProvider.GENERIC,
        isEmailVerified: profile.email_verified !== false,
        mfaEnabled: false,
        picture: typeof profile.picture === 'string' ? profile.picture : undefined,
        oidcContext: {
          id_token: idTokenClaims,
          access_token: accessTokenClaims,
          userinfo: profile,
          client: {
            provider: AuthProvider.GENERIC,
            client_id: this.config.clientId,
            issuer: this.config.authority,
            scope: this.config.scope || 'openid profile email',
            token_type: typeof tokens.token_type === 'string' ? tokens.token_type : undefined,
          },
          authorization_request: {
            nonce: session.nonce,
            redirect_uri: this.config.redirectUri,
          },
        },
      };
    } catch (e) {
      throw new Error(safeProblemMessage(e));
    }
  }
}
