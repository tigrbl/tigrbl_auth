
import { useState, useCallback } from 'react';
import { User, AuthState } from '../types';
import { getDiscoveredLogoutUrl } from '../services/tigrblAuthDiscovery';

const getInitialState = (): { user: User | null; isAuthenticated: boolean } => {
  const savedUser = localStorage.getItem('tigrbl_auth_user');
  if (savedUser) {
    try {
      const user = JSON.parse(savedUser);
      return {
        user,
        isAuthenticated: user.isEmailVerified,
      };
    } catch (e) {
      localStorage.removeItem('tigrbl_auth_user');
    }
  }
  return { user: null, isAuthenticated: false };
};

export const useAuthSession = () => {
  const [session, setSession] = useState(getInitialState);

  const updateSession = useCallback((user: User | null) => {
    if (user) {
      localStorage.setItem('tigrbl_auth_user', JSON.stringify(user));
      setSession({ user, isAuthenticated: user.isEmailVerified });
    } else {
      localStorage.removeItem('tigrbl_auth_user');
      setSession({ user: null, isAuthenticated: false });
    }
  }, []);

  const logout = useCallback(async () => {
    const logoutUrl = await getDiscoveredLogoutUrl();
    updateSession(null);
    if (logoutUrl) {
      window.location.assign(logoutUrl);
      return;
    }
    window.location.hash = '#/login';
  }, [updateSession]);

  return { ...session, updateSession, logout };
};
