
import React, { useState } from 'react';
import { Card, Input } from '../components/UI';

interface ResetPasswordPageProps {
  onReset: (password: string, token: string) => Promise<void>;
  isLoading: boolean;
}

export const ResetPasswordPage: React.FC<ResetPasswordPageProps> = ({ onReset, isLoading }) => {
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{password?: string, confirm?: string}>({});

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const newErrors: any = {};
    if (password.length < 8) newErrors.password = 'Must be at least 8 characters';
    if (password !== confirmPassword) newErrors.confirm = 'Passwords do not match';

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    const token = new URLSearchParams(window.location.hash.split('?')[1]).get('token') || 'INVALID';
    onReset(password, token);
  };

  return (
    <div className="flex-grow flex items-center justify-center p-6 bg-slate-50">
      <div className="w-full max-w-md space-y-8 animate-in slide-in-from-bottom-4 duration-500">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Set New Password</h1>
          <p className="text-slate-500">Choose a strong, unique password.</p>
        </div>

        <Card className="p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
            <Input
              label="New Password"
              type="password"
              placeholder="••••••••"
              value={password}
              error={errors.password}
              onChange={e => setPassword(e.target.value)}
            />
            <Input
              label="Confirm New Password"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              error={errors.confirm}
              onChange={e => setConfirmPassword(e.target.value)}
            />
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-indigo-600 text-white py-3 rounded-xl font-semibold shadow-lg hover:bg-indigo-700 transition-all disabled:opacity-50"
            >
              {isLoading ? 'Updating...' : 'Reset Password'}
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
};
