
import React from 'react';

export const Card: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = "" }) => (
  <div className={`bg-white rounded-brand shadow-xl shadow-slate-200/50 border border-slate-100 overflow-hidden ${className}`}>
    {children}
  </div>
);

export const SocialButton: React.FC<{
  onClick: () => void;
  icon: React.ReactNode;
  label: string;
  disabled?: boolean;
}> = ({ onClick, icon, label, disabled }) => (
  <button
    onClick={onClick}
    disabled={disabled}
    className="w-full flex items-center justify-center gap-3 px-4 py-3 border border-slate-200 rounded-brand hover:bg-slate-50 transition-all active:scale-[0.98] disabled:opacity-50 disabled:cursor-not-allowed font-medium text-slate-700"
  >
    {icon}
    <span>Continue with {label}</span>
  </button>
);

export const Input: React.FC<{
  label: string;
  type?: string;
  placeholder?: string;
  value: string;
  error?: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void;
}> = ({ label, type = "text", placeholder, value, error, onChange }) => (
  <div className="space-y-1.5 w-full">
    <div className="flex justify-between items-center">
      <label className="text-sm font-semibold text-slate-700 ml-0.5">{label}</label>
      {error && <span className="text-[10px] font-bold text-red-500 uppercase tracking-tighter">{error}</span>}
    </div>
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`w-full px-4 py-3 bg-slate-50 border ${error ? 'border-red-300 ring-1 ring-red-100' : 'border-slate-200'} rounded-brand focus:ring-2 focus:ring-brand focus:border-transparent outline-none transition-all placeholder:text-slate-400`}
    />
  </div>
);

export const Checkbox: React.FC<{
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}> = ({ label, checked, onChange }) => (
  <label className="flex items-center gap-2 cursor-pointer group">
    <div className="relative flex items-center">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="peer sr-only"
      />
      <div className="w-5 h-5 border-2 border-slate-200 rounded-md peer-checked:bg-brand peer-checked:border-brand transition-all group-hover:border-brand/40"></div>
      <svg className="absolute w-3.5 h-3.5 text-white left-[3px] opacity-0 peer-checked:opacity-100 transition-opacity" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
      </svg>
    </div>
    <span className="text-sm text-slate-600 font-medium group-hover:text-brand transition-colors">{label}</span>
  </label>
);

export const Modal: React.FC<{
  isOpen: boolean;
  onClose: () => void;
  title: string;
  children: React.ReactNode;
}> = ({ isOpen, onClose, title, children }) => {
  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
      <div
        className="absolute inset-0 bg-slate-900/40 backdrop-blur-sm animate-in fade-in duration-300"
        onClick={onClose}
      />
      <div className="relative w-full max-w-lg bg-white rounded-brand shadow-2xl overflow-hidden animate-in zoom-in-95 duration-300">
        <div className="px-6 py-4 border-b border-slate-100 flex justify-between items-center">
          <h3 className="text-lg font-bold text-slate-800">{title}</h3>
          <button onClick={onClose} className="text-slate-400 hover:text-slate-600 p-1">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="p-6 max-h-[85vh] overflow-y-auto">
          {children}
        </div>
      </div>
    </div>
  );
};
