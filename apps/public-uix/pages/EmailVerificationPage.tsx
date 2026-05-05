
import React from 'react';
import { Card } from '../components/UI';

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
    <div className="flex-grow flex items-center justify-center p-6 bg-gradient-to-br from-indigo-50 to-white">
      <div className="w-full max-w-md text-center space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-700">
        <div className="w-24 h-24 bg-white shadow-xl rounded-3xl flex items-center justify-center mx-auto mb-6">
          <svg className="w-12 h-12 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
          </svg>
        </div>

        <div className="space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">Verify your email</h1>
          <p className="text-slate-500 max-w-xs mx-auto">
            We've sent a verification link to <span className="font-bold text-slate-800">{email}</span>.
          </p>
        </div>

        <Card className="p-8 space-y-6">
          {resendSuccess && (
            <div className="p-3 bg-emerald-50 border border-emerald-100 rounded-xl text-emerald-700 text-xs font-bold animate-in fade-in zoom-in-95">
              Verification email resent successfully!
            </div>
          )}

          <p className="text-sm text-slate-600">
            Please click the link in the email to activate your tigrbl_auth account and complete registration.
          </p>

          <button
            onClick={onVerify}
            disabled={isLoading}
            className="w-full bg-slate-900 text-white py-4 rounded-xl font-bold shadow-lg hover:bg-slate-800 active:scale-[0.99] transition-all disabled:opacity-50"
          >
            {isLoading ? 'Verifying Identity...' : 'Simulate Clicking Verification Link'}
          </button>

          <div className="pt-4 border-t border-slate-100">
            <p className="text-xs text-slate-400">
              Can't find the email? Check your spam or{' '}
              <button
                onClick={onResend}
                disabled={isLoading}
                className="text-indigo-600 font-bold hover:underline disabled:opacity-50"
              >
                resend verification email
              </button>.
            </p>
          </div>
        </Card>

        <button
          onClick={() => window.location.hash = '#/login'}
          className="text-sm font-semibold text-slate-400 hover:text-slate-600 transition-colors"
        >
          Back to Login
        </button>
      </div>
    </div>
  );
};
