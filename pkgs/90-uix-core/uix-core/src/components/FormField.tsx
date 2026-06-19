import type { InputHTMLAttributes } from "react";

export function FormField({
  error,
  help,
  label,
  ...props
}: InputHTMLAttributes<HTMLInputElement> & {
  error?: string;
  help?: string;
  label: string;
}) {
  return (
    <label className="tigrbl-field">
      <span className="tigrbl-field-label">
        <span>{label}</span>
        {error && <ValidationMessage>{error}</ValidationMessage>}
      </span>
      <input {...props} aria-invalid={error ? "true" : props["aria-invalid"]} />
      {help && <small className="tigrbl-field-help">{help}</small>}
    </label>
  );
}

export function FormError({ children }: { children: string }) {
  return <p className="tigrbl-form-error">{children}</p>;
}

export function ValidationMessage({ children }: { children: string }) {
  return <span className="tigrbl-validation-message">{children}</span>;
}
