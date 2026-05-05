
import { useState, useCallback } from 'react';

export const usePasswordRecovery = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [resetRequestSent, setResetRequestSent] = useState(false);

  const requestPasswordReset = useCallback(async (email: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await new Promise(r => setTimeout(r, 1000));
      setResetRequestSent(true);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const resetPassword = useCallback(async (password: string, token: string) => {
    setIsLoading(true);
    setError(null);
    try {
      await new Promise(r => setTimeout(r, 1000));
      window.location.hash = '/login';
    } catch (err: any) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return { requestPasswordReset, resetPassword, resetRequestSent, isLoading, error };
};
