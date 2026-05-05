
import React, { useState } from 'react';
import { Card } from '../components/UI';

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
    <div className="flex-grow flex items-center justify-center p-6 bg-slate-50">
      <div className="w-full max-w-md space-y-8 animate-in zoom-in-95 duration-500">
        <div className="text-center space-y-2">
          <div className="w-16 h-16 bg-indigo-100 text-indigo-600 rounded-2xl flex items-center justify-center mx-auto mb-4">
            <svg className="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
            </svg>
          </div>
          <h1 className="text-2xl font-bold text-slate-900">Multi-Factor Authentication</h1>
          <p className="text-slate-500 text-sm">Enter the 6-digit code sent to your registered device.</p>
        </div>

        <Card className="p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-xl text-red-600 text-xs font-bold text-center">
                {error}
              </div>
            )}

            <div className="flex justify-between gap-2">
              {code.map((digit, i) => (
                <input
                  key={i}
                  id={`mfa-${i}`}
                  type="text"
                  inputMode="numeric"
                  value={digit}
                  onChange={(e) => handleChange(i, e.target.value)}
                  className="w-12 h-14 text-center text-xl font-bold bg-slate-50 border border-slate-200 rounded-xl focus:ring-2 focus:ring-indigo-500 outline-none transition-all"
                />
              ))}
            </div>

            <button
              type="submit"
              disabled={isLoading || code.some(d => !d)}
              className="w-full bg-indigo-600 text-white py-4 rounded-xl font-bold shadow-lg hover:bg-indigo-700 disabled:opacity-50 transition-all"
            >
              {isLoading ? 'Verifying...' : 'Verify & Continue'}
            </button>

            <p className="text-center text-xs text-slate-400">
              Didn't receive the code? <button type="button" className="text-indigo-600 font-bold hover:underline">Resend code</button>
            </p>
          </form>
        </Card>
      </div>
    </div>
  );
};
