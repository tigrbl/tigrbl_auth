
import React, { useState } from 'react';
import { Card } from '../components/UI';
import './MfaPage.css';

interface MfaPageProps {
  onVerify: (code: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

export const MfaPage: React.FC<MfaPageProps> = ({ onVerify, isLoading, error }) => {
  const [code, setCode] = useState(['', '', '', '', '', '']);

  const handleChange = (index: number, value: string) => {
    if (!/^\d*$/.test(value)) return;
    const newCode = [...code];
    newCode[index] = value.slice(-1);
    setCode(newCode);

    // Auto-focus next
    if (value && index < 5) {
      const nextInput = document.getElementById(`mfa-${index + 1}`);
      nextInput?.focus();
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onVerify(code.join(''));
  };

  return (
    <div className="mfa-page">
      <div className="mfa-shell u-animate-zoom">
        <div className="mfa-heading">
          <div className="mfa-icon-shell">
            <svg className="mfa-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 className="mfa-title">Multi-Factor Authentication</h1>
          <p className="mfa-subtitle">Enter the 6-digit code sent to your registered device.</p>
        </div>

        <Card className="mfa-card">
          <form onSubmit={handleSubmit} className="mfa-form">
            {error && (
              <div className="mfa-error">
                {error}
              </div>
            )}

            <div className="mfa-code-row">
              {code.map((digit, i) => (
                <input
                  key={i}
                  id={`mfa-${i}`}
                  type="text"
                  inputMode="numeric"
                  value={digit}
                  onChange={(e) => handleChange(i, e.target.value)}
                  className="mfa-code-input"
                />
              ))}
            </div>

            <button
              type="submit"
              disabled={isLoading || code.some(d => !d)}
              className="mfa-submit"
            >
              {isLoading ? 'Verifying...' : 'Verify & Continue'}
            </button>

            <p className="mfa-help">
              Didn't receive the code? <button type="button" className="mfa-resend">Resend code</button>
            </p>
          </form>
        </Card>
      </div>
    </div>
  );
};
