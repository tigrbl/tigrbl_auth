
import React, { useState } from 'react';
import { Card, SocialButton, Input, Checkbox } from '../components/UI';
import { ConfigPanel } from '../components/ConfigPanel';
import { GOOGLE_ICON, GITHUB_ICON, KEYCLOAK_ICON } from '../constants';
import { AuthProvider } from '../types';
import { usePlatform } from '../hooks/usePlatform';

interface LoginPageProps {
  onLogin: (provider: AuthProvider, remember: boolean) => void;
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
    if (!email) {
      newErrors.email = 'Email is required';
    } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      newErrors.email = 'Invalid email format';
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
      onLogin(AuthProvider.GENERIC, remember);
    }
  };

  const navigateToRegister = () => {
    window.location.hash = '/register';
  };

  return (
    <div className="flex-grow flex items-center justify-center p-6">
      {showConfigPanel && (
        <ConfigPanel
          isOpen={isConfigOpen}
          onClose={() => setIsConfigOpen(false)}
          showBrandingSettings={showBrandingSettings}
          showAdapterSettings={showAdapterSettings}
        />
      )}

      <div className="w-full max-w-md space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">{platform.loginTitle}</h1>
          <p className="text-slate-500">{platform.loginSubtitle}</p>
        </div>

        <Card className="p-8">
          <div className="space-y-4">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-brand text-red-600 text-sm font-medium animate-in fade-in zoom-in-95">
                <div className="flex gap-2 text-xs font-bold uppercase">
                  <svg className="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{error}</span>
                </div>
              </div>
            )}

            <div className="grid grid-cols-1 gap-3">
              <SocialButton
                label="Google"
                icon={GOOGLE_ICON}
                onClick={() => onLogin(AuthProvider.GOOGLE, remember)}
                disabled={isLoading}
              />
              <SocialButton
                label="GitHub"
                icon={GITHUB_ICON}
                onClick={() => onLogin(AuthProvider.GITHUB, remember)}
                disabled={isLoading}
              />
              <SocialButton
                label="Keycloak"
                icon={KEYCLOAK_ICON}
                onClick={() => onLogin(AuthProvider.KEYCLOAK, remember)}
                disabled={isLoading}
              />
            </div>

            <div className="relative py-2">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-slate-100"></div>
              </div>
              <div className="relative flex justify-center text-[10px] uppercase tracking-widest">
                <span className="bg-white px-3 text-slate-400 font-bold">Identity Credentials</span>
              </div>
            </div>

            <form className="space-y-5" onSubmit={handleEmailSignIn}>
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
                placeholder="••••••••"
                value={password}
                error={errors.password}
                onChange={e => {
                  setPassword(e.target.value);
                  if (errors.password) setErrors(prev => ({...prev, password: undefined}));
                }}
              />

              <div className="flex items-center justify-between pt-1">
                <Checkbox label="Remember this device" checked={remember} onChange={setRemember} />
                <button
                  type="button"
                  onClick={() => window.location.hash = '/forgot-password'}
                  className="text-xs font-bold text-brand hover:opacity-80 transition-colors"
                >
                  Forgot Secret?
                </button>
              </div>

              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-brand text-white py-3 rounded-brand font-semibold shadow-lg shadow-brand/20 hover:opacity-90 active:scale-[0.99] transition-all disabled:opacity-50"
              >
                {isLoading ? 'Synchronizing...' : 'Authorize Session'}
              </button>
            </form>

            {showConfigPanel && (
              <button
                type="button"
                onClick={() => setIsConfigOpen(true)}
                className="w-full text-center text-[10px] text-slate-400 font-bold hover:text-brand transition-colors pt-4 flex items-center justify-center gap-2 uppercase tracking-tighter"
              >
                <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37a1.724 1.724 0 002.572-1.065z" />
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                {settingsLabel}
              </button>
            )}
          </div>
        </Card>

        <p className="text-center text-sm text-slate-500">
          New Identity? <button onClick={navigateToRegister} className="text-brand font-bold hover:underline">Create Account</button>
        </p>
      </div>
    </div>
  );
};
