
import { useState, useCallback } from 'react';
import { User } from '../types';

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
      await new Promise(r => setTimeout(r, 2000));
      const updatedUser = { ...currentUser, isEmailVerified: true };
      onVerified(updatedUser);
      window.location.hash = '/profile';
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [currentUser, onVerified]);

  const resendVerificationEmail = useCallback(async () => {
    setIsLoading(true);
    setResendSuccess(false);
    try {
      await new Promise(r => setTimeout(r, 1500));
      setResendSuccess(true);
    } catch (err: any) {
      setError('Failed to resend verification email.');
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { verifyEmail, resendVerificationEmail, resendSuccess, isLoading, error };
};
