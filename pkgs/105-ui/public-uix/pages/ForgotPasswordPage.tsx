
import React, { useState } from 'react';
import { Card, Input } from '../components/UI';
import './ForgotPasswordPage.css';

interface ForgotPasswordPageProps {
  onRequestReset: (email: string) => Promise<void>;
  isLoading: boolean;
  isSent?: boolean;
}

export const ForgotPasswordPage: React.FC<ForgotPasswordPageProps> = ({ onRequestReset, isLoading, isSent }) => {
  const [email, setEmail] = useState('');
  const [error, setError] = useState<string>();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError('Enter a valid work email');
      return;
    }
    onRequestReset(email);
  };

  if (isSent) {
    return (
      <div className="forgot-page">
        <div className="forgot-shell u-animate-zoom">
          <Card className="forgot-sent-card">
            <div className="forgot-icon-shell">
              <svg className="forgot-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div>
              <h2 className="forgot-title forgot-title--sent">Check your inbox</h2>
              <p className="forgot-copy">We've sent a secure reset link to <span className="forgot-email">{email}</span></p>
            </div>
            <div className="forgot-sent-actions">
              <button
                onClick={() => window.location.hash = '#/login'}
                className="forgot-secondary"
              >
                Return to Login
              </button>
            </div>
          </Card>
        </div>
      </div>
    );
  }

  return (
    <div className="forgot-page">
      <div className="forgot-shell forgot-stack u-animate-in">
        <div className="forgot-heading">
          <h1 className="forgot-title">Forgot Password?</h1>
          <p className="forgot-subtitle">We'll send you instructions to reset it.</p>
        </div>

        <Card className="forgot-card">
          <form className="forgot-form" onSubmit={handleSubmit}>
            <Input
              label="Work Email"
              placeholder="name@company.com"
              value={email}
              error={error}
              onChange={e => {
                setEmail(e.target.value);
                setError(undefined);
              }}
            />
            <button
              type="submit"
              disabled={isLoading}
              className="forgot-primary"
            >
              {isLoading ? 'Sending...' : 'Send Reset Link'}
            </button>
            <button
              type="button"
              onClick={() => window.location.hash = '#/login'}
              className="forgot-secondary"
            >
              Wait, I remember it!
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
};
