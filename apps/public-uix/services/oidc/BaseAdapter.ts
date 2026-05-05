import { OidcConfig, User } from '../../types';

export abstract class BaseAdapter {
  protected config: OidcConfig;

  constructor(config: OidcConfig) {
    this.config = config;
  }

  abstract authorize(): Promise<void>;
  abstract handleCallback(): Promise<User>;

  /**
   * Opens a popup for OIDC authorization to bypass iframe restrictions.
   */
  protected openAuthPopup(url: string): Promise<void> {
    return new Promise((resolve, reject) => {
      console.log(`[BaseAdapter] Attempting to open auth popup for URL: ${url}`);

      const width = 600;
      const height = 700;
      const left = window.screen.width / 2 - width / 2;
      const top = window.screen.height / 2 - height / 2;

      const popup = window.open(
        url,
        'oidc-auth-popup',
        `width=${width},height=${height},left=${left},top=${top},status=no,location=no,menubar=no`
      );

      if (!popup) {
        console.error('[BaseAdapter] Popup was blocked by the browser.');
        reject(new Error('Popup blocked. Please enable popups for this site in your browser settings.'));
        return;
      }

      console.log('[BaseAdapter] Popup opened successfully. Monitoring for completion...');

      // Check for closure
      const timer = setInterval(() => {
        if (popup.closed) {
          clearInterval(timer);
          console.log('[BaseAdapter] Popup closed by user or system.');
          resolve();
        }
      }, 1000);
    });
  }

  protected performRedirect(url: string): void {
    this.openAuthPopup(url).catch(err => {
      console.warn('[BaseAdapter] Popup auth failed or blocked, falling back to full page redirect:', err);
      // If we're in an iframe environment, full page redirect might still fail due to IDP CSP
      window.location.href = url;
    });
  }

  protected generateRandomString(length: number = 32): string {
    const array = new Uint8Array(length);
    window.crypto.getRandomValues(array);
    return Array.from(array, byte => byte.toString(16).padStart(2, '0')).join('');
  }

  protected async generateCodeChallenge(verifier: string): Promise<string> {
    const encoder = new TextEncoder();
    const data = encoder.encode(verifier);
    const digest = await window.crypto.subtle.digest('SHA-256', data);
    return btoa(String.fromCharCode(...new Uint8Array(digest)))
      .replace(/\+/g, '-')
      .replace(/\//g, '_')
      .replace(/=+$/, '');
  }

  protected saveAuthSession(state: string, verifier: string, nonce?: string): void {
    const session = {
      state,
      verifier,
      nonce,
      timestamp: Date.now()
    };
    localStorage.setItem(`oidc_session_${this.constructor.name}`, JSON.stringify(session));
  }

  protected getAuthSession(): { state: string; verifier: string; nonce?: string; timestamp: number } | null {
    const raw = localStorage.getItem(`oidc_session_${this.constructor.name}`);
    if (!raw) return null;
    return JSON.parse(raw);
  }

  protected clearAuthSession(): void {
    localStorage.removeItem(`oidc_session_${this.constructor.name}`);
  }

  protected verifyState(receivedState: string): boolean {
    const session = this.getAuthSession();
    return !!session && session.state === receivedState;
  }
}