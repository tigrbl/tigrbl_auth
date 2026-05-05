
import { useState, useCallback } from 'react';
import { postDiscoveredJson, safeProblemMessage } from '../services/tigrblAuthDiscovery';

export const usePasswordRecovery = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resetRequestSent, setResetRequestSent] = useState(false);

  const requestPasswordReset = useCallback(async (email: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await postDiscoveredJson('password_recovery_endpoint', 'password recovery', { email });
      setResetRequestSent(true);
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  const resetPassword = useCallback(async (password: string, token: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await postDiscoveredJson('password_reset_endpoint', 'password reset', { password, token });
      window.location.hash = '#/login';
    } catch (err: any) {
      setError(safeProblemMessage(err));
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { requestPasswordReset, resetPassword, resetRequestSent, isLoading, error };
};
