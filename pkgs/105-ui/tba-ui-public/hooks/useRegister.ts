
import { useState, useCallback } from 'react';
import { User, AuthProvider } from '../types';
import { postDiscoveredJson, safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const useRegister = (onUserCreated: (user: User) => void) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [verificationEmailSent, setVerificationEmailSent] = useState(false);

  const register = useCallback(async (name: string, email: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await postDiscoveredJson<Partial<User>>('registration_endpoint', 'registration', {
        name,
        email,
      });
      const user: User = {
        id: String(response?.id || email),
        email: String(response?.email || email),
        name: String(response?.name || name),
        picture: typeof response?.picture === 'string' ? response.picture : undefined,
        provider: AuthProvider.GENERIC,
        isEmailVerified: response?.isEmailVerified === true,
        mfaEnabled: response?.mfaEnabled === true
      };
      onUserCreated(user);
      setVerificationEmailSent(true);
      window.location.hash = '#/verify-email';
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, [onUserCreated]);

  return { register, verificationEmailSent, isLoading, error };
};
