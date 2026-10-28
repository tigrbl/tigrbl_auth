import type { FormHTMLAttributes, ReactNode } from "react";

export function ResourceForm({
  children,
  footer,
  ...props
}: FormHTMLAttributes<HTMLFormElement> & {
  children: ReactNode;
  footer?: ReactNode;
}) {
  return (
    <form {...props} className={`tba-resource-form ${props.className ?? ""}`.trim()}>
      <div className="tba-resource-form-fields">{children}</div>
      {footer && <footer>{footer}</footer>}
    </form>
  );
}

