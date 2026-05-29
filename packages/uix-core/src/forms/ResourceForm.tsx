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
    <form {...props} className={`tigrbl-resource-form ${props.className ?? ""}`.trim()}>
      <div className="tigrbl-resource-form-fields">{children}</div>
      {footer && <footer>{footer}</footer>}
    </form>
  );
}

