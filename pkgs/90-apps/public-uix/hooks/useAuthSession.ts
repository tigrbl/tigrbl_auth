
import { useState, useCallback } from 'react';
import { User } from '../types';
import { getDiscoveredLogoutUrl } from '../services/tigrblAuthDiscovery';
import {
  clearPersistedPublicUser,
  clearPublicSessionCookie,
  persistPublicUser,
  PUBLIC_SESSION_STORAGE_KEY,
  resolvePublicSessionState,
  writePublicSessionCookie,
} from '../services/publicSession';

const getInitialState = (): { user: User | null; isAuthenticated: boolean } => {
  const savedUser = typeof localStorage === 'undefined'
    ? null
    : localStorage.getItem(PUBLIC_SESSION_STORAGE_KEY);
  const state = resolvePublicSessionState(savedUser);
  if (!state.user && typeof localStorage !== 'undefined' && savedUser) {
    localStorage.removeItem(PUBLIC_SESSION_STORAGE_KEY);
  }
  return state;
};

export const useAuthSession = () => {
  const [session, setSession] = useState(getInitialState);

  const updateSession = useCallback((user: User | null) => {
    if (user) {
      persistPublicUser(typeof localStorage === 'undefined' ? null : localStorage, user);
      if (typeof document !== 'undefined' && typeof window !== 'undefined') {
        writePublicSessionCookie(document, window.location.origin);
      }
      setSession({ user, isAuthenticated: user.isEmailVerified });
    } else {
      clearPersistedPublicUser(typeof localStorage === 'undefined' ? null : localStorage);
      if (typeof document !== 'undefined' && typeof window !== 'undefined') {
        clearPublicSessionCookie(document, window.location.origin);
      }
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
