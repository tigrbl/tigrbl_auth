
import { useState, useCallback } from 'react';
import { User, AuthProvider } from '../types';

export const useRegister = (onUserCreated: (user: User) => void) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [verificationEmailSent, setVerificationEmailSent] = useState(false);

  const register = useCallback(async (name: string, email: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await new Promise(resolve => setTimeout(resolve, 1500));
      const user: User = {
        id: 'nexus-' + Math.random().toString(36).substr(2, 9),
        email,
        name,
        picture: `https://api.dicebear.com/7.x/avataaars/svg?seed=${name}`,
        provider: AuthProvider.GENERIC,
        isEmailVerified: false,
        mfaEnabled: false
      };
      onUserCreated(user);
      setVerificationEmailSent(true);
      window.location.hash = '/verify-email';
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [onUserCreated]);

  return { register, verificationEmailSent, isLoading, error };
};
