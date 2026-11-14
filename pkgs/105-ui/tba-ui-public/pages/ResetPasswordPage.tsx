import React, { useState } from 'react';
import { Card, Input } from '../components/UI';
import './ResetPasswordPage.css';

interface ResetPasswordPageProps {
  onReset: (password: string, token: string) => Promise<void>;
  isLoading: boolean;
  error?: string | null;
}

export const ResetPasswordPage: React.FC<ResetPasswordPageProps> = ({ onReset, isLoading, error }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{password?: string, confirm?: string}>({});
  const token = new URLSearchParams(window.location.hash.split('?')[1]).get('token');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: any = {};
    if (password.length < 8) newErrors.password = 'Must be at least 8 characters';
    if (password !== confirmPassword) newErrors.confirm = 'Passwords do not match';

    setErrors(newErrors);
    if (Object.keys(newErrors).length > 0 || !token) return;

    onReset(password, token);
  };

  return (
    <div className="reset-page">
      <div className="reset-shell u-animate-in">
        <div className="reset-heading">
          <h1 className="reset-title">Set New Password</h1>
          <p className="reset-subtitle">Choose a strong, unique password.</p>
        </div>

        <Card className="reset-card">
          {token ? <form className="reset-form" onSubmit={handleSubmit}>
            {error && <p role="alert">{error}</p>}
            <Input
              label="New Password"
              type="password"
              autoComplete="new-password"
              placeholder="********"
              value={password}
              error={errors.password}
              onChange={e => setPassword(e.target.value)}
            />
            <Input
              label="Confirm New Password"
              type="password"
              autoComplete="new-password"
              placeholder="********"
              value={confirmPassword}
              error={errors.confirm}
              onChange={e => setConfirmPassword(e.target.value)}
            />
            <button
              type="submit"
              disabled={isLoading}
              className="reset-submit"
            >
              {isLoading ? 'Updating...' : 'Reset Password'}
            </button>
          </form> : <p role="alert">Use the reset link from your email or <a href="#/forgot-password">request a new link</a>.</p>}
        </Card>
      </div>
    </div>
  );
};
