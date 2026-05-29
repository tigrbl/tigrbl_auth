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
    <header className="tigrbl-page-header">
      <div>
        <h1>{title}</h1>
        {description && <p>{description}</p>}
      </div>
      {actions && <div className="tigrbl-page-actions">{actions}</div>}
    </header>
  );
}

