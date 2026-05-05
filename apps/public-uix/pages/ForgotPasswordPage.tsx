
import React, { useState } from 'react';
import { Card, Input } from '../components/UI';

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
      <div className="flex-grow flex items-center justify-center p-6 bg-slate-50">
        <div className="w-full max-w-md animate-in zoom-in-95 duration-500">
          <Card className="p-10 text-center space-y-6">
            <div className="w-20 h-20 bg-emerald-100 text-emerald-600 rounded-full flex items-center justify-center mx-auto">
              <svg className="w-10 h-10" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
              </svg>
            </div>
            <div className="space-y-2">
              <h2 className="text-2xl font-bold text-slate-900">Check your inbox</h2>
              <p className="text-slate-500">We've sent a secure reset link to <span className="font-bold text-slate-700">{email}</span></p>
            </div>
            <div className="pt-4 space-y-3">
              <button
                onClick={() => window.location.hash = '#/login'}
                className="w-full py-3 text-slate-500 font-semibold hover:text-slate-700"
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
    <div className="flex-grow flex items-center justify-center p-6 bg-slate-50">
      <div className="w-full max-w-md space-y-8 animate-in slide-in-from-bottom-4 duration-500">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Forgot Password?</h1>
          <p className="text-slate-500">We'll send you instructions to reset it.</p>
        </div>

        <Card className="p-8">
          <form className="space-y-6" onSubmit={handleSubmit}>
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
              className="w-full bg-indigo-600 text-white py-3 rounded-xl font-semibold shadow-lg hover:bg-indigo-700 transition-all disabled:opacity-50"
            >
              {isLoading ? 'Sending...' : 'Send Reset Link'}
            </button>
            <button
              type="button"
              onClick={() => window.location.hash = '#/login'}
              className="w-full text-sm font-bold text-slate-400 hover:text-indigo-600 transition-colors"
            >
              Wait, I remember it!
            </button>
          </form>
        </Card>
      </div>
    </div>
  );
};
