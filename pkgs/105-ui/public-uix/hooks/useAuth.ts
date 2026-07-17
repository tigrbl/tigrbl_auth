
import { useAuthSession } from './useAuthSession';
import { useLogin } from './useLogin';
import { useRegister } from './useRegister';
import { useMfa } from './useMfa';
import { useEmailVerification } from './useEmailVerification';
import { usePasswordRecovery } from './usePasswordRecovery';
import { useOidcActions } from './useOidcActions';

/**
 * Aggregator Hook (Facade)
 * Composes specialized hooks into a unified interface for the App component.
 */
export const useAuth = () => {
  const session = useAuthSession();

  const loginActions = useLogin();
  const registrationActions = useRegister(session.updateSession);
  const mfaActions = useMfa((user) => {
    session.updateSession(user);
    loginActions.setMfaPending(false);
  });
  const verificationActions = useEmailVerification(session.user, session.updateSession);
  const recoveryActions = usePasswordRecovery();
  const oidcActions = useOidcActions(session.updateSession);

  // Combine error and loading states for a simple UI consumption
  const isLoading =
    loginActions.isLoading ||
    registrationActions.isLoading ||
    mfaActions.isLoading ||
    verificationActions.isLoading ||
    recoveryActions.isLoading;

  const error =
    loginActions.error ||
    registrationActions.error ||
    mfaActions.error ||
    verificationActions.error ||
    recoveryActions.error;

  return {
    // State
    user: session.user,
    isAuthenticated: session.isAuthenticated,
    mfaPending: loginActions.mfaPending,
    verificationEmailSent: registrationActions.verificationEmailSent,
    resendSuccess: verificationActions.resendSuccess,
    resetRequestSent: recoveryActions.resetRequestSent,
    isLoading,
    error,

    // Actions
    login: loginActions.login,
    logout: session.logout,
    register: registrationActions.register,
    verifyMfa: mfaActions.verifyMfa,
    verifyEmail: verificationActions.verifyEmail,
    resendVerification: verificationActions.resendVerificationEmail,
    requestPasswordReset: recoveryActions.requestPasswordReset,
    resetPassword: recoveryActions.resetPassword,
    handleCallback: oidcActions.handleCallback
  };
};
