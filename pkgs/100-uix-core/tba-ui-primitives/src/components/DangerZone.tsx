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
    <section className="tba-danger-zone">
      <div>
        <h2>{title}</h2>
        <div className="tba-danger-zone-body">{children}</div>
      </div>
      {action && <div className="tba-danger-zone-action">{action}</div>}
    </section>
  );
}
