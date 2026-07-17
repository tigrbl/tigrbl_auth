import type { TextareaHTMLAttributes } from "react";

export function CodeField({
  help,
  label,
  rows = 8,
  ...props
}: TextareaHTMLAttributes<HTMLTextAreaElement> & {
  help?: string;
  label: string;
}) {
  return (
    <label className="tigrbl-field">
      <span className="tigrbl-field-label">{label}</span>
      <textarea {...props} className={`tigrbl-code-field ${props.className ?? ""}`.trim()} rows={rows} />
      {help && <span className="tigrbl-field-help">{help}</span>}
    </label>
  );
}
