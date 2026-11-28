import type { ReactNode } from "react";
import { Button } from "./Button";

export function DetailDrawer({
  actions,
  children,
  description,
  onClose,
  open,
  title
}: {
  actions?: ReactNode;
  children: ReactNode;
  description?: ReactNode;
  onClose: () => void;
  open: boolean;
  title: string;
}) {
  if (!open) return null;

  return (
    <div className="tba-drawer-backdrop" role="presentation">
      <aside aria-modal="true" className="tba-drawer" role="dialog">
        <header className="tba-drawer-header">
          <div>
            <h2>{title}</h2>
            {description && <p>{description}</p>}
          </div>
          <Button onClick={onClose} type="button" variant="subtle">
            Close
          </Button>
        </header>
        <div className="tba-drawer-body">{children}</div>
        {actions && <footer className="tba-drawer-actions">{actions}</footer>}
      </aside>
    </div>
  );
}
