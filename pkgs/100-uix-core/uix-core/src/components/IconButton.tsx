import type { ButtonHTMLAttributes, ReactNode } from "react";

export function IconButton({
  children,
  label,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  label: string;
}) {
  return (
    <button {...props} aria-label={label} className={`tigrbl-icon-button ${props.className ?? ""}`.trim()} title={label}>
      {children}
    </button>
  );
}

