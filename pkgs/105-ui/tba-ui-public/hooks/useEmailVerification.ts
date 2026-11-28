
import { useState, useCallback } from 'react';
import { User } from '../types';
import { postDiscoveredJson, safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const useEmailVerification = (currentUser: User | null, onVerified: (user: User) => void) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resendSuccess, setResendSuccess] = useState(false);

  const verifyEmail = useCallback(async () => {
    if (!currentUser) {
      setError('No user session found.');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      await postDiscoveredJson('email_verification_endpoint', 'email verification', {
        user_id: currentUser.id,
        email: currentUser.email,
      });
      const updatedUser = { ...currentUser, isEmailVerified: true };
      onVerified(updatedUser);
      window.location.hash = '#/profile';
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, [currentUser, onVerified]);

  const resendVerificationEmail = useCallback(async () => {
    setIsLoading(true);
    setResendSuccess(false);
    try {
      await postDiscoveredJson('email_verification_resend_endpoint', 'email verification resend', {
        user_id: currentUser?.id,
        email: currentUser?.email,
      });
      setResendSuccess(true);
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, [currentUser]);

  return { verifyEmail, resendVerificationEmail, resendSuccess, isLoading, error };
};
