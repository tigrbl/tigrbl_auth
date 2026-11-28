import React, { useEffect, useRef } from 'react';
import { AuthProvider } from '../types';
import './CallbackPage.css';

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
    <div className="callback-page">
      <div className="callback-spinner-shell">
        <div className="callback-spinner-track"></div>
        <div className="callback-spinner-ring"></div>
      </div>
      <div className="callback-copy">
        <h2 className="callback-title">Finalizing Identity</h2>
        <p className="callback-text">
          Verifying credentials and synchronizing session...
        </p>
      </div>
    </div>
  );
};
