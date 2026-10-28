import type { ReactNode } from "react";

export function PageHeader({
  actions,
  description,
  title
}: {
  actions?: ReactNode;
  description?: string;
  title: string;
}) {
  return (
    <header className="tba-page-header">
      <div>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {actions && <div className="tba-page-actions">{actions}</div>}
    </header>
  );
}

