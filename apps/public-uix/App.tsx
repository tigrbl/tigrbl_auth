
import React, { useState, useEffect } from 'react';
import { useAuth } from './hooks/useAuth';
import { Layout } from './components/Layout';
import { LoginPage } from './pages/LoginPage';
import { RegisterPage } from './pages/RegisterPage';
import { ProfilePage } from './pages/ProfilePage';
import { CallbackPage } from './pages/CallbackPage';
import { ForgotPasswordPage } from './pages/ForgotPasswordPage';
import { ResetPasswordPage } from './pages/ResetPasswordPage';
import { MfaPage } from './pages/MfaPage';
import { EmailVerificationPage } from './pages/EmailVerificationPage';
import { TermsOfServicePage } from './pages/TermsOfServicePage';
import { ConsentPage } from './pages/ConsentPage';
import { AuthProvider } from './types';
import { usePlatform } from './hooks/usePlatform';
import { parseConsentViewModel, sanitizePublicHashTarget } from './services/publicUxPolicy';
import {
  publicHashPath,
  resolveInitialPublicHash,
  resolvePublicRedirect,
  shouldNormalizeCallbackLocation,
} from './services/publicRouting';

const App: React.FC = () => {
  const [currentHash, setCurrentHash] = useState(() =>
    resolveInitialPublicHash(window.location.pathname, window.location.search, window.location.hash),
  );
  const {
    user,
    isAuthenticated,
    isLoading,
    error,
    login,
    register,
    logout,
    handleCallback,
    requestPasswordReset,
    resetPassword,
    resetRequestSent,
    mfaPending,
    verifyMfa,
    verifyEmail,
    resendVerification,
    resendSuccess
  } = useAuth();
  const platform = usePlatform();

  useEffect(() => {
    const handleHashChange = () => setCurrentHash(window.location.hash);
    window.addEventListener('hashchange', handleHashChange);
    return () => window.removeEventListener('hashchange', handleHashChange);
  }, []);

  useEffect(() => {
    if (window.location.pathname === '/callback') {
      const callbackHash = shouldNormalizeCallbackLocation(window.location.pathname, window.location.search);
      if (callbackHash) {
        window.history.replaceState(null, '', `/${callbackHash}`);
        setCurrentHash(callbackHash);
      }
    }
  }, []);

  const callbackTarget = sanitizePublicHashTarget(platform.postLoginRedirectUri, '#/profile');

  useEffect(() => {
    const target = resolvePublicRedirect({
      currentHash,
      isAuthenticated,
      user,
      callbackTarget,
      mfaPending,
    });
    if (target && window.location.hash !== target) {
      window.location.hash = target;
      setCurrentHash(target);
    }
  }, [callbackTarget, currentHash, isAuthenticated, mfaPending, user]);

  const renderContent = () => {
    const path = publicHashPath(currentHash);

    // MFA Flow takes precedence
    if (mfaPending) return <MfaPage onVerify={verifyMfa} isLoading={isLoading} error={error} />;

    switch (path) {
      case '#/callback':
        return <CallbackPage onHandleCallback={handleCallback} />;

      case '#/forgot-password':
        return <ForgotPasswordPage onRequestReset={requestPasswordReset} isLoading={isLoading} isSent={resetRequestSent} />;

      case '#/reset-password':
        return <ResetPasswordPage onReset={resetPassword} isLoading={isLoading} />;

      case '#/terms':
        return <TermsOfServicePage />;

      case '#/consent': {
        const consent = parseConsentViewModel(currentHash, callbackTarget, '#/login');
        return (
          <ConsentPage
            approveTarget={consent.approveTarget}
            cancelTarget={consent.cancelTarget}
            clientName={consent.clientName}
            scopes={consent.scopes}
          />
        );
      }

      case '#/verify-email':
        return (
          <EmailVerificationPage
            email={user?.email || 'your email'}
            onVerify={verifyEmail}
            onResend={resendVerification}
            resendSuccess={resendSuccess || false}
            isLoading={isLoading}
          />
        );

      case '#/register':
        if (isAuthenticated) { return null; }
        return <RegisterPage onRegister={register} isLoading={isLoading} error={error} />;

      case '#/login':
        if (isAuthenticated) { return null; }
        return <LoginPage onLogin={login} isLoading={isLoading} error={error} />;

      case '#/profile':
        if (!isAuthenticated) {
          return null;
        }
        return user ? <ProfilePage user={user} /> : null;

      case '#/':
      default: {
        return isAuthenticated ? null : <LoginPage onLogin={login} isLoading={isLoading} error={error} />;
      }
    }
  };

  return (
    <Layout user={user && user.isEmailVerified ? user : null} onLogout={logout}>
      {renderContent()}
    </Layout>
  );
};

export default App;
