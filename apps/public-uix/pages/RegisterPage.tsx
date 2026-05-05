
import React, { useState } from 'react';
import { Card, Input } from '../components/UI';
import { usePlatform } from '../hooks/usePlatform';

interface RegisterPageProps {
  onRegister: (name: string, email: string) => Promise<void>;
  isLoading: boolean;
  error: string | null;
}

export const RegisterPage: React.FC<RegisterPageProps> = ({ onRegister, isLoading, error }) => {
  const platform = usePlatform();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [errors, setErrors] = useState<{name?: string, email?: string, password?: string, confirm?: string}>({});

  const getPasswordStrength = () => {
    if (!password) return 0;
    let strength = 0;
    if (password.length > 8) strength += 1;
    if (/[A-Z]/.test(password)) strength += 1;
    if (/[0-9]/.test(password)) strength += 1;
    if (/[^A-Za-z0-9]/.test(password)) strength += 1;
    return strength;
  };

  const validate = () => {
    const newErrors: any = {};
    if (!name.trim()) newErrors.name = 'Full name is required';
    if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) newErrors.email = 'Valid email is required';
    if (password.length < 8) newErrors.password = 'Min 8 characters';
    if (password !== confirmPassword) newErrors.confirm = 'Passwords do not match';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (validate()) onRegister(name, email);
  };

  const navigateToLogin = () => {
    window.location.hash = '#/login';
  };

  const strength = getPasswordStrength();

  return (
    <div className="flex-grow flex items-center justify-center p-6">
      <div className="w-full max-w-md space-y-8 animate-in slide-in-from-bottom-4 duration-700">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold text-slate-900 tracking-tight">{platform.registerTitle}</h1>
          <p className="text-slate-500">{platform.registerSubtitle}</p>
        </div>

        <Card className="p-8">
          <form className="space-y-5" onSubmit={handleSubmit}>
            {error && (
              <div className="p-3 bg-red-50 border border-red-200 rounded-brand text-red-600 text-xs font-bold text-center">
                {error}
              </div>
            )}
            <Input label="Display Name" placeholder="Your Full Name" value={name} error={errors.name} onChange={e => setName(e.target.value)} />
            <Input label="Email Identity" placeholder="you@company.com" value={email} error={errors.email} onChange={e => setEmail(e.target.value)} />

            <div className="space-y-2">
              <Input label="Secret Key" type="password" placeholder="••••••••" value={password} error={errors.password} onChange={e => setPassword(e.target.value)} />
              {password && (
                <div className="flex gap-1 h-1.5 px-1">
                  {[1, 2, 3, 4].map(i => (
                    <div key={i} className={`flex-grow rounded-full transition-all duration-500 ${strength >= i ? (strength < 3 ? 'bg-amber-400' : 'bg-brand') : 'bg-slate-200'}`} />
                  ))}
                </div>
              )}
            </div>

            <Input label="Verify Secret" type="password" placeholder="••••••••" value={confirmPassword} error={errors.confirm} onChange={e => setConfirmPassword(e.target.value)} />

            <div className="pt-2">
              <button
                type="submit"
                disabled={isLoading}
                className="w-full bg-brand text-white py-3 rounded-brand font-bold shadow-lg shadow-brand/20 hover:opacity-90 active:scale-[0.99] transition-all disabled:opacity-50"
              >
                {isLoading ? 'Generating Identity...' : 'Join Platform'}
              </button>
            </div>
          </form>

          <div className="mt-6 pt-6 border-t border-slate-100 text-center">
            <p className="text-sm text-slate-500">
              By proceeding, you agree to our <button onClick={() => window.location.hash = '#/terms'} className="text-brand font-bold hover:underline">Terms of Service</button>.
            </p>
          </div>
        </Card>

        <p className="text-center text-sm text-slate-500">
          Already have an identity? <button onClick={navigateToLogin} className="text-brand font-bold hover:underline">Sign in</button>
        </p>
      </div>
    </div>
  );
};
