import type { ButtonHTMLAttributes, ReactNode } from "react";

export function SocialButton({
  children,
  icon,
  label,
  ...props
}: ButtonHTMLAttributes<HTMLButtonElement> & {
  children?: ReactNode;
  icon?: ReactNode;
  label: string;
}) {
  return (
    <button {...props} className={`tba-social-button ${props.className ?? ""}`.trim()} type={props.type ?? "button"}>
      {icon && <span aria-hidden="true" className="tba-social-button-icon">{icon}</span>}
      <span>{children ?? `Continue with ${label}`}</span>
    </button>
  );
}
