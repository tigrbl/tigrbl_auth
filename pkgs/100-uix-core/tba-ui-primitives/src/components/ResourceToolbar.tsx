import type { ReactNode } from "react";
import { Button } from "./Button";

export function ResourceToolbar({
  actions,
  children,
  createLabel,
  description,
  onCreate,
  title
}: {
  actions?: ReactNode;
  children?: ReactNode;
  createLabel?: string;
  description?: ReactNode;
  onCreate?: () => void;
  title?: string;
}) {
  return (
    <div className="tba-resource-toolbar">
      <div className="tba-resource-toolbar-copy">
        {title && <h2>{title}</h2>}
        {description && <p>{description}</p>}
        {children}
      </div>
      <div className="tba-resource-toolbar-actions">
        {actions}
        {onCreate && (
          <Button onClick={onCreate} type="button">
            {createLabel ?? "Create"}
          </Button>
        )}
      </div>
    </div>
  );
}
