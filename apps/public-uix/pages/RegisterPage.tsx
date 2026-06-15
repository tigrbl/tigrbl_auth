import React, { useState } from 'react';
import { Card, Input } from '../components/UI';
import { usePlatform } from '../hooks/usePlatform';
import './RegisterPage.css';

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
  const strengthClass = (step: number): string => {
    if (strength < step) return 'register-strength-bar';
    return `register-strength-bar ${strength < 3 ? 'register-strength-bar--weak' : 'register-strength-bar--strong'}`;
  };

  return (
    <div className="register-page">
      <div className="register-shell u-animate-in">
        <div className="register-heading">
          <h1 className="register-title">{platform.registerTitle}</h1>
          <p className="register-subtitle">{platform.registerSubtitle}</p>
        </div>

        <Card className="register-card">
          <form className="register-form" onSubmit={handleSubmit}>
            {error && (
              <div className="register-error">
                {error}
              </div>
            )}
            <Input label="Display Name" placeholder="Your Full Name" value={name} error={errors.name} onChange={e => setName(e.target.value)} />
            <Input label="Email Identity" placeholder="you@company.com" value={email} error={errors.email} onChange={e => setEmail(e.target.value)} />

            <div className="register-secret">
              <Input label="Secret Key" type="password" placeholder="********" value={password} error={errors.password} onChange={e => setPassword(e.target.value)} />
              {password && (
                <div className="register-strength">
                  {[1, 2, 3, 4].map(i => (
                    <div key={i} className={strengthClass(i)} />
                  ))}
                </div>
              )}
            </div>

            <Input label="Verify Secret" type="password" placeholder="********" value={confirmPassword} error={errors.confirm} onChange={e => setConfirmPassword(e.target.value)} />

            <div className="register-action">
              <button
                type="submit"
                disabled={isLoading}
                className="register-submit-button"
              >
                {isLoading ? 'Generating Identity...' : 'Join Platform'}
              </button>
            </div>
          </form>

          <div className="register-terms">
            <p className="register-terms-text">
              By proceeding, you agree to our <button onClick={() => window.location.hash = '#/terms'} className="register-link">Terms of Service</button>.
            </p>
          </div>
        </Card>

        <p className="register-footer">
          Already have an identity? <button onClick={navigateToLogin} className="register-link">Sign in</button>
        </p>
      </div>
    </div>
  );
};
