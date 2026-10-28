import React, { useState, useEffect, useRef } from 'react';
import { Eye, EyeOff, Shield, RotateCcw } from 'lucide-react';

interface SecurePinFieldProps {
  id: string;
  value: string;
  onChange: (val: string) => void;
  onSubmit: () => void;
  disabled?: boolean;
  maxLength?: number;
  label?: string;
  placeholder?: string;
  error?: string;
  autoFocus?: boolean;
}

export function SecurePinField({
  id,
  value,
  onChange,
  onSubmit,
  disabled = false,
  maxLength = 12,
  label = 'Enter secure PIN',
  placeholder = '••••••',
  error,
  autoFocus = true,
}: SecurePinFieldProps) {
  const [showPin, setShowPin] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (autoFocus && inputRef.current) {
      inputRef.current.focus();
    }
    // Clean up PIN on unmount
    return () => {
      onChange('');
    };
  }, [autoFocus, onChange]);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const val = e.target.value.replace(/[^0-9]/g, ''); // Numeric input enforced
    if (val.length <= maxLength) {
      onChange(val);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter' && value.length > 0 && !disabled) {
      e.preventDefault();
      onSubmit();
    }
  };

  const handleClear = () => {
    onChange('');
    if (inputRef.current) {
      inputRef.current.focus();
    }
  };

  const handleKeypadClick = (num: string) => {
    if (disabled) return;
    if (value.length < maxLength) {
      onChange(value + num);
    }
  };

  const handleBackspace = () => {
    if (disabled) return;
    onChange(value.slice(0, -1));
  };

  return (
    <div className="flex flex-col space-y-2 w-full max-w-sm mx-auto" id={`${id}-container`}>
      <div className="flex justify-between items-center">
        <label htmlFor={id} className="text-xs font-semibold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
          <Shield size={13} className="text-blue-400 animate-pulse" />
          {label}
        </label>
        {value.length > 0 && (
          <button
            type="button"
            onClick={handleClear}
            disabled={disabled}
            className="text-[10px] font-mono text-slate-500 hover:text-red-400 flex items-center gap-1 transition-colors cursor-pointer"
            title="Clear secure buffer"
          >
            <RotateCcw size={10} />
            CLEAR SECURE BUFFER
          </button>
        )}
      </div>

      <div className="relative">
        <input
          id={id}
          ref={inputRef}
          type={showPin ? 'text' : 'password'}
          value={value}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          maxLength={maxLength}
          placeholder={placeholder}
          autoComplete="off"
          data-testid="secure-pin-input"
          className="w-full text-center tracking-[0.4em] font-mono text-lg md:text-xl py-3 px-12 rounded-xl bg-slate-900 border border-slate-800 text-slate-100 placeholder-slate-700 focus:outline-none focus:ring-2 focus:ring-blue-500/50 focus:border-blue-500 transition-all shadow-inner disabled:opacity-50"
          style={{ WebkitTextSecurity: showPin ? 'none' : 'disc' } as any}
        />

        {/* Visibility Toggle Button */}
        <button
          type="button"
          onClick={() => setShowPin(!showPin)}
          disabled={disabled}
          className="absolute right-3 top-1/2 -translate-y-1/2 p-2 text-slate-500 hover:text-slate-300 transition-colors cursor-pointer"
          aria-label={showPin ? 'Hide PIN' : 'Show PIN'}
        >
          {showPin ? <EyeOff size={18} /> : <Eye size={18} />}
        </button>

        {/* Counter Badge */}
        <div className="absolute left-3 top-1/2 -translate-y-1/2 text-[10px] font-mono font-bold text-slate-600 border border-slate-800 px-1.5 py-0.5 rounded bg-slate-950">
          {value.length}/{maxLength}
        </div>
      </div>

      {error && (
        <p className="text-xs text-red-400 font-medium leading-relaxed bg-red-950/20 px-3 py-1.5 rounded-lg border border-red-900/30">
          ⚠️ {error}
        </p>
      )}

      {/* Screen-reader friendly message */}
      <span className="sr-only">
        PIN entered: {value.length} of {maxLength} characters maximum. Only numbers are accepted.
      </span>

      {/* Embedded Secure Keypad */}
      <div className="mt-4 grid grid-cols-3 gap-2 bg-slate-950/50 p-3 rounded-2xl border border-slate-900 shadow-inner">
        {['1', '2', '3', '4', '5', '6', '7', '8', '9'].map((num) => (
          <button
            key={num}
            type="button"
            onClick={() => handleKeypadClick(num)}
            disabled={disabled || value.length >= maxLength}
            className="py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800/80 text-slate-200 text-sm font-mono font-medium transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
          >
            {num}
          </button>
        ))}
        <button
          type="button"
          onClick={handleClear}
          disabled={disabled || value.length === 0}
          className="py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-red-950/40 text-xs font-mono font-medium text-slate-400 hover:text-red-300 transition-all active:scale-95 disabled:opacity-30 cursor-pointer"
        >
          Clear
        </button>
        <button
          type="button"
          onClick={() => handleKeypadClick('0')}
          disabled={disabled || value.length >= maxLength}
          className="py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800/80 text-slate-200 text-sm font-mono font-medium transition-all hover:scale-[1.02] active:scale-95 disabled:opacity-30 cursor-pointer"
        >
          0
        </button>
        <button
          type="button"
          onClick={handleBackspace}
          disabled={disabled || value.length === 0}
          className="py-2.5 rounded-lg bg-slate-900 border border-slate-800 hover:bg-slate-800 text-xs font-mono font-medium text-slate-400 hover:text-slate-200 transition-all active:scale-95 disabled:opacity-30 cursor-pointer"
        >
          ⌫
        </button>
      </div>

      <div className="flex justify-center pt-2">
        <button
          type="button"
          onClick={onSubmit}
          disabled={disabled || value.length === 0}
          className="w-full py-2 px-4 rounded-xl bg-gradient-to-r from-blue-600 to-blue-500 text-white font-semibold text-xs tracking-wider uppercase shadow-md hover:from-blue-500 hover:to-blue-400 transition-all hover:shadow-blue-500/10 active:scale-98 disabled:opacity-30 disabled:pointer-events-none cursor-pointer"
        >
          Submit Secure Verifier Challenge
        </button>
      </div>
    </div>
  );
}
