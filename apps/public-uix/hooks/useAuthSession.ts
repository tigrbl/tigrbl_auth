
import { useState, useCallback } from 'react';
import { User, AuthState } from '../types';

const getInitialState = (): { user: User | null; isAuthenticated: boolean } => {
  const savedUser = localStorage.getItem('nexus_user');
  if (savedUser) {
    try {
      const user = JSON.parse(savedUser);
      return {
        user,
        isAuthenticated: user.isEmailVerified,
      };
    } catch (e) {
      localStorage.removeItem('nexus_user');
    }
  }
  return { user: null, isAuthenticated: false };
};

export const useAuthSession = () => {
  const [session, setSession] = useState(getInitialState);

  const updateSession = useCallback((user: User | null) => {
    if (user) {
      localStorage.setItem('nexus_user', JSON.stringify(user));
      setSession({ user, isAuthenticated: user.isEmailVerified });
    } else {
      localStorage.removeItem('nexus_user');
      setSession({ user: null, isAuthenticated: false });
    }
  }, []);

  const logout = useCallback(() => {
    updateSession(null);
    window.location.hash = '#/login';
  }, [updateSession]);

  return { ...session, updateSession, logout };
};
