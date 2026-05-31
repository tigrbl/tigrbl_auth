import type { ReactNode } from "react";

export function DangerZone({
  action,
  children,
  title = "Danger zone"
}: {
  action?: ReactNode;
  children: ReactNode;
  title?: string;
}) {
  return (
    <section className="tigrbl-danger-zone">
      <div>
        <h2>{title}</h2>
        <div className="tigrbl-danger-zone-body">{children}</div>
      </div>
      {action && <div className="tigrbl-danger-zone-action">{action}</div>}
    </section>
  );
}
