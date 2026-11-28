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
    <label className="tba-field">
      <span className="tba-field-label">{label}</span>
      <textarea {...props} className={`tba-code-field ${props.className ?? ""}`.trim()} rows={rows} />
      {help && <span className="tba-field-help">{help}</span>}
    </label>
  );
}
