
import { useState, useCallback } from 'react';
import { User, AuthProvider } from '../types';
import { postDiscoveredJson, safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const useMfa = (onMfaSuccess: (user: User) => void) => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const verifyMfa = useCallback(async (code: string) => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await postDiscoveredJson<Partial<User>>('mfa_verification_endpoint', 'MFA verification', { code });
      const user: User = {
        id: String(response?.id || 'tigrbl-auth-user'),
        email: String(response?.email || ''),
        name: String(response?.name || 'Verified tigrbl_auth user'),
        provider: AuthProvider.GENERIC,
        isEmailVerified: response?.isEmailVerified !== false,
        mfaEnabled: true,
        picture: typeof response?.picture === 'string' ? response.picture : undefined,
      };
      onMfaSuccess(user);
      window.location.hash = '#/profile';
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, [onMfaSuccess]);

  return { verifyMfa, isLoading, error };
};
