import React, { useState } from 'react';
import { Card, Input } from '../components/UI';
import './RequiredPasswordChangePage.css';

interface RequiredPasswordChangePageProps {
  onChangePassword: (newPassword: string) => void;
  isLoading: boolean;
  error: string | null;
}

export const RequiredPasswordChangePage: React.FC<RequiredPasswordChangePageProps> = ({
  onChangePassword,
  isLoading,
  error,
}) => {
  const [password, setPassword] = useState('');
  const [confirmation, setConfirmation] = useState('');
  const [validationError, setValidationError] = useState<string | null>(null);

  const submit = (event: React.FormEvent) => {
    event.preventDefault();
    if (password.length < 12) {
      setValidationError('Use at least 12 characters.');
      return;
    }
    if (password !== confirmation) {
      setValidationError('The passwords do not match.');
      return;
    }
    setValidationError(null);
    onChangePassword(password);
  };

  return (
    <div className="login-page">
      <div className="login-shell u-animate-in">
        <div className="login-heading">
          <h1 className="login-title">Replace your temporary password</h1>
          <p className="login-subtitle">
            This bootstrap identity cannot authorize an application session until its temporary password is changed.
          </p>
        </div>
        <Card className="login-card">
          <form className="login-form" onSubmit={submit}>
            {(error || validationError) && (
              <div className="login-error" role="alert">
                <div className="login-error-inner">{error || validationError}</div>
              </div>
            )}
            <Input
              label="New password"
              type="password"
              autoComplete="new-password"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
            />
            <Input
              label="Confirm new password"
              type="password"
              autoComplete="new-password"
              value={confirmation}
              onChange={(event) => setConfirmation(event.target.value)}
            />
            <button type="submit" disabled={isLoading} className="login-submit-button">
              {isLoading ? 'Updating...' : 'Change password and continue'}
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
};
