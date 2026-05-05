import React, { useEffect, useRef } from 'react';
import { AuthProvider } from '../types';

interface CallbackPageProps {
  onHandleCallback: (provider: AuthProvider) => Promise<void>;
}

export const CallbackPage: React.FC<CallbackPageProps> = ({ onHandleCallback }) => {
  const handledRef = useRef(false);

  useEffect(() => {
    if (handledRef.current) return;

    // Support both Hash and Query params
    const queryString = window.location.search || window.location.hash.split('?')[1] || '';
    const params = new URLSearchParams(queryString);
    const provider = params.get('provider') as AuthProvider;
    const code = params.get('code');

    if (provider || code) {
      handledRef.current = true;

      // If we are in a popup, we notify the parent window
      if (window.opener && window.opener !== window) {
        // We'll perform the callback logic in the context of the parent
        // by sending the current URL/params back.
        window.opener.postMessage({
          type: 'OIDC_CALLBACK',
          payload: {
            url: window.location.href,
            search: queryString
          }
        }, window.location.origin);

        // Brief pause to ensure message is sent
        setTimeout(() => window.close(), 500);
      } else {
        // Standard redirect flow
        onHandleCallback(provider || AuthProvider.GENERIC);
      }
    }
  }, [onHandleCallback]);

  return (
    <div className="flex-grow flex flex-col items-center justify-center p-6 text-center space-y-6">
      <div className="relative w-20 h-20">
        <div className="absolute inset-0 border-4 border-indigo-100 rounded-full"></div>
        <div className="absolute inset-0 border-4 border-indigo-600 rounded-full border-t-transparent animate-spin"></div>
      </div>
      <div className="space-y-2">
        <h2 className="text-2xl font-bold text-slate-900">Finalizing Identity</h2>
        <p className="text-slate-500 max-w-xs mx-auto">
          Verifying credentials and synchronizing session...
        </p>
      </div>
    </div>
  );
};
