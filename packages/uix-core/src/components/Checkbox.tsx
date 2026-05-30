import type { InputHTMLAttributes, ReactNode } from "react";

export function Checkbox({
  children,
  label,
  onCheckedChange,
  ...props
}: Omit<InputHTMLAttributes<HTMLInputElement>, "type" | "onChange"> & {
  children?: ReactNode;
  label?: ReactNode;
  onCheckedChange?: (checked: boolean) => void;
}) {
  return (
    <label className="tigrbl-checkbox">
      <span className="tigrbl-checkbox-box">
        <input
          {...props}
          type="checkbox"
          onChange={(event) => onCheckedChange?.(event.target.checked)}
        />
        <span aria-hidden="true" className="tigrbl-checkbox-mark">✓</span>
      </span>
      <span>{children ?? label}</span>
    </label>
  );
}
