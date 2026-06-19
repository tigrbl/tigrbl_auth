import type { InputHTMLAttributes, ReactNode } from "react";

export function ToggleField({
  description,
  label,
  ...props
}: Omit<InputHTMLAttributes<HTMLInputElement>, "type"> & {
  description?: ReactNode;
  label: string;
}) {
  return (
    <label className="tigrbl-toggle-field">
      <span className="tigrbl-toggle-copy">
        <span className="tigrbl-toggle-label">{label}</span>
        {description && <span className="tigrbl-toggle-description">{description}</span>}
      </span>
      <span className="tigrbl-toggle-control">
        <input {...props} type="checkbox" />
        <span aria-hidden="true" className="tigrbl-toggle-track">
          <span className="tigrbl-toggle-thumb" />
        </span>
      </span>
    </label>
  );
}
