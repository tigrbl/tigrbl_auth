
import React from 'react';
import './UI.css';

export const Card: React.FC<{ children: React.ReactNode; className?: string }> = ({ children, className = "" }) => (
  <div className={`ui-card ${className}`}>
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
    className="ui-social-button"
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
  <div className="ui-input-field">
    <div className="ui-input-header">
      <label className="ui-input-label">{label}</label>
      {error && <span className="ui-input-error">{error}</span>}
    </div>
    <input
      type={type}
      placeholder={placeholder}
      value={value}
      onChange={onChange}
      className={`ui-input-control ${error ? 'ui-input-control--error' : ''}`}
    />
  </div>
);

export const Checkbox: React.FC<{
  label: string;
  checked: boolean;
  onChange: (checked: boolean) => void;
}> = ({ label, checked, onChange }) => (
  <label className="ui-checkbox">
    <div className="ui-checkbox-control">
      <input
        type="checkbox"
        checked={checked}
        onChange={(e) => onChange(e.target.checked)}
        className="ui-checkbox-input"
      />
      <div className="ui-checkbox-box"></div>
      <svg className="ui-checkbox-check" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="3" d="M5 13l4 4L19 7" />
      </svg>
    </div>
    <span className="ui-checkbox-label">{label}</span>
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
    <div className="ui-modal-shell">
      <div
        className="ui-modal-backdrop"
        onClick={onClose}
      />
      <div className="ui-modal-panel">
        <div className="ui-modal-header">
          <h3 className="ui-modal-title">{title}</h3>
          <button onClick={onClose} className="ui-modal-close">
            <svg className="ui-modal-close-icon" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        <div className="ui-modal-body">
          {children}
        </div>
      </div>
    </div>
  );
};
