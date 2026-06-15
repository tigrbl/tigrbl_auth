import React, { useState } from 'react';
import { Card, Input, Checkbox } from '../components/UI';
import { ConfigPanel } from '../components/ConfigPanel';
import { AuthProvider } from '../types';
import { usePlatform } from '../hooks/usePlatform';
import './LoginPage.css';

interface LoginPageProps {
  onLogin: (
    provider: AuthProvider,
    remember: boolean,
    credentials: { identifier: string; password: string },
  ) => void;
  isLoading: boolean;
  error: string | null;
}

export const LoginPage: React.FC<LoginPageProps> = ({ onLogin, isLoading, error }) => {
  const platform = usePlatform();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [remember, setRemember] = useState(false);
  const [errors, setErrors] = useState<{email?: string, password?: string}>({});
  const [isConfigOpen, setIsConfigOpen] = useState(false);
  const showBrandingSettings = platform.enableBrandingSettings;
  const showAdapterSettings = platform.enableAdapterSettings;
  const showConfigPanel = showBrandingSettings || showAdapterSettings;
  const settingsLabel = showBrandingSettings && showAdapterSettings
    ? 'Branding & Adapter Settings'
    : showBrandingSettings
      ? 'Branding Settings'
      : 'Adapter Settings';

  const validate = () => {
    const newErrors: {email?: string, password?: string} = {};
    if (!email.trim()) {
      newErrors.email = 'Identifier is required';
    } else if (email.trim().length < 3) {
      newErrors.email = 'Minimum 3 characters';
    }

    if (!password) {
      newErrors.password = 'Password is required';
    } else if (password.length < 8) {
      newErrors.password = 'Minimum 8 characters';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleEmailSignIn = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) {
      onLogin(AuthProvider.GENERIC, remember, {
        identifier: email.trim(),
        password,
      });
    }
  };

  const navigateToRegister = () => {
    window.location.hash = '#/register';
  };

  return (
    <div className="login-page">
      {showConfigPanel && (
        <ConfigPanel
          isOpen={isConfigOpen}
          onClose={() => setIsConfigOpen(false)}
          showBrandingSettings={showBrandingSettings}
          showAdapterSettings={showAdapterSettings}
        />
      )}

      <div className="login-shell u-animate-in">
        <div className="login-heading">
          <h1 className="login-title">{platform.loginTitle}</h1>
          <p className="login-subtitle">{platform.loginSubtitle}</p>
        </div>

        <Card className="login-card">
          <div className="login-card-stack">
            {error && (
              <div className="login-error u-animate-zoom">
                <div className="login-error-inner">
                  <svg className="login-error-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{error}</span>
                </div>
              </div>
            )}

            <form className="login-form" onSubmit={handleEmailSignIn}>
              <Input
                label="Identifier"
                placeholder="Email or Username"
                value={email}
                error={errors.email}
                onChange={e => {
                  setEmail(e.target.value);
                  if (errors.email) setErrors(prev => ({...prev, email: undefined}));
                }}
              />
              <Input
                label="Secret"
                type="password"
                placeholder="********"
                value={password}
                error={errors.password}
                onChange={e => {
                  setPassword(e.target.value);
                  if (errors.password) setErrors(prev => ({...prev, password: undefined}));
                }}
              />

              <div className="login-row">
                <Checkbox label="Remember this device" checked={remember} onChange={setRemember} />
                <button
                  type="button"
                  onClick={() => window.location.hash = '#/forgot-password'}
                  className="login-text-button"
                >
                  Forgot Secret?
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="login-submit-button"
              >
                {isLoading ? 'Synchronizing...' : 'Authorize Session'}
              </button>
            </form>

            {showConfigPanel && (
              <button
                type="button"
                onClick={() => setIsConfigOpen(true)}
                className="login-config-button"
              >
                <svg className="login-config-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {settingsLabel}
              </button>
            )}
          </div>
        </Card>

        <p className="login-footer">
          New Identity? <button onClick={navigateToRegister} className="login-footer-button">Create Account</button>
        </p>
      </div>
    </div>
  );
};
