
import React from 'react';
import { Card } from '../components/UI';
import './EmailVerificationPage.css';

interface EmailVerificationPageProps {
  email: string;
  onVerify: () => Promise<void>;
  onResend: () => Promise<void>;
  resendSuccess: boolean;
  isLoading: boolean;
}

export const EmailVerificationPage: React.FC<EmailVerificationPageProps> = ({
  email,
  onVerify,
  onResend,
  resendSuccess,
  isLoading
}) => {
  return (
    <div className="email-verification-page">
      <div className="email-verification-shell u-animate-in">
        <div className="email-verification-icon-shell">
          <svg className="email-verification-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>

        <div>
          <h1 className="email-verification-title">Verify your email</h1>
          <p className="email-verification-subtitle">
            We've sent a verification link to <span className="email-verification-email">{email}</span>.
          </p>
        </div>

        <Card className="email-verification-card">
          {resendSuccess && (
            <div className="email-verification-success u-animate-zoom">
              Verification email resent successfully!
            </div>
          )}

          <p className="email-verification-copy">
            Please click the link in the email to activate your tigrbl_auth account and complete registration.
          </p>

          <button
            onClick={onVerify}
            disabled={isLoading}
            className="email-verification-primary"
          >
            {isLoading ? 'Verifying Identity...' : 'Simulate Clicking Verification Link'}
          </button>

          <div className="email-verification-help">
            <p className="email-verification-help-text">
              Can't find the email? Check your spam or{' '}
              <button
                onClick={onResend}
                disabled={isLoading}
                className="email-verification-resend"
              >
                resend verification email
              </button>.
            </p>
          </div>
        </Card>

        <button
          onClick={() => window.location.hash = '#/login'}
          className="email-verification-back"
        >
          Back to Login
        </button>
      </div>
    </div>
  );
};
