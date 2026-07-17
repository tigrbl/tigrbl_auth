import type { ReactNode } from "react";
import { Button } from "./Button";

export function Modal({
  children,
  onClose,
  open,
  title
}: {
  children: ReactNode;
  onClose: () => void;
  open: boolean;
  title: string;
}) {
  if (!open) return null;
  return (
    <div className="tigrbl-modal-backdrop" role="presentation">
      <section aria-modal="true" className="tigrbl-modal" role="dialog">
        <header>
          <h2>{title}</h2>
          <Button onClick={onClose} type="button" variant="subtle">Close</Button>
        </header>
        {children}
      </section>
    </div>
  );
}

