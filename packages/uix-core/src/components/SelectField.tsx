import type { SelectHTMLAttributes } from "react";

export type SelectFieldOption = {
  label: string;
  value: string;
};

export function SelectField({
  help,
  label,
  options,
  ...props
}: SelectHTMLAttributes<HTMLSelectElement> & {
  help?: string;
  label: string;
  options: SelectFieldOption[];
}) {
  return (
    <label className="tigrbl-field">
      <span className="tigrbl-field-label">{label}</span>
      <select {...props}>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      {help && <span className="tigrbl-field-help">{help}</span>}
    </label>
  );
}
