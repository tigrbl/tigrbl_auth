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
    <label className="tba-toggle-field">
      <span className="tba-toggle-copy">
        <span className="tba-toggle-label">{label}</span>
        {description && <span className="tba-toggle-description">{description}</span>}
      </span>
      <span className="tba-toggle-control">
        <input {...props} type="checkbox" />
        <span aria-hidden="true" className="tba-toggle-track">
          <span className="tba-toggle-thumb" />
        </span>
      </span>
    </label>
  );
}
