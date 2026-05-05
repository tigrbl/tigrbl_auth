
import { useState, useCallback } from 'react';
import { User, AuthProvider } from '../types';

export const useMfa = (onMfaSuccess: (user: User) => void) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const verifyMfa = useCallback(async (code: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await new Promise(r => setTimeout(r, 1500));
      if (code === '123456') {
        const mockUser: User = {
          id: 'ent-' + Math.random().toString(36).substr(2, 9),
          email: 'enterprise.user@company.com',
          name: 'Verified Enterprise User',
          provider: AuthProvider.GENERIC,
          isEmailVerified: true,
          mfaEnabled: true,
          picture: 'https://api.dicebear.com/7.x/avataaars/svg?seed=Enterprise'
        };
        onMfaSuccess(mockUser);
        window.location.hash = '/profile';
      } else {
        throw new Error('Invalid MFA code. Please try again.');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, [onMfaSuccess]);

  return { verifyMfa, isLoading, error };
};
