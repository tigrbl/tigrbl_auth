import type { InputHTMLAttributes } from "react";

export function FormField({
  help,
  label,
  ...props
}: InputHTMLAttributes<HTMLInputElement> & {
  help?: string;
  label: string;
}) {
  return (
    <label className="tigrbl-field">
      <span>{label}</span>
      <input {...props} />
      {help && <small>{help}</small>}
    </label>
  );
}

