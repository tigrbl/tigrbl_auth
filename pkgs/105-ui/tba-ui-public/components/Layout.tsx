
import React from 'react';
import { usePlatform } from '../hooks/usePlatform';
import './Layout.css';

interface LayoutProps {
  children: React.ReactNode;
  user?: any;
  onLogout?: () => void | Promise<void>;
}

export const Layout: React.FC<LayoutProps> = ({ children, user, onLogout }) => {
  const platform = usePlatform();

  return (
    <div className="layout-shell">
      <header className="layout-header">
        <div className="layout-header-inner">
          <div
            className="layout-brand"
            onClick={() => window.location.hash = '#/'}
          >
            <div className="layout-brand-mark">
              {platform.logoLetter}
            </div>
            <span className="layout-brand-name">{platform.name}</span>
          </div>
          <nav>
            {user ? (
              <div className="layout-auth-nav">
                <div className="layout-user-chip">
                  {user.picture ? (
                    <img src={user.picture} className="layout-avatar" alt="Profile" />
                  ) : (
                    <div className="layout-avatar-fallback" aria-label="Profile">
                      {String(user.name || user.email || 'U').slice(0, 1).toUpperCase()}
                    </div>
                  )}
                  <span className="layout-user-name">{user.name}</span>
                </div>
                <button
                  onClick={() => void onLogout?.()}
                  className="layout-link-button"
                >
                  Sign Out
                </button>
              </div>
            ) : (
              <div className="layout-guest-nav">
                <button
                  onClick={() => window.location.hash = '#/login'}
                  className="layout-link-button"
                >
                  Sign In
                </button>
                <button
                  onClick={() => window.location.hash = '#/register'}
                  className="layout-join-button"
                >
                  Join {platform.name}
                </button>
              </div>
            )}
          </nav>
        </div>
      </header>
      <main className="layout-main">
        {children}
      </main>
      <footer className="layout-footer">
        <div className="layout-footer-inner">
          <div className="layout-footer-copy">
            &copy; {new Date().getFullYear()} {platform.name} {platform.footerText}
          </div>
          <div className="layout-footer-links">
            <button
              onClick={() => window.location.hash = '#/terms'}
              className="layout-footer-link"
            >
              Terms of Service
            </button>
            <button
              className="layout-footer-link"
            >
              Privacy Policy
            </button>
            <button
              className="layout-footer-link"
            >
              Contact Support
            </button>
          </div>
        </div>
      </footer>
    </div>
  );
};
