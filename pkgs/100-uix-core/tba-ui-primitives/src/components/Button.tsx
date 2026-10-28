import type { ButtonHTMLAttributes, ReactNode } from "react";

export function Button({
  children,
  variant = "primary",
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children: ReactNode;
  variant?: "danger" | "primary" | "subtle";
}) {
  return (
    <button {...props} className={`tba-button tba-button-${variant} ${props.className ?? ""}`.trim()}>
      {children}
    </button>
  );
}

